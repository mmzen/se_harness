```toml
artifact = "WO-TCM-011"
checkpoint = "handoff"
formal_snapshot_sha256 = "c9b3f5e6c75a95ffd8bbcf491f26b085f4967095fbf21b72befca3696924092e"
rebound_at = "2026-09-09T11:02:58Z"
```

# WO-TCM-011 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

A definition draft that still draws an authoring advisory is not approved.
The validator exposes `authoring_advisories(artifact)`, the `W-AUT`
diagnostics its four per-type passes raise for one artifact read as a
draft whatever its recorded status; the gate's `authoring_ready` reads it
through the validator module preflight loads, after the placeholder and
`Open decisions` checks, for intents, capabilities, requirements and
specifications only, and refuses with every advisory named in the
validator's order, ending with "fix the draft and run the transition
again". Any other type passes the check without reading the validator; no
authoring predicate is bound to a target other than `approved`, so
implementation, supersession and rejection read nothing. `validate` keeps
passing with advisories present and lists them apart; no budget constant,
code or message of `SPEC-TCM-003` to `SPEC-TCM-006` moved; the two contract
copies are byte-identical and unchanged. The candidate `ARTIFACT_AUTHORING.md`
states the gate in one sentence per definition checklist; the two notes
describe it without the word "governor".

## Evaluators

- Governing: released `se-harness 0.17.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0170` from the wheel file whose
  digest equals `RLS-SEH-026`, for `validate`, `doctor`, the preflights, the
  delegated transitions, this packet and the handoff check.
- Candidate: this checkout, branch `wo/tcm-011-advisory-gate` off `main` at
  `65f972f6` (the 0.17.0 root), PR #428; the implementation commit is
  `33db8ce6`; the candidate reads 0.18.0.
- Delegated route (`ECP-TMB-007`): the gate is
  `.engineering-harness.delegation.toml` (`github-checks`, `check_name =
  "validate"`, `base_ref = "origin/main"`); each mechanical decision is taken
  on the evaluator's own restitution naming `delegated-executor`, and each
  lifecycle event records the class, the check-run id and the exact head.

## Rule-to-case map (VER-TCM-007)

| Row | Rules | Test or reading |
| --- | --- | --- |
| function | TCM-RFB-001, TCM-RFB-002, TCM-RFB-006 | `AuthoringAdvisoriesFunctionTests`: a clean draft returns none; an over-budget draft returns exactly the validator's diagnostics; an approved body returns what the draft returns while `validate` is silent on it; the six other types return none with the passes patched to raise; the entry module and the seam expose one function |
| refusal | TCM-RFB-004, TCM-RFB-005, TCM-RFB-010 | `AuthoringGateRefusalTests`: a requirement draft with a 36-word statement (`W-AUT-003`), an intent draft with a 34-word outcome (`W-AUT-011`), a capability draft without `under` (`W-AUT-016`), a specification draft with two 40-word rules (`W-AUT-021` twice), each refused unapplied and applied, the predicate `QGP-G1-AUTHORING` or `QGP-G2-AUTHORING`, the codes in the validator's order, the closing sentence, no byte written |
| order | TCM-RFB-003 | `test_the_placeholder_failure_is_reported_before_the_advisory` |
| other types and targets | TCM-RFB-006, TCM-RFB-012 | `test_other_types_pass_without_reading_the_validator` (verification, architecture, ADR with the reader patched to raise), `test_a_placeholder_in_a_verification_draft_is_refused_without_reading_an_advisory`, `test_an_implementation_transition_reads_no_advisory` (`check --checkpoint transition --target implemented` binds no authoring predicate) |
| validation unchanged | TCM-RFB-009 | `test_validate_keeps_passing_with_advisories_listed_apart`: five advisories, exit 0, `advisory_count` equal to the list |
| budgets unchanged | TCM-RFB-008 | `test_the_budgets_and_codes_of_the_four_families_are_unchanged`: twenty constants and `W-AUT-001` to `W-AUT-023` pinned; `git diff main -- se_harness/engine/validation_authoring.py` changes no constant |
| one module | TCM-RFB-007 | `test_the_gate_reads_the_validator_module_and_holds_no_budget`: `workflow_predicates` calls `validate_engineering_artifacts.authoring_advisories` and no module outside the engine defines a `*_LIMIT` budget |
| checklist | TCM-RFB-011 | `test_the_four_definition_checklists_state_the_gate` on the candidate guide |
| corpus | all | `CorpusTests`: `REQ-TCM-017` and `SPEC-TCM-007` read as drafts draw no advisory; the acceptance scenario below |
| existing suite | all | the Windows suite and the Linux lane, below |

