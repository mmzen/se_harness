# Historical evidence assessment

Measured commit: `d52e6a88efb819bc36d082503813d55a995f6aa8`. Command: `python scripts/inventory_evidence.py --repository . --ref d52e6a88efb819bc36d082503813d55a995f6aa8`.
These are uncompressed Git blob bytes in that committed tree, excluding `.git`, untracked files and working-copy edits.

- Tracked checkout: 250.72 MiB.
- Evidence: 232.83 MiB (92.9%).
- Evidence bundles: 500.
- Three largest bundles: 134.67 MiB.

| Bundle | MiB | Files | Detected record references |
| --- | ---: | ---: | --- |
| `WO-PLG-020` | 72.03 | 95 | VREC-PLG-015 |
| `WO-PLG-011` | 35.41 | 826 | VREC-PLG-008, VREC-PLG-010 |
| `WO-PLG-017` | 27.23 | 669 | VREC-PLG-010 |
| `WO-PLG-006` | 20.85 | 555 | VREC-PLG-013 |
| `WO-PLG-012` | 16.96 | 937 | VREC-PLG-009 |
| `WO-PLG-005` | 11.32 | 969 | VREC-PLG-012 |
| `WO-PLG-003` | 9.98 | 977 | VREC-PLG-001 |
| `WO-PLG-004` | 8.23 | 598 | VREC-PLG-002 |
| `WO-PLG-010` | 5.24 | 387 | VREC-PLG-007 |
| `WO-PLG-019` | 5.09 | 149 | VREC-PLG-014 |
| `WO-RLO-009` | 4.32 | 10 | VREC-RLO-009 |
| `WO-PLG-018` | 3.61 | 19 | VREC-PLG-011 |
| `WO-PLG-007` | 2.78 | 256 | VREC-PLG-005 |
| `WO-PLG-001` | 1.91 | 200 | VREC-PLG-003 |
| `WO-PLG-008` | 1.83 | 214 | VREC-PLG-006 |
| `WO-PLG-002` | 1.51 | 182 | VREC-PLG-004 |
| `WO-AUT-005` | 0.22 | 12 | RLS-SEH-026, VREC-AUT-005, VREC-SEH-026 |
| `WO-PLG-021` | 0.22 | 27 | VREC-PLG-016 |
| `WO-CIP-009` | 0.14 | 44 | VREC-CIP-009 |
| `WO-KIS-001` | 0.11 | 17 | VREC-KIS-001 |

The table shows the largest 20; the command reproduces all 500 from the exact commit.
References are direct VREC/RLS paths plus release links through VRECs. Nested sidecars and every indirect dependency are not exhaustively resolved. No detected reference is not permission to delete.

## Archive options

| Option | Consequence |
| --- | --- |
| Keep current paths | Works with today's readers and preserves bound hashes; the checkout stays large. |
| Compressed assets on an explicitly approved GitHub archive release | Recommended destination if an archive move is later approved. Reuses existing hosting. Needs an index, a successful download/extraction check and compatible readers before removing any current files. |
| Git LFS or a new storage service | Adds installation and storage administration. Not recommended for this one-user project. |

A concrete later proposal should start with WO-PLG-020, WO-PLG-011 and WO-PLG-017 (134.67 MiB combined). Proposed asset names: `evidence-WO-PLG-020-d52e6a88efb8.tar.gz`, `evidence-WO-PLG-011-d52e6a88efb8.tar.gz`, and `evidence-WO-PLG-017-d52e6a88efb8.tar.gz`, attached to a dedicated owner-approved archive release in `mmzen/se_harness`.

Before moving those bytes, enumerate the files and indirect sidecar references for VREC-PLG-015, VREC-PLG-008 and VREC-PLG-010. Preserve each original path and byte sequence in the archive. Retain a small index with source commit, original path, destination URL, byte count, archive digest and affected records. Download and extract into a disposable directory and compare against that commit. Prove the existing evidence readers still resolve the bound material; if they require local paths, keep the originals until a separately approved reader change exists.

Submit the exact destination and deletion diff for the owner's archive decision only after those checks. A later current-tree move will not shrink already recorded Git history or existing clones. Reducing historical clone transfer would need a separate decision; this work does not rewrite history.

No archive asset was created, no historical bytes were removed, and no old record or bound evidence was edited in WO-KIS-006.
