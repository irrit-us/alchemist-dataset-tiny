"""Build the current parent checkout as a Linux binary for Harbor containers."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "target" / "harbor-build" / "x86_64-unknown-linux-gnu" / "release" / "alchemist"


def build() -> Path:
    subprocess.run(
        [
            "docker", "run", "--rm", "-v", f"{ROOT}:/src", "-w", "/src",
            "rust@sha256:59037199c44290f2befcdd58dcc540164763fc296950255aaefeef096a1866b0",
            "sh", "-c",
            "cargo build --locked --release --bin alchemist "
            "--target x86_64-unknown-linux-gnu --target-dir /src/target/harbor-build",
        ],
        check=True,
        timeout=1800,
    )
    if OUTPUT.read_bytes()[:4] != b"\x7fELF":
        raise RuntimeError(f"Docker build did not produce a Linux ELF at {OUTPUT}")
    return OUTPUT


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(build())


if __name__ == "__main__":
    main()
