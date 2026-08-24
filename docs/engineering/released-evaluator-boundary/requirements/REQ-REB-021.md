+++
id = "REQ-REB-021"
type = "requirement"
title = "Emit provenance-bound release qualification results"
status = "approved"
owners = ["requirements-steward", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a role-specific release qualification operation completes, THE SYSTEM SHALL emit a deterministic result that identifies the operation, evaluator, target, checks, independence boundary, and outcome without overstating authority."
verification_method = "automated-schema-and-replay-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "requirements-steward"
+++

# Requirement: Emit provenance-bound release qualification results

## Rationale

Release 0.6.0 accumulated evidence from multiple interpreters, packages, checkouts, compatibility views, and workflows. Similar-looking pass messages made it difficult to distinguish a released-governor result from a candidate self-check. A durable result must answer: what operation ran, which evaluator bytes ran it, what target bytes were inspected, which checks ran, and whether the result was independent.

## Required response

Every role-specific qualification shall support a canonical machine-readable result and a concise human rendering of the same facts. The machine-readable result shall include:

- schema identifier and schema version;
- qualification operation and fixed independence classification;
- evaluator role, distribution name/version, entry-point identity, and verified digest or declared external identity as applicable;
- target kind and stable target identity, including repository commit, view manifest/hash, archive/payload digest, wheel digest, or installed distribution identity as applicable;
- ordered check identifiers, outcomes, and deterministic diagnostics;
- overall `passed` value and completion status;
- a statement that the result grants no lifecycle or external-action authority.

The result shall be written atomically only after all input identities are bound. A failed or interrupted run shall not leave a passing result. Replaying the same operation over the same immutable inputs shall produce the same decision-bearing fields.

## Failure and boundary behavior

- Missing or unverifiable provenance makes the operation fail; it is not represented as `unknown` on a passing result.
- The result shall distinguish independent released-verifier evidence, external-predecessor evidence, candidate-controlled evidence, and public-install evidence.
- Human output shall not omit a provenance mismatch that appears in JSON, and JSON shall not claim a pass when the process exits non-zero.
- Repository-relative paths may identify governed inputs, but absolute workstation paths, environment secrets, credentials, tokens, and unrelated environment variables shall not appear in retained output.
- A result file is evidence input only. It does not transition an artifact, satisfy an assurance decision by itself, authorize release, or mutate any governed state.

## Constraints

- Canonical JSON is UTF-8, LF-stable, key-stable, and free of wall-clock values in decision-bearing identity fields.
- Diagnostics are deterministic and bounded; untrusted file bodies are not echoed.
- Existing retained evidence can remain historical. Migration does not rewrite released evidence.

## Acceptance examples

### Example: candidate-controlled pass

**Given** the candidate evaluator validates its complete graph successfully

**When** `qualify complete-candidate` emits a result

**Then** the result records the candidate commit and distribution identity and says `independence = "candidate-controlled"` rather than implying independent assurance.

### Example: provenance mismatch

**Given** the expected candidate wheel digest differs from the supplied wheel

**When** qualification starts

**Then** it exits non-zero, identifies the digest check, and does not create a passing retained result.
