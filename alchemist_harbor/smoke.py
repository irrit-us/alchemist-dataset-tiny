"""Run one complete Harbor trial with a local deterministic model fixture.

This proves container, adapter, CLI, artifact, and verifier wiring. Its reward
does not measure vulnerability discovery because the response is prescribed.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from alchemist_harbor.build import OUTPUT
from alchemist_harbor.export import export


CASE = "chunked-trailer-not-validated"
TASK = "h11-chunked-framing--" + CASE


def smoke(binary: Path) -> None:
    binary = binary.resolve(strict=True)
    harbor = Path(sys.executable).with_name(
        "harbor.exe" if os.name == "nt" else "harbor"
    )
    if not harbor.is_file():
        raise FileNotFoundError(
            "Harbor executable is missing from this Python environment; "
            "install requirements-harbor.txt"
        )
    with tempfile.TemporaryDirectory(prefix="alchemist-harbor-smoke-") as temporary:
        root = Path(temporary)
        tasks = root / "tasks"
        export(tasks, {CASE})
        task = tasks / TASK
        environment = task / "environment"
        expected = json.loads((task / "tests" / "expected.json").read_text())
        response = {
            "schema_version": 1,
            "findings": [
                {
                    **key,
                    "severity": "high",
                    "title": "Chunk framing mismatch",
                    "evidence": "The chunk reader discards two bytes without validating CRLF.",
                }
                for key in expected
            ],
        }
        shutil.copyfile(Path(__file__).with_name("fixture_server.py"), environment / "fixture_server.py")
        (environment / "response.json").write_text(json.dumps(response), encoding="utf-8")
        (environment / "start-mock.sh").write_text(
            "#!/bin/sh\n"
            "python3 /opt/mock/fixture_server.py --response /opt/mock/response.json "
            "--host 127.0.0.1 --port 8999 >/tmp/mock-provider.log 2>&1 &\n"
            "sleep 1\nexec \"$@\"\n",
            encoding="utf-8",
            newline="\n",
        )
        with (environment / "Dockerfile").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(
                "COPY fixture_server.py response.json /opt/mock/\n"
                "COPY start-mock.sh /usr/local/bin/start-mock.sh\n"
                "RUN chmod 755 /usr/local/bin/start-mock.sh\n"
                'ENTRYPOINT ["/usr/local/bin/start-mock.sh"]\n'
            )
        env = os.environ.copy()
        suite_root = str(Path(__file__).resolve().parent.parent)
        env["PYTHONPATH"] = os.pathsep.join(filter(None, (suite_root, env.get("PYTHONPATH"))))
        env["PYTHONIOENCODING"] = "utf-8"
        env["AUDIT_API_KEY"] = "fake"
        subprocess.run(
            [
                str(harbor), "run", "--path", str(task),
                "--agent", "alchemist_harbor.agent:AlchemistAgent",
                "--model", "mock-model",
                "--ak", f"binary_path={binary}",
                "--ak", "endpoint=http://127.0.0.1:8999/v1/chat/completions",
                "--jobs-dir", str(root / "jobs"),
                "--job-name", "smoke", "--quiet",
            ],
            check=True,
            env=env,
            timeout=900,
        )
        result = json.loads((root / "jobs" / "smoke" / "result.json").read_text())
        saved_config = (root / "jobs" / "smoke" / "config.json").read_text()
        if "AUDIT_API_KEY" in saved_config:
            raise RuntimeError("Harbor serialized the agent credential into its job config")
        stats = result["stats"]
        evals = next(iter(stats["evals"].values()))
        if stats["n_errored_trials"] or evals["metrics"][0]["mean"] != 1.0:
            raise RuntimeError(f"Harbor smoke trial failed: {stats}")
        print("Harbor audit integration smoke passed: reward 1.0")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=OUTPUT)
    args = parser.parse_args()
    smoke(args.binary)


if __name__ == "__main__":
    main()
