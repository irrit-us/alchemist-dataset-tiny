# Fix: filelock 3.20.0 -> 3.20.1

Upstream: tox-dev/filelock, GHSA-w853-jp5j-5j7f, CVE-2025-68146.
The Unix lock path adds `os.O_NOFOLLOW` so a symlink at the lock path is not followed (and therefore not truncated by `O_TRUNC`).

```diff
--- a/src/filelock/_unix.py
+++ b/src/filelock/_unix.py
@@ -38,7 +38,7 @@
 
         def _acquire(self) -> None:
             ensure_directory_exists(self.lock_file)
-            open_flags = os.O_RDWR | os.O_TRUNC
+            open_flags = os.O_RDWR | os.O_TRUNC | os.O_NOFOLLOW
             if not Path(self.lock_file).exists():
                 open_flags |= os.O_CREAT
             fd = os.open(self.lock_file, open_flags, self._context.mode)
```
