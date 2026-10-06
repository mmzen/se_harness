+++
id = "CAP-HAG-002"
type = "capability"
title = "Complete and export one hosted lifecycle rehearsal"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
ability = "An operator rehearses a complete engineering change in an isolated graph project and exports its exact records and evidence."

[relations]
derives_from = ["INT-HAG-002"]
+++

# Complete and export one hosted lifecycle rehearsal

## Ability

An operator can prepare a disposable project, and a human or agent can use the
remote client to author its definitions, inspect gates, request allowed lifecycle
operations, retain test evidence, prepare test verification and release records,
and export a selected snapshot. A lost reply can be reconciled without repeating
an accepted change.

## Conditions

The selected project is explicitly a test copy. Imported real records remain
immutable history. New rehearsal records and supplied actor labels are test
inputs; they do not establish real human identity, consent or authority.

The same separately installed released evaluator supplies templates, lifecycle
rules, gate results and generated record bytes. The service commits the complete
result atomically or leaves its selected graph state unchanged.

## Boundary

Git remains authoritative outside the disposable project. Exports are reviewable
test data, never automatic writes to a real checkout. The pilot issues no GitHub,
PyPI, registry, tag, marketplace or deployment action.
