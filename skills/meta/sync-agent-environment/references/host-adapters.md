# Host adapters

Official sources checked 2026-10-27. Recheck when an installed client's behavior differs. These are discovery/format facts, not evidence that the current account can run a model.

| Client | User skills | User instructions | Manual-only skills |
|---|---|---|---|
| Codex | `$HOME/.agents/skills/<name>/SKILL.md` | `$HOME/.codex/AGENTS.md` by default | `agents/openai.yaml`: `policy.allow_implicit_invocation: false` |
| Claude Code | `$HOME/.claude/skills/<name>/SKILL.md` | `$HOME/.claude/CLAUDE.md` | `disable-model-invocation: true` in skill frontmatter |
| Gemini CLI | `$HOME/.gemini/skills` or `$HOME/.agents/skills` alias | `$HOME/.gemini/GEMINI.md` | No equivalent established by the cited documentation; retain outside discovery pending a verified adapter |

Codex follows linked skill directories and can show both same-named entries. Gemini has workspace-over-user precedence; duplication still obscures the source. Choose one active location per name per client. Inspect legacy `$HOME/.codex/skills`, other user roots, project roots, plugins, admin settings, and disabled entries on the actual device. Existing machine paths are observations, not a reason to replicate them. Explicit installer targets allow existing compatibility paths without claiming universal discovery support.

Claude and Gemini have import mechanisms for instruction text; Codex reads `AGENTS.md`. For portable cross-host instructions, keep a neutral source and compose small host-specific local files using each host's supported mechanism. Inspect current content and retain unrelated policy. A pointer must tell the agent when and how to read its target; a plain link alone does not prove eager loading. Avoid copying tool permissions or runtime controls into prose and claiming equivalent enforcement.

The installer adds only the two documented manual-only adapters to otherwise neutral bundles. It refuses Gemini manual-only installations and unsupported or contradictory source policy metadata. The known OpenAI sidecar UI strings and a matching invocation-policy boolean are preserved. Natural invocation preserves source bytes. Tools, subagent formats, permissions, Goal lifecycles, hooks, and provider/model settings require separate local review.

Sources:

- [OpenAI skill discovery and invocation policy](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code skills and invocation](https://code.claude.com/docs/en/skills)
- [Claude Code instruction files and imports](https://code.claude.com/docs/en/memory)
- [Gemini CLI skill discovery tiers](https://geminicli.com/docs/cli/using-agent-skills/)
- [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/)
