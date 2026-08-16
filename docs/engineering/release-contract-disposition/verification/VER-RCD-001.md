+++
id = "VER-RCD-001"
type = "verification"
title = "Verify release-proposal disposition"
status = "approved"
owners = ["quality-owner", "release-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-RCD-001"]
+++

# Verification Contract: Verify release-proposal disposition

## Verification matrix

| Concern | Pass condition |
| --- | --- |
| selected proposals | exactly the six specified REL records change from `draft` to `rejected` |
| original facts | IDs, owners, gates, and original contract clauses remain unchanged |
| authoritative lineage | every gate is present in the named released RLS and its active aggregate contract |
| historical integrity | no existing REL other than the six, VREC, RLS, tag identity, or release evidence changes |
| operating separation | all six corresponding OPS records remain approved and unchanged |
| graph | formal validation and doctor pass without a new diagnostic |
| inspection | `definition_pending` becomes empty and no automatic action is taken |
| determinism | consecutive inspection JSON reports are byte-identical |
| change hygiene | review preflight and `git diff --check` pass |

## Evidence retention

Retain the before/after lifecycle inventory, exact lineage mapping, changed-path audit, validation, doctor, inspection, preflight, and diff results under `docs/engineering/release-contract-disposition/evidence/WO-RCD-001-verification.md`.
