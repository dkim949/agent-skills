---
name: idea-refine
description: Shapes rough ideas into useful directions with purposeful alternatives, assumption checks, and minimal tests. Use when asked to refine or explore an idea, or explicitly stress-test it interactively; perform ordinary reviews directly or use review-and-improve if installed. Extended interviewing requires an explicit request.
license: MIT
metadata:
  category: productivity
---

# Idea Refine

## When to use

Use when asked to shape an idea, explore alternatives, or question a plan interactively. Natural-language requests such as “help me refine this idea” are sufficient; naming the skill is optional. For a few missing decisions in an otherwise clear request, use `ask-me` if installed; otherwise ask only the decision-changing questions under the same ceiling below. Perform ordinary artifact or plan reviews directly, using `review-and-improve` if installed.

## Workflow

1. Frame the idea or decision in a sentence using the available context. Inspect relevant evidence before asking questions that files, code, documents, or tools can answer. Separate known facts from untested assumptions.
2. Choose the useful depth. By default, ask zero to three meaningful questions only where answers change the direction or recommendation, resolving upstream decisions first. Independent decisions may be bundled. If the user explicitly asks for a deep interview or thorough interactive stress-test, read [references/deep-interview.md](references/deep-interview.md) and follow that mode instead.
3. Explore alternatives only when they could change the decision. Compare a few materially different approaches, including the simpler version or current workaround when relevant. For an already chosen direction, test its strongest alternative rather than generating variations to fill a quota.
4. Evaluate the relevant trade-offs: who benefits and how, practical feasibility, and why the approach improves on the current alternative. Identify the assumption most likely to invalidate the direction, evidence against it, and the smallest check that could disprove it. Challenge unsupported claims with specific reasons.
5. Converge on a recommendation or an explicit unresolved choice. Define the smallest useful scope, key exclusions and their reason, and the next test or action. Stop once further discussion would not change that next step. Honor “skip,” “you choose,” and requests for a draft using supported, reversible assumptions.

## Output

Give a compact recommendation matched to the request: problem and intended beneficiary, chosen direction and trade-off, critical assumption with a minimal test, and next step. Include scope exclusions or open questions where they affect the decision. Use a one-page brief only when useful; save documents or start implementation only within the user's authorized scope.

## Boundaries

- The default three-question ceiling applies across the whole task, including decisions already asked through `ask-me`; switching skills does not reset it. Explicitly requested deep interviewing uses its own stopping criteria.
- Use the user's language in conversation; author saved official artifacts in their required language.
- An interview is not an exhaustive checklist. Scale effort to the consequence and uncertainty of the decision. Team review, extra approvals, and document creation are separate choices governed by the actual request and host rules.
- Keep facts, assumptions, and user decisions distinct. “Not sure,” silence, or delegated judgment does not grant missing authorization for consequential actions; complete the safe portion and identify the exact blocker.

Approach informed by [Addy Osmani's idea-refine](https://github.com/addyosmani/agent-skills/tree/main/skills/idea-refine) and [Matt Pocock's grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling), with local question limits and stopping rules. This skill is independently worded rather than a copy of those workflows.
