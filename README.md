# Audit Alchemist Harbor suite

Real-world audit fixtures for [Audit Alchemist](../../), exported as standard
tasks for the [Harbor framework](https://github.com/harbor-framework/harbor).
Each fixture keeps
audited code under `audit/` and fix/evidence under `reference/`. The exporter
creates one Harbor task per case. Its Docker context contains only audited code;
labels and oracle reports are placed under Harbor's delayed `tests/` and
`solution/` directories.

| Dataset | Class | Upstream | Vulnerable → fixed |
| --- | --- | --- | --- |
| `ajna-protocol-compromise-2` | Accounting / reward manipulation | Ajna legacy pool (2026-08-28 incident) | immutable deployment; exploit PoC |
| `filelock-toctou` | TOCTOU / symlink (`CWE-59`) | tox-dev/filelock, CVE-2025-68146 | 3.20.0 → 3.20.1 |
| `fast-jwt-iss` | Authentication (`CWE-290`) | nearform/fast-jwt, CVE-2025-30144 | 5.0.5 → 5.0.6 |
| `thin-vec-uaf` | Rust unsafe (`CWE-415`) | mozilla/thin-vec, CVE-2026-6654 | 0.2.15 → 0.2.16 |
| `pymonocypher-overflow` | Cross-language heap overflow (`CWE-122`) | jetperch/pymonocypher, CVE-2026-53720 | 4.0.2.6 → 4.0.2.8 |
| `h11-chunked-framing` | Protocol parsing (`CWE-444`) | python-hyper/h11, CVE-2025-43859 | 0.14.0 → 0.16.0 |
| `zk-email-sha256` | ZK constraint soundness | zkemail/zk-email-verify, zkSecurity #02 | `f2fb77c` → `ad0ad6`/`e14e88`/`d667a1` |

## Run with Harbor

Use Python 3.12 or later, Docker, and Harbor 0.24.0. From this submodule:

```sh
python -m pip install -r requirements-harbor.txt
python -m alchemist_harbor.export --output harbor-tasks
python -m alchemist_harbor.build
python -m alchemist_harbor.smoke
export PYTHONPATH="$PWD"
harbor run --path harbor-tasks \
  --agent alchemist_harbor.agent:AlchemistAgent \
  --model YOUR-MODEL \
  --ak binary_path=../../target/harbor-build/x86_64-unknown-linux-gnu/release/alchemist \
  --ak endpoint=https://YOUR-PROVIDER/v1/chat/completions \
  --n-concurrent 1 --jobs-dir "$PWD/harbor-jobs"
```

`--model` is passed directly to `alchemist audit`. Use `--ak wire_api=responses`
or `--ak wire_api=anthropic` for those provider endpoints. The adapter runs the
current parent checkout's Linux binary inside each Harbor task container. It
reads `AUDIT_API_KEY` from the Harbor process environment and forwards it only
to the agent command. Avoid `--ae AUDIT_API_KEY=...` for local runs: Harbor saves
agent environment values in its job config. `--n-attempts` retries a failed
trial; run separate named jobs for independent repeats.
The adapter uploads [`alchemist_harbor/node.toml`](alchemist_harbor/node.toml)
for explicit budgets and tool-loop settings; `--ak config_path=PATH` selects
another complete standalone TOML file. In PowerShell, use
`$env:PYTHONPATH = (Get-Location).Path` and
`$env:PYTHONIOENCODING = 'utf-8'` before `harbor run` and pass an absolute
`--jobs-dir` path.

After repeated jobs, summarize Harbor reward alongside exact and line metrics:

```sh
python -m alchemist_harbor.summarize --tasks harbor-tasks \
  --job harbor-jobs/round1 --job harbor-jobs/round2
```

The summary treats failed runs as misses and checks each verifier reward against
the report and exported labels. It reads labels only after trials finish. When
ordinary agent traces are present, it also totals empty completions, output
repairs, tool errors, token usage, and the largest completed stream response.
[`alchemist_harbor/round30-long-output.toml`](alchemist_harbor/round30-long-output.toml)
records the larger output cap used in the first live Harbor round; the CLI
deadline and Harbor timeout multiplier were supplied explicitly for that round.

`--case CASE_ID` on the exporter selects individual cases. Use a new output
directory for each export; it never overwrites an existing directory. Keep the
exported task tree and job results for reproducible comparisons, and record
the parent and submodule commits, model/settings, budgets, and repeated trials.
Each trial logs the binary and TOML SHA-256 fingerprints in
`alchemist-manifest.json`.
The smoke command uses a prescribed local model response and checks only the
end-to-end integration; it does not measure audit quality.

Harbor's reward is 1 only when the CLI run succeeds and its unique
`(CWE, path, line)` keys exactly equal that task's expected keys; clean controls
require an empty report. Missing, malformed, timed-out, or extra findings score
0. `details.json` under `/logs/verifier` records matched, missed, unexpected,
duplicate, and outcome counts. Exact reward measures label detection, not
exploit demonstration. The 18 existing cases include secondary issues and one
safe control; the seven primary findings remain the headline capability set.

The task-specific instructions are preserved to retain their scope. Some are
strongly leading, so this suite is public regression/tuning data rather than a
held-out estimate of general vulnerability discovery. Harbor's Docker boundary
keeps `tests/`, `solution/`, and `reference/` out of the agent workspace. A
provider credential forwarded from the Harbor process is available to the
agent process inside its task container.

## Source layout

```
<dataset>/
├── README.md          scope, boundaries, expected label
├── audit/
│   ├── dataset.json   case metadata used by the Harbor exporter
│   └── ...            vulnerable source the agent may read
└── reference/
    ├── FIX.md         fix diff and advisory/report notes
    └── ...            second parser, patched files, etc. (never staged)
```

The exporter copies `audit/` into each task's Docker context while excluding
`dataset.json`, build/dependency directories, and links. The old manifest format
remains for historical Alchemist reports and compatibility with the built-in
evaluator; Harbor is the standard path for new suite runs.

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
