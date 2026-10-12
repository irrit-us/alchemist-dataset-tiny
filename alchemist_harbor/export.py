"""Materialize the versioned fixture manifests as standard Harbor tasks.

Run from the submodule with ``python -m alchemist_harbor.export --output DIR``.
The destination must be new. No labels or reference fixes enter the Docker
build context; they are written only to Harbor's delayed verifier/solution dirs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil


FIXTURES = Path(__file__).resolve().parent.parent
BASE_IMAGES = {
    "ajna-protocol-compromise-2": "python:3.12-bookworm",
    "fast-jwt-iss": "node:22-bookworm",
    "filelock-toctou": "python:3.12-bookworm",
    "h11-chunked-framing": "python:3.12-bookworm",
    "pymonocypher-overflow": "python:3.12-bookworm",
    "thin-vec-uaf": "rust:1.90-bookworm",
    "zk-email-sha256": "node:22-bookworm",
}
EXCLUDED = {
    "dataset.json", ".git", "__pycache__", "node_modules", "target", "dist",
    "build", ".venv", "venv", ".pytest_cache", "reference",
}


def _relative(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if not raw or not path.parts or path.is_absolute() or "\\" in raw or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"unsafe relative path: {raw!r}")
    return path


def _check_fixture(audit: Path, case: dict) -> None:
    target = audit.joinpath(*_relative(case["target"]).parts)
    if not target.exists() or target.is_symlink():
        raise ValueError(f"missing or linked target: {target}")
    for entry in case["expected"]:
        source = audit.joinpath(*_relative(entry["path"]).parts)
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"missing or linked expected source: {source}")
        lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
        if not isinstance(entry["line"], int) or not 1 <= entry["line"] <= len(lines):
            raise ValueError(f"invalid expected line: {source}:{entry['line']}")
    for path in audit.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"linked source must not enter Harbor context: {path}")


def _copy_audit(audit: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return set(names) & EXCLUDED

    shutil.copytree(audit, destination, ignore=ignore)
    if sum(path.stat().st_size for path in destination.rglob("*") if path.is_file()) > 64 * 1024 * 1024:
        raise ValueError(f"task source exceeds 64 MiB: {audit}")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _task(audit: Path, fixture: str, case: dict, output: Path) -> None:
    name = case["id"]
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", name):
        raise ValueError(f"invalid case ID: {name!r}")
    task = output / f"{fixture}--{name}"
    task.mkdir()
    _check_fixture(audit, case)
    _copy_audit(audit, task / "environment" / "workdir")
    _write(task / "environment" / "workdir" / ".alchemist-target", case["target"] + "\n")
    base = BASE_IMAGES[fixture]
    _write(
        task / "environment" / "Dockerfile",
        f"FROM {base}\n"
        "RUN apt-get update && apt-get install -y --no-install-recommends "
        "bash git curl ripgrep build-essential python3 && rm -rf /var/lib/apt/lists/*\n"
        "WORKDIR /workspace\nCOPY workdir/ /workspace/\n",
    )
    _write(
        task / "task.toml",
        'schema_version = "1.4"\n'
        f"artifacts = [\"/logs/agent/report.json\"]\n\n"
        "[task]\n"
        f"name = {json.dumps('audit-alchemist/' + fixture + '--' + name)}\n"
        'version = "1.0.0"\n'
        f"description = {json.dumps('Audit ' + fixture + ': ' + name)}\n"
        'keywords = ["security", "audit", "vulnerability"]\n\n'
        "[agent]\ntimeout_sec = 210.0\n\n"
        "[verifier]\ntimeout_sec = 30.0\n\n"
        "[environment]\nworkdir = \"/workspace\"\n",
    )
    _write(task / "instruction.md", case["instruction"].strip() + "\n")
    _write(
        task / "tests" / "expected.json",
        json.dumps(case["expected"], indent=2) + "\n",
    )
    shutil.copyfile(Path(__file__).with_name("verify.py"), task / "tests" / "verify.py")
    _write(task / "tests" / "test.sh", "#!/bin/sh\npython3 /tests/verify.py\n")
    oracle = {
        "case_id": "audit", "outcome": "success", "elapsed_ms": 0,
        "exit_code": 0, "error": None,
        "findings": [
            {**key, "severity": "high", "title": "Expected finding", "evidence": "Oracle fixture"}
            for key in case["expected"]
        ],
    }
    _write(
        task / "solution" / "solve.sh",
        "#!/bin/sh\nmkdir -p /logs/agent\ncat > /logs/agent/report.json <<'REPORT'\n"
        + json.dumps(oracle, indent=2) + "\nREPORT\n",
    )


def export(output: Path, only: set[str] | None = None) -> int:
    output.mkdir(parents=True, exist_ok=False)
    count = 0
    for fixture, _image in BASE_IMAGES.items():
        audit = FIXTURES / fixture / "audit"
        manifest = json.loads((audit / "dataset.json").read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 1:
            raise ValueError(f"unsupported manifest: {fixture}")
        for case in manifest["cases"]:
            if only and case["id"] not in only:
                continue
            _task(audit, fixture, case, output)
            count += 1
    if not count:
        raise ValueError("no cases matched")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", action="append", help="case ID to export; repeatable")
    args = parser.parse_args()
    print(f"Exported {export(args.output, set(args.case) if args.case else None)} Harbor tasks to {args.output}")


if __name__ == "__main__":
    main()
