+++
id = "REQ-DST-035"
type = "requirement"
title = "Keep the Explorer overview concise"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN Harness Explorer renders the Overview, THE SYSTEM SHALL summarize definition coverage without presenting an exhaustive requirement-by-requirement coverage listing, while preserving the underlying coverage evidence and artifact-level inspection paths."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep the Explorer overview concise

## Rationale

The current Definition Coverage table grows with every active requirement. In a realistic repository it dominates the Overview, duplicates information available through metrics and artifact inspection, and makes the topology and actionable state harder to reach.

Removing visual repetition must not remove assessable evidence. Definition coverage remains a canonical snapshot concept and must stay distinct from commit-bound VREC assurance.

## Required response

- Remove the exhaustive Definition Coverage table from the Overview page.
- Retain the compact active-coverage metric, including total, specified, and verification-contract-covered counts.
- Retain canonical `coverage` data unchanged in `harness-dashboard-snapshot-v1` and `dashboard-data.json`.
- Retain artifact-level definition-coverage labels and the ability to locate a requirement through graph search and focused lineage.
- Preserve missing, partial, and complete coverage distinctions without introducing a score or implying verification.
- Do not replace the table with another unbounded list on the Overview.

## Acceptance examples

### Large covered repository

**Given** a repository contains many active requirements

**When** the Overview renders

**Then** it shows the compact coverage metric and no exhaustive coverage table.

### Requirement inspection

**Given** a reader searches for one requirement and opens its focused lineage

**When** its detail is inspected

**Then** the reader can still distinguish definition covered, specification only, definition gap, or not applicable from canonical data.

### Authority boundary

**Given** every active requirement has a specification and verification contract

**When** the coverage metric is complete

**Then** the interface does not label the repository verified, released, compliant, or healthy.

## Out of scope

This requirement does not change coverage computation, active-coverage policy, canonical snapshot fields, validation, commit-bound verification, readiness gates, or lifecycle authority.
