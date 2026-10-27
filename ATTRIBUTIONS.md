# Attribution and provenance

This is a selected, edited collection, not a mirror of a dotfiles repository or a vendor plugin. The original material and modifications in this repository are distributed under the MIT license. Upstream notices are retained in `LICENSES/` and in each affected skill's `LICENSE`, so installing a single skill retains its applicable notices.

| Material | Origin and treatment | Notice |
|---|---|---|
| `ask-me` | Local clarification workflow, refined with the dependency-aware questioning approach of Matt Pocock's [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling). The question ceiling and stopping rules are local adaptations. | [Matt Pocock](LICENSES/matt-pocock.txt) |
| `idea-refine` | Independently worded consolidation informed by [Addy Osmani's idea-refine](https://github.com/addyosmani/agent-skills/tree/main/skills/idea-refine) and Matt Pocock's grilling. | [Addy Osmani](LICENSES/addy-osmani.txt), [Matt Pocock](LICENSES/matt-pocock.txt) |
| `explain` | Rewritten local explanation and optional learning workflow incorporating the explanation-repair approach studied in Matt Pocock and Addy Osmani's skill collections, plus a local conversation-interpretation reference. No upstream automatic learning workspace or persistence mechanism is included. | [Matt Pocock](LICENSES/matt-pocock.txt), [Addy Osmani](LICENSES/addy-osmani.txt) |
| `handoff` | Edited local continuation workflow informed by the four implementations listed below; action status and evidence handling are explicit local additions. | Notices listed below |
| `review-and-improve` | Local review workflow. Requirement coverage is adapted from [GitHub Spec Kit's converge template](https://github.com/github/spec-kit/blob/v1.2.3/templates/commands/converge.md). The PR review reference is independently worded. Red-team review uses independently worded research and reconciliation techniques, with design sources linked in that reference, including [Addy's orchestration patterns](https://github.com/addyosmani/agent-skills/blob/main/references/orchestration-patterns.md) and doubt-driven development. Research debate is a generalized local procedure. | [GitHub Spec Kit](LICENSES/github-spec-kit.txt), [Addy Osmani](LICENSES/addy-osmani.txt) |
| `review-and-improve/references/environment-review.md` | Retains the former standalone retrospective capability, adapted and shortened from [Matt Pocock's coding-environment retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md). Automatic infrastructure expansion and fixed reviewer assumptions were removed. | [Matt Pocock](LICENSES/matt-pocock.txt) |
| `write-a-skill` | Rewritten local authoring workflow, informed by the [Agent Skills specification](https://agentskills.io/specification) and Matt Pocock's agent-writing principles, plus a generalized local learnings-maintenance procedure. | [Matt Pocock](LICENSES/matt-pocock.txt) |
| `tldr`, `data-investigation`, `sql-style-guide` | Local workflows and examples, generalized for standalone use. Scientific reasoning and SQL formatting conventions are common methods, not republished company runbooks. | [Project license](LICENSE) |

Handoff implementations reviewed:

- [Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md): [notice](LICENSES/matt-pocock.txt).
- [ToolMonsters](https://github.com/ToolMonsters/handoff-skill/blob/main/SKILL.md): [notice](LICENSES/toolmonsters.txt).
- [espennilsen/pi](https://github.com/espennilsen/pi/blob/main/skills/handoff/SKILL.md): [notice](LICENSES/espennilsen-pi.txt).
- [jumpifequal](https://github.com/jumpifequal/handoff-skill/blob/main/SKILL.md): [notice](LICENSES/jumpifequal.txt).

Upstream license texts were checked on 2026-10-27 and retained without editing their copyright lines, including the placeholder present in the espennilsen/pi source. Notices are included conservatively for adaptations and source-informed rewrites; they do not imply upstream endorsement or that every skill is copied verbatim.

External tools mentioned in documentation remain separate dependencies. No installed plugin bundles, private operational references, agent memories, or conversation logs are distributed here.
