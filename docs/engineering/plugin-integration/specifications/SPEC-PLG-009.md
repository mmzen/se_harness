+++
id = "SPEC-PLG-009"
type = "specification"
title = "Repository connection and compatible skill discovery"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Repository connection uses the reviewed released installer operation and becomes ready only when overlapping skills have a supported, ownership-compatible resolution."

[relations]
specifies = ["REQ-PLG-015", "REQ-PLG-016"]
+++

# Specification: Repository connection and compatible skill discovery

## In plain words

Setup connects the repository without replacing its installer or guessing which skill copy should win.

## Scope

Governs the repository procedures of `setup`. Runtime creation belongs to SPEC-PLG-002; existing installer ownership rules and [SPEC-AEX-005](../../agentic-execution/specifications/SPEC-AEX-005.md) remain authoritative.

## Terms

- **Discovery ready.** The host selects one approved, compatible implementation for each overlapping skill name.

## Rules

**PLG-REPO-001.** Setup MUST inspect the selected released CLI and use its real installation or upgrade preview and application forms for the reviewed target.

**PLG-REPO-002.** Setup MUST apply only the still-authorized reviewed operation and verify its actual result through existing installer and integrity checks.

**PLG-REPO-003.** Setup MUST preserve owner content, customized managed files, and repository version locks except where the existing authorized installer operation explicitly changes them.

**PLG-REPO-004.** Overlapping skills MUST have one active implementation through the approved compatibility choice and supported host and installer behavior.

**PLG-REPO-005.** While DEC-PLG-004 remains unresolved or its supported route is unavailable, setup MUST keep discovery unready without editing or deleting locked skill copies.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Installer conflict or changed reviewed operation | Preserve affected files; report the blocker. | Existing installer finding |
| Duplicate skills lack an approved compatible route | Keep discovery unready; retain existing files. | DEC-PLG-004 |

## Examples

**Given** a managed repository-local skill, **when** plugin discovery exposes another copy without a supported migration, **then** PLG-REPO-005 blocks readiness rather than deleting either owned file.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-015` | PLG-REPO-001, PLG-REPO-002, PLG-REPO-003 |
| `REQ-PLG-016` | PLG-REPO-004, PLG-REPO-005 |

## Not decided here

- DEC-PLG-004 decides compatibility with existing repository-local skill contracts.
- Core installer changes require separate governed work and a released evaluator.
