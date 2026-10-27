"""Exercise privacy failures with synthetic data in disposable Git repositories."""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check_privacy.py"


class PrivacyTests(unittest.TestCase):
    """Check the actual index, outgoing refs, metadata, and local transport."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="privacy-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env["GIT_CONFIG_GLOBAL"] = os.devnull
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Public Author")
        self.git("config", "user.email", "author@users.noreply.github.com")

    def git(self, *args: str, check: bool = True) -> str:
        result = subprocess.run(["git", *args], cwd=self.repo, env=self.env, capture_output=True, text=True)
        if check and result.returncode:
            self.fail("Fixture Git command failed: " + args[0])
        return result.stdout.strip()

    def write(self, path: str, text: str | bytes) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode() if isinstance(text, str) else text)

    def stage(self, path: str, text: str | bytes) -> None:
        self.write(path, text)
        self.git("add", "--", path)

    def commit(self, message: str = "Fixture change") -> str:
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def scan(self, mode: str, stdin: str = "") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(CHECKER), mode], cwd=self.repo, env=self.env,
                              input=stdin, capture_output=True, text=True)

    def company_policy(self) -> str:
        marker = "private-" + "company-" + "sentinel"
        path = self.base / "private-policy.json"
        path.write_text(json.dumps({"deny_patterns": {"company": marker}}))
        self.git("config", "privacy.policyFile", str(path))
        self.git("config", "privacy.requirePolicy", "true")
        return marker

    def push_line(self, oid: str, base: str | None = None) -> str:
        return "refs/heads/main " + oid + " refs/heads/main " + (base or "0" * 40) + "\n"

    def test_clean_index_allows_public_identity(self) -> None:
        self.stage("README.md", "Public Author on GitHub\n")
        self.assertEqual(self.scan("staged").returncode, 0)

    def test_staged_leak_is_blocked_even_if_worktree_is_clean(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", marker)
        self.write("README.md", "clean")
        result = self.scan("staged")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_unstaged_leak_is_not_mistaken_for_published_content(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", "clean")
        self.write("README.md", marker)
        self.assertEqual(self.scan("staged").returncode, 0)

    def test_secret_is_blocked_without_printing_value(self) -> None:
        token = "gh" + "p_" + "aBcD1234" * 5
        self.stage("config.py", "access_token = '" + token + "'\n")
        result = self.scan("staged")
        self.assertEqual(result.returncode, 1)
        self.assertIn("secret-", result.stderr)
        self.assertNotIn(token, result.stdout + result.stderr)

    def test_company_identity_is_blocked(self) -> None:
        self.git("config", "user.email", "person" + "@" + "mail.test")
        self.stage("README.md", "clean")
        self.assertEqual(self.scan("staged").returncode, 1)

    def test_required_missing_policy_blocks(self) -> None:
        self.git("config", "privacy.requirePolicy", "true")
        self.stage("README.md", "clean")
        self.assertEqual(self.scan("staged").returncode, 2)

    def test_policy_inside_repository_is_rejected(self) -> None:
        policy = self.repo / "policy.json"
        policy.write_text('{"deny_patterns": {}}')
        self.git("config", "privacy.policyFile", str(policy))
        self.stage("README.md", "clean")
        self.assertEqual(self.scan("staged").returncode, 2)

    def test_private_filename_blocks_even_when_empty(self) -> None:
        self.stage(".env", "")
        self.assertEqual(self.scan("staged").returncode, 1)

    def test_binary_is_not_silently_skipped(self) -> None:
        self.stage("attachment.bin", b"private\0attachment")
        self.assertEqual(self.scan("staged").returncode, 1)

    def test_symbolic_link_is_not_followed(self) -> None:
        (self.repo / "link").symlink_to(self.base / "outside")
        self.git("add", "link")
        self.assertEqual(self.scan("staged").returncode, 1)

    def test_scanner_filename_has_no_exemption(self) -> None:
        self.stage("scripts/validate.py", self.company_policy())
        self.assertEqual(self.scan("staged").returncode, 1)

    def test_outgoing_deleted_leak_is_still_detected(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", "clean")
        base = self.commit()
        self.stage("leak.txt", marker)
        self.commit()
        self.git("rm", "leak.txt")
        head = self.commit()
        self.assertEqual(self.scan("push", self.push_line(head, base)).returncode, 1)

    def test_remote_history_is_excluded_from_updated_ref(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", marker)
        old = self.commit()
        self.stage("README.md", "clean")
        head = self.commit()
        self.assertEqual(self.scan("push", self.push_line(head, old)).returncode, 0)
        self.assertEqual(self.scan("push", self.push_line(head)).returncode, 1)

    def test_actual_ref_not_current_checkout_is_scanned(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", marker)
        other = self.commit()
        self.stage("README.md", "clean")
        current = self.commit()
        self.assertEqual(self.scan("push", self.push_line(other)).returncode, 1)
        self.assertEqual(self.scan("push", self.push_line(current, other)).returncode, 0)

    def test_tag_identity_and_message_are_scanned(self) -> None:
        self.stage("README.md", "clean")
        self.commit()
        self.git("-c", "user.email=person" + "@" + "mail.test", "tag", "-a", "v1", "-m", "Release")
        tag = self.git("rev-parse", "v1")
        line = "refs/tags/v1 " + tag + " refs/tags/v1 " + "0" * 40 + "\n"
        self.assertEqual(self.scan("push", line).returncode, 1)
        self.assertEqual(self.scan("history").returncode, 1)

    def test_missing_remote_object_blocks(self) -> None:
        self.stage("README.md", "clean")
        head = self.commit()
        self.assertEqual(self.scan("push", self.push_line(head, "a" * 40)).returncode, 2)

    def test_real_pre_push_hook_prevents_local_transport(self) -> None:
        marker = self.company_policy()
        self.stage("README.md", marker)
        self.commit()
        remote = self.base / "remote.git"
        self.git("init", "--bare", str(remote))
        hooks = self.base / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-push"
        hook.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + " " + shlex.quote(str(CHECKER)) + " push\n")
        hook.chmod(0o700)
        self.git("config", "core.hooksPath", str(hooks))
        result = subprocess.run(["git", "push", str(remote), "main"], cwd=self.repo, env=self.env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("ls-remote", str(remote)), "")
        self.assertNotIn(marker.encode(), result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
