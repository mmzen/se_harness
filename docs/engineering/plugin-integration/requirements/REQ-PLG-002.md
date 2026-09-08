+++
id = "REQ-PLG-002"
type = "requirement"
title = "Assemble both host packages from shared sources"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN supported host packages are assembled, THE PACKAGER SHALL produce Codex and Claude Code packages from one versioned set of evaluator and shared assets."
verification_method = ["test","inspection"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Assemble both host packages from shared sources

## In plain words

Both coding tools receive the same checking tool and shared instructions. Only their integration files differ.

## Why

Separate source copies can drift and make one host follow different rules.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Assembly of Codex and Claude Code packages | Shared files and evaluator identity agree across both outputs. | Refuse an output assembled from a different or incomplete source set. |

## Examples

### Normal

**Given** one selected source revision.

**When** both packages are assembled.

**Then** their shared files and wheel have matching digests.

### Failure

**Given** different shared instruction copies in the two outputs.

**When** package contents are checked.

**Then** the mismatch blocks acceptance.
