+++
id = "ADR-AGR-001"
type = "adr"
title = "Extend existing provenance records with explicit aggregate scope"
status = "approved"
owners = ["technical-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-19"

[relations]
decides = ["ARCH-AGR-001"]
+++

# ADR: Extend existing provenance records with explicit aggregate scope

## Status

Accepted.

Reassessed on 2026-08-19 against `SPEC-EVK-001`. Exact keyed coverage now recognizes both governed layouts, while the selected aggregate record model, final-candidate identity, explicit scope, and accountable authority boundaries remain applicable.

## Context

The existing formal schema already defines work orders, verification contracts, evidence paths, verification records, and release records as list-valued relations. Only the preparation APIs and some consistency rules assume a single item. Normal versions require an explicit aggregate scope.

## Decision drivers

Preserve intent-to-commit lineage, verify final integration, avoid new overlapping concepts, remain backward-compatible, and keep release authority human-controlled.

## Considered options

1. Release only the latest work order. Rejected because it understates version scope.
2. Put every repository work order in a release contract. Rejected because `gates` is an allow-list and governance-only work is not payload.
3. Include historical verification records with different ancestor commits. Rejected because ancestry does not prove the final integrated candidate.
4. Add a new release-manifest artifact type. Rejected because existing record relations already express the required aggregate sets.
5. Extend current commands and consistency rules to support explicit sets at one final candidate commit. Selected.

## Decision

Use one aggregate verification record at the clean final release candidate. It enumerates all selected release-bearing work orders, the union of their declared verification contracts, and evidence for each. Use one release record with the same work set and commit. Accept multiple included verification records only when they share that exact candidate identity and their coverage union equals the released-work set.

Expose repeatable CLI options, keep single occurrences backward-compatible, and recommend release-centric record IDs. Governance-only work remains outside `releases_work` and may be retained in later commits.

## Consequences

Release lineage becomes complete and mechanically checkable. Final-candidate evidence must be assembled for every selected work item, adding deliberate release-qualification work. Historical VRECs at earlier commits remain useful history but cannot alone qualify a later integrated candidate. Existing records and installations remain valid.

## Validation

Automated tests must prove aggregate success, exact set and commit failure cases, single-item compatibility, deterministic rendering, safe upgrade, dashboard lineage, and absence of Git or authority mutations.
