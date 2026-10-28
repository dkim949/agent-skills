#!/usr/bin/env python3
"""Preflight resource check before a heavy local run.

Checks available RAM and, for any parquet/csv paths given, estimates in-memory
size and returns a verdict: SAFE / PROJECT-COLUMNS / SAMPLE / ABORT, with a
recommended sample fraction and memory budget.

Usage:
  preflight.py [--budget-gb N] [--est-gb N] [FILE ...]

Dependency-light: uses sysctl/vm_stat for RAM (psutil if present), pyarrow for
parquet metadata if present, else falls back to on-disk size x blowup factor.
No data is loaded into memory.
"""
import argparse
import math
import os
import shutil
import subprocess
import sys

GB = 1073741824


def total_ram_gb() -> float | None:
    try:
        out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True)
        return int(out.strip()) / GB
    except Exception:
        try:
            import psutil
            return psutil.virtual_memory().total / GB
        except Exception:
            return None


def available_ram_gb() -> float | None:
    """Best-effort free+inactive+speculative memory on macOS."""
    try:
        import psutil
        return psutil.virtual_memory().available / GB
    except Exception:
        pass
    try:
        out = subprocess.check_output(["vm_stat"], text=True)
        page = 4096
        first = out.splitlines()[0]
        if "page size of" in first:
            page = int(first.split("page size of")[1].split("bytes")[0].strip())
        free = inactive = spec = 0
        for line in out.splitlines():
            if line.startswith("Pages free:"):
                free = int(line.split(":")[1].strip().rstrip("."))
            elif line.startswith("Pages inactive:"):
                inactive = int(line.split(":")[1].strip().rstrip("."))
            elif line.startswith("Pages speculative:"):
                spec = int(line.split(":")[1].strip().rstrip("."))
        return (free + inactive + spec) * page / GB
    except Exception:
        return None


def parquet_est_gb(path: str) -> tuple[float, int, int]:
    """Estimate in-memory pandas size (GB), rows, cols. Conservative."""
    try:
        import pyarrow.parquet as pq
        md = pq.ParquetFile(path).metadata
        uncompressed = sum(
            md.row_group(i).total_byte_size for i in range(md.num_row_groups)
        )
        # pandas overhead vs parquet-uncompressed encoding: ~1.5-2.5x; use 2.2x.
        return uncompressed * 2.2 / GB, md.num_rows, md.num_columns
    except Exception:
        # fallback: on-disk compressed size x blowup (parquet ~3-6x compressed).
        size = os.path.getsize(path)
        return size * 6.0 / GB, -1, -1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--budget-gb", type=float, default=None,
                    help="memory budget; default min(65%% RAM, RAM-8)")
    ap.add_argument("--est-gb", type=float, default=None,
                    help="manual in-memory estimate if no files given")
    args = ap.parse_args()
    if args.est_gb is not None and (not math.isfinite(args.est_gb) or args.est_gb < 0):
        ap.error("--est-gb must be finite and nonnegative")
    if args.budget_gb is not None and (not math.isfinite(args.budget_gb) or args.budget_gb <= 0):
        ap.error("--budget-gb must be positive and finite")

    total = total_ram_gb()
    avail = available_ram_gb()
    if avail is None or not math.isfinite(avail) or avail <= 0:
        print("verdict: ABORT — available RAM must be known, positive, and finite.")
        return 2
    if args.budget_gb is not None:
        budget = args.budget_gb
    else:
        if total is None or not math.isfinite(total) or total <= 0:
            print("verdict: ABORT — cannot determine a memory budget from host RAM.")
            return 2
        budget = min(total * 0.65, total - 8)
        budget = max(budget, 2.0)

    total_text = f"{total:.1f} GB" if total is not None else "unknown"
    print(f"host RAM:      {total_text} total, {avail:.1f} GB available")
    print(f"safe budget:   {budget:.1f} GB  (sampled RSS threshold; transient peaks may exceed it)")

    est = args.est_gb if args.est_gb is not None else 0.0
    for f in args.files:
        if not os.path.isfile(f):
            print(f"verdict: ABORT — input file is missing or not a regular file: {f}")
            return 2
        e, rows, cols = parquet_est_gb(f) if f.endswith(".parquet") else (
            os.path.getsize(f) * 4.0 / GB, -1, -1)
        est += e
        meta = f"{rows:,} rows x {cols} cols" if rows >= 0 else "size-heuristic"
        print(f"  {os.path.basename(f):<45} ~{e:5.1f} GB in pandas  ({meta})")

    if not math.isfinite(est) or est < 0:
        print("verdict: ABORT — total estimate must be finite and nonnegative.")
        return 2
    if est == 0:
        print("\nverdict: NO ESTIMATE — pass files or --est-gb. Default to caution.")
        return 0

    print(f"\ntotal estimate: ~{est:.1f} GB in memory")
    headroom = min(budget, avail)

    if est <= headroom * 0.5:
        print(f"verdict: SAFE — fits well under {headroom:.1f} GB. Run via safe_run.sh.")
    elif est <= headroom:
        print(f"verdict: PROJECT-COLUMNS — tight ({est:.1f}/{headroom:.1f} GB). "
              f"Load only needed columns; run via safe_run.sh with sampled RSS monitoring.")
    else:
        # Round down at the displayed precision so the recommendation stays within headroom.
        frac = math.floor(headroom * 0.5 / est * 1000) / 1000
        if frac == 0:
            print("verdict: ABORT — required sample fraction is below 0.001; "
                  "stream by row-group/chunk. Do NOT full-load.")
            return 2
        print(f"verdict: SAMPLE/ABORT — estimate {est:.1f} GB > {headroom:.1f} GB headroom.")
        print(f"  -> use columns= projection AND sample frac<= {frac:.3f}, "
              f"or stream by row-group/chunk. Do NOT full-load.")
    if not shutil.which("nice"):
        print("  (note: safe_run.sh expects standard macOS coreutils)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
