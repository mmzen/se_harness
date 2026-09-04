# Release 0.15.0

The content release after the 0.14.0 root adoption: the decision artifact
(`WO-DCM-001`), the reader-first requirement, intent and capability shapes
(`WO-TCM-005`, `WO-TCM-007`, `WO-TCM-008`), the repository-owned glossary
and its drift report (`WO-TCM-006`), the diagnostic-code index registration
(`WO-TCM-004`), and the four smaller work orders that landed since
`v0.14.0` (`WO-HUP-015`, `WO-DPG-002`, `WO-ECP-025`, `WO-CIP-006`).

- `REL-SEH-026`: the release contract; ten content members plus the release
  work order, eleven notes-only merges exempted by name, the build of record
  taken from the hosted pinned producer.
- `WO-RLS-021`: cut, qualify and build the candidate.
- `VREC-SEH-024`: the aggregate verification record over every gate (to be
  prepared by `WO-RLS-021`).
- `RLS-SEH-024`: the release record binding the build of record (to be
  prepared after verification).

Drafted on 2026-09-04 on the repository owner's instruction "you can
prepare the 0.15.0 release, however there is a work in progress, that will
finish soon". Both artifacts stay `draft` until that work has landed; the
census is then re-measured with `harnessctl release-unit . --from v0.14.0
--to <main>` and the contract's `gates` and exemptions are brought to it
before the release owner approves. This packet authorizes no candidate,
build or publication.
