# alchemist-dataset-tiny

Small, real-world audit fixtures for the
[Audit Alchemist](../../) harness. Each dataset is self-contained and keeps the
audited code under `audit/` and the fix/evidence under `reference/`, so the
solution stays out of the evaluation workspace.

| Dataset | Class | Upstream | Vulnerable → fixed |
| --- | --- | --- | --- |
| `ajna-protocol-compromise-2` | Accounting / reward manipulation | Ajna legacy pool (2026-08-28 incident) | immutable deployment; exploit PoC |
| `filelock-toctou` | TOCTOU / symlink (`CWE-59`) | tox-dev/filelock, CVE-2025-68146 | 3.20.0 → 3.20.1 |
| `fast-jwt-iss` | Authentication (`CWE-290`) | nearform/fast-jwt, CVE-2025-30144 | 5.0.5 → 5.0.6 |
| `thin-vec-uaf` | Rust unsafe (`CWE-415`) | mozilla/thin-vec, CVE-2026-6654 | 0.2.15 → 0.2.16 |
| `pymonocypher-overflow` | Cross-language heap overflow (`CWE-122`) | jetperch/pymonocypher, CVE-2026-53720 | 4.0.2.6 → 4.0.2.8 |
| `h11-chunked-framing` | Protocol parsing (`CWE-444`) | python-hyper/h11, CVE-2025-43859 | 0.14.0 → 0.16.0 |
| `zk-email-sha256` | ZK constraint soundness | zkemail/zk-email-verify, zkSecurity #02 | `f2fb77c` → `ad0ad6`/`e14e88`/`d667a1` |

## Layout

```
<dataset>/
├── README.md          scope, boundaries, expected label
├── audit/
│   ├── dataset.json   harness manifest (this is the dataset root)
│   └── ...            vulnerable source the agent may read
└── reference/
    ├── FIX.md         fix diff and advisory/report notes
    └── ...            second parser, patched files, etc. (never staged)
```

The dataset root is `audit/`, so the harness stages only the audited code and
never copies `reference/` into the agent workspace.

## Boundaries

Three fixtures deliberately keep a narrow claim:

- `fast-jwt-iss`: the loose `iss` array check is only exploitable together with
  a dynamic key fetcher that trusts the same claim; it is not a universal
  authentication bypass.
- `h11-chunked-framing`: the malformed-body acceptance is the precondition for
  request smuggling; `reference/two_parsers.py` shows the two-parser
  disagreement but does not claim a completed exploit.
- `zk-email-sha256`: the target is the standalone SHA256 template; the full
  EmailVerifier adds `AssertZeroPadding` constraints that make the end-to-end
  attack infeasible.

## Compliance

Each dataset embeds the upstream source at the specified version. Upstream
licenses and SPDX headers are retained in the vendored files; see each
`README.md` and `reference/FIX.md` for the exact sources. This repository holds
research and test material only.
