+++
id = "REQ-DST-017"
type = "requirement"
title = "Place provenance records in their engineering domain"
status = "implemented"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN verification or release provenance is captured for work belonging to one engineering domain, THE SYSTEM SHALL default the record to that domain while preserving explicit output control and repository-wide placement for aggregate or ambiguous records."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Place provenance records in their engineering domain

## Rationale

The current verification and release commands default to repository-wide record directories even when every selected work order belongs to one product domain. That separates generated provenance from the intent, requirements, design, and work it substantiates and makes domain exploration less coherent.

## Required response

- Add explicit domain selection to verification capture and release preparation.
- Retain explicit output-path selection as the highest-precedence placement instruction.
- When neither output nor domain is supplied, infer a domain only when all selected work orders resolve unambiguously to the same first-level domain below `docs/engineering/`.
- Place single-domain verification records under that domain's `verification-records/` directory and release records under its `releases/` directory.
- Preserve repository-wide defaults for cross-domain, domainless, or ambiguous aggregate provenance.
- Keep record contents, declared artifact relations, commit binding, state transitions, and release authority independent of the chosen path.

## Failure and boundary behavior

Explicit invalid domains or unsafe outputs fail before writing. Automatic inference must never guess among multiple domains. Legacy flat work orders immediately below a valid domain may still establish that domain for placement.

Repository-wide aggregate records remain valid and must not generate a noncanonical-path advisory merely because they intentionally cover multiple domains.

## Constraints

- Preserve existing `--output` behavior and safe-path enforcement.
- Preserve historical records at their current paths.
- Do not move records during install or upgrade.
- Do not interpret record placement as verification or release authorization.

## Acceptance examples

Capturing a verification record for work orders found only below `docs/engineering/simulation/` defaults to `docs/engineering/simulation/verification-records/`. Preparing a release across `simulation` and `billing` defaults to the repository-wide `docs/engineering/releases/` directory unless the caller supplies an explicit safe output.

## Open decisions

The specification proposes precedence and inference rules. Accountable review must confirm them before the CLI contract changes.
