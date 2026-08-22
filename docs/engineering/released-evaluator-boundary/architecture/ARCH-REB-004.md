+++
id = "ARCH-REB-004"
type = "architecture"
title = "Contract-bound predecessor preparation compatibility boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
addresses = ["REQ-REB-011", "REQ-REB-012"]
conforms_to = ["SPEC-REB-005"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction adds a narrowly mediated view between an immutable predecessor evaluator and a newer repository graph, changes release-version cardinality, and must preserve fail-closed provenance across Git, validation, binding, and publication boundaries."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "technical-owner"
+++

# Architecture: Contract-bound predecessor preparation compatibility boundary

## Context and scope

Released evaluator 0.5.0 is intentionally immutable and cannot parse rejected release records. Candidate C3 parses them but treats all records, including rejected history, as active version claims. This architecture introduces one repository-owned compatibility boundary without promoting candidate code to root authority or rewriting historical artifacts.

## Components and responsibilities

- **Complete-graph candidate validator:** validates rejected history, active-version cardinality, bootstrap contracts, evidence, and final repository state.
- **Preparation-view adapter:** derives an exact two-artifact omission, creates an isolated exact-commit sparse worktree, invokes predecessor preparation, proves output, and imports only the proposal and view evidence.
- **Released evaluator 0.5.0:** generates predecessor-format RLS bytes and validates every materialized artifact it understands.
- **Bootstrap binder:** independently proves old lock/evaluator/public-wheel identity and binds canonical evaluator evidence.
- **Git:** provides commit, tree, blob, sparse-worktree, and clean-state identities.
- **Accountable owners:** retain all lifecycle and external-action decisions.

## Dependency direction

```text
approved corrective contract
  -> complete candidate validation
  -> derived compatibility view
  -> external released-0.5 preparation
  -> adapter proof/import
  -> independent bootstrap binding
  -> complete candidate validation
  -> accountable RLS review
```

The predecessor never imports candidate modules. The adapter never supplies release authority. The binder never creates the predecessor-owned RLS.

## Data and control flow

The adapter resolves the exact governance commit and validates the full graph. It derives the rejected pair through typed relations, records their Git and raw-byte identities, establishes an isolated sparse worktree at the same commit, and executes exact 0.5.0 preparation. It validates the generated RLS, exclusive-creates the RLS and canonical view sidecar in the complete worktree, then hands off to the existing binder. Final validation reads the complete graph, including untouched rejected history.

## Trust boundaries

- Candidate code is trusted only as exact reviewed candidate source, not as released root evaluator.
- The sparse view is untrusted until its Git source, patterns, materialized file set, and omissions match the closed contract.
- Predecessor output is untrusted until exact semantic and byte checks pass.
- Git configuration, paths, environment, executable resolution, JSON, hashes, and repository content are untrusted.
- Human approvals are external to every automated observation.

## Required patterns

- Derive omissions from one validated closed rejected pair.
- Preserve exact source commit and historical blob/raw identities.
- Use isolated external evaluator execution and canonical closed evidence.
- Exclusive-create/atomic-replace only newly authorized outputs with digest-bound rollback.
- Count active release versions by lifecycle authority, never by record existence alone.
- Validate complete state before and after the compatibility operation.

## Prohibited patterns

- Candidate `prepare-release` against the operational schema-2 root.
- Root evaluator upgrade, lock synthesis, historical relocation, deletion, renumbering, or content rewrite.
- User-supplied arbitrary sparse patterns or generic validation-error suppression.
- Claiming the predecessor validated artifacts absent from its view.
- Multiple ready/released records for the same version.

## Quality attributes

- Integrity: every omission and output is hash-bound.
- Auditability: the exact view and command are retained as canonical evidence.
- Compatibility: released 0.5.0 remains unchanged and remains the RLS generator.
- Fail safety: ambiguity or drift produces zero durable write.
- Portability: default Windows and LF checkouts produce identical canonical evidence.

## Conformance checks

Execute `VER-REB-004`, including active-version and rejected-history matrices, sparse-view derivation, arbitrary-omission negatives, runtime isolation, atomicity/rollback, TOCTOU cases, dual-checkout hashes, full regression, reproducible C4 distributions, released/candidate identities, and hosted qualification.

## Related ADRs

`ADR-REB-004` records the decision to use an exact-commit sparse compatibility view rather than upgrading the root, rewriting history, changing the version, or synthesizing the RLS.
