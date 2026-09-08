+++
id = "WO-RSK-010"
type = "work_order"
title = "Implement the risk artifact, its raise, and the decision pairing"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The work adds an artifact family that can stop any transition of any domain, a lifecycle family in the workflow contract, validator diagnostics, two commands, a managed template and a change to the scope check. Every later engineering, assurance and release decision reads that machinery, so the correctness of the changed state must be assessed at an exact commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/risks.py",
  "se_harness/artifact_layout.py",
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_contract.json",
  "se_harness/quality_gates_contract.json",
  "se_harness/engine/artifact_layout_registry.py",
  "se_harness/engine/validate_engineering_artifacts.py",
  "repository_tools/diagnostic_code_index.py",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/templates/RISK.template.md",
  "templates/repository/standard/docs/engineering/templates/README.md",
  "tests/test_risk_management.py",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_catalog.py",
  "tests/test_cli_shape.py",
  "tests/test_fixture_support.py",
  "tests/test_lifecycle_state_contract.py",
  "tests/test_validation_taxonomy.py",
  "docs/notes/README.md",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/risk-artifacts.md",
  "docs/engineering/README.md",
  "docs/engineering/risk-management/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-RSK-010", "REQ-RSK-011", "REQ-RSK-012", "REQ-RSK-013", "REQ-RSK-015"]
