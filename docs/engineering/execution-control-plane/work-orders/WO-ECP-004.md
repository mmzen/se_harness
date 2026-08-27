+++
id = "WO-ECP-004"
type = "work_order"
title = "Authenticated decision records"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes how every lifecycle transition establishes who decided. Every future approval, verification, and release event will be accepted or refused by this code, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/decision_record.py",
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-008"]
specifications = ["SPEC-ECP-004"]
architecture = ["ARCH-ECP-001", "ADR-ECP-003"]
verification = ["VER-ECP-004"]
+++

# Work Order: Authenticated decision records

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-008`,
`SPEC-ECP-004`, `ARCH-ECP-001`, `ADR-ECP-003`, and `VER-ECP-004` are
separate acts by their owners and precede approval of this work order. This
work order is independent of the others in the packet.

## Objective

Make "accountable humans retain authority" an enforced property. Today a
decision is `--decision ID=ACTOR`, validated for length and control
characters only (`se_harness/workflow.py:606`; `se_harness/cli.py:1037`),
and no Git-author, `GITHUB_ACTOR`, `CODEOWNERS`, or signature check exists
in `se_harness/` or `scripts/` (the 2026-08 agentic execution review,
section 3, "Human control"; section 5, weakness 1).

## In scope

- `se_harness/decision_record.py`, a new module: the record schema
  (artifact, decision right, outcome, reason, signer), signature
  verification against the configured identity source, and the role check
  against `DECISION_RIGHTS.md`, per `ECP-DEC-*`.
- `transition --apply --decision-record <path>` consuming records;
  `--decision ID=ACTOR` refused with a pointer to the record form.
- The configuration template gaining the identity-source section; the
  template `DECISION_RIGHTS.md` and `WORKFLOW.md` describing the record and
  its refusal codes.
- Tests with a fixture identity source and throwaway keys; work-order-keyed
  evidence.

## Out of scope

- Any transition of any artifact in this repository; the delegation class
  (`WO-ECP-006`); evaluating contract gates inside `transition`
  (`WO-ECP-005`); root managed copies and the root configuration file; any
  change to lifecycle states, gate predicates, or the decision-rights table
  itself.

## Authorized decision envelope

The implementation agent may decide the record serialisation, the signature
scheme among those the standard library can verify, the diagnostic code
numbers, and test names. It may not accept an unverified signer, accept a
role outside the rights table, read the identity source from an
environment path, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings;
  exercise the candidate `transition` only against temporary repositories.
- Root managed copies and `.engineering-harness.toml` at the root are not
  edited; the template `.tpl` is.
- LF line endings; assert bytes against blobs.
- Stage every deletion before any preflight or check run.
- No private key enters the tree or the evidence.

## Expected change surface

CLI parser and dispatch, the transition planner's decision validation, one
new module, one configuration template, two policy templates, tests,
evidence. `se_harness/decision_record.py` does not exist today and is listed
in scope as a path to be created.

## Required verification

Execute `VER-ECP-004` completely plus the repository-required checks; run
the complete suite on Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-004/`:
the fixture identity source, public fingerprints, each record with its
verdict, refusal diagnostics, per-platform test figures, and the complete
changed-path set.

## Stop and escalate conditions

Stop if signature verification needs a dependency outside the standard
library, if the identity source cannot be expressed in the configuration
template without a schema-version bump, if the released evaluator refuses
the new configuration section, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-004 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
