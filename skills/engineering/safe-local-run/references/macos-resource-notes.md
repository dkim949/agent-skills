# macOS resource-control notes

Background for `safe-local-run`. Read when tuning budgets or debugging a kill.

## Why `ulimit` cannot bound memory on macOS

- `ulimit -v` (virtual address space) and `ulimit -d` (data segment) are
  effectively ignored on macOS. The kernel lazily commits pages and reserves
  large virtual ranges (BLAS, Metal, Python arenas), so an address-space cap
  either fires immediately on a process that uses little real memory, or never
  fires at all. Linux cgroups have no macOS equivalent for a user shell.
- The local guard samples process-tree RSS and terminates the supervised
  process group after an observed breach. `safe_run.sh` applies resource policy
  and delegates this work to the shared `run-and-verify` runner; it does not run
  a second watchdog. Sampling can miss transient spikes and is not a sandbox.
- `RLIMIT_RSS` exists in the headers but is not enforced by the macOS kernel.

## Unified memory

Apple Silicon shares one memory pool across CPU and GPU/MPS. There is no
separate VRAM budget — a PyTorch MPS tensor and a pandas DataFrame compete for
the same GB. Budget the whole run against total RAM, not "CPU RAM + GPU RAM".

When the system runs low it compresses memory then swaps to SSD; swap thrash is
what makes the machine unresponsive and triggers force-quit. Keep peak RSS below
~65% of total so the OS and other open apps keep their working sets resident.

## Thread / library env caps

Oversubscribed BLAS threads inflate both CPU contention and transient memory.
`safe_run.sh` sets these to `ncpu/2` unless already exported:

| var | controls |
|---|---|
| `OMP_NUM_THREADS` | OpenMP (LightGBM, sklearn, numpy) |
| `OPENBLAS_NUM_THREADS` | OpenBLAS |
| `MKL_NUM_THREADS` | Intel MKL (rare on ARM) |
| `VECLIB_MAXIMUM_THREADS` | Apple Accelerate / vecLib |
| `NUMEXPR_NUM_THREADS` | numexpr / pandas eval |
| `PYTORCH_MPS_HIGH_WATERMARK_RATIO` | MPS allocator ceiling (set 0.6) |

LightGBM: also pass `num_threads` in params. PyTorch DataLoader: keep
`num_workers` small (2–4); each worker forks and copies memory.

## Tuning the budget

- Default `min(65% total, total-8GB)`: M4 24GB → 15.6GB; M2 Max 32GB → 20.8GB.
- Tighten with `--mem-gb` when other heavy apps are open (preflight prints live
  `available` RAM — if it is already low, lower the budget).
- `--timeout` is a wall-clock backstop for hangs. Set it to a few times the
  expected runtime.
- `--poll` default 2s. Lower to 1s for fast-allocating jobs; the watchdog can
  only react at poll granularity, so a single huge alloc between polls can still
  spike — pair with column projection so no single load is catastrophic.
- The shared runner bounds each `ps` sample and fails the run if monitoring
  fails; it does not silently interpret missing monitoring as zero memory.
  It reports `PEAK_RSS_KB`, `MEMORY_LIMIT_KB`, and explicit breach/timeout markers.
  Job and logger exit status are checked separately, including cancellation
  and a child keeping the output pipe open after the main command exits.

## Parquet memory estimate

`preflight.py` uses pyarrow metadata (`row_group.total_byte_size` summed ×2.2)
when pyarrow is importable, else on-disk size ×6 (compressed parquet blowup).
The heuristic is deliberately conservative — prefer a false SAMPLE verdict over
a force-quit. Run preflight inside the ML venv to get the precise pyarrow path.

## Reading big parquet safely

```python
import pyarrow.parquet as pq
pf = pq.ParquetFile(path)
# Synthetic example columns; choose the fields needed by the actual task.
cols = ["record_id", "value", "category"]
# whole projected table (if it fits):
df = pf.read(columns=cols).to_pandas()
# or stream by row group (bounded peak):
import gc
for i in range(pf.num_row_groups):
    chunk = pf.read_row_group(i, columns=cols).to_pandas()
    ...  # aggregate incrementally
    del chunk; gc.collect()
```
