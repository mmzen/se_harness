+++
id = "REQ-REB-008"
type = "requirement"
title = "Bridge one predecessor-evaluator release-readiness boundary"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-27"
statement = "WHEN an approved product release first activates evaluator-evidence rules that the currently selected predecessor evaluator cannot emit, THE SYSTEM SHALL permit exactly one contract-bound bootstrap release record to retain canonical proof of that predecessor evaluator and SHALL validate and publish it without granting candidate code root-evaluator authority or weakening the ordinary schema-3 rule."
verification_method = "automated-schema-provenance-publication-and-negative-boundary-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "requirements-steward"
+++

# Requirement: Bridge one predecessor-evaluator release-readiness boundary

## Retirement amendment of 2026-08-27

Retired on 2026-08-27 by `REQ-REB-029` under `WO-REB-029`, on the repository owner's direction, which decided this requirement is superseded. The contract-bound bootstrap release record is withdrawn. No release contract carries bootstrap authority, no release record resolves one, and the consumer-installed validator no longer reads a `[bootstrap]` tuple, resolves a bootstrap contract for a release record, or enforces at most one approved bootstrap contract in a repository. The requirement was authored for one event, the 0.6.0 activation of evaluator-evidence rules that the then-selected 0.5.0 evaluator could not emit. That event is closed: `REL-SEH-011` and `RLS-SEH-012` record it, `REQ-REB-011` removed its cause in 0.6.0, and 0.7.0 and 0.7.1 were released with no bootstrap record at all. Everything below records what the release path did while this requirement was active and is retained unchanged as history; it is no longer an obligation. The four closed release contracts keep their `[bootstrap]` tables and the two closed release records keep their `preparation_schema` markers and their hash-bound digests, which still verify; the tuple is deliberately inert data that no rule reads, and its digests are recomputed by `tests/test_predecessor_bootstrap_retirement.py` rather than by a validator rule.

The declared `superseded` status is not applied. `docs/engineering/WORKFLOW.json` admits no `approved` to `superseded` transition for a definition, and this artifact carries its own `draft` to `approved` event, which `WFL-005` requires to stay append-only. Setting the status therefore either contradicts that event (`E014`, measured on 2026-08-27) or deletes it. The retirement is recorded here instead, the instrument `WO-REB-028` already used for `REQ-REB-012`, `REQ-REB-015`, `SPEC-REB-003`, `SPEC-REB-005` and `SPEC-REB-007`. Whether the status is applied through a new transition or the definition family gains one is a separate owner decision; the retirement itself does not wait on it.

## Rationale

Candidate 0.6.0 correctly requires new release records to bind canonical evaluator evidence, but the operational root remains governed by released 0.5.0 and a schema-2 lock. Released 0.5.0 can prepare an authoritative legacy ready RLS but cannot emit the schema-3 evidence binding. Candidate validation therefore rejects the first RLS needed to publish the release that introduces the new format.

Ignoring the candidate gate would make the repository invalid after later adoption. Using candidate code as the evaluator would reverse the approved trust direction. Publishing a separate bridge evaluator could solve the cycle but would add a second product release. A narrow predecessor-evaluator bootstrap must instead preserve evidence and current authority without becoming a reusable bypass.

## Preconditions and trigger

- One approved replacement release contract explicitly declares the bootstrap schema, release version, one future release-record ID, exact canonical `utf8-text-lf-v1` schema-2 root-lock SHA-256, predecessor evaluator version, safe wheel name, and independently reconciled wheel SHA-256.
- The current root lock canonicalizes to that exact schema-2 identity and retains the configured predecessor version.
- The release record is newly prepared as `ready` by the exact external predecessor evaluator and binds the same release contract, version, candidate, verified aggregate, and released-work set.
- The predecessor evaluator wheel is available as immutable public bytes and is installed outside the checkout with isolation and checkout exclusion.

## Required response

- Retain canonical `se-harness-evaluator-evidence-v1` bytes describing the exact external predecessor evaluator, including complete archive identity and bounded runtime origins.
- Bind the evidence path and digest to the one declared ready RLS without changing its candidate, version, relations, lifecycle state, or release decision.
- Mark the predecessor preparation format explicitly so legacy preparation fields cannot be mistaken for a release decision.
- Validate the binding against the approved release contract and exact canonical current schema-2 lock rather than pretending the lock already contains schema-3 evaluator identity.
- Resolve publication evaluator bytes from the approved bootstrap contract only for that record, verify them before installation, and stop before credentials on any mismatch.
- Preserve ordinary schema-3 current-lock matching for every other ready RLS.

## Failure and boundary behavior

Missing approval, wrong record ID, wrong version, canonical lock-content drift, evaluator-version drift, archive mismatch, noncanonical or modified evidence, contaminated origins, candidate-source execution as evaluator, relation drift, or more than one bootstrap record fails closed before RLS or root mutation and before credential-bearing publication work.

The bootstrap never transitions a VREC or RLS, creates a commit or tag, publishes, deploys, upgrades the root, changes maintenance state, or grants a human decision right.

## Constraints

- Exactly one release-record ID is named by one approved release contract.
- The RLS still carries canonical evaluator evidence; this is not a missing-evidence allowlist.
- The schema-2 lock remains unchanged through release preparation and publication.
- Candidate source may package and verify an observation through a repository-owned binder, but released 0.5.0 remains the evaluator that prepares and validates the RLS.
- Historical VREC/RLS facts and the stopped candidate `827b2709292abaa3458bb3b4cac37b582378c585` are not repointed or rewritten.
- Post-publication root adoption remains a separate evaluator-upgrade transaction.

## Acceptance examples

### Example: normal behavior

**Given** an approved release contract naming `RLS-SEH-009`, the exact current schema-2 lock, and the public 0.5.0 evaluator archive

**When** released 0.5.0 prepares the ready record and the bounded binder observes that exact isolated evaluator

**Then** the record receives canonical evidence, both released-0.5 and candidate validation pass under their declared compatibility rules, and publication can resolve the same public evaluator without changing the root.

### Example: failure behavior

**Given** a ready RLS with the same version but a different ID, lock digest, candidate role, archive digest, or evidence byte

**When** binding, validation, or publication resolution runs

**Then** it fails before mutation or credentials and cannot fall back to a generic legacy allowlist.

## Open decisions

Resolved on 2026-08-21: the accountable owners approved the exact contract-bound bootstrap design together with its specification, architecture, ADR, verification contract, bounded work order, and replacement release contract. Later candidate, assurance, release, external, and root actions remain separately governed.

Corrected on 2026-08-21 at `2026-08-21T16:31:42Z`: the accountable owners authorized the bounded canonical-LF correction across the seven-artifact packet while preserving every status and other scope boundary. The lock identity is the canonical `utf8-text-lf-v1` content digest, so Git's LF blob and a platform-smudged CRLF checkout represent one governed lock rather than different release facts.
