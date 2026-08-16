# Aggregate Release Packet

This draft packet governs release manifests that contain multiple release-bearing work orders while remaining bound to one exact, fully verified candidate commit.

Chain: `INT-AGR-001` -> `CAP-AGR-001` -> `REQ-AGR-001..008` -> `SPEC-AGR-001`, `ARCH-AGR-001`, `ADR-AGR-001`, `VER-AGR-001` -> `WO-AGR-001` -> `REL-AGR-001`, `OPS-AGR-001`.

The proposed model extends the existing array-valued `verification_record` and `release_record` relations. One aggregate verification record covers the selected release-bearing work at the final candidate commit, and one release record copies that commit and enumerates the same work. Governance-only work orders may authorize review, status transitions, tags, or publication, but they are not release payload.

The accountable repository owner approved the intent-through-verification chain and `WO-AGR-001` for implementation on 2026-08-11 with the instruction `ok, perform the change`. The bounded implementation is complete with retained evidence under `evidence/WO-AGR-001-verification.md`. `OPS-AGR-001` was separately reviewed and approved through `WO-OCA-001` on 2026-08-16; it assures the eight implemented aggregate-release requirements as a continuing operating obligation. `REL-AGR-001` is a rejected historical proposal: `WO-AGR-001` was released through `REL-DST-001` and `RLS-SEH-001` in `v0.2.0` instead.
