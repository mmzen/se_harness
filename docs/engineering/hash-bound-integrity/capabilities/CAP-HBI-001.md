+++
id = "CAP-HBI-001"
type = "capability"
title = "Prove that committed hash-bound text keeps its bound bytes"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
derives_from = ["INT-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "repository-owner"
+++

# Capability: Prove that committed hash-bound text keeps its bound bytes

## Actor and need

Repository owners, coding agents and release owners need to know, before they
depend on a recorded digest, that the file it binds will present the same bytes
on every supported checkout, and that no hash-bound file is relying on an
undeclared assumption.

Today they cannot know this. The evidence class is protected, the lock class is
not, and nothing distinguishes the two. Discovery happens when a bound
comparison fails on one machine and passes on another, which is the most
expensive moment to learn it.

## Capability statement

`A repository operator can determine, from versioned repository content alone,
the byte rule governing every committed hash-bound text file, and receives a
fail-closed diagnostic when a raw-mode class has no effective Git attribute or
when one class is hashed under two modes.`

## Boundaries

- The capability applies only to files tracked in Git whose bytes a governed
  artifact field or an authorization input binds by SHA-256, and to the
  declaration of those files' byte rules.
- Uncommitted build and release outputs are outside the boundary, including
  `SHA256SUMS` and the source manifest named by `RLS-SEH-012`.
- Generated content under `target/` is outside the boundary.
- Binary archives are outside the boundary; no binary canonicalization is
  inferred.
- Managed-file digests recorded in `.engineering-harness.lock` under
  `utf8-text-lf-v1` remain owned by `CAP-PMI-001`. This capability declares
  their mode so the distinction is explicit, and changes nothing about how they
  are computed.
- The capability produces technical evidence and enforces declared policy. It
  grants no human decision right, performs no lifecycle transition, and never
  rewrites a recorded digest.
- Operator Git configuration is observed for effectiveness assessment. It is
  never treated as formal authority and is never modified.

## Outcomes

- One reviewable declaration answers "what governs this file's bytes" for every
  committed hash-bound path.
- An undeclared hash-bound file, a missing or overridden attribute, and a
  two-mode class each produce a named failing check rather than silence.
- Byte rules that must reach consumer installations travel in the canonical
  template; repository-specific rules stay in owner-controlled content, and
  completeness spans both regions.
- Cross-platform checkout behaviour becomes a tested property per class instead
  of a property proven once for one class.

## Candidate requirements

`REQ-HBI-001` defines the declaration, attribute-effectiveness and fail-closed
completeness obligation. `REQ-HBI-002` defines single-mode determination, so a
file's hash mode follows its declared class rather than the call site that
happens to read it.
