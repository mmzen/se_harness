+++
id = "SPEC-PLG-001"
type = "specification"
title = "Shared native plugin package assembly"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Both host packages carry the same selected published evaluator wheel and shared assets, with host-specific integration files and no Python runtime."

[relations]
specifies = ["REQ-PLG-001", "REQ-PLG-002"]
+++

# Specification: Shared native plugin package assembly

## In plain words

Build the two host packages from one shared source. Include the released checking tool without rebuilding it.

## Scope

This contract governs package assembly. SPEC-PLG-002 owns environment creation; SPEC-PLG-005 and SPEC-PLG-006 own host integration.

## Terms

- **Shared assets.** The versioned scripts, skills, and optional helper definitions shared by both hosts.

## Rules

**PLG-PKG-001.** Assembly MUST select one published evaluator wheel by immutable release reference and independently obtained expected SHA-256.

**PLG-PKG-002.** Assembly MUST verify the wheel digest before copying its unchanged bytes into each output's `packages/` directory.

**PLG-PKG-003.** Outputs MUST exclude Python runtimes, candidate evaluator builds, downloaded dependencies, and top-level `bin/` directories.

**PLG-PKG-004.** Both outputs MUST derive shared components from one source revision and use the same verified evaluator wheel.

**PLG-PKG-005.** Assembly MUST combine shared assets with only the selected host's manifest and integration files.

**PLG-PKG-006.** Each output MUST inventory its source revision, evaluator version, archive SHA-256, canonical payload SHA-256 computed from the verified wheel, and packaged file digests.

**PLG-PKG-007.** Assembly MUST refuse conflicting paths, escaped destinations, and incomplete inventories before marking an output usable.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Wheel differs or is absent | Refuse assembly | Nonzero result with the failed input |
| Shared assets disagree | Refuse acceptance of both outputs | Inventory mismatch |
| Destination escapes output | Refuse the write | Unsafe destination |

## Examples

**Given** one verified wheel, **when** both packages are assembled, **then** their shared file digests agree under PLG-PKG-004.

**Given** changed wheel bytes, **when** assembly starts, **then** PLG-PKG-002 prevents a usable output.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-001` | PLG-PKG-001, PLG-PKG-002, PLG-PKG-003 |
| `REQ-PLG-002` | PLG-PKG-004, PLG-PKG-005, PLG-PKG-006, PLG-PKG-007 |

## Not decided here

- Archive filenames and compression settings.
- Public release approval or marketplace publication.
- The host support matrix established by later compatibility decisions.
