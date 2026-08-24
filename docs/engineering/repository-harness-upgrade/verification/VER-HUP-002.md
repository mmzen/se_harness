+++
id = "VER-HUP-002"
type = "verification"
title = "Verify standard-root adoption of exact public 0.6.0"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "quality-owner"

[relations]
verifies = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
+++

# Verification Contract: Verify standard-root adoption of exact public 0.6.0

## Independence

All authoritative upgrade, doctor, integrity, and root-validation commands run from the isolated public wheel installation. Checkout source may provide non-authoritative comparison tests only.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-HUP-004 | archive, distribution, module, entry-point and payload identity | exact public 0.6.0 hashes and all evaluator origins outside checkout |
| REQ-HUP-005 | authorization match, plan/apply/no-op, lock and transaction evidence | only exact reviewed paths change; schema-3 lock and canonical evidence agree |
| REQ-HUP-006 | complete-root doctor/validate/inspect/dashboard, tests and diff ledger | zero formal errors; managed CI selects 0.6.0; non-root identities unchanged |

## Required cases

- Wrong archive, payload, runtime origin, work order, prior lock, or evidence path fails before mutation.
- Pre-adjustment `.gitattributes` customization blocks apply.
- Exact repository-owned rule separation produces a conflict-free plan without changing rule semantics.
- Apply succeeds atomically and repeat planning is a no-op.
- Public 0.6.0 validates the complete retained rejected history without a compatibility view.
- Schema-3 lock contains exact archive and installed-payload identity.
- Repository tests pass on the default runtime and Python 3.11 where available.
- Product source/templates, package version, RLS/VREC/REL, tag-related bytes, publication workflows, and external state are unchanged.

## Hosted evidence

After an authorized candidate commit, require the managed Engineering Harness lane and separately labeled candidate lanes. Hosted success does not verify a VREC or authorize merge.

## Evidence retention

Retain canonical transaction JSON at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json` and a human-readable ledger at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-verification.md`.
