"""Exact, failure-aware grading for one Harbor audit task.

The expected keys live in /tests, which Harbor uploads after the agent phase.
The audited workspace contains neither labels nor this verifier.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


def grade(report_path: Path, expected_path: Path) -> tuple[float, dict]:
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    keys = {(item["cwe"], item["path"], item["line"]) for item in expected}
    result = {
        "expected": len(keys),
        "matched": 0,
        "missed": len(keys),
        "unexpected": 0,
        "duplicate_findings": 0,
        "outcome": "missing_report",
    }
    if not report_path.is_file():
        return 0.0, result
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError("report is not an object")
        if report.get("outcome") != "success":
            result["outcome"] = str(report.get("outcome", "invalid_report"))
            return 0.0, result
        findings = report["findings"]
        if not isinstance(findings, list):
            raise ValueError("findings is not a list")
        found = []
        for item in findings:
            if not isinstance(item, dict):
                raise ValueError("finding is not an object")
            key = (item["cwe"], item["path"], item["line"])
            if not isinstance(key[0], str) or not isinstance(key[1], str):
                raise ValueError("finding key has invalid types")
            if isinstance(key[2], bool) or not isinstance(key[2], int) or key[2] <= 0:
                raise ValueError("finding line is invalid")
            found.append(key)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        result["outcome"] = "invalid_report"
        return 0.0, result
    unique = set(found)
    result.update(
        outcome="success",
        matched=len(unique & keys),
        missed=len(keys - unique),
        unexpected=len(unique - keys),
        duplicate_findings=len(found) - len(unique),
    )
    return float(unique == keys), result


def main() -> int:
    report = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/logs/agent/report.json")
    expected = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/tests/expected.json")
    reward, details = grade(report, expected)
    output = Path("/logs/verifier")
    output.mkdir(parents=True, exist_ok=True)
    (output / "reward.txt").write_text(f"{reward:.1f}\n", encoding="utf-8")
    (output / "details.json").write_text(
        json.dumps(details, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
