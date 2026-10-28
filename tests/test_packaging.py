"""Check the public package inventory and narrowly allowed runtime sources."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("package_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

EXPECTED_SKILLS = {
    "ask-me": "productivity", "idea-refine": "productivity", "tldr": "productivity",
    "explain": "productivity", "handoff": "productivity",
    "concise-work-writing": "productivity", "to-tickets": "productivity",
    "data-investigation": "data-science", "sql-style-guide": "data-science",
    "review-and-improve": "engineering", "goal-loop": "engineering",
    "multi-agent-coordination": "engineering", "run-and-verify": "engineering",
    "safe-local-run": "engineering", "diagnosing-bugs": "engineering",
    "write-a-skill": "meta", "sync-agent-environment": "meta",
}


class PackagingTests(unittest.TestCase):
    """Validate disposable packages without executing their runtime scripts."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="packaging-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        required_files = (validator.ROOT_FILES | validator.SUPPORT_FILES | validator.RUNTIME_FILES
                          | validator.SKILL_NOTICE_FILES
                          | {f"LICENSES/{name}" for name in validator.LICENSE_FILES})
        for path in required_files:
            self.write(path, "Public package fixture.\n")
        for name, category in EXPECTED_SKILLS.items():
            base = f"skills/{category}/{name}"
            self.write(f"{base}/SKILL.md", self.manifest(name, category))
            self.write(f"{base}/LICENSE", "MIT\n")
            self.write(f"{base}/agents/openai.yaml", "policy:\n  allow_implicit_invocation: true\n")

    def write(self, path: str, content: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    @staticmethod
    def manifest(name: str, category: str) -> str:
        return (f"---\nname: {name}\ndescription: Public package fixture.\nlicense: MIT\n"
                f"metadata:\n  category: {category}\n---\n")

    def test_expected_inventory_has_seventeen_skills(self) -> None:
        self.assertEqual(len(EXPECTED_SKILLS), 17)
        self.assertEqual(validator.EXPECTED_SKILLS, EXPECTED_SKILLS)
        self.assertEqual(validator.validate(self.root), [])

    def test_unexpected_runtime_source_is_rejected(self) -> None:
        paths = (
            "skills/engineering/run-and-verify/scripts/extra.sh",
            "skills/engineering/safe-local-run/references/preflight.py",
            "skills/productivity/ask-me/scripts/run_logged.sh",
        )
        for path in paths:
            with self.subTest(path=path):
                target = self.write(path, "#!/bin/sh\nexit 0\n")
                target.chmod(0o755)
                self.assertIn(f"{path}: unexpected skill file type", validator.validate(self.root))
                target.unlink()

    def test_missing_safe_local_run_companion_is_rejected(self) -> None:
        path = "skills/engineering/safe-local-run/scripts/preflight.py"
        (self.root / path).unlink()
        self.assertIn(f"{path}: required package file is missing", validator.validate(self.root))

    def test_runtime_allowance_does_not_exempt_content_scan(self) -> None:
        path = "skills/engineering/safe-local-run/scripts/preflight.py"
        self.write(path, "/" + "Users" + "/" + "fixture" + "/" + "private.txt\n")
        self.assertIn(f"{path}: possible private home path", validator.validate(self.root))

    def test_forbidden_credential_filename_is_rejected(self) -> None:
        path = "skills/engineering/run-and-verify/.env"
        self.write(path, "")
        self.assertIn(f"{path}: forbidden credential filename", validator.validate(self.root))

    def test_runtime_symlink_is_rejected(self) -> None:
        path = "skills/engineering/safe-local-run/scripts/preflight.py"
        target = self.root / path
        target.unlink()
        target.symlink_to(self.root / "README.md")
        self.assertIn(f"{path}: symlinks are not distributable source files", validator.validate(self.root))

    def test_duplicate_manifest_metadata_is_rejected(self) -> None:
        path = "skills/productivity/ask-me/SKILL.md"
        content = self.manifest("ask-me", "productivity").replace(
            "  category: productivity\n", "  category: productivity\n  category: productivity\n"
        )
        self.write(path, content)
        self.assertTrue(any(f"{path}: invalid YAML: duplicate YAML key: category" == error
                            for error in validator.validate(self.root)))

    def test_mismatched_category_is_rejected(self) -> None:
        path = "skills/productivity/ask-me/SKILL.md"
        self.write(path, self.manifest("ask-me", "engineering"))
        self.assertIn(f"{path}: missing or mismatched metadata category", validator.validate(self.root))

    def test_implicit_invocation_policy_is_required(self) -> None:
        path = "skills/productivity/ask-me/agents/openai.yaml"
        self.write(path, "policy:\n  allow_implicit_invocation: false\n")
        self.assertIn(f"{path}: allow_implicit_invocation must be True", validator.validate(self.root))

    def test_mit_declaration_is_required(self) -> None:
        path = "skills/productivity/ask-me/SKILL.md"
        content = self.manifest("ask-me", "productivity").replace("license: MIT", "license: Other")
        self.write(path, content)
        self.assertIn(f"{path}: expected MIT license declaration", validator.validate(self.root))

    def test_unlisted_notice_is_rejected(self) -> None:
        path = "skills/meta/sync-agent-environment/references/extra-LICENSE.txt"
        self.write(path, "Public fixture notice.\n")
        self.assertIn(f"{path}: unexpected skill file type", validator.validate(self.root))

    def test_required_third_party_notice_is_preserved(self) -> None:
        path = "skills/meta/sync-agent-environment/references/legacy-migration-LICENSE.txt"
        (self.root / path).unlink()
        self.assertIn(f"{path}: required package file is missing", validator.validate(self.root))


if __name__ == "__main__":
    unittest.main()
