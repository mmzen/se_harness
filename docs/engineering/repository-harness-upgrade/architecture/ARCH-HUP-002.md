+++
id = "ARCH-HUP-002"
type = "architecture"
title = "Adopt 0.6.0 through the existing standard-root boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "technical-owner"

[relations]
addresses = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
conforms_to = ["SPEC-HUP-002"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The adoption uses the already selected external released-evaluator boundary, ordinary standard upgrade, schema-3 identity lock, atomic evidence transaction, and separately governed post-publication adoption described by SPEC-REB-002 and SPEC-REB-003. The gitattributes adjustment only separates repository-owned post-release LF rules from the immutable public 0.6.0 fragment."
assessed_by = "technical-owner"
+++

# Architecture: Adopt 0.6.0 through the existing standard-root boundary

## Components and responsibilities

- Exact public 0.6.0 supplies templates, evaluator identity, plan, transaction, and root checks.
- `WO-HUP-002` binds prior lock, public archive, installed payload, scope, and accountable actor.
- The installer owns managed writes, schema-3 lock creation, rollback, canonical evidence, and no-op replay.
- The repository owns the three post-release migration LF rules outside the managed fragment.
- Human owners retain approval, assurance, commit, integration, and all external decisions.

## Control flow

`public identity -> approved packet -> exact integration adjustment -> clean plan -> atomic apply -> complete-root validation -> retained evidence -> later commit-bound assurance`

## Trust boundaries

Checkout source and locally rebuilt wheels are untrusted as governors. Public 0.6.0 is trusted only after archive and installed-payload verification. The operational root changes only when the approved transaction applies; publication did not make that change automatically.

## Prohibited patterns

- Candidate-source upgrade execution or hand-edited managed output.
- Hiding complete history through a compatibility view after adoption.
- Combining root adoption with product, release, publication, deployment, maintenance, or transitional-workflow cleanup.

## Decision assessment

No ADR is required because this packet executes the previously selected standard adoption mechanism without introducing a new architecture boundary or policy.
