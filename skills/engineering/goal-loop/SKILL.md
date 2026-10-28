---
name: goal-loop
description: "Define and run a verifiable goal when the user asks to keep working until an outcome is reached, repeat improvements, or prepare an unattended run. Questions or setup requests stay read-only with respect to goal activation; ordinary checks use run-and-verify."
license: MIT
metadata:
  category: engineering
---

# Goal Loop

Turn an explicitly requested continuing task into a bounded work-and-check cycle. This skill defines the working method; the host's native Goal supplies continuation between turns. Installing or discussing it starts no Goal, schedule, worker, or background process.

## Establish the finish line

Reuse the user's decisions and current context. State the outcome, inspectable proof, owned files or repositories, constraints, and stopping conditions. Resolve only missing decisions that materially affect the work. A useful contract fits in a few sentences:

> Complete <outcome>, demonstrated by <checks and expected observations>. Work within <scope>; preserve <constraints>. After each attempt, inspect the evidence and choose the next justified change. Stop on verified completion, the agreed limit, or a blocker requiring unavailable input or authorization; report unmet criteria honestly.

Use requested limits. Otherwise state a modest, task-appropriate attempt allowance based on the cost of a baseline check. Distinguish a conversational attempt/time limit from a runtime-enforced cap. Add a native token budget only when the user explicitly specifies one.

## Choose continuation

Read [Native Goal execution](references/native-goals.md) for the current host. Check actual tools or command support before activation. Explain the selected mechanism and its limits briefly.

Verify the actual Goal state after activation. A model saying it activated a Goal, or a command exiting successfully, does not establish automatic continuation. Confirm that the chosen runtime can start the next turn; one-shot CLI execution may end while its Goal remains active.

- **Goal-based work:** continue after a turn toward the stated outcome. Prefer the host's native Goal; keep one continuation owner.
- **Timed work:** use the host's scheduling tools only when the user asks for intervals, later wakeups, monitoring, or recurring work. A Goal is not a timer.
- **Parallel work:** use `multi-agent-coordination` when the user requests a task graph or team. A single Goal does not itself authorize extra agents.

If activation is unavailable, provide the supported command or a ready-to-use contract. Label it prepared, not running. Work within the current turn when authorized, while disclosing that automatic continuation has not been activated.

## Work, check, decide

1. Establish a baseline using the actual acceptance checks. Preserve relevant existing work and keep the finish line fixed.
2. Choose one justified next change, implement it within scope, and inspect the result. Use `run-and-verify` when installed, or the project's existing check commands. Its logged runner bounds individual commands; it does not bound the whole Goal.
3. Compare evidence with every acceptance criterion. A passing test subset or a completion phrase cannot substitute for missing evidence. Repair real failures; preserve meaningful tests and benchmarks.
4. Track attempts across turns. Count verification repairs inside the same allowance rather than multiplying nested retry budgets. For measured optimization, its experiment procedure owns candidate selection; this skill only supplies the contract and continuation.
5. Continue only while the target is unmet and the next attempt is justified within scope and limits. On completion, a limit, repeated lack of progress, or a material blocker, report the evidence and follow the host's supported lifecycle rules. An exhausted limit is not success.

For work spanning turns or an unattended run, update one existing task record with the contract, attempts used, latest evidence, current state, and next action. Create a small record in the owned project only when none exists. Keep sensitive data out of summaries. After an interruption, inspect actual Goal/process state and artifacts before resuming; a saved note does not restart anything.

## Handover

Return the achieved and unmet criteria, relevant changes and locations, checks actually run, attempt count, stopping reason, and remaining decisions. Surface enough evidence for the user to understand the result without replaying the session. Host permissions, account routing, and external-action authorization remain in force throughout the loop.
