from __future__ import annotations

import json
from pathlib import Path
import tempfile
import tomllib
import unittest

from alchemist_harbor.export import export
from alchemist_harbor.summarize import summarize
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

    def test_summary_keeps_exact_line_and_clean_rewards_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tasks = root / "tasks"
            tasks.mkdir()
            job = root / "job"
            job.mkdir()
            (job / "result.json").write_text('{"n_total_trials": 2}')
            for name, expected, findings, reward in (
                ("vulnerable", [{"cwe": "CWE-59", "path": "file.py", "line": 3}],
                 [{"cwe": "CWE-78", "path": "file.py", "line": 3}], 0.0),
                ("clean", [], [], 1.0),
            ):
                task = tasks / name
                (task / "tests").mkdir(parents=True)
                (task / "task.toml").write_text(f'[task]\nname = "audit/{name}"\n')
                (task / "tests" / "expected.json").write_text(json.dumps(expected))
                trial = job / name
                (trial / "agent").mkdir(parents=True)
                (trial / "result.json").write_text(json.dumps({
                    "task_name": f"audit/{name}", "exception_info": None,
                    "task_checksum": f"checksum-{name}",
                    "verifier_result": {"rewards": {"reward": reward}},
                }))
                (trial / "agent" / "report.json").write_text(json.dumps({
                    "outcome": "success", "findings": findings,
                }))
                (trial / "agent" / "alchemist-manifest.json").write_text('{"binary_sha256":"same"}')
            summary = summarize(tasks, [job])
            totals = summary["totals"]
            self.assertEqual(summary["missing_manifests"], 0)
            self.assertEqual(totals["reward_mean"], 0.5)
            self.assertEqual((totals["exact"]["tp"], totals["exact"]["fp"], totals["exact"]["fn"]), (0, 1, 1))
            self.assertEqual((totals["line"]["tp"], totals["line"]["fp"], totals["line"]["fn"]), (1, 0, 0))
            trace_dir = job / "vulnerable" / "agent" / "traces"
            trace_dir.mkdir()
            (trace_dir / "audit.jsonl").write_text("\n".join(json.dumps({"event": event}) for event in (
                {"type": "operation", "name": "stream_end", "details": {"bytes": 123}},
                {"type": "operation", "name": "empty_completion_thinking_disabled", "details": {}},
                {"type": "operation", "name": "run_end", "details": {
                    "empty_completions": 2, "output_repairs": 1, "tool_errors": 0,
                    "tools": 4, "turns": 5, "usage": {
                        "prompt_tokens": 100, "completion_tokens": 20,
                        "reasoning_tokens": 10, "total_tokens": 120,
                    },
                }},
            )) + "\n")
            traced = summarize(tasks, [job])
            self.assertEqual(traced["totals"]["trace"]["empty_completions"], 2)
            self.assertEqual(traced["totals"]["trace"]["thinking_fallbacks"], 1)
            self.assertEqual(traced["totals"]["trace"]["max_completed_stream_bytes"], 123)
            self.assertEqual(traced["totals"]["trace"]["usage"]["total_tokens"], 120)
            (job / "clean" / "agent" / "alchemist-manifest.json").write_text('{"binary_sha256":"changed"}')
            with self.assertRaisesRegex(ValueError, "agent configuration changed"):
                summarize(tasks, [job])


if __name__ == "__main__":
    unittest.main()
