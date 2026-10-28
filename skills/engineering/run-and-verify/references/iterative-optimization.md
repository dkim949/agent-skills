# Iterative optimization

Use only when the user requests repeated optimization of a measurable target. A one-off fix or failed-test repair follows the ordinary execution workflow. This procedure does not schedule future runs or expand a domain-specific experiment into a general optimizer.

When a native Goal is active, this procedure still owns experiment selection and its cumulative attempt budget. Goal continuation resumes the same procedure; it does not add another repair or optimization loop.

1. Set the target, representative workload, direction of improvement, correctness checks, authorized scope, and stopping conditions. Use the user's resource limits; otherwise state a proportionate time, compute, or attempt budget based on the cost of a baseline run. Ask only when a material goal, cost, or authorization cannot be resolved. Avoid a universal attempt floor or time cap.
2. Validate the measurement using `performance-measurement.md` in this reference directory for execution-performance claims. Check that contrasting relevant workloads produce a sensible signal. Record a baseline and passing correctness checks, then fix the measurement command, data, and configuration. A necessary measurement change starts a newly documented baseline; it cannot be compared as if nothing changed.
3. Form one mechanism-based hypothesis per attempt. Preserve the starting state and identify the exact edits owned by that attempt so an unsuccessful change can be removed without touching the user's or another task's work.
4. Apply the scoped change, measure with the fixed procedure, and run the correctness checks. Keep it only when the claimed improvement is supported and correctness holds; otherwise undo only that attempt's edits using an authorized method. If ownership is unclear, stop and resolve it. Do not multiply the ordinary repair-retry limit inside every optimization attempt.
5. Record the hypothesis, evidence, result, and keep/undo reason in an existing result table or task record, or in the response when no saved record is needed. Reuse that evidence in a handoff rather than creating competing logs.
6. Stop when the target is met and confirmed, the budget is reached, a material blocker appears, or remaining ideas do not justify their cost. Keep the target unchanged; report an unmet target honestly. Recompare the final candidate against the original baseline with fresh measurements to check that selecting the best attempt did not merely select noise.
7. Return baseline versus final, checks passed/failed, attempts kept/undone, evidence locations, and the stopping reason.

Run directly unless team work is explicitly requested or other applicable instructions authorize delegation. Parallel attempts require separate owned work areas. Commits, publishing, external writes, and background scheduling retain their own authorization boundaries.

Source: [pstack hillclimb](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md). This optional procedure adds measured optimization to execution verification without another top-level skill. Domain-specific experiment protocols remain with their existing owner.
