# pymonocypher `argon2i_32` heap overflow (CVE-2026-53720)

Real-world cross-language fixture: `jetperch/pymonocypher` 4.0.2.6 (vulnerable)
→ 4.0.2.8 (fixed). Advisory [GHSA-8f95-v3jq-cj86](https://github.com/jetperch/pymonocypher/security/advisories/GHSA-8f95-v3jq-cj86),
medium, published 2026-07-09. CWEs: CWE-122 (Heap Overflow), CWE-787, CWE-1284.

## Scope

`argon2i_32` sizes its Cython work area as `nb_blocks * 1024` from a
caller-supplied count, but Monocypher's Argon2 requires at least `8 * lanes`
blocks. A count below that makes the C routine write past the allocation. The
fix adds `if config.nb_blocks < (config.nb_lanes * 8): raise ValueError(...)`
before the allocation. The defect is the missing lower-bound check at the
wrapper/C contract boundary.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/c_monocypher.pyx` | Cython wrapper; the allocation sink. |
| `audit/monocypher.c`, `audit/monocypher.h` | Underlying C implementation. |
| `audit/setup.py` | Build script. |
| `reference/FIX.md` | Fix diff and advisory notes. |

## Evaluation notes

Expected key: `CWE-122` at `c_monocypher.pyx:345`, the `work_area = malloc((
<size_t> nb_blocks) * (<size_t> 1024))` line. CWE-787 and CWE-1284 are the
upstream alternates.

## Verified secondary cases

Secondary cases: blake2b-key-overflow (CWE-121, c_monocypher.pyx:281) and aead-key-length (CWE-125, c_monocypher.pyx:181) come from verified unexpected findings in the live rounds.

The model's unexpected findings were independently verified; see the superproject docs/reports/tiny-unexpected-verification.json.
