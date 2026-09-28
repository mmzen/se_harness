+++
id = "REQ-IAR-028"
type = "requirement"
title = "Retire compatibility guides without losing owner content"
status = "draft"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "New installations omit the six obsolete human-guide pointers; supported upgrades preserve existing owner files, and an explicitly authorized repository cleanup removes only reviewed stock pointers after current consumers no longer need them."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "2026-09-28 instruction reassessment, retirement findings, and the repository owner's request for an artifact-backed implementation plan; product-wide scope is proposed in DEC-IAR-002."

[relations]
derives_from = ["CAP-IAR-002"]
+++

# Retire compatibility guides without losing owner content

## In plain words

Agents use the current instruction collection. Older filenames remain only
where an existing installation or a supported old-release adapter still needs
them. An upgrade does not silently delete an owner's editable files.

## Why

The six files contain compatibility links, not unique current policy. Continuing
to generate them keeps obsolete entry points visible. Deleting existing copies
without checking consumers and ownership can break discovery or lose owner text.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Fresh installation of the future release | No OPERATING_CARD.md, DECISION_RIGHTS.md, QUALITY_GATES.md, WORKFLOW.md, TRACEABILITY.md or TECHNICAL_COMMUNICATION.md is generated under docs/engineering/. Current routes resolve. | Refuse an invalid instruction collection before apply. |
| Upgrade from the current instruction collection | Existing stock pointers and custom owner bytes remain intact; removed seeds do not reappear; the resulting lock and readiness checks agree. | Refuse unsafe or unsupported inputs without partial writes. |
| Supported older instruction migration | Recognized old full guides follow their accepted migration; customized content needs an explicit owner plan. | Refuse unsafe or ambiguous inputs without partial writes. |
| Separately authorized cleanup in an adopted repository | Only reviewed, unchanged stock pointers are removed, after consumer and replacement-route checks. | Keep a customized, ambiguous or still-required file and report the exact reason. |

## Acceptance

Use SPEC-IAR-015 and VER-IAR-017. Test fresh installs, retained stock pointers,
customized owner files, already removed files, invalid destinations and retry.
Keep machine policy, ARTIFACT_AUTHORING.md, historical evidence, migration
fingerprints and required version-conditioned adapters. A source grep alone
does not prove that the active plugin no longer reads a legacy path.

## Examples

### Normal

An owner upgrades a repository with an added paragraph in OPERATING_CARD.md.
The paragraph and the rest of that file remain byte-identical. A fresh repository
uses CONTINUE.md and receives no OPERATING_CARD.md.

### Failure

If the active skill still requests OPERATING_CARD.md, repository cleanup stops
before deleting it. This does not prevent independent reference corrections.
