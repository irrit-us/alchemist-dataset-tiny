# zk-email standalone SHA256 comparator soundness (zkSecurity finding #02)

Real-world ZK-circuit fixture from the zkSecurity audit of `zkemail/zk-email-verify`
(2024-05), finding #02, report pages 24–26. Vulnerable commit `f2fb77c`; fixed
by commits `ad0ad6`/`e14e88`/`d667a1` (merge `95cd90`).

## Scope and boundary

Target the **standalone SHA256 template** (`sha.circom`), not the full
EmailVerifier. `paddedInLength` is fed to `LessEqThan(maxBitsPaddedBits)` without
a bit-width constraint, and `ItemAtIndex` (`array.circom`) constrains the final
compression selector with `LessThan(bitLength)` without constraining the index.
A malicious prover can set a length/index near the field modulus so both
comparators misbehave and `ItemAtIndex` returns zero, yielding an all-zero hash
for any input.

The report is explicit that the full EmailVerifier is not meaningfully
exploitable: `AssertZeroPadding` is also applied to the header/body lengths, so
a small negative length would force an all-zero message. Only consumers that use
the SHA256 templates in a different context are exposed. Do not label the email
verification scheme as broken.

The recommended fix is to drop `LessThan` in `ItemAtIndex` and assert that
exactly one index matches, document the `paddedInLength` bit-width assumption in
the SHA256 templates, and constrain the lengths with `Num2Bits` in the
EmailVerifier.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/sha.circom` | Standalone SHA256 templates (the case target). |
| `audit/array.circom` | `ItemAtIndex` / `CalculateTotal` used by the selector. |
| `audit/functions.circom` | Shared helpers. |
| `reference/FIX.md` | Audit finding summary and fix diff. |

## Evaluation notes

Expected key: `CWE-1284` at `sha.circom:126`, the `bitLengthVerifier.in[0] <==
paddedInLength` connection. `array.circom:25` (the `LessThan(bitLength)` in
`ItemAtIndex`) is the enabling sink and a defensible alternate; there is no
upstream CWE, so the taxonomy mapping is a project choice.
