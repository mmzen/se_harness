+++
id = "REQ-IAR-011"
type = "requirement"
title = "Route review procedure to its focused workflow owner"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN the managed router presents review and visualization guidance, THE SYSTEM SHALL retain the evidence-and-authority boundary while routing exact review commands and ordered activity to WORKFLOW.md without duplicating them."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Route review procedure to its focused workflow owner

## Rationale

The managed router currently repeats the review-preflight command already present in `WORKFLOW.md` and is the only managed policy location containing the dashboard command. This mixes stable authority boundaries with procedural detail and creates another synchronization obligation.

## Required response

- `ENGINEERING_HARNESS.md` routes review readiness and visualization to `WORKFLOW.md`, subject to `QUALITY_GATES.md`.
- The router states that preflight and Harness Explorer outputs are derived, read-only evidence and cannot approve work or verify a candidate.
- `WORKFLOW.md` owns the exact review-preflight and dashboard commands, their place in the lifecycle, and the instruction to inspect consistency and anomaly findings.
- Fresh installations, safe upgrades, and the self-hosted repository expose the same responsibility boundary.

## Failure and boundary behavior

- Removing duplication must not remove review preflight, visualization, evidence retention, or the distinction between evidence and accountable verification.
- Existing fail-closed preservation applies to customized or ambiguous managed router or workflow content.
- Neither document may imply that a dashboard, preflight result, or passing check performs a verification transition.

## Constraints

- Preserve the summary-route-detail pattern selected by `ADR-IAR-002`.
- Do not change preflight, dashboard, lifecycle, VREC, or quality-gate behavior.
- Do not make an owner-controlled document the only location of mandatory review procedure.

## Acceptance examples

### Example: reviewing a completed candidate

**Given** an actor reaches the managed router's review section

**When** the actor needs exact review commands

**Then** the router identifies their focused owners and `WORKFLOW.md` provides the commands and ordered activity.

### Example: evaluating a dashboard

**Given** Harness Explorer shows no critical anomaly

**When** the candidate is reviewed

**Then** the result remains derived evidence and does not verify or approve the candidate.
