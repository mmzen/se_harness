+++
id = "REQ-REB-004"
type = "requirement"
title = "Keep retired self-hosting surfaces inactive"
status = "approved"
owners = ["requirements-steward", "technical-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN the product package, standard template, root governance, or active repository automation is validated, THE SYSTEM SHALL reject executable special self-hosting profiles, descriptors, workflows, packaged templates, promotion commands, and retired runtime roles while preserving explicitly historical documentation and fixtures."
verification_method = "automated-active-surface-invariant"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Keep retired self-hosting surfaces inactive

## Rationale

The specialized self-hosting lifecycle was the architectural cause of the deadlock. Existing absence tests cover several product paths but do not reject active repository workflows that still consume the retired descriptor and CLI role.

## Preconditions and trigger

Candidate-source CI, candidate-package acceptance, or repository workflow-policy validation inspects the exact candidate tree and built wheel.

## Required response

- Reject active `.self-hosting` descriptors, dedicated self-hosting workflows, role-specific packaged templates, reconciliation or promotion commands, and unsupported `governor` CLI invocations.
- Inspect portable package members and active repository workflows/scripts.
- Permit historical RCA prose, superseded artifacts, and isolated migration fixtures only when they cannot be executed as current policy.
- Report the exact active path and forbidden contract when the invariant fails.

## Failure and boundary behavior

An uncertain classification fails closed for executable or packaged paths and requires accountable disposition. The check does not rewrite, delete, or reinterpret historical evidence.

## Constraints

- The term `governor` is not globally banned from historical text.
- General repository-owned release automation may remain non-portable, but it must use the standard released-evaluator identity contract.
- Absence checks must inspect behavior and entry points rather than only selected filenames.

## Acceptance examples

### Example: normal behavior

**Given** active workflows using `released-evaluator` and historical RCA text describing the former governor

**When** the invariant runs

**Then** active automation passes and historical evidence remains untouched.

### Example: failure behavior

**Given** a workflow step invoking `identity --role governor`

**When** candidate-source policy tests run

**Then** the candidate fails and identifies that workflow line as an active retired contract.

## Open decisions

The implementation must define a narrow historical-fixture allowlist for technical-owner review; a broad text exclusion is not acceptable.
