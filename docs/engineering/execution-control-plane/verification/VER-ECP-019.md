+++
id = "VER-ECP-019"
type = "verification"
title = "Independent evidence that one Git-derived handoff run is the declared result"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
verifies = ["REQ-ECP-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T07:44:38Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-31 by selecting the presented option 'Approve and start WO-ECP-023': CLI-driven rows for ECP-SBH-001 to -006 over Git fixtures, with digest stability asserted by comparing two independently produced results."
+++

# Verification Contract: Independent evidence that one Git-derived handoff run is the declared result

## Independence

Expected behaviour derives from `REQ-ECP-028` and the `ECP-SBH-` rules of
`SPEC-ECP-017`. Every case drives the public CLI (`check`, `evidence`) over
a Git fixture the test itself creates, and reads packet bytes and result
JSON directly; no case reads the evaluator's internals to predict a digest,
and digest stability is asserted by comparing two independently produced
results.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `ECP-SBH-001` rebind before evaluation | test: CLI over a Git fixture | `tests/test_workflow_compliance.py` | after the formal snapshot moves, one handoff run completes; the header carries the current snapshot and the run's `rebound_at`; the owner body is byte-identical |
| `ECP-SBH-001` idempotence | test: same | same | a packet bound to the current snapshot keeps its exact bytes across a run |
| `ECP-SBH-002` no creation, grace kept | test: same | same | with no packet, the run blocks with `QGP-G4I-EVIDENCE` `not_assessable`, no packet file appears, and the corrective names `harnessctl evidence`; a headerless legacy packet is not rewritten |
| `ECP-SBH-003` refusals kept | test: same | same | a foreign header blocks with `WEX-ECP-010`; a converting `.gitattributes` rule blocks with `WEX-ECP-011`; packet bytes are unchanged on both |
| `ECP-SBH-004` one-run fixed point | test: same | same | the first completed run's `changed_paths` contain the retained result path, and its `result_sha256` equals a second run's over the unchanged tree |
| `ECP-SBH-005` write reporting | test: same | same | `mutation.writes` carries the packet entry with the two moved fields beside the retained-result entry, and only then |
| `ECP-SBH-006` everything else read-only | test: same | same | a declared-path handoff run with a stale packet stays `not_assessable` and rewrites nothing; the `scope` checkpoint still writes nothing |

## Acceptance scenarios

### Scenario 1: one run, after a base merge

Bind the packet, then move the formal snapshot (edit a formal artifact) and
change an in-scope file. Run `check --checkpoint handoff --from-git BASE`
once and assert it completes, that the packet header carries the current
snapshot with the body preserved, and that `handoff.json` is retained. Run
it again and assert the two `result_sha256` values are equal.

### Scenario 2: nothing to bind

Delete the packet and run the same check. Assert the run blocks with
`QGP-G4I-EVIDENCE` `not_assessable`, that no packet was created, and that
the corrective command is `harnessctl evidence`.

### Scenario 3: the guards refuse

Point the packet header at another work order and assert the run blocks
with `WEX-ECP-010` and identical packet bytes. Restore it, add a
`.gitattributes` rule converting `*.md` line endings, and assert the run
blocks with `WEX-ECP-011` while the packet keeps its prior binding.

## Open decisions

None.
