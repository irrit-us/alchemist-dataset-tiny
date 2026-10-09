# filelock TOCTOU (CVE-2025-68146)

Real-world race-condition fixture: `tox-dev/filelock` 3.20.0 (vulnerable) →
3.20.1 (fixed). Advisory [GHSA-w853-jp5j-5j7f](https://github.com/tox-dev/filelock/security/advisories/GHSA-w853-jp5j-5j7f),
medium, published 2025-12-16. CWEs listed upstream: CWE-59, CWE-362, CWE-367.

## Scope

Unix lock acquisition only. When the lock directory is attacker-writable, a
symlink placed at the lock path is followed by `os.open`, so `O_TRUNC` truncates
the symlink target instead of the lock file. The fix adds `os.O_NOFOLLOW`.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/filelock/` | Vulnerable package (`_unix.py`, `_api.py`, `_util.py`, ...). |
| `reference/FIX.md` | Fix diff and advisory notes. |

## Evaluation notes

Expected key: `CWE-59` at `filelock/_unix.py:41`, the `open_flags = os.O_RDWR |
os.O_TRUNC` line. The advisory also names CWE-362 and CWE-367 (TOCTOU); those are
defensible alternate labels. The Windows reparse-point fix is real but out of
scope here.
