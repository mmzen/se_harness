+++
id = "SPEC-ECP-010"
type = "specification"
title = "The line-ending-canonical formal snapshot"
status = "draft"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-021"]
+++

# Specification: The line-ending-canonical formal snapshot

## Scope

The byte rule of `formal_snapshot_digest`, the one function every formal
snapshot in the product comes from: the evidence packet header, the
`compliance.formal_snapshot_sha256` of `check`, and a verification record's
`artifact_snapshot_sha256`. Issue #256. `SPEC-ECP-001`'s `ECP-SNP-001` is
amended by record to name this rule for the bytes it hashes.

## Terms

- **Canonical bytes:** the `utf8-text-lf-v1` representation
  `se_harness/integrity.py` defines for the managed-file lock: UTF-8 text
  with every `CRLF` and lone `CR` line ending rendered as `LF`; content
  that is not UTF-8 text is left as its raw bytes.

## Behavioral rules

**ECP-CSN-001:** `formal_snapshot_digest` hashes, for each artifact in
POSIX-path order, the length-prefixed relative path and the length-prefixed
canonical bytes of the artifact's content; the path, the ordering and the
framing are unchanged from the raw rule.

**ECP-CSN-002:** For a tree whose artifacts carry LF line endings the digest
equals the raw-byte digest, so every packet header and verification record
bound from an LF checkout keeps its value; a conformance test asserts
equality against a digest fixed before this change.

**ECP-CSN-003:** For a tree whose artifacts carry CRLF line endings the
digest equals the LF tree's; a conformance test builds both from one
fixture and asserts equality, and asserts inequality after one character of
content changes.

**ECP-CSN-004:** The rule reaches every caller through the one function:
`write_evidence_packet`, `build_context`, and `repository_state._formal_state`
call `formal_snapshot_digest` and nothing else computes a snapshot.

**ECP-CSN-005:** `docs/notes/harnessctl-check.md` states that the snapshot
is line-ending-canonical and that a packet bound on any checkout matches
the runner.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-021 | ECP-CSN-001 to ECP-CSN-005 |

## Failure behaviour

Content that is not UTF-8 text is hashed raw; an unreadable artifact fails
the evaluator as it does today. Nothing is refused that was accepted
before.

## Compatibility and migration

No stored digest on an LF tree moves. A packet bound on a CRLF checkout
under the raw rule (none exists on `main`) would read as stale and is
rebound with `harnessctl evidence`.
