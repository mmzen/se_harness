+++
id = "ARCH-REB-011"
type = "architecture"
title = "Evaluator identity from the installed payload; the upgrade as an ordinary transaction"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
addresses = ["REQ-REB-027", "REQ-REB-028"]
conforms_to = ["SPEC-REB-012"]

[decision_assessment]
outcome = "adr_required"
triggers = ["security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse"]
rationale = "Removing the work-order packet and the archive-digest requirement changes what the trust boundary accepts as the target evaluator's identity and retires a cross-cutting gate that every upgrade and the managed workflow depended on."
assessed_by = "technical-owner"
+++

# Architecture: Evaluator identity from the installed payload; the upgrade as an ordinary transaction

## Components and responsibilities

- **`evaluator_identity`**: reports version, installed-payload digest, and
  the archive identity when PEP 610 recorded one; absence is a fact, not a
  failure.
- **`mutation_guard`**: proves the released evaluator's identity and
  isolation before any root write; for an upgrade it accepts the installed
  evaluator as the target on version and payload.
- **`installer`**: plans and applies the managed set and the lock atomically;
  writes transition evidence on request.
- **`release_qualification.released-root`** and the managed workflow
  template: qualify an index-installed root evaluator.
- **Repository-owned candidate-evidence lane**: selects the acceptance
  operation by the verifier's capability.

Retired: `upgrade_authorization` (the `[evaluator_upgrade]` packet loader).

## Control flow

install evaluator (any means) → `identity` → `upgrade` plan → review →
`upgrade --apply` (guard, atomic write, lock, optional evidence) → `doctor`,
`validate` → the repository's own work order records the change.

## Trust boundaries

The evaluator still runs from outside the checkout with `-I` and never
imports from the repository (`RID018` unchanged). What changes is the
identity the boundary accepts: version plus installed-payload digest, with
the archive digest as corroboration when present rather than as a
precondition.

## Prohibited patterns

Re-introducing a required declaration table for upgrades; treating a missing
`direct_url.json` as tampering; applying from candidate source.

## Decision assessment

`ADR-REB-011` records the decision and the alternatives.
