+++
id = "INT-HBI-001"
type = "intent"
title = "Keep committed hash-bound bytes stable on every checkout"
status = "approved"
owners = ["repository-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "repository-owner"
+++

# Intent: Keep committed hash-bound bytes stable on every checkout

## Problem

A committed text file whose raw bytes are bound by a recorded SHA-256 has no
stable identity unless something versioned in the repository forces its
checkout bytes. Git may legitimately translate line endings according to
unversioned local configuration, so the same logical file acquires different
raw identities on different machines. Root cause `RC-060-02` recorded this after
`RLS-SEH-009` bound canonical LF evaluator evidence that a default Windows
checkout rewrote to CRLF, failing validation with `E012` on one machine and
passing on another.

The correction shipped at the time was correct and deliberately narrow.
`ADR-REB-003` selected one versioned attribute for one path class,
`docs/engineering/**/evidence/*.json`, and `REQ-REB-009` bounded the obligation
to evaluator evidence. Nothing generalizes that obligation, and nothing detects
its absence. A new hash-bound text file can be added today with no byte rule,
and `doctor`, `validate`, required CI and the full test suite all pass.

That gap is not hypothetical. `.engineering-harness.lock` is committed as LF
but has no attribute, and two code paths hash it under two different rules:
`repository_tools/release_bootstrap.py` canonicalizes before hashing, while
`se_harness/upgrade_authorization.py` hashes the raw worktree bytes handed to it
by `se_harness/mutation_guard.py`. On a checkout with `core.autocrlf=true` those
two paths therefore disagree about the identity of one file, and the raw path
governs evaluator-upgrade authorization.

## Desired outcomes

- Every committed file whose bytes are hash-bound resolves to a declared class
  carrying an explicit byte rule.
- A raw-mode class with no effective versioned Git attribute fails closed
  instead of passing on whichever machine happens to be configured favourably.
- One committed file is never hashed under two different modes by two callers.
- Adding a new hash-bound text file without declaring its rule is detected at
  the time it is added, not at the release that depends on it.
- Every recorded historical digest remains readable and unrewritten.

## Actors and stakeholders

- Repository owners and coding agents, who currently depend on unversioned local
  Git configuration for a correctness property.
- Release owners, who bear the cost when a bound digest fails on the machine
  performing a release.
- Security and quality owners, who require that exact-byte trust is preserved
  rather than relaxed to make diagnostics pass.
- Consumers of installed harnesses, who inherit whichever byte rules the
  canonical template declares.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Committed hash-bound text classes with a declared byte rule | 2 of 3 | 3 of 3 | packet verification |
| Raw-mode classes lacking an effective Git attribute | 1 | 0 | every `doctor` run |
| Committed files hashed under two different modes | 1 | 0 | every CI run |
| Raw-mode classes proven under LF, CRLF and CR checkout | 1 of 2 | 2 of 2 | every CI run |
| Undeclared new hash-bound text file reaching `main` | undetected | fails closed | every `doctor` and CI run |

## Non-goals

- Changing repository-wide line-ending policy or any operator's Git
  configuration.
- Reopening the option `ADR-REB-003` rejected, namely normalizing evidence
  before validator hashing. That decision stands and this intent depends on it.
- Uncommitted release-bundle text such as `SHA256SUMS` and the source manifest
  named by `RLS-SEH-012`.
- Generated content, including the `dashboard-manifest.json` behind
  `artifact_snapshot_sha256`, which already writes an explicit LF newline.
- Canonicalizing binary archives.
- Rewriting, recomputing or repointing any historical `WO`, `REL`, `VREC` or
  `RLS` digest.
- Adopting a new governor. A new check binds the repository's own gate only
  after a separately authorized governor upgrade.

## Principles and immutable constraints

Exact-byte trust is preserved, never relaxed. Byte rules are versioned
repository content, never local Git configuration. Unknown, unreadable or
unassessable state fails closed and is never reported as a pass. Declarations
are data, not executable expressions. Historical digests remain valid history
and are read, never rewritten.

## Risks and assumptions

- Fact: at `469dd9c` on a clone with `core.autocrlf=true`,
  `.engineering-harness.lock` is stored as a 6,184-byte LF blob with SHA-256
  `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79` and checks
  out as 6,343 CRLF bytes with SHA-256
  `978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e`. The
  canonical digest of the worktree copy equals the blob digest.
- Fact: `se_harness/upgrade_authorization.py` compares a raw digest;
  `repository_tools/release_bootstrap.py` compares a canonical digest; both
  describe `.engineering-harness.lock`.
- Fact: `se_harness/integrity.py` already exposes
  `matches_legacy_newline_variant`, so a digest recorded before its class was
  declared can be recognized without rewriting it.
- Fact: `docs/engineering/**/evidence/*.json` is declared in the managed
  template fragment; the migration-protocol paths are declared only in the
  owner-controlled region of the repository's own `.gitattributes`.
- Assumption: a declaration inside the harness with a fail-closed check is
  preferable to review discipline over a hand-maintained attribute list.
- Assumption: the evaluator-upgrade path is exercised rarely enough that the
  known lock defect has not yet caused a visible failure, which makes it a
  latent rather than an active incident.
- Resolved decision: on 2026-08-24 the accountable owner answered the one open
  decision this intent carried — whether the completeness check is a `doctor`
  check only, or additionally a validator plane rule — with `doctor alone`. The
  reasoning the specification offered stands: checkout-byte effectiveness is a
  property of an installed working tree rather than of the artifact graph, and a
  validator rule would not bind this repository's own required gate until a
  separately authorized governor upgrade. No open decision remains in this
  intent. A validator plane rule is now a non-goal of this packet and would
  require its own governing chain.
