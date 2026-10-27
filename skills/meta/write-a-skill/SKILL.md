---
name: write-a-skill
description: Creates or updates a small, triggerable agent skill with clear scope and optional bundled resources. Use when asked to write, improve, consolidate, or package a skill.
license: MIT
metadata:
  category: meta
---

# Write a Skill

## Workflow

1. Establish the task, intended user, useful triggers, and observable result from the request. Read nearby skills before adding one. Prefer a reference or a focused mode when it shares an existing skill's purpose.
2. Choose invocation deliberately. Use natural-language eligibility for recurring tasks the agent should recognize. For workflows that should begin only on a user's explicit request, use the host's manual-invocation metadata; verify each target host's mechanism instead of assuming one field is universal.
3. Write `SKILL.md` with YAML `name` and `description`. Match the name to its folder. Describe what it does and when to use it in at most 1,024 characters; put the useful task trigger first. Use optional `license` and string-valued `metadata` for distribution information.
4. Keep the body small: when to use, the necessary steps, stopping conditions, and expected output. Ground decisions in available context; avoid repeated generic policy, fixed question quotas, or automatic extra workflows. The skill cannot grant permission beyond the user's request and host rules.
5. Bundle references only for branches that need them and link them directly from the main file. Bundle scripts only for deterministic repeated work. Resolve resources relative to the installed skill directory; avoid usernames, home-directory assumptions, and mandatory unbundled dependencies.
6. Verify manifest syntax, relative links, license/provenance, standalone use, and the intended discovery mode. Include a representative positive case, an adjacent task that should not trigger it, and any important stopping boundary. Distinguish static inspection from a real host invocation test.

## Output

Deliver the skill and explain its trigger, expected result, and important boundary. Save only the files needed for use and distribution. Do not add a separate README or changelog inside every skill by default.

## Packaging and maintenance

- Keep one canonical body across supported hosts. Add host-specific invocation metadata or packaging adapters only where needed.
- When the user asks for multi-host installation, verify each active path, stale duplicates, references, and resulting availability. Refresh their skill catalog if names or invocation modes changed.
- Retain third-party attribution and license notices when adapting existing material. Keep private operational context outside a public skill package.
- Categories organize source and selection; they do not guarantee grouped menus in every client.
- Validate current format and client behavior against the [Agent Skills specification](https://agentskills.io/specification) and the target client's documentation when unfamiliar.
