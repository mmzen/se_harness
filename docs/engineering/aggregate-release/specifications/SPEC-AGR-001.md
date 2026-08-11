+++
id = "SPEC-AGR-001"
type = "specification"
title = "Aggregate verification and release manifests"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-AGR-001", "REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-004", "REQ-AGR-005", "REQ-AGR-006", "REQ-AGR-007", "REQ-AGR-008"]
+++

# Specification: Aggregate verification and release manifests

## Scope

Extend commit-bound provenance so a final software candidate and release version can explicitly cover multiple release-bearing work orders. Preserve the existing artifact types, ready-only preparation behavior, exact-commit rule, and single-work-order compatibility.

## Actors and external systems

Engineering owners identify implemented work. Quality owners select and assess verification coverage. Release owners select a release contract and authorize promotion. Git provides bounded candidate identity. The filesystem contains formal artifacts and retained evidence. No external service is required.

## Inputs

`capture-verification` accepts one or more occurrences of each of:

- `--work-order WO-nnn`;
- `--verification VER-nnn`;
- `--evidence docs/engineering/...`.

`prepare-release` accepts one or more occurrences of:

- `--work-order WO-nnn`;
- `--verification-record VREC-nnn`.

Existing scalar options, IDs, owner, version, tag, target, and output rules remain unchanged. A single occurrence preserves the existing workflow.

## Outputs

The commands write one `ready` Markdown record atomically. Aggregate values are emitted as lexicographically sorted TOML arrays with no duplicates:

```toml
[relations]
verifies_work_order = ["WO-A-001", "WO-B-001"]
conforms_to = ["VER-A-001", "VER-B-001"]
```

```toml
[relations]
satisfies = ["REL-PKG-001"]
includes_verification = ["VREC-PKG-001"]
releases_work = ["WO-A-001", "WO-B-001"]
```

## State model

1. Release-bearing work orders and their verification contracts are active.
2. Implementation and evidence are committed in one clean final candidate.
3. Aggregate verification is captured as `ready` against that candidate.
4. A later governance change records and, through accountable review, transitions the record to `verified`.
5. Aggregate release is prepared as `ready`, copying the exact candidate identity.
6. A later governance change records release-owner authorization and transitions the record to `released`.
7. Separately authorized operations may tag the candidate and publish artifacts built from it.

## Behavioral rules

1. Each repeatable collection must contain at least one value and must reject duplicate values.
2. All referenced IDs must exist, have the expected artifact type, and be in a lifecycle state accepted by the existing provenance workflow.
3. For multi-work-order aggregate verification, the selected verification-contract set must equal the union of `verification` relations declared by the selected work orders. A single-work-order record may retain the existing behavior of selecting a non-empty declared subset.
4. For a multi-work-order candidate, each selected work order must have at least one repository-contained retained evidence path keyed to that work-order ID. All listed evidence paths must exist and pass existing containment and symlink checks; the existing single-work-order path behavior remains compatible.
5. Aggregate verification uses one clean full `HEAD`, one Git object format, one timestamp, and one artifact snapshot hash for the complete set.
6. For aggregate release, the selected released-work set must equal the union of `verifies_work_order` relations from included verification records.
7. Every released work order must occur in the selected release contract's `gates` relation. A contract may gate additional work not selected for this instance.
8. Every included verification record must declare the same commit and object format. The release record copies those values.
9. A `released` record requires every included verification record to be `verified` or `released`.
10. Commands validate all inputs and repository cleanliness before creating output, refuse an existing destination, and leave Git state unchanged.
11. Record identifiers remain semantic labels only. Documentation recommends release-centric IDs such as `RLS-SEH-001`; suffix similarity to a work order has no implied relationship.

## Error and recovery behavior

Failures identify the duplicate, unknown, incorrectly typed, inactive, uncovered, extra, ungated, unsafe, missing, or commit-inconsistent values. No partial record remains. The operator corrects explicit inputs or governing artifacts and reruns from a clean worktree.

## Data and interface contracts

No new artifact type or metadata field is introduced. Existing list-valued fields become fully supported as non-empty sets. JSON dashboard output retains current fields and includes complete related-work-order lists for aggregate records.

## Security and privacy properties

All IDs and paths are explicit untrusted inputs. Existing path containment, regular-file, symlink, safe-destination, command timeout, and atomic non-overwrite controls remain mandatory. No artifact body is executed.

## Performance and capacity

Validation is linear in selected artifacts plus catalog lookup. A bounded repository-scale list is expected; no network access or unbounded subprocess is introduced.

## Observability

CLI success identifies the prepared record path and candidate commit. Deterministic diagnostics identify scope inconsistencies. Dashboard provenance exposes the version, commit, verification records, and complete work-order set.

## Compatibility and migration

One supplied value produces the current single-item relation arrays and behavior. Existing records remain valid. Canonical templates, installed scripts, workflow documentation, configuration hashes, and package data are upgraded through existing customization-preserving mechanisms.

## Examples and counterexamples

A valid aggregate candidate selects `WO-DST-001`, `WO-REV-001`, and `WO-DST-003`, the verification contracts declared by those work orders, and evidence for each, all against one clean final commit. A release record lists the same work set and includes verification bound to that commit.

An invalid candidate combines historical verification records naming different commits, adds a publication-only work order as payload, omits a selected work order from `releases_work`, or relies on Git ancestry instead of final-candidate evidence.

## Explicitly unspecified decisions

Internal collection helper names, exact diagnostic wording, line wrapping for generated arrays, and test fixture organization are delegated to implementation, provided output stays deterministic and requirements remain observable.
