+++
id = "ARCH-REB-003"
type = "architecture"
title = "Versioned Git policy for exact evaluator evidence"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
addresses = ["REQ-REB-009", "REQ-REB-010"]
conforms_to = ["SPEC-REB-004"]

[decision_assessment]
outcome = "adr_required"
triggers = ["security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction chooses where canonical byte identity is enforced and how a failed one-shot bootstrap becomes terminal history across Git, candidate source, installed templates, validators, and release authority; those cross-cutting trust decisions have materially different alternatives and release consequences."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "technical-owner"
+++

# Architecture: Versioned Git policy for exact evaluator evidence

## Context and scope

Evaluator evidence is a security-sensitive exact-byte object referenced from formal release metadata. Git checkout is an intervening serialization boundary: without a versioned attribute, Windows may change LF to CRLF after the digest has been committed. A second boundary exists between active and terminal bootstrap authority: rejected history must remain valid without keeping its contract approved. This architecture places line-ending preservation at the repository-content boundary and models a closed rejected RLS/contract pair while leaving exact evidence semantics intact.

## Components and responsibilities

- Candidate-root Git policy declares the narrow evidence-JSON LF rule used by the release repository.
- Canonical standard-template policy delivers the same rule to future installations.
- Installer/package parity ensures the template policy is shipped without changing the current released root.
- Bootstrap binder continues producing canonical JSON and exact hashes.
- Candidate validator continues enforcing raw-byte digest and canonical form.
- Candidate validator distinguishes active `ready + approved` bootstrap authority from terminal `rejected + rejected` history.
- Binder and publication resolver accept only the active approved form.
- Checkout-matrix tests prove the policy at the Git boundary.

## Dependency direction

```text
approved requirement/specification
  -> versioned Git attribute
  -> checkout bytes
  -> exact evidence digest validation
  -> accountable release review
```

Local Git configuration is subordinate to the versioned rule and never becomes authority.

## Data and control flow

The binder writes LF JSON. Git stores normalized LF blob bytes. On checkout, `eol=lf` reproduces those bytes under every supported configuration. Validators hash the worktree file and compare it to the RLS digest before parsing canonical JSON.

## Trust boundaries

- Git configuration and global attributes are untrusted environment input.
- Repository `.gitattributes` is trusted only through reviewed candidate history and exact commit identity.
- Evidence remains untrusted until path, bytes, digest, schema, and evaluator identity pass.
- Released evaluator authority and candidate implementation remain separate.

## Required patterns

- Narrow explicit `text eol=lf` rule for governed evidence JSON.
- Candidate/template byte parity.
- Fresh-clone tests with isolated Git configuration.
- Retention of failing C2/RLS evidence without mutation.
- Exact terminal-pair validation with no operational reuse.

## Prohibited patterns

- Global `* text eol=lf` changes in this correction.
- Validator normalization presented as raw-byte proof.
- `.git/info/attributes` or operator configuration as release evidence.
- Amending C2, `VREC-SEH-009`, or `RLS-SEH-009`.
- Treating a rejected contract as preparation, binding, publication, or release authority.

## Quality attributes

- Portability: identical evidence bytes on supported platforms.
- Integrity: raw SHA-256 remains authoritative.
- Auditability: policy and evidence are versioned.
- Compatibility: no pre-publication root-evaluator upgrade.
- Fail safety: any mismatch blocks promotion.

## Conformance checks

Execute `VER-REB-003`, including Git configuration matrices, terminal-pair state matrices, candidate/template parity, installation/package surface, raw-byte tamper cases, both validator planes, binder/publication authority negatives, reproducible distributions, and hosted qualification for the successor candidate.

## Related ADRs

Draft `ADR-REB-003` selects versioned LF enforcement over validator normalization, local configuration, or abandoning exact-byte evidence.
