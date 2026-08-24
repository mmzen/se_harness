+++
id = "WO-REB-020"
type = "work_order"
title = "Implement role-specific release qualification commands"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "Candidate, predecessor, release, publication, and future root-health decisions will rely on the evaluator/target bindings, independence claims, workflow wiring, and canonical evidence introduced here; a substitution or provenance defect could misstate release assurance, so verification must bind the exact implementation commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/candidate-evidence.yml",
  ".github/workflows/predecessor-evaluator-assessment.yml",
  ".github/workflows/publish-dashboard-pages.yml",
  ".github/workflows/publish-pypi.yml",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-009.md",
  "docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-009.md",
  "docs/engineering/released-evaluator-boundary/evidence/WO-REB-020-role-specific-qualification.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-020.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-021.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-022.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-010.md",
  "docs/engineering/released-evaluator-boundary/verification/VER-REB-009.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-020.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/evaluator-migration-rehearsal.md",
  "docs/notes/harness-dashboard-publication.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/release-qualification-roles.md",
  "repository_tools/predecessor_assessment.py",
  "repository_tools/predecessor_preparation.py",
  "repository_tools/predecessor_publication.py",
  "repository_tools/release_bootstrap.py",
  "repository_tools/release_distribution.py",
  "scripts/assess_predecessor_evaluator.py",
  "scripts/check_portable_release_surface.py",
  "scripts/prepare_predecessor_release.py",
  "scripts/validate_governor_transition.py",
  "scripts/validate_predecessor_publication_view.py",
  "scripts/validate_release_distributions.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/cli.py",
  "se_harness/evaluator_identity.py",
  "se_harness/governance_migration.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/runtime_identity.py",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "tests/mutation_guard_support.py",
  "tests/test_dashboard_publication.py",
  "tests/test_evaluator_identity.py",
  "tests/test_governance_migration.py",
  "tests/test_harnessctl.py",
  "tests/test_instruction_architecture.py",
  "tests/test_mutation_guard.py",
  "tests/test_predecessor_assessment_contract.py",
  "tests/test_predecessor_preparation.py",
  "tests/test_predecessor_publication.py",
  "tests/test_progressive_documentation.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "tests/test_release_orchestration.py",
  "tests/test_release_qualification.py",
  "tests/test_standard_repository_lifecycle.py",
]

