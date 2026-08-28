# WO-ECP-009 implementation and verification evidence

Work-order-keyed evidence for `WO-ECP-009` (`REQ-ECP-009`; issue #212 step 3).
Retained under `VER-ECP-005`, the rows and scenarios that name `REQ-ECP-009`.
Readings taken on 2026-08-28 on Linux (CPython 3.12.13, Git 2.52.0) from
branch `governance/ecp-009-one-precondition-engine`, based on `main` at
`62997a3` (#239 merged, `WO-ECP-005` verified) plus the approval-and-start
commit `d29b894`. Windows figures come from the hosted lanes, section 8.

## 1. Changed paths

| Path | Change |
| --- | --- |
| `se_harness/quality_gates_contract.json`, template `QUALITY_GATES.json` | schema `se-harness-quality-gates-v2`; `QGP-G4I-COMPLETE` and `QGP-G4I-PATHS` declare `checkpoints: ["pre-action", "handoff"]`; a `transition_bindings` table of 16 entries keyed by lifecycle family and target state (definition approvals split by artifact type), each naming the gate predicates and the `QGS-` structural checks of the `ECP-KRN-005` edge table; both copies byte-identical |
| `se_harness/workflow_contract.py` | `effective_checkpoints`, `transition_binding`; loader validates predicate-level checkpoints and the bindings and fails with `WEX-ECP-030` when a lifecycle edge has no binding, a binding names an unknown predicate or structural check, or a bound predicate does not declare the `transition` checkpoint; a v1 copy loads as `WEX-ECP-030` |
| `se_harness/workflow_compliance.py` | `build_context` (the one context builder), `CheckpointContext.target`, `_gate_results` honouring predicate-level checkpoints and a bound subset, `transition_gate_results` (bindings + synthetic `QG-STRUCTURAL` gate), `lifecycle_relevant_diagnostics` (the one preflight filter), `review_evidence_available` accepting the handoff-bound document at the transition checkpoint, `check_workflow` accepting `--checkpoint transition --target`, `ensure_governed_checkpoint` reduced to contract-load and integrity refusals, `_classify` tolerating definition primaries, `selected_result` carrying a checkpoint and gates |
| `se_harness/workflow.py` | `PreconditionError` (typed, carries the predicate id) and `RepositoryWorkflowError`; `_validate_preconditions` and `_workflow_preflight_blocker` deleted; `structural_precondition_results` (`QGS-EDGE`, `-ASSURANCE`, `-VREC-COVERAGE`, `-RLS-COVERAGE`, `-VERIFIED-INCLUSION`, `-SUCCESSOR`); `plan_transition` evaluates every transitioned artifact through `build_context` + `transition_gate_results` before the proposed-graph validation, renders a blocked schema-2 result with `Blocked by` naming each refusing predicate and writes nothing, and an `apply` that would be blocked raises `PreconditionError` |
| `se_harness/cli.py` | `check --checkpoint transition --target STATE`; refusals coded by the refusing check (`_refusal_code`), repository blockers classified by exception type; `_repository_workflow_error` (message matching) deleted |
| template `QUALITY_GATES.md` | `QG-010` restated as what the code does; new `QG-011` (predicate-level checkpoints); transition binding index; graph-structural checks table |
| `docs/notes/harnessctl-reference.md`, `SPEC-WEX-002` | the preview command; the contract version by dated amendment (scope amended by the owner during execution, section 6 item 7) |
| tests | `OnePreconditionEngineTests` (7 cases), the two completion-drift tests retargeted, the delegated fixture delivering handoff-bound evidence through its change bundle, the `QUALITY_GATES.md` root/template divergence declared |

Not changed: any predicate evaluator or identifier, any lifecycle edge or decision right, `WORKFLOW.json`, `OPERATING_CARD.md` (its rendering is byte-identical), the root managed `docs/engineering/QUALITY_GATES.*` copies (hash-locked 0.7.1).

## 2. What the engine does now

- `transition` and `check --checkpoint transition --target` evaluate the same predicates through the same evaluator and the same context builder; a conformance test asserts equal `compliance.gates` (`ECP-KRN-004`, `-007`).
- The change-set predicates are bound to `pre-action`/`handoff` only, so `check --checkpoint handoff` evaluates a superset of `transition -> implemented` with identical statuses on the shared predicates (`ECP-KRN-009`; asserted).
- `review_evidence_available` at the transition checkpoint accepts the handoff-bound evidence document for the same formal snapshot: a transition can no longer apply on weaker evidence than `check` evaluated (the 2026-08 review's weakness 4).
- The two former private precondition sets are gone: `_validate_preconditions` (start/review preflight, keyed evidence, plus the structural checks) and `ensure_governed_checkpoint`'s re-implementation of `QGP-G1/G2-AUTHORING` and `QGP-G5P-RELEASE-UNIT`; the structural checks remain, as `QGS-` predicates (`ECP-KRN-005`).
- Refusals carry the refusing check: an illegal edge is `QGS-EDGE`, a failing review preflight is `QGP-G4I-PREFLIGHT`, a missing record is `QGS-VREC-COVERAGE`; the CLI's finding code is that identifier and repository blockers are classified by exception type (`ECP-KRN-008`).
- A predicate added to the `transition` binding in a copy of the contract blocks the transition naming it, with no code change (`VER-ECP-005` scenario 2; asserted).

## 3. Behaviour readings (candidate, fixture repository)

| Command | Reading |
| --- | --- |
| `check --artifact WO-001 --checkpoint transition --target verified` | blocked; `QG-G4-VERIFIED-COVERAGE` pass/pass, `QG-STRUCTURAL` `QGS-EDGE` pass, `QGS-VREC-COVERAGE` fail; `Blocked by` `QGS-VREC-COVERAGE: work order WO-001 has no direct eligible verification record` |
| `transition --set WO-001=verified …` (plan) | identical gates and blocker; `mutation.writes` empty |
| `transition … --apply` on the same state | blocked, finding code `QGS-VREC-COVERAGE`, nothing written |
| `transition --set WO-001=approved …` (illegal edge) | blocked, `QGS-EDGE: transition WO-001: implemented -> approved is not allowed` |
| `check … --checkpoint transition` without `--target` | `WEX210: --target is required for the transition checkpoint` |
| `focus --artifact WO-001 --json` | `result_sha256 d22f5e48…`, the `WO-ECP-005` golden, unchanged |

## 4. Tests

`python scripts/run_tests.py`: 1012 tests, 1 failure, 4 skipped; the failure is
`test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
the file-mode artefact of this Linux checkout that fails identically at `main`
here and passes on the hosted runner. `tests.test_workflow_execution` and
`tests.test_delegated_workflow`: OK.

Added, `OnePreconditionEngineTests`: plan-versus-preview conformance for
`VREC ready -> verified` and `WO approved -> in_progress`; the handoff
superset for `-> implemented`; a predicate added to a contract copy moving the
transition; a v1 contract refused with `WEX-ECP-030`; an unbound lifecycle
edge refused at contract loading; refusals labelled by check; `--target`
required for and limited to the transition checkpoint. Retargeted: the two
completion-drift tests (now blocked results and a typed `apply` refusal rather
than a raised string), the `run_preflight` mock point (the one filter lives in
the compliance module), the delegated fixture (section 6, item 1), and the
`QUALITY_GATES.md` parity test (section 6, item 2).

## 5. Released evaluator readings

Exact public `se-harness==0.7.1` outside the checkout, run with `-I`:
`validate` 1059 artifacts, 0 errors, 471 warnings; `doctor` 0 FAIL;
`preflight --work-order WO-ECP-009 --phase review` PASS;
`check --checkpoint handoff` in section 7. Repository-required:
`validate_release_distributions.py` PASS (4 records); `python -m se_harness --help` exit 0.
Parity: package and template `QUALITY_GATES.json` byte-identical; `render_operating_card()` equals the template.

## 6. Disclosures

1. **Phase 4 delegated completion now needs handoff-bound evidence.** The
   delegated route (`delegated_work_order_complete`) calls `plan_transition`
   with `apply=True` and retains no evidence bound to the handoff checkpoint,
   so `QGP-G4I-EVIDENCE` refuses it, and Phase 4's live-state continuity forbids
   an unreceipted write after start. The fixture therefore delivers the bound
   evidence through the receipted change bundle. The product change belongs to
   `WO-ECP-006`, which depends on this work order; until then a delegated
   completion in a real target would be refused with `QGP-G4I-EVIDENCE`. No
   target has ever declared `[agentic_delegation]` (complexity audit P0-5).
2. The root `docs/engineering/QUALITY_GATES.md` and `.json` are the
   hash-locked 0.7.1 copies and now diverge from the template; the divergence
   is declared by `test_policy_and_operator_reference_define_the_same_small_vocabulary`
   (every released line survives, the additions are absent from the root)
   instead of the former byte equality. The released evaluator loads its own
   packaged contract, so this repository's own verdicts are unaffected until
   the root advances.
3. `check --checkpoint transition` accepts only WO, VREC and RLS primaries, as
   every `check` does; definition transitions are evaluated by `transition`
   through the same bindings but have no public preview.
4. The revision-provenance policy refusal and the "not allowed" edge are both
   `QGS-EDGE`; the reason-required and actor checks stay argument errors
   (`WEX201`), because they are inputs, not graph properties.
5. A blocked `--apply` raises `PreconditionError` and is rendered by the CLI
   as a schema-2 failure whose finding code is the refusing predicate; the
   `compliance.gates` of the plan are not carried into that failure result.
   The read-only plan and the preview carry them.
6. Windows readings are the hosted lanes'.
7. **Scope amendment and a corrected declaration.** `docs/notes/harnessctl-reference.md`
   and `SPEC-WEX-002` were outside the original execution scope;
   `QGP-G4I-PATHS` refused the first handoff run on the reference note. The
   implementer intended to withdraw both edits and bind the handoff on the
   in-scope set, but the withdrawal (`git checkout --` after `git add`)
   restored the staged, edited files rather than the committed ones, so commit
   `7557801` carried both edits while its handoff declared completeness
   without them. That declaration was wrong. The owner then amended the scope
   to include both paths ("Amend scope, include both"); the handoff below is
   re-bound over the complete fourteen-path change set, which is what the
   pull request contains. The work-order file itself carries the owner's
   dated scope amendment (a governance write, not implementation) and is not
   part of the declared implementation change set.

## 7. Handoff checkpoint binding

Bound over the complete change set after the scope amendment (thirteen implementation paths; the work-order file carries the owner amendment).

artifact: WO-ECP-009
checkpoint: handoff
formal_snapshot_sha256: 356d39fa37f426dcaad8271adff82724887827f1ce8776bdbf71753530d0d7cc

Rerun: completed pass 4967ff179565d2117235e930be13c3d14de1b37d9edc93d57057b0bc81c22e25

## 8. Hosted lanes

Recorded in a later commit once the pull request has run them.
