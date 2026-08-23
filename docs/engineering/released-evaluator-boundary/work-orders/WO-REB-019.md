+++
id = "WO-REB-019"
type = "work_order"
title = "Centralize lifecycle semantics and rejected-history handling"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[assurance]
commit_bound_verification = "required"
rationale = "Transition, assurance, release preparation, graph validation, and future governance migration decisions will rely on the centralized lifecycle registry; a drift or authority error could block or misstate a release, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-018.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-019.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-009.md",
  "docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-008.md",
  "docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-008.md",
  "docs/engineering/released-evaluator-boundary/verification/VER-REB-008.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-019.md",
  "docs/engineering/released-evaluator-boundary/evidence/WO-REB-019-lifecycle-state-contract.md",
  "docs/notes/lifecycle-state-contract.md",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow.py",
  "se_harness/provenance.py",
  "se_harness/governance_migration.py",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "tests/test_lifecycle_state_contract.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_execution.py",
  "tests/test_release_bootstrap.py",
  "tests/test_governance_migration.py",
]

[relations]
implements = ["REQ-REB-018", "REQ-REB-019"]
specifications = ["SPEC-REB-009"]
architecture = ["ARCH-REB-008", "ADR-REB-008"]
verification = ["VER-REB-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T10:05:17Z"
decided_by = "engineering-owner"
+++

# Work Order: Centralize lifecycle semantics and rejected-history handling

## Lifecycle and authorization

The accountable owners approved `REQ-REB-018`, `REQ-REB-019`, `SPEC-REB-009`, `ARCH-REB-008`, `ADR-REB-008`, `VER-REB-008`, and this work order on 2026-08-23 for the bounded GitHub issue #103 / RCA `RC-060-03` scope. The engineering owner separately authorized start, and exact released `se-harness==0.5.0` passed start preflight in the deterministic predecessor-compatible view after the complete candidate graph passed current validation.

The approval authorizes bounded implementation and local qualification only. Commit, push, pull request, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, credential use, external policy change, and operational root-evaluator adoption remain unauthorized.

Complete-graph qualification then exposed seven terminal compatibility states
missing from the initial exact matrix. The owner approved the bounded amendment
to add definition `ready`, `in_progress`, `verified`, `released`, and
`superseded`, and work-order `ready` and `superseded`, with no new transitions,
reservations, or adapter behavior. WO-REB-019 remains `in_progress`; every
original authorization boundary remains unchanged.

## Objective

Replace duplicated lifecycle status and version-reservation policy with one strict workflow v3 lifecycle registry consumed by transition, provenance, validation, and migration checks, while preserving candidate 0.6 rejected-history behavior and keeping the released 0.5 boundary explicit.

## In scope

- Advance the packaged and managed-template workflow contract from v2 to v3 and replace the standalone transition map with the complete state registry in `SPEC-REB-009`.
- Add strict all-or-nothing lifecycle parsing and immutable semantic indexes to `se_harness.workflow_contract`.
- Remove the independent transition loader/table from `se_harness.workflow` and consume the canonical index for edges and VREC/RLS authority-sensitive predicates.
- Make `se_harness.provenance` use registry version-reservation semantics when preparing same-version releases and use registry authority semantics where formal authority is selected.
- Make the standalone candidate validator derive admitted/global/type states, transition edges, authority status, and active release-version uniqueness from adjacent managed `WORKFLOW.json`.
- Keep dashboard/inspection behavior aligned through validator-derived semantics; change another managed script only if review proves it contains an independent contradictory authority rule, in which case stop for scope amendment rather than editing it implicitly.
- Bind the migration rehearsal's rejected-state compatibility observation to the registry marker without implementing or broadening a production compatibility view.
- Add the focused contract/consumer/rejected-history test matrix, package parity checks, hostile contract cases, and Windows/Linux qualification required by `VER-REB-008`.
- Add one developer/operator note and retained `WO-REB-019` evidence.

## Out of scope

- Editing root managed files, `.engineering-harness.lock`, `.engineering-harness.toml`, or the exact external released 0.5 evaluator.
- Implementing or consolidating production compatibility views from issue #104.
- Adding role-specific release commands from issue #109.
- Performing root adoption, release preparation, release, publication, deployment, or any credential-bearing operation.
- Rewriting, deleting, moving, reopening, or superseding historical VREC, RLS, REL, candidate, evidence, tag, distribution, or RCA facts.
- Treating the v3 registry as permission to import candidate code into a predecessor process.
- Adding diagnostic allowlists, caller-selected omissions, a self-hosting profile, generated policy-bearing Python copies, or a fallback lifecycle vocabulary.
- Changing release-version syntax, work-completion rules, lifecycle decision rights, metadata field meaning beyond rejected-state consistency, or the current transition graph.

## Authorized decision envelope

After packet approval and explicit start, implementation may choose internal immutable index types, helper names, diagnostic suffixes, and focused test-module organization. It may refactor existing status predicates only where the specification assigns them to a registry semantic.

It may not add/remove a state, edge, authority flag, reservation flag, visibility rule, or predecessor-adapter marker; change schema v3 field names; broaden compatibility behavior; modify an out-of-scope file; or alter historical records without a separately reviewed amendment.

## Constraints

- Python 3.11+ standard library only for contract parsing and lifecycle indexing.
- Preserve deterministic UTF-8/LF JSON and duplicate-key rejection.
- Validate the entire lifecycle registry before exposing any index or performing any repository write.
- Treat contract paths/bytes, artifact metadata, Git state, package data, and environments as untrusted.
- Keep package and standalone validator roles isolated; semantic parity is proven through common contract data and tests, not shared candidate imports.
- Root managed copies remain byte-for-byte owned by the released evaluator.
- Do not build promotable distributions; candidate package tests may build only clearly non-promotable ephemeral artifacts outside the checkout.

## Expected change surface

- Seven draft/approved packet artifacts and one later evidence file under `released-evaluator-boundary`.
- Workflow contract source and managed-template copy, strict loader, transition consumer, provenance consumer, and migration observation.
- Candidate managed workflow prose and standalone validator.
- One lifecycle-contract note and five focused/existing test modules.

The execution scope is a maximum allowlist, not a requirement to modify every file. If implementation proves another production file contains an authority or version-reservation rule that contradicts the registry and cannot safely remain, stop and request an explicit scope amendment.

## Required verification

- Execute every method and case in `VER-REB-008`.
- Prove exact contract byte parity across source, managed template, installed fixture, sdist, and wheel.
- Prove planner, validator, release preparation, and migration observations agree for every registry row and reject every malformed registry variant.
- Re-run rejected/corrected same-version history, complete current validation, explicit predecessor assessment, and issue #101 migration scenarios.
- Run focused tests, the complete supported suite, graph, distribution, portable-surface, CLI-help, managed-parity, whitespace, and diff checks.
- Run candidate source/package and Windows/Linux hosted lanes without credentials or privileged operations.
- Independently prove root, history, refs, release identities, credentials, and external services unchanged.

## Evidence to record

Record the exact approved preflight manifest; contract v2/v3 structural diff; canonical contract bytes/hash; independent lifecycle matrix; all consumer matrix results; rejected-history before/after hashes; same-version property results; malformed-contract corpus; package/install parity; issue #101 rehearsal results; predecessor/current validation distinction; focused/full/platform commands and outputs; changed paths; candidate commit when separately authorized; hosted run identities; and every lifecycle or external action not performed.

## Stop and escalate conditions

- A consumer needs semantics not represented by the approved registry fields.
- A new state, edge, flag, decision right, metadata meaning, or release-version rule is needed.
- A standalone predecessor check can pass only by importing candidate code, patching the root, hiding unbound history, or accepting diagnostics.
- Issue #104 or #109 implementation is required to make this packet pass.
- Historical record bytes, root managed files, root evaluator identity, Git refs, credentials, or external state would change.
- Contract parity, complete validation, rejected succession, package conformance, deterministic replay, or cross-platform agreement cannot be proven.

Retain the failing case and request a bounded amendment; do not absorb another RCA issue or create a bypass.

## Completion report format

Report workflow schema and exact registry matrix; consumers changed; removal of independent policy constants; rejected/same-version results; predecessor/current distinction; package and platform results; root/history/external non-mutation proofs; changed paths; evidence path; candidate/VREC state; residual risks; actions not performed; and one next accountable decision.
