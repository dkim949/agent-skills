#!/usr/bin/env python3
"""Check Git snapshots and outgoing history without printing matched values."""
from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import BinaryIO

MAX_BLOB_BYTES = 5 * 1024 * 1024
EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
PUBLIC_EMAIL = re.compile(r"(?i)^[^@]+@(?:users\.noreply\.github\.com|example\.(?:com|org|net))$")
PATTERNS = {
    "home-path": r"(?:/(?:Users|home)/[A-Za-z0-9_.-]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)",
    "private-agent-path": r"~/(?:\.codex|\.claude|\.agents|second-brain|git)/",
    "internal-host": r"(?i)https?://[^\s/]+\.(?:internal|corp)(?:[/:\s]|$)",
}
PRIVATE_PARTS = {".ssh", ".aws", ".gcloud", "agent-memory", "project-memory", "private"}
PRIVATE_FILES = {"auth.json", "credentials.json", ".netrc", ".git-credentials", "id_rsa", "id_ed25519"}


def git(*args: str, optional: bool = False) -> bytes:
    """Run a Git read and keep error output out of logs."""
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode and not optional:
        raise RuntimeError("Git inspection failed; fetch missing objects or fix the repository before retrying")
    return result.stdout if result.returncode == 0 else b""


def policy_patterns() -> dict[str, str]:
    """Load an optional private policy from Git configuration, never the worktree."""
    raw_path = git("config", "--get", "privacy.policyFile", optional=True).decode().strip()
    required = git("config", "--bool", "--get", "privacy.requirePolicy", optional=True).strip() == b"true"
    if not raw_path:
        if required:
            raise RuntimeError("Required private privacy policy is not configured")
        return dict(PATTERNS)
    try:
        path = Path(raw_path).expanduser().resolve(strict=True)
        if path.is_relative_to(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()):
            raise ValueError("private policy must live outside the repository")
        extra = json.loads(path.read_text())["deny_patterns"]
        if not isinstance(extra, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in extra.items()):
            raise ValueError("invalid private policy")
        patterns = dict(PATTERNS)
        for key, value in extra.items():
            if not re.fullmatch(r"[a-z0-9-]+", key):
                raise ValueError("invalid rule identifier")
            re.compile(value)
            patterns["local-" + key] = value
        return patterns
    except (OSError, ValueError, KeyError, TypeError, re.error):
        raise RuntimeError("Private privacy policy is missing or invalid; refusing to continue") from None


