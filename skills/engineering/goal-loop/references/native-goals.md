# Native Goal execution

Use the current host's own capability. The shared skill defines scope and proof; it neither installs a loop engine nor makes Goal lifecycles identical across clients.

## Codex

- Inspect the available Goal tools. When the user explicitly requests activating a Goal, use the exposed creation tool and inspect the returned objective/status. Read existing Goal state first when there may already be an objective; do not replace unrelated work.
- Pass a token budget only when the user explicitly requests a numeric token budget. An instruction to stop after several attempts is not a token budget.
- When a command surface is needed, the documented commands are `/goal <objective>`, `/goal`, `/goal pause`, `/goal resume`, and `/goal clear`. Ordinary assistant text containing one of these commands does not execute it.
- Goals persist with a thread and may continue at idle boundaries. Completion requires evidence; lifecycle changes and blocker timing must follow the actual tool contract. Budget exhaustion and a blocker do not mean completion.
- Verify continuation in the selected runtime, not only Goal activation. A local Codex 0.164.0 smoke test found that `codex exec` persisted an active Goal but exited after its first turn. Do not promise unattended continuation through that one-shot route. The app-server route was verified with one initial `turn/start`, two automatically sequenced turns, and a final `complete` Goal state.
- For a custom app-server client, use documented `thread/goal/set` and `thread/goal/get` responses/notifications as state evidence. Inject the skill through a supported skill input when appropriate. Keep the connection alive for continuation events; do not write private state databases or send a second work prompt and describe it as automatic continuation.
- A Goal does not provide an always-on machine, bypass permissions, or prove continuation after an app exit, sleep, or authentication failure.

Sources: [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) and [app-server protocol](https://learn.chatgpt.com/docs/app-server). The version-specific execution observation is from a local two-turn smoke test on 2026-10-27; recheck after runtime changes.

## Claude Code

Prefer the built-in `/goal <condition>` over adding a stop-hook plugin. Check command availability and applicable hook/trust restrictions; installed version alone does not establish policy access. If the current agent has no supported Goal-activation tool, return one exact command for the user to submit. Do not claim to activate a built-in command by mentioning it in a response or by editing settings/state files.

```text
/goal Implement the agreed feature within its owned files, demonstrate every acceptance check, and report the evidence. Stop and report unmet criteria after five implementation attempts or on a blocker needing unavailable input or authorization.
```

- `/goal` shows state; `/goal clear` removes the active condition. Setting another condition replaces an active one, so inspect state before replacing it.
- The native evaluator reads the conversation; it does not independently run checks. Surface command results and inspected artifacts before declaring success.
- In headless tests, make required inputs accessible through the native Skill tool or narrowly scoped documented `--add-dir` paths. A shell read of a skill outside the allowed working directories may be denied. Grant only the required inputs/check commands; preserve existing permission rules and hooks. Use the actual host's file tools rather than requiring a Claude-specific tool name in Codex.
- Attempt/time clauses are evaluated from the conversation, not independent hard counters. In non-interactive runs, documented CLI options such as `--max-turns` and `--max-budget-usd` may supply separate runtime limits; confirm their applicability and account semantics before promising a cap. Do not change permission mode to force unattended work through.
- Active goals can be restored when the user resumes a session, but turn/time/spend baselines reset. Preserve cumulative attempt evidence in the task record. Resume is not an automatic restart service.
- `/loop [interval] [prompt]` is the separate built-in timed mechanism. Use it for explicitly requested polling, with cancellation and limits appropriate to the host. It is not required for ordinary Goal continuation.
- Leave an existing disabled Ralph plugin disabled unless the user specifically asks to use it. Do not stack native Goal evaluation, a Ralph stop hook, and a scheduled re-prompt for the same work.

Sources: [Claude Code Goal](https://code.claude.com/docs/en/goal), [scheduled prompts](https://code.claude.com/docs/en/scheduled-tasks), and [CLI reference](https://code.claude.com/docs/en/cli-reference).

Local Claude Code 2.1.296 verification on 2026-10-27 observed the evaluator return not-met after the first final response, automatically start the next turn without another prompt, and return met after final acceptance. The correctness tests were unchanged and independently rerun. This verifies a small local task, not overnight uptime or crash recovery.

## Other hosts

Use documented equivalents only after inspecting the actual tools and account route. Disclose whether repetition is confined to the current turn, driven by a persistent Goal, or triggered by a timer. Without a verified continuation mechanism, deliver the contract and current-turn work rather than promising unattended continuation.
