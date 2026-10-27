# Architecture and scope

## One portable source

The repository stores one canonical directory per skill under `skills/<category>/<name>/`. A skill contains `SKILL.md` and only the references or client metadata it uses. The Skills CLI discovers and installs a selected subset for supported clients. There is no custom installer, plugin requirement, background process, or automatic hook.

Categories describe the repository, not client interface behavior. Skill names are unique across categories. All nine skills may be selected for matching requests. Environment retrospectives, independent team review, and research debates are explicit-request branches of `review-and-improve`; ordinary reviews stay direct. The host still controls invocation and authorization.

## Partial installation

A selected skill must remain useful without sibling skills. Cross-skill pointers describe distinct outcomes and provide a direct fallback when the target is absent. They must not trigger duplicate analysis or create a hidden mandatory dependency. Local reference links stay inside the repository and accompany the skill they support.

Operational workflows, private agents, machine-specific setup, and organization-specific procedures remain outside this repository. Public skills may inspect a user's authorized material at use time; the package itself contains no private configuration or operational identifiers.

## Decisions

| Decision | Reason | Alternative considered | Revisit when |
| --- | --- | --- | --- |
| Nine focused skills with optional references | Preserve distinct outcomes while folding conversation interpretation, research debate, environment review, and skill maintenance into existing entrypoints | Bulk export, one broad router, or a separate skill for each mode | Real requests repeatedly miss a necessary workflow |
| Four category folders | Help readers browse a growing collection | Flat folder | Discovery tooling fails on nesting or readers cannot find skills |
| Standard Skills CLI | Reuse selection and client support | Maintain a custom installer | A verified client requirement cannot be served by the CLI |
| Optional sibling routing | Allow useful partial installations | Require the whole collection | Shared behavior cannot remain accurate without a dependency |
| Explicit environment-retrospective branch in review | Keep environment review intentional with fewer entrypoints | Standalone manual skill or automatic retrospective | Real requests fail to reach the branch or evidence supports changing its boundary |
| Static validation plus documented behavior cases | Separate package correctness from model behavior | Treat a passing linter as behavioral proof | Fresh-session evaluation becomes available and repeatable |

## Validation limits

The validator checks manifests, references, packaging boundaries, symlinks, and selected leak patterns. Its checks are deliberately bounded and can miss unfamiliar secret formats. Document review checks intended behavior and routing; it does not demonstrate actual client selection or benchmark reliability.

Historical installation evidence: on 2026-10-27, before the retrospective consolidation, Skills CLI 1.7.4 was run against a temporary project for both supported clients. All ten then-current skills were discovered and twenty installed copies matched their sources, including invocation metadata and licenses. This check has not been repeated for the current nine-skill package and does not establish fresh-session model behavior.