class Scan:
    """Inspect bounded Git objects and spool text to the standard secret scanner."""

    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream
        self.patterns = {key: re.compile(value) for key, value in policy_patterns().items()}
        self.findings: set[tuple[str, str]] = set()
        self.seen: set[str] = set()
        self.starts: list[int] = []
        self.locations: list[str] = []
        self.next_line = 1

    def text(self, location: str, content: str) -> None:
        """Check privacy markers and add content to the secret scan input."""
        for key, pattern in self.patterns.items():
            if pattern.search(content):
                self.findings.add((location, key))
        if any(not PUBLIC_EMAIL.fullmatch(match.group()) for match in EMAIL.finditer(content)):
            self.findings.add((location, "non-public-email"))
        self.starts.append(self.next_line)
        self.locations.append(location)
        self.stream.write(content.encode("utf-8") + b"\n")
        self.next_line += content.count("\n") + 1

    def blob(self, mode: str, oid: str, path: str, context: str) -> None:
        """Check names and every unique blob, including files removed in later commits."""
        location = f"{context}:{path}"
        self.text(location + " (path)", path)
        parts = {part.lower() for part in Path(path).parts}
        name = Path(path).name.lower()
        env_file = name == ".env" or name.startswith(".env.") or name.startswith(".metaflow.env")
        example_env = name in {".env.example", ".env.sample", ".env.template"}
        if set(parts) & PRIVATE_PARTS or name in PRIVATE_FILES or (env_file and not example_env):
            self.findings.add((location, "private-filename"))
        if path.endswith((".pem", ".p12", ".pfx", ".key")) or path.endswith(".claude/settings.local.json"):
            self.findings.add((location, "private-filename"))
        if mode not in {"100644", "100755"}:
            self.findings.add((location, "uninspectable-link-or-submodule"))
            return
        if oid in self.seen:
            return
        self.seen.add(oid)
        if int(git("cat-file", "-s", oid)) > MAX_BLOB_BYTES:
            self.findings.add((location, "oversized-uninspected-file"))
            return
        content = git("cat-file", "blob", oid)
        try:
            if b"\0" in content:
                raise UnicodeError
            text = content.decode("utf-8")
        except UnicodeError:
            self.findings.add((location, "binary-or-unreadable-file"))
            return
        self.text(location, text)

    def staged(self) -> None:
        """Inspect the index rather than unstaged working-tree content."""
        for row in git("ls-files", "--stage", "-z").split(b"\0"):
            if row:
                info, path = row.split(b"\t", 1)
                mode, oid, stage = info.decode().split()
                if stage != "0":
                    raise RuntimeError("Unmerged index entries cannot be scanned")
                self.blob(mode, oid, os.fsdecode(path), "index")
        self.text("effective commit identity", git("var", "GIT_AUTHOR_IDENT").decode() + git("var", "GIT_COMMITTER_IDENT").decode())

    def commits(self, revisions: list[str]) -> None:
        """Inspect full snapshots and metadata for a Git revision selection."""
        for oid in git("rev-list", *revisions).decode().splitlines():
            self.text(oid[:12] + " commit metadata", git("show", "-s", "--format=%B%n%an%n%ae%n%cn%n%ce", oid).decode())
            for row in git("ls-tree", "-r", "-z", oid).split(b"\0"):
                if row:
                    info, path = row.split(b"\t", 1)
                    mode, _, blob_oid = info.decode().split()
                    self.blob(mode, blob_oid, os.fsdecode(path), oid[:12])

    def tags(self, oid: str) -> None:
        """Inspect annotations and identities while peeling nested tags."""
        while git("cat-file", "-t", oid).strip() == b"tag":
            content = git("cat-file", "tag", oid).decode()
            self.text(oid[:12] + " tag metadata", content)
            oid = content.splitlines()[0].removeprefix("object ")
            if not re.fullmatch(r"[0-9a-f]{40,64}", oid):
                raise RuntimeError("Invalid annotated tag")

    def push(self, lines: list[str]) -> None:
        """Inspect the actual pushed refs, not the currently checked-out branch."""
        for line in lines:
            fields = line.split()
            if len(fields) != 4:
                raise RuntimeError("Invalid pre-push input")
            local_ref, local_oid, remote_ref, remote_oid = fields
            if not all(re.fullmatch(r"[0-9a-f]{40,64}", oid) for oid in [local_oid, remote_oid]):
                raise RuntimeError("Invalid pre-push object identifier")
            if set(local_oid) == {"0"}:
                continue
            self.text("pushed reference names", local_ref + "\n" + remote_ref)
            self.tags(local_oid)
            commit = git("rev-parse", "--verify", local_oid + "^{commit}").decode().strip()
            selection = [commit]
            if set(remote_oid) != {"0"}:
                base = git("rev-parse", "--verify", remote_oid + "^{commit}").decode().strip()
                selection.append("^" + base)
            self.commits(selection)

    def secrets(self, directory: Path) -> None:
        """Scan all collected text with defaults and no repository-controlled exclusions."""
        binary = shutil.which("gitleaks")
        if not binary:
            raise RuntimeError("Gitleaks is required; install it before committing or pushing")
        config = directory / "scanner.toml"
        config.write_text("[extend]\nuseDefault = true\n")
        report = directory / "report.json"
        self.stream.flush()
        self.stream.seek(0)
        command = [binary, "stdin", "--config", str(config), "--ignore-gitleaks-allow", "--gitleaks-ignore-path", os.devnull,
                   "--redact=100", "--no-banner", "--log-level", "error", "--timeout", "120",
                   "--report-format", "json", "--report-path", str(report)]
        result = subprocess.run(command, stdin=self.stream, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=130)
        if result.returncode not in {0, 1} or not report.is_file():
            raise RuntimeError("Secret scanner failed; refusing to continue")
        findings = json.loads(report.read_text())
        if result.returncode == 1 and not findings:
            raise RuntimeError("Secret scanner returned an incomplete result")
        for finding in findings:
            index = bisect.bisect_right(self.starts, finding["StartLine"]) - 1
            location = self.locations[max(index, 0)] if self.locations else "scan input"
            self.findings.add((location, "secret-" + finding["RuleID"]))

    def print_results(self) -> bool:
        """Report locations and rule identifiers without matched content."""
        for location, rule in sorted(self.findings)[:20]:
            safe = EMAIL.sub("<redacted>", location)
            for pattern in self.patterns.values():
                safe = pattern.sub("<redacted>", safe)
            safe = re.sub(r"(?:gh[pousr]_|sk-)[A-Za-z0-9_-]{12,}", "<redacted>", safe)
            print(f"BLOCKED: {ascii(safe)[:220]} [{rule}]", file=sys.stderr)
        if self.findings:
            print(f"Privacy check failed ({len(self.findings)} findings). No matched values were printed.", file=sys.stderr)
            return False
        print("Privacy check passed: Git content, metadata, and standard secret rules.")
        return True


def main() -> int:
    """Run an index, pre-push, message, or complete-history scan."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["staged", "push", "history", "message"])
    parser.add_argument("--file", type=Path)
    args = parser.parse_args()
    try:
        with tempfile.TemporaryDirectory(prefix="git-privacy-") as temporary:
            directory = Path(temporary)
            with (directory / "input").open("w+b") as stream:
                scan = Scan(stream)
                if args.mode == "staged":
                    scan.staged()
                elif args.mode == "push":
                    scan.push(sys.stdin.read().splitlines())
                elif args.mode == "history":
                    scan.commits(["--all"])
                    for oid in git("for-each-ref", "--format=%(objectname)", "refs/tags").decode().splitlines():
                        scan.tags(oid)
                elif args.file:
                    scan.text("commit message", args.file.read_text())
                else:
                    raise RuntimeError("Commit message path is required")
                scan.secrets(directory)
                return 0 if scan.print_results() else 1
    except RuntimeError as error:
        print(f"Privacy check blocked: {error}.", file=sys.stderr)
        return 2
    except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired):
        print("Privacy check could not finish; operation blocked. Check policy, Git objects, and Gitleaks availability.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
