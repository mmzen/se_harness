+++
id = "SPEC-VSP-001"
type = "specification"
title = "Verification-record supersession contract"
status = "implemented"
owners = ["technical-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
+++

# Specification: Verification-record supersession contract

## Scope

Extend the existing `verification_record` lifecycle with explicit retirement of a `ready` record in favor of one authoritative verified or released record. Preserve the existing artifact type, commit-bound metadata, capture behavior, human decision rights, and installed-repository compatibility.

## Actors and external systems

Assurance owners authorize transitions. Release owners consume eligible verification. Repository owners retain governance history. The validator checks authored metadata. The dashboard and Explorer project derived state. Git supports governance diff review but is not used to infer authority. No external service is required.

## Inputs

A superseded VREC retains its existing metadata and adds:

```toml
status = "superseded"
superseded_at = "2026-08-11T12:00:00Z"
supersession_authorized_by = "repository-owner"

[relations]
verifies_work_order = ["WO-AGR-001"]
conforms_to = ["VER-AGR-001"]
superseded_by = ["VREC-PMI-001"]
```

The transition also retains a narrative decision note and evidence keyed to its separate governance work order. There is no automated status-transition command in scope.

## Outputs

Validation emits deterministic pass or blocking diagnostics for lifecycle, required fields, relation cardinality, target type and status, coverage, cycles, active-release references, evidence, and provenance shape. Dashboard JSON exposes `superseded_at`, `supersession_authorized_by`, `superseded_by`, and derived inverse `supersedes`. Explorer renders the historical edge and active/historical classification.

## State model

1. A captured VREC is `ready` and remains a possible assurance decision.
2. A distinct VREC becomes `verified` or `released` through existing accountable governance.
3. An assurance owner may determine that the ready VREC is obsolete and authorize `ready -> superseded`.
4. The governance change adds the successor relation, timestamp, authorizer, decision note, and separate work-order evidence while preserving captured provenance.
5. `superseded` is terminal in this iteration and never satisfies verification or release readiness.

No automatic transition occurs when step 2 happens. `verified` and `released` VRECs cannot enter supersession under this packet.

## Behavioral rules

1. Verification-record statuses accepted by formal validation are `ready`, `verified`, `released`, and `superseded`.
2. A `superseded` VREC must have exactly one non-empty `superseded_by` target, one valid UTC `superseded_at`, and one non-empty `supersession_authorized_by` value.
3. A VREC not in `superseded` status must not declare supersession-specific fields or relations.
4. The successor must exist, be a distinct `verification_record`, and have status `verified` or `released`.
5. The successor's `verifies_work_order` set must be a superset of the source set. Additional work orders and verification contracts are allowed.
6. Supersession edges must be acyclic. Diagnostics list the deterministic affected record IDs.
7. A VREC referenced by a `ready` or `released` release record cannot transition to `superseded`; the release lifecycle must be resolved separately.
8. `prepare-release` and release-record validation never treat a superseded VREC as eligible or as verification coverage.
9. Captured `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, `evidence_paths`, `verifies_work_order`, and `conforms_to` remain unchanged during transition. Governance review compares the bounded diff because current-state validation cannot reconstruct unretained prior bytes.
10. The dashboard retains superseded records in revision history, exposes their explicit successor, excludes them from active-ready and verified-coverage calculations, and never treats them as a checkout anomaly solely because their candidate differs from HEAD.
11. For each `ready` VREC, the dashboard finds other `verified` or `released` VRECs whose work-order sets are supersets. When at least one exists and no explicit supersession is present, it emits derived warning `W-REV-004` with all possible successors; it does not select one.
12. Existing records without supersession metadata preserve current semantics and validation behavior.

## Error and recovery behavior

Malformed or unauthorized shapes fail without mutation and identify the source, target, and violated invariant. The operator restores `ready`, corrects metadata, resolves release references, or obtains a separate governance decision. No tool edits Git history or substitutes a successor automatically.

## Data and interface contracts

`superseded_by` is a one-element relation array so it participates in the existing graph. `superseded_at` uses the existing UTC timestamp grammar. `supersession_authorized_by` uses the bounded non-empty actor identifier rules applied to other authority fields. Dashboard schema additions are backward-compatible optional fields.

## Security and privacy properties

Artifact fields are untrusted. IDs are resolved through the typed catalog; cycles and duplicate targets fail; bodies are never executed. Diagnostics expose IDs and paths, not evidence bodies or secrets. Automation cannot manufacture the authority decision.

## Performance and capacity

Successor validation uses catalog lookups and bounded set comparisons. Cycle detection is linear in VRECs plus supersession edges. Stale-ready analysis is acceptable as a deterministic pairwise comparison for repository-scale artifact counts; implementation may index work sets without changing semantics.

## Observability

JSON and Explorer show source status, immutable candidate, successor status and candidate, shared and additional work coverage, authorizer, timestamp, and whether the relation is valid. Findings distinguish blocking explicit-relation errors from non-authoritative stale-ready warnings.

## Compatibility and migration

No existing record changes automatically. Existing VRECs remain valid. Canonical validator, dashboard, Explorer template, workflow, traceability guidance, VREC template, lock hashes, tests, and package data update through the single customization-preserving installation. The known `VREC-AGR-001` transition occurs only after feature deployment and a separate authorized governance work order.

## Examples and counterexamples

Valid: `VREC-AGR-001` remains bound to `3f3ba521...`, becomes `superseded`, and names verified `VREC-PMI-001`, whose work set includes `WO-AGR-001`.

Invalid: deleting `VREC-AGR-001`; marking it verified; naming a ready successor; omitting `WO-AGR-001` from the successor; changing the old commit; creating a cycle; or automatically transitioning it because a dashboard heuristic found overlap.

## Explicitly unspecified decisions

Internal graph helper names, diagnostic sentence wording, Explorer layout details, index implementation, and test-fixture organization are delegated to implementation provided IDs, severity, authority labels, and normative behavior remain stable.
