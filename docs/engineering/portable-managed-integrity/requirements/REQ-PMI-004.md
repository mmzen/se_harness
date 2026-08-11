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
