# Agent Skills

Seventeen reusable skills for clearer thinking, evidence-led analysis, writing, development, and agent coordination. Install the selection you need; `safe-local-run` requires its `run-and-verify` companion.

| Category | Purpose | Skills |
| --- | --- | --- |
| Productivity | Clarify, understand, write, and hand work over | `ask-me`, `idea-refine`, `tldr`, `explain`, `handoff`, `concise-work-writing`, `to-tickets` |
| Data science | Investigate evidence and work with SQL | `data-investigation`, `sql-style-guide` |
| Engineering | Diagnose, verify, and coordinate delivery | `review-and-improve`, `diagnosing-bugs`, `run-and-verify`, `safe-local-run`, `goal-loop`, `multi-agent-coordination` |
| Meta | Maintain and move the agent environment | `write-a-skill`, `sync-agent-environment` |

All seventeen skills are eligible for model selection and can also be invoked directly; selection depends on the client and request. Goals, teams, research debates, and coding-environment retrospectives require the corresponding explicit request. Installing them starts no agent, Goal, schedule, hook, or background service. Category folders organize the repository and do not promise groups in a client's skill picker.

## Install a selection

Use the [Skills CLI](https://github.com/vercel-labs/skills). It requires Node.js; consult its current requirements before running it. This repository does not install plugins or automatic hooks.

List the collection, then install the skills you want for both clients:

```sh
npx skills add dkim949/agent-skills --list
npx skills add dkim949/agent-skills --skill ask-me tldr -a codex claude-code
```

The first command lists available skills without installing them. The second selects two skills for both clients in the current project. Omit `--skill` to choose interactively; add `-g` only when you want a global installation. Review existing skills with the same names before replacing them.

From a local checkout, use `.` as the source instead:

```sh
npx skills add . --list
npx skills add . --skill ask-me tldr -a codex claude-code
```

Installation does not require a plugin. Named sibling skills are optional unless explicitly marked as required: when an optional sibling is absent, follow the direct workflow described in the selected skill rather than repeating the task.

The one required companion is `run-and-verify` for `safe-local-run`. Install them together; the memory wrapper refuses to launch without the shared command supervisor:

```sh
npx skills add dkim949/agent-skills --skill run-and-verify safe-local-run -a codex claude-code
```

Use `--skill '*'` to select all seventeen. `safe-local-run` targets macOS; the bundled command supervisor and offline sync installer require Python 3.10+ and their documented system tools. Goal continuation and native subagents depend on capabilities actually exposed by the current client. A skill cannot add those runtime capabilities.

## Update on another device

Keep public skills separate from account state, company procedures, and personal profiles. This repository contains no company-only knowledge or personal writing samples. Plugins such as Ponytail are separate installations.

For a CLI-managed installation, use `npx skills check` and `npx skills update`. For a local checkout directly linked into each client's discovery path, update that checkout with `git pull --ff-only`, then confirm discovery in a fresh session. Pulling a checkout does not update unrelated installed copies. Inspect existing names and back up conflicting content before first linking or replacing a skill.

`sync-agent-environment` provides an optional reviewed-bundle copier. It does not install models, copy credentials, reproduce provider settings, or enable Syncthing. Use local adapters for portable instruction files and keep device permissions local.

## Use

Ask for the result in ordinary language, or explicitly invoke a skill using your client's skill picker or supported command syntax. Examples:

- “Summarize these notes in three lines.”
- “Explain the missing step in your previous answer.”
- “Investigate why this metric changed.”
- “Review this plan and suggest concrete improvements.”
- “Review this coding session for improvements to the working environment.”

Skills preserve the host's permissions. A review, summary, or handoff does not authorize publishing, sending messages, or changing external systems.

## Validate and contribute

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

Validation checks packaging, metadata, local references, and common publication leaks. It does not prove the absence of every secret or establish behavior in a fresh agent session. See [behavior cases](evals/BEHAVIOR.md), [architecture](docs/ARCHITECTURE.md), and [attributions](ATTRIBUTIONS.md).

On 2026-10-28, Skills CLI 1.7.4 discovered all seventeen skills and installed them into isolated Codex and Claude Code project paths. All 34 installed resource trees matched source bytes and executable flags, including references, notices, scripts, and invocation metadata. The optional offline copier also passed dry-run, 51 exact copies into three isolated client roots, and an unchanged repeat plan. These are packaging and copy checks; fresh-session selection and end-to-end Goal/team behavior are not established by them.

Before publishing, also run the [privacy checks](docs/PRIVACY.md). Installed local hooks can stop a commit or push; the GitHub workflow repeats checks after upload and cannot retract disclosed data.

## License

See [LICENSE](LICENSE), [ATTRIBUTIONS.md](ATTRIBUTIONS.md), and bundled notices under `LICENSES/` for provenance and third-party terms.
