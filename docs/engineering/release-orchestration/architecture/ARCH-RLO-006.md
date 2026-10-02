+++
id = "ARCH-RLO-006"
type = "architecture"
title = "Prepared release delivery across existing trust boundaries"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[decision_assessment]
outcome = "adr_required"
triggers = ["security-privacy-or-trust-boundary", "responsibility-or-dependency-direction", "material-alternatives"]
rationale = "Preparation crosses the current public-wheel dependency and activation changes an independent PyPI human gate; these choices require explicit review."
assessed_by = "Codex agent (proposal for mmzen review)"

[relations]
addresses = ["REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]
conforms_to = ["SPEC-RLO-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 d96c6475636a3c5f9be258e146f2c1bf519abbe1ddc6d360d3eeb4ff01fac40e; approved transition input SHA-256 d96c6475636a3c5f9be258e146f2c1bf519abbe1ddc6d360d3eeb4ff01fac40e. Only the confirmed WO assurance fields were added before this transition."
+++

# Prepared release delivery across existing trust boundaries

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Released evaluator and task instructions | Govern formal state and present the complete-release decision; reuse matching supplied authority. |
| Existing repository preparation and plugin builder | Produce verified immutable deliverables and a frozen plan without publication credentials. |
| Human owner | Accept required verification and approve the exact complete release plan. |
| Trusted-main workflow and repository publication tools | Check authority inputs and provider controls, then publish the listed inert payloads. |
| Existing observation and delivery checker | Retain public results, compare identities and report complete or incomplete. |

## Data flow

Verified candidate and staged payloads -> reviewed plan -> recorded human decision
and released RLS -> trusted-main publication -> independent public observations.
Observed results do not rewrite the reviewed plan. Governance receipts link to
the same immutable payloads rather than replacing them.

## Trust and dependency direction

Repository tools depend on portable lifecycle results. Portable code does not
depend on GitHub, PyPI, plugin catalogs or repository package layouts. Preparation
runs candidate code without publish credentials. Publication uses trusted-main
tools and checked bytes. No candidate-provided command is executed with credentials.

Provider policy is independently administered. Removal of the pypi reviewer is a
one-time human-approved configuration change after the replacement readiness
checks are verified. This is not an agent exemption or an administrator bypass.

## Failure and recovery

Preserve exact completed stages. Observe uncertain writes before replay. Never
overwrite a versioned package or immutable tag. Check the expected parent before
moving mutable refs. Any missing obligation remains visible in the existing report.

## Decision and cost

ADR-RLO-006 compares a wording-only change, extending the existing flow and a new
service. The selected design requires a staged plugin input and changes one
provider control; it adds no new service, formal state or artifact type.
