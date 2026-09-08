+++
id = "SPEC-PLG-016"
type = "specification"
title = "Truthful released installation guidance"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Public onboarding accurately describes an available released plugin, including supplied Python, setup effects, activation evidence and current limitations."

[relations]
specifies = ["REQ-PLG-027"]
+++

# Specification: Truthful released installation guidance

## In plain words

The installation page shows what people can install today. Planned commands remain clearly marked as future work.

## Scope

This contract governs the focused installation guide. DEC-PLG-003 resolves its relationship to existing approved installation guidance before this work order proceeds.

## Terms

- **Available route.** Published commands and versions usable under the claimed support conditions.

## Rules

**PLG-DOC-001.** The guide MUST name the available release and host installation route without presenting proposed packages or commands as published.

**PLG-DOC-002.** The guide MUST require provided Python 3.11 or newer with usable venv and ensurepip, directing missing-Python users to install it before continuing.

**PLG-DOC-003.** Setup instructions MUST explain automatic isolated environment creation and offline wheel installation without user environment activation or global package installation.

**PLG-DOC-004.** The guide MUST distinguish downloaded files, successful setup and observed hook activation; missing observations remain unconfirmed.

**PLG-DOC-005.** The guide MUST state evaluator compatibility, supported hosts, maintenance recovery and the independent authority limits of local hooks.

**PLG-DOC-006.** Public onboarding changes MUST wait for DEC-PLG-003 and an available qualified release; prospective drafts MUST remain labelled prospective.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Unavailable release, missing Python, or unobserved activation | Identify the incomplete step without claiming readiness. | unavailable release or incomplete setup |

## Examples

**Given** downloaded plugin files and missing Python, **when** setup is followed, **then** plugin use stops pending supplied Python (PLG-DOC-002, PLG-DOC-004).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-027` | PLG-DOC-001, PLG-DOC-002, PLG-DOC-003, PLG-DOC-004, PLG-DOC-005, PLG-DOC-006 |

## Not decided here

- Existing approved installation artifacts need separate authorized disposition.
- README replacement and publication actions.
