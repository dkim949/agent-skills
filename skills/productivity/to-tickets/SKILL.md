---
name: to-tickets
description: "Draft or improve concise English Jira tickets and decompose plans, specifications, or conversations into independently verifiable work with dependencies. Use for software, research, ML experiments, investigations, and documentation tickets; sprint capacity and commitments require a separate planning workflow. Publish only when explicitly requested."
license: MIT
metadata:
  category: productivity
---

# To Tickets

## When to use

Draft in the conversation by default. Create, update, transition, assign, link, or comment on real issues only when the user explicitly requests the exact action; follow any additional applicable approval boundary. Approval of a draft or breakdown alone does not authorize publication. Save local files only when requested.

## Workflow

1. Read the supplied context and referenced sources needed for the ticket. Preserve facts and label assumptions. Inspect relevant code or project conventions when implementation details affect scope; a simple draft does not require codebase exploration.
2. Choose a single ticket or a breakdown. Keep one ticket when it has one coherent, verifiable outcome. For larger work, use the breakdown rules below.
3. Use `concise-work-writing` when installed for workplace wording; otherwise write directly for the intended reader with concise prose and preserved facts. Write a short English title and the smallest useful combination of Context, Objective, Scope, and Acceptance Criteria, usually 5–8 bullets total for a single ticket. Adapt sections to the work rather than filling a template.
4. State observable completion conditions and a practical verification method. Preserve supplied owners, dates, metrics, and technical decisions; leave missing ones unspecified. Ask only when a missing decision materially changes the draft, otherwise deliver it with the uncertainty visible.

## Breakdown

- Give each ticket one independently assessable outcome, its acceptance criteria, how to verify them, and blocking tickets. Order blockers first; distinguish genuine prerequisites from a preferred sequence.
- For software features, prefer a narrow working path across the layers actually involved. Include refactoring only when it is a demonstrated prerequisite.
- For research or ML, define the question, bounded comparison or experiment, evidence to produce, and decision or handoff. Completion can be an inconclusive result with documented limits; promising a positive metric gain is not an acceptance criterion unless the user explicitly sets it as a requirement.
- For investigations, define the symptom or question, evidence and competing explanations to assess, and the expected diagnosis or next check. For documentation, define the audience, coverage, and reviewable artifact.
- Size work for one focused session when practical. Split by separable outcomes or risk, rather than an arbitrary file count. Keep necessary stable paths, interfaces, or decision-rich snippets when they make the task actionable.
- For a broad mechanical migration, use expand, migrate, contract: introduce the compatible form, migrate bounded caller groups, then remove the old form after all callers move. State any integration branch or final verification dependency needed to keep the sequence safe.

## Output

Present a numbered list with **Title**, **Outcome**, **Acceptance criteria / verification**, and **Blocked by**. Omit redundant fields for a small single ticket. Capacity, sprint goals, and Must/Should/Stretch commitments are outside this skill's scope; use the user's available planning workflow when separately requested. Ordinary drafting and decomposition stay here.

## Requested saving or publication

Resolve the target, issue type, fields, and tracker conventions before writing. Create one item per agreed ticket in dependency order so links can use real identifiers. Use native blocking relationships when supported; otherwise record blockers in the body. Apply labels, parent/sub-issue relationships, estimates, or sprint assignments only when requested or established by the target's conventions within the authorized action.

For local files, use the user or repository's destination and format; if unspecified, choose a clearly scoped directory and state it. Preserve existing files and unrelated tracker items. Report saved paths or issue links and any unresolved dependencies. Drafting never starts implementation or changes a parent issue.
