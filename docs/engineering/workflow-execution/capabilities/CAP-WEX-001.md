+++
id = "CAP-WEX-001"
type = "capability"
title = "Operate one governed lifecycle scope predictably"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
derives_from = ["INT-WEX-001"]
+++

# Capability: Operate one governed lifecycle scope predictably

## Actor and need

## Capability statement

An authorized operator can select one formal lifecycle object, obtain its bounded governed context and legal next actions, apply an explicitly authorized mechanical transition atomically, validate the resulting change, and receive a canonical handoff under the repository's existing decision-rights policy.

## Boundaries

## Outcomes

## Candidate requirements
Repository contributors, accountable owners, and coding agents need one provider-neutral way to calculate the scope, legality, effect, and next authorized step of a workflow action without delegating governance decisions to automation.
- The capability calculates and validates actions but does not make accountable product, architecture, assurance, release, risk, or operational decisions.
- It does not expand the selected working scope without an explicit operator request.
- It does not commit, push, tag, publish, release, deploy, or operate software.
- It treats Skills, prompts, and agent-specific instructions as optional adapters, never as lifecycle authority.
- It preserves readable historical artifacts while requiring new mutations to follow the active contract.
- It does not compare candidate changes to a trusted Git base or enforce direct edits outside governed workflow commands in this stage.
- The same trusted repository state and explicit inputs yield the same scoped result for every supported agent.
- Invalid or unauthorized mutations fail before writes and report a bounded remediation path.
- Execution, assurance, and release state remain independently attributable.
- Human and machine consumers receive the same current state, blockers, permitted action, authority boundary, and recommended next step.
- `REQ-WEX-001`: project one bounded workflow scope.
- `REQ-WEX-002`: enforce lifecycle mutation preconditions atomically.
- `REQ-WEX-003`: keep execution, assurance, and release state independent.
- `REQ-WEX-004`: separate preparation provenance from accountable decision metadata.
- `REQ-WEX-005`: emit a canonical workflow handoff.
