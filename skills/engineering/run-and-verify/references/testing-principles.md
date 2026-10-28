# Testing principles

Read when adding or changing tests. Running an existing check does not require a new test-design workflow.

## Choose a useful boundary

- Follow the repository's test conventions and exercise observable behavior through a public interface, API, or relevant integration boundary. Choose the boundary that can actually reveal the failure. A tiny helper test cannot prove a defect in an end-to-end call chain is fixed.
- Take expected results from the requirement, an independently worked example, or trusted fixtures. An assertion that repeats the implementation's calculation may pass by construction.
- Prefer real behavior over internal call counts or mocks of the behavior being claimed. Use test doubles for necessary external boundaries while retaining an integration check when the conclusion depends on the real boundary.
- Select the smallest set of cases that establishes the changed behavior and material edge cases. Avoid fixed coverage percentages, fixed test-pyramid ratios, and tests that merely mirror an implementation. A trivial prose/configuration edit may need no new test.

## Prove the test can detect the defect

For a bug fix with a suitable seam, reproduce the original symptom, observe the test fail for that reason, make the scoped fix, and observe it pass. A collection error, missing dependency, or syntax mistake is not the intended red signal. Keep the test and acceptance condition unchanged across that comparison.

If implementation is already present, preserve it and use an isolated, owned comparison against the previous behavior when useful. Respect others' edits; never delete working implementation to satisfy a test-first ritual. If no suitable reproduction seam exists, record the gap and use the strongest available behavior check without claiming regression protection was proven.

When test-first development is requested or materially useful for new behavior, work in small vertical slices: one observable behavior, its failing check, the minimal implementation, then the next justified slice. Reuse known requirements and interfaces; clarify only decisions that materially affect the result. Do not require an interview or approval for every test boundary.

## Preserve what a pass means

- Keep the scope visible: focused test, build, full suite, runtime interaction, and requirement coverage establish different claims. Run broader relevant checks when warranted by the change and cost; report unavailable, unrelated failing, or deliberately omitted checks honestly.
- Review changes to tests and gates alongside the implementation. Skips, deleted cases, weakened assertions, suppression comments, threshold changes, and disabled CI jobs can hide the original failure. Explain justified changes separately and verify the original acceptance where it remains applicable.
- Reuse trustworthy evidence until a relevant implementation, test, input, command, or environment change invalidates it. Share one evidence record across debugging, review, and Goal work; each skill does not need its own identical run.

These independently written guidelines draw on [Matt Pocock's TDD](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md), [Addy Osmani's TDD](https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md) and [constraint-driven development](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md), and [Superpowers verification](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md). They retain project-specific judgment rather than importing the source workflows' mandatory interviews, universal test rules, or per-message reruns.
