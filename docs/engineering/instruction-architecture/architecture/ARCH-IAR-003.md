+++
id = "ARCH-IAR-003"
type = "architecture"
title = "Review routing responsibility boundary"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-09-08"

[relations]
addresses = ["REQ-IAR-011"]
conforms_to = ["SPEC-IAR-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "cross-cutting-policy"]
rationale = "ADR-IAR-003 assigned review preflight, dashboard generation and candidate inspection to WORKFLOW.md, leaving routing and the evidence-versus-authority invariant in the router. It continues one modular boundary for every mandatory review instruction."
assessed_by = "technical-owner"
+++

# Architecture: Review routing responsibility boundary

## Context and scope

Apply the established summary-route-detail architecture to the review and visualization phase without changing the underlying review mechanisms.

## Components and responsibilities

- **Managed router:** selects workflow and quality-gate policy and preserves the evidence-versus-authority invariant.
- **`WORKFLOW.md`:** owns exact review commands, lifecycle placement, evidence retention, and candidate inspection activity.
- **`QUALITY_GATES.md`:** owns the evidence conditions for review and verification.
- **Preflight and Explorer:** produce derived observations without exercising authority.
- **Installer and lock:** distribute and protect both managed instruction files transactionally.

## Dependency direction

The router points to workflow and gates. Workflow may invoke tools but does not depend on duplicated router procedure. Tool output remains evidence consumed by accountable review.

## Required patterns

- Stable invariant in the router; exact procedure in the focused workflow.
- Direct managed routing, with no owner-controlled document required to discover mandatory procedure.
- Canonical-template-first propagation through the supported upgrade mechanism.

## Prohibited patterns

- Exact review commands in both router and workflow.
- Dashboard output described as approval, verification, or authority.
- Hand-edited lock digests or partial managed-file updates.

## Conformance checks

Content responsibility assertions, exact-prior upgrade and conflict fixtures, root/distribution/lock parity, review preflight, artifact validation, deterministic Explorer generation, and full regression suites.

## Related ADRs

- `ADR-IAR-001`: Use a thin adapter, one managed router, and modular policy.
- `ADR-IAR-002`: Keep invariant summaries in the router and procedure in focused policy.
- `ADR-IAR-003`: Assign review commands to the workflow module.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-IAR-003`).** The addressed
requirement becomes `REQ-IAR-011` and `conforms_to` names `SPEC-IAR-003`, the
active specification that specifies it. The assessment reads the drivers and
decision of `ADR-IAR-003`, the one active ADR that decides this architecture;
that ADR records no enumerated alternatives, so no alternatives trigger is
claimed. Title, status, statement and ADR relations are unchanged.