The failure row "the validator module cannot be loaded" is
`test_an_unreadable_validator_is_not_assessable`: the predicate reads
`not_assessable`, never `pass`.

## Acceptance scenarios

- `REQ-HUP-031` as it was drafted, copied to a draft requirement in a
  throwaway repository under the fixture chain: `validate` reads five advisories (`W-AUT-003`, `W-AUT-005`, `W-AUT-007`, `W-AUT-008`, `W-AUT-010`)
  and the approval is refused naming the same codes in the same order.
  Trimmed to a statement within budget, the applied approval completes and
  the file reads `status = "approved"`.
- `SPEC-TCM-007` and `REQ-TCM-017`, the packet's own definitions, read as
  drafts by the function they specify: no advisory (`CorpusTests`).
- A verification contract draft with a placeholder: refused for the
  placeholder with the advisory reader patched to raise, so nothing was
  read.

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.17.0 | 1,443 artifacts, 0 errors, 46 warnings (all `W013`, pre-existing), 0 advisories |
| `doctor` | exact 0.17.0 | 99 PASS, 0 FAIL |
| `preflight --work-order WO-TCM-011 --phase start` at `6b6dbfd7` | exact 0.17.0 | PASS |
| `preflight --work-order WO-TCM-011 --phase review` | exact 0.17.0 | PASS |
| in-tree `doctor` (candidate 0.18.0 on the 0.17.0 root) | candidate | four `differs from distribution` findings: the three version-substitution skews a leading candidate always reads, and `docs/engineering/ARTIFACT_AUTHORING.md`, whose root copy lags the candidate guide by the four checklist sentences until the release that carries them is adopted |
| contract copies | workstation | `QUALITY_GATES.json` and `WORKFLOW.json` byte-identical between `docs/engineering/` and the template, and unchanged |
| budgets | workstation | no `*_LIMIT` constant, code or message changed against `main` |
| `tests/test_authoring_gate.py` | candidate, Windows | 20 tests, OK |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full --workers 8` | candidate, Windows 11 (CPython 3.13.3) | 1,118 tests, 1 error, 23 skipped: the workstation baseline plus the twenty tests this work order adds |
| `check --checkpoint handoff --from-git main` | exact 0.17.0 | section below |

### The Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full --workers 8` over this branch at
`42296e6f` on this Windows 11 workstation (CPython 3.13.3, LF checkout): 1,118
tests, 23 skipped, 1 error, the known baseline name present on `main` and outside
this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a read-only temporary Git object during teardown).
The 23 skips are the platform set plus the complexity test that runs only where
radon is installed. Before the two transaction tests held the reader silent, the
suite at `33db8ce6` read two more failures, both approvals of minimal fixture
drafts the gate now refuses (disclosure 1); the Linux lane read the same two.

### The handoff check

`check --artifact WO-TCM-011 --checkpoint handoff --from-git main`, exact
0.17.0, over this packet: Completed; every `QGP-G4I-*` predicate passes;
every changed path inside the declared scope; `complete: true`. The
schema-2 result is retained beside this packet as `handoff.json`.

## Hosted lanes

At the implementation head `33db8ce6` (pull-request event of PR #428): Predecessor
Evaluator Assessment 34342005157 and Publication Rehearsal 34342005286 `success`; SE
Harness Candidate Evidence 34342005200 `failure` on the two transaction tests the
gate refused, the same two names the Windows suite read; Engineering Harness
34342005138 stopped at the handoff step on `QGP-G4I-EVIDENCE`, no readable evidence
yet.

At the fix head `42296e6f`: SE Harness Candidate Evidence 34342737662 `success`
(source and package evidence, the upgrade rehearsal 0.17.0 to 0.18.0 on Linux and
Windows, the integration package built and verified on both platforms), Predecessor
Evaluator Assessment 34342737557 and Publication Rehearsal 34342738100 `success`;
Engineering Harness 34342737581 again stopped on `QGP-G4I-EVIDENCE` before this
packet existed. The lanes at the evidence head, the completion head and the record
head are read the same way before each delegated act, which quotes the check-run id
and the head it read.

## Disclosures

1. `tests/test_decision_management.py`'s Open-decisions test writes a
   requirement in the legacy body shape, which the new check would refuse
   for its advisories; the test now holds the advisory reader silent with a
   patch so it keeps reading the two checks it was written for. The gate's
   own order test covers the interaction.
2. The root copy of `ARTIFACT_AUTHORING.md` is hash-locked and lags the
   candidate guide until the next release is adopted; the in-tree `doctor`
   reads that skew as one more `differs from distribution` finding, by
   design, and no test compares the root copy to the template
   unconditionally.
3. The fixture requirement of the gate tests reads a 36-word statement where
   `VER-TCM-007` says 31; the budget is 30 and the reading is the same code.
