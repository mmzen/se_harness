+++
id = "WO-HUP-005"
type = "work_order"
title = "Adopt the released successor of 0.6.0 as the standard root evaluator"
status = "draft"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "Every later root lifecycle action and managed CI gate depends on the exact public successor, its schema-3 lock, and complete-graph validation established by this transaction."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".gitattributes",
  ".github/workflows/engineering-harness.yml",
  "AGENTS.md",
  "CLAUDE.md",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/OPERATING_CARD.md",
  "docs/engineering/QUALITY_GATES.json",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/README.md",
  "docs/engineering/TECHNICAL_COMMUNICATION.md",
  "docs/engineering/TRACEABILITY.md",
  "docs/engineering/WORKFLOW.json",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/templates/",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-005.md",
  "docs/notes/developing-se-harness.md",
  "scripts/artifact_layout_registry.py",
  "scripts/check_engineering_harness.ps1",
  "scripts/check_engineering_harness.sh",
  "scripts/generate_harness_dashboard.py",
  "scripts/harness_explorer/index.template.html",
  "scripts/inspect_engineering_artifacts.py",
  "scripts/select_harness_work_order.py",
  "scripts/validate_engineering_artifacts.py",
  ".agents/skills/",
  ".claude/skills/",
  "tests/",
]

[relations]
implements = ["REQ-HUP-010", "REQ-HUP-011"]
specifications = ["SPEC-HUP-005"]
verification = ["VER-HUP-005"]
+++

# Work Order: Adopt the released successor of 0.6.0 as the standard root evaluator

## Lifecycle

This draft cannot be approved until a `released` release record covering
`WO-ADS-001`, `WO-ADS-002`, and `WO-RSK-001` exists on `main` and its
version and digests are copied into an `[evaluator_upgrade]` table here
(`HUP5-PRE-001`). Approval authorizes only the scope below; the apply step
is a separate repository-owner authorization at action time.

## Objective

Replace this repository's 0.6.0 root evaluator with the exact released
successor so that the operating card, the closed reading manifest, the
corrective forms, the router scope, and the risk artifact are in effect
here; retire the test exceptions that recorded the interim skew.

## In scope

- Complete the `[evaluator_upgrade]` table from the release record.
- Prove the successor in isolation; retain identity evidence.
- Plan, review, and apply the standard-root upgrade; commit the new lock,
  managed copies, fragments, and the merged `[risk]` section.
- Run every postcondition of `SPEC-HUP-005`; retire the five test
  exceptions; update the two notes.
- Retain evidence; the work order's own file changes only through the
  table completion and lifecycle events.

## Out of scope

- Building or publishing the release; changing any candidate template;
  disposing any risk raised in the scratch postcondition beyond withdrawing
  it; any operating change to consumers.

## Authorized decision envelope

Evidence file layout; the scratch domain name for `HUP5-PST-002`; test
rewrite style (equality vs template-to-template). Not: the target identity,
the managed set, the fragment bytes, or any path outside scope.

## Constraints

Run the proof and the transaction from the isolated successor only; 0.6.0
remains the governor until the lock is replaced; never edit a managed root
file by hand.

## Expected change surface

Lock, installation file, CI workflow, managed policy documents and
contracts, router, card, templates, eight managed scripts, skills, fragments,
tests, two notes, evidence.

## Required verification

`VER-HUP-005` completely; full suite on Windows and Linux; the successor's
`doctor`, `validate`, `preflight`, and handoff check.

## Evidence to record

Under `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-005/`
plus `WO-HUP-005-evaluator-upgrade.json` in the domain evidence directory,
as `WO-HUP-002` did.

## Stop and escalate conditions

Stop if no released record covers the three work orders, if the isolated
identity is candidate-source or digests differ, if the plan touches a path
outside the expected managed set, or if any postcondition fails.

## Completion report format

The `harnessctl check . --artifact WO-HUP-005 --checkpoint handoff` schema-2
block verbatim from the successor, with the complete changed-path set, and
its `result_sha256`.
