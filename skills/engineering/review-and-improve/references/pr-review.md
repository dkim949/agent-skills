# Pull request and code review

Use for a requested PR review or a local diff. Reading a PR does not authorize posting comments, submitting a review, merging, or changing its state.

## Establish the exact target

Identify the repository and PR or base/head comparison from the request. Inspect the description, changed files, diff, and relevant surrounding code. Use connected tools or explicit commands such as `gh pr view <number> --repo <owner/repo>` and `gh pr diff <number> --repo <owner/repo>` when available. Never silently fall back to a different branch or suppress a failed diff fetch.

## Inspect what can change behavior

- Correctness: trace input, state changes, outputs, and callers; check boundaries, error handling, data types, and compatibility.
- Data and access: check exposed secrets, access checks, unsafe input handling, unintended writes, and data loss where the diff creates a concrete risk.
- Tests: check whether meaningful changed behavior and failure cases are covered. Inspect actual results; code inspection cannot establish passing tests.
- Integration: follow the project's documented architecture, formatting, lint, typing, and build conventions. Do not impose unrelated framework or company conventions.
- Performance: require a workload and measurement for performance claims; do not infer a speedup from shorter code.
- ML or analysis changes: compare data, splits, targets, preprocessing, evaluation, uncertainty, and possible leakage. Reused or overlapping inputs need an empirical baseline comparison, not a universal overlap cutoff.

Check all relevant call sites when signatures change and downstream logging or visualization when output fields change. Use the narrowest checks that resolve material uncertainty, within the existing execution permissions.

## Report

For each actionable finding, name the trigger, observed or predicted failure, supporting file/line, and a fix or discriminating check. Separate confirmed defects from unverified concerns. If no actionable issue is found, say so and identify any important untested area. Match the conversation language; use the destination's required language for a saved or posted review.
