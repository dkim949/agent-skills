# Orca execution

Use only when the actual backend is Orca-managed Tasks/Dispatch. Read the installed version-matched `orchestration` guide for its exact creation, state, mailbox, completion, cancellation, replay and retention APIs. Native Codex or Claude workers in another app use the native adapter instead.

1. Verify actual Run, coordinator, terminal, workspace, account route, available models and required execution guarantees before dispatch. A profile or installed CLI is not route evidence. Keep unknown company routes blocked.
2. Use native task dependencies if the installed host supports them. Otherwise verify prerequisites in the lead and label ordering as coordinator-managed. Record native Task/Dispatch identifiers without inventing lifecycle guarantees.
3. Bind each receipt and result to the actual task and artifact revision. Inspect ambiguous state before retrying; receipt existence alone does not prove exactly-once execution. Reuse the existing workspace when appropriate.
4. Follow native completion and retention rules. Check artifacts independently before marking acceptance or releasing dependents. Keep execution, verified output, and actual human decisions separate.
5. For explicitly requested checkpoints, use the host's verified gate mechanism and the shared dependent-task reference. Match the real response, revision and artifact digest before releasing work. Reviewer agreement or synthetic test feedback never substitutes for approval.

An environment may additionally provide a local `graph_workflow.py` preflight helper and account policy. Discover their paths and version from that environment's instructions, and apply them when required there. They are not bundled with this portable skill and are not a universal scheduler. Missing locally required checks block the affected operation; do not substitute another host or bypass account restrictions.
