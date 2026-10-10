# Unexpected buffer-bound findings, 2026-10-09

These are source-verified wrapper contract failures in the vendored version;
they do not establish remote reachability in every embedding application.
The Python caller must be able to supply the indicated byte buffers.

- `blake2b-key-overflow`: wrapper line 281 passes unrestricted len(key) into
  `crypto_blake2b_keyed`; `monocypher.c:545-546` copies key_size bytes into
  key_block[128]. A key longer than 128 bytes exceeds the stack buffer.
- `aead-key-length`: wrapper line 181 passes key and nonce without length
  checks to the native AEAD routine requiring 32/24 bytes.
- `chacha20-short-key`: wrapper line 267 selects the valid 8-byte nonce branch
  but does not check the key length. The native ChaCha20 operation reads 32
  bytes of key. The 24-byte nonce branch has the same root cause.
- `signature-check-short-buffers`: wrapper line 429 passes signature and public
  key without size checks; native EdDSA verification expects 64/32 bytes.

These exact keys are tuning labels. Alternate CWE or adjacent native sink
lines should receive independent evidence review, not automatic dismissal.
No native crash reproduction or upstream advisory is claimed for the newly
added ChaCha20 and signature-check cases.
