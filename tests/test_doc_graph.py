from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/antigpt-exec/scripts/check_doc_graph.py"


class DocGraphTests(unittest.TestCase):
    def run_graph(self, files: dict[str, str], include: list[str], entries: list[str]):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        config = root / ".docgraph.toml"
        config.write_text(
            "version = 1\n[docgraph]\n"
            + "entries = [" + ", ".join(repr(x) for x in entries) + "]\n"
            + "include = [" + ", ".join(repr(x) for x in include) + "]\n"
            + "exclude = []\nnavigation_heading = \"Navigation\"\n",
            encoding="utf-8",
        )
        proc = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root)], text=True, capture_output=True)
        temp.cleanup()
        return proc

    def test_reciprocal_navigation_passes(self):
        proc = self.run_graph(
            {
                "README.md": "# Root\n## Navigation\n- [Guide](guide.md)\n",
                "guide.md": "# Guide\n## Navigation\n- [Root](README.md)\n",
            },
            ["README.md", "guide.md"],
            ["README.md"],
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_missing_reciprocal_link_fails(self):
        proc = self.run_graph(
            {
                "README.md": "# Root\n## Navigation\n- [Guide](guide.md)\n",
                "guide.md": "# Guide\n",
            },
            ["README.md", "guide.md"],
            ["README.md"],
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("missing reciprocal", proc.stdout)

    def test_orphan_fails(self):
        proc = self.run_graph(
            {"README.md": "# Root\n", "orphan.md": "# Orphan\n"},
            ["README.md", "orphan.md"],
            ["README.md"],
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unreachable", proc.stdout)

    def test_inline_reference_does_not_create_navigation_edge(self):
        proc = self.run_graph(
            {
                "README.md": "# Root\nSee [Guide](guide.md).\n## Navigation\n- [Guide](guide.md)\n",
                "guide.md": "# Guide\n## Navigation\n- [Root](README.md)\nSee [Other](other.md).\n",
                "other.md": "# Other\n## Navigation\n- [Root](README.md)\n",
            },
            ["README.md", "guide.md"],
            ["README.md"],
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
