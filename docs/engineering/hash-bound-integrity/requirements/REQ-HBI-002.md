+++
id = "REQ-HBI-002"
type = "requirement"
title = "Determine hash mode from the declared class, not the call site"
status = "approved"
owners = ["repository-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN the harness computes or compares a SHA-256 over a committed hash-bound text file, THE SYSTEM SHALL take the hash mode from that file's declared class, and SHALL NOT apply two different modes to one class."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "repository-owner"
+++

# Requirement: Determine hash mode from the declared class, not the call site

## Rationale

`.engineering-harness.lock` is hashed by two callers under two rules.
`repository_tools/release_bootstrap.py` canonicalizes its bytes before hashing,
so `from_lock_sha256` is line-ending independent.
`se_harness/upgrade_authorization.py` hashes the raw bytes supplied by
`se_harness/mutation_guard.py`, so `prior_lock_sha256` is line-ending dependent.
Both describe the same file. Whichever is correct, they cannot both be, and no
reader of either digest field can tell which rule applies to it.

`RC-060-02`'s completion criteria require distinguishing raw from normalized
hashes. Distinguishing them at the call site is what produced the divergence.
The distinction has to live with the file, in one place, so that adding a caller
cannot introduce a third answer.

## Preconditions and trigger

The installer, upgrade authorization, mutation guard, release bootstrap,
candidate acceptance, preflight, `doctor` or a test computes or compares a
SHA-256 over a committed text file that a declared class covers.

## Required response

- Obtain the hash mode for the path from its declared class before hashing or
  comparing.
- Apply exactly one mode per class across every caller.
- Where a stored digest predates its class declaration, permit recognition
  through the documented newline-variant comparison already available in
  `se_harness/integrity.py`, and report explicitly that a legacy variant matched
  rather than reporting an ordinary match.
- Write committed hash-bound text with an explicit LF newline at every producing
  call site, so a producer's platform cannot decide a bound file's bytes.

## Failure and boundary behavior

A caller that cannot resolve a mode fails closed rather than defaulting. A second
mode applied to one class is a defect detectable by test, not a configuration
option. Invalid UTF-8 in a text-mode class fails closed with a bounded
path-level diagnostic.

No historical digest is recomputed or rewritten. `WO-HUP-002`'s recorded
`prior_lock_sha256` remains exactly as recorded and is read, never corrected. A
mode correction therefore changes future comparisons only, and legacy
recognition exists precisely so that history stays readable.

## Constraints

Mode determination introduces no new hashing algorithm and no new canonical
form. The two modes are the existing raw bytes and the existing
`utf8-text-lf-v1` canonical representation defined by `REQ-PMI-001`. SHA-256,
path containment, symlink safety, atomic writes and authority separation are
unchanged.

## Acceptance examples

### Example: normal behavior

**Given** `.engineering-harness.lock` declared as a canonical-mode class,

**When** upgrade authorization and release bootstrap each compare a recorded lock
digest on a CRLF checkout,

**Then** both compute the same canonical digest and both reach the same verdict.

### Example: failure behavior

**Given** a test that hashes a declared class's file with the raw mode while its
declaration says canonical,

**When** the mode-consistency test runs,

**Then** it fails naming the class and both modes observed.

**Given** a digest recorded before the class was declared, whose bytes differ from
the canonical form only by line endings,

**When** a comparison runs,

**Then** the comparison succeeds through legacy newline-variant recognition and
reports that a legacy variant matched.

## Open decisions

None when approved. The mode assigned to each existing class is fixed by
`SPEC-HBI-001` rather than left open: evaluator evidence and the migration
protocol paths remain raw, and `.engineering-harness.lock` becomes canonical.
