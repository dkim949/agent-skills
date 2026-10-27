---
name: retro
description: Reviews a coding session for concrete improvements to the agent's working environment.
disable-model-invocation: true
license: MIT
metadata:
  category: meta
---

# Coding Environment Retro

## When to use

Use when the user explicitly requests a retrospective on how an agent worked. Focus on recurring friction in the environment and instructions. A service incident investigation belongs to an evidence-based incident workflow; a team ceremony is a different task.

## Workflow

1. Read the specified session and relevant artifacts. Default to the current conversation. Inspect only the logs needed for that session; avoid collecting unrelated history.
2. Identify concrete friction: hard-to-find files, missing evidence, repeated mistakes, costly tool use, misleading instructions, or a check that existed but was not run. Tie each candidate to an observed example and its cost.
3. Check what already exists before adding a rule or tool. Inspect relevant repository guidance and check commands. For a repeatable mechanical error, prefer the smallest deterministic check using existing tooling. For a judgment call, clarify the relevant guidance. Remove redundant instructions rather than adding another layer.
4. Propose only improvements likely to change a future run: the target file or check, expected benefit, and how to verify that benefit. Distinguish a repeatable issue from a one-off inconvenience. A missing hook or CI file alone does not justify adding infrastructure.
5. Prioritize the smallest useful changes. Implement only changes the user has requested or already authorized; a retrospective alone produces recommendations. Do not launch a team, modify permissions, or install tooling automatically.

## Output

Give the observed friction, evidence, recommended change, and a future check. Omit categories without a material finding. If the environment already supports the task well, say so rather than inventing work.

For agent-facing text, keep the main instruction short, put infrequently needed detail behind a clear pointer, and preserve applicable user preferences. Avoid encoding one session's accident as a universal rule.

Adapted from [Matt Pocock's retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md), with scope and evidence requirements tailored for small, user-directed improvements.
