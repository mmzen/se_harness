+++
id = "REQ-DST-053"
type = "requirement"
title = "Contain progressive-loading failures and races"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a progressive dashboard request fails, times out, is superseded by newer navigation, or returns invalid data, THE SYSTEM SHALL contain the outcome to its requesting panel and preserve the latest verified user selection without presenting partial data as authoritative."
verification_method = "automated-browser-test-and-failure-injection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Contain progressive-loading failures and races

## Rationale

Splitting one embedded snapshot into asynchronous resources creates ordering, cancellation, caching, and partial-failure risks. A slow earlier selection must not overwrite a later one, and a single missing resource must not make verified unrelated data disappear.

## Preconditions and trigger

Explorer has issued one or more manifest-bound resource requests and the reader navigates, retries, changes revision by reopening a newly generated bundle, or encounters an HTTP, integrity, schema, parsing, or rendering failure.

## Required response

- Associate each request with its manifest revision, resource descriptor, and initiating view or artifact.
- Abort superseded requests when practical and always ignore stale completion for current-panel rendering.
- Deduplicate identical in-flight requests and retain only verified results in the revision-scoped cache.
- Report loading, retryable failure, unavailable, and integrity-failure states with the exact affected resource class.
- Preserve already verified summary, topology, history, and detail data that is independent of the failed request.

## Failure and boundary behavior

No failure may silently become empty data, reuse a cache entry from another manifest, bypass hash verification on retry, infer graph invalidity, or transition any lifecycle or assurance state.

## Constraints

- Failure messages must not expose unsafe raw URLs or execute repository text.
- Retry remains an observation action, not a governance decision.
- Cache and request bookkeeping must be bounded by the generated resource set and visit behavior.

## Acceptance examples

### Example: rapid navigation

**Given** detail A is loading,

**When** the reader selects B and B completes before A,

**Then** B remains selected and A cannot overwrite its panel.

### Example: evidence integrity failure

**Given** an evidence response differs from its manifest digest,

**When** verification completes,

**Then** only that evidence entry reports integrity failure and no returned bytes are rendered.

## Open decisions

None when approved.
