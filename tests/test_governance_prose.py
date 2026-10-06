from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/antigpt-exec/scripts/check_governance_prose.py"
CONFIG = ROOT / "skills/antigpt-exec/scripts/scanner.toml"


class GovernanceProseTests(unittest.TestCase):
    def run_check(self, text: str, *extra: str):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.md"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--config", str(CONFIG), *extra],
                cwd=temp,
                text=True,
                capture_output=True,
            )

    def test_block_rule_fails_by_default(self):
        proc = self.run_check("This does not mean the design is correct.\n")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("defensive-negation-en", proc.stdout)

    def test_review_rule_does_not_block_default(self):
        proc = self.run_check("I think we should delete the adapter.\n")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        strict = self.run_check("I think we should delete the adapter.\n", "--fail-on", "review")
        self.assertEqual(strict.returncode, 2)

    def test_fenced_inline_code_and_url_are_ignored(self):
        text = """```text\nThis does not mean anything.\n```\nUse `this does not mean` as test text.\nhttps://example.com/this-does-not-mean\n"""
        proc = self.run_check(text)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertNotIn("defensive-negation", proc.stdout)

    def test_reasoned_waiver_applies_to_next_prose_line(self):
        text = """<!-- antigpt: allow rule=defensive-negation-en reason=\"Live distinction in quoted API guarantee\" -->\nThis does not mean the API accepts null.\n"""
        proc = self.run_check(text, "--format", "json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["findings"], [])
        self.assertEqual(payload["waivers"][0]["rule"], "defensive-negation-en")

    def test_bare_waiver_is_invalid(self):
        proc = self.run_check("<!-- antigpt: allow -->\nThis does not mean x.\n")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("invalid-waiver", proc.stdout)

    def test_chinese_block_rule(self):
        proc = self.run_check("这并不意味着系统已经正确。\n")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("defensive-negation-zh", proc.stdout)


if __name__ == "__main__":
    unittest.main()
