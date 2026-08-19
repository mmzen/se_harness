+++
id = "REQ-IAR-019"
type = "requirement"
title = "Guide agents through authorized lifecycle handoffs"
status = "implemented"
owners = ["repository-owner", "requirements-steward", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN a coding agent completes a lifecycle stage and yields control, SE Harness SHALL require a stage-aware handoff that reports the completed work, current lifecycle state, recommended next authorized step, required human authority, an applicable exact command or suggested response, and valid alternatives without performing separately authorized actions."
verification_method = "Automated installed-template, responsibility-boundary, README, upgrade, and regression tests plus accountable semantic review"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Guide agents through authorized lifecycle handoffs

## Lifecycle

Approved and implemented on 2026-08-19 through `WO-IAR-011`, following the repository owner's instruction `ok go implement`, review of the complete `IAR-011` packet, and acceptance of its no-new-architecture applicability assessment.

## Rationale

SE Harness defines ordered artifact, implementation, verification, and release stages, but the managed agent route does not currently require a coding agent to explain what should happen after it finishes one of those stages. A technically complete response can therefore leave a user unsure whether the next accountable action is artifact approval, implementation authorization, evidence review, candidate commitment, verification, pull-request preparation, release preparation, or escalation.

The repository already offers deterministic, non-authoritative suggestions from `harnessctl inspect`. Those suggestions concern machine-observed queues and a closed finding catalog. This requirement addresses a different surface: the coding agent's conversational handoff after work it actually completed or a check it attempted.

## Preconditions and trigger

- The coding agent has completed one or more authorized lifecycle stages and is yielding control to the user; or
- a required check, managed-integrity condition, authority boundary, or stop condition prevents the selected stage from completing.

Routine progress updates while work continues are not lifecycle handoffs. When one authorized turn completes several adjacent stages without yielding, the final handoff may summarize all completed work but must recommend from the final state actually reached.

## Required response

At each lifecycle handoff, the agent must provide:

1. what was completed;
2. the current lifecycle state, including applicable artifact, work-order, verification-record, release-record, and commit identities;
3. one primary recommended next step selected from the managed workflow;
4. the human decision, accountable role, or approval required before that step when applicable;
5. the exact safe command or a suggested user response when either is applicable; and
6. alternative next steps when more than one governed path is valid.

The recommendation must use the actual IDs known in the repository, remain explicit about unperformed actions, and avoid a generic question when the managed workflow identifies a bounded next step.

## Failure and boundary behavior

- A failed check or stop condition keeps the reported lifecycle state unchanged and produces a bounded remediation or escalation recommendation.
- The agent must not present failure as partial approval, verification, or release readiness.
- The agent must not perform a recommended commit, push, pull request, lifecycle transition, tag, release, publication, deployment, or other separately authorized action merely because it named that action.
- When authority or state is ambiguous, the agent stops, identifies the ambiguity, and requests the accountable decision instead of guessing.
- When no safe command exists for a human decision, the handoff gives a suggested accountable response rather than inventing a command.

## Constraints

- Preserve the thin `AGENTS.md` gate, the single managed router, and the existing router-to-focused-policy responsibility split.
- Keep ordered stage procedure in managed `WORKFLOW.md`; the router states the non-waivable handoff obligation and routes to that procedure.
- Do not change `harnessctl inspect`, its JSON schema, its closed suggestion catalog, or its prohibition on executable remediation.
- Do not create machine-readable conversational output or a new CLI command in this packet.
- Do not infer product, technical, assurance, release, or service-owner decisions from a user message that does not explicitly exercise that authority.
- Preserve one standard installation, Python 3.11+ standard-library runtime behavior, managed integrity, and transactional upgrade behavior.

## Acceptance examples

### Example: completed definition packet

**Given** `REQ-ABC-001`, its governing definition, `VER-ABC-001`, and draft `WO-ABC-001` are ready for review

**When** the coding agent yields control

**Then** it reports those artifacts as draft, recommends accountable review and approval, and offers a response such as `Approve the governing packet and WO-ABC-001; do not implement yet.` without changing any status.

### Example: implemented work with alternatives

**Given** `WO-ABC-001` is implemented with retained evidence and review checks pass

**When** the coding agent yields before a candidate commit

**Then** it reports the implemented state, recommends an authorized clean candidate commit, explains that commit-bound verification follows the commit, and distinguishes that path from any valid request for further changes.

### Example: failure behavior

**Given** review preflight fails for `WO-ABC-001`

**When** the coding agent reports the result

**Then** it states that the work order has not advanced, names the failing condition, and recommends an in-scope remediation or accountable escalation without preparing a VREC or implying verification readiness.

## Open decisions

No unresolved product behavior remains. Accountable review confirmed that the router/workflow responsibility split is preserved, the conversational and Inspector guidance surfaces remain distinct, and no architecture artifact is applicable to this requirement.
