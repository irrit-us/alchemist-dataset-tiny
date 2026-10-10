# Unexpected findings rechecked, 2026-10-09

The previous `empty-signature-accepted` case incorrectly expected a vulnerability
when the caller explicitly permitted `none`. It is replaced with the narrow
`unsigned-opt-in-control` (empty expected findings). The keyed HS256 control
rejects an empty signature, and a null-key HS256 verifier rejects `alg: none`.

There is a separate configuration-dependent failure: `key:null` with
`algorithms:['HS256']` accepts an **HS256-header token with an empty signature**.
`verifyToken` skips both key/signature mismatch branches when both are absent;
`validateAlgorithmAndSignature` allows HS256 then skips verification at line 139.
`empty-hs256-null-key` captures this failure to reject an invalid configuration.
This is not a bypass of a verifier configured with a real key. An async key
fetcher returning null is rejected earlier; do not claim that route works.

`cache-expiry-without-iat` records an independently reproduced expiry bypass.
With a real HS256 key and `cache:true`, an initially valid signed token with
`exp` but no `iat` remains accepted after expiry. The `hasIat` branch at line 92
skips the exp-derived bound and uses cacheTTL (default 600000 ms). The same token
is rejected without caching, and a cached token with numeric iat is rejected
after expiry. Lines 89 and 92 represent one root cause, not two vulnerabilities.
Caching must be enabled; this is a meaningful authorization-lifetime violation,
not merely hardening advice. No CVE or upstream confirmation is claimed.

The parent harness's `scripts/verify_tiny_jwt.cjs` runs these controls against
the unmodified vendored source. Its output is in
`docs/reports/round4-jwt-verification.json` in the parent repository.
