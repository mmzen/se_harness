+++
id = "WO-IAR-004"
type = "work_order"
title = "Implement conditional ADR applicability and coverage"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-IAR-012"]
specifications = ["SPEC-IAR-004"]
architecture = ["ARCH-IAR-004", "ADR-IAR-004"]
verification = ["VER-IAR-004"]
+++

# Work Order: Implement conditional ADR applicability and coverage

## Lifecycle

The repository owner approved this packet before execution. Implementation progresses through `in_progress` and stops at `implemented` after retained evidence. Commit, verification capture or transition, push, PR, release, tag, publication, and deployment require separate authority.

## Objective

Make ADR applicability explicit and accountable for every architecture, conditionally require ADR coverage for significant decisions, permit justified routine no-ADR outcomes, and surface inconsistencies through authoring, validation, preflight, CI, and Explorer.

## Authorization

The repository owner approved `REQ-IAR-012`, `SPEC-IAR-004`, `ARCH-IAR-004`, `ADR-IAR-004`, `VER-IAR-004`, and this bounded work order on 2026-08-12 with the instruction `ok for implementation`. This authorizes implementation and retained evidence only; it does not authorize commit, push, pull-request creation, verification capture or transition, release, tag, publication, or deployment.

## In scope

- Extend the architecture metadata and canonical architecture, ADR, and work-order templates.
- Update focused workflow, decision-rights, quality-gate, and traceability policies without duplicating them into the router.
- Add formal validation of assessment shape and contradictions.
- Replace unconditional preflight ADR presence with per-architecture conditional coverage and deterministic text/JSON diagnostics.
- Add Explorer assessment states, edges, filters or detail where needed, and anomaly reporting.
- Update candidate CI/product tests and document the independent-baseline bootstrap limitation accurately.
- Implement the bounded legacy compatibility window without rewriting repository-owned artifacts.
- Apply the supported self-upgrade and retain `WO-IAR-004` evidence.

## Out of scope

Natural-language inference of significance; automatic ADR creation or approval; one ADR per requirement; automatic modification of existing formal artifacts; host branch-protection changes; new installation profiles; unrelated artifact types or lifecycle rules; commits; pushes; PRs; verification transitions; releases; tags; publication; and deployment.

## Authorized decision envelope

Implementation may choose stable diagnostic numbers, parser-helper boundaries, dashboard presentation, and bounded compatibility-warning names. It may not expand the trigger vocabulary without approval, weaken per-architecture coverage, treat omission as no-ADR, infer technical approval, or make the migration rewrite owner artifacts.

## Expected change surface

Formal parser/validator; preflight; dashboard generator/template; canonical policies and artifact templates; self-hosted managed files and lock; focused validation, preflight, dashboard, installer, authoring, security, and CI tests; instruction-architecture acceptance/index; public explanation if required; and retained evidence.

## Implementation plan

1. Approve the `IAR-004` chain and this work order through an accountable product/technical/quality decision.
2. Add failing metadata-matrix, preflight-coverage, legacy-compatibility, Explorer, policy-content, and security tests.
3. Implement the shared assessment parser and validator diagnostics.
4. Replace global ADR presence with per-architecture conditional preflight coverage and update deterministic outputs.
5. Update canonical templates and focused policies, then extend Explorer and candidate CI verification.
6. Apply the supported self-upgrade and confirm transactional parity and idempotence.
7. Execute `VER-IAR-004` on Python 3.11 and the local runtime, retain exact evidence, mark implementation artifacts complete, and stop for separate commit authority.

## Required verification

Perform every check in `VER-IAR-004`, including all assessment combinations, per-architecture graph coverage, first-design and routine cases, multi-architecture cardinality, legacy migration, untrusted input, transactional upgrade, managed parity, independent/candidate CI distinction, deterministic Explorer, review preflight, dual-runtime full tests, and diff hygiene.

## Evidence to record

Commands and exit codes; Python versions; fixtures and diagnostic codes; test counts; assessment/coverage matrix; legacy outcomes; security inputs; CI assurance source; canonical/root/lock parity; Explorer states and snapshots; changed paths; deviations; and residual risk.

## Stop and escalate conditions

Stop if significance would be inferred from arbitrary prose, technical-owner accountability becomes automated, a no-ADR path can omit rationale, a significant architecture can pass without related ADR coverage, existing artifacts would be rewritten automatically, baseline/candidate assurance is mislabeled, a required test fails, or external/governance authority is needed.

## Completion report format

Report the delivered decision model, diagnostics, migration behavior, changed components, verification results, evidence path, residual risks, lifecycle status, and explicitly unperformed actions.
