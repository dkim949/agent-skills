# Architecture and scope

## One portable source

The repository stores one canonical directory per skill under `skills/<category>/<name>/`. A skill contains `SKILL.md` and only the references or client metadata it uses. The Skills CLI is the standard collection installation path. The optional offline copier bundled with `sync-agent-environment` installs a separately reviewed allowlist bundle. Neither installation path requires a plugin or starts a background process or hook.

Categories describe the repository, not client interface behavior. Skill names are unique across categories. All seventeen skills may be selected for matching requests. Environment retrospectives, independent team review, and research debates are explicit-request branches of `review-and-improve`; ordinary reviews stay direct. Goals and teams also require their corresponding explicit request. The host still controls invocation and authorization.

## Partial installation

A selected skill must remain useful without optional siblings. Cross-skill pointers describe distinct outcomes and provide a direct fallback when the target is absent. They must not trigger duplicate analysis or hide a mandatory dependency. The explicit exception is `safe-local-run`: its scripts require the sibling `run-and-verify` command supervisor and refuse an unprotected launch when it is absent. Installation instructions select both; the CLI does not resolve this dependency automatically. Local reference links stay inside the repository and accompany the skill they support.

Generic execution, coordination, and selective synchronization workflows are included. Private agents, machine-specific configuration, company reference material, personal voice profiles, and organization-specific procedures remain outside this repository. Public skills may inspect a user's authorized material at use time; the package itself contains no private configuration or operational identifiers. Global instructions can conditionally point to a private reference without embedding it in a public skill.

## Decisions

| Decision | Reason | Alternative considered | Revisit when |
| --- | --- | --- | --- |
| Seventeen focused skills with conditional references | Cover the reusable development and coordination workflows as well as thinking, writing, analysis, and maintenance | Keep only the earlier nine, bulk-export a mixed environment, or add one broad router | Real requests repeatedly miss a necessary workflow |
| Four category folders | Help readers browse a growing collection | Flat folder | Discovery tooling fails on nesting or readers cannot find skills |
| Stable category and skill names | Add writing to productivity, execution and coordination to engineering, and environment sync to meta without moving existing entrypoints | Add separate writing/automation categories or rename team skills again | A category grows enough to obscure distinct outcomes |
| One required execution companion | Keep memory policy and command supervision under separate owners with one supervisor implementation | Duplicate the runner or merge the two skills | Independent distribution becomes necessary beyond the documented pair |
| Standard Skills CLI | Reuse selection and client support | Maintain a custom installer | A verified client requirement cannot be served by the CLI |
| Optional sibling routing | Allow useful partial installations | Require the whole collection | Shared behavior cannot remain accurate without a dependency |
| Explicit environment-retrospective branch in review | Keep environment review intentional with fewer entrypoints | Standalone manual skill or automatic retrospective | Real requests fail to reach the branch or evidence supports changing its boundary |
| Static validation plus documented behavior cases | Separate package correctness from model behavior | Treat a passing linter as behavioral proof | Fresh-session evaluation becomes available and repeatable |

## Validation limits

The validator checks manifests, references, packaging boundaries, symlinks, and selected leak patterns. Its checks are deliberately bounded and can miss unfamiliar secret formats. Document review checks intended behavior and routing; it does not demonstrate actual client selection or benchmark reliability.

On 2026-10-28, Skills CLI 1.7.4 installed the seventeen-skill expansion into isolated Codex and Claude project paths; all 34 resource trees matched source bytes and executable flags. A materialized allowlist bundle passed the optional copier's no-write dry-run, 51 exact copies across three isolated host roots, and an unchanged repeat plan. Neither installation nor static validation establishes fresh-session model behavior, another physical device, or unattended runtime recovery.
