# Agent Skills

Ten reusable skills for clearer thinking, evidence-led analysis, review, and skill maintenance. Each skill works on its own; installing the whole collection is optional.

| Category | Skills |
| --- | --- |
| Productivity | `ask-me`, `idea-refine`, `tldr`, `explain`, `handoff` |
| Data science | `data-investigation`, `sql-style-guide` |
| Engineering | `review-and-improve` |
| Meta | `retro`, `write-a-skill` |

`retro` requires explicit invocation. The other skills are eligible for model selection and can also be invoked directly; selection depends on the client and request. Category folders organize the repository and do not promise groups in a client's skill picker.

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

Installation does not require a plugin. Named sibling skills are optional: when one is absent, follow the direct workflow described in the selected skill rather than stopping or repeating the task.

## Use

Ask for the result in ordinary language, or explicitly invoke a skill using your client's skill picker or supported command syntax. Examples:

- “Summarize these notes in three lines.”
- “Explain the missing step in your previous answer.”
- “Investigate why this metric changed.”
- “Review this plan and suggest concrete improvements.”
- Explicitly select `retro` to review your working environment.

Skills preserve the host's permissions. A review, summary, or handoff does not authorize publishing, sending messages, or changing external systems.

## Validate and contribute

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

Validation checks packaging, metadata, local references, and common publication leaks. It does not prove the absence of every secret or establish behavior in a fresh agent session. See [behavior cases](evals/BEHAVIOR.md), [architecture](docs/ARCHITECTURE.md), and [attributions](ATTRIBUTIONS.md). On 2026-10-27, Skills CLI 1.7.4 discovered all ten skills and installed them into isolated Codex and Claude Code project paths; all twenty installed copies retained every source file, reference, license, and invocation setting. Behavior evidence is still document-based review; fresh Codex and Claude Code invocation checks remain pending.

Before publishing, also run the [privacy checks](docs/PRIVACY.md). Installed local hooks can stop a commit or push; the GitHub workflow repeats checks after upload and cannot retract disclosed data.

## License

See [LICENSE](LICENSE), [ATTRIBUTIONS.md](ATTRIBUTIONS.md), and bundled notices under `LICENSES/` for provenance and third-party terms.
