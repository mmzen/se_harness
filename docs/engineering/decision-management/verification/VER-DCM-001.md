+++
id = "VER-DCM-001"
type = "verification"
title = "Verify the decision artifact contract"
status = "draft"
owners = ["quality-owner", "technical-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
verifies = ["REQ-DCM-001", "REQ-DCM-002", "REQ-DCM-003"]
+++

# Verification Contract: Verify the decision artifact contract

## Independence

Expected behaviour is derived from the three requirements and
`SPEC-DCM-001`, and checked with fixtures the implementation did not write:
a fixture repository per scenario, built from the templates, with decisions
in each state and blocked artifacts in each family. The refusal messages
are compared with the contract, not with the implementation's own text.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-DCM-001` | fixture tests per blocked family | an open decision blocking a requirement, a specification, a work order, a verification record, a release record; a deferred decision with a scope | every transition of a blocked artifact is refused with the decision, its options, the role and the `decide` command; the admitted transition of a scoped deferral proceeds; no state changes on refusal |
| `REQ-DCM-001` | validator taxonomy tests | a decision with a missing `blocks` target; a wrong target type; a missing field | `E-DCM-001`, `E-DCM-002` raised; the graph is invalid and transitions refuse |
| `REQ-DCM-002` | command tests | `decide` with each declared option, with an undeclared option, by the right role, by a wrong role, with and without reason | the disposition carries option id, label, role, time and verbatim reason; the lifecycle event matches; undeclared option and wrong role are refused with no change |
| `REQ-DCM-002` | contract tests | `WORKFLOW.json`, `QUALITY_GATES.json`, `DECISION_RIGHTS.md`, `TRACEABILITY.md` in the candidate templates | the `decision` family, `QGP-DECISION-OPEN` bound to every transition checkpoint of the four families, `DR-DECISION-DISPOSE`, and `concerns`, `blocks`, `produces` are present and consistent with `SPEC-DCM-001` |
| `REQ-DCM-003` | fixture and Explorer tests | a deviation accepted with revisit; accepted without revisit; two acceptances against one rule; a revisit that has passed | `accept` without revisit refused; the standing deviation appears on the specification, the work order and a captured record's evidence; the Explorer projection names it; `W-DCM-001` and `W-DCM-002` raised in the two warning cases |
| all | authoring and template tests | `DECISION.template.md`, the layout registry, `ARTIFACT_AUTHORING.md` threshold, `create-artifact --type decision` | the template scaffolds two options and the kind fields; the registry places `DEC-` under `decisions/`; the threshold paragraph exists; `E-DCM-004` fires on prose in `## Open decisions` |
| all | upgrade tests | a consumer repository at the previous release | the upgrade adds the type, the family, the gate and the template without touching repository-owned artifacts |

## Acceptance scenarios

- Raise `DEC-X-001` (question) blocking `REQ-X-004` and `WO-X-002`;
  request `REQ-X-004=approved`; confirm the refusal text and the unchanged
  state; dispose with option `b` as the product owner; confirm the
  disposition and that the approval proceeds.
- Defer `DEC-X-001` with a scope admitting `WO-X-002: approved ->
  in_progress`; confirm the start proceeds and the completion is refused.
- Raise `DEC-X-002` (deviation against `SPEC-X-001#rule-7`, concerning
  `WO-X-002`); attempt `accept` without revisit; then accept with revisit
  as the technical owner; complete the work order, capture a record;
  confirm the standing deviation on all three and in the evidence.
- Attempt to dispose `DEC-X-002` as the engineering owner; confirm the
  refusal names the technical owner.
- Generate the Explorer bundle for the fixture; confirm the in-flight tile
  lists the open decision with its age and decider, and the record panel
  shows the standing deviation.
- Run the full suite and the released-evaluator validation on this
  repository; confirm no regression and zero errors.

## Property and invariant tests

- No `--apply` on a blocked artifact changes any file while a blocking
  decision is `open`.
- `build_explorer_metrics` counts open and decided decisions and computes
  raise-to-dispose hours deterministically.
- The gate is deterministic: the same tree yields the same refusal text.
- A disposition without a matching lifecycle event is `E-DCM-003`.

## Static and architecture checks

- `ARCH-DCM-001` conforms to `SPEC-DCM-001`; `ADR-DCM-001` decides it.
- The root managed copies are unchanged by the work order.
- No component other than the CLI's transition path writes a disposition.

## Security and privacy checks

- Hostile decision text (script tags, sentinels, long strings) renders as
  text in refusals and in the Explorer.
- A disposition by a role without the right is refused; a hand-written
  disposition fails validation.

## Performance and resilience checks

- Gate evaluation time on this repository stays within the existing
  `check` budget; the decision count is reported.

## Manual assessments

Review one refusal and one Explorer in-flight tile with an accountable
owner: is the decision, its options and the next command clear without
opening a policy?

## Evidence retention

`docs/engineering/decision-management/evidence/WO-DCM-001-verification.md`
retains commands, exit codes, test counts against the Windows baseline,
fixture identities, refusal texts, Explorer observations, and the actions
not performed.

## Residual uncertainty

Fixtures prove the gate, not the threshold's effect on agent behaviour;
whether agents raise decisions instead of asking open questions is observed
after adoption, in the effectiveness bench.
