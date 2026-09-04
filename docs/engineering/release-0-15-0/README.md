# Release 0.15.0

The content release after the 0.14.0 root adoption: the decision artifact
(`WO-DCM-001`), the reader-first requirement, intent and capability shapes
(`WO-TCM-005`, `WO-TCM-007`, `WO-TCM-008`), the repository-owned glossary
and its drift report (`WO-TCM-006`), the diagnostic-code index registration
(`WO-TCM-004`), the four smaller work orders that landed since
`v0.14.0` (`WO-HUP-015`, `WO-DPG-002`, `WO-ECP-025`, `WO-CIP-006`), and the
owner-reviewed Verity Plane README with its logo (`WO-DOC-014`,
`WO-DOC-015`).

- `REL-SEH-026`: the release contract; twelve content members plus the
  release work order, eleven notes-only merges exempted by name, the build of record
  taken from the hosted pinned producer.
- `WO-RLS-021`: cut, qualify and build the candidate.
- `VREC-SEH-024`: the aggregate verification record over every gate (to be
  prepared by `WO-RLS-021`).
- `RLS-SEH-024`: the release record binding the build of record (to be
  prepared after verification).

Drafted on 2026-09-04 on the repository owner's instruction "you can
prepare the 0.15.0 release, however there is a work in progress, that will
finish soon". That work landed the same day as `WO-DOC-014` and
`WO-DOC-015`; `WO-DOC-014` had reached `main` without its verification
record (issue #347), so `VREC-DOC-007` was prepared and verified as a
post-merge repair (PR #349) before the census was re-measured at `2e90dc6`
and the contract brought to it. Both artifacts are ready for the two
approval acts: the contract by the release owner, the work order by the
engineering owner. This packet authorizes no candidate,
build or publication.
