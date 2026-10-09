# Fix: thin-vec 0.2.15 -> 0.2.16

Upstream: mozilla/thin-vec, GHSA-xphw-cqx3-667j, CVE-2026-6654.
A `DropGuard` sets the length to zero during unwinding in `IntoIter::drop` and `ThinVec::clear`, so a panicking element destructor cannot cause the remaining elements to be dropped twice.

```diff
--- a/src/lib.rs
+++ b/src/lib.rs
@@ -1081,8 +1081,18 @@
     /// ```
     pub fn clear(&mut self) {
         unsafe {
-            ptr::drop_in_place(&mut self[..]);
-            self.set_len(0); // could be the singleton
+            // Decrement len even in the case of a panic.
+            struct DropGuard<'a, T>(&'a mut ThinVec<T>);
+            impl<T> Drop for DropGuard<'_, T> {
+                fn drop(&mut self) {
+                    unsafe {
+                        // Could be the singleton.
+                        self.0.set_len(0);
+                    }
+                }
+            }
+            let guard = DropGuard(self);
+            ptr::drop_in_place(&mut guard.0[..]);
         }
     }
 
@@ -1746,7 +1756,7 @@
             (*ptr).set_cap_and_auto(new_cap, (*ptr).is_auto());
             self.ptr = NonNull::new_unchecked(ptr);
         } else {
-            let new_header = header_with_capacity::<T>(new_cap, self.is_auto_array());
+            let mut new_header = header_with_capacity::<T>(new_cap, self.is_auto_array());
 
             // If we get here and have a non-zero len, then we must be handling
             // a gecko auto array, and we have items in a stack buffer. We shouldn't
@@ -1767,6 +1777,7 @@
                     .cast::<T>()
                     .copy_from_nonoverlapping(self.data_raw(), len);
                 self.set_len_non_singleton(0);
+                new_header.as_mut().set_len(len);
             }
 
             self.ptr = new_header;
@@ -2542,10 +2553,18 @@
         #[cold]
         #[inline(never)]
         fn drop_non_singleton<T>(this: &mut IntoIter<T>) {
+            // Leak on panic.
+            struct DropGuard<'a, T>(&'a mut IntoIter<T>);
+            impl<T> Drop for DropGuard<'_, T> {
+                fn drop(&mut self) {
+                    unsafe {
+                        self.0.vec.set_len_non_singleton(0);
+                    }
+                }
+            }
             unsafe {
-                let mut vec = mem::replace(&mut this.vec, ThinVec::new());
-                ptr::drop_in_place(&mut vec[this.start..]);
-                vec.set_len_non_singleton(0)
+                let guard = DropGuard(this);
+                ptr::drop_in_place(&mut guard.0.vec[guard.0.start..]);
             }
```
