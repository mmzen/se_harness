+++
id = "REQ-AEX-004"
type = "requirement"
title = "Retain attributable execution receipts"
status = "approved"
owners = ["product-owner", "requirements-steward", "assurance-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a governed autonomous stage completes or stops, THE SYSTEM SHALL produce a deterministic execution receipt that binds the selected scope, autonomy envelope when applicable, execution profiles, skill identities and digests, normalized commands and results, changed paths, retained evidence, subagent contributions, final validation, and repository identity; and SHALL represent the receipt as non-authoritative evidence that cannot approve, verify, release, or expand scope."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Retain attributable execution receipts

## Rationale

Delegated execution reduces direct supervision, so reviewers need a durable and
bounded account of what ran, what changed, which procedure was used, and which
evidence supports the next decision. Agent summaries and conversation history
are not stable enough to serve this purpose.

## Preconditions and trigger

A governed autonomous stage reaches completion, an
`accountable-decision-required` decision, a failed gate, a bounded retry limit,
or another declared stop condition.

## Required response

- Identify the repository, selected artifact, before and after state, and
  envelope identity when mutation was delegated.
- Record execution profiles separately from accountable actors.
- Bind every invoked skill by stable name, version, and content digest.
- Record normalized command arguments, exit status, and output digest or
  retained output path without exposing secrets.
- Record changed paths, evidence paths and digests, and each subagent's bounded
  contribution.
- Record final harness validation, evaluator identity observation, and any
  deviations or residual uncertainty.
- Emit stable ordering and canonical encoding for identical semantic input.

## Failure and boundary behavior

- A receipt cannot claim that a human decision occurred unless the corresponding
  formal lifecycle evidence records it through the managed process.
- Missing or inconsistent required receipt data fails the stage handoff rather
  than producing a successful but incomplete receipt.
- Secret-bearing output, environment variables, credentials, private tokens,
  and unnecessary evidence bodies are omitted or referenced through approved
  retained paths.
- Failed or interrupted workers remain visible and cannot be silently dropped
  from an aggregate receipt.

## Constraints

- Conversation transcripts and hidden reasoning are not required evidence.
- Runtime and model observations support diagnosis and reproducibility but are
  not product authority.
- Receipt retention and privacy rules must be explicit and bounded by
  repository policy.
- Evidence digests bind bytes; they do not establish that the evidence is
  persuasive or the implementation is correct.

## Acceptance examples

### Example: read-only orientation

**Given** the `harness-orient` skill reads a repository and emits a current-state
summary

**When** the stage completes

**Then** the receipt records the skill digest, read-only commands, repository
identity, and no changed paths without claiming an accountable decision.

### Example: partial subagent failure

**Given** three review workers and one failed worker

**When** the orchestrator aggregates results

**Then** the receipt records all three outcomes, marks coverage incomplete, and
prevents a complete-success claim unless the governing procedure permits and
explains that degraded result.

## Open decisions

Before approval, the specification must decide which receipt fields are retained
in-repository, which may remain ephemeral observations, and how receipt schema
evolution preserves existing evidence digests.
