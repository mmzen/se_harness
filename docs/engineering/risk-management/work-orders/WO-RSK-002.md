+++
id = "WO-RSK-002"
type = "work_order"
title = "Close the accepted deviations of the risk artifact"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes the mutation guard, the doctor check set, and the portable skill cores and their pinned digests; later engineering and assurance decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/mutation_guard.py",
  "se_harness/preflight.py",
  "se_harness/artifact_layout.py",
  "se_harness/cli.py",
  "se_harness/skill_contract.py",
  "templates/repository/standard/.agents/skills/",
  "tests/",
  "docs/notes/risk-management.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/engineering/risk-management/evidence/",
]

[relations]
implements = ["REQ-RSK-007"]
specifications = ["SPEC-RSK-002"]
verification = ["VER-RSK-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "engineering-owner"
+++

# Work Order: Close the accepted deviations of the risk artifact

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Implement `SPEC-RSK-002`: the dedicated guard operation, the `doctor` check,
the skill-core integration with regenerated vectors, and the three amendments
that make the specification match what `WO-RSK-001` shipped.

## In scope

- `raise-risk` guard operation; `C-RSK-001` doctor check.
- `harness-draft-change`, `harness-execute-work-order`, `harness-prepare-assurance`
  cores, helpers, contracts, and vectors.
- Tests for each rule; note and reference updates.
- Work-order-keyed evidence.

## Out of scope

- The Explorer register view; any change to the artifact schema, family,
  gates, decision rights, or the Claude adapters; a release or root upgrade.

## Authorized decision envelope

Skill sentence wording that preserves the approved semantics; test names;
fixture layout. Not: operation name, check identifier, the amendment
semantics, or any path outside scope.

## Constraints

Use the exact external released evaluator for identity, integrity, graph,
focus, and preflight; regenerate vectors with `build_skill_manifest`; LF line
endings.

## Expected change surface

Guard, preflight, artifact layout, CLI, skill contract parser, three skill
cores, vectors, tests, two notes, evidence.

## Required verification

Execute `VER-RSK-002` completely plus the repository-required checks; full
suite on Windows and Linux; released-evaluator validation and review
preflight; handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/risk-management/evidence/WO-RSK-002/`.

## Stop and escalate conditions

Stop if a skill sentinel cannot distinguish a new risk file from a disposed
one, or if any path outside scope must change.

## Completion report format

The `harnessctl check . --artifact WO-RSK-002 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
