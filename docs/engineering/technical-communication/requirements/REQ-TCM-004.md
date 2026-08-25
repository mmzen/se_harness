+++
id = "REQ-TCM-004"
type = "requirement"
title = "Produce an operator brief through an explicit read-only skill"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN an operator explicitly invokes `harness-operator-brief` with one bounded supported source, THE SYSTEM SHALL produce one inline decision-ready English brief and execution receipt under the managed operator-communication profile, preserve protected content, and perform no repository, lifecycle, Git, credential, network, or external mutation."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Produce an operator brief through an explicit read-only skill

## Rationale

A concrete outcome skill proves that the managed policy can be applied through
the portable skill architecture. Explicit activation avoids overlap with
`harness-orient` and current writing skills while triggers and results are
evaluated. Read-only execution keeps the first increment outside work,
assurance, delivery, and external-action authority.

## Preconditions and trigger

- The operator explicitly selects `harness-operator-brief` and one repository.
- One source is supplied as a supported structured harness result or bounded
  technical text with declared protected content.
- The complete skill, managed policy, repository instructions, and exact target
  released evaluator are available.
- The request is an explanation, not an artifact edit, transition,
  implementation, assurance action, Git operation, or external action.

## Required response

- Install one canonical portable core at
  `.agents/skills/harness-operator-brief/` from the standard template source.
- Retain a strict closed contract, complete `SKILL.md`, and deterministic helper
  that checks protected-content preservation without judging hidden reasoning or
  substantive correctness.
- Require explicit activation and declare non-matches for orientation, artifact
  drafting, work execution, assurance preparation, lifecycle decisions, and
  external actions.
- Verify managed integrity and exact released-evaluator identity before claiming
  a policy-governed result.
- Accept one bounded source kind and payload, a protected-content declaration,
  the requested outcome, and optional approved project terms.
- Return one existing structured skill-result and one execution receipt inline;
  retain no target evidence.
- Identify the profile and material deviations without exposing hidden reasoning
  or copying the complete policy.
- Stop at the current accountable decision and preserve canonical blocks exactly.

## Failure and boundary behavior

- Implicit or ambiguous activation is blocked in the first increment.
- Missing policy, failed integrity, wrong evaluator, malformed source,
  overlapping protected spans, preservation mismatch, unsupported language, or
  meaning ambiguity stops before a completed brief is claimed.
- The skill does not repair artifacts, invoke another writing skill, download the
  standard, or search the network for terminology.
- If current harness state is requested without a current structured evaluator
  result, the skill routes to existing orientation rather than inventing state.

## Constraints

- Mutation class is `read-only`; delegation is disabled and the single-agent path
  is complete.
- Skill prose is not product, lifecycle, or communication-policy authority.
- Existing skill contract instances and portable-core digests remain unchanged.
- The skill is not an implicit wrapper around every other skill.
- It cannot claim ASD-STE100 compliance or ASD endorsement.

## Acceptance examples

### Example: explicit structured result

**Given** a current structured harness result with one decision and one verbatim
command block

**When** the operator explicitly invokes `harness-operator-brief`

**Then** the skill returns one clear inline brief, preserves the block, records
the profile, emits a receipt, and changes no repository or external state.

### Example: implicit natural-language match

**Given** a question that could match `harness-orient` or the brief skill

**When** the operator does not select a skill

**Then** `harness-operator-brief` does not activate.

### Example: request includes implementation

**Given** a request to simplify an explanation and edit the repository

**When** the brief skill is selected

**Then** it may explain the boundary but performs no edit and does not reinterpret
the request as work authorization.

## Open decisions

Before approval, technical and assurance owners must accept the closed contract,
supported source kinds, helper boundary, result fields, stop outcomes, and
compatibility behavior in `SPEC-TCM-001` and `VER-TCM-001`.
