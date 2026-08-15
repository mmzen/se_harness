+++
id = "WO-DOC-012"
type = "work_order"
title = "Reconcile validation and inspection documentation"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "documentation-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-DST-034"]
specifications = ["SPEC-DST-009"]
verification = ["VER-DST-009"]
+++

# Work Order: Reconcile validation and inspection documentation

## Lifecycle

On 2026-08-15, after reviewing the documentation impact of the layered validator and new inspection command, the repository owner instructed `yes go for the correction artifact packet`. That instruction authorized drafting `REQ-DST-034`, `SPEC-DST-009`, `VER-DST-009`, this bounded work order, and the domain-index entry only.

After reviewing the draft packet, the repository owner instructed `ok go for implementation` on 2026-08-15. That decision approves `REQ-DST-034`, `SPEC-DST-009`, `VER-DST-009`, and this bounded work order and authorizes implementation, focused verification, retained `WO-DOC-012` evidence, and an honest `implemented` state after completion. The bounded correction and verification are complete, with evidence retained at `docs/engineering/harness-distribution/evidence/WO-DOC-012-verification.md`; `implemented` records completed work rather than commit-bound assurance. The decision does not authorize a candidate commit, deletion or replacement of the existing ready VREC, VREC preparation or transition, push, pull-request mutation, merge, release, publication, or deployment.

No architecture relation is present because this requirement does not introduce or alter an architectural boundary and no active architecture directly addresses `REQ-DST-034`. Existing layered documentation architecture remains context, not selected coverage. Creating a nominal architecture or ADR would misrepresent routine documentation consistency as a significant design decision.

## Objective

Remove the semantic contradiction between the current six-command README/tests and the older active five-command documentation contract, then synchronize the progressive notes with the implemented `validate` and `inspect` behavior without changing runtime behavior or historical evidence.

## In scope

- Reconcile the current active wording and assertions in `REQ-DST-025`, `SPEC-DST-007`, and `VER-DST-007` with a six-command human operational surface.
- Preserve `init`, `adopt`, `doctor`, `validate`, `inspect`, and `dashboard` as the concise root examples while retaining the existing agent-command exclusion.
- Update `docs/notes/harness-overview.md`, `harness-operational-phasing.md`, `harness-installation-and-upgrades.md`, and `harness-lineage-example.md` as specified by `SPEC-DST-009`.
- Confirm rather than duplicate the already-current README, command reference, managed quality-gate taxonomy, and managed workflow wording; change them only if verification finds a bounded inconsistency.
- Update focused documentation assertions so they derive the current six-command contract and protect validate/inspect authority and exit distinctions.
- Retain work-order-keyed verification evidence and update the harness-distribution index.

## Out of scope

CLI, validator, inspection, Explorer, suggestion-catalog, installer, upgrade, governor, self-hosting, workflow, package version, artifact-schema, lifecycle, verification-record, release, publication, or deployment behavior. Historical evidence, VRECs, RLS records, release contracts, released candidates, external issues, and consumer repositories are not changed.

## Authorized decision envelope

After explicit approval, the implementation agent may choose concise sentences, table placement, cross-links, and focused assertion organization within the named surfaces. It may not add a command, change command behavior, copy detailed rule catalogs into multiple notes, reinterpret an earlier candidate, modify historical evidence, create architecture or ADR coverage, or broaden the work beyond documentation consistency.

## Constraints

- Keep all current edits for `WO-IAR-008` and `WO-IAR-009` intact and preserve unrelated user changes.
- The uncommitted `VREC-IAR-005` binds candidate `8ffdbe4b0562e1729f0292607b68dd0417588ee7`; it must not be approved or committed after a new documentation candidate is created.
- After authorized implementation and one new clean candidate commit, prepare a replacement aggregate VREC covering `WO-IAR-008`, `WO-IAR-009`, and `WO-DOC-012`, their three verification contracts, and their separate evidence paths.
- Do not edit `WO-DOC-008-verification.md`, `VREC-DST-005`, `VREC-SEH-005`, `RLS-SEH-005`, or other historical assurance and release facts.
- Keep the root README concise and expertise labels hidden as Markdown comments.
- Use repository-relative Markdown links and preserve root/canonical managed parity.

## Expected change surface

- `docs/engineering/harness-distribution/requirements/REQ-DST-025.md`
- `docs/engineering/harness-distribution/specifications/SPEC-DST-007.md`
- `docs/engineering/harness-distribution/verification/VER-DST-007.md`
- `docs/notes/harness-overview.md`
- `docs/notes/harness-operational-phasing.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `docs/notes/harness-lineage-example.md`
- focused public-onboarding and documentation tests
- `docs/engineering/harness-distribution/evidence/WO-DOC-012-verification.md`
- this packet and domain index

The root README, `docs/notes/harnessctl-reference.md`, managed `QUALITY_GATES.md`, managed `WORKFLOW.md`, and their canonical copies are inspection targets and should change only if they fail the approved contract.

## Required verification

Apply `VER-DST-009`. Run focused public-onboarding, documentation, validator, inspection, suggestion, CLI, installer, managed-integrity, package-data, and instruction-architecture tests; the complete suite on Python 3.11 and the local supported runtime; formal graph validation; `doctor`; start and review preflight; deterministic `inspect --json`; deterministic Harness Explorer generation; root/canonical parity; local-link and Markdown checks; protected-history inspection; and `git diff --check`.

## Evidence to record

Record exact changed files, six-command extraction, parser comparison, active-contract reconciliation, validation plane and exit checks, inspection validity/exit/suggestion/no-write checks, note coverage, focused and complete test results, runtime versions, formal validation, doctor, both preflight phases, deterministic hashes, link checks, README budget, root/canonical parity, historical protected-path result, deviations, and residual reader-comprehension uncertainty.

## Stop and escalate conditions

Stop if the correction requires a runtime or managed-policy behavior change, an architecture or ADR decision, a new suggestion or validator rule, modification of historical evidence or commit-bound facts, removal of current IAR work, a package version change, consumer-repository mutation, or authority to approve, commit, replace a VREC, push, merge, release, publish, or deploy.

## Completion report format

Report the reconciled formal contract, four updated progressive notes, unchanged runtime behavior, focused and complete verification, protected historical records, retained evidence path, and any residual inconsistency. Do not claim approval, commit-bound verification, release, publication, or merge.

## Implementation result

The active public contract now consistently defines six ordinary human-facing repository commands and distinguishes gate-oriented validation from non-gating inspection. The Tier-0 overview, operational phasing, installation/upgrade guide, and practical lineage example now place inspection at their appropriate audience depth. Focused assertions protect the revised contract and documentation route while the already-correct concise README, command reference, managed quality gates, and managed workflow remain unchanged.

Focused and complete Python 3.11/3.14 tests, formal validation, doctor, CLI help, deterministic inspection and Explorer generation, managed parity, link and Markdown checks, README budgets, protected-history inspection, and diff hygiene pass. Runtime behavior and historical evidence remain unchanged. Exact results and residual environmental notes are retained in `docs/engineering/harness-distribution/evidence/WO-DOC-012-verification.md`.
