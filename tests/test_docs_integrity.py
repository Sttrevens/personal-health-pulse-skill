from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocsIntegrityTest(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_ported_guidance_is_discoverable(self):
        combined = "\n".join(
            [
                self.read("personal-health-pulse/SKILL.md"),
                self.read("personal-health-pulse/references/agent-workflow.md"),
                self.read("personal-health-pulse/references/coaching-principles.md"),
                self.read("personal-health-pulse/references/data-schema.md"),
                self.read("personal-health-pulse/examples/event-driven-supervisor.md"),
            ]
        )

        required_terms = [
            "no-token-idle",
            "provisional",
            "official score",
            "Cross-Day Recovery Debt",
            "merge",
            "recent_context",
            "daily_assessments.jsonl",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, combined)

    def test_reusable_docs_do_not_contain_private_identifiers(self):
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "personal-health-pulse").rglob("*")
            if path.is_file()
        )

        forbidden_patterns = [
            r"/Users/[^\\s]+",
            r"Documents/keeping",
            r"ou_[0-9a-f]{12,}",
            r"oc_[0-9a-f]{12,}",
            r"4dgames",
        ]
        for pattern in forbidden_patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, docs))


if __name__ == "__main__":
    unittest.main()
