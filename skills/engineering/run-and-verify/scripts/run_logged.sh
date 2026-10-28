#!/usr/bin/env bash
# Become the controller so signals to this PID also clean up the command.
exec python3 -c '
import argparse
import math
import os
import signal
import subprocess
import sys
import tempfile
import time
from typing import Optional, Union

parser = argparse.ArgumentParser(description="Run argv with a deadline and full output log.")
parser.add_argument("--timeout", type=float, default=300)
parser.add_argument("--log")
parser.add_argument("--mem-gb", type=float)
parser.add_argument("--poll", type=float, default=2)
parser.add_argument("--label", default="job")
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command[1:] if args.command[:1] == ["--"] else args.command
if not command or not math.isfinite(args.timeout) or args.timeout <= 0:
    parser.error("a command and a positive finite deadline are required")
if not math.isfinite(args.poll) or args.poll <= 0:
    parser.error("--poll must be positive and finite")
if args.mem_gb is not None and (not math.isfinite(args.mem_gb) or args.mem_gb <= 0):
    parser.error("--mem-gb must be positive and finite")
memory_limit_kb = int(args.mem_gb * 1048576) if args.mem_gb is not None else None
if memory_limit_kb is not None and memory_limit_kb < 1:
    parser.error("--mem-gb must allow at least one KiB")
log_file = args.log
if log_file is None:
    log_fd, log_file = tempfile.mkstemp(prefix="run-and-verify.", dir="/tmp")
    os.close(log_fd)
print(f"LOG_FILE={log_file}", flush=True)

producer = None
logger = None
cancel_signal = 0
timed_out = False
memory_exceeded = False
monitor_failed = False
logger_failed = False
peak_rss_kb = 0
setup_code = 0

def handle_signal(signum: int, _frame: object) -> None:
    global cancel_signal
    if not cancel_signal:
        cancel_signal = signum

def stop_group(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        # macOS can return EPERM after TERM has already emptied the group.
        # Ignore it only after confirming that no live group member remains.
        groups = subprocess.check_output(
            ["ps", "-axo", "pgid=,stat="], text=True, timeout=1,
        )
        if any(
            int(group) == process.pid and not state.startswith("Z")
            for group, state in (line.split() for line in groups.splitlines() if line.strip())
        ):
            raise
    process.wait()

def exit_code(process: Optional[subprocess.Popen]) -> Union[int, str]:
    if process is None:
        return "NOT_RUN"
    code = process.returncode
    return code if code >= 0 else 128 - code

def tree_rss_kb(root_pid: int, timeout: float) -> int:
    output = subprocess.check_output(
        ["ps", "-axo", "pid=,ppid=,pgid=,rss="], text=True,
        stderr=subprocess.DEVNULL, timeout=timeout,
    )
    rows = [tuple(map(int, line.split())) for line in output.splitlines() if line.strip()]
    owned = {root_pid} | {pid for pid, _parent, group, _rss in rows if group == root_pid}
    while True:
        descendants = owned | {pid for pid, parent, _group, _rss in rows if parent in owned}
        if descendants == owned:
            break
        owned = descendants
    return sum(rss for pid, _parent, _group, rss in rows if pid in owned)

for signal_number in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
    signal.signal(signal_number, handle_signal)
deadline = time.monotonic() + args.timeout
next_memory_check = time.monotonic()
try:
    producer = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True
    )
    logger = subprocess.Popen(
        ["tee", "-a", log_file], stdin=producer.stdout, start_new_session=True
    )
    producer.stdout.close()
    while True:
        if cancel_signal:
            break
        if producer.poll() is not None and logger.poll() is not None:
            break
        if logger.poll() not in (None, 0):
            logger_failed = True
            break
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            break
        if memory_limit_kb is not None and time.monotonic() >= next_memory_check:
            try:
                rss_kb = tree_rss_kb(producer.pid, min(1, remaining))
                peak_rss_kb = max(peak_rss_kb, rss_kb)
                if rss_kb > memory_limit_kb:
                    memory_exceeded = True
                    break
            except (OSError, subprocess.SubprocessError, ValueError) as error:
                monitor_failed = True
                print(f"Memory monitoring failed: {error}", file=sys.stderr)
                break
            next_memory_check = time.monotonic() + args.poll
        time.sleep(min(0.05, remaining))
except FileNotFoundError:
    print("Executable or logger not found.", file=sys.stderr)
    setup_code = 127
except PermissionError:
    print("Executable or logger permission denied.", file=sys.stderr)
    setup_code = 126
except OSError as error:
    print(f"Execution setup failed: {error}", file=sys.stderr)
    setup_code = 1
finally:
    if producer is not None and producer.stdout is not None:
        producer.stdout.close()
    if timed_out or cancel_signal or setup_code or memory_exceeded or monitor_failed or logger_failed:
        if producer is not None:
            stop_group(producer)
        if logger is not None:
            try:
                logger.wait(timeout=1)
            except subprocess.TimeoutExpired:
                stop_group(logger)

producer_code = exit_code(producer)
logger_code = exit_code(logger)
if cancel_signal:
    result = 128 + cancel_signal
    print(f"CANCEL_SIGNAL={cancel_signal}", flush=True)
elif timed_out:
    result = 124
    print("TIMED_OUT=1", flush=True)
elif memory_exceeded:
    result = 137
    print("MEMORY_LIMIT_EXCEEDED=1", flush=True)
elif monitor_failed:
    result = 1
    print("MEMORY_MONITOR_ERROR=1", flush=True)
elif setup_code:
    result = setup_code
elif logger_failed:
    result = logger_code
else:
    result = producer_code if producer_code else logger_code
print(
    f"PRODUCER_EXIT_CODE={producer_code}\nLOGGER_EXIT_CODE={logger_code}\nEXIT_CODE={result}",
    flush=True,
)
if memory_limit_kb is not None:
    print(f"PEAK_RSS_KB={peak_rss_kb}\nMEMORY_LIMIT_KB={memory_limit_kb}", flush=True)
    print(
        f"[safe_run] done {args.label} rc={result} "
        f"peak={peak_rss_kb / 1048576:.1f}GB / {args.mem_gb:.1f}GB budget",
        file=sys.stderr, flush=True,
    )
sys.exit(result)
' "$@"
