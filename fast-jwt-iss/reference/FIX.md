# Fix: fast-jwt 5.0.5 -> 5.0.6

Upstream: nearform/fast-jwt, GHSA-gm45-q3v2-6cf8, CVE-2025-30144.
Array claim values must all match an allowed pattern; the fix splits the scalar and array checks and uses `every`.

```diff
--- a/src/verifier.js
+++ b/src/verifier.js
@@ -153,6 +153,16 @@
 
 function validateClaimValues(values, claim, allowed, arrayValue) {
   const failureMessage = arrayValue
+    ? `Not all of the ${claim} claim values are allowed.`
+    : `The ${claim} claim value is not allowed.`
+
+  if (!values.every(v => allowed.some(a => a.test(v)))) {
+    throw new TokenError(TokenError.codes.invalidClaimValue, failureMessage)
+  }
+}
+
+function validateClaimArrayValues(values, claim, allowed, arrayValue) {
+  const failureMessage = arrayValue
     ? `None of ${claim} claim values are allowed.`
     : `The ${claim} claim value is not allowed.`
 
@@ -222,6 +232,8 @@
 
     if (type === 'date') {
       validateClaimDateValue(value, modifier, now, greater, errorCode, errorVerb)
+    } else if (array) {
+      validateClaimArrayValues(values, claim, allowed, arrayValue)
     } else {
       validateClaimValues(values, claim, allowed, arrayValue)
     }
```

Exploit context (from the advisory): the bypass needs a dynamic key fetcher that trusts the same claim, e.g. `get-jwks` with `domain: jwt.payload.iss`.
