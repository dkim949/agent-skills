# Native subagent execution

Use this path inside Codex or Claude Code without requiring Orca or Paseo. Inspect the current tool catalog for delegation, messages, task state, completion notifications, and cancellation. Product names alone do not establish available tools or account routing.

## Apply the model choice

Read the live creation schema before mapping each planned model/effort into arguments. Agent role, native task ID, and model ID are separate facts: a role such as `worker` does not select a model. Use explicit model/effort controls where supported. If inheritance fits the node, record the resolved parent settings and the reason for choosing them as the common entrypoint requires.

Some Codex tools permit model overrides only with a fresh-context fork. When this is the verified contract, launch the chosen model with that fork and a complete bounded task prompt, or deliberately choose the parent model when shared history is needed. Check higher-priority launch restrictions as well. A restriction on one fork mode does not establish that all native subagents must inherit. If the selected model cannot be applied, disclose the specific constraint and resolve the choice before launch.

For model evidence, inspect matching native worker metadata; an enclosing app may also expose the parent's runtime. Preserve that distinction and the capture time. A parent runtime plus a documented inheritance rule supports an inherited-setting report, not a claim of independently observed child inference.

## Coordinate dependencies

1. Keep stable node IDs, owned outputs, acceptance checks, and prerequisites in the existing task plan. Label dependency enforcement as coordinator-managed unless an actual native task API enforces it.
2. Launch ready independent nodes using the host's native subagent tool, within available concurrency. Give each worker explicit file/output ownership and tell it to preserve others' work. A task with no independent useful outputs may run sequentially without extra agents.
3. Consume actual completion messages or the documented wait mechanism. Inspect each result and its evidence before marking the node verified. Launch a dependent only when its prerequisites have passed and any required user decision has actually arrived.
4. Reuse existing workers for related follow-ups where appropriate. A failed or silent worker is not permission to duplicate its edits. Inspect its state and ownership before retrying, and integrate only verified outputs.

The coordinator remains responsible for integration and the final checks. Subagent completion is not proof that the full user outcome works. Native subagents use the routes and model controls the host actually exposes; a role name cannot change account identity.

## Goal and recovery boundaries

If the user requests continuing until a measurable outcome, `goal-loop` can supply the completion contract and native Goal continuation. It does not replace node acceptance or authorize additional agents. Use one coordinator and one continuation mechanism for the job.

Ordinary subagent tools do not establish a persistent DAG, restart-safe gates, exactly-once launches, or a graph UI. After interruption, inspect actual worker and task state before continuing. Save node IDs and evidence in the existing task record only when needed for work across turns. If required workers no longer exist, disclose that limitation before reconstructing the remaining work. A job requiring unverified recovery guarantees remains unexecuted.

Live verification on 2026-10-27 completed a public three-node fixture on the current Codex desktop native collaboration backend and Claude Code 2.1.296 native Agent tools: two concurrent workers, independent prerequisite verification, then a dependent integration worker. Matching child runtime records verified the models; immutable fixture hashes and fixed expected results passed. The environment owner retains the dated local test record; this portable package does not include private runtime logs or machine paths. This does not certify Codex CLI orchestration, a persistent DAG engine, interruption recovery, overnight operation, or human approval gates. An Orca fixture also cannot certify these other backends. Validate the actual selected backend when materially different guarantees are required.
