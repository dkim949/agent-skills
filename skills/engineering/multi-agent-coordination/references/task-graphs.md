# Dependent tasks and recovery

Read this only for dependent multi-stage work, interruption recovery, required durable execution, or requested human checkpoints. Ordinary fan-out reviews use the common entrypoint.

## Plan

Planning is read-only. Give nodes stable display IDs such as `T1`, `T2`, and `T3.r2`; state dependencies, exclusive output owners, input/output classifications, required execution guarantees, and account route. Name the human checkpoints requested for this graph, or state that none are active; invoking the skill alone does not add approval gates. The current environment's private policy supplies exact routes and content constraints; [account boundaries](account-boundaries.md) supplies portable checks. Machine-local paths apply only on their host.

Choose each node's provider/model and supported effort from the selected account's current catalog or verified host profiles according to difficulty, capabilities, and cost. Record the choice, rationale, catalog/profile source, and any fallback before creation, including for small samples. The same model may suit multiple nodes; inheritance is a deliberate choice only after resolving the parent runtime and explaining its fit. Use only an available same-account fallback; keep current company access restrictions from the user's active guidance.

## Execute and show progress

Before each launch, check that the node has a resolved model choice and that the documented creation arguments implement it, explicitly or by deliberate inheritance. Resolve incompatible context-fork/model options using the selected backend's procedure. An unmet model-selection requirement keeps that node unlaunched; writing `unknown` in a progress row does not satisfy it. This is a coordinator check, not an additional human approval gate.

Give every worker its input, ownership, constraints, and observable acceptance. Start independent work before waiting, using the host's documented completion mechanism. Verify returned artifacts before fan-in and launch a dependent only after its prerequisites and any requested human checkpoint pass. Record native host/workspace/agent/attempt identifiers without inventing equivalents for another tool's lifecycle.

Company inputs and outputs stay on verified company routes unless the policy, graph classification, and receiving node explicitly permit transfer. Apply the same boundary to task titles, progress, gate text, feedback, and decision records. A profile label is not company-route evidence; use only non-secret configuration/runtime facts and do not inspect credentials.

At start, a meaningful state change, a checkpoint, and completion, show a compact text table: T alias, task, native execution state, planned account, selected/observed model and effort, native owner, and verified output or blocker. Keep execution, verification, and user decision separate. Native completion is execution evidence; declared outputs are not verified artifacts or user approval. Disclose coordinator-managed ordering instead of native dependency enforcement.

Check matching worker runtime metadata and available enclosing-host records before declaring a model unobservable. Distinguish requested settings, configured settings, inherited settings derived from a parent, and directly observed worker runtime; a model menu, profile, or self-description alone is not execution evidence. Record evidence source and capture time with native IDs. A current parent snapshot cannot independently prove an earlier child's model. Where direct child evidence is unavailable, report that precise limit and assess it against the graph's requirements.

Keep saved node-to-native-ID mappings with the selected host. On interruption or an ambiguous receipt, inspect native state and current ownership before retrying. Silence is not failure. Use a native replay/attempt mechanism only if that host documents it; disclose missing recovery guarantees and remain plan-only when the job requires them. Existing sessions are retained when the user asks. A text checklist is a view, not proof of a native DAG or an identical UI across clients.

## User verification and understanding

Use human checkpoints when requested or when an existing authorization rule requires them. The usual two are direction before the execution wave and integrated result after independent verification. Reuse an earlier explicit approval within its original scope. Other work may continue only if it is independent of the pending decision.

Put the actual question, what changed and why, one inspectable example, evidence, how to use or revise the result, and the remaining limitation in ordinary chat. Offer approve, request changes, explain, or pause, and accept a plain-chat reply tied to the displayed revision. A choice widget is optional; explain any required submit action and provide a text fallback. A short example or optional readback can repair confusion; a quiz requires a user request. Acknowledged understanding is separate from authorization.

Present an immutable artifact revision and record its path, revision, digest, decision, source, and actual user-response reference together with the selected host's native context. Keep the decision pending on an explanation request or silence. TEST feedback, reviewer agreement, and successful execution cannot authorize it. The coordinator must verify the real response and scope from the conversation; local records cannot authenticate a human by themselves.

Use the selected host's verified gate mechanism where available. Otherwise the coordinator withholds affected launches and clearly records that the checkpoint is coordinator-managed. If native enforcement or restart-safe approval is required but unverified, keep that work unexecuted. A gate resolution alone never authorizes launch. A request to pause stops the affected work.

On a revision request, preserve the rejected artifact and native outcomes, create a new revision node/output, and revalidate affected dependents. Present the new revision for any required acceptance; approval of an old digest cannot accept it. Expand feedback into new nodes rather than cyclic dependencies. Resolve repeated disagreement with concrete user choices, not automatic approval.

## Verification

Use public fixtures to check independent workers, verified fan-in, native identity, progress, a plain-chat explanation/revision, and preservation of unrelated work. Include per-node model choices reaching actual creation arguments, deliberate inheritance, incompatible fork options, and missing or time-mismatched runtime evidence. Check ordinary requests do not activate graph execution, missing capabilities produce zero launches, unknown company routes receive no company data, and old or synthetic decisions cannot accept a new revision. Distinguish inspected instructions, simulated scenarios, actual host tests, and unrun recovery checks; evidence from one backend does not certify another. Actual human feedback remains a separate live check.


The original graph-specific procedure is retained here to preserve account checks, completion evidence, recovery limits, and actual user-decision boundaries. It does not add those requirements to every small team review.
