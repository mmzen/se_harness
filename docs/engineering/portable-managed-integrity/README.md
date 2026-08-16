# Portable Managed-File Integrity Packet

This packet governs a corrective change to make managed-file integrity checks stable across supported operating systems and Git newline policies without weakening customization protection.

Chain: `INT-PMI-001` -> `CAP-PMI-001` -> `REQ-PMI-001..007` -> `SPEC-PMI-001`, `ARCH-PMI-001`, `ADR-PMI-001`, `VER-PMI-001` -> `WO-PMI-001` -> `REL-PMI-001`, `OPS-PMI-001`.

The triggering anomaly is retained in `evidence/doctor-anomaly-2026-08-11.md`: after pull request #4 was merged, five managed files differed from their lock entries only by CRLF/LF representation, while the managed validator also had a genuinely stale lock digest. Artifact validation, all unit tests, CLI loading, candidate availability, ancestry, and diff hygiene passed, but `harnessctl doctor .` correctly prevented the verification transition from being recorded.

The accountable repository owner accepted the intent-through-verification chain and `WO-PMI-001` on 2026-08-11 with the instruction `ok accepted`, then explicitly requested implementation with `go implementation`. The bounded implementation is complete with retained evidence under `evidence/WO-PMI-001-verification.md`. Requirements, specification, architecture, and work order are `implemented`. `OPS-PMI-001` was separately reviewed and approved through `WO-OCA-001` on 2026-08-16 as the continuing integrity obligation. `REL-PMI-001` is a rejected historical proposal: `WO-PMI-001` was released through `REL-DST-001` and `RLS-SEH-001` in `v0.2.0` instead. Operating approval remains independent from release authority.
