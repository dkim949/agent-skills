#!/usr/bin/env bash
# Apply local resource policy, then use the shared logged command supervisor.
set -eu

MEM_GB=""
TIMEOUT=3600
LABEL="job"
POLL=2
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mem-gb|--timeout|--label|--poll)
      [[ $# -ge 2 ]] || { echo "safe_run: $1 requires a value" >&2; exit 2; }
      case "$1" in
        --mem-gb) MEM_GB="$2";;
        --timeout) TIMEOUT="$2";;
        --label) LABEL="$2";;
        --poll) POLL="$2";;
      esac
      shift 2;;
    --) shift; break;;
    *) echo "safe_run: unknown arg $1" >&2; exit 2;;
  esac
done
[[ $# -gt 0 ]] || { echo "safe_run: no command after --" >&2; exit 2; }

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
RUNNER="$SCRIPT_DIR/../../run-and-verify/scripts/run_logged.sh"
[[ -f "$RUNNER" ]] || { echo "safe_run: install the companion run-and-verify skill; refusing an unprotected run" >&2; exit 2; }

TOTAL_BYTES=$(sysctl -n hw.memsize 2>/dev/null) || { echo "safe_run: cannot determine host RAM; use the platform-specific resource policy" >&2; exit 2; }
TOTAL_GB=$(awk -v b="$TOTAL_BYTES" 'BEGIN{printf "%.1f", b/1073741824}')
if [[ -z "$MEM_GB" ]]; then
  MEM_GB=$(awk -v t="$TOTAL_GB" 'BEGIN{a=t*0.65; b=t-8; m=(a<b)?a:b; if(m<2)m=2; printf "%.1f", m}')
fi
CORES=$(sysctl -n hw.ncpu 2>/dev/null || echo 4)
CAP=$(awk -v c="$CORES" 'BEGIN{h=int(c/2); if(h<1)h=1; print h}')
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-$CAP}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-$CAP}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-$CAP}"
export VECLIB_MAXIMUM_THREADS="${VECLIB_MAXIMUM_THREADS:-$CAP}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-$CAP}"
export PYTORCH_MPS_HIGH_WATERMARK_RATIO="${PYTORCH_MPS_HIGH_WATERMARK_RATIO:-0.6}"

echo "[safe_run] label=$LABEL host=${TOTAL_GB}GB budget=${MEM_GB}GB timeout=${TIMEOUT}s threads=$CAP" >&2
exec bash "$RUNNER" --mem-gb "$MEM_GB" --timeout "$TIMEOUT" --poll "$POLL" --label "$LABEL" -- nice -n 10 "$@"
