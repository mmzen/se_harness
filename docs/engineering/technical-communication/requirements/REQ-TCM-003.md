+++
id = "REQ-TCM-003"
type = "requirement"
title = "Apply distinct operator and technical-artifact profiles"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a supported agent authors eligible operator-facing or technical-artifact English prose, THE SYSTEM SHALL select the declared communication profile, apply its bounded clarity principles during drafting rather than as an uncontrolled rewrite pass, and retain the profile and any material deviation in the result or review evidence."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Apply distinct operator and technical-artifact profiles

## Rationale

Operator interaction benefits from direct, action-first language. Formal
artifacts need more nuance and contain normative or structured sections that
must not be simplified. One formatter would be too weak for operator guidance
or too aggressive for technical artifacts.

## Preconditions and trigger

- The agent is authoring new or materially revised eligible English prose.
- The purpose is known as operator communication or technical-artifact prose.
- Protected content is identified before the policy is applied.

## Required response

- Use `operator-communication` for operator explanations. Lead with the outcome
  or required action, identify the accountable actor, keep one principal action
  per sentence, use consistent terms, and state limits directly.
- Use `technical-artifact-writing` for human-readable artifact prose. Prefer
  explicit actors, conditions, actions, results, consistent terminology, and
  focused sentences while keeping necessary engineering detail.
- Apply profiles while composing or deliberately revising selected draft prose.
  Do not run an automatic whole-file or repository-wide rewrite.
- Keep code, contracts, evidence, front matter, semantic tables, normative
  statements, and other protected content outside automatic transformation.
- Record the selected profile in a skill result or work-order evidence when a
  governed skill or implementation uses it materially.
- Record a material deviation when a recommendation is intentionally not used
  to preserve meaning. Routine protected spans are not deviations.

## Failure and boundary behavior

- Unknown purpose, unsupported language, or ambiguous profile selection stops
  automatic rendering and preserves the source.
- For non-English prose, ordinary owner instructions may apply, but the agent
  does not claim that the managed profile was applied.
- An operator request for exact output selects exact preservation.
- Existing approved or historical artifacts remain unchanged unless separate
  governed scope authorizes a substantive revision.

## Constraints

- Profiles use selected clarity principles, not a copied controlled dictionary
  or a complete ASD-STE100 rules engine.
- Profiles do not correct operator input or modify direct quotations.
- Repository terminology may be stricter, but cannot weaken exact preservation
  or harness authority.
- Routine use adds no human review step. Human input is requested only for
  meaning, terminology, accountable decisions, or declared exceptions.

## Acceptance examples

### Example: operator asks what happens next

**Given** one structured harness result with one current decision point

**When** the operator profile is applied

**Then** the response states the outcome, one next action, accountable role, and
non-effects without adding another action.

### Example: requirement artifact

**Given** a new draft requirement with rationale, a normative statement, and
acceptance examples

**When** the artifact profile is applied during authoring

**Then** rationale and examples use clear consistent prose while normative force,
identifiers, metadata, and thresholds are preserved.

### Example: style-only migration request

**Given** approved artifacts and no authorized substantive revision

**When** an agent is asked to rewrite them only for profile consistency

**Then** the agent reports that the migration is outside this capability and
changes no artifact.

## Open decisions

Before approval, reviewers must accept the two profile definitions, application
strengths, deviation threshold, and no-mass-rewrite rule.
