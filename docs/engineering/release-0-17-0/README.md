# Release 0.17.0

The release of the code-health programme (issues #375 to #381): wave 0
correctness (`WO-ECP-027`), the wave 1 deletions (`WO-ECP-028`, `WO-ECP-029`,
`WO-ECP-030`), the wave 2 primitives (`WO-ECP-031`, `WO-ECP-032`,
`WO-ECP-033`), the wave 3 engine (`WO-ECP-034`, `WO-ECP-035`, `WO-ECP-036`),
the wave 4 test suite (`WO-TST-004`) and wave 5 (`WO-AUT-005`, `WO-CIP-007`,
`WO-DST-026`); with them the risk artifact (`WO-RSK-010`), the five-key
installed configuration (`WO-DST-025`) and the adoption that moved the
candidate to 0.17.0 (`WO-HUP-017`).

- `REL-SEH-028`: the release contract; seventeen content members plus the
  release work order, six trailer-less merges exempted by name (five
  definition packets and the execution of `WO-TST-004`, whose trace the
  release branch repairs), the released `WO-RLS-022` outside the unit by
  construction, the build of record taken from the hosted pinned producer.
- `WO-RLS-023`: cut, qualify and build the candidate.
- `VREC-SEH-026`: the aggregate verification record over every gate, bound
  to the candidate; prepared and verified after the candidate exists.
- `RLS-SEH-026`: the release record binding the build of record; prepared,
  bound and released after the verification.

Drafted on 2026-09-09 on the repository owner's instruction "prepare
release 0.17.0", with `main` at `4ea947be`, no work order in progress and
every required member verified. This packet authorizes no publication; the
verification and release decisions are recorded on `VREC-SEH-026` and
`RLS-SEH-026`.
