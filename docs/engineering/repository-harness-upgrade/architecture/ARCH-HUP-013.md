+++
id = "ARCH-HUP-013"
type = "architecture"
title = "Retain the external evaluator boundary during 0.18.0 adoption"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-09-15"
updated = "2026-09-15"
[relations]
addresses = ["REQ-HUP-037", "REQ-HUP-038"]
conforms_to = ["SPEC-HUP-019"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The proposal applies the existing released-evaluator boundary and the supplied 0.18.0 ownership rules. Candidate source remains evidence; the external published evaluator remains the only installer. No new trust boundary is introduced."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "technical-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
+++

# Retain the external evaluator boundary during 0.18.0 adoption

## Components and responsibilities

The external evaluator verifies package identity and performs the atomic upgrade. The repository retains its lock, formal artifacts and owner instructions.

## Dependency direction

The repository selects the released evaluator. Candidate source cannot substitute for that evaluator when the repository is upgraded.

## Trust boundary

Published wheel bytes are checked against the existing release record before installation. Historical verification and release evidence remains unchanged.

The new release makes supplied human guides, templates, CI and settings editable. The explicit replacement set contains existing uncustomized supplied files.

## Decision assessment

The owner accepted reuse of the established external-evaluator boundary with the reviewed upgrade approval on 2026-09-15. The front matter records the applied approval decision.
