+++
id = "SPEC-HUP-002"
type = "specification"
title = "Standard-root adoption contract for released 0.6.0"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "technical-owner"

[relations]
specifies = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
+++

# Specification: Standard-root adoption contract for released 0.6.0

## Scope

Define one local, plan-first adoption of exact public 0.6.0 from the current released 0.5.0 schema-2 root. Product, release, publication, deployment, maintenance, and historical governance state remain outside the transaction.

## Inputs

- Clean main-derived repository at base `7b5a705` or an explicitly reviewed successor containing only this packet.
- Current raw lock SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- Exact public wheel and installed payload identities declared by `REQ-HUP-004`.
- Approved and started `WO-HUP-002`.

## State model

`draft packet -> explicit approval -> reviewed dry run -> work in progress -> bounded apply -> complete local qualification -> implemented candidate -> commit-bound VREC -> integration`

No state transition is inferred from a passing command.

## Behavioral rules

1. Execute the evaluator only from the isolated public 0.6.0 environment.
2. Validate archive and installed-payload identities before plan and again before apply.
3. Treat `.gitattributes` as a reviewed integration boundary: the public 0.6 fragment remains inside its markers; post-release migration LF rules remain outside the markers as repository-owned policy.
4. Re-run the plan after that adjustment and require no `customized` or `conflict` result.
5. Apply only through `harnessctl upgrade . --work-order WO-HUP-002 --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json --apply`.
6. Require atomic managed writes, schema-3 evaluator identity, canonical evidence, and no-op replay.
7. Run exact public 0.6.0 doctor and validation on the complete checkout, not a predecessor view.
8. Run inspection, dashboard, preflight/review where applicable, repository tests, workflow checks, diff checks, and product/release preservation comparisons.
9. Do not edit candidate product/templates, version metadata, RLS/VREC/REL history, tags, publication workflows, Pages, maintenance state, or external policy.
10. Stop before commit, push, PR, merge, VREC transition, release, publication, or deployment unless separately authorized.

## Reviewed managed plan

The pre-adjustment dry run reports 36 template entries: 17 unchanged, 18 update/add operations, and one `.gitattributes` customization. After the exact integration adjustment, the permitted installer-owned paths are:

- `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, `AGENTS.md`, `CLAUDE.md`, and `ENGINEERING_HARNESS.md`;
- `docs/engineering/DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `QUALITY_GATES.json`, `TRACEABILITY.md`, `WORKFLOW.md`, and `WORKFLOW.json`;
- release-record, verification-record, and work-order templates;
- root dashboard generator, Explorer template, inspector, and validator.

No other installer-owned path is permitted. Packet, context, `.gitattributes`, and retained HUP evidence are reviewed repository-owned additions outside the installer plan.

## Error and recovery behavior

Wrong identity, wrong prior lock, plan expansion, customization, conflict, evidence collision, failed write, failed postcondition, source mutation, or failing qualification stops. Recovery uses the installer's transaction snapshot or an separately reviewed Git revert; partial hand repair is prohibited.

## Compatibility and exit

After integration, ordinary complete-graph root evaluation replaces the managed 0.5 lane. Historical 0.5 artifacts and migration fixtures remain visible. Removing repository-specific transitional compatibility workflows is a separate reviewed cleanup.
