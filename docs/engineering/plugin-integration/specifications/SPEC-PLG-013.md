+++
id = "SPEC-PLG-013"
type = "specification"
title = "Fresh repair and explicit repository upgrade"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Maintenance verifies a fresh environment before switching selection and preserves repository authority unless an explicitly authorized existing upgrade changes it."

[relations]
specifies = ["REQ-PLG-022", "REQ-PLG-023"]
+++

# Specification: Fresh repair and explicit repository upgrade

## In plain words

Repair makes a clean replacement. Updating plugin files alone never updates project rules.

## Scope

Setup maintenance instructions. SPEC-PLG-001 supplies trusted package inputs; SPEC-PLG-002 defines setup identity and plugin readiness.

## Terms

- **Active selection.** The verified environment currently selected for this installation.

## Rules

**PLG-MNT-001.** Repair MUST discover provided Python through the host shell before Python-dependent checks; missing Python requires operator repair, never automatic interpreter download.

**PLG-MNT-002.** Setup MUST create an empty isolated replacement outside the repository and install only the verified bundled wheel with --no-index --no-deps.

**PLG-MNT-003.** Active selection MUST change only after SPEC-PLG-002's identity and readiness checks pass; failure MUST preserve any usable previous selection.

**PLG-MNT-004.** Maintenance MUST use absolute isolated Python, cleared PYTHONPATH and controlled subprocess PATH without importing repository code.

**PLG-MNT-005.** Plugin update, repair and removal MUST preserve repository locks, owned content and historical governance evidence.

**PLG-MNT-006.** Repository version changes MUST follow explicitly authorized existing upgrade preview and apply; incompatible ordinary use MUST stop.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Replacement identity failure | Keep previous selection; reject replacement | Existing identity result or missing/mismatched archive |
| Installer conflict | Preserve repository | Existing installer refusal |

## Examples

**Given** a working environment, **when** replacement archive metadata is absent, **then** PLG-MNT-003 keeps the working selection.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-022` | PLG-MNT-001, PLG-MNT-002, PLG-MNT-003, PLG-MNT-004 |
| `REQ-PLG-023` | PLG-MNT-005, PLG-MNT-006 |

## Not decided here

- Host plugin installation/removal mechanisms.
- No runtime manager or interpreter installer.
