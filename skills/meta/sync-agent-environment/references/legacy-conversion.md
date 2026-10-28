# Selected legacy conversion

The retired `migrate-to-codex` workflow was a one-way converter. Preserve its useful review sequence: inspect sources, plan, dry-run, inspect generated instructions and skill resources, validate target artifacts, then compare again. Source Claude files and unrelated target entries remain intact.

[Archived migration differences](legacy-migration-differences.md) preserve the earlier mapping tables under their [Apache 2.0 license](legacy-migration-LICENSE.txt). They were last checked in April 2026 and describe the old converter, not this installer. They are historical review prompts, not current configuration instructions. In particular, the old statement that Codex has no manual-only equivalent is superseded by [the current host adapter](host-adapters.md).

For a selected conversion:

1. Rewrite provider-specific instruction/tool assumptions into a neutral task workflow and local host adapter.
2. Convert a selected slash command into a named skill only after inspecting argument substitution, dynamic shell expansion, allowed tools, and supporting files. Text resemblance does not establish runtime equivalence.
3. Compare relative references and the complete resource tree, not just `SKILL.md` or link destinations.
4. Treat agents, plugins, hooks, MCP transports/authentication, sandbox settings, and model/effort controls as host-specific manual work. Keep these outside the portable installer and personal export.
5. Report unsupported semantics precisely and preserve the original for rollback. Do not repeatedly rewrite configuration in pursuit of an empty warning report.

The old migrator scripts are deliberately not bundled or invoked: they write broad runtime configuration beyond selective synchronization.
