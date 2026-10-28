# Bundle and installer

Use Python 3.10+ and a dedicated staging directory containing reviewed regular files. This is a selective skill installer, not a home-directory mirror or a settings translator.

```text
portable/
  manifest.json
  skills/
    explain/
      SKILL.md
      references/...
```

`manifest.json` explicitly allowlists each directory:

```json
{
  "version": 1,
  "skills": [
    {"name": "explain", "path": "skills/explain", "profile": "public", "invocation": "natural", "hosts": ["codex", "claude", "gemini"]}
  ]
}
```

Use `public` for distributable reviewed material, `private` for personal-only material, and `company` for company-only material. Profiles classify whole skills, including every resource. A label is not automatic content classification. Review references, metadata, URLs, examples, identifiers, and license/provenance before export. Never transfer an excluded profile merely because installation would skip it: prepare a physically separate personal export containing only selected public/private directories and its reduced manifest.

Resolve `installer` to `scripts/sync_skills.py` beside this skill and set `bundle` to the absolute materialized bundle path on this device. Run a plan first:

```bash
python3 "$installer" --root "$bundle" --manifest "$bundle/manifest.json" \
  --profile public --profile private \
  --target "codex=$HOME/.agents/skills" \
  --target "claude=$HOME/.claude/skills" \
  --discovery-root "codex=$HOME/.codex/skills" \
  --discovery-root "gemini=$HOME/.agents/skills"
```

When an observed root is a symlink, inspect its target and supply the resolved directory; the installer refuses symlinked path components. Supply every other observed active discovery root for each client with `--discovery-root`; duplicates outside supplied roots are not detected. The example installs neutral skills once in the shared Codex/Gemini `.agents/skills` location and separately in Claude; verify Gemini discovery afterward. Host-specific adapters require distinct target directories. A supplied cross-host shared discovery root refuses manual-only or host-excluded entries, since that would widen their behavior. If Codex uses `.agents/skills` and Gemini also discovers that directory, installing the same name again in `.gemini/skills` is a duplicate: select one shared neutral copy or use the existing verified Codex compatibility directory on that device and audit all cross-visible roots. The installer deliberately refuses ambiguous plans. Fresh Gemini installations should use `.gemini/skills` only after checking `.agents/skills`.

With the local destinations authorized, repeat the same command with `--apply`. Different existing content refuses application unless each replacement is selected with `--replace codex:explain` (or its actual host/name) and an explicit `--backup-root` is supplied. The backup root must be on the same filesystem and outside the bundle and every supplied discovery root. Replacements move the entire old skill directory to a unique backup; unrelated skill names remain untouched. To roll back, inspect both versions, move the generated directory aside, and move the recorded backup back to its original destination. The installer never prunes old names or backups.

Optional selection: `--name explain` restricts names. `--profile company --device company` is required for a company profile and still requires authorization for any actual transfer. Personal is the default device classification. Excluded profiles are not read or installed. All selected destinations are planned before any write; application is sequential per skill rather than one transaction. A later filesystem failure can leave earlier selected skills installed; inspect the JSON/error and re-audit before retrying.

The script compares paths, bytes, and executable flags; equal files are untouched. Source symlinks, symlinked path components, linked destinations, non-regular files, secret/local-state names, common credential patterns, merge markers, and `.sync-conflict` artifacts stop the run. Only UTF-8 files of the listed text types and exact extensionless notice basenames `LICENSE` and `NOTICE`, at most 2 MB each, are supported. Notice bytes are preserved and receive the same size, conflict, credential, and UTF-8 checks as other text files. Binary assets require a separately reviewed installation. Inline Markdown links and single-line reference definitions without titles are checked; local resource links must exist inside the bundle. Other reference-definition forms require review; external machine-local references require a reviewed local adapter. Reserved client names and bundled host configuration/plugin directories are refused. Canonical frontmatter accepts only unquoted top-level keys `name`, `description`, optional `license`/`compatibility`, and a two-space `metadata` map of string values. Values are single-line plain strings, JSON double-quoted strings, or YAML single-quoted strings; duplicate keys, multiline scalars, inline comments, aliases, tags, flow maps/lists, quoted keys, and host runtime controls require review. Existing OpenAI sidecars accept only the three string-valued `interface` keys `display_name`, `short_description`, `default_prompt`, and an optional `policy.allow_implicit_invocation` boolean matching the manifest. Those supported source bytes are preserved; other sidecar fields or contradictory policy are refused. Manual invocation adds Claude frontmatter or generates a Codex sidecar when absent. Gemini manual-only remains excluded/refused until its semantics are verified.

The secret scan is a refusal heuristic, not a proof of absence. Run only against reviewed input in a quiescent local staging tree; concurrent adversarial filesystem changes are outside its protection. It reads selected skill contents in memory and does not install dependencies or run bundled skill code. No client inference is needed for the plan/install checks.
