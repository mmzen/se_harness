+++
id = "REQ-TCM-002"
type = "requirement"
title = "Preserve protected content and technical meaning"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a supported agent applies the technical-communication policy, THE SYSTEM SHALL preserve exact protected content byte for byte, preserve the meaning and force of semantically protected content, and stop rather than simplify when the applicable boundary is ambiguous."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Preserve protected content and technical meaning

## Rationale

Writing style is a quality constraint, not a source of authority. A simpler
synonym, removed qualifier, reordered condition, or modified token can change
lifecycle meaning, test behavior, evidence identity, or a technical contract.
The preservation boundary must be explicit and fail closed.

## Preconditions and trigger

The agent is preparing or revising eligible prose and the source contains, or
may contain, exact technical spans or semantically normative statements.

## Required response

- Treat commands, code, paths, identifiers, hashes, versions, URLs, schema
  fields, machine data, logs, diagnostics, evaluator output, canonical
  restitution blocks, quotations, and operator text as exact protected content.
- Treat normative obligations, lifecycle and decision meanings, acceptance
  thresholds, safety qualifications, legal text, and established terminology as
  semantically protected content.
- Preserve exact protected content byte for byte, including significant ordering
  and whitespace.
- Do not automatically paraphrase semantically protected content. During first
  drafting, clarify its actor, condition, obligation, and result without changing
  scope, force, or defined terminology.
- Apply harness authority, machine contracts, and accountable artifact decisions
  before communication policy when rules conflict.
- Report one precise deviation or request one accountable clarification when
  meaning and clarity cannot both be preserved.

## Failure and boundary behavior

- Ambiguous boundaries, overlapping spans, malformed structured input, or a
  failed preservation check stops the rendering result.
- The agent does not guess whether an unfamiliar token is replaceable.
- A canonical lifecycle block that forbids surrounding text is returned alone
  and unchanged.
- Preservation failure never permits omission or an apparently clearer substitute.

## Constraints

- Readability metrics and vocabulary flags are advisory evidence only.
- Project-specific nouns and verbs remain valid when defined or supplied by the
  repository; the agent does not invent simpler-looking synonyms.
- Existing approved artifacts are not reopened or rewritten only for style.
- The first increment does not claim automatic semantic equivalence proof.
  Independent human assessment covers representative sensitive cases.

## Acceptance examples

### Example: canonical lifecycle result

**Given** a canonical result that requires verbatim restitution

**When** the agent communicates it

**Then** every byte is unchanged and no preface, conclusion, or second action is
added.

### Example: specification narrative and code

**Given** a draft specification with prose, one JSON example, and defined fields

**When** eligible prose is written under the policy

**Then** the explanation may become clearer while the JSON and field names are
identical to the source.

### Example: ambiguous technical term

**Given** an unfamiliar term whose substitution could change behavior

**When** the profile cannot classify it safely

**Then** the agent preserves the term and requests or records one terminology
decision instead of inventing a synonym.

## Open decisions

Before approval, the product, technical, and assurance owners must accept the
exact-versus-semantic classification and fail-closed ambiguity behavior in
`SPEC-TCM-001` and `VER-TCM-001`.
