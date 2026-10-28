---
name: safe-local-run
description: "Reduce memory risk before heavy local Mac workloads: large parquet/CSV loads, ML training, multiprocessing, or data-loading agents, and after a host freeze. Uses RAM preflight, bounded reads, thread caps, and sampled RSS protection. Excludes trivial scripts and remote runs."
license: MIT
compatibility: "Requires macOS, Python 3.10+, Bash, and the run-and-verify companion skill; dataframe checks may require installed pyarrow."
metadata:
  category: engineering
---

# Safe Local Run

Keep large local loads and training within a shared memory budget. CPU and MPS/GPU allocations share unified memory on Apple Silicon. Discover current RAM and available capacity rather than assuming a machine size.

## Rule of thumb — when this is mandatory

Run the preflight and protected runner before a potentially large pandas/parquet/CSV load (about 100 MB on disk already merits inspection), ML training, multiprocessing/joblib, or parallel agents that load local data. Also use it after a host freeze or force-quit when retrying the workload.

Skip for trivial scripts (no big data, no training, sub-second).

## Required companion

Install `run-and-verify` beside this skill. Its shared supervisor owns command execution; without it, the protected runner refuses to launch. Installing this skill does not install the companion automatically.

## Workflow

1. **Preflight** — resolve `preflight` to `scripts/preflight.py` beside this skill and estimate memory against available RAM:
   ```bash
   python3 "$preflight" FILE1.parquet FILE2.parquet
   # With a known estimate instead of files:
   python3 "$preflight" --est-gb 10
   ```
   Verdicts: `SAFE` (run) · `PROJECT-COLUMNS` (load only needed cols) ·
   `SAMPLE/ABORT` (project + sample frac, or stream by chunk — never full-load).
   Honor the verdict. Unknown, nonfinite, or exhausted capacity and missing inputs abort with status 2; do not treat an unavailable measurement as spare RAM. Available RAM fluctuates; re-run if other apps are open.

2. **Apply data discipline** (always, not just on tight verdicts):
   - `pd.read_parquet(path, columns=[...])` — project the few columns you need.
   - Bound reads with row-group/chunk streaming or sampling before materializing a large table. Calling `.sample()` after a full read does not reduce that read's peak memory.
   - `del df; import gc; gc.collect()` between substrates; one table at a time.
   - never `read_parquet` a multi-GB file with no `columns=`.

3. **Run once under the protected supervisor** — resolve `safe_runner` to `scripts/safe_run.sh` beside this skill:
   ```bash
   bash "$safe_runner" --label train --timeout 1800 -- \
     python3 experiments/my_script.py
   ```
   The wrapper sets a default budget of `min(65% RAM, RAM-8GB)`, floored at 2GB; use a smaller `--mem-gb N` when preflight shows less headroom. It preserves BLAS/OMP thread caps, the MPS watermark, and lower scheduling priority, then delegates to the companion `run-and-verify` runner. That one supervisor owns logs, deadline, RSS sampling, cancellation, and process-group cleanup. Do not wrap `safe_run.sh` in `run_logged.sh`, or launch the job without protection when the companion is missing.

4. **Concurrency**: serialize heavy jobs. Do NOT launch multiple data-loading
   jobs/agents in parallel — sum their estimates against ONE budget first. In a
   dynamic workflow, keep data loading in a sequential phase, not a `parallel()`
   fan-out, and tell agents text-only phases must not load parquet.

## Output

Report the preflight verdict and capacity, command, shared `LOG_FILE`, exit metadata, and peak/budget. Require both producer and logger success plus the task's acceptance checks. `MEMORY_LIMIT_EXCEEDED=1` distinguishes an observed RSS breach from a command that independently returns 137; `TIMED_OUT=1` distinguishes the supervisor deadline from an ordinary exit 124. A logger or RSS-monitoring error invalidates the run. Reuse this evidence in `run-and-verify`; do not rerun the same unchanged job for a second report.

After an observed memory breach, reduce the load or budgeted concurrency before any authorized retry. An execution-only request authorizes reporting the failure, not editing the workload. Shared retry limits remain with the parent task.

## Why ulimit does not work here

Address-space limits do not provide the intended resident-memory protection on macOS. RSS polling reduces risk but can miss short allocation spikes; detached processes may escape supervised-group cleanup. Combine the watchdog with bounded input reads and conservative concurrency. Read [macOS resource notes](references/macos-resource-notes.md) when tuning budgets or investigating a kill.

## Execution ownership

Keep resource estimation and Mac policy here. Keep the shared logging, timeout, signal handling, and RSS monitor in `run-and-verify/scripts/run_logged.sh`. Both skills must be installed as siblings; missing supervision fails closed. Revisit a standalone runner package only if these skills need independent distribution.
