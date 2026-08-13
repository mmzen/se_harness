+++
id = "WO-DOC-010"
type = "work_order"
title = "Explain refused verification and its Git consequences"
status = "implemented"
owners = ["repository-owner", "documentation-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
implements = ["REQ-DST-021", "REQ-DST-022"]
specifications = ["SPEC-DST-006"]
architecture = ["ARCH-DST-006", "ADR-DST-006"]
verification = ["VER-DST-006"]
+++

# Work Order: Explain refused verification and its Git consequences

## Lifecycle

Use `approved` to authorize bounded execution and `implemented` after the work and retained evidence are complete. Governance-only work normally stops at `implemented`. Use `verified` or `released` only when an eligible commit-bound VREC explicitly covers this work order under the repository's configured provenance policy.

The `architecture` relation selects every applicable architecture plus every required deciding ADR. An ADR may be omitted only for a selected architecture whose accepted `decision_assessment` is `no_significant_decision`; every `adr_required` architecture needs at least one selected active ADR that decides it.

An architecture is applicable when it addresses an architecturally significant requirement implemented by this work order. Every selected architecture must conform to at least one of the selected specifications. Routine requirements without an active `addresses` edge do not require fabricated architecture coverage.

## Objective

Correct the happy-path-only lifecycle explanation so readers understand what an assurance refusal means for a candidate, its work order, any ready verification record, later correction work, release eligibility, and Git history. Keep operational lifecycle mechanics in the phasing note and only the Git-topology consequence in the branching note.

The accountable repository owner reviewed the proposed gap, implementation facts, corrections, and sequencing boundary, then instructed `ok go` on 2026-08-13. This authorizes the bounded documentation, focused tests, packet lifecycle updates, and retained evidence described here. It does not amend candidate `1e3790f746e0a8fa75a00ab6b0db371a39a63675` or `VREC-DST-006`.

After reviewing the completed implementation and its verification results, the owner explicitly instructed `ok, push to PR` on 2026-08-13. This separately authorizes selecting the completed five-file diff as a clean candidate commit, normally pushing branch `docs/verification-refusal-path`, and opening one reviewable pull request. Because PR 33 remains open, the new pull request may be stacked temporarily against `docs/update-readme` and later retargeted to `main` after PR 33 merges; it must not add commits to or otherwise change PR 33. This publication authority does not authorize VREC capture or transition, pull-request merge, release preparation or approval, tagging, package publication, or deployment.

## In scope

- Add a concise `When verification is refused` subsection after the operational phase table.
- Explain that refusal withholds the `ready -> verified` transition; VRECs have no `rejected` state, and the completed work order honestly remains `implemented`.
- Explain the enforced release gates, including that a ready release proposal can technically include a ready VREC but cannot become `released` until every included VREC is verified or released and commit identities agree.
- Distinguish an uncommitted generated VREC from a committed ready VREC and explain evidence retention without claiming that evidence is a formal status-bearing artifact.
- Explain human-authorized `ready -> superseded` disposition only after a distinct verified or released successor covers the original work, preserving captured provenance and linking to the UML model for the relation.
- State that a defective payload requires a new candidate; avoid inventing a permanent negative VREC decision that the model cannot record.
- Explain `rejected` as a definition-artifact lifecycle value that removes the artifact from active coverage while warning that active dependents must be reconciled.
- Report accurately that `W-REV-004` is coverage-based, derived, and non-authoritative rather than age-based or an automated transition.
- Report the current early-release-proposal ambiguity: `prepare-release` accepts a ready VREC, but a retained ready RLS referencing it prevents clean supersession and the RLS model has no rejected or superseded state. Recommend following managed workflow order and retaining an RLS only after verification; do not invent a disposal mechanism.
- Add a short prose-only branching subsection after Phase 3 covering append-only correction, a later bounded work order/candidate, and revert commits for severe defects, with a cross-link to operational phasing.
- Add focused assertions for the stable lifecycle and topology statements while preserving exactly two `gitGraph` occurrences.
- Retain verification evidence in `docs/engineering/harness-distribution/evidence/WO-DOC-010-verification.md`.

## Out of scope

Changing validator, CLI, Explorer, lifecycle vocabulary, managed policy, templates, release preparation behavior, Git history, hosting controls, versioning, releases, tags, packages, or historical artifacts. This work does not transition, supersede, replace, delete, or reinterpret any concrete VREC or RLS and does not modify PR #33 or its declared candidate. Publication is limited to the new branch and pull request authorized above.

## Authorized decision envelope

The implementation agent may choose concise prose, cross-reference wording, and focused non-brittle assertions. It may classify verified implementation facts and the ready-RLS dead-end as an explicitly reported current-model limitation. It may not define a new lifecycle transition, imply automatic authority, or turn the illustrative branching example into repository law.

## Constraints

- Keep each note within its responsibility under `SPEC-DST-006`; do not copy managed workflow sections wholesale.
- Preserve the internal expertise comments and existing reader levels.
- Preserve exactly one non-authoritative branching model and exactly two `gitGraph` source occurrences.
- Use `must not be deleted or rewritten` for the governance rule rather than claiming current-state validation can reconstruct deletion history.
- Say that no formal VREC enters history when an uncommitted generated record is discarded; separately explain that retained refusal evidence enters history only when committed.
- Describe `W-REV-004` only when a verified or released record already covers the ready record's work set.
- Do not say a candidate can never be reconsidered; state only that a defective payload is corrected by a new candidate and that a refused VREC remains unverified unless an accountable later decision changes it.

## Expected change surface

- `docs/notes/harness-operational-phasing.md`
- `docs/notes/harness-branching-model.md`
- `tests/test_progressive_documentation.py`
- this work order and its retained evidence

## Required verification

Run focused progressive-documentation and public-onboarding tests, the complete standard-library suite, formal validation, doctor, start and review preflight, deterministic Explorer generation, Markdown link and structure checks, exact `gitGraph` count, protected-path inspection, and `git diff --check`. Manually verify the refusal sequence against validator status, coverage, commit, release, supersession, and dashboard rules plus the `prepare-release` implementation.

## Evidence to record

Record inspected source and policy lines, exact facts and corrections, changed files, focused and complete test counts, validation and warning classification, doctor and preflight outcomes, deterministic Explorer snapshot, Markdown/link/diagram results, protected-path result, and the unresolved ready-RLS lifecycle limitation.

## Stop and escalate conditions

Stop if accurate documentation would require a new VREC/RLS state, an automated transition, managed-policy change, behavior change, alteration of candidate `1e3790f746e0a8fa75a00ab6b0db371a39a63675`, or an edit to historical verification/release facts. Report any additional contradiction rather than inventing intended behavior.

## Completion report format

Report the two note changes, focused assertions, verification results, unchanged behavior/policy surfaces, and residual ready-RLS limitation. Do not claim verification, release, merge, or publication.

## Implementation result

Operational phasing now explains withheld verification, honest work-order state, enforced release blocking, uncommitted and committed ready-record paths, human-authorized supersession, coverage-based `W-REV-004`, new-candidate correction, and definition-artifact rejection without inventing a negative VREC state. It also reports the current committed-ready-RLS dead end and recommends the managed workflow order. The branching guide adds only the Git consequence: append-only main history, later bounded correction candidates, and revert commits as new candidates. Focused tests protect the stable distinctions and preserve exactly two `gitGraph` blocks. Detailed results and residual limitations are retained in `docs/engineering/harness-distribution/evidence/WO-DOC-010-verification.md`.
