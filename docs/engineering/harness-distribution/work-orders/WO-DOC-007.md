+++
id = "WO-DOC-007"
type = "work_order"
title = "Create progressive current SE Harness documentation"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-DST-019", "REQ-DST-020", "REQ-DST-021", "REQ-DST-022", "REQ-DST-023"]
specifications = ["SPEC-DST-006"]
architecture = ["ARCH-DST-006", "ADR-DST-006"]
verification = ["VER-DST-006"]
+++

# Work Order: Create progressive current SE Harness documentation

## Lifecycle

The accountable repository owner approved the governing chain and this bounded work order on 2026-08-12 with the instruction `go for implementation`. Use `implemented` only after the work and retained evidence are complete. Commit-bound verification remains a later VREC decision.

Implementation, focused and complete tests, formal validation, installed integrity, phase-appropriate preflight, CLI help, Explorer generation, link and terminology inspection, manual reader-level review, protected-path audit, and retained evidence were completed on 2026-08-12. This lifecycle transition records completion of authorized work only; it does not grant commit-bound verification or release authority.

## Authorization basis

On 2026-08-12, the repository owner supplied a detailed documentation objective and required work: preserve the useful README structure while correcting it, establish expertise-labeled overview, UML, phasing, branching, and practical-example notes, inspect implementation before documenting behavior, avoid duplication, distinguish authority categories, and report ambiguous inconsistencies. After reviewing the completed packet, the owner explicitly instructed `go for implementation`, approving `REQ-DST-019` through `REQ-DST-023`, `SPEC-DST-006`, `ARCH-DST-006`, `ADR-DST-006`, `VER-DST-006`, and this work order for bounded execution.

## Objective

Turn the current README and draft notes into a progressive, technically current human documentation system spanning target expertise 4/10 through 7/10, without changing SE Harness behavior or creating a competing source of governance authority.

## In scope

- Inspect current managed policy, CLI and control-plane implementation, canonical templates, root operational copies, tests, release metadata, self-hosting configuration, and relevant Git state before finalizing behavior claims.
- Preserve and correct the current root `README.md` structure at target expertise 6/10; add a clear route into the deeper notes.
- Add `docs/notes/README.md` as the non-authoritative learning-path index.
- Rewrite `docs/notes/harness-overview.md` for SE Harness at 4/10.
- Rewrite `docs/notes/harness-uml-model.md` for the current simplified typed conceptual model at 6/10.
- Add `docs/notes/harness-operational-phasing.md` at 6/10.
- Add `docs/notes/harness-branching-model.md` at 6.5/10 using exactly one illustrative model.
- Rewrite `docs/notes/harness-lineage-example.md` as realistic current practical examples at 7/10.
- Align or remove the unapproved branching-model draft in `docs/engineering/REPOSITORY_CONTEXT.md` so repository guidance and the illustrative note cannot contradict each other.
- Make bounded current-status corrections to repository-owned indexes or guides that the new documentation directly relies on, including `docs/engineering/README.md`, `docs/engineering/harness-distribution/README.md`, `docs/engineering/instruction-architecture/README.md`, and `docs/engineering/self-hosting-boundary/README.md`, without changing historical formal facts.
- Add or update focused standard-library documentation tests.
- Retain verification evidence at `docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md` and set this work order to `implemented` only after all checks pass.

## Out of scope

- Changing CLI, installer, validator, preflight, provenance, runtime identity, Explorer computation, templates, workflows, locks, package metadata, package version, dependencies, or release-build behavior.
- Resolving the authoritative G0-G5 versus current Explorer-readiness semantic discrepancy; this work reports it and leaves behavior unchanged for separate governance.
- Changing formal artifact semantics, lifecycle rules, decision rights, quality-gate policy, or traceability policy.
- Rewriting completed formal artifacts, historical evidence, VREC or RLS provenance, release tags, GitHub Releases, PyPI files, attestations, or governor selection.
- Creating new 0.2.2 publication evidence without separate authority.
- Reading from or writing to Mokiterions or any other consumer repository.
- Configuring branch protection, required checks, CODEOWNERS, merge strategy, branch names, or remote hosting policy.
- Building a distribution, committing, pushing, opening or merging a pull request, tagging, releasing, publishing, or deploying.

## Authorized decision envelope

The implementation agent may choose exact prose, cross-reference placement, diagram syntax, visual layout, examples, and focused test organization within `SPEC-DST-006`. It may make a narrowly justified README section move only when the evidence shows reduced duplication or a clearer required learning path. It may use fictional product identifiers only when labeled illustrative and internally consistent.

The agent may not choose intended harness behavior when implementation and managed policy disagree. It must retain the discrepancy, identify the authoritative surface, and stop if truthful documentation would require a product or policy decision outside this packet.

## Constraints

- Work only in the existing `C:\Users\mathi\RustroverProjects\se_harness` checkout and preserve unrelated user changes.
- Treat the existing staged README and notes as draft input, not approved truth.
- Keep the current 0.2.2 self-hosting control files at `HEAD` and do not reintroduce the earlier local rollback.
- Use current commands and exact repository paths; avoid hypothetical flags or files.
- Keep the README compatible with GitHub and PyPI rendering and keep diagrams meaningful as source text.
- Do not eliminate the 38 classified historical compatibility warnings by modifying old artifacts.

## Expected change surface

- `README.md`
- `docs/notes/`
- owner-controlled repository and domain indexes or guides explicitly named in scope
- focused documentation tests under `tests/`
- this packet's lifecycle metadata and `evidence/WO-DOC-007-verification.md`

Managed templates, product runtime, release automation, and historical provenance are protected surfaces.

## Required verification

Apply every check and manual assessment in `VER-DST-006`. At minimum, run focused documentation tests, the complete unit suite on Python 3.11 and the available local runtime when feasible, CLI help for documented commands, formal graph validation, `doctor`, start and review preflight, deterministic dashboard generation, Markdown link and control-character inspection, `git diff --check`, and a changed/protected-path audit.

Classify every warning and discrepancy. The known 38 legacy location/architecture advisories may remain; any new warning, graph error, managed-integrity failure, false command, broken link, missing expertise label, copied consumer fact, or undocumented authority ambiguity blocks completion.

## Evidence to record

Retain the initial documentation audit, inspected implementation and policy paths, requirements-to-evidence matrix, exact commands and exit codes, test counts, runtime versions, version synchronization, expertise inventory, link graph, terminology scan, manual reader reviews, diagram and timeline inspections, example walkthrough, branching-policy boundary, gate-semantic discrepancy, validator warning classification, dashboard snapshot, diff summary, protected-path proof, deviations, and residual risks.

## Stop and escalate conditions

Stop if the work requires behavior or managed-policy changes; if public facts cannot be verified; if the single branching example would conflict with an approved repository policy; if current Explorer behavior cannot be described without implying false authority; if an existing user edit cannot be reconciled safely; if any protected file changes; if validation, doctor, preflight, focused or full tests fail; or if scope expands beyond the named documentation system.

## Completion report format

Report changed documents and target levels, corrected obsolete claims, source-of-truth inspections, cross-reference and duplication outcomes, verification results, remaining known discrepancies, unchanged protected surfaces, deviations, and residual risks. State explicitly that documentation does not grant approval or change SE Harness behavior.
