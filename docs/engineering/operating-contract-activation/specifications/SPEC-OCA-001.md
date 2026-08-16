+++
id = "SPEC-OCA-001"
type = "specification"
title = "Six-contract accountable activation"
status = "implemented"
owners = ["service-owner", "technical-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-OCA-001"]
+++

# Specification: Six-contract accountable activation

## Scope

Activate exactly the six existing contracts below after normalizing their traceability and operating content. Correct the managed operating-contract template example so future authoring uses the same relation model.

## Contract scope matrix

| Contract | Required `assures` targets |
| --- | --- |
| `OPS-AGR-001` | `REQ-AGR-001` through `REQ-AGR-008` |
| `OPS-IAR-001` | `REQ-IAR-001` through `REQ-IAR-018` |
| `OPS-PMI-001` | `REQ-PMI-001` through `REQ-PMI-007` |
| `OPS-PYP-001` | `REQ-PYP-001` through `REQ-PYP-005` |
| `OPS-VSP-001` | `REQ-VSP-001` through `REQ-VSP-007` |
| `OPS-WLC-001` | `REQ-WLC-001` through `REQ-WLC-006` |

## Behavioral rules

1. Each listed contract becomes `approved` only after all rules in this specification pass.
2. `assures` contains exactly the matrix targets, in deterministic numeric order, and contains no `REL-*` target.
3. Each contract contains the canonical nine operating sections and uses current repository commands, paths, roles, and boundaries.
4. Objectives describe observable repository or publication outcomes; they do not claim an always-on external service.
5. Alerts distinguish release-blocking failures from review prompts where the governed behavior makes that distinction.
6. Backup and recovery preserve immutable Git and external publication history; no procedure rewrites a published decision.
7. Automated remediation is explicitly bounded away from accountable transitions and external publication authority.
8. The six domain indexes state that the operating contract is approved independently from the draft release contract.
9. Both canonical and installed `OPERATING_CONTRACT.template.md` examples use `assures = ["REQ-xxx"]`; managed integrity metadata is synchronized through the supported upgrade path.
10. No release contract, release record, runtime validator rule, CLI behavior, version, or historical commit-bound record changes.

## Error and recovery behavior

If a contract cannot meet the matrix or canonical sections without changing software, leave that contract `draft`, record the reason, and split the behavior into a separately authorized work order. If managed synchronization reports a conflict, stop without overwriting owner-controlled content.

## Observability

- Formal validation must report zero errors.
- `harnessctl inspect .` must reduce `definition_pending` by exactly six, leaving the six draft release contracts.
- `harnessctl doctor .` must pass managed integrity after synchronization.
- Diff inspection must show no release artifact or executable source change.

## Compatibility and migration

Existing active repository data needs no migration. New and upgraded installations receive the corrected authoring example. The validator's present permissive target-type behavior remains compatible and is explicitly not changed here.

## Explicitly unspecified decisions

Future release-contract disposition, validator target-type enforcement, configurable operating profiles, external monitoring, and automated remediation remain outside this work order.
