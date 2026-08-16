+++
id = "WO-DST-010"
type = "work_order"
title = "Reassess architecture after dependency revisions"
status = "implemented"
owners = ["repository-owner", "technical-owner", "documentation-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-DST-025", "REQ-DST-033"]
specifications = ["SPEC-DST-007", "SPEC-DST-008"]
architecture = ["ARCH-DST-007", "ADR-DST-007", "ARCH-DST-008", "ADR-DST-008"]
verification = ["VER-DST-007", "VER-DST-008"]
+++

# Work Order: Reassess architecture after dependency revisions

## Authorization

After reviewing the three `W-HEX-003` observations and the exact 2026-08-15 dependency changes, the accountable repository owner instructed `ok now` and selected this reassessment action on 2026-08-16. That decision authorizes this bounded work order, accountable reassessment of `ARCH-DST-007` and `ARCH-DST-008`, the one identified terminology correction, retained evidence, and an honest `implemented` state after checks pass.

After the architecture dates exposed the two downstream `ADR.decides -> ARCH` observations, the owner explicitly instructed `yes go`. That follow-up authorizes reaffirming `ADR-DST-007` and `ADR-DST-008`, updating their reassessment dates, and correcting the obsolete five-command sentence in `ADR-DST-007` to include `inspect`. It does not authorize a different selected option, changed ADR outcome, new decision, behavior change, requirement or specification rewrite, architecture replacement, validator or inspection-rule change, historical evidence rewrite, commit, push, pull request, VREC transition, release, publication, or deployment.

## Exact observations

1. `ARCH-DST-007.updated` predates revised `REQ-DST-025` through `addresses`.
2. `ARCH-DST-007.updated` predates revised `SPEC-DST-007` through `conforms_to`.
3. `ARCH-DST-008.updated` predates revised `SPEC-DST-008` through `conforms_to`.

## In scope

- Review the `REQ-DST-025` and `SPEC-DST-007` revisions that added the read-only, non-gating `inspect` command to the human documentation surface.
- Confirm whether those revisions alter `ARCH-DST-007` components, dependency direction, trust boundaries, required patterns, prohibited patterns, or `ADR-DST-007`.
- Review the `SPEC-DST-008` revision that removed redundant `templates/webui/` design sources and designated the canonical standard template as the sole reusable Explorer source.
- Clarify the ambiguous `ARCH-DST-008` source-copy sentence so it names the canonical distribution template and active managed root copy.
- Confirm whether the revision alters the snapshot boundary, browser boundary, CDN risk, fallback, distribution integrity, or `ADR-DST-008`.
- Record both accountable conclusions in the source architectures, set their `updated` dates to the reassessment date, and retain exact evidence.
- Reaffirm both deciding ADRs against the reassessed architectures, preserve their accepted outcomes, and align only the stale command-list detail in `ADR-DST-007`.

## Out of scope

README, notes, command behavior, Explorer implementation or appearance, template content, package data, managed lock, requirements, specifications, ADR outcomes or selected options, verification contracts, other architectures, formal relation changes, lifecycle changes other than this work order, and all external lifecycle actions.

## Required verification

- Capture the exact target revisions and source/target dates before reassessment.
- Confirm each architecture remains structurally and semantically compatible with its newer dependency.
- Confirm the two architectures, their two deciding ADRs, this work order, distribution index, and keyed evidence are the only changed paths.
- Run formal validation, doctor, start and review preflight, deterministic inspection, focused documentation and Explorer tests, and `git diff --check`.
- Confirm all three `W-HEX-003` observations disappear without suppressing the rule or changing target dates.

## Stop conditions

Stop if either newer definition requires a component, boundary, trust, dependency, selected option, accepted risk, or ADR outcome change; if another source must change; or if the warning cannot be resolved through a truthful reassessment and reaffirmation.

## Completion result

The accountable reassessment confirmed that both architectures and their accepted ADR outcomes remain applicable. The only corrections are the clarified Explorer source-copy terminology and the addition of the already implemented `inspect` command to `ADR-DST-007`'s public command list. All three original dependency observations and both downstream ADR observations are resolved without changing the inspection rule, target dates, product behavior, or architecture decisions. Evidence is retained in `../evidence/WO-DST-010-architecture-reassessment.md`.