[relations]
implements = ["REQ-REB-020", "REQ-REB-021", "REQ-REB-022"]
specifications = ["SPEC-REB-010"]
architecture = ["ARCH-REB-009", "ADR-REB-009"]
verification = ["VER-REB-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T08:17:36Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement role-specific release qualification commands

## Lifecycle and authorization

This draft packet proposes the bounded implementation for GitHub issue #109 / RCA `RC-060-09`, including the independent-candidate-verifier boundary tracked by issue #46. It grants no execution or lifecycle authority while draft.

If the accountable owners approve the seven definition artifacts and this work order, a separate explicit start may authorize only the local implementation and qualification described here. Approval/start do not authorize a candidate commit, push, pull request, hosted dispatch, credential use, VREC/RLS preparation or transition, release, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade.

## Objective

Replace release-workflow selection of raw validator and executable paths with five typed `harnessctl qualify` operations that enforce evaluator/target compatibility, process isolation, provenance, independence semantics, canonical results, and workflow conformance before their output can be used as release evidence.

## In scope

- Add the `harnessctl qualify` namespace and exactly the five operations in `SPEC-REB-010`.
- Add one package-owned qualification layer for parser dispatch, role contracts, identity/target binding, fixed checks, canonical result construction, exclusive atomic output, stable diagnostics, cleanup, and no-change proof.
- Extend existing evaluator/runtime identity code only where required to represent the five fixed roles and independently bind installed/archive/payload/entry-point/checkout identities.
- Reuse the hardened candidate acceptance implementation for `candidate-package`; convert `accept-candidate` to a thin one-cycle compatibility alias.
- Preserve exact public 0.6.0 `accept-candidate` only as the initial independent candidate-package bootstrap lane: bind its fixed archive/payload/entry-point identity and legacy schema, forbid relabeling it as canonical qualification output, and encode removal when a typed released verifier becomes available.
- Reuse the production predecessor preparation/assessment/publication services behind the `predecessor-view` handler, eliminating raw script selection from workflows without duplicating or broadening view policy.
- Adapt repository scripts to thin typed wrappers where they remain useful for compatibility or local operation.
- Migrate repository-owned candidate, predecessor-assessment, PyPI-publication, and dashboard-publication qualification steps to the matching role operations.
- Update only the candidate managed-workflow template so future upgrades install typed released-root behavior; preserve the currently installed root managed workflow.
- Add the command/role documentation, workflow map, package/help surface, focused/adversarial tests, Windows/POSIX coverage, and retained work-order evidence required by `VER-REB-009`.

## Out of scope

- Editing `.engineering-harness.lock`, `.engineering-harness.toml`, root `ENGINEERING_HARNESS.md`, root `.github/workflows/engineering-harness.yml`, root managed docs, or root managed scripts.
- Changing lifecycle workflow v3, rejected-history semantics, version reservation, predecessor-view contents/omission policy, release-record schema, or governance-migration stage policy.
- Removing support for exact pre-command predecessors beyond the bounded adapter or claiming their partial view is complete validation.
- Changing product version, building promotable distributions, preparing/transiting VREC or RLS records, releasing, tagging, publishing, deploying, upgrading/adopting the root evaluator, or mutating maintenance state.
- Rewriting historical artifacts, evidence, commits, refs, release records, verification records, tags, distributions, RCA facts, or hosted results.
- Adding credentials/network access, caller-selected omissions, diagnostic allowlists, arbitrary validator/script execution, a free-form role flag, candidate root authority, or an emergency bypass.
- Resolving the distinct `prepared_at` VREC succession defect tracked by issue #123.

## Authorized decision envelope

After approval and explicit start, implementation may choose private class/function names, dataclass boundaries, subprocess buffering, temporary-directory layout, diagnostic suffixes, test-module decomposition, and concise human formatting. It may refactor allowlisted predecessor/release helpers into package-owned reusable functions when required by the public CLI, provided behavior and trust boundaries stay unchanged and repository wrappers delegate to one implementation.

It may not add/remove/rename a qualification operation, introduce a general role/script selector, change an independence classification, relax identity or isolation, change canonical result fields, alter compatibility-view or lifecycle policy, touch an unlisted path, or broaden workflow/external authority. If a required production dependency lies outside the execution scope, stop and request a reviewed amendment.

## Constraints

- Python 3.11+ standard library only for the new qualification layer.
- Treat repository/package/archive/view/release/manifest/Git/environment/subprocess inputs as untrusted.
- Establish evaluator identity before importing or executing repository-controlled code.
- Use isolated argument-vector subprocesses with minimal environments; never load candidate/successor code in released-verifier or predecessor interpreters.
- Preserve deterministic UTF-8/LF canonical JSON, stable check ordering, bounded diagnostics/output, exclusive atomic output, and cross-platform path handling.
- No operation opens a network connection, reads credentials, mutates the inspected repository/root/refs/lifecycle/external state, or grants authority.
- The root managed workflow and exact installed root evaluator remain unchanged. Candidate template drift is expected until a later governed upgrade installs it.
- Temporary builds/installations are clearly non-promotable, external to the checkout, and removed after tests unless separately retained as evidence.

## Expected change surface

- Eight proposal artifacts and one later evidence file in the released-evaluator-boundary domain.
- One new package module plus bounded CLI, identity, candidate-acceptance, migration, and provenance integration.
- Existing production predecessor/release services and their thin script adapters.
- Four repository-owned workflows and one candidate managed-workflow template.
- Six operator/developer notes including one new role guide.
- Focused qualification tests and adjacent existing workflow, release, migration, identity, package, dashboard, mutation, and documentation tests.

The execution scope is a maximum allowlist, not an instruction to change every path. Unnecessary files shall remain unchanged and the evidence shall record the actual changed-path subset.

## Required verification

- Execute every case and manual review in `VER-REB-009`.
- Run parser/help/schema tests for all five roles and every invalid cross-role option class.
- Run runtime/target identity, candidate substitution, import isolation, predecessor-view tamper, archive/path/environment/privacy, deterministic replay, interruption/output, cleanup, and no-change cases.
- Prove repository workflows and candidate template use the intended roles and fail under raw-command/wrong-environment mutations.
- Prove the sole public-0.6.0 bootstrap lane rejects every version, digest, entry point, command, schema, contract, or artifact-label substitution and cannot survive the typed-verifier availability trigger.
- Prove source, sdist, wheel, installed CLI/help/resources, and compatibility alias parity.
- Run focused tests, the complete supported suite, graph validation, released-root doctor where authoritative, distribution, portable-surface, managed/template parity, whitespace, and diff checks.
- Run exact-candidate source/package and unprivileged Windows/Linux hosted lanes only after a separately authorized candidate commit and hosted dispatch.
- Independently prove root managed bytes, lock/configuration, history, refs, credentials, public distributions, maintenance state, and external services unchanged.

## Evidence to record

Retain the approved packet/preflight and this status-preserving bootstrap amendment; base and exact candidate identities when authorized; changed-path manifest; command/role/independence table; CLI help/parser matrix; result schema/goldens; evaluator/target and hostile-case matrices; workflow before/after and mutation results; import/process traces; predecessor adapter/view bindings; exact-public-0.6.0 bootstrap identity, legacy schema, and removal trigger; source/package/install parity; root/template hashes; focused/full/platform outputs; deterministic result hashes; no-change snapshots; hosted run identities when authorized; and the complete actions-not-performed statement.

## Stop and escalate conditions

- Any operation needs a sixth role, free-form evaluator/script selector, different independence claim, weaker identity, or candidate/predecessor shared interpreter.
- The predecessor view must change, omit another path, accept a diagnostic, or duplicate production policy.
- A workflow can pass only by retaining a raw validator as release evidence, importing checkout code into an independent runtime, using credentials/network inside qualification, or editing root managed bytes.
- Candidate-controlled output can affect an independent pass without independent corroboration.
- Another file, lifecycle policy change, historical mutation, public version/distribution change, or external action is required.
- Complete validation, exact role checks, package parity, deterministic replay, no-change proof, or Windows/Linux agreement cannot be established.

Retain the exact failure and request a bounded amendment; do not absorb another RCA issue or create a bypass.

## Completion report format

Report the five command contracts and independence classes; actual changed paths; evaluator/target and hostile-case results; workflow before/after map; alias and predecessor-adapter status; source/package/platform/full-suite results; root/template/history/external no-change proofs; evidence path; candidate/VREC state; residual risks; actions not performed; and one next accountable decision.
