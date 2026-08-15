+++
id = "REQ-SHB-009"
type = "requirement"
title = "Reconcile published governor controls safely"
status = "approved"
owners = ["requirements-steward", "repository-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN an authorized self-hosting change selects a different published governor or adopts its control schema, THE SYSTEM SHALL plan and transactionally reconcile the governor descriptor, repository policy, role-correct GitHub workflow, and integrity lock from immutable release inputs while preserving repository-owned policy and requiring explicit decisions for authority-bearing changes."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Reconcile published governor controls safely

## Rationale

Normal upgrade must not overwrite the implementation repository's self-hosting controls, but permanent protection alone would leave schema evolution, workflow evolution, and governor promotion as an undocumented manual process. Reconciliation therefore needs a separate, explicit operation whose target is an already published immutable release. The operation must distinguish mechanical schema evolution from repository policy and accountable authority changes.

## Preconditions and trigger

- An approved or in-progress work order explicitly authorizes the target published governor release and the intended reconciliation scope.
- The command executes from the currently selected, checksum-verified released governor outside the implementation checkout.
- The target release is identified by exact version, release commit, artifact identity, and SHA-256; candidate source, a locally built wheel, or a mutable tag is insufficient.
- The current governor descriptor and both protected controls match their accepted integrity state before reconciliation begins.

## Required response

- Provide `harnessctl reconcile-governor` as a plan-first operation; require `--apply` for writes.
- Treat `.self-hosting/governor.toml`, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and the corresponding lock metadata as one bounded reconciliation set. The protected set used by normal upgrade remains exactly the latter two managed files.
- Read target schemas, migration declarations, configuration defaults, and workflow material as verified release data without importing or executing target candidate code.
- Migrate TOML structurally by declared field ownership: preserve repository policy and identity, update release-managed fields, and add only properties with defined safe defaults automatically.
- Stop for an explicit governed value when a new or changed property expresses policy, permissions, authority, secrets, environments, triggers, or another decision without a safe default.
- Select the self-hosting workflow variant, never the consumer workflow. Replace release-managed workflow mechanics from the target release rather than applying a generic YAML merge.
- Preserve repository-specific workflow choices only through documented inputs or extension points. An unrecognized local workflow delta is a conflict requiring explicit resolution.
- Validate descriptor, configuration, workflow pins, three-plane separation, permissions, dependencies, runtime isolation, and lock agreement before committing any write.
- Apply the complete reconciled set transactionally and update integrity evidence only for the bytes actually written.

## Failure and boundary behavior

- Unknown migration protocol, unsupported schema jump, missing immutable release identity, checksum mismatch, mutable reference, target-code execution requirement, ambiguous field ownership, unsafe default, workflow-role mismatch, unrecognized YAML customization, or incomplete authority decision blocks all writes.
- If the current released governor cannot interpret the target data-only migration contract, use a separately published compatible bridge release; never execute the target as its own migration authority.
- A successful command performs mechanics authorized by the selected work order. It does not approve the work order, verify a VREC, release or publish software, or silently promote a governor without the separate accountable decision required by the self-hosting model.
- Failure or interruption preserves or recoverably restores the prior descriptor, protected controls, and lock without a mixed-governor state.

## Constraints

- Schema evolution may be automatic only where the target release declares a deterministic safe migration.
- Policy evolution is always explicit and remains repository-owned.
- Workflow mechanics should be release-managed and minimal; repository-specific checks belong in documented inputs, extension points, or separate workflows where practical.
- The public consumer installation and normal consumer upgrade behavior remain unchanged.
- Promotion of the runner implemented by this work remains subject to publication and a later, separately authorized governor reconciliation.

## Acceptance examples

### Example: safe configuration schema addition

**Given** the current accepted policy sets `require_clean_worktree = false`, and the target published schema adds a release-managed property with a safe default,

**When** reconciliation is planned and applied,

**Then** the existing repository policy is preserved, the new property is added with its declared default, the schema version advances, and all related integrity evidence agrees.

### Example: new authority-bearing workflow input

**Given** the target workflow requires a new permission or deployment environment with no safe repository-independent value,

**When** reconciliation is planned without an explicit governed decision,

**Then** the plan reports `decision-required` or an equivalent blocking disposition and writes nothing.

### Example: wrong workflow role

**Given** target release material contains both consumer and self-hosting workflow variants,

**When** reconciliation targets the implementation repository,

**Then** selection of the consumer variant fails before any file or lock change.

## Open decisions

Exact internal migration-manifest fields, stable diagnostic codes, recovery-journal representation, and documented workflow extension syntax remain delegated to the specification and implementation. The immutable-target, current-governor execution, field-ownership, role-selection, and fail-closed boundaries are not delegated.
