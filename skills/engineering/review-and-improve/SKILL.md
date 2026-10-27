---
name: review-and-improve
description: Reviews artifacts, plans, designs, research, code changes, and pull requests against their intended outcomes. Use for a substantive review or improvement; ordinary reviews run directly, while interviews and independent team reviews require an explicit request.
license: MIT
metadata:
  category: engineering
---

# Review and Improve

## When to use

Review a supplied artifact or direction and recommend concrete improvements. Scale the work to its consequence: a small edit needs a small review.

## Workflow

1. Identify the current intended outcome and constraints. Read the artifact and relevant evidence before asking for missing decisions. If clarification matters, ask at most three decision-changing questions across the task; stop earlier when enough is known. The optional `ask-me` skill supplies examples.
2. Preserve strengths, then inspect actionable weaknesses, assumptions, failure scenarios, and missing evidence. For a logical claim, inspect premises, inference, and counterexamples. For an empirical claim, inspect observations, competing explanations, confounders, and a falsifiable check. Do not force a causal narrative or fixed number of why questions.
3. Compare the strongest plausible alternative when it could change the recommendation. For consequential decisions, state the claim, evidence, material assumption, alternative, smallest discriminating test, and decision rule. Omit empty templates and low-impact hypothetical concerns.
4. Map meaningful recommendations to evidence, a relevant file, an executable check, or an observable decision rule. Distinguish source inspection, completed checks, assumptions, and checks not run.
5. Deliver the prioritized findings and the requested improvements. Reuse a completed review unless changed evidence warrants another pass. Edit the artifact only within the user's authorized scope.

## Select a focused path

- Pull request or code diff: read [PR review](references/pr-review.md).
- Substantive implementation: check requirement coverage below.
- Explicit idea shaping or interactive stress-test: use `idea-refine` if installed; otherwise explore only the missing choices directly. An ordinary review does not start an interview.
- Empirical explanation needing investigation: use `data-investigation` if installed, or examine competing hypotheses and evidence directly; do not run a second full review afterward.
- Explicit team review: use the team procedure below. A topic alone does not request delegation.
- Brief challenge: give one critical pass directly. A separate skill is optional.

## Requirement coverage

Use the latest agreed requirements and acceptance criteria. For each material criterion, identify the implementation location, verification evidence, and any gap. A checked task box is not evidence of working behavior.

Report missing or partial behavior, contradictions, and unrequested additions. Flag extra work for review rather than deleting it automatically. Use a compact `Requirement | Implementation | Verification | Gap` table when helpful. Distinguish a future product outcome from behavior testable today. Keep failed or unavailable checks visible.

This mode adapts [Spec Kit's convergence review](https://github.com/github/spec-kit/blob/v1.2.3/templates/commands/converge.md). A full specification workflow may help when requirements repeatedly drift across sessions.

## Explicit team review

1. Form an initial assessment before reading reviewer conclusions.
2. Assign two or three available native subagents different, bounded questions and only the context they need. Reviewers stay read-only unless implementation was requested.
3. Check important findings against evidence, resolve disagreements, and own the final recommendation. Distinguish verified facts, assumptions, and unresolved differences.

Use the current host. If delegation is unavailable, disclose that limit and review directly. External providers require an explicit request and an authorized data scope. Team review does not authorize publication, messages, or operational changes.

## Output

Lead with the judgment and its practical consequence. Include the strengths worth preserving, actionable findings with evidence, and the next useful changes or checks. Use file and line references for code findings. Do not manufacture findings to fill a severity quota.
