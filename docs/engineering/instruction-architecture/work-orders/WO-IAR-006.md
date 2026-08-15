+++
id = "WO-IAR-006"
type = "work_order"
title = "Implement the authoritative artifact applicability catalog"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-IAR-014"]
specifications = ["SPEC-IAR-006"]
architecture = ["ARCH-IAR-006", "ADR-IAR-006"]
verification = ["VER-IAR-006"]
+++

# Work Order: Implement the authoritative artifact applicability catalog

## Lifecycle and authorization

The repository owner approved `REQ-IAR-014`, `SPEC-IAR-006`, `ARCH-IAR-006`, `ADR-IAR-006`, `VER-IAR-006`, and this bounded work order on 2026-08-15 with the instruction `ok go for implementation`. The bounded implementation and retained evidence are complete, so this work order is now `implemented`. Evidence is retained at `docs/engineering/instruction-architecture/evidence/WO-IAR-006-verification.md`. This state records completed work, not independent verification, and does not authorize commit, push, pull-request creation, verification capture or transition, release, tag, publication, or deployment.

## Objective

Give operators and coding agents one authoritative, complete, and enforceably consistent answer for every canonical artifact type's purpose and applicability, while eliminating the validator rule that currently forces nominal architecture onto routine work.

## In scope

- Add the complete normative artifact-applicability catalog to managed `TRACEABILITY.md`.
- Route artifact purpose, applicability, omission, reuse, and relation questions from `ENGINEERING_HARNESS.md` to that catalog.
- Add concise relative cross-references from the Tier-0 overview and simplified UML/model documentation without duplicating the catalog.
- Keep the template index focused on canonical locations and authoring mechanics; align type-specific guidance where it conflicts.
- Correct formal validation so `work_order.architecture` is conditional on active typed architecture applicability.
- Preserve failures for omitted applicable architecture, irrelevant architecture, missing conforming specifications, and missing deciding ADRs.
- Add deterministic registry/catalog completeness tests and focused validator/preflight matrices.
- Update canonical standard templates, candidate managed copies, package data expectations, and schema-2 lock through the supported transactional path.
- Retain `WO-IAR-006`-keyed implementation and verification evidence.

## Out of scope

New artifact types or prefixes; lifecycle or status changes; automatic semantic authoring; generated normative policy; one-file-per-change quotas; inference of architectural significance; rewriting historical artifacts; changing VREC/RLS provenance, supersession, release aggregation, self-hosting identities, branch policy, or accountable decision rights; commits, pushes, pull requests, releases, tags, publication, and deployment.

## Authorized decision envelope

If approved, implementation may choose exact headings, table layout, structural test helpers, stable diagnostic identifiers, and concise cross-reference wording. It may not move normative authority into source, notes, templates, or generated output; omit a canonical standard type; weaken applicable architecture or ADR coverage; require ceremonial artifacts; or rewrite repository-owned formal artifacts.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior.
- Treat repository content, Markdown, TOML, paths, IDs, and relation values as untrusted.
- Preserve the single managed router and focused policy responsibilities.
- Keep root, canonical template, package data, and lock consistent where managed parity applies.
- Protect repository customizations and fail transactionally without partial writes.
- Preserve unrelated user changes and historical commit-bound records.

## Expected change surface

- `docs/engineering/TRACEABILITY.md` and its canonical standard-template copy.
- `ENGINEERING_HARNESS.md` and its canonical template if routing wording changes.
- `docs/notes/harness-overview.md` and `docs/notes/harness-uml-model.md` for concise relative links.
- Work-order and related formal-artifact templates only where applicability wording requires correction.
- `scripts/validate_engineering_artifacts.py`, canonical validator copy, and preflight behavior if required by the matrix.
- Artifact registry/documentation consistency tests, progressive-documentation tests, validator/preflight tests, installer/integrity tests, acceptance scenarios, and full regression.
- `.engineering-harness.lock` and retained `WO-IAR-006` evidence.

## Implementation plan

1. Obtain accountable approval for `REQ-IAR-014`, `SPEC-IAR-006`, `ARCH-IAR-006`, `ADR-IAR-006`, `VER-IAR-006`, and this work order.
2. Transition the approved work order to `in_progress`, run start preflight, and read the complete manifest.
3. Add failing catalog-membership, routing, cross-reference, and work-order architecture applicability tests.
4. Implement the catalog in `TRACEABILITY.md` and the thin router/human/template references.
5. Align validator and preflight cardinality with conditional typed architecture applicability.
6. Apply the supported transactional self-upgrade, verify managed/root/template/package parity, lock integrity, customization protection, and idempotence.
7. Execute `VER-IAR-006` on Python 3.11 and the local runtime, retain evidence, move implementation artifacts to `implemented`, and stop for separate commit authority.

## Required verification

Execute every case in `VER-IAR-006`: exact catalog/type coverage, duplicate and unknown entries, responsibility separation, operator and agent readability, routine work without architecture, all applicable architecture and ADR failures, managed parity, safe upgrade, package/fresh-install behavior if authorized, malicious inputs, deterministic output, review preflight, dual-runtime full regression, and diff hygiene.

## Evidence to record

Commands and exit codes; runtimes and test counts; canonical type/catalog matrix; responsibility and link inspection; validator and preflight fixture results; diagnostics; managed-file parity and lock hashes; upgrade and customization outcomes; package identity if exercised; dashboard snapshot; changed paths; deviations; and residual risks.

## Stop and escalate conditions

Stop if implementation requires a new artifact type, relocates authority into non-authoritative material, duplicates the full catalog, cannot align validator behavior without weakening applicable architecture coverage, rewrites historical artifacts, damages managed customization safety, introduces nondeterminism, encounters a required test failure, or needs authority beyond this work order.

## Completion report format

Report the authoritative catalog location, covered type set, routing and cross-reference changes, applicability semantics, validator/preflight correction, managed distribution changes, verification results, evidence path, residual risks, lifecycle state, and explicitly unperformed actions.
