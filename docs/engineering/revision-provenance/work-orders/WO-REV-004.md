+++
id = "WO-REV-004"
type = "work_order"
title = "Approve aggregate verification of portable managed integrity"
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

# Work Order: Approve aggregate verification of portable managed integrity

## Objective

Record the accountable assurance decision for `VREC-PMI-001` after reviewing its retained evidence, aggregate scope, and exact candidate commit.

## Authorization

The accountable repository owner explicitly validated the evidence and authorized this verification decision and its governance commit on 2026-08-11 with the instruction `i validate, then transition and governance commit`.

## In scope

- Confirm `VREC-PMI-001` is a valid ready aggregate record for `WO-AGR-001` and `WO-PMI-001` under `VER-AGR-001` and `VER-PMI-001`.
- Confirm it names the clean corrective candidate `505e889777c3c50f544b7e6d6fe58e2f765c1fea`.
- Review both retained evidence files and the successful checks recorded for that candidate.
- Transition only `VREC-PMI-001` from `ready` to `verified` and retain an explicit human-decision note.
- Retain evidence keyed to this work order.
- Create one separate governance commit containing the bounded transition artifacts.

## Out of scope

Changing the candidate commit or snapshot, creating a release record or tag, pushing, opening or merging a pull request, package publication, deployment, and release authorization are not authorized.

## Required verification

The expanded graph must validate, the declared candidate must remain available locally and in the checkout ancestry, aggregate relations and both evidence paths must remain consistent, the complete unit suite, CLI help, and doctor checks must pass, and the final diff must contain only this decision's bounded governance artifacts.

## Completion evidence

Retain the reviewed facts, commands, outcomes, deviations, and authority boundary in `docs/engineering/revision-provenance/evidence/WO-REV-004-verification.md`.
