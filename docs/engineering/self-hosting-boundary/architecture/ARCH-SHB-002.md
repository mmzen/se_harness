+++
id = "ARCH-SHB-002"
type = "architecture"
title = "Protected control plane, governor reconciler, and released acceptance runner"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
addresses = ["REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
conforms_to = ["SPEC-SHB-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "material-alternatives"]
rationale = "Protecting and reconciling repository-specific controls changes installer ownership, schema migration, workflow generation, promotion, and failure semantics, while a verifier-owned runner changes the trust direction between released governor and candidate; these have material alternatives and cross-cutting CI, CLI, lock, and security consequences."
assessed_by = "technical-owner"
+++

# Architecture: Protected control plane, governor reconciler, and released acceptance runner

## Context and scope

The self-hosting model correctly distinguishes governor, candidate source, and candidate package, but normal upgrade still interprets the two repository-specific controls as replaceable consumer-managed files. Permanent protection alone would also leave configuration-schema evolution, workflow evolution, and governor promotion as an undocumented manual process. Separately, candidate-owned tests are extensive but do not provide a replayable verifier-owned functional contract. This architecture closes those gaps without adding a consumer profile or letting an unreleased candidate become authority.

## Components and responsibilities

- **Self-hosting policy:** dependency-light classification, exact protected paths, and bounded diagnostics shared by installer, doctor, preflight, reconciliation, and tests.
- **Standard upgrade planner:** renders consumer desired state, delegates protected paths to the policy, and preserves existing transactional behavior for all ordinary paths.
- **Governor reconciler:** running from the current released governor, resolves an immutable published target, parses its data-only migration contract, plans repository-policy-preserving TOML migration, selects its self-hosting workflow material, and coordinates a recoverable control transaction.
- **Field-ownership schema:** classifies configuration fields as release-managed, repository identity, or repository policy and declares compatible transformations, safe defaults, decision requirements, and extension namespaces.
- **Role-specific workflow contract:** keeps release-managed mechanics reproducible, exposes documented repository inputs or extension points, and prevents consumer/self-hosting substitution or generic YAML merging.
- **Control transaction:** stages and validates the governor descriptor, protected configuration, role-correct workflow, and lock before bounded replacement or recovery.
- **Governor descriptor validator:** proves the selected published governor identity and agreement with workflow constants.
- **Released acceptance runner:** verifier-owned black-box scenarios and canonical evidence serialization.
- **Candidate-source adapter:** invokes source tests with explicit checkout identity and labels results as candidate evidence.
- **Candidate-package adapter:** creates a fresh environment, installs the exact candidate wheel, invokes only installed behavior, and supplies disposable targets.
- **Evidence manifest:** deterministic role, input, scenario, outcome, and hash record retained for human assurance review.

## Dependency direction

```text
self_hosting_policy  <--- installer / doctor / preflight / reconciler
        |
        +-----------> exact protected-path and classification decisions

current released governor ---> governor reconciler ---> verified target release data
                                  |             |
                                  v             v
                         field-owned TOML   self-hosting workflow
                                  \             /
                                   control transaction
                                           |
                                           v
                              descriptor + controls + lock

published governor ---> released acceptance runner ---> candidate-package adapter
                                                          |
candidate commit ---> candidate-source adapter             v
        |                                             disposable targets
        +---------> exact candidate wheel -----------------+

candidate evidence -------------------------------> accountable human review
released-governor assessment ---------------------> accountable human review
```

The policy depends only on the standard library and low-level data contracts, avoiding an installer/self-hosting circular import. The current governor interprets a stable data-only migration protocol and never imports target release code; an unsupported protocol requires a bridge release. The released runner never imports candidate source. Candidate adapters cannot modify governor state or formal decisions.

## Data and control flow

### Normal upgrade

1. Parse target configuration and lock without writing.
2. Classify the target before rendering actions for protected paths.
3. For consumers, use existing managed upgrade semantics.
4. For valid self-hosting, verify protected current content against the current root lock and emit `protected`.
5. Validate all remaining actions and block on any ambiguity or customization.
6. Apply eligible ordinary changes transactionally while preserving protected bytes and equivalent digests.

### Explicit governor reconciliation

1. Execute the currently selected released governor outside the checkout, select the approved/in-progress work order, and run start preflight.
2. Resolve the requested target version to an immutable published release commit, artifact digest, data-only migration contract, and self-hosting workflow material.
3. Verify current descriptor and control integrity, target identity, migration-protocol compatibility, and every non-protected managed entry.
4. Structurally migrate TOML: update release-managed fields, preserve repository identity and policy, add safe defaults, and stop for explicit decisions or ambiguous ownership.
5. Replace release-managed workflow mechanics with the target self-hosting variant. Preserve only documented inputs or extension points and stop on unrecognized YAML deltas or authority-bearing changes without explicit decisions.
6. Validate governor constants, immutable pins, permissions, three non-substitutable CI roles, dependency order, isolation assertions, and the exact complete write set.
7. Present descriptor, per-field, workflow, and lock dispositions in a read-only plan.
8. On explicit apply, use a recoverable transaction so the descriptor, configuration, workflow, and lock reach one target state or restore the prior state.

### Functional acceptance

1. Resolve released-governor and verifier identities outside the checkout.
2. Bind candidate source to a full commit and candidate package to a wheel digest.
3. Run source evidence separately.
4. Create a fresh candidate environment and run verifier-owned black-box scenarios through installed entry points.
5. Normalize canonical outputs, fail on missing scenarios or identity ambiguity, and serialize the replay manifest.
6. Retain candidate and governor outputs as distinct evidence inputs for human verification.

## Trust boundaries

- Repository configuration cannot enlarge the protected set or self-declare a valid implementation identity incompletely.
- The root lock is integrity evidence, not permission to replace self-hosting content with a consumer template.
- The reconciler executes only from the selected released governor, consumes target release data without executing target code, and changes controls only after explicit work-order selection and complete structural validation; it grants no governance status by itself.
- Repository policy, identity, triggers, permissions, secrets, environments, and deployment authority cannot be inferred from a target template or safe-looking default.
- The consumer workflow and self-hosting workflow are distinct roles. Neither filename similarity nor template availability permits substitution.
- Candidate source, package, archive, test output, paths, and environment are untrusted.
- The released runner is independently immutable only after publication and separate governor promotion.
- Human owners retain work authorization, VREC verification, release, publication, and governor-promotion decisions.

## Required patterns

- One shared protected-path constant and classification result.
- Tri-state fail-closed classification.
- Plan before apply and validate the complete write set.
- Versioned data-only migration protocols with explicit field ownership.
- Release-managed workflow mechanics with documented inputs or extension points.
- Recoverable multi-control replacement and byte preservation on failure.
- Component-aware path containment and installed-entry-point checks.
- Canonical evidence separated from non-canonical timing and temporary-path observations.
- Two-release activation for new governor semantics.

## Prohibited patterns

- Importing `self_hosting.py` from `installer.py` through a circular dependency.
- Treating a current lock match as permission to overwrite protected content with consumer desired bytes.
- Silently calling protected content `unchanged` when consumer divergence exists.
- Generic YAML merging, consumer/self-hosting workflow substitution, or preservation of undocumented workflow deltas.
- Silent selection of repository policy, permissions, triggers, secrets, environments, or deployment authority.
- Importing or executing the target release to migrate the controls that would select it.
- Recomputing protected digests in normal upgrade after a mismatch.
- Running the candidate's own test code as the sole independent package acceptance contract.
- Activating a candidate verifier as governor in the implementation or publication commit.

## Quality attributes

Fail-closed integrity, explicit authority provenance, transactional reliability, deterministic replay, import isolation, consumer compatibility, narrow repository specificity, auditability, and standard-library portability.

## Conformance checks

- Static dependency checks prove the shared policy has no installer or CLI dependency.
- Planner fixtures cover consumer, valid self-hosting, ambiguous identity, missing control, schema variants, customization, and mixed ordinary/protected changes.
- Transaction snapshots prove failure atomicity and protected byte preservation.
- Reconciliation fixtures prove exact target publication, current-governor execution, protocol compatibility, TOML field ownership, safe-default and decision-required behavior, role-correct workflow replacement, permission review, exact write scope, recovery, and descriptor/workflow agreement.
- Acceptance fixtures prove source/package/governor origins, required scenarios, canonical replay, negative authority paths, and staged activation.
- Package and GitHub workflow tests prove the released runner can assess a candidate wheel outside the checkout.

## Related ADRs

`ADR-SHB-002` selects protected normal upgrade plus released-governor-driven, data-only reconciliation and a released verifier-owned black-box contract over consumer-template replacement, owner-seed conversion, manual or generic merges, target-code migration, or candidate-only testing.
