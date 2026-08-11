# Verification Supersession Packet

This packet governs explicit retirement of a stale `ready` verification record when a later accountable verification record covers its work. It preserves both records as audit history while making the authoritative lineage and release eligibility unambiguous.

Chain: `INT-VSP-001` -> `CAP-VSP-001` -> `REQ-VSP-001..007` -> `SPEC-VSP-001`, `ARCH-VSP-001`, `ADR-VSP-001`, `VER-VSP-001` -> `WO-VSP-001` -> `REL-VSP-001`, `OPS-VSP-001`.

The triggering example is `VREC-AGR-001`: it remains `ready` at candidate `3f3ba521d7b19455e1f2eacb9aeea42928806aef`, while the corrected aggregate `VREC-PMI-001` is `verified` at candidate `505e889777c3c50f544b7e6d6fe58e2f765c1fea` and covers both `WO-AGR-001` and `WO-PMI-001`.

The implemented lifecycle adds a typed, human-authorized `ready -> superseded` transition. A superseded record must name exactly one distinct `verified` or `released` successor through `superseded_by`; the successor must cover every work order covered by the old record. Superseded records remain visible history but cannot satisfy verification or release readiness.

The accountable repository owner validated the intent-through-verification chain and explicitly authorized `WO-VSP-001` for implementation on 2026-08-11 with the instruction `go implementation`. The bounded implementation is complete and its results are retained in `evidence/WO-VSP-001-verification.md`; the requirements, specification, architecture, and work order are `implemented`, while `VER-VSP-001` remains `approved` pending a later commit-bound verification transition. `REL-VSP-001` and `OPS-VSP-001` remain `draft`. This approval does not authorize transition of `VREC-AGR-001`, commit, push, pull request, release, tag, publication, or deployment. Changing `VREC-AGR-001` requires a separate accountable governance decision and work order after this implementation is independently verified and merged.
