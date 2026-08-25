+++
id = "WO-RSK-001"
type = "work_order"
title = "Implement the risk artifact, its lifecycle, gates, commands, and configuration"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes managed contracts (traceability, workflow, quality gates, decision rights), the validator, the installer configuration, and public commands. Future engineering, assurance, and release decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/templates/",
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/scripts/artifact_layout_registry.py",
  "templates/repository/standard/scripts/inspect_engineering_artifacts.py",
  "templates/repository/standard/scripts/generate_harness_dashboard.py",
  "templates/repository/standard/scripts/harness_explorer/",
  "templates/repository/standard/.agents/skills/",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_procedures.py",
  "se_harness/artifact_layout.py",
  "se_harness/provenance.py",
  "se_harness/preflight.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  "se_harness/skill_contract.py",
  "pyproject.toml",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/README.md",
  "docs/notes/risk-management.md",
  "docs/engineering/risk-management/evidence/",
]

[relations]
implements = ["REQ-RSK-001", "REQ-RSK-002", "REQ-RSK-003", "REQ-RSK-004", "REQ-RSK-005", "REQ-RSK-006"]
specifications = ["SPEC-RSK-001"]
architecture = ["ARCH-RSK-001", "ADR-RSK-001"]
verification = ["VER-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the risk artifact, its lifecycle, gates, commands, and configuration

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Implement `SPEC-RSK-001` in the candidate source and standard templates so
that a risk can be identified anywhere, is raised by policy, is disposed by
the stage owner, blocks the stage it threatens, and is listed by the release
that ships with it.

## In scope

- Validator and layout registry: `risk` type, `risks/` directory, `[risk]`
  schema, `E-RSK-001/002`, relation pairs `TRC-REL-020..023`, stage/type
  match, residual requirement.
- Managed contracts: lifecycle family, `WFL-RISK-RAISED`,
  `WFL-RISK-MITIGATING`, procedures, `STEP-*-RISKS` reading steps,
  corrective forms; evaluator and seven predicates; `DR-RISK-DISPOSE` and the
  stage table; `TRACEABILITY.md`, `WORKFLOW.md`, `QUALITY_GATES.md`,
  `DECISION_RIGHTS.md` prose; `RISK.template.md`.
- `[risk]` section in the installation template; `doctor` check `C-RSK-001`.
- Commands `raise-risk` and `risks`; `transition` role resolution by stage;
  `prepare-release` deriving `lists_risks` and the record table; scope
  exception in `workflow_compliance`.
- Explorer register view; `inspect` raised queue.
- Skill cores: draft and execute may raise; prepare-assurance includes the
  register; contracts updated and digests re-recorded.
- Tests and fixtures per `VER-RSK-001`; one non-authoritative note;
  reference updates; work-order-keyed evidence.

## Out of scope

- Approving or transitioning any definition or this work order.
- Editing root managed copies or the lock of this repository.
- A dedicated risk-owner role; per-category levels; any scale but 5x5;
  quantitative models; independence checks between raiser and disposer.
- Building a release or upgrading the governor.

## Authorized decision envelope

The implementation agent may decide internal names, diagnostic numbers in
the reserved `RSK` family, template wording that preserves the approved
semantics, fixture layout, and note structure. It may not change the state
names, the stage table, the default level, the blocking rules, the relation
pairs, or any path outside scope.

## Constraints

- Use the exact external released evaluator for identity, integrity, graph,
  focus, and preflight results; the candidate for implementation and tests.
- Keep packaged and template contracts byte-identical.
- LF line endings; stage deletions before any preflight.

## Expected change surface

Validator, layout registry, four managed policy documents and two machine
contracts, installation template, artifact template, six package modules,
skill cores and contracts, tests, one note, evidence.

## Required verification

Execute `VER-RSK-001` completely plus the repository-required checks; full
suite on Windows and Linux, figures labelled per platform; released
evaluator validation and review preflight; handoff check with the complete
changed-path set.

## Evidence to record

Under `docs/engineering/risk-management/evidence/WO-RSK-001/`: commands and
results, per-platform figures, gate matrix outcomes, Scenario 2 transcript,
complete changed-path set, material deviations.

## Stop and escalate conditions

Stop if a predicate cannot be added to a gate without changing its
checkpoint set, if the scope exception cannot be bounded to undisposed
risk files, if the stage table cannot resolve a threatened artifact type,
or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-RSK-001 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
