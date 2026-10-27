#!/usr/bin/env python3
"""Validate public skill packaging without executing installed skills."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "ask-me": "productivity", "idea-refine": "productivity", "tldr": "productivity",
    "explain": "productivity", "handoff": "productivity",
    "data-investigation": "data-science", "sql-style-guide": "data-science",
    "review-and-improve": "engineering", "write-a-skill": "meta",
}
ROOT_FILES = {"README.md", "LICENSE", "ATTRIBUTIONS.md", "requirements-dev.txt", ".gitignore"}
PACKAGED_DIRS = {"skills", "LICENSES", "docs", "evals", "scripts", "tests", ".github"}
IGNORED_DIRS = {".git", ".venv", "__pycache__"}
LICENSE_FILES = {
    "addy-osmani.txt", "espennilsen-pi.txt", "github-spec-kit.txt",
    "jumpifequal.txt", "matt-pocock.txt", "toolmonsters.txt",
}
SUPPORT_FILES = {
    "docs/ARCHITECTURE.md", "docs/PRIVACY.md", "evals/BEHAVIOR.md", "scripts/validate.py",
    "scripts/check_privacy.py", "tests/test_privacy.py",
    ".github/workflows/validate.yml",
}
# Pattern definitions are not exempt from the package scan.
LEAK_PATTERNS = {
    "private home path": r"/(?:Users|home)/[A-Za-z0-9_.-]+/",
    "private platform path": r"~/(?:\.codex|\.claude|\.agents|second-brain|git)/",
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    "cloud access key": r"\bAKIA[A-Z0-9]{16}\b",
    "provider token": r"\bsk-[A-Za-z0-9_-]{24,}\b",
    "internal deployment identifier": r"\b[a-z0-9]+(?:-[a-z0-9]+)+-(?:staging|production)\b",
    "private dataset owner": r"\buser_[a-z]+_[a-z]+\b",
    "assigned credential": r"\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
    + r"\s*[:=]\s*[\"'][A-Za-z0-9_+/=-]{12,}[\"']",
}
FORBIDDEN_NAMES = {".env", ".metaflow.env", "auth.json", "id_rsa", "id_ed25519"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of overwriting metadata."""


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    """Build a YAML mapping while checking key uniqueness."""
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def validate(root: Path) -> list[str]:
    """Return packaging and content findings for a repository root."""
    errors: list[str] = []
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append(f"{rel}: symlinks are not distributable source files")
            continue
        if len(rel.parts) == 1 and path.name not in ROOT_FILES | PACKAGED_DIRS:
            errors.append(f"{rel}: unexpected top-level package entry")
        if path.is_dir():
            continue
        files.append(path)
        if path.name in FORBIDDEN_NAMES or path.name.startswith(".env."):
            errors.append(f"{rel}: forbidden credential filename")
        if rel.parts[0] in {"docs", "evals", "scripts", "tests", ".github"} and str(rel) not in SUPPORT_FILES:
            errors.append(f"{rel}: unexpected support file")
        if rel.parts[0] == "LICENSES" and (len(rel.parts) != 2 or path.name not in LICENSE_FILES):
            errors.append(f"{rel}: unexpected third-party notice file")
        if rel.parts[0] == "skills":
            if len(rel.parts) < 4 or rel.parts[2] not in EXPECTED_SKILLS:
                errors.append(f"{rel}: unrecognized skill package")
            elif rel.parts[1] != EXPECTED_SKILLS[rel.parts[2]]:
                errors.append(f"{rel}: incorrect category directory")
            if path.suffix not in {".md", ".yaml", ".yml"} and path.name != "LICENSE":
                errors.append(f"{rel}: unexpected skill file type")
            if path.name in {"CHANGELOG.md", "learnings.md"}:
                errors.append(f"{rel}: maintenance history is not packaged")
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(f"{rel}: package files must be readable UTF-8 text")
            continue
        for label, pattern in LEAK_PATTERNS.items():
            if re.search(pattern, content, re.IGNORECASE):
                errors.append(f"{rel}: possible {label}")
        if path.suffix == ".md":
            for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)", content):
                destination = match.group(1).strip("<>")
                parsed = urlsplit(destination)
                if parsed.scheme or destination.startswith("#"):
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root.resolve()) or not target.is_file():
                    errors.append(f"{rel}: missing or escaping local reference {destination}")
    seen: set[str] = set()
    for path in [entry for entry in files if entry.name == "SKILL.md"]:
        rel = path.relative_to(root)
        if len(rel.parts) != 4 or rel.parts[0] != "skills":
            errors.append(f"{rel}: manifest must be skills/category/name/SKILL.md")
            continue
        text = path.read_text()
        if not text.startswith("---\n") or len(text.split("---", 2)) != 3:
            errors.append(f"{rel}: missing or unclosed YAML frontmatter")
            continue
        try:
            data = yaml.load(text.split("---", 2)[1], Loader=UniqueKeyLoader)
        except (yaml.YAMLError, ValueError, TypeError) as error:
            errors.append(f"{rel}: invalid YAML: {error}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: frontmatter must be a mapping")
            continue
        name, description = data.get("name"), data.get("description")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{rel}: invalid skill name")
            continue
        if name in seen:
            errors.append(f"{rel}: duplicate skill name {name}")
        seen.add(name)
        if name != path.parent.name or name not in EXPECTED_SKILLS:
            errors.append(f"{rel}: name does not match expected directory")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{rel}: description must contain 1–1024 characters")
        metadata = data.get("metadata")
        if not isinstance(metadata, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()):
            errors.append(f"{rel}: metadata must map strings to strings")
        elif metadata.get("category") != EXPECTED_SKILLS.get(name):
            errors.append(f"{rel}: missing or mismatched metadata category")
        if data.get("license") != "MIT":
            errors.append(f"{rel}: expected MIT license declaration")
        if data.get("disable-model-invocation") is True:
            errors.append(f"{rel}: expected eligibility for model selection")
        if not (path.parent / "LICENSE").is_file():
            errors.append(f"{rel}: per-skill LICENSE is missing")
        client_path = path.parent / "agents" / "openai.yaml"
        if not client_path.is_file():
            errors.append(f"{rel}: agents/openai.yaml is missing")
        else:
            try:
                client_data = yaml.load(client_path.read_text(), Loader=UniqueKeyLoader)
            except (yaml.YAMLError, ValueError, TypeError) as error:
                errors.append(f"{client_path.relative_to(root)}: invalid YAML: {error}")
            else:
                policy = client_data.get("policy") if isinstance(client_data, dict) else None
                expected_implicit = True
                if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not expected_implicit:
                    errors.append(
                        f"{client_path.relative_to(root)}: allow_implicit_invocation must be {expected_implicit}"
                    )
    if seen != set(EXPECTED_SKILLS):
        errors.append(f"skill inventory mismatch; missing={sorted(set(EXPECTED_SKILLS) - seen)}")
    required_files = (ROOT_FILES - {".gitignore"}) | SUPPORT_FILES | {f"LICENSES/{name}" for name in LICENSE_FILES}
    for required in required_files:
        if not (root / required).is_file():
            errors.append(f"{required}: required package file is missing")
    return errors


def main() -> int:
    """Print validation results and return a process status."""
    errors = validate(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(EXPECTED_SKILLS)} skills and public package boundaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
