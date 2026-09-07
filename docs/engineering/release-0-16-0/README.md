# Release 0.16.0

The distribution release after the 0.15.0 root adoption: the evaluator's
scripts leave the governed repository and ship inside the wheel
(`WO-DST-024`), `init` becomes the one installation command with `adopt`
kept as an alias for this release only (`WO-ECP-026`), the reader-first
specification shape with one identifier per rule and the `Coverage` table
(`WO-TCM-009`, corrected by record in `WO-TCM-010`), and the adoption that
moved the candidate to 0.16.0 (`WO-HUP-016`).

- `REL-SEH-027`: the release contract; five content members plus the
  release work order, four notes-class merges exempted by name, the
  released `WO-RLS-021` and the approved, waiting `WO-TCM-011` outside the
  unit by construction, the build of record taken from the hosted pinned
  producer.
- `WO-RLS-022`: cut, qualify and build the candidate.
- `VREC-SEH-025`: the aggregate verification record over every gate.
- `RLS-SEH-025`: the release record binding the build of record.

Drafted on 2026-09-07 on the repository owner's instruction "release
0.16.0", with `main` at `9069ff5d`, no work order in progress and every
required member verified. The release owner approved the contract and the
engineering owner approved the work order the same day, by selecting the
presented option "Approve both" (PR #368); the engineering owner then gave
"start, complete on green, prepare record", and `WO-RLS-022` runs on
`release/0.16.0` off `main` at `2e46b49`. This packet authorizes no
publication; the verification and release decisions are recorded on
`VREC-SEH-025` and `RLS-SEH-025`.
