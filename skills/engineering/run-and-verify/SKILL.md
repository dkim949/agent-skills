---
name: run-and-verify
description: "Run project checks and verify their evidence. Use for tests, builds, scripts, lint, or measured performance; read the testing reference when adding tests. Verification-only requests do not authorize implementation changes."
license: MIT
compatibility: "Requires Python 3.10+ and Bash for the bundled command supervisor."
metadata:
  category: engineering
---

# Run and Verify

## When to use

Use when code or a command needs execution-based verification. Before memory-heavy local macOS runs, use `safe-local-run` when installed. It is an optional macOS resource guard. On other hosts, or when it is absent, use the environment's existing verified resource policy and disclose unavailable protection before heavy execution. Protected resources and external writes retain their existing authorization requirements.

## Routing

- For measured speedup, regression, or choosing options by performance, read [Performance measurement](references/performance-measurement.md).
- For explicitly requested repeated optimization of a measurable target, read [Iterative optimization](references/iterative-optimization.md). It owns the attempt loop; the execution checks below still apply.
- For explicitly requested work that should continue across turns until a verified outcome, use `goal-loop` when installed. It supplies native Goal continuation; this skill supplies execution evidence. Keep one shared attempt allowance rather than nesting repair loops.
- When adding or revising tests, read [Testing principles](references/testing-principles.md). It is also the shared test-quality reference for `diagnosing-bugs`.
- Ordinary execution of existing checks needs no additional reference.

## Workflow

1. Discover this project's commands from README/CONTRIBUTING, checked-in build scripts, package or test configuration, and CI. Prefer the repository's wrapper and environment over guessed global commands. Identify focused checks and the broader checks relevant to the change. Honor a requested lint-only or execution-only scope; report what it cannot establish. Missing tooling or a network-dependent suite is an unrun check, not a pass or permission to install tools.
2. State task-specific success criteria and the evidence each needs before executing. Tests/build/lint need their relevant successful output and exit status; a script also needs its expected artifacts or behavior. A running training process or a short decreasing-loss streak cannot establish model quality: use the experiment's own evaluation protocol. Check relevant existing thresholds without inventing coverage targets or weakening them.
3. Reuse existing evidence when the checked implementation, tests, command, environment, and inputs remain applicable. Rerun affected checks after a relevant change or when evidence is stale, incomplete, or not trustworthy. A worker's success message alone is insufficient. Keep one evidence record with the command, scope, relevant revision/inputs, outcome, and log; avoid duplicate reports or unchanged reruns.
4. Run in the intended directory and environment using one supervisor. For ordinary commands, resolve `runner` to `scripts/run_logged.sh` beside this skill. For memory-heavy local macOS work with `safe-local-run` installed, use it directly; its wrapper delegates to the same runner with memory limits. Otherwise follow the resource policy above. Do not nest the two wrappers. Pass executable and arguments separately; never use `eval` or interpolate an untrusted request into a shell command.

```bash
bash "$runner" --timeout 300 -- \
  python -m pytest tests/test_model.py -v --tb=short
```

The runner logs complete command output, checks command and logger status, handles cancellation and process-group cleanup, and applies a deadline while waiting for both. Its optional RSS monitor is used by `safe-local-run`. Adjust limits for the task; sampled memory protection is not an operating-system sandbox.

5. Wait for completion. Require wrapper status 0, `PRODUCER_EXIT_CODE=0`, `LOGGER_EXIT_CODE=0`, and all task-specific criteria. `TIMED_OUT=1` identifies a deadline; status 124 alone does not. `MEMORY_LIMIT_EXCEEDED=1` identifies an observed RSS breach; status 137 alone does not. Cancellation reports `CANCEL_SIGNAL`. Logging or monitoring failures invalidate the run.
6. Inspect the output and relevant test/check configuration changes before claiming success. Surface skipped/deleted tests, weaker assertions, suppressed errors, relaxed thresholds, or disabled gates; a legitimate change needs its own rationale and acceptance. A green result obtained by weakening the agreed check is not proof of the original requirement. Do not infer build, end-to-end behavior, or complete requirements from a narrower passing check.
7. Report failure with evidence and likely cause. An execution-only request ends with the result; implementation changes require authorization. For an authorized repair, use the active task's shared attempt allowance, or at most three retries when none exists. Reuse the diagnosis rather than starting nested repair loops. Stop on an unmet limit, material blocker, or repeated lack of progress, and preserve the unmet criteria.

## Output

Report target, command, criteria, outcome, attempts, changes made, and evidence or logs. Distinguish unrun checks from passes.

## Boundaries

- Do not change success criteria after execution to make a run pass.
- Skip lint if its tool is unavailable; report the omission. Do not use automatic lint fixes without authorization.
- Obtain the required exact authorization before destructive side effects or protected-resource changes. This skill does not grant permissions.

## Provenance and continuation

This package maintains the verification workflow and shared command supervisor. The optional performance, optimization, and testing references identify their design sources; their applicable notices accompany this skill.

The repair and optimization loops are agent instructions. The shared runner owns one command's logging, deadline, cancellation, and optional RSS monitoring; `safe-local-run` owns local memory policy and thread caps. Neither starts another model turn. Native Goal continuation belongs to `goal-loop`.
