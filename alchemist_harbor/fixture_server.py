"""Deterministic local chat-completions fixture for Harbor adapter smoke tests.

This is a protocol plumbing fixture, not an audit-quality measurement.
"""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


def serve(response: str, host: str, port: int) -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            self.rfile.read(length)
            event = {"choices": [{"delta": {"content": response}, "finish_reason": "stop"}]}
            body = ("data: " + json.dumps(event) + "\n\ndata: [DONE]\n\n").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    ThreadingHTTPServer((host, port), Handler).serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8999)
    args = parser.parse_args()
    serve(args.response.read_text(encoding="utf-8"), args.host, args.port)


if __name__ == "__main__":
    main()
