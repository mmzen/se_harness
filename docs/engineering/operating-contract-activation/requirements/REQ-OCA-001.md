+++
id = "REQ-OCA-001"
type = "requirement"
title = "Activate only complete and requirement-scoped operating contracts"
status = "implemented"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN an existing operating contract is proposed for activation, THE REPOSITORY SHALL require current requirement-only traceability, complete actionable operating controls, and explicit accountable approval without changing release authority."
verification_method = "artifact inspection and deterministic repository validation"

[relations]
derives_from = ["CAP-OCA-001"]
+++

# Requirement: Activate only complete and requirement-scoped operating contracts

## Rationale

A `draft` contract is a proposal. Moving it to `approved` creates continuing obligations, so the decision must be based on an explicit scope and usable controls rather than the presence of a file. Draft release proposals cannot be used as substitutes for requirements or as implied release authority.

## Preconditions and trigger

- The assured domain behavior already exists and its selected requirements are active.
- Accountable owners have reviewed the operational claims and available evidence.
- Any discovered behavior change is removed from this work and governed separately.

## Required response

1. `assures` names only active requirements that the contract genuinely operates.
2. The contract defines service objectives, observability, alerts and escalation, capacity and cost, backup and recovery, security and compliance, automated-remediation limits, runbooks, and evidence retention.
3. Commands and paths reflect the current repository.
4. The accountable service owner accepts the contract independently from release approval.
5. Authoring guidance remains consistent with the authoritative artifact catalog.

## Failure and boundary behavior

Leave a contract `draft` if an obligation, owner, evidence source, or recovery boundary is unresolved. Do not weaken a contract to obtain approval and do not change executable behavior inside this work order.

## Constraints

- Preserve every draft `REL-*` artifact and its relations.
- Do not claim availability guarantees that require an unimplemented service.
- Automation may observe and propose; it may not approve, transition, release, publish, or deploy.
- Report the missing validator target-type enforcement as a follow-up rather than expanding this packet.

## Acceptance examples

### Example: normal activation

**Given** an implemented domain with current requirements and an observable operating procedure

**When** accountable owners review the complete contract

**Then** the contract becomes `approved`, assures only those requirements, and leaves release artifacts unchanged.

### Example: unresolved behavior

**Given** a draft contract whose recovery procedure requires new executable behavior

**When** activation is reviewed

**Then** the contract stays `draft` and the behavior change receives a separate governed packet.

## Open decisions

None for this bounded activation. Validator enforcement of `OPS.assures` target types is deferred.
