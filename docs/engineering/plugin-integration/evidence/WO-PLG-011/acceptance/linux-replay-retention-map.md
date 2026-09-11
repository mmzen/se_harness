# Retention copy map

This package contains evidence files only. It excludes disposable repository
directories, `.git` directories, evaluator environments, and the intentionally
corrupted input copy. Full file hashes, including Git metadata, remain inside
the original trace JSON. Selected actual artifact/dashboard/control bytes are
retained separately as evidence products.

| Package source | Suggested WO-PLG-011 acceptance destination |
|---|---|
| `attempt1/` | `acceptance/linux-replay-attempt1/` |
| `attempt2/` | `acceptance/linux-replay-attempt2/` |
| `native-products/` | `acceptance/linux-replay-attempt2/native-products/` |
| `preparation/` | `acceptance/linux-replay-attempt2/platform-preparation/` |
| `runner-source-before-error-retention-fix/` | `acceptance/linux-replay-attempt2/runner-source-before-error-retention-fix/` |
| `portable-source-sha256.json` | `acceptance/linux-replay-attempt2/portable-source-sha256-before-error-retention-fix.json` |
| `RETENTION-INVENTORY.json` | `acceptance/linux-replay-retention-inventory.json` |
| `RETENTION-MAP.md` | `acceptance/linux-replay-retention-map.md` |

`attempt2/REPORT.md` and `attempt2/audit.json` are the final replay report and
passed 82-record audit. `attempt2/runner-version-history.json` distinguishes the
actual historical runner bytes from later source corrections. Original top-level
attempt1 and attempt2's initial `external/` failure remain labeled separately;
`external-attempt2/` is the successful same-runner retry after fixture ordering
was corrected.

The portable source file hash manifest describes the frozen sources before the
reviewer's separate timeout/launch-error correction. It must not be relabeled
as the hash of the later corrected source tree. Exact byte-for-byte recovered
2ef8e7ab source is also retained; four earlier source versions are unavailable,
with their original hashes and executed records preserved.

The inventory hashes every payload file, including this map, and excludes only
the inventory itself from its own entries. Copy byte-for-byte; the inventory's
paths refer to this original package layout before the mapping above.
