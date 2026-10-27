# Coding environment retrospective

Use only when the user explicitly requests a retrospective on how an agent worked. Examine recurring friction in the environment and instructions. An operational incident investigation belongs to an evidence investigation; a team ceremony has a different purpose.

1. Read the specified session and relevant artifacts, defaulting to the current conversation. Inspect only the logs needed for that session.
2. Identify concrete friction: hard-to-find files, missing evidence, repeated mistakes, costly tool use, misleading instructions, or an available check that was missed. Tie each candidate to an observed example and its cost.
3. Check existing guidance and tooling before proposing another rule or tool. For a repeatable mechanical error, prefer a small deterministic check with existing tools; for a judgment call, improve the relevant guidance. Remove redundancy when it contributes to the problem.
4. Recommend changes likely to improve a future run. Name the target file or check, expected benefit, and verification. Distinguish repeatable problems from one-off inconvenience. A missing hook or CI file alone does not justify adding infrastructure.
5. Prioritize the smallest useful changes. A retrospective by itself produces recommendations; implement only changes already authorized by the user. It does not automatically launch a team, change permissions, or install tooling.

Deliver observed friction, supporting evidence, the proposed change, and a future check. Omit empty categories; say when the environment already supports the task well.

For agent-facing text, keep the main instruction short and place occasional detail behind a clear conditional pointer. Preserve applicable preferences and avoid making one session's accident a universal rule.

Adapted from [Matt Pocock's retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md), through this collection's earlier environment-retrospective skill. Retain this collection's MIT license and bundled upstream notice when redistributing it.
