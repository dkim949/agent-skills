# Optional Syncthing transport

Use Syncthing only to carry a dedicated, physically separated personal export of regular portable files. Keep installation, device pairing, folder sharing, and startup changes separate from preparing the export. The user must authorize those targets/operations; this skill does not enable them.

Recommended sequence:

1. Export only reviewed `public` and explicitly selected `private` skill directories and a reduced manifest. Keep company profiles in a separate, unshared location. Prefer a single editing device initially.
2. After authorization, share only that export folder between the named personal devices. Never share whole `.codex`, `.claude`, `.gemini`, `.agents`, `.config/agent-workflow`, or home directories. These contain local policy, account state, runtime history, backups, or machine paths. Avoid placing a Syncthing folder inside another active cloud-sync folder.
3. Configure local `.stignore` on each device, optionally including one reviewed shared pattern file. Ignore rules are defense in depth; a separate personal export is the data boundary. Do not use ignores to hide company material within a shared root.
4. Enable a suitable file-versioning policy on each authorized device. Keep an independent source/backup copy: Syncthing's versioning covers remote replacements/deletions and does not archive your own local edits.
5. Wait for transport completion, then stop concurrent editing and inspect `.sync-conflict` files and merge markers. Resolve source conflicts before any installer apply. Never choose a winner by timestamp automatically.
6. On each device, run the installer dry-run using that device's absolute roots and observed discovery paths. Generate local discovery copies/adapters. Then verify the actual clients. This proves portable content relocation only after the second device has been tested.

Syncthing preserves symbolic links on supported platforms but does not follow them; Windows does not sync them. Absolute links therefore do not transport their referenced skill files and may point to another user's path. This workflow transports regular files and generates any desired local links separately, after duplicate checks.

`.stignore` belongs at the shared folder root and is not itself synchronized. A shared included pattern file can distribute rules; inspect first-match ordering. Useful exclusions include `.env`, credential/key files, runtime/session/log directories, and local backups. Do not ignore `.sync-conflict` artifacts as a way of making validation pass.

Sources checked 2026-10-27:

- [Syncthing file types and symlink behavior](https://docs.syncthing.net/users/faq.html#what-things-are-synced)
- [Ignore files, include files, and ordering](https://docs.syncthing.net/users/ignoring.html)
- [File versioning and its local-change limitation](https://docs.syncthing.net/users/versioning.html)
- [Synchronization and conflicts](https://docs.syncthing.net/users/syncing.html)

No second-device transfer, service installation, or background agent execution is established by this document.
