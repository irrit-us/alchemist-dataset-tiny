"""Custom Harbor agent that runs the bounded Alchemist CLI in a task container."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import shlex

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext


class AlchemistAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "audit-alchemist"

    def __init__(
        self,
        logs_dir: Path,
        model_name: str | None = None,
        *,
        binary_path: str,
        config_path: str | None = None,
        endpoint: str | None = None,
        wire_api: str = "chat-completions",
        auth: str = "api-key",
        timeout_ms: int = 180000,
        **kwargs,
    ) -> None:
        super().__init__(logs_dir=logs_dir, model_name=model_name, **kwargs)
        self.binary_path = Path(binary_path).resolve(strict=True)
        with self.binary_path.open("rb") as stream:
            magic = stream.read(4)
            stream.seek(0)
            self.binary_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
        if magic != b"\x7fELF":
            raise ValueError("binary_path must be a Linux ELF executable")
        self.config_path = (
            Path(config_path).resolve(strict=True)
            if config_path
            else Path(__file__).with_name("node.toml")
        )
        self.config_sha256 = hashlib.sha256(self.config_path.read_bytes()).hexdigest()
        if not model_name:
            raise ValueError("Harbor --model is required")
        if auth == "api-key" and not endpoint:
            raise ValueError("endpoint is required for API-key authentication")
        if auth not in ("api-key", "codex"):
            raise ValueError("auth must be api-key or codex")
        self.endpoint = endpoint
        self.wire_api = wire_api
        self.auth = auth
        self.timeout_ms = int(timeout_ms)

    def version(self) -> str | None:
        return f"0.1.2+{self.binary_sha256[:12]}"

    async def setup(self, environment: BaseEnvironment) -> None:
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        (self.logs_dir / "alchemist-manifest.json").write_text(
            json.dumps(
                {
                    "binary_sha256": self.binary_sha256,
                    "config_sha256": self.config_sha256,
                    "model": self.model_name,
                    "wire_api": self.wire_api,
                    "auth": self.auth,
                    "timeout_ms": self.timeout_ms,
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        await environment.upload_file(self.binary_path, "/usr/local/bin/alchemist")
        await environment.upload_file(self.config_path, "/tmp/alchemist-node.toml")
        result = await environment.exec("chmod 755 /usr/local/bin/alchemist")
        if result.return_code != 0:
            raise RuntimeError(f"cannot install alchemist: {result.stderr}")

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        target_result = await environment.exec("cat /workspace/.alchemist-target")
        if target_result.return_code != 0:
            raise RuntimeError("task target metadata is missing")
        target = target_result.stdout.strip()
        path = PurePosixPath(target)
        if not target or path.is_absolute() or ".." in path.parts or "\\" in target:
            raise ValueError("invalid task target")
        args = [
            "/usr/local/bin/alchemist", "--config", "/tmp/alchemist-node.toml",
            "audit", "--root", "/workspace",
            "--target", target, "--instruction", instruction,
            "--model", self.model_name, "--auth", self.auth,
            "--wire-api", self.wire_api, "--timeout-ms", str(self.timeout_ms),
            "--format", "quiet",
        ]
        if self.endpoint:
            args.extend(("--endpoint", self.endpoint))
        command = " ".join(shlex.quote(part) for part in args)
        command += " > /logs/agent/report.json"
        env = dict(self.extra_env)
        if self.auth == "api-key":
            key = env.get("AUDIT_API_KEY") or os.environ.get("AUDIT_API_KEY")
            if not key:
                raise ValueError("AUDIT_API_KEY is required in the Harbor process environment")
            env["AUDIT_API_KEY"] = key
        result = await environment.exec(
            command,
            env=env,
            cwd="/workspace",
            timeout_sec=max(1, self.timeout_ms // 1000 + 10),
        )
        if result.return_code != 0:
            diagnostic = (result.stderr or result.stdout or "").strip()[-2000:]
            raise RuntimeError(
                f"alchemist exited {result.return_code}: {diagnostic}"
            )
        check = await environment.exec("test -s /logs/agent/report.json")
        if check.return_code != 0:
            raise RuntimeError("alchemist produced no report")
