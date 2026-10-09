# fast-jwt issuer-array validation (CVE-2025-30144)

Real-world authentication fixture: `nearform/fast-jwt` 5.0.5 (vulnerable) →
5.0.6 (fixed). Advisory [GHSA-gm45-q3v2-6cf8](https://github.com/nearform/fast-jwt/security/advisories/GHSA-gm45-q3v2-6cf8),
medium, published 2025-03-19. CWE-290 (Authentication Bypass by Spoofing).

## Scope and boundary

The verifier accepts an `iss` claim that is an array of strings. The vulnerable
`validateClaimValues` requires only that *some* array entry matches an allowed
issuer, so a token carrying `["https://attacker-domain/", "https://valid-iss"]`
passes issuer validation. The fix requires every array entry to match.

Accepting an unexpected issuer is **not** by itself a full authentication
bypass. The advisory's exploit requires the application to resolve the signing
key dynamically from the same claim, e.g. `get-jwks` with

```js
const keyFetcher = async (jwt) =>
  jwks.getPublicKey({ kid: jwt.header.kid, alg: jwt.header.alg, domain: jwt.payload.iss })
```

so that the attacker's array entry selects the attacker's JWKS key. Preserve
that dynamic key-fetch context when judging the finding; do not claim a
universal bypass from the issuer check alone.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/src/` | Vulnerable library source; focus `verifier.js`. |
| `reference/FIX.md` | Fix diff and advisory notes. |

## Evaluation notes

Expected key: `CWE-290` at `src/verifier.js:159`, the `values.some(...)`
issuer check in `validateClaimValues`.
