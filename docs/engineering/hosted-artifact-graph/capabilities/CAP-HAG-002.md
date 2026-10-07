+++
id = "CAP-HAG-002"
type = "capability"
title = "Complete and export one hosted lifecycle rehearsal"
status = "approved"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
ability = "An operator rehearses a complete engineering change in an isolated graph project and exports its exact records and evidence."

[relations]
derives_from = ["INT-HAG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-06T18:40:36Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the Phase 3 package published in PR #542 at 689dee3b1929e5c58338df1331a0eb9df484ce25. Approves the nine governing definitions and WO-HAG-008, including required commit-bound verification under VER-HAG-006 and its bounded local execution. Git remains authoritative; this is a private test-copy lifecycle rehearsal. Authentication and database ACL implementation remain deferred; existing controls stay. Includes the reviewed bounded publication grant to mmzen/se_harness, source codex/hosted-artifact-phase3, target main, draft PR #542, including the ready record and a later separately supplied verification-decision push. No risk acceptance, actual assurance decision, merge, real authority cutover, release, deployment or host-plugin update is granted."
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
