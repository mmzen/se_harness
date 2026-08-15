+++
id = "SPEC-IAR-009"
type = "specification"
title = "Deterministic inspection suggestion projection"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-IAR-017"]
+++

# Specification: Deterministic inspection suggestion projection

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `ok i approve` as part of the complete `IAR-009` packet.

## Scope

Extend the uncommitted first `harnessctl inspect` candidate with deterministic, non-authoritative next-step suggestions. Suggestions are a presentation projection over existing queue action classes and selected existing Harness Explorer warning rule IDs. They add no validation rule, finding rule, eligibility check, or remediation command.

Because `IAR-008` and this packet will first be assessed at the same candidate commit, the additive suggestion field remains part of `se-harness-inspection-v1`. Before implementation, `REQ-IAR-016` and `SPEC-IAR-008` must be amended to distinguish this governed structured guidance from the free-form or automatic recommendations that remain prohibited.

## JSON contract

The inspection report gains a top-level `suggestions` array. Each entry contains exactly these public fields:

- `source_kind`: `queue` or `finding`;
- `source_id`: the queue name for a queue entry or the existing finding rule ID for a finding;
- `subjects`: sorted unique artifact IDs copied from the source observation;
- `action`: one stable catalog action class;
- `message`: static catalog guidance with only escaped subject IDs substituted;
- `accountable_role`: one role from the managed decision-rights vocabulary;
- `automatic`: always `false`.

No suggestion contains a command, path assembled from repository input, requested target status, confidence value, deadline, score, or URL.

## Source rules

1. A queue suggestion is emitted for each existing `decision_required`, `definition_pending`, or `active_work` entry by looking up that entry's existing mechanical action class.
2. A finding suggestion is emitted only for warning findings whose rule is explicitly present in the catalog below.
3. Validator-authority findings, informational findings, and unknown rule IDs remain fully visible in `findings` but emit no suggestion.
4. Suggestion selection never reads artifact title, prose body, owner text, path text, evidence text, or finding message.
5. Suggestions neither replace nor annotate the source finding. Existing rule, severity, authority, message, artifacts, paths, evidence, ordering, and counts remain unchanged.
6. JSON suggestions sort by source kind, source ID, action, subjects, accountable role, and message.
7. Human output groups repeated suggestions by source ID, action, and accountable role, lists bounded subject IDs, and labels the section `Suggested next steps`.

## Closed catalog

### Existing queue action classes

| Source action class | Suggestion action | Accountable role | Guidance intent |
| --- | --- | --- | --- |
| `assurance-review` | `review-assurance-decision` | `assurance-owner` | Review retained evidence and record or withhold the accountable verification decision. |
| `release-review` | `review-release-decision` | `release-owner` | Review the verified candidate and release controls and record or withhold the release decision. |
| `accountable-review` | `review-accountable-decision` | `artifact-owner` | Identify the accountable owner and review the ready artifact without assuming an outcome. |
| `complete-definition` | `complete-or-dispose-definition` | `artifact-owner` | Complete the definition or explicitly dispose of it through an allowed governed state. |
| `start-authorized-work` | `start-bounded-work` | `engineering-owner` | Run start preflight and begin only the approved scope. |
| `continue-authorized-work` | `continue-bounded-work` | `engineering-owner` | Continue only the authorized scope and retain work-order-keyed evidence. |

### Existing actionable derived warning rules

| Rule | Suggestion action | Accountable role | Guidance intent |
| --- | --- | --- | --- |
| `W-HEX-001` | `retain-work-order-evidence` | `engineering-owner` | Retain evidence keyed to the implemented work order and reassess the observation. |
| `W-HEX-002` | `review-governing-scope` | `engineering-owner` | Review inactive governing references before continuing active work. |
| `W-HEX-003` | `reassess-dependent-artifact` | `artifact-owner` | Reassess the older source against its newer declared dependency or parent. |
| `W-HEX-004` | `review-relation-cycle` | `technical-owner` | Determine whether the declared cycle is intentional and correct unintended edges through governed work. |
| `W-HEX-005` | `review-unlinked-artifact` | `artifact-owner` | Declare the applicable relation or explicitly dispose of an artifact that is no longer applicable. |
| `W-HEX-006` | `deduplicate-relation` | `artifact-owner` | Remove an unintended repeated relation through governed work. |
| `W-REV-002` | `review-release-provenance` | `release-owner` | Reconcile the released work claim with an eligible commit-bound release record. |
| `W-REV-003` | `restore-candidate-availability` | `repository-owner` | Make the declared candidate commit available for assessment without changing its recorded identity. |
| `W-REV-004` | `review-verification-supersession` | `assurance-owner` | Assess explicit supersession against one eligible verified or released successor; do not transition automatically. |

Catalog text is implementation-owned static text, not artifact-controlled input. Adding, removing, or changing a catalog trigger or its authority meaning requires governed specification and verification updates.

## Compatibility and failure behavior

- The existing inspection schema identifier, authority, producer, validation summary, counts, queues, and findings remain present and compatible.
- Empty or unsupported guidance produces an empty `suggestions` array, not an error.
- Malformed source data continues to fail through the existing inspection boundary.
- Successfully rendering suggestions does not affect exit status.
- Human and JSON escaping, determinism, no-write behavior, Python 3.11+ support, root/canonical parity, and standard installation remain mandatory.

## Explicitly unspecified decisions

Exact human spacing, bounded subject display count, and internal catalog representation may be selected during implementation. Free-form advice, model calls, plugin calls, command execution, interactive remediation, policy configuration, and new finding semantics are not delegated choices.
