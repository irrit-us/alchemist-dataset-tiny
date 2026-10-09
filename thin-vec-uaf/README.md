# thin-vec `IntoIter` double free / use-after-free (CVE-2026-6654)

Real-world Rust `unsafe` fixture: `mozilla/thin-vec` 0.2.15 (vulnerable) →
0.2.16 (fixed). Advisory [GHSA-xphw-cqx3-667j](https://github.com/mozilla/thin-vec/security/advisories/GHSA-xphw-cqx3-667j),
high, published 2026-04-15. CWEs: CWE-415 (Double Free), CWE-416 (UAF).

## Scope

`IntoIter::drop` moves the backing `ThinVec` out with `mem::replace` before
dropping the remaining elements. If an element's `Drop` panics, unwinding drops
the moved-out vector again, so the remaining elements are destroyed twice. The
fix keeps the vector in place and uses a `DropGuard` that sets the length to zero
during unwinding. `ThinVec::clear` got the same guard. The trigger requires an
element type with a panicking `Drop`.

## Layout

| Path | Contents |
| --- | --- |
| `audit/dataset.json` | Version 1 manifest (dataset root is `audit/`). |
| `audit/src/lib.rs` | Full crate source including tests. |
| `audit/Cargo.toml` | Crate manifest. |
| `reference/FIX.md` | Fix diff and advisory notes. |

## Evaluation notes

Expected key: `CWE-415` at `src/lib.rs:2546`, the `mem::replace(&mut this.vec,
ThinVec::new())` line in `IntoIter::drop::drop_non_singleton`. CWE-416 is the
upstream alternate.

## Verified secondary cases

Secondary case: clear-panic-double-free (CWE-415, src/lib.rs:1084) is the ThinVec::clear variant of the same unwind double-drop, verified from the live rounds.


