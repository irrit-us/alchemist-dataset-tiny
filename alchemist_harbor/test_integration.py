from __future__ import annotations

import json
from pathlib import Path
import tempfile
import tomllib
import unittest

from alchemist_harbor.export import export
from alchemist_harbor.verify import grade


class HarborSuiteTests(unittest.TestCase):
    def test_export_all_cases_without_labels_in_agent_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "tasks"
            self.assertEqual(export(output), 18)
            tasks = list(output.iterdir())
            self.assertEqual(len(tasks), 18)
            for task in tasks:
                config = tomllib.loads((task / "task.toml").read_text())
                self.assertEqual(config["schema_version"], "1.4")
                self.assertEqual(config["environment"]["workdir"], "/workspace")
                self.assertTrue((task / "tests" / "test.sh").is_file())
                self.assertTrue((task / "environment" / "Dockerfile").is_file())
                self.assertFalse(list((task / "environment").rglob("dataset.json")))
                self.assertFalse(list((task / "environment").rglob("expected.json")))
                self.assertFalse(list((task / "environment").rglob("FIX.md")))

    def test_verifier_requires_exact_successful_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = root / "expected.json"
            report = root / "report.json"
            expected.write_text('[{"cwe":"CWE-59","path":"file.py","line":3}]')
            base = {"outcome": "success", "findings": [{"cwe": "CWE-59", "path": "file.py", "line": 3}]}
            report.write_text(json.dumps(base))
            self.assertEqual(grade(report, expected)[0], 1.0)
            base["findings"].append({"cwe": "CWE-78", "path": "file.py", "line": 4})
            report.write_text(json.dumps(base))
            self.assertEqual(grade(report, expected)[0], 0.0)
            base["outcome"] = "timeout"
            report.write_text(json.dumps(base))
            self.assertEqual(grade(report, expected)[0], 0.0)
            report.write_text("[]")
            self.assertEqual(grade(report, expected)[0], 0.0)

    def test_clean_control_rejects_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = root / "expected.json"
            report = root / "report.json"
            expected.write_text("[]")
            report.write_text('{"outcome":"success","findings":[]}')
            self.assertEqual(grade(report, expected)[0], 1.0)
            report.write_text('{"outcome":"success","findings":[{"cwe":"CWE-78","path":"file.py","line":1}]}')
            self.assertEqual(grade(report, expected)[0], 0.0)


if __name__ == "__main__":
    unittest.main()
