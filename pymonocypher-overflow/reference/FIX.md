# Fix: pymonocypher 4.0.2.6 -> 4.0.2.8

Upstream: jetperch/pymonocypher, GHSA-8f95-v3jq-cj86, CVE-2026-53720.
`argon2i_32` now rejects a block count below the Argon2 minimum (`8 * lanes`) before allocating the work area.

```diff
--- a/c_monocypher.pyx
+++ b/c_monocypher.pyx
@@ -12,14 +12,14 @@
 
 
 # also edit setup.py
-__version__ = '4.0.2.6'   # also change setup.py
+__version__ = '4.0.2.8'   # also change setup.py
 __title__ = 'pymonocypher'
 __description__ = 'Python ctypes bindings to the Monocypher library'
 __url__ = 'https://github.com/jetperch/pymonocypher'
 __author__ = 'Jetperch LLC'
 __author_email__ = 'joulescope-dev@jetperch.com'
 __license__ = 'BSD 2-clause'
-__copyright__ = 'Copyright 2018-2025 Jetperch LLC'
+__copyright__ = 'Copyright 2018-2026 Jetperch LLC'
 
 
 cdef extern from "monocypher.h":
@@ -329,6 +329,9 @@
     config.nb_passes = nb_iterations
     config.nb_lanes = 1
 
+    if config.nb_blocks < (config.nb_lanes * 8):
+       raise ValueError(f'nb_blocks must be >= {config.nb_lanes * 8}, got {config.nb_blocks}')
+
     cdef crypto_argon2_inputs inputs;
     inputs.pass_ = password
     inputs.pass_size = _validate_u32('password', len(password))
@@ -352,25 +355,93 @@
     return hash
 
 
+def x25519_public_key(secret_key: bytes) -> bytes:
+    """Compute the X25519 public key from a secret key.
+
+    :param secret_key: The 32-byte secret key.
+    :return: The 32-byte public key.
+    """
+    if len(secret_key) != 32:
+        raise ValueError(f'Invalid secret_key length {len(secret_key)} != 32')
+    public_key = bytes(32)
+    crypto_x25519_public_key(public_key, secret_key)
+    return public_key
+
+
+def x25519(your_secret_key: bytes, their_public_key: bytes) -> bytes:
+    """Compute the raw X25519 shared secret.
+
+    WARNING: The raw shared secret is not uniformly random.
+    Do not use it directly as a session key.
+    You MUST apply a key derivation function (KDF) such as
+    crypto_chacha20_h (HChacha20) or BLAKE2b before use.
+
+    :param your_secret_key: Your private, secret 32-byte key.
+    :param their_public_key: Their public 32-byte key.
+    :return: The 32-byte raw shared secret.
+    """
+    if len(your_secret_key) != 32:
+        raise ValueError(f'Invalid your_secret_key length {len(your_secret_key)} != 32')
```
