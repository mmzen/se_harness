+++
id = "INT-WEX-001"
type = "intent"
title = "Make governed workflow execution deterministic across agents"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
+++

# Intent: Make governed workflow execution deterministic across agents

## Problem

Lifecycle behavior is split between formal artifacts, managed prose, direct file edits, and a small set of preparation commands. Given the same repository state and human instruction, different agents can therefore choose different working scopes, mutate related records differently, report unrelated findings as current work, or recommend different next actions. The harness validates many resulting states but does not yet provide one executable contract for calculating and applying lifecycle actions.

## Desired outcomes

- Given the same repository snapshot, selected lifecycle object, workflow phase, and explicit human decision, every supported agent receives the same bounded working set, permitted action, validation result, and next-step handoff.
- Lifecycle preparation and transitions fail without partial writes when their type-specific preconditions are not satisfied.
- Work execution, commit-bound assurance, and release authorization remain independently represented and never change merely because a related record changes state.
- Current-scope blockers remain prominent while unrelated repository maintenance observations remain visible without becoming actions for the selected scope.

## Actors and stakeholders

- Repository contributors and coding agents operate the workflow through provider-neutral harness behavior.
- Product and requirements owners decide the governed outcome and obligations.
- Technical and engineering owners decide implementation structure and bounded work authorization.
- Assurance and release owners retain exclusive authority for verification and release decisions.
- Repository owners bear compatibility and migration risk for historical artifacts and integrations.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Supported-agent conformance for identical workflow scenarios | Agent-dependent behavior is observed | 100% identical permitted action, mutation plan, validation outcome, and structured handoff | Each supported-agent acceptance run |
| Invalid preparation or transition scenarios that write any file | Possible through incomplete command preconditions or agent variation | 0 | Every automated boundary-test run |
| Related lifecycle records changed without an explicit selected transition | Agent-dependent | 0 | Every lifecycle transition test and review |
| Unrelated background findings presented as selected-scope actions | Global inspection does not distinguish a selected scope | 0 | Every scoped inspection acceptance scenario |

## Non-goals

- It does not grant approval, verification, release, risk-acceptance, commit, push, tag, publication, deployment, or operational authority.
- It does not replace the formal artifact graph with agent memory, prompt text, a Skill, or generated output.
- It does not automatically migrate or reinterpret historical lifecycle records.
- It does not make all repository findings part of one selected work scope.
- It does not compare candidate changes to a trusted Git base or enforce direct lifecycle edits in this stage.
- It does not prescribe a provider-specific conversational style beyond the canonical workflow result.

## Principles and immutable constraints

- Accountable human decisions remain distinct from deterministic mechanical execution.
- Formal TOML metadata and typed relations remain the authority source; projections and handoffs are derived evidence.
- A failed operation leaves the repository without partial lifecycle writes.
- The same explicit inputs against the same trusted state produce the same result independently of agent host.
- A lifecycle mutation changes only its declared target and permitted fields; related state changes require separate explicit transitions.
- Python 3.11+ standard-library runtime behavior and the single standard installation are preserved.

## Risks and assumptions

- **Fact:** current preparation commands and validation rules admit some states broader than the normal workflow describes.
- **Fact:** current inspection is repository-wide and has no selected-work-order scope.
- **Fact:** conversational handoff fields exist, but no provider-neutral machine-readable workflow handoff currently governs agent output.
- **Assumption:** supported agents can converge when authoritative action calculation and rendering inputs come from the same CLI contract.
- **Risk:** tightening lifecycle rules can expose legacy records or external integrations that depend on permissive behavior; compatibility must be explicit and tested.
- **Risk:** direct edits outside the governed commands remain dependent on snapshot validation until separately governed transition-diff enforcement is proposed.
- **Open decision:** the technical design must decide whether transition application and scoped projection are one command family or separate interfaces.
