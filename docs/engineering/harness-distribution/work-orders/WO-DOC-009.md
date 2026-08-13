+++
id = "WO-DOC-009"
type = "work_order"
title = "Clarify the illustrative trunk and maintenance branching model"
status = "implemented"
owners = ["repository-owner", "documentation-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
implements = ["REQ-DST-022"]
specifications = ["SPEC-DST-006"]
architecture = ["ARCH-DST-006", "ADR-DST-006"]
verification = ["VER-DST-006"]
+++

# Work Order: Clarify the illustrative trunk and maintenance branching model

## Authorization and objective

After iteratively reviewing a realistic Git example, the accountable repository owner explicitly instructed `update the example page with this` on 2026-08-13. This authorizes a documentation-only refinement of the single illustrative branching model and focused tests.

After reviewing three concrete consistency corrections and the proposed `WO-QUAL-031` refinement, the owner explicitly instructed `ok go` on 2026-08-13. This extends the same documentation-only work to align the owner-controlled repository context, complete the maintenance contract and verification chain, and correct conditional canonical record placement.

After reviewing the completed implementation, the owner explicitly instructed `ok, now commit + PR,then prepare the verification record` on 2026-08-13. This authorizes selecting the completed documentation diff as a clean candidate commit, publishing the branch normally in a new pull request, capturing one ready `VREC-DST-006` bound to that exact candidate, and retaining the ready record in a later governance commit. It does not authorize verification-record approval or transition, pull-request merge, release preparation or approval, tagging, package publication, or deployment.

Retain the compact one-change example as an introductory walkthrough, then add a realistic example of the same trunk-based policy showing independently integrated and verified changes, delayed release selection, exact integrated release qualification, aggregate verification, release decision, creation of a supported maintenance branch from the released commit, and later patch maintenance.

## In scope

- Update `docs/notes/harness-branching-model.md` as the explanatory product surface and narrowly align the existing branching-note description in `docs/engineering/REPOSITORY_CONTEXT.md`.
- Keep the document-level expertise target at 6.5/10 and make the central walkthrough approachable at the requested 5/10 level.
- Preserve one non-authoritative model and the repository-policy boundary while presenting it through two examples of increasing depth.
- Show per-change VRECs for every illustrated normal-development work order.
- Distinguish the release contract, release-qualification work order, aggregate VREC, and RLS.
- Explain that earlier VRECs bind different commits and are not combined to verify a later integrated candidate.
- Show that new release lines originate from `main`, while `release/x.y` begins at an already released commit and exists only for compatible maintenance.
- Show `REL-031`, `WO-FIX-014`, `VER-FIX-014`, `WO-QUAL-031`, and its qualification contract as the complete maintenance planning and candidate chain.
- State that the release-contract/VREC/RLS work-set agreement applies equally to normal and maintenance releases.
- Explain conditional canonical VREC/RLS placement for single-domain and cross-domain work, the advisory-only `W013` behavior, non-relocation, and the fact that paths do not grant authority.
- Update focused documentation assertions without freezing incidental wording.
- Retain verification evidence in `docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md`.

## Out of scope

Changing harness behavior, managed policy, templates, CLI, validator, Explorer, CI, repository-host controls, actual branch protection, current version, release contracts, existing VRECs, RLS records, tags, packages, publication state, or any historical formal artifact. The later authorization permits only the new ready `VREC-DST-006` described above. This work does not create a release or claim that the illustrative policy is active repository law.

## Verification and completion

Run focused documentation tests, the complete suite, formal validation, doctor, review preflight, deterministic Explorer generation, Markdown structure and link checks, protected-path inspection, and diff hygiene. Mark this work order `implemented` only after the checks and retained evidence are complete.

The currently verified `VREC-DST-005` remains immutable assurance for candidate `755785bb5be296b6920bf68b7398260454cd200b`; it does not cover this later documentation refinement. Any commit-bound assurance for this change requires a new candidate and later VREC.

## Implementation result

The single illustrative page starts with the compact candidate/VREC/RLS example, then applies the same trunk-based policy to independently retained per-change VRECs, delayed release selection, distinct qualification work, aggregate release verification, release-owner decisions, and supported-line maintenance. The final maintenance path includes `REL-031`, fix and qualification work orders, their verification contracts, candidate P, and exact contract/VREC/RLS coverage agreement. Conditional canonical record placement and advisory-only `W013` behavior are explained, and repository context accurately describes the note without declaring policy. Focused and complete tests, formal validation, doctor, preflight, deterministic Explorer generation, Markdown structure, protected-path, and diff checks passed; detailed results are retained in the evidence path above.
