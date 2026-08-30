+++
id = "REQ-PMI-004"
type = "requirement"
title = "Migrate legacy locks conservatively"
status = "implemented"
owners = ["repository-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the harness reads a schema-1 raw-byte lock, THE SYSTEM SHALL preserve legacy compatibility and migrate to canonical schema-2 evidence only when unchanged desired content can be proven without overwriting customization."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Migrate legacy locks conservatively

## Rationale

A raw SHA-256 digest cannot in general be reinterpreted as a canonical text digest because the original bytes are unavailable.

## Preconditions and trigger

Doctor or upgrade reads a valid schema-1 lock with no canonical hash-mode declaration.

## Required response

Accept exact raw-digest matches. A safe upgrade may also recognize current content that is canonically identical to the fully rendered desired managed file or fragment. Applied safe outcomes write a complete schema-2 lock. Ambiguous mismatches remain customized and retain their legacy evidence.

## Failure and boundary behavior

Unknown schemas, invalid entries, unsafe paths, invalid text, or content matching neither exact legacy evidence nor the canonical desired template fail closed. Doctor never rewrites a legacy lock.

## Constraints

Migration must be atomic and deterministic. It must not claim that an arbitrary legacy mismatch is a newline-only change.

## Acceptance examples

An exact schema-1 target migrates safely during applied upgrade. A target canonically equal to the current desired template may migrate without rewriting its content. An unrelated edit remains customized.

## Open decisions

None when approved.

## Amendment record

**Schema-1 reading is retired, 2026-08-30 under `WO-HUP-012`.** This
requirement made the harness read a schema-1 raw-byte lock conservatively
and migrate it only on proven equality. The owner's floor decision of
2026-08-30 (issue #285, item #285a: "locks older than schema 3 are not
read", taken as the hard floor) supersedes that obligation: per
`REQ-HUP-024` and `SPEC-HUP-012`, a lock whose schema is below 3 is refused
at read with one diagnostic naming re-adoption as the route, and the
legacy digest machinery this requirement mandated is deleted. The
requirement's history stays valid as the record of the 0.2.x-era
compatibility it governed. Nothing else in this requirement changes.
