+++
id = "VER-VSP-001"
type = "verification"
title = "Verify verification-record supersession"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
+++

# Verification Contract: Verify verification-record supersession

## Independence

Temporary artifact repositories construct VREC and RLS graphs directly from the normative metadata contract. Expected lifecycle, set, cycle, release, and dashboard results are asserted without calling production helpers to derive expected values. Governance-diff review separately checks historical field preservation.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-VSP-001 | validator matrix | ready source, authorized superseded source, invalid source states | only the governed ready-to-superseded shape passes; no automatic mutation occurs |
| REQ-VSP-002 | type and cardinality tests | absent, empty, duplicate, multiple, unknown, wrong-type, self, ineligible and eligible targets | exactly one distinct verified or released VREC is accepted |
| REQ-VSP-003 | set and graph tests | equal, superset, subset, disjoint, self-loop, two-node and long cycle | coverage is never lost and every cycle is rejected deterministically |
| REQ-VSP-004 | transition-diff review | old and changed VREC plus governance evidence | only permitted lifecycle fields, relation, and narrative change; captured provenance is identical |
| REQ-VSP-005 | provenance CLI and validator | prepare-release selection, ready/released RLS back-reference, unreferenced source | superseded records never qualify and active release references block transition |
| REQ-VSP-006 | JSON, finding and Explorer snapshots | stale ready, explicit successor, extra successor work, multiple possible successors | warning is derived, explicit lineage is readable, and historical records do not satisfy active gates |
| REQ-VSP-007 | regression and distribution | existing records, init/adopt/upgrade, customization, wheel and fresh install | behavior remains compatible and one standard installation carries source-equivalent semantics |

## Acceptance scenarios

The scenarios in `acceptance/verification-supersession.feature` are the minimum public behavior contract.

## Property and invariant tests

- Supersession never reduces the source work-order set.
- No supersession graph contains a directed cycle.
- Every superseded VREC has exactly one eligible terminal successor.
- Input or artifact ordering does not change diagnostics, JSON, or rendered edges.
- Superseded records never contribute verified or release-ready coverage.
- Stale-ready analysis never changes repository files or status.
- Existing VREC graphs without supersession metadata preserve their previous result.

## Static and architecture checks

Confirm the validator owns normative graph validation, provenance preparation only reads eligible status, dashboard logic remains derived, and Explorer remains presentation-only. Confirm source/canonical parity for validator, dashboard, HTML template, workflow, traceability, and VREC template.

## Security and privacy checks

Exercise malicious IDs, duplicate keys, wrong artifact types, missing targets, cycles, oversized bounded graphs, invalid timestamps, control characters in authorizer fields, symlinked artifacts and evidence, and malicious-looking bodies. No body executes and diagnostics reveal no evidence contents.

## Performance and resilience checks

Validate a bounded large acyclic chain and a large stale-ready set deterministically without network access. Failed validation, dashboard generation, and upgrade leave no partial authoritative artifacts.

## Manual assessments

Review the Explorer at desktop and narrow widths. Confirm active, verified, and historical records are distinguishable; arrows read old-to-new; extra successor coverage is understandable; warnings clearly say derived and require human decision.

## Evidence retention

Retain exact commands, test counts, requirement matrix, graph fixtures, diagnostics, JSON snapshots, screenshots or visual observations, source/canonical parity, wheel hash and contents, fresh-install results, deviations, and residual risks in `docs/engineering/verification-supersession/evidence/WO-VSP-001-verification.md`.

## Residual uncertainty

The harness cannot determine whether overlapping coverage expresses the owner's intended successor. Current-state validation cannot independently reconstruct unretained prior VREC bytes, so human authorization and governance-diff evidence remain necessary.
