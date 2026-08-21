+++
id = "REQ-REB-009"
type = "requirement"
title = "Preserve canonical evaluator evidence through Git checkout"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN canonical evaluator-evidence JSON is retained in Git, THE SYSTEM SHALL preserve its exact LF bytes and bound SHA-256 across supported checkout line-ending configurations without weakening exact-byte validation."
verification_method = "automated-cross-platform-checkout-and-provenance-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Preserve canonical evaluator evidence through Git checkout

## Rationale

The committed ready `RLS-SEH-009` binds canonical evaluator evidence with SHA-256 `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404`. A normal Windows checkout with `core.autocrlf=true` converts its terminal LF to CRLF and produces SHA-256 `7881148c63f6e8e7edf701dff36b2efe5f8c6dd4caebe3e18e2a4bb8f5ebc4d4`. Candidate validation then correctly fails with `E012`, while an LF checkout passes. The content is semantically identical, but the repository failed to preserve the exact canonical bytes that the release record governs.

Normalizing evidence inside the validator would change the approved exact-byte trust contract. Relying on local Git configuration would make correctness depend on unversioned operator state. The repository therefore needs a versioned, candidate-contained checkout policy.

## Preconditions and trigger

- Evaluator evidence is canonical `se-harness-evaluator-evidence-v1` JSON with one terminal LF.
- A VREC or RLS binds its repository-relative path and raw-byte SHA-256.
- Git checks out the repository under any supported `core.autocrlf` or `core.eol` configuration.

## Required response

- Declare a narrowly scoped versioned Git attribute that forces JSON below `docs/engineering/**/evidence/` to checkout with LF.
- Carry the same policy in candidate source and the canonical standard installation so fresh repositories retain portable evidence.
- Preserve raw-byte SHA-256 validation, canonical JSON validation, safe path handling, and all existing evaluator-identity checks.
- Prove fresh checkouts under LF- and CRLF-oriented Git configurations retain the canonical evidence digest and pass candidate validation.

## Failure and boundary behavior

Missing, broadened, conflicting, or ineffective attributes; CRLF evidence bytes; changed JSON content; changed digest; unsafe path; or inconsistent candidate/template policy fails qualification. Local or global Git configuration is never treated as formal authority.

The correction does not rewrite `RLS-SEH-009`, change its evidence digest, reinterpret its failed qualification, repoint C2, or authorize a VREC/RLS transition, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or root-evaluator upgrade.

## Constraints

- Keep exact canonical evidence bytes as the trust object.
- Do not add a general line-ending normalization exception to the validator.
- Do not change `.engineering-harness.toml`, the operational schema-2 lock, or the installed released 0.5.0 evaluator.
- Keep one standard installation and Python 3.11+ standard-library runtime behavior.
- Treat Git attributes, configuration, paths, evidence, and repository bytes as untrusted inputs.

## Acceptance examples

### Example: normal behavior

**Given** a successor candidate contains the approved LF attribute in source and its canonical standard template

**When** the later bound evaluator JSON is committed and checked out with `core.autocrlf=true`, `input`, or `false`

**Then** every worktree contains the exact LF bytes, the recorded digest matches, and released and candidate validation pass.

### Example: failure behavior

**Given** the attribute is absent or a checkout contains CRLF evidence

**When** candidate validation checks the bound raw-byte digest

**Then** it fails closed and the release cannot transition.

## Decision state

The exact-byte LF policy is approved for bounded local implementation under `WO-REB-005`. Candidate commit, hosted qualification, historical release disposition, aggregate verification, release, publication, deployment, maintenance, and root adoption remain separately governed.
