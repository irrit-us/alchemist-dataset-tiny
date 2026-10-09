# Ajna Protocol Compromise 2 — dataset

Real-world audit fixture derived from the 2026-08-28 Ajna incident on Ethereum
mainnet, in which seven permissionless Ajna pools lost roughly $775K to a
reward-manipulation attack on the liquidation `bucketTake` path. The cbETH/WETH
pool alone lost about $124.8K.

Unlike the synthetic `datasets/smoke` set, this dataset vendors the actual
on-chain implementation that was exploited. Ajna is immutable and the attacked
pools used a legacy 2023-07 deployment, so no patched revision of this exact
code exists.

The tree separates what the agent may read from the material that would reveal
the answer. The dataset root is `audit/`; the manifest lives there, so
`evaluate` stages only the audited code. `reference/` holds the exploit, the
on-chain evidence, and the incident analysis.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 dataset manifest; the dataset root is `audit/`. |
| `audit/ajna-v2/src/` | Vulnerable protocol source (ERC20 pool, libraries, interfaces); the case target. |
| `audit/ajna-v2/lib/` | Pinned build dependencies (OpenZeppelin, prb-math, clones, forge-std). |
| `audit/ajna-v2/foundry.toml` | Remappings and compiler settings (solc 0.8.18, optimizer off). |
| `reference/ajna-v2/script/` | Foundry exploit PoCs and helpers, including `AjnaExploit.s.sol`. |
| `reference/ajna-v2/PROVENANCE.md` | Source provenance, on-chain addresses, and compile metadata. |
| `reference/verification/` | Chain call traces, receipts, state diffs, and decoded evidence. |
| `reference/*.md` | Incident README, root-cause scope, economic model, verified callstack. |
| `reference/import-manifest.json` | SHA-256 for every file imported from the source archive. |

## Provenance

The source was reconstructed from Sourcify verification records for the deployed
implementation and action libraries; every file hash matched the on-chain solc
metadata. See `reference/ajna-v2/PROVENANCE.md` for contract addresses, the
compiler configuration, and the relationship to the public `ajna-core` v1.0.0
tag. The PoC was assembled locally and mirrors the on-chain setup and exploit
transactions; `reference/import-manifest.json` records the import hashes. Ajna
source files are licensed `BUSL-1.1`; dependencies retain their own licenses.

## Running

Validate the manifest from the repository root:

```sh
cargo run --locked -- validate --dataset datasets/ajna-protocol-compromise-2/audit/dataset.json
```

Audit the vulnerable source with the built-in agent (`--root` is the dataset
root, `audit/`):

```sh
cargo run --locked -- audit \
  --root datasets/ajna-protocol-compromise-2/audit \
  --target ajna-v2/src \
  --instruction 'Audit this permissionless ERC20 lending pool for economically exploitable violations of pool solvency and loss allocation.'
```

Score the dataset:

```sh
cargo run --locked -- evaluate \
  --dataset datasets/ajna-protocol-compromise-2/audit/dataset.json \
  --endpoint https://api.deepseek.com/chat/completions \
  --model deepseek-flash --jobs 1 --output evaluation-ajna.json
```

Reproduce the exploit locally (requires Foundry). The PoC is intentionally kept
out of `audit/`, so copy the scripts next to the runnable project first:

```sh
cp -r datasets/ajna-protocol-compromise-2/reference/ajna-v2/script \
      datasets/ajna-protocol-compromise-2/audit/ajna-v2/
cd datasets/ajna-protocol-compromise-2/audit/ajna-v2
forge script script/AjnaExploit.s.sol:AjnaExploitScript -vvv
```

## Evaluation notes

The case targets the whole `ajna-v2/src` directory and pins `CWE-841` to
`ajna-v2/src/libraries/external/TakerActions.sol:168`, the borrower-debt update
inside `bucketTake`. The incident also supports other mappings (for example a
calculation or price-manipulation CWE) and nearby sink lines; the label is one
defensible choice and should be adjusted deliberately before the score is read
as a quality signal. Because the exploit, provenance, and evidence stay under
`reference/`, evaluation staging never exposes them to the agent. No live-model
result for this fixture is recorded yet.
