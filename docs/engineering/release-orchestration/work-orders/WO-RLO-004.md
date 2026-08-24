+++
id = "WO-RLO-004"
type = "work_order"
title = "Implement recipe-bound release build replay"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "Future release and publication decisions will rely on changed build provenance schemas, candidate execution, tool supply, hosted qualification, and production credential boundaries."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/scripts/publish_release.py",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/release-candidate-replay.yml",
  "AGENTS.md",
  "docs/engineering/REPOSITORY_CONTEXT.md",
  "docs/engineering/release-orchestration/README.md",
  "docs/engineering/release-orchestration/acceptance/release-build-recipe.feature",
  "docs/engineering/release-orchestration/architecture/ARCH-RLO-004.md",
  "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-004.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-004-verification.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-013.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-014.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-004.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-004.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-004.md",
  "docs/notes/developing-se-harness.md",
  "release/build-recipe.json",
  "release/build-toolchain.lock",
  "repository_tools/release_build.py",
  "repository_tools/release_distribution.py",
  "scripts/create_release_bundle_manifest.py",
  "scripts/replay_release_build.py",
  "scripts/validate_release_distributions.py",
  "se_harness/hash_bound_classes.json",
  "tests/test_context_routing_retirement.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "tests/test_maintenance_branch.py",
  "tests/test_pypi_publishing.py",
  "tests/test_release_build.py",
  "tests/test_release_orchestration.py",
]

