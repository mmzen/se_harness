+++
id = "ARCH-HAG-002"
type = "architecture"
title = "Bind one decision actor to an existing accountability"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
addresses = ["REQ-HAG-010"]
conforms_to = ["SPEC-HAG-005"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "security-privacy-or-trust-boundary"]
rationale = "The change separates identity and declared accountability at an existing human-decision interface without adding authentication."
assessed_by = "Codex; proposed for human review"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T16:52:37Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved WO-HAG-003 and required verification in response to the reviewed six-artifact correction package. This applies only to that package: local implementation, checks, commits and commit-bound verification preparation. Human verification acceptance, publication, release, adoption and the live DEC-HAG-001 disposition remain separate. Reviewed file hashes were compared before this transition; approval bindings are retained under docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/."
+++

# Bind one decision actor to an existing accountability

## Components and flow

The CLI carries the actual decision-maker and optional authority-owner value
through the existing paired-risk dispatcher and workflow planner. The
decision validator reuses the existing holder resolver. The atomic writer
retains the binding on the DEC disposition and the actual actor on events.
There is no new registry, policy engine, authentication service or store.

## Trust boundary

The human's recorded decision and the caller's authority checks remain the
source of authorization. The evaluator checks shape, declared accountability,
state, graph and gates; it does not authenticate a person from a string.
Preview is read-only. Candidate tests use disposable fixtures; the live
checkout continues to use released 0.22.0 until separately authorized adoption.

## Design assessment

The additive public command option and audit representation need a recorded
design decision. ADR-HAG-002 compares it with implicit inference and ownership
rewrites. The cost is one optional command argument and disposition field.
