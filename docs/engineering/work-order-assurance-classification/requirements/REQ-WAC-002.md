+++
id = "REQ-WAC-002"
type = "requirement"
title = "Protect the non-required assurance exception"
status = "implemented"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN commit-bound verification is declared not required, SE Harness SHALL retain an accountable rationale, SHALL preserve ordinary implementation verification and evidence obligations, and SHALL NOT treat the declaration as an assurance decision or release waiver."
verification_method = "metadata, decision-rights, negative-path, and release-regression tests"

[relations]
derives_from = ["CAP-WAC-001"]
+++

# Requirement: Protect the non-required assurance exception

## Rationale

Without a bounded exception, agents may use `not_required` to avoid evidence or release controls. Governance-only work needs a legitimate terminal `implemented` state, but the reason and accountable role must remain inspectable.

## Required response

- Require rationale and `decided_by` for both values, with accountable review specifically required for `not_required`.
- Keep work-order verification relations, required checks, review preflight, and retained evidence unchanged.
- Permit a later explicitly selected VREC to cover a non-required work order; the declaration means no standing obligation, not a prohibition.
- Preserve exact release-record and configured provenance requirements.

## Failure and boundary behavior

Automation rejects malformed metadata but cannot determine whether a human rationale is substantively honest. A mixed work order must be split or classified `required`; an agent encountering uncertainty must stop rather than select the exception.

## Constraints

Do not create an aggregate score, automatic exemption, role impersonation check, recursive governance requirement, or release bypass.

## Acceptance examples

A work order that only records an already authorized VREC transition may declare `not_required` with accountable rationale. A work order that changes validator behavior cannot use publication work in the same scope to avoid a required VREC.

## Open decisions

None.
