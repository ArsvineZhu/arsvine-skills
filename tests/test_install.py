from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install.py"


class InstallTests(unittest.TestCase):
    def test_install_is_idempotent_and_preserves_other_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            instructions = root / "AGENTS.md"
            skills = root / "skills"
            instructions.write_text("# Existing\n\nKeep this rule.\n", encoding="utf-8")
            command = [
                sys.executable,
                str(SCRIPT),
                "--instructions-file",
                str(instructions),
                "--skills-dir",
                str(skills),
                "--skill",
                "session-handoff",
            ]
            first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            content = instructions.read_text(encoding="utf-8")
            self.assertIn("Keep this rule.", content)
            self.assertEqual(content.count("arsvine-skills:antigpt-constitution:start"), 1)
            self.assertTrue((skills / "session-handoff" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
