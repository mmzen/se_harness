```toml
artifact = "WO-ECP-023"
checkpoint = "handoff"
formal_snapshot_sha256 = "5a486ce7c6607b9f301c650dc8d5ba7f1c4002684c1d4be8fc953da08b7a5555"
rebound_at = "2026-08-31T08:43:37Z"
```

# WO-ECP-023 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The Git-derived handoff check is self-binding (`REQ-ECP-028`;
`ECP-SBH-001` to `-006`): before evaluating, it rebinds an existing packet
header to the current formal snapshot — body preserved byte for byte, the
`evidence` command's `WEX-ECP-010`/`WEX-ECP-011` guards unchanged, no
packet created — and it evaluates the change set united with the retained
`handoff.json` path, so the first completed run is the declared,
digest-stable result. The rebind is reported in `mutation.writes` beside
the retained entry, outside the canonical block, so a run that rebinds and
a repeat that does not share one digest. Every other checkpoint and the
declared change-set forms stay read-only, and `check` keeps its
`WEX-ECP-0*` refusal codes on the blocked result instead of relabelling
them `WEX210`.

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, this packet and the handoff
  check included. It keeps the released two-run behaviour until the next
  root adoption, so this work order's own handoff digest is declared from
  the confirming second run, recorded here as the expected released
  behaviour.
- Candidate: this checkout, branch `wo/ecp-023-self-binding-handoff` off
  `main` at `609cb25`; the suite and the new tests run candidate source.

## Change

- `se_harness/workflow_compliance.py`: `rebind_handoff_packet` reusing
  `parse_evidence_header`, `render_evidence_header` and
  `_line_ending_conversion`; the self-binding step in `check_workflow`
  before the change set is derived, so a rewritten packet is a change-set
  member like any other; the retained-path union (`ECP-SBH-004`); the
  rebind entry passed to `build_result` as `writes` (`ECP-SBH-005`).
- `se_harness/cli.py`: the retained-result entry appended beside the
  rebind entry instead of replacing the writes list; the `_check` refusal
  split widened from `WEX-ECP-00` to `WEX-ECP-0`, so `WEX-ECP-010` and
  `WEX-ECP-011` keep their code on the blocked result.
- `tests/test_workflow_compliance.py`: new `SelfBindingHandoffTests`
  (one-run declared result with rebind, idempotent second run and byte
  stability; no creation and the untouched headerless legacy packet; the
  foreign-header and converting-rule refusals without a write; the
  read-only declared change set); the Git-derived expectations extended
  with the retained path, and digest parity asserted across two runs of
  the retention test.
- `docs/notes/harnessctl-check.md`: the self-binding write in "What the
  command does", the one-run digest in "Outcomes", the operator flow steps
  5 and 6, and the `WEX-ECP-011` row in the refusal table.
- `docs/notes/harnessctl-reference.md`: the `check` row's read-only
  exception and the self-binding paragraph beside the retained result.
- This domain's index: the `REQ-ECP-028` row and the `WO-ECP-023`
  ordering row.

## Tests

- `ECP-SBH-001`: after the formal snapshot moves, one run completes; the
  header carries the current snapshot and the run's `rebound_at`; the
  owner body is byte-identical; a packet already bound keeps its exact
  bytes across the repeat.
- `ECP-SBH-002`: with no packet, the run blocks with `QGP-G4I-EVIDENCE`
  `not_assessable` and creates nothing; a headerless legacy packet passes
  through the `W-ECP-002` grace unrewritten.
- `ECP-SBH-003`: a foreign header blocks with `WEX-ECP-010`, a converting
  `.gitattributes` rule with `WEX-ECP-011`; packet bytes unchanged on
  both.
- `ECP-SBH-004`: the first completed run's `changed_paths` carry the
  retained path and its `result_sha256` equals the second run's; also
  asserted on the pre-existing retention test.
- `ECP-SBH-005`: `mutation.writes` carries the packet entry with exactly
  `formal_snapshot_sha256` and `rebound_at` beside the retained entry on
  the run that rebinds, and only the retained entry on the repeat.
- `ECP-SBH-006`: a declared-path handoff run with a stale packet stays
  `not_assessable`, rewrites nothing and reports no write; the `scope`
  checkpoint still writes nothing (pre-existing `ECP-SCP-004` test).

## Suite readings

Windows workstation, candidate source: `tests/test_workflow_compliance.py`
145 tests OK; the six suites that pin the checkpoints, the notes and the
managed lane (`test_workflow_execution`, `test_workflow_documentation_contract`,
`test_context_routing_retirement`, `test_delegation_class`,
`test_ci_pipeline`, `test_instruction_architecture`) 310 tests OK,
5 skipped; the full `scripts/run_tests.py` suite at its baseline
(1189 tests, the one known `test_artifact_authoring` teardown error that
precedes this work order and was measured on `main` `609cb25` before this
change, 26 skipped). Graph validation 0 errors; release
distribution validation PASS; governing 0.11.0 `doctor` 0 FAIL (the
in-tree candidate `doctor` reads the expected candidate-versus-root skew).
Linux: the pull request's lanes at the completion commit.

## Demonstration on this repository

The governing 0.11.0 root evaluator ran this work order's own handoff:
`evidence` bound this packet, and `check --checkpoint handoff --from-git
main` was run twice, the second run confirming the declared digest — the
released two-run behaviour this work order removes, recorded as expected
until the next root adoption. The candidate's one-run behaviour is
demonstrated by `SelfBindingHandoffTests` over Git fixtures, because a
candidate-source `check` on this governed checkout is refused by runtime
identity, as designed.
