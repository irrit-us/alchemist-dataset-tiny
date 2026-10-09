# h11 malformed chunked framing (CVE-2025-43859)

Real-world protocol-parsing fixture: `python-hyper/h11` 0.14.0 (vulnerable) →
0.16.0 (fixed). Advisory [GHSA-vqfr-h8mv-ghfj](https://github.com/python-hyper/h11/security/advisories/GHSA-vqfr-h8mv-ghfj),
critical, published 2025-04-24. CWE-444 (Inconsistent Interpretation of HTTP
Requests).

## Scope and boundary

In 0.14.0 the chunked reader discards exactly two bytes after each chunk body
without checking that they are `\r\n`, so it accepts malformed chunk
terminators. The fix stores `b"\r\n"` and raises `LocalProtocolError` when the
discarded bytes differ.

Acceptance of a malformed body is a **precondition** for request smuggling, not
a proof of it. Smuggling needs a second parser (for example a reverse proxy that
reads until the next `\r\n`) to delimit the same byte stream differently. The
reference material includes that second parser and the advisory's example
stream; use it to demonstrate the disagreement rather than claiming an exploit.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/h11/` | Vulnerable runtime package; focus `_readers.py`. |
| `reference/FIX.md` | Fix diff and advisory notes. |
| `reference/two_parsers.py` | h11 vs. a lenient proxy-style parser on the same bytes. |

## Evaluation notes

Expected key: `CWE-444` at `h11/_readers.py:197`, the `self._bytes_to_discard =
2` line in `ChunkedReader`.
