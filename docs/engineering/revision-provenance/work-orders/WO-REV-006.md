+++
id = "WO-REV-006"
type = "work_order"
title = "Approve aggregate verification of the se-harness 0.2.0 candidate"
status = "verified"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-REV-002", "REQ-REV-004", "REQ-REV-005", "REQ-REV-006"]
specifications = ["SPEC-REV-001"]
architecture = ["ARCH-REV-001", "ADR-REV-001"]
verification = ["VER-REV-001"]
+++

# Work Order: Approve aggregate verification of the se-harness 0.2.0 candidate

## Objective

Record the accountable assurance decision for `VREC-SEH-001` after reviewing its complete retained evidence and exact ten-work-order candidate commit.

## Authorization

The accountable repository owner explicitly validated the aggregate candidate evidence and authorized this verification transition and its governance commit on 2026-08-11 with the instruction `i validate, then transition and governance commit`.

## In scope

- Confirm `VREC-SEH-001` is a valid `ready` record for the ten explicitly selected release-bearing work orders and six applicable verification contracts.
- Confirm it names clean candidate commit `1329c7a4472f323c4b21d869545cad3c647fe568` and was retained in ready-record governance commit `656f94276b7d6100c6c344c0b4db8cf1c1db261c`.
- Review all ten retained evidence paths and the aggregate artifact snapshot recorded by `VREC-SEH-001`.
- Transition only `VREC-SEH-001` from `ready` to `verified` and retain an explicit human-decision note.
- Retain evidence keyed to this work order.
- Create one separate governance commit containing the bounded transition artifacts.

## Out of scope

Changing the candidate commit, artifact snapshot, evidence paths, verification contracts, or selected work orders; preparing or transitioning a release record; creating a tag; pushing or updating the pull request; package publication; deployment; and release authorization are not authorized.

## Required verification

The expanded graph must validate; the declared candidate must remain available locally and in the checkout ancestry; every retained evidence path, relation, commit field, and snapshot must remain unchanged; the complete unit suite must pass on Python 3.11 and the local runtime; CLI help and doctor checks must pass; and the final diff must contain only this decision's bounded governance artifacts.

## Completion evidence

Retain the reviewed facts, hashes, commands, outcomes, deviations, and authority boundary in `docs/engineering/revision-provenance/evidence/WO-REV-006-verification.md`.
