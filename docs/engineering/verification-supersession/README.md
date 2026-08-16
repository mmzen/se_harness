# Verification Supersession Packet

This packet governs explicit retirement of a stale `ready` verification record when a later accountable verification record covers its work. It preserves both records as audit history while making the authoritative lineage and release eligibility unambiguous.

Chain: `INT-VSP-001` -> `CAP-VSP-001` -> `REQ-VSP-001..007` -> `SPEC-VSP-001`, `ARCH-VSP-001`, `ADR-VSP-001`, `VER-VSP-001` -> `WO-VSP-001` -> `REL-VSP-001`, `OPS-VSP-001`.

The triggering example is `VREC-AGR-001`: it remains `ready` at candidate `3f3ba521d7b19455e1f2eacb9aeea42928806aef`, while the corrected aggregate `VREC-PMI-001` is `verified` at candidate `505e889777c3c50f544b7e6d6fe58e2f765c1fea` and covers both `WO-AGR-001` and `WO-PMI-001`.

The implemented lifecycle adds a typed, human-authorized `ready -> superseded` transition. A superseded record must name exactly one distinct `verified` or `released` successor through `superseded_by`; the successor must cover every work order covered by the old record. Superseded records remain visible history but cannot satisfy verification or release readiness.

The accountable repository owner validated the intent-through-verification chain and explicitly authorized `WO-VSP-001` for implementation on 2026-08-11 with the instruction `go implementation`. The bounded implementation is complete and its results are retained in `evidence/WO-VSP-001-verification.md`; the requirements, specification, architecture, and work order are `implemented`, while `VER-VSP-001` remains `approved` pending a later commit-bound verification transition. `REL-VSP-001` and `OPS-VSP-001` remain `draft`. This approval does not authorize transition of `VREC-AGR-001`, commit, push, pull request, release, tag, publication, or deployment. Changing `VREC-AGR-001` requires a separate accountable governance decision and work order after this implementation is independently verified and merged.

On 2026-08-16, the accountable repository owner authorized `WO-VSP-003` to transition only ready `VREC-DST-006` to `superseded` by verified aggregate `VREC-SEH-005`. The implemented transition preserves both records and all captured source provenance; the successor covers `WO-DOC-009` and `VER-DST-006`. Exact results are retained in `evidence/WO-VSP-003-verification.md`. Commit, push, pull-request creation, release, publication, and merge remain separately controlled.

The repository owner then authorized `WO-VSP-004` for the packet's original stale candidate. Ready `VREC-AGR-001` is now `superseded` by verified corrected candidate `VREC-PMI-001`, exactly as the packet's intent, requirements, specification, ADR, and examples prescribe. The direct successor covers `WO-AGR-001` and `VER-AGR-001`; later release aggregate `VREC-SEH-001` remains unchanged. Exact results are retained in `evidence/WO-VSP-004-verification.md`, and all external lifecycle actions remain separately controlled.

After the inspection-semantics correction merged, `WO-VSP-005` refreshed both evidence sets on the current baseline and provides the single PR-level publication envelope for the two independently authorized transitions. It changes neither successor nor source provenance. One later aggregate ready VREC may cover all three VSP work orders at their shared clean candidate commit; accountable assurance remains separate.

`OPS-VSP-001` was separately reviewed and approved through `WO-OCA-001` on 2026-08-16. It accepts the continuing obligation to preserve eligible supersession lineage, release exclusion, human authority, and historical provenance. `REL-VSP-001` remains a draft release proposal and grants no release authority.