[relations]
implements = ["REQ-RLO-013", "REQ-RLO-014"]
specifications = ["SPEC-RLO-004"]
architecture = ["ARCH-RLO-004", "ADR-RLO-004"]
verification = ["VER-RLO-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T12:02:52Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T12:58:09Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement recipe-bound release build replay

## Lifecycle

This draft is a bounded proposal for GitHub issue #110. Approval would authorize only the declared recipe, repository tooling, schema compatibility, no-credential workflows, documentation, tests, retained evidence, and exact paths. Separate explicit transitions are required to approve the definition packet and start this work order.

Implementation completion, candidate commit, push, pull request, hosted dispatch, VREC preparation or decision, RLS preparation or decision, release, tag, publication, deployment, maintenance mutation, credentials, external policy, and governor adoption remain separate decisions.

## Objective

Make future SE Harness release bytes reproducible from one complete RLS-bound machine-readable recipe, and prove the exact accepted wheel and normalized sdist in an independent hosted no-credential replay before release approval.

## In scope

- Add canonical candidate-tree recipe and full hash-locked build-toolchain files.
- Add one strict repository parser, planner, and immutable-OCI producer adapter using argument arrays and a closed environment.
- Build twice with isolated state, observe the exact producer/runtime/tool inventory, compare bytes, and retain bounded replay evidence.
- Advance repository bundle and distribution provenance to recipe-bearing schema 2 for new ready records.
- Preserve already released schema-1 records and their isolated legacy publication replay without rewriting history.
- Make manifest creation, binder validation, repository distribution validation, hosted pre-release replay, and schema-2 production qualification use the same repository implementation.
- Add one read-only, one-RLS-input hosted pre-release workflow for ready records.
- Remove schema-2 build-tool, environment, command, and normalization duplication from publication YAML.
- Preserve privileged-job separation and inert-byte transfer.
- Add complete schema, property, failure, compatibility, package-boundary, workflow-policy, local real-build, and hosted exact-replay tests.
- Update focused repository instructions and retain work-order-keyed evidence.

## Out of scope

- Native Linux and Windows runner, shell, virtual-environment, path, and cleanup parity governed by issue #111.
- Modifying `RLS-SEH-012`, any historical VREC/RLS/evidence, v0.6.0 distribution bytes, tag, GitHub Release, PyPI state, Pages deployment, or maintenance line.
- Adding recipe semantics to portable `harnessctl`, the packaged `se_harness` namespace, managed consumer templates, consumer CI, or root hash-locked managed files.
- Adding a general build plugin, multi-ecosystem recipe framework, remote build service, custom credential, private registry, new package format, prerelease channel, or cache authority.
- Approving or preparing a concrete product release; exercising a verification/release decision; committing, pushing, opening a PR, dispatching hosted work, publishing, deploying, or changing external configuration under this proposal alone.

## Authorized decision envelope

After approval and start, the implementation agent may choose internal repository-module types and names, temporary layout, bounded diagnostic codes, deterministic JSON helpers, process timeouts, and test-fixture factoring. The agent must select and record one exact public Linux/amd64 OCI digest, exact CPython 3.11 patch, and complete hash-locked tool inventory that preserve the currently qualified build contract.

The agent may not change recipe/schema locations or names, use a mutable producer, permit host fallback or environment inheritance, allow free-form commands, omit transitive tools, weaken two-build or expected-hash comparison, remove schema-1 historical replay, broaden schema 1 to new ready records, add workflow identity inputs, move candidate execution into privileged jobs, absorb issue #111, or change portable product policy.

## Constraints

- Treat repository, Git, RLS, JSON, lock, image, package, environment, path, command, archive, output, and workflow data as untrusted.
- Validate recipe and binding before candidate execution; execute candidate content only inside the no-credential producer.
- Keep exact image and package identities public and hash-addressed; add no credential or secret.
- Use fresh source, tool, cache, raw, normalized, and output state for each build.
- Keep accepted hashes immutable during replay and fail on unavailable exact inputs.
- Preserve candidate-source versus released-root ownership; do not edit root managed files.
- Preserve unrelated repository work, including the existing draft `WO-HBI-002`.
- Do not build or describe a promotable product release under this engineering work order. Real package tests are non-promotable implementation evidence outside the checkout.

## Expected change surface

Exactly the thirty-one paths declared in `[execution_scope]`, including the three-path bounded scope amendment authorized on 2026-08-24; authorized paths that prove unnecessary may remain unchanged. No other path may enter the implementation diff without a separately reviewed scope amendment.

## Required verification

- Start and review preflight for `WO-RLO-004` at the appropriate lifecycle stages.
- Every method, matrix, invariant, and manual review in `VER-RLO-004`.
- Exact issue reproduction showing the current RLS/workflow split identity, followed by corrected schema-2 resolution and replay.
- Focused recipe, distribution, release-build, orchestration, PyPI, maintenance, and instruction tests.
- Local two-producer exact build and a separately authorized hosted exact-candidate pre-release replay against already accepted hashes.
- Historical `RLS-SEH-012` schema-1 resolution/replay compatibility without mutation.
- Built-wheel and disposable consumer inspection proving repository policy exclusion.
- Complete unit suite, formal graph validation, repository distribution validation, CLI help, exact released-0.6.0 doctor/validate, inspection, strict YAML parsing, managed-source parity, `git diff --check`, and exact changed-path scope comparison.

## Evidence to record

Retain the approved scope, baseline and corrected identity maps, exact candidate, recipe, lock, image and package hashes, local A/B build results, accepted wheel/sdist hashes, hosted run and result digest, schema and failure matrices, RLS unchanged-byte proofs, workflow permissions and command-source comparison, historical compatibility, package/consumer boundaries, commands and test counts, warnings, deviations, residual risks, and every unperformed lifecycle or external action under `docs/engineering/release-orchestration/evidence/WO-RLO-004-verification.md`.

## Stop and escalate conditions

Stop for an invalid graph or managed integrity failure; recipe identity that cannot be complete; unavailable exact public producer/tool bytes; need for a credential or mutable tag; host fallback; arbitrary recipe execution; incomplete installed inventory; nondeterministic or mismatched outputs; new-ready schema-1 requirement; historical rewrite; portable or root-managed impact; candidate execution in a privileged job; path outside scope; issue #111 dependency required for #110 correctness; or any lifecycle/external action needed to claim implementation completion.

## Completion report format

Report the complete bound identity; schema-1/schema-2 behavior; exact recipe, producer, Python, toolchain, environment, command, and normalizer facts; local and hosted replay hashes; workflow permission boundaries; historical and portable compatibility; changed paths; tests and validation; evidence path; work-order state; candidate identity if separately authorized; deviations and residual risks; and every excluded commit, push, PR, hosted dispatch, VREC/RLS transition, release, tag, publication, deployment, credential, maintenance, external-policy, or governor action.
