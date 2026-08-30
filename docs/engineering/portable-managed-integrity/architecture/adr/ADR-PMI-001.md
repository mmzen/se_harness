+++
id = "ADR-PMI-001"
type = "adr"
title = "Versioned canonical UTF-8 LF integrity"
status = "approved"
owners = ["engineering-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-PMI-001"]
+++

# ADR: Versioned canonical UTF-8 LF integrity

## Status

Accepted.

## Context

Raw byte hashes conflate logical text customization with checkout newline representation. Enforcing one Git configuration would not protect archives, package installs, copied repositories, or existing consumers, while silently interpreting old raw digests under new rules is not cryptographically sound.

## Decision drivers

- Correctness on Windows, Linux, and macOS.
- Continued detection of every non-line-ending managed change.
- Conservative, auditable legacy migration.
- One standard installation and standard-library runtime.
- No dependence on Git configuration or network services.
- Deterministic source, package, and installed behavior.

## Considered options

1. Continue raw byte SHA-256 and update lock entries manually.
2. Enforce LF through `.gitattributes` and require repository renormalization.
3. Store multiple platform-specific raw digests.
4. Canonicalize managed UTF-8 line terminators, record an explicit versioned mode in schema 2, and keep schema-1 handling conservative.

## Decision

Choose option 4. Canonical integrity validates UTF-8, maps CRLF and CR to LF, preserves all other content exactly, and hashes with SHA-256. New locks use schema 2 and `utf8-text-lf-v1`. Schema 1 retains its historical evidence semantics, including former fragment CRLF handling; it migrates only on legacy equality or canonical equality to the fully rendered current desired content.

Do not use repository-wide Git policy as the correctness mechanism. Git attributes may be adopted independently for contributor convenience but cannot substitute for lock semantics.

## Consequences

- Positive: portable doctor and upgrade decisions; explicit future-extensible semantics; shared producer/consumer logic; newline conversion no longer causes false customization.
- Negative: lock schema increases; schema-1 ambiguous mismatches still require manual review; strict UTF-8 limits future binary-managed assets until a separate mode is designed.
- Operational: the self-repository lock must be regenerated through the supported writer and verified in clean checkout and wheel scenarios.
- Security: non-newline changes, fragment boundaries, path containment, and non-overwrite controls remain strict; no fuzzy equivalence is introduced.
- Migration: new operations emit schema 2, while legacy exact matches remain valid and safe desired-content equality can migrate without rewriting content.

## Validation

Property tests cover newline equivalence and content sensitivity. Integration tests cover schema-1 and schema-2 doctor/upgrade behavior, fragments, invalid inputs, atomic failure, and path safety. Distribution verification covers self-lock consistency, canonical template parity, wheel contents, and fresh LF/CRLF installations.

## Amendment record

**The schema-1 retention consequence is closed, 2026-08-30 under
`WO-HUP-012`.** This decision retained schema-1 evidence semantics with
conservative migration while 0.2.x roots existed. The owner's floor
decision of 2026-08-30 (issue #285, item #285a) ends that retention: locks
below schema 3 are not read, and the migration path is removal of the
stale lock plus re-adoption (`REQ-HUP-024`, `SPEC-HUP-012`). The canonical
integrity semantics this decision chose are unchanged and remain in force
for the schema-3 lock. Nothing else in this decision record changes.
