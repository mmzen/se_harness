# Engineering Harness for se_harness

This repository uses SE Harness 0.6.0.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in BCP 14
(RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## Goals

This harness makes engineering authority explicit, limits execution to approved
scope, binds assurance and release claims to exact evidence, and gives every
actor the same deterministic next step. These goals are informative; the rules
below and the routed policies are normative.

## Global invariants

`HRN-001` - Formal artifacts under `docs/engineering/` are the repository-native
source of product intent, requirements, architecture decisions, work authority,
verification contracts, assurance decisions, and release decisions. Code,
tests, commits, tickets, dashboards, and conversation text are evidence or
observations; they MUST NOT substitute for formal authority.

`HRN-002` - Repository facts and commands belong in the owner-controlled region
of `AGENTS.md`. That content is repository-owned and MUST NOT grant product,
engineering, assurance, release, or external-action authority. This harness does
not scaffold, track, or require it.

`HRN-003` - An actor MUST select one bounded artifact scope before acting. It
MUST NOT report findings from unrelated work orders as findings of the selected
scope. A discovered issue outside scope MAY be identified only as an unassessed
observation with its artifact ID, and MUST NOT block the selected work unless a
declared dependency or gate connects it.

`HRN-004` - Only `harnessctl` MAY compute lifecycle legality and the canonical
next action. Agent prose, prompts, Skills, dashboards, and repository notes MAY
render or invoke that result and MUST NOT redefine it.

`HRN-005` - Preparation, inspection, validation, and evidence capture MUST NOT
exercise a decision right. A state change requires the exact artifact, target
state, accountable actor, passing gates, and an explicit applied transition.

`HRN-006` - A transition MUST change only the artifacts explicitly selected by
the accountable actor. Related artifact states MUST NOT be synchronized by
inference.

`HRN-007` - Repository-owned instructions MAY add stricter local constraints.
They MUST NOT waive, weaken, or contradict this managed contract.

`HRN-008` - Managed integrity, graph validation, scope validation, and required
gates MUST fail closed. A warning MUST NOT be treated as approval or accepted
risk.

## Routing

Each subject has one policy owner. Other documents MUST reference the owner and
MUST NOT restate its rules.

| Subject | Normative owner |
| --- | --- |
| Lifecycle states, transitions, procedures, next actions, and handoff fields | `docs/engineering/WORKFLOW.md` and its machine-readable `WORKFLOW.json` |
| Roles, accountabilities, delegation, and reserved decisions | `docs/engineering/DECISION_RIGHTS.md` |
| Gate criteria, executable predicates, validation planes, pass/fail behavior, and exceptions | `docs/engineering/QUALITY_GATES.md` and `docs/engineering/QUALITY_GATES.json` |
| Normative chain, artifact applicability, relation types, and coverage | `docs/engineering/TRACEABILITY.md` |
| Artifact authoring locations and templates | `docs/engineering/templates/README.md` |
| Repository-specific facts and commands | the owner-controlled region of `AGENTS.md` |

`docs/engineering/README.md` is an index. It MUST NOT become a second policy
source.

## Lifecycle restitution

After completing a lifecycle stage or reaching a stop condition, the actor MUST
return the canonical human block produced by selected `harnessctl check`,
`harnessctl focus --result-schema 2`, or another workflow command using
`--result-schema 2`. The headings are `Outcome`, `Done`,
`Not done`, conditional `Blocked by`, `Current lifecycle state`, `Decision
required`, `Next`, `Command or response`, and conditional `Alternatives`.

The actor MUST return that block verbatim, use actual artifact IDs, expose one
typed next step, report only effects that occurred, and preserve every stated
non-effect. It MUST NOT add a preface, conclusion, unrelated finding,
open-ended question, or second next action. The complete procedure is
`WORKFLOW.md#lifecycle-restitution-procedure`.

## Stop conditions

The actor MUST stop before changing state or scope when any of these conditions
is true:

- managed integrity fails;
- the formal graph is invalid;
- no phase-eligible selected work order exists;
- a required governing artifact or gate is missing;
- a required check fails;
- owner instructions conflict with this contract;
- remediation would exceed the selected work order; or
- the requested action lacks the decision right or explicit authority defined
  by the routed policies.

The actor MUST report the failing rule or gate, the unchanged lifecycle state,
and one exact retry or accountable escalation. It MUST NOT ask an open-ended
next-action question when `harnessctl` provides a canonical recommendation.
