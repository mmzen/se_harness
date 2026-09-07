+++
id = "WO-RSK-011"
type = "work_order"
title = "Close a risk under verified coverage and state the risks a release carries"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The work adds a decision right, a transition refused on the strength of verification coverage, and a derived block on the release record. The assurance and release decisions read that machinery directly, so its correctness must be assessed at an exact commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/risks.py",
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_contract.json",
  "se_harness/engine/validate_engineering_artifacts.py",
  "se_harness/engine/inspect_engineering_artifacts.py",
  "se_harness/engine/generate_harness_dashboard.py",
  "se_harness/engine/harness_explorer/",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/templates/RELEASE_RECORD.template.md",
  "tests/test_risk_management.py",
  "tests/test_validation_taxonomy.py",
  "tests/test_dashboard_webui.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/risk-artifacts.md",
  "docs/engineering/risk-management/",
]

[relations]
implements = ["REQ-RSK-014", "REQ-RSK-016"]
specifications = ["SPEC-RSK-010"]
architecture = ["ARCH-RSK-010", "ADR-RSK-010"]
verification = ["VER-RSK-010"]
+++

# Work Order: Close a risk under verified coverage and state the risks a release carries

## Objective

Make "mitigated" a claim that rests on verified work, and make a release record
state the threats its work carries, derived from the graph.

## In scope

- The closure edge `mitigating -> mitigated`, applied by `harnessctl transition`
  under the new decision right `DR-RISK-CLOSE`, refused unless a `verified` or
  `released` record covers every work order in `mitigated_by` and a residual is
  recorded.
- `DR-RISK-CLOSE` in the template `DECISION_RIGHTS.md`, held by the assurance
  owner, and no right anywhere to dispose a risk.
- The validator's `E-RSK-006`, `E-RSK-007` and `E-RSK-008`.
- The derived `[[risks]]` block written by `prepare-release`, its row shape, and
  the rejection of a hand-edited block; the release-record template gains the
  block with a note that the tool writes it.
- The Explorer's in-flight rows for risks in `raised` and `mitigating`, and the
  inspection's projection of the type.
- The cases of `VER-RSK-010` for `REQ-RSK-014` and `REQ-RSK-016`, in the module
  `WO-RSK-010` created.
- The two notes, extended with closure and the register.
- The evidence packet and the verification record of this work order.

## Out of scope

- Everything `WO-RSK-010` delivers; this work order is stacked on it and assumes
  it merged.
- Any second decision right, and any right to dispose a risk.
- Both quality-gates contract copies, by RSK-MGT-014.
- Release qualification, publication, and the release contract of any release.
- The repository's root managed copies.

## Authorized decision envelope

The implementer may decide: where the coverage query lives and whether it reuses
the existing record-coverage reader; the row order and column order of the
register; the Explorer's wording and row ordering; test names and placement; the
wording of the three diagnostics, provided each names the risk, the work order or
the divergence the contract requires.

The implementer may not decide: the name or holder of `DR-RISK-CLOSE`; that
closure is refused without verified coverage or without a residual; that the
register is derived rather than authored; any rule identifier or diagnostic code
of `SPEC-RSK-010`.

## Constraints

- Preparing a release twice from one commit must produce identical register
  bytes.
- A `verified` record is never rewritten by this work; closure writes only the
  risk.
- Coverage means a `verified` or `released` record; `implemented` is not coverage.
- The register lists a risk reachable from the released work only, never every
  risk in the repository.
- Any question that blocks this work order is a `DEC-` artifact naming it in
  `blocks`.

## Expected change surface

The risk module's closure and coverage functions; the transition path and the
workflow contract's decision-right binding; three validator diagnostics; the
release preparation and the release-record template; the Explorer's in-flight tile
and the inspection projection; the test module and two existing test modules; two
notes.

## Required verification

`VER-RSK-010`, for the rows of `REQ-RSK-014` and `REQ-RSK-016`, including
acceptance scenarios 2 and 3, the register's determinism property, the
decision-rights diff, and the performance reading of the graph on both platforms.

## Evidence to record

`docs/engineering/risk-management/evidence/WO-RSK-011-verification.md`, holding:
the rule-to-case citation map for RSK-MGT-022 to RSK-MGT-025, RSK-MGT-028 to
RSK-MGT-030, RSK-MGT-032 and RSK-MGT-035; the decision-rights catalog before and
after; the verbatim refusal text of a closure attempted without coverage; the
register bytes from two preparations of one commit; the predicate identifier sets
against `main`; and the governing readings from the released evaluator outside the
checkout, labelled per platform, with the hosted lane run identifiers.

## Stop and escalate conditions

- Closure cannot be refused without reading a `verified` record's own bytes:
  stop and report what it must read.
- The register cannot be derived deterministically: stop; an authored register is
  prohibited by RSK-MGT-030.
- The coverage query would require a second decision right: stop and raise a
  decision.
- A rule of `SPEC-RSK-010` cannot be met as written: raise a deviation decision
  against that rule identifier.

## Completion report format

The schema-2 handoff result, then: each rule identifier with its covering test;
the three diagnostics added; the decision-rights diff; the two register readings;
the files changed against the declared scope; the governing readings with
commands, platforms and evaluator version; and the one decision now due with its
role.
