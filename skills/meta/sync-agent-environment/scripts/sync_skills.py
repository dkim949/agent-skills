#!/usr/bin/env python3
"""Plan or install explicitly allowlisted, neutral skill bundles using stdlib only."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
import stat
import sys
import tempfile
import uuid
from urllib.parse import unquote, urlsplit

HOSTS = {"codex", "claude", "gemini"}
PROFILES = {"public", "private", "company"}
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
CONFLICT = re.compile(rb"(?m)^(?:<{7}|={7}|>{7})(?:\s|$)")
CREDENTIAL_PATTERN = re.compile(
    rb"-----BEGIN (?:[A-Z ]*PRIVATE KEY)-----|"
    rb"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})\b"
)
ASSIGNMENT = re.compile(
    r'''(?im)^\s*["']?(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret|credential)["']?\s*[:=]\s*["']?([^\s"',}]+)'''
)
LOCAL_NAMES = {"auth.json", "credentials.json", "token.json", "tokens.json", ".env", ".metaflow.env", "settings.json", "config.toml", ".mcp.json", ".claude.json", "policy.toml"}
LOCAL_DIRS = {".git", "node_modules", "__pycache__", "sessions", "history", "logs", "backups", "auth", "credentials", "hooks", "mcp", ".claude-plugin", ".claude", ".codex", ".gemini", ".agents"}
TEXT_TYPES = {".md", ".py", ".sh", ".toml", ".yaml", ".yml", ".json", ".txt", ".js", ".ts", ".html", ".css", ".svg"}
TEXT_NOTICES = {"LICENSE", "NOTICE"}


class Rejected(ValueError):
    """A bundle or target requires human review before installation."""


def absolute_path(raw: str) -> Path:
    """Validate a path without silently resolving symlinked components."""
    path = Path(raw).expanduser()
    if not path.is_absolute() or ".." in path.parts:
        raise Rejected("Use an explicit absolute path without '..'")
    for candidate in [path, *path.parents]:
        if candidate.is_symlink():
            raise Rejected(f"Symlinked path requires a materialized local path: {candidate}")
    return path


def mapping(raw: str) -> tuple[str, Path]:
    """Read an explicit host=directory option."""
    host, separator, raw_path = raw.partition("=")
    if not separator or host not in HOSTS:
        raise Rejected("Expected codex=PATH, claude=PATH, or gemini=PATH")
    return host, absolute_path(raw_path)


def read_tree(root: Path, inspect_content: bool = True) -> dict[str, tuple[bytes, bool]]:
    """Read regular files only, rejecting local state and unresolved conflicts."""
    if root.is_symlink() or not root.is_dir():
        raise Rejected(f"Expected a regular directory: {root}")
    files = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_symlink():
            raise Rejected(f"Symlink inside skill: {rel}")
        if any(".sync-conflict" in part or part in LOCAL_DIRS for part in rel.parts):
            raise Rejected(f"Conflict or local-state path: {rel}")
        if path.is_dir():
            continue
        mode = path.stat().st_mode
        if not stat.S_ISREG(mode):
            raise Rejected(f"Non-regular file: {rel}")
        if path.stat().st_size > 2_000_000:
            raise Rejected(f"Review large files separately: {rel}")
        data = path.read_bytes()
        if CONFLICT.search(data):
            raise Rejected(f"Unresolved merge markers: {rel}")
        if inspect_content:
            if (path.name.lower() in LOCAL_NAMES or path.name.startswith(".env.")
                    or path.suffix.lower() in {".key", ".pem", ".p12", ".pfx"}
                    or path.name.lower().startswith(("token.", "credentials."))):
                raise Rejected(f"Device-local or secret filename: {rel}")
            if path.suffix.lower() not in TEXT_TYPES and path.name not in TEXT_NOTICES:
                raise Rejected(f"Review unsupported asset type separately: {rel}")
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise Rejected(f"Only reviewed UTF-8 text is supported: {rel}") from exc
            if CREDENTIAL_PATTERN.search(data):
                raise Rejected(f"Possible credential material: {rel}")
            for value in ASSIGNMENT.findall(content):
                if value.lower() not in {"example", "placeholder", "redacted", "none", "null", "true", "false"} and not value.startswith(("$", "<", "os.environ", "process.env")):
                    raise Rejected(f"Possible literal credential assignment: {rel}")
        files[rel.as_posix()] = (data, bool(mode & 0o111))
    return files


def validate_links(files: dict) -> None:
    """Keep Markdown resource links inside the reviewed skill bundle."""
    for name, (data, _) in files.items():
        if not name.endswith(".md"):
            continue
        content = data.decode("utf-8")
        links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content)
        for definition in re.findall(r"(?m)^ {0,3}\[[^\]]+\]:[ \t]*(.*)$", content):
            # A bounded subset: one destination on the definition's own line.
            if not definition or re.search(r"\s", definition.strip("<>")):
                raise Rejected(f"Review unsupported Markdown reference syntax: {name}")
            links.append(definition)
        for raw in links:
            link = raw.strip().strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme in {"https", "http", "mailto"} or not parsed.path:
                continue
            if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
                raise Rejected(f"Machine-specific Markdown link requires review: {name}")
            relative = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path)))
            if relative.startswith("../") or relative == "..":
                raise Rejected(f"Markdown link escapes its skill bundle: {name}")
            if relative not in files and not any(path.startswith(relative.rstrip("/") + "/") for path in files):
                raise Rejected(f"Missing bundled Markdown resource: {name} -> {relative}")


def parse_scalar(value: str) -> str | bool:
    """Read one supported YAML scalar, rejecting advanced or ambiguous syntax."""
    if value.startswith('"'):
        scalar = json.loads(value)
        if not isinstance(scalar, str):
            raise Rejected("Expected a quoted string")
        return scalar
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise Rejected("Unsupported single-quoted YAML scalar")
        return value[1:-1].replace("''", "'")
    if value in {"true", "false"}:
        return value == "true"
    if (not value or value[0] in "[{&*!|>@`%?:-'\"" or ": " in value or " #" in value
            or value.lower() in {"null", "~", "yes", "no", "on", "off"}
            or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", value)):
        raise Rejected("Use a supported single-line quoted string")
    return value


def parse_mapping(content: str) -> dict:
    """Read plain keys and at most one nested mapping; reject other YAML forms."""
    result = {}
    nested = None
    for line in content.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"( {0}| {2})([a-z][a-z0-9_-]*):(?: +(.*))?", line)
        if not match:
            raise Rejected("Use unquoted YAML keys, single-line scalars, and two-space map indentation")
        indentation, key, value = match.groups()
        if indentation:
            if nested is None or value is None or key in nested:
                raise Rejected("Invalid or duplicate nested YAML key")
            nested[key] = parse_scalar(value)
        else:
            if key in result:
                raise Rejected("Duplicate YAML key")
            result[key] = {} if value is None else parse_scalar(value)
            nested = result[key] if isinstance(result[key], dict) else None
    return result


def validate_sidecar(files: dict, invocation: str) -> None:
    """Preserve known UI metadata only when its declared policy matches the manifest."""
    if "agents/openai.yaml" not in files:
        return
    sidecar = parse_mapping(files["agents/openai.yaml"][0].decode("utf-8"))
    if set(sidecar) - {"interface", "policy"}:
        raise Rejected("OpenAI sidecar supports only reviewed interface and invocation policy")
    interface = sidecar.get("interface", {})
    if (not isinstance(interface, dict) or set(interface) - {"display_name", "short_description", "default_prompt"}
            or any(not isinstance(value, str) for value in interface.values())):
        raise Rejected("Unsupported OpenAI interface metadata")
    policy = sidecar.get("policy", {})
    if (not isinstance(policy, dict) or set(policy) - {"allow_implicit_invocation"}
            or any(not isinstance(value, bool) for value in policy.values())):
        raise Rejected("Unsupported OpenAI invocation policy")
    expected = invocation == "natural"
    if policy.get("allow_implicit_invocation", True) != expected:
        raise Rejected("OpenAI invocation policy disagrees with the manifest")


def render(files: dict, entry: dict, host: str) -> dict:
    """Render only documented manual-only adapters; preserve neutral bytes."""
    files = dict(files)
    try:
        text = files["SKILL.md"][0].decode("utf-8")
    except KeyError as exc:
        raise Rejected(f"Missing SKILL.md: {entry['name']}") from exc
    sections = text.split("---\n", 2)
    if len(sections) != 3 or sections[0] != "":
        raise Rejected("SKILL.md needs LF-delimited YAML frontmatter")
    header = sections[1]
    metadata = parse_mapping(header)
    if set(metadata) - {"name", "description", "license", "compatibility", "metadata"}:
        raise Rejected("Canonical SKILL.md supports only neutral top-level fields")
    if (metadata.get("name") != entry["name"] or not isinstance(metadata.get("description"), str)
            or not metadata["description"] or len(metadata["description"]) > 1024):
        raise Rejected("Manifest and SKILL.md name/description must agree")
    if any(not isinstance(value, str) for key, value in metadata.items() if key != "metadata"):
        raise Rejected("Neutral frontmatter fields must be strings")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(not isinstance(value, str) for value in extra.values()):
        raise Rejected("metadata must be a map of string values")
    validate_sidecar(files, entry["invocation"])
    if entry["invocation"] == "manual":
        if host == "gemini":
            raise Rejected("Gemini manual-only policy has no verified adapter")
        if host == "claude":
            adapted = "---\n" + header + "disable-model-invocation: true\n---\n" + sections[2]
            files["SKILL.md"] = (adapted.encode(), files["SKILL.md"][1])
        elif "agents/openai.yaml" not in files:
            files["agents/openai.yaml"] = (b"policy:\n  allow_implicit_invocation: false\n", False)
    return files


def digest(files: dict) -> str:
    """Hash paths, bytes, and executable flags rather than link destinations."""
    result = hashlib.sha256()
    for name, (data, executable) in sorted(files.items()):
        result.update(json.dumps([name, executable, len(data)]).encode() + b"\0" + data)
    return result.hexdigest()


def load_manifest(root: Path, manifest: Path) -> list[dict]:
    """Validate the small supported allowlist schema."""
    if not manifest.is_relative_to(root) or manifest.is_symlink():
        raise Rejected("Manifest must be a regular file inside the bundle root")
    data = manifest.read_bytes()
    if b".sync-conflict" in data or CONFLICT.search(data):
        raise Rejected("Manifest contains unresolved conflicts")
    document = json.loads(data)
    if set(document) != {"version", "skills"} or document["version"] != 1 or not isinstance(document["skills"], list):
        raise Rejected("Expected version 1 and skills array")
    seen = set()
    for entry in document["skills"]:
        if not isinstance(entry, dict) or set(entry) != {"name", "path", "profile", "invocation", "hosts"}:
            raise Rejected("Each skill needs name, path, profile, invocation, hosts")
        name = entry["name"]
        if not isinstance(name, str) or len(name) > 64 or not NAME.fullmatch(name) or name in {"synced", "anthropic-skills"} or name in seen:
            raise Rejected("Invalid or duplicate skill name")
        seen.add(name)
        if entry["path"] != f"skills/{name}":
            raise Rejected("Skill paths must be skills/<name>")
        if entry["profile"] not in PROFILES or entry["invocation"] not in {"natural", "manual"}:
            raise Rejected("Unknown profile or invocation")
        hosts = entry["hosts"]
        if not isinstance(hosts, list) or not hosts or any(host not in HOSTS for host in hosts) or len(set(hosts)) != len(hosts):
            raise Rejected("hosts must list distinct supported clients")
    return document["skills"]


def plan(args: argparse.Namespace) -> list[dict]:
    """Plan all destinations before any write; fail on conflicting discovery."""
    root = absolute_path(args.root)
    manifest = absolute_path(args.manifest)
    entries = load_manifest(root, manifest)
    if any(".sync-conflict" in path.name for path in root.rglob("*")):
        raise Rejected("Resolve Syncthing conflict files before planning")
    if args.name and not set(args.name).issubset({entry["name"] for entry in entries}):
        raise Rejected("A selected name is absent from the manifest")
    if "company" in args.profile and args.device != "company":
        raise Rejected("Company profile requires an explicitly selected company device")
    targets = [mapping(value) for value in args.target]
    if len({host for host, _ in targets}) != len(targets):
        raise Rejected("Choose one target directory per host")
    if any(left != right and (left.is_relative_to(right) or right.is_relative_to(left)) for _, left in targets for _, right in targets):
        raise Rejected("Target discovery directories must not nest")
    if len({path for _, path in targets}) != len(targets):
        raise Rejected("Host-specific adapters require distinct target directories")
    discovery = [mapping(value) for value in args.discovery_root]
    rows = []
    for entry in entries:
        if args.name and entry["name"] not in args.name:
            continue
        if entry["profile"] not in args.profile:
            rows.append({"name": entry["name"], "status": "excluded", "profile": entry["profile"]})
            continue
        source = absolute_path(str(root / entry["path"]))
        source_files = read_tree(source)
        validate_links(source_files)
        for host, target in targets:
            if host not in entry["hosts"]:
                rows.append({"name": entry["name"], "host": host, "status": "unsupported-host"})
                continue
            destination = target / entry["name"]
            if destination.is_relative_to(root) or root.is_relative_to(destination):
                raise Rejected("Source bundle and destination must not overlap")
            for discovery_host, discovery_root in discovery + targets:
                if discovery_host != host:
                    continue
                planned_duplicate = discovery_root != target and any(other_root == discovery_root and other_host in entry["hosts"] for other_host, other_root in targets)
                existing_duplicate = False
                if discovery_root.exists():
                    for skill_file in discovery_root.glob("*/SKILL.md"):
                        if skill_file.parent == destination:
                            continue
                        if skill_file.stat().st_size > 2_000_000:
                            raise Rejected("Review large discovery metadata separately")
                        skill_text = skill_file.read_text(encoding="utf-8")
                        same_name = re.search(r"(?m)^[ \t]*(?:name|\"name\"|'name')[ \t]*:[ \t]*[\"']?" + re.escape(entry["name"]) + r"[\"']?[ \t]*$", skill_text)
                        existing_duplicate |= bool(same_name) or skill_file.parent.name == entry["name"]
                if planned_duplicate or existing_duplicate:
                    raise Rejected(f"Duplicate discovery entry requires review: {discovery_root / entry['name']}")
            for visible_host, visible_root in discovery + targets:
                if visible_host != host and visible_root == target:
                    if visible_host not in entry["hosts"] or entry["invocation"] == "manual":
                        raise Rejected("Shared discovery would expose unsupported host or manual-only semantics")
            expected = render(source_files, entry, host)
            actual = read_tree(destination, inspect_content=False) if destination.exists() else None
            if destination.is_symlink():
                raise Rejected(f"Existing linked destination requires materialization review: {destination}")
            status = "equal" if actual == expected else "replace" if actual is not None else "add"
            rows.append({"name": entry["name"], "host": host, "status": status,
                         "destination": str(destination), "sha256": digest(expected),
                         "_files": expected, "_prior": digest(actual) if actual is not None else None})
    return rows


def apply(rows: list[dict], replacements: list[str], backup_root: Path | None) -> None:
    """Install selected files with colocated backups; leave unrelated names intact."""
    valid = {f"{row.get('host')}:{row['name']}" for row in rows if row["status"] == "replace"}
    if set(replacements) - valid:
        raise Rejected("--replace must select a planned host:name replacement")
    if valid - set(replacements):
        raise Rejected("Different existing content requires --replace host:name")
    if valid and backup_root is None:
        raise Rejected("Replacements require an explicit --backup-root outside discovery")
    for row in rows:
        if row["status"] not in {"add", "replace"}:
            continue
        destination = absolute_path(row["destination"])
        actual = read_tree(destination, inspect_content=False) if destination.exists() else None
        if (digest(actual) if actual is not None else None) != row["_prior"]:
            raise Rejected("Destination changed after planning; rerun dry-run")
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".sync-stage-", dir=destination.parent.parent))
        backup = None
        try:
            for relative, (data, executable) in row["_files"].items():
                path = staging / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                path.chmod(0o755 if executable else 0o644)
            if actual is not None:
                backup_root.mkdir(parents=True, exist_ok=True)
                backup = backup_root / f"{destination.name}-{uuid.uuid4().hex}"
                destination.rename(backup)
                row["backup"] = str(backup)
            try:
                os.rename(staging, destination)
            except OSError:
                if backup is not None and not destination.exists():
                    backup.rename(destination)
                raise
            if read_tree(destination, inspect_content=False) != row["_files"]:
                raise Rejected(f"Installed content verification failed: {destination}")
        finally:
            if staging.exists():
                shutil.rmtree(staging)


def main() -> int:
    """Run a read-only plan unless --apply is explicit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--target", action="append", required=True, help="host=/absolute/skills/directory")
    parser.add_argument("--discovery-root", action="append", default=[], help="Other active host=directory to inspect for duplicates")
    parser.add_argument("--profile", action="append", choices=sorted(PROFILES), required=True)
    parser.add_argument("--device", choices=["personal", "company"], default="personal")
    parser.add_argument("--name", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-root", help="Reversible backups outside bundle and all discovery roots")
    parser.add_argument("--replace", action="append", default=[], help="Explicit host:name replacement; never deletes other names")
    args = parser.parse_args()
    try:
        rows = plan(args)
        if args.apply:
            backup_root = absolute_path(args.backup_root) if args.backup_root else None
            if backup_root is not None:
                protected = [absolute_path(args.root)] + [mapping(value)[1] for value in args.target + args.discovery_root]
                if any(backup_root.is_relative_to(path) or path.is_relative_to(backup_root) for path in protected):
                    raise Rejected("Backup root must not overlap the bundle or discovery roots")
            apply(rows, args.replace, backup_root)
        for row in rows:
            row.pop("_files", None)
            row.pop("_prior", None)
        print(json.dumps({"mode": "applied" if args.apply else "dry-run", "items": rows}, indent=2))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