specifications = ["SPEC-RSK-010"]
architecture = ["ARCH-RSK-010", "ADR-RSK-010"]
verification = ["VER-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. Selected for execution. This work order carries [delegation] class = execution, so this approval is the delegating act under DR-015 and DR-007; the class activates only from the base of a later pull request, and every non-delegated right stays human. WO-RSK-011 stays draft until this work has merged."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-07T21:02:59Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 008c7b9819df62d1b0bb50f3ac6858a78ca7d1f3 (check-run 101864362911, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-07T22:31:03Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 87708bb28862b9d317d559d4bb782cbd20a4859c (check-run 101879174068, source github-checks)."
+++

# Work Order: Implement the risk artifact, its raise, and the decision pairing

## Objective

Make a threat a governed file: one measured risk, raised by the act of recording
it, stopped through a paired decision, and answered by disposing that decision.
Add no gate predicate and no configuration key.

## In scope

- `se_harness/risks.py`: the risk schema, the score, the lifecycle edges the tool
  applies, the pairing rule read from the graph, and the coordinating function
  that disposes a decision and moves the risk it concerns in one journalled act.
- The type in `se_harness/artifact_layout.py` and
  `se_harness/engine/artifact_layout_registry.py`: prefix `RISK-`, directory
  `risks/`, and the reference pattern.
- The `risk` lifecycle family in `se_harness/workflow_contract.json` and the
  template `WORKFLOW.json`, with the edges of `SPEC-RSK-010`'s state model, and
  the matching rows in the template `WORKFLOW.md`.
- The validator: `E-RSK-001` to `E-RSK-005` and `W-RSK-001`, and the `risk` row
  of the generated artifact catalog in the template `TRACEABILITY.md`, together
  with the three relation rows `threatens`, `mitigated_by` and `avoided_by`.
- `harnessctl raise-risk` and `harnessctl risks` in `se_harness/cli.py`, in the
  command shape of `WO-ECP-021`: `--artifact` for an identifier, refusals exit 2.
- The scope admission of RSK-MGT-026 and RSK-MGT-027 in
  `se_harness/workflow_compliance.py`.
- `RISK.template.md` and its row in the templates index.
- `tests/test_risk_management.py`, plus the existing catalog, command-shape,
  lifecycle and taxonomy tests that pin the type sets.
- The reader's note `docs/notes/risk-artifacts.md` and the two command entries in
  `docs/notes/harnessctl-reference.md`.
- The evidence packet and the verification record of this work order.

## Out of scope

- Closure, the release register, the Explorer and the inspection projection:
  `WO-RSK-011`.
- `DR-RISK-CLOSE` and the managed `DECISION_RIGHTS.md`: `WO-RSK-011`.
- `SPEC-DCM-001`, `se_harness/decisions.py` and the decision family's own
  behaviour: unchanged, by ARCH-RSK-010's dependency direction.
- Any gate predicate or gate group in either quality-gates contract copy, by
  RSK-MGT-014. The copies gain only the six edge bindings of the `risk`
  lifecycle family, each with no predicate and the `QGS-EDGE` structural check,
  because the kernel refuses to load a lifecycle edge that has no binding
  (`WEX-ECP-030`, ECP-KRN-009); the predicate identifier sets stay `main`'s.
- `.engineering-harness.toml.tpl`: unchanged, by RSK-MGT-011.
- The repository's root managed copies: they change at the next release adoption.
- Recording any actual risk of this repository.

## Authorized decision envelope

The implementer may decide: module layout inside `se_harness/risks.py`; whether
the pairing rule is read by the validator, the risk module or both; test names
and placement; the wording of diagnostics, provided each names the field or
identifier the contract requires; the wording of the note and the reference rows;
the option flag spellings of `raise-risk` beyond those the contract fixes.

The implementer may not decide: any rule identifier or diagnostic code of
`SPEC-RSK-010`; the state model; whether a gate predicate is added; whether a
configuration key is added; the dependency direction between the risk and
decision modules; the command names.

This work order carries `[delegation] class = "execution"`. Under `DR-015` the
`delegated-executor` role may apply `DR-WO-START`, `DR-WO-COMPLETE` and
`DR-VREC-PREPARE` for this work order alone, one at a time, only while the
required pull-request check for the candidate head reads `success`. The class is
read at the base of the pull request, so it activates only once this packet has
merged. Every other decision right, including the assurance decision on the
resulting record, stays with the human owner.

## Constraints

- Every risk field is untrusted repository text; render it as text everywhere.
- The disposing act writes two files and must leave neither half-written; use the
  existing journalled apply.
- `tests/test_configuration_surface.py` must pass unchanged, which it will only
  if no configuration key is added.
- The predicate identifier sets of both quality-gates contract copies must equal
  `main`'s.
- Do not edit the repository's root managed copies under
  `docs/engineering/`; the candidate templates are the source.
- Any question that blocks this work order is a `DEC-` artifact naming it in
  `blocks`, not prose in the evidence.

## Expected change surface

The risk module and the layout registry; the CLI parser and two handlers; the
workflow contract's lifecycle families, the family set the kernel accepts, the
two quality-gates contract copies' edge bindings and the three template policy
documents; the transition writer's risk branch; the validator's artifact rules and
the catalog generator; the scope check's path admission; one new template; the
diagnostic-code registry and its generated page; one new test module and four
existing test modules that pin type or command sets; two notes and the notes
index.

## Required verification

`VER-RSK-010`, for the rows of `REQ-RSK-010`, `REQ-RSK-011`, `REQ-RSK-012`,
`REQ-RSK-013` and `REQ-RSK-015`, including acceptance scenarios 1 and 4, the
property and invariant tests other than the register's determinism, the static
checks other than the decision-rights diff, and every security check.

## Evidence to record

`docs/engineering/risk-management/evidence/WO-RSK-010-verification.md`, holding:
the rule-to-case citation map for RSK-MGT-001 to RSK-MGT-021 and RSK-MGT-026,
RSK-MGT-027, RSK-MGT-031, RSK-MGT-033, RSK-MGT-034, RSK-MGT-036; the verbatim
refusal text a threatened artifact receives; the predicate identifier sets of
both contract copies against `main`; the five-key configuration reading; the
governing `validate`, `preflight --phase review` and `check` readings from the
released evaluator outside the checkout, labelled per platform; and the hosted
lane run identifiers as the record.

## Stop and escalate conditions

- The pairing rule cannot be expressed without the decision module importing the
  risk module: stop; the dependency direction is architectural.
- Admitting an added risk path requires widening the scope check beyond one added
  file: stop and raise a decision.
- The scope check cannot admit the path without reading the work order's domain:
  stop; report what it would have to read.
- A rule of `SPEC-RSK-010` cannot be met as written: raise a deviation decision
  against that rule identifier; do not adjust the rule.

## Completion report format

The schema-2 handoff result, then: each rule identifier with its covering test;
the diagnostics added; the files changed against the declared scope; the
configuration and predicate-set readings; the governing readings with commands,
platforms and evaluator version; and the one decision now due with its role.

## Amendment record

2026-09-07, engineering owner, under `DR-REMEDIATION-SCOPE`: added
`docs/engineering/README.md` to `[execution_scope].paths`. The engineering domain
index must name a new domain from the moment the domain exists, by that file's
own maintenance rule, so the packet's own diff touches it. Its omission was a
drafting error in this work order, found by `QGP-G4I-PATHS` reading `WEX201`
against `main` and corrected before start and before any evidence was bound. No
other field changed, and the objective, the in-scope list and the expected change
surface are unaffected.

2026-09-07, engineering owner, under `DR-REMEDIATION-SCOPE`, after the delegated
start and before the first code change: added eight paths. The implementer's
survey measured that the contract cannot be met within the approved paths.
`se_harness/workflow_contract.py` holds the closed family set the kernel accepts,
so `RSK-MGT-007` needs it. The kernel refuses to load any lifecycle edge without
a binding in the quality-gates contract (`WEX-ECP-030`, ECP-KRN-009), so the
`risk` family needs six bindings in `se_harness/quality_gates_contract.json`, the
template `QUALITY_GATES.json` and one row of the template `QUALITY_GATES.md`;
each binding carries no predicate and `QGS-EDGE` only, so `RSK-MGT-014` holds and
the predicate identifier sets stay `main`'s. `se_harness/workflow.py` holds the
one journalled writer and the only permitted writer of a `[disposition]` table,
so `RSK-MGT-016`, `RSK-MGT-018`, `RSK-MGT-019` and `RSK-MGT-020` need it.
`repository_tools/diagnostic_code_index.py` and `docs/notes/diagnostic-codes.md`
register and list the `E-RSK` and `W-RSK` families, without which the code-index
test fails. `docs/notes/README.md` gains the row of the new note. The
quality-gates bullet of `Out of scope` and the expected change surface were
reworded to match; every rule, diagnostic code, state and constraint is
unchanged.

2026-09-07, engineering owner, under `DR-REMEDIATION-SCOPE`, after the full
test suite was first run against the implementation: added
`tests/test_artifact_authoring.py` and `tests/test_fixture_support.py`. Both pin
the installed surface and change by one line each: the first expects the state a
created risk starts in, `identified`, as it expects `open` for a decision; the
second counts the files `init` installs, which the risk template raises from 41
to 42. They are of the kind the in-scope list names, "existing tests that pin
the type sets", and were not enumerated. A control run on a clean `main`
worktree showed the two other failing tests of the Windows run fail there too
(the owner-region byte count and a `PermissionError` on Git objects), so they
are not this work's.
