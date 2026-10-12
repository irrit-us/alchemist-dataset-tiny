"""Summarize Harbor audit trials using the exported, verifier-only labels.

Pass one or more completed job directories. Separate jobs are independent
repeats; Harbor's --n-attempts is a retry setting, not a repeat count.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import median
import tomllib


def _keys(items: list[dict]) -> set[tuple[str, str, int]]:
    keys = set()
    for item in items:
        cwe, path, line = item["cwe"], item["path"], item["line"]
        if not isinstance(cwe, str) or not isinstance(path, str):
            raise ValueError("finding key has invalid types")
        if isinstance(line, bool) or not isinstance(line, int) or line <= 0:
            raise ValueError("finding line is invalid")
        keys.add((cwe, path, line))
    return keys


def _score(expected: set[tuple], found: set[tuple]) -> dict:
    tp = len(expected & found)
    fp = len(found - expected)
    fn = len(expected - found)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def _display_keys(keys: set[tuple[str, str, int]]) -> list[dict]:
    return [{"cwe": cwe, "path": path, "line": line} for cwe, path, line in sorted(keys)]


def _failure_class(report: dict | None) -> str | None:
    if report is None:
        return "missing_or_invalid_report"
    if report.get("outcome") == "success":
        return None
    error = str(report.get("error") or "")
    if "model response contained no output text or tool calls" in error:
        return "empty_model_completion"
    if "finish_reason length" in error:
        return "response_length"
    return str(report.get("outcome") or "invalid_report")


def _totals(rows: list[dict]) -> dict:
    exact = {"tp": 0, "fp": 0, "fn": 0}
    line = {"tp": 0, "fp": 0, "fn": 0}
    for row in rows:
        for name, target in (("exact", exact), ("line", line)):
            for field in target:
                target[field] += row[name][field]
    for target in (exact, line):
        tp, fp, fn = target["tp"], target["fp"], target["fn"]
        target["precision"] = tp / (tp + fp) if tp + fp else None
        target["recall"] = tp / (tp + fn) if tp + fn else None
        target["f1"] = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
    latencies = [
        row["elapsed_ms"] for row in rows
        if row["completed"] and row["elapsed_ms"] is not None
    ]
    failures = Counter(row["failure_class"] for row in rows if row["failure_class"] is not None)
    return {
        "trials": len(rows),
        "completed": sum(row["completed"] for row in rows),
        "errored": sum(row["errored"] for row in rows),
        "reward_sum": sum(row["reward"] for row in rows),
        "reward_mean": sum(row["reward"] for row in rows) / len(rows) if rows else None,
        "outcomes": dict(sorted(Counter(row["outcome"] for row in rows).items())),
        "failure_classes": dict(sorted(failures.items())),
        "median_completed_elapsed_ms": median(latencies) if latencies else None,
        "exact": exact,
        "line": line,
    }


def summarize(tasks: Path, jobs: list[Path]) -> dict:
    if len({job.resolve() for job in jobs}) != len(jobs):
        raise ValueError("duplicate Harbor job path")
    labels = {}
    for task in sorted(tasks.iterdir()):
        if task.is_dir() and (task / "task.toml").is_file():
            name = tomllib.loads((task / "task.toml").read_text(encoding="utf-8"))["task"]["name"]
            if name in labels:
                raise ValueError(f"duplicate Harbor task name: {name}")
            labels[name] = _keys(json.loads((task / "tests" / "expected.json").read_text(encoding="utf-8")))
    if not labels:
        raise ValueError("no exported Harbor tasks found")
    rows = []
    agent_manifest = None
    task_checksums = {}
    prior_task_set = None
    missing_manifests = 0
    for job in jobs:
        job_result_path = job / "result.json"
        if not job_result_path.is_file():
            raise ValueError(f"Harbor job is not complete: {job}")
        job_result = json.loads(job_result_path.read_text(encoding="utf-8"))
        seen = set()
        for trial in sorted(job.iterdir()):
            result_path = trial / "result.json"
            if not result_path.is_file():
                continue
            result = json.loads(result_path.read_text(encoding="utf-8"))
            name = result["task_name"]
            if name not in labels:
                raise ValueError(f"unrecognized task in {job}: {name}")
            if name in seen:
                raise ValueError(f"duplicate task in {job}: {name}")
            seen.add(name)
            checksum = result.get("task_checksum")
            if not checksum:
                raise ValueError(f"missing task checksum in {trial}")
            if name in task_checksums and task_checksums[name] != checksum:
                raise ValueError(f"task source changed between jobs: {name}")
            task_checksums[name] = checksum
            manifest_path = trial / "agent" / "alchemist-manifest.json"
            if manifest_path.is_file():
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if agent_manifest is not None and manifest != agent_manifest:
                    raise ValueError(f"agent configuration changed between trials: {trial}")
                agent_manifest = manifest
            else:
                missing_manifests += 1
            report_path = trial / "agent" / "report.json"
            try:
                report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else None
                found = _keys(report["findings"]) if isinstance(report, dict) else set()
            except (OSError, ValueError, KeyError, TypeError):
                report = None
                found = set()
            completed = (
                result.get("exception_info") is None
                and isinstance(report, dict)
                and report.get("outcome") == "success"
                and isinstance(report.get("findings"), list)
            )
            if not completed:
                found = set()
            expected = labels[name]
            reward = ((result.get("verifier_result") or {}).get("rewards") or {}).get("reward")
            if reward is None:
                reward = 0.0
            if isinstance(reward, bool) or reward not in (0, 0.0, 1, 1.0):
                raise ValueError(f"invalid reward in {trial}: {reward}")
            if bool(reward) != bool(completed and found == expected):
                raise ValueError(f"Harbor reward disagrees with exact labels in {trial}")
            elapsed = report.get("elapsed_ms") if isinstance(report, dict) else None
            if isinstance(elapsed, bool) or not isinstance(elapsed, int) or elapsed < 0:
                elapsed = None
            rows.append({
                "job": job.name,
                "task": name,
                "completed": bool(completed),
                "errored": result.get("exception_info") is not None,
                "reward": float(reward),
                "outcome": report.get("outcome", "invalid_report") if isinstance(report, dict) else "missing_report",
                "failure_class": _failure_class(report),
                "elapsed_ms": elapsed,
                "expected_keys": _display_keys(expected),
                "reported_keys": _display_keys(found),
                "exact": _score(expected, found),
                "line": _score({(path, line) for _, path, line in expected},
                               {(path, line) for _, path, line in found}),
            })
        if len(seen) != job_result["n_total_trials"]:
            raise ValueError(f"missing trial results in {job}: {len(seen)} of {job_result['n_total_trials']}")
        if not seen:
            raise ValueError(f"no trial results in {job}")
        if prior_task_set is not None and seen != prior_task_set:
            raise ValueError(f"task set changed between jobs: {job}")
        prior_task_set = seen
    cases = {name: _totals([row for row in rows if row["task"] == name]) for name in labels}
    return {
        "schema_version": 1,
        "jobs": [job.name for job in jobs],
        "agent_manifest": agent_manifest,
        "missing_manifests": missing_manifests,
        "task_checksums": task_checksums,
        "totals": _totals(rows),
        "distinct": {
            "exact": len({row["task"] for row in rows if row["exact"]["tp"]}),
            "line": len({row["task"] for row in rows if row["line"]["tp"]}),
        },
        "cases": cases,
        "trials": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--job", type=Path, required=True, action="append")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(summarize(args.tasks, args.job), indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
