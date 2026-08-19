+++
id = "WO-RLO-002"
type = "work_order"
title = "Decouple repository distribution policy from portable harnessctl"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[assurance]
commit_bound_verification = "required"
rationale = "Future consumer upgrades and SE Harness releases will rely on changed packaged CLI behavior, managed validation policy, trusted workflow imports, atomic distribution binding, and credential-bound release decisions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-RLO-009", "REQ-RLO-010", "REQ-RLO-011"]
specifications = ["SPEC-RLO-002"]
verification = ["VER-RLO-002"]
architecture = ["ARCH-RLO-002", "ADR-RLO-002"]
+++

# Work Order: Decouple repository distribution policy from portable harnessctl

## Lifecycle

On 2026-08-18 the accountable repository owner approved the correction plan and authorized creation of this artifact packet. The linked capability, requirements, specification, architecture, ADR, and verification contract are approved definitions. `WO-RLO-002` intentionally remains `draft`: no implementation, managed-file mutation, commit, push, PR, VREC, release, tag, publication, deployment, or external configuration change is authorized by that statement.

On 2026-08-18 the accountable repository owner then stated `ok go implement`. This separately approved the bounded work order and authorized its transition to `in_progress`. It authorizes only the scope below and does not authorize a commit, push, PR, VREC, release, tag, publication, deployment, environment approval, or governor promotion.

Completed bounded work transitions only to `implemented`; because commit-bound assurance is required, future release or operational reliance requires a separate clean candidate, ready VREC, accountable assurance decision, and governance commit.

On 2026-08-18 the bounded implementation and local evidence completed successfully, so this work order transitioned to `implemented`. The retained evidence is `docs/engineering/release-orchestration/evidence/WO-RLO-002-verification.md`. No commit-bound assurance, VREC, release decision, commit, push, PR, tag, publication, deployment, environment approval, external configuration change, or governor promotion is implied.

## Objective

Restore the intended product boundary by keeping portable SE Harness release preparation format-neutral while retaining exact repository-owned distribution provenance and the deterministic one-input SE Harness publication workflow.

## In scope

- Remove the unreleased `prepare-release --distribution-manifest` input and corresponding portable provenance code.
- Remove the Python-specific distribution module from the packaged `se_harness*` namespace.
- Remove `python-wheel-sdist`, SE Harness filenames, checksum-layout rules, and publication guidance from the managed validator and standard release-record template.
- Preserve generic RLS preparation, validation, path safety, aggregate coverage, and lifecycle authority behavior.
- Relocate the existing bundle/distribution schema implementation to one repository-owned, non-packaged module shared by creation, binding, policy validation, workflow resolution, and tests.
- Add an explicit atomic repository binder that operates only on one ready RLS and one exact bundle manifest.
- Add a separate repository policy check for distribution-bearing SE Harness RLS files and include it in local/hosted required verification.
- Update the one-input release resolver to use trusted-main repository tooling while preserving every current security, deterministic-build, replay, PyPI, Pages, and observation invariant.
- Reconcile managed templates and `.engineering-harness.lock` transactionally.
- Update repository-specific and consumer documentation to state the boundary and revised two-step preparation process.
- Add acceptance, boundary, compatibility, failure, and package-content tests and retain work-order-keyed evidence.

## Out of scope

- Changing generic RLS lifecycle, relations, eligible VREC/work coverage, release authority, tag semantics, or accountable decision rights.
- Creating a plugin system, generic payload framework, second installation profile, or support for other package ecosystems and publication channels.
- Changing the top-level PyPI workflow filename, publisher registration, protected environments, action identities, permissions, or normal one-input operator interface.
- Weakening exact bundle identity, deterministic reconstruction, candidate/credential separation, immutable external-state rules, Pages recovery, or stage-specific results.
- Preparing or transitioning a product release, creating or moving a tag, publishing GitHub/PyPI assets, deploying Pages, approving an environment, or promoting a governor.
- Rewriting `SPEC-RLO-001`, `VREC-RLO-001`, historical RLS files, tags, releases, evidence, or workflow history.

## Authorized decision envelope

After separate work-order approval, the implementation agent may choose repository helper filenames, safe atomic-write mechanics, bounded output wording, internal function decomposition, and test fixture organization.

The agent may not retain an alias for the removed portable flag, introduce a generic extension API, change the schema-1 repository distribution fields, change core RLS semantics, alter the one-input publication contract or trust boundaries, or treat repository validation as formal lifecycle authority.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and exactly one consumer installation.
- Treat target paths, TOML/JSON, duplicate keys, Git output, manifests, filenames, archives, workflow data, and external responses as untrusted.
- Keep repository distribution code out of the built wheel and managed consumer template.
- Keep the released governor isolated from candidate source and candidate packages.
- Preserve unrelated user changes and all historical artifact facts.
- Perform no promotable build or production external mutation under this work order.
- Fail closed if the correction would require candidate code in a privileged job, a stored credential, publisher/environment migration, weakened managed-upgrade safety, or a historical rewrite.

## Expected change surface

- Portable CLI and release-provenance preparation.
- Packaged module inventory and build tests.
- Root and canonical managed validators and release-record templates.
- Repository distribution manifest generation, binding, policy validation, and release resolver helpers.
- One-input release workflow only where imports or explicit policy gates change.
- Installer/upgrade integrity lock and disposable consumer fixtures.
- Revision-provenance and release-orchestration tests, acceptance scenarios, repository context, command/development notes, and domain index.

## Required verification

- Start and review preflight for `WO-RLO-002` after it is approved.
- Formal graph validation with zero new structure, governance, or policy findings; baseline maintenance observations remain separately classified.
- Doctor, managed-file integrity, and root/template byte-equivalence checks.
- Every method and invariant in `VER-RLO-002`, plus regression of `VER-RLO-001`, `VER-PYP-001`, and `VER-DPG-001` where workflow behavior is preserved.
- Built-wheel inspection and disposable init/adopt/upgrade evidence proving absence of repository release semantics.
- Exact, replay, malformed, mismatch, conflict, and injected-write-failure binder tests with before/after file hashes.
- Strict workflow YAML parsing and static permission/input/import/action-pin/checkout checks.
- Complete repository-default and Python 3.11 unit suites, CLI help, `git diff --check`, released-governor candidate-source assessment, and candidate-package acceptance.
- Hosted PR checks without production publication, deployment, tag, release, or environment approval.

## Evidence to record

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-002-verification.md` with the approved boundary, exact changed surfaces, command results and counts, candidate/governor/package origins, wheel and consumer-install inventories, CLI/template before-and-after observations, binder/state matrices and unchanged-file hashes, workflow security comparison, documentation updates, warnings, deviations, residual risks, and every unperformed governance or production action.

## Stop and escalate conditions

Stop for an invalid graph, managed drift, unclear ownership of a managed file, inability to preserve generic RLS behavior, need for a public compatibility layer, any existing distribution-bearing released RLS, duplicate repository schema implementations, non-atomic binding, repository tooling entering the wheel/template, candidate execution in a privileged job, workflow input or external identity changes, failing deterministic/replay/security tests, historical mutation, or production action needed as implementation evidence.

## Completion report format

Report implemented requirements; exact portable surfaces removed; repository components added or relocated; generic RLS compatibility; binder atomicity and schema matrix; wheel and disposable consumer observations; workflow input/permission/import comparison; test counts on both Python versions; governor/source/package identities; documentation and lock changes; warnings/deviations/residual risks; evidence path; candidate commit plan; and every commit, push, PR, VREC, release, tag, publication, deployment, environment approval, or governor promotion not performed.
