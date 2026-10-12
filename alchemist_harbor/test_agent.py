from __future__ import annotations

import asyncio
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

try:
    from alchemist_harbor.agent import AlchemistAgent
except ImportError:
    AlchemistAgent = None


class FakeEnvironment:
    def __init__(self) -> None:
        self.uploads = []
        self.commands = []

    async def upload_file(self, source_path, target_path):
        self.uploads.append((str(source_path), target_path))

    async def exec(self, command, **kwargs):
        self.commands.append((command, kwargs))
        if command == "cat /workspace/.alchemist-target":
            return SimpleNamespace(return_code=0, stdout="src/file.py\n", stderr="")
        return SimpleNamespace(return_code=0, stdout="", stderr="")


@unittest.skipIf(AlchemistAgent is None, "Harbor is not installed")
class AgentIntegrationTests(unittest.TestCase):
    def test_cli_receives_task_target_and_config_without_shell_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "alchemist"
            binary.write_bytes(b"\x7fELFfake")
            environment = FakeEnvironment()
            agent = AlchemistAgent(
                logs_dir=Path(temporary), model_name="example-model",
                binary_path=str(binary), endpoint="https://example.invalid/v1/chat/completions",
                extra_env={"AUDIT_API_KEY": "private-test-key"},
            )
            asyncio.run(agent.setup(environment))
            asyncio.run(agent.run("Audit the target.", environment, None))
            manifest = json.loads((Path(temporary) / "alchemist-manifest.json").read_text())
            self.assertEqual(len(manifest["binary_sha256"]), 64)
            self.assertEqual(len(manifest["config_sha256"]), 64)
            self.assertEqual(len(environment.uploads), 2)
            run_command, options = next(
                (command, kwargs) for command, kwargs in environment.commands
                if " audit " in command
            )
            self.assertIn("--config /tmp/alchemist-node.toml", run_command)
            self.assertIn("--target src/file.py", run_command)
            self.assertIn("> /logs/agent/report.json", run_command)
            self.assertNotIn("private-test-key", run_command)
            self.assertEqual(options["env"]["AUDIT_API_KEY"], "private-test-key")

    def test_api_key_comes_from_host_environment_without_harbor_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "alchemist"
            binary.write_bytes(b"\x7fELFfake")
            agent = AlchemistAgent(
                logs_dir=Path(temporary), model_name="example-model",
                binary_path=str(binary), endpoint="https://example.invalid/v1/chat/completions",
                extra_env={},
            )
            environment = FakeEnvironment()
            with patch.dict("os.environ", {"AUDIT_API_KEY": "host-only-key"}):
                asyncio.run(agent.run("Audit the target.", environment, None))
            run_command, options = next(
                (command, kwargs) for command, kwargs in environment.commands
                if " audit " in command
            )
            self.assertNotIn("host-only-key", run_command)
            self.assertEqual(options["env"]["AUDIT_API_KEY"], "host-only-key")


if __name__ == "__main__":
    unittest.main()
