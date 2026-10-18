"""Regression cases for prose boundaries, policy calibration, and explicit waivers."""

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts/check/governance_prose.py"
spec = importlib.util.spec_from_file_location("governance_prose", SCRIPT)
assert spec is not None and spec.loader is not None
scanner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scanner
spec.loader.exec_module(scanner)
CONFIG_PATH = SCRIPT.parents[1] / ".config/scanner.toml"
CONFIG = scanner.load_config(CONFIG_PATH)


class ProseScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def scan(self, text, name="sample.md"):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return scanner.scan_file(path, self.root, CONFIG)

    def test_rule_families(self):
        examples = {
            "invented-contrast-en": ("Use plain text, not JSON but ordinary prose.", "review"),
            "invented-contrast-zh": ("不是保留旧入口，而是统一所有者。", "review"),
            "defensive-negation-en": ("That does not mean it works everywhere.", "block"),
            "defensive-negation-zh": ("这并不意味着已经解决全部问题。", "block"),
            "logical-limitation-en": ("The sample cannot prove population-level causation.", "review"),
            "logical-limitation-zh": ("这个样本不足以判断总体趋势。", "review"),
            "trailing-limitation-zh": ("项目完成了本地搜索，不把它说成完整的智能平台。", "review"),
            "self-defensive-reframing-en": (
                "This is not a rejection of testing; it simply means tests should remain proportionate.",
                "block",
            ),
            "self-defensive-reframing-zh": ("这不是反对测试，而是强调适度。", "block"),
            "subjectivization-en": ("I would lean toward removing the adapter.", "review"),
            "subjectivization-zh": ("我认为应该删除适配器。", "review"),
            "commitment-weakening-en": ("You could consider removing it.", "review"),
            "commitment-weakening-zh": ("可以考虑删除旧接口。", "review"),
            "research-deferral-en": ("More research is needed.", "review"),
            "research-deferral-zh": ("需要进一步研究。", "review"),
            "hypothetical-defeater-en": ("There may be unknown consumers.", "review"),
            "hypothetical-defeater-zh": ("未来可能出现外部调用方。", "review"),
            "safety-preface-en": ("To be safe, wait.", "signal"),
            "safety-preface-zh": ("谨慎起见，先等待。", "signal"),
            "preservation-pretext-en": ("Preserve the old adapter to avoid changing existing tests.", "review"),
            "preservation-pretext-zh": ("为了保持最小改动，继续保留重复实现。", "review"),
            "process-substitution-en": (
                "First create an evidence package before implementing the agreed change.",
                "review",
            ),
            "process-substitution-zh": ("必须完成风险矩阵才能实施已定方案。", "review"),
            "correction-memorial-en": ("The old error is no longer present.", "review"),
            "correction-memorial-zh": ("旧的错误已经删除。", "review"),
        }
        examples.update({
            "indirect-agent-instruction-en": ("Prevent the agent from inventing a review ritual.", "review"),
            "policy-self-description-en": ("This skill aims to prevent hallucination.", "review"),
        })
        self.assertEqual(set(examples), {p.key for p in CONFIG.patterns})
        for rule, (text, severity) in examples.items():
            with self.subTest(rule=rule):
                findings, _ = self.scan(text, "SKILL.md" if rule in {"indirect-agent-instruction-en", "policy-self-description-en"} else "sample.md")
                self.assertIn((rule, severity), {(f["rule"], f["class"]) for f in findings})

    def test_non_matches_and_non_blocking_distinctions(self):
        for text in [
            "It is not only faster but safer.",
            "Choose the storage owner and delete the duplicate.",
            "The adapter serves the documented v1 client until its agreed sunset.",
            "Complete the checklist required by the release contract.",
            "I found two conflicting definitions.",
            "Do not preserve the old adapter to avoid changing existing tests.",
            "不要为了避免修改测试而保留旧接口。",
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.scan(text)[0], [])
        for text in [
            "Use the public endpoint, not the internal endpoint, but retain the authentication header.",
            "The sample cannot prove causation.",
        ]:
            self.assertFalse(scanner.should_fail(self.scan(text)[0], "block"))

    def test_ai_only_instruction_voice_and_chinese_false_positive(self):
        sample = "Prevent the agent from inventing tests."
        self.assertEqual(self.scan(sample, "notes.md")[0], [])
        self.assertIn("indirect-agent-instruction-en", {f["rule"] for f in self.scan(sample, "SKILL.md")[0]})
        self.assertEqual(self.scan("不要把用户示例写成全局禁令。", "SKILL.md")[0], [])
        self.assertEqual(self.scan("不把这种情况视为已验证的事实。", "SKILL.md")[0], [])
        self.assertEqual(self.scan("不要把旧测试复制到新架构。", "SKILL.md")[0], [])
        findings, _ = self.scan("项目已完成本地搜索，不把它说成完整平台。", "README.md")
        self.assertIn("trailing-limitation-zh", {f["rule"] for f in findings})
        self.assertFalse(scanner.should_fail(findings, "block"))

    def test_soft_wrap_location_and_boundaries(self):
        findings, _ = self.scan("An intro.\n\n> That does not\n> mean it works everywhere.\n")
        hit = next(f for f in findings if f["rule"] == "defensive-negation-en")
        self.assertEqual((hit["line"], hit["column"], hit["end_line"]), (3, 3, 4))
        for separator in ["\n\n", "\n# Heading\n", "\n- ", "\n```text\ncode\n```\n"]:
            self.assertFalse(
                any(
                    f["rule"] == "defensive-negation-en"
                    for f in self.scan("That does not" + separator + "mean it works.")[0]
                )
            )

    def test_fences_inline_prose_and_original_columns(self):
        text = "````text\n```\nI think this is hidden.\n````\nI think this is visible."
        self.assertEqual([f["line"] for f in self.scan(text)[0]], [5])
        findings, _ = self.scan("`symbol` [docs](https://example.org/a) `I think this is correct.`")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["column"], 41)
        self.assertEqual(self.scan("`I_think` https://example.org/I_think")[0], [])

    def test_comments_do_not_hide_visible_prose(self):
        for text in [
            "That does not mean success. <!-- ordinary comment -->",
            "<!-- hidden --> That does not mean success.",
            "<!-- hidden\n```\ncomment --> That does not mean success.",
        ]:
            findings, _ = self.scan(text)
            self.assertEqual([f["rule"] for f in findings], ["defensive-negation-en"])
        self.assertEqual(self.scan("<!-- That does not mean success. -->")[0], [])
        findings, _ = self.scan("That does not mean success. A sample cannot prove causation.")
        self.assertEqual([f["rule"] for f in findings], ["defensive-negation-en", "logical-limitation-en"])

    def test_stacked_waivers_and_scope(self):
        directives = (
            '<!-- antirlhf: allow rule=subjectivization-en reason="Quoted bad example under discussion" -->\n'
            '<!-- antirlhf: allow rule=defensive-negation-en reason="Quoted bad example under discussion" -->\n'
        )
        findings, waivers = self.scan(
            directives + "> I think that does not\n> mean it is correct.\n\nThat does not mean it is wrong."
        )
        self.assertEqual(len(waivers), 2)
        blocks = [f for f in findings if f["class"] == "block"]
        self.assertEqual([(f["rule"], f["line"]) for f in blocks], [("defensive-negation-en", 6)])
        self.assertEqual(waivers[0]["end_line"], 4)
        for text, expected in [
            (directives, "unused-waiver"),
            (directives + "Clean prose.", "unused-waiver"),
            (directives + directives + "I think that does not mean it works.", "invalid-waiver"),
            ('<!-- antirlhf: allow rule=unknown reason="Specific reason" -->\nText', "invalid-waiver"),
            ('<!-- antirlhf: allow rule=subjectivization-en reason="x" -->\nI think so.', "invalid-waiver"),
        ]:
            with self.subTest(text=text):
                self.assertIn(expected, {f["rule"] for f in self.scan(text)[0]})

    def test_config_and_io_errors_remain_failures(self):
        for suffix in [
            '\n[[patterns]]\nkey = "bad"\nclass = "block"\nregex = "["\nnote = "Fix"\n',
            '\n[[patterns]]\nkey = "invented-contrast-en"\nclass = "block"\nregex = "x"\nnote = "Fix"\n',
        ]:
            path = self.root / "bad.toml"
            path.write_text(CONFIG_PATH.read_text() + suffix)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                result = scanner.main([str(self.root), "--config", str(path), "--format", "json", "--fail-on", "never"])
            self.assertEqual(result, 1)
            self.assertTrue(json.loads(out.getvalue())["errors"])
        path = self.root / "binary.md"
        path.write_bytes(b"\xff")
        for args in [[str(self.root / "missing.md")], [str(path)], [str(path), "--max-bytes", "0"]]:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                result = scanner.main([*args, "--format", "json", "--fail-on", "never"])
            self.assertEqual(result, 1)
            self.assertTrue(json.loads(out.getvalue())["errors"])

    def test_scanner_config_without_project_config(self):
        self.assertEqual(scanner.resolve_config(None, self.root, "scanner.toml"), CONFIG_PATH.resolve())
        config_dir = self.root / ".config" / "arsvine-skills"
        config_dir.mkdir(parents=True)
        local_config = config_dir / "scanner.toml"
        local_config.write_text(CONFIG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(scanner.resolve_config(None, self.root, "scanner.toml"), local_config.resolve())

    def test_archive_is_not_implicitly_exempt(self):
        path = self.root / "archive" / "README.md"
        path.parent.mkdir()
        path.write_text("That does not mean success.")
        args = scanner.parse_args([str(self.root)])
        self.assertIn(path, list(scanner.iter_files(args, self.root, CONFIG)))


if __name__ == "__main__":
    unittest.main()
