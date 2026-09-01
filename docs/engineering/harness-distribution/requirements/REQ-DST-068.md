+++
id = "REQ-DST-068"
type = "requirement"
title = "Emit computed governance indicators and record proof fields"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-09-01"
updated = "2026-09-01"
statement = "WHEN a dashboard bundle is generated, THE SYSTEM SHALL emit deterministic governance indicators and record proof fields derived only from recorded lifecycle events, declared relations, and record front matter, without inferring any approval, verification, or release decision."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-01T20:51:14Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-01 by selecting the presented option 'Approve, start, complete on green (Recommended)', after reviewing the designed Explorer against the complete repository bundle in the local design loop and instructing its integration as the canonical template. The owner also accepted, by selecting 'Accept now, next design round fixes it (Recommended)', the recorded deviation that the Lineage view prefetches every artifact detail until a following design round loads details for the selected spine only."
+++

# Requirement: Emit computed governance indicators and record proof fields

## Rationale

The designed Overview states facts a visitor can act on: how many lifecycle
decisions are recorded and whether every one names its decider, how many were
taken by a delegated executor under the required check, the lead time from
approval to implementation, whether every released work order carries a
verified record, and which release is current with which bound commit and
distribution digests. Today those facts exist only across 1,224 artifact
detail documents; a page that computed them client-side would fetch the whole
bundle to draw one screen.

The generator already holds every input. Computing the indicators once, at
generation time, keeps the page's initial path bounded (`REQ-DST-055`), keeps
the figures identical between two generations of the same repository state
(`REQ-DST-031`), and makes them testable against fixtures.

Two proof fields that records carry in their front matter were never
projected into the bundle: a release record's `[distribution]` table (wheel
and sdist names and digests, the checksum file, the source manifest digest)
and a record's `evaluator_evidence_sha256`. Without them the page cannot show
the "verify it yourself" line that turns a claim into something an auditor
recomputes.

## Behavior

- Trigger: `generate_harness_dashboard.py` builds a bundle from a valid
  canonical projection.
- Response: the summary resource carries a `metrics` object restating event
  counts, attribution by decider, delegated transitions and records, lead
  times per work order, released-work coverage by verified records, the
  latest released record, and its contract-to-release arc; release-record
  and verification-record details carry `evaluator_evidence_path` and
  `evaluator_evidence_sha256`; release-record details and their compact
  topology rows carry the scalar fields of the `[distribution]` table plus
  `version` and `released_at`; the repository descriptor carries a
  normalized public `source_url` when the origin remote is a GitHub
  repository.
- On failure: a missing or malformed input field is omitted or nulled, never
  invented; a repository without a recognized public remote carries
  `source_url: null`; no figure is an aggregate score.

## Assumptions and dependencies

- Lifecycle events are recorded as `from`, `to`, `decided_at`, `decided_by`,
  `reason` in artifact front matter, as `SPEC-DST-008` and the lifecycle
  contracts already require.
- Release records relate to their contract through `satisfies`, to their
  aggregate record through `includes_verification`, and to shipped work
  through `releases_work`; verification records relate to work through
  `verifies_work_order`.

## Acceptance examples

### Example: a small fixture

**Given** one released record that releases one work order approved at 10:00
and implemented at 11:30 by a delegated executor, verified by one record,

**When** the bundle is generated twice,

**Then** both summaries carry identical `metrics` with one lead time of 1.5
hours, two delegated transitions, one delegated record, and a released-work
coverage of one of one.

### Example: fields absent from history

**Given** a release record written before the `[distribution]` table existed,

**When** its detail is projected,

**Then** `distribution` is `null`, the page omits the digest rows, and no
digest is fabricated.

## Open decisions

None.
