+++
id = "REQ-REB-007"
type = "requirement"
title = "Provide and rehearse bounded governance-deadlock recovery"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN maintainers assess governance-deadlock recovery readiness, THE SYSTEM SHALL provide a maintainer-only bounded recovery runbook and a disposable rehearsal that prove immutable source selection, isolated evaluator installation, restricted publication authority, public-install verification, and restoration of normal standard controls."
verification_method = "disposable-repository-rehearsal-and-manual-security-review"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Provide and rehearse bounded governance-deadlock recovery

## Rationale

The emergency recovery succeeded because maintainers improvised a careful bounded bootstrap, but an undocumented procedure increases supply-chain and authority risk during the next high-pressure failure.

## Preconditions and trigger

Maintainers perform a scheduled rehearsal or an accountable owner declares that normal governance cannot authorize the transition needed to restore the standard lifecycle.

## Required response

- State the stop condition, emergency decision rights, and evidence required before bypass.
- Select one immutable candidate commit and exact distribution identity.
- Build or acquire in isolation and use short-lived trusted publication credentials.
- Install the public artifact into a fresh external environment and prove its identity and checkout exclusion.
- Convert or repair only the bounded standard installation through a reviewed transaction.
- restore the normal publisher, managed evaluator workflow, candidate-evidence workflow, and absence invariants.
- Retain an incident record and require ordinary governance for every follow-up action.

## Failure and boundary behavior

The runbook stops on ambiguous source, mutable reference, digest disagreement, unavailable trusted publishing, contaminated environment, expanded mutation surface, failed public verification, or incomplete restoration. A rehearsal never publishes, changes the operational root, or exercises production credentials.

## Constraints

- The runbook is recovery guidance, not standing authorization.
- The automated rehearsal uses disposable repositories and fake or local publication boundaries.
- Any real external publication requires immediate action-time human authorization and protected-environment controls.

## Acceptance examples

### Example: normal behavior

**Given** a disposable legacy or deadlocked repository fixture

**When** the recovery rehearsal executes

**Then** it establishes a standard root with an external released evaluator, verifies restored controls, and leaves no active self-hosting surface.

### Example: failure behavior

**Given** a mutable branch name instead of an exact candidate commit

**When** recovery selection begins

**Then** the procedure stops before build, install, or publication simulation.

## Open decisions

The security and release owners must approve the final emergency authority and credential-boundary language; this draft does not grant those rights.
