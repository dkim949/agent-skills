---
name: multi-agent-coordination
description: "Coordinate work when the user explicitly requests a team, parallel agents, delegation, a red team, a debate, or a task graph. Shared rules for the current lead; ordinary work and questions about teams do not launch agents."
license: MIT
metadata:
  category: engineering
---

# Multi-agent coordination

Use this whenever an authorized task delegates work. A request to work as a team is sufficient; a slash command is unnecessary. A question about teams, a skill installation, or an ordinary review is not a launch request. If no useful independent work exists, explain that and handle it directly.

The current lead owns decomposition, dispatch, integration, and the answer. Read these instructions in the lead's context; do not spawn another coordinator or recursively build a hierarchy. Workers report evidence and may recommend follow-up; the lead decides whether further delegation fits the authorized scope.

## Choose the smallest useful pattern

| Need | Pattern |
|---|---|
| Independent questions or disjoint implementation areas | Parallel workers, then lead integration. |
| A large reading task with a compact useful result | One bounded research worker. |
| Tasks that consume earlier outputs | Ready tasks only; verify prerequisites before launching dependents. |
| Explicit team review, red team, or debate | `review-and-improve` owns criteria and challenge modes; this skill owns delegation. |

Ordinary domain work keeps its existing skill. `goal-loop` alone owns requested continuation; `run-and-verify` owns execution evidence. Do not create duplicate coordinators, repair loops, or approval steps.

## Coordinate

1. Frame the outcome and acceptance. Give each worker a distinct question or owned files, necessary inputs, constraints, expected output, and a completion check. Tell editing workers they share the workspace and must preserve others' changes. Use read-only reviewers unless edits were requested.
2. Select the current host's verified backend below. Keep the current authorized account and data boundary. Resolve the model and supported effort from actual available tools or profiles before creation; choose for task difficulty and record the reason. Deliberate inheritance is valid when parent settings are resolved. Never silently change account, provider, or global settings. Follow [account and content boundaries](references/account-boundaries.md) plus any routing policy configured by the current environment. Device-specific routes and credentials are never part of this portable skill.
3. Launch independent ready work before waiting, within actual concurrency limits. Usually two or three focused workers suffice. Prevent overlapping file ownership; sequential dependent work need not get another agent just to paraphrase the previous result.
4. Use native completion/state tools. Inspect important evidence and outputs before accepting them; worker completion or consensus is not acceptance. Keep claims, assumptions, and unrun checks separate. Verify prerequisites before a dependent launch.
5. Integrate in the lead. Resolve disagreements with evidence or a discriminating check, not majority vote. Reuse the same worker for a related correction when useful; inspect ambiguous state before retrying. Explain remaining uncertainty and the final decision.

Show a compact plan and meaningful progress: task/owner, dependency if any, chosen model/effort, execution state, and verified result or blocker. Reuse task records; do not create a second reporting system. Distinguish selected, inherited, and observed runtime settings, and state any verification limit. A simple review does not need a durable graph file.

## Host adapters

| Actual delegation backend | Read |
|---|---|
| Native Codex, Claude Code, or another verified native subagent API | [Native subagents](references/native-subagents.md) |
| Orca-managed Tasks/Dispatch | [Orca execution](references/orca.md) and its installed version-matched `orchestration` guide |
| Paseo-managed agents | [Paseo execution](references/paseo.md) and its installed `paseo` guide |
| No suitable delegation tool | Disclose the limit; offer a direct review or unexecuted plan without claiming a team ran. |

Identify the actual backend separately from the enclosing app. Native subagents inside another app still follow the native adapter. Installations and model menus do not prove available execution or account access. Gemini discovery of this skill does not establish a delegation API; inspect that host's actual tools.

Read [dependent tasks and recovery](references/task-graphs.md) only when dependencies, persistence, restart recovery, or requested human checkpoints matter. Native coordinator-managed ordering is not a durable scheduler. A request to pause stops affected work; a goal, reviewer agreement, synthetic feedback, or silence cannot grant user approval.

## Design basis

[Addy's orchestration patterns](https://github.com/addyosmani/agent-skills/blob/main/references/orchestration-patterns.md) inform independent fan-out, compact research isolation, lead-owned integration, and avoiding extra routing personas. These are adapted principles, not copied platform restrictions: verify each host's current tools. This local successor to `graph-engineering` broadens the trigger while preserving its advanced procedures and earlier test evidence.
