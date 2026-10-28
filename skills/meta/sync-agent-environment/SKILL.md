---
name: sync-agent-environment
description: "Synchronize selected agent skills and portable instructions across Codex, Claude Code, Gemini CLI, or another personal device. Use for environment portability, drift audits, and replacing one-way Claude-to-Codex migration; ordinary project code changes and account setup keep their own workflows."
license: MIT
compatibility: "Requires Python 3.10+ for the optional offline skill installer; runtime and account configuration remain local."
metadata:
  category: meta
---

# Sync agent environment

Keep one reviewed source of portable instructions and skills. Generate each host's discovery files locally; the source bundle is the transferable artifact. Audit requests stay read-only. A sync request authorizes only its selected files, profiles, and destinations.

## Workflow

1. Identify the source root, target clients/device, selected names, and sensitivity profiles. Inventory active discovery paths, links, duplicate names, and disabled/plugin entries before changing them. Consult [host adapters](references/host-adapters.md) for current discovery and invocation differences. Record observed client versions; installed software does not prove account access or runtime behavior.
2. Classify every selected item as `public`, `private`, or `company` in an explicit allowlist manifest. Stage only reviewed regular files in a dedicated portable bundle. Keep credentials, account/provider settings, runtime history, model selection, hooks, MCP configuration/authentication, and device paths local. Company material stays off a personal second laptop by default. See [bundle and installer](references/bundle-and-installer.md) for the supported subset and commands.
3. Compare actual file content, references, and invocation policy. Resolve symlinks only during inspection; materialize approved files before transport. Rebase relative references within each bundle. Refuse unresolved merge/Syncthing conflicts, secrets, unsafe paths, duplicate discovery entries, or unsupported invocation changes. Read [legacy conversion guidance](references/legacy-conversion.md) only when an existing Claude artifact needs semantic conversion.
4. Produce a dry-run with additions, equal content, exclusions, conflicts, and required manual work. For an authorized local installation, apply the selected plan with reversible destination backups. Existing different content requires an explicitly selected replacement. Preserve unrelated files and source clients. Instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) need a reviewed local adapter; the bundled installer only installs skill directories.
5. Re-audit content and active paths. Refresh the local skill catalog when names/invocation change. Verify discovery in each actual client and separately report untested invocation/inference. Retire an old entrypoint only after its selected replacement and references are checked and a recoverable backup exists.

For a second laptop, read [Syncthing transport](references/syncthing.md). Prepare a separate personal-only export first; enabling a service, pairing a device, or transferring company material requires the user's authorized target and operation.

## Result

Report source, profiles, targets, changed/equal/excluded items, backups, active duplicates, manual work, and evidence. Distinguish source equality, local client discovery, invocation behavior, and a second-device test. A successful copy establishes only the first.
