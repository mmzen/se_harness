```toml
artifact = "WO-ECP-016"
checkpoint = "handoff"
formal_snapshot_sha256 = "37c2e660cbb94806f82d67ad7c2aac1cbcdf1759f457f5ff6cd21aa24d4b0d5e"
rebound_at = "2026-08-29T11:51:52Z"
```

# WO-ECP-016 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`build_context` admits, as exact paths, every verification record whose
`verifies_work_order` and every release record whose `releases_work` names
the selected work order, together with each record's
`evaluator_evidence_path` (`ECP-ADM-001`). Admission is by relation: a
record for another work order in the same diff still fails `QGP-G4I-PATHS`
with `WEX201` (`ECP-ADM-002`); the construction holds at `scope` and
`handoff` and for Git-derived, typed and manifest change sets
(`ECP-ADM-003`); `scope.declared_paths` is unchanged (`ECP-ADM-004`); the
check note states it (`ECP-ADM-005`). Issue #264.

## Evaluators

- Governing: released `se-harness 0.10.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-016-admit-own-records` off
  `main` at `5bde10a`; the suite and the demonstration run candidate source.

## Change

- `se_harness/workflow_compliance.py`: `own_record_paths(root, catalog,
  work_order_id)` returns the sorted, de-duplicated exact paths of the own
  records and their evaluator evidence; `build_context` splices it into
  `admitted_scope` after the work order's own file and packet directory.
  No contract file, gate, digest preimage or refusal changes.
- `docs/notes/harnessctl-check.md`: the admission sentence names the
  records and their evaluator evidence.
- `SPEC-ECP-001`: amendment record on `ECP-CHG-007`; domain index rows.

## Tests

`tests/test_workflow_compliance.py::OwnRecordAdmissionTests` (five tests):

- own record and its evaluator evidence admitted from Git at `scope`, and
  absent from `declared_paths` (scenario 1);
- a record for `WO-002` in the same diff blocks with `WEX201` naming
  `VREC-002`, never `VREC-001` (scenario 2);
- typed paths with `--changes-complete` and a change manifest admit the
  same (scenario 3);
- `handoff` admits the own record (scenario 4);
- `own_record_paths` on a catalog with two release records admits the one
  naming the work order and its evidence, as exact paths, and nothing for
  an unnamed work order (the release branch of `ECP-ADM-001`).

The fixture's ready record carries canonical evaluator evidence derived
from the fixture repository's own standard lock, as `capture-verification`
records it.

## Suite readings

- Windows 11 workstation (CPython 3.12, CRLF checkout, `87d7984`): 1194
  tests, 27 skipped, 2 failing names, both present on `main` and outside
  this work order (`test_artifact_authoring…test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  `test_instruction_architecture…test_owner_region_stays_within_the_size_bound`).
- Linux: the pull request's suite lane, in the hosted-lanes section.

## Demonstration on this repository

The case of issue #264, re-read from a worktree at `main` (`5bde10a`) with
`check --artifact WO-ECP-015 --checkpoint scope --from-git 5e5e9d6`, the
whole diff of pull request #263 including `VREC-ECP-018`:

- released 0.10.0 (`-I`): `blocked`, `QGP-G4I-PATHS: WEX201: changed path
  is outside execution scope:
  docs/engineering/execution-control-plane/verification-records/VREC-ECP-018.md`;
- candidate `87d7984`: `completed`, `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`
  and `QGP-G4I-PATHS` all `pass`, nothing blocking.

## Readings under the 0.10.0 root

- `validate .`: 1134 artifacts, 0 errors, 478 warnings.
- `doctor .`: the two pre-existing `W013` placement warnings, no FAIL.
- `validate_release_distributions.py`: PASS (7 records).
- Start preflight for `WO-ECP-016`: PASS over `e4131b9`.

## Deviations, recorded for the completion decision

None. This work order's own scope lists the domain's
`verification-records/` because the hosted lane runs the released 0.10.0
evaluator, which does not carry this rule; that is the declared interim
rule of issue #264, not a deviation.

## Complete changed-path set

Every path this work order changed since `main` at `5bde10a`, packet
included, as Git derived it (11 paths); the handoff check completed at its
fixed point with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing,
run by the released 0.10.0 evaluator on this Windows checkout:

```
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/evidence/WO-ECP-016/WO-ECP-016-handoff.md
docs/engineering/execution-control-plane/evidence/WO-ECP-016/handoff.json
docs/engineering/execution-control-plane/requirements/REQ-ECP-023.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-012.md
docs/engineering/execution-control-plane/verification/VER-ECP-012.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-016.md
docs/notes/harnessctl-check.md
se_harness/workflow_compliance.py
tests/test_workflow_compliance.py
```

## Hosted lanes

Read on the pull request at its heads; recorded in the pull-request body
and the verification record.
