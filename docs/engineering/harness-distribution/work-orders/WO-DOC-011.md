+++
id = "WO-DOC-011"
type = "work_order"
title = "Show Harness Explorer in the public README"
status = "implemented"
owners = ["repository-owner", "documentation-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
implements = ["REQ-DST-020"]
specifications = ["SPEC-DST-006"]
architecture = ["ARCH-DST-006", "ADR-DST-006"]
verification = ["VER-DST-006"]
+++

# Work Order: Show Harness Explorer in the public README

## Lifecycle

Use `approved` to authorize this bounded implementation, `in_progress` while the approved work is being performed, and `implemented` only after the README, repository-owned images, tests, and retained evidence are complete. Commit-bound assurance remains a later decision through a new VREC; this work does not amend `VREC-DST-007` or candidate `52e713a9b041a0c8355f2ad8ad8f71c7dd65d1f2`.

## Authorization and objective

After supplying three current Harness Explorer screenshots, the accountable repository owner instructed the implementation agent to integrate them into the main `README.md` to show SE Harness in action on 2026-08-13. This authorizes a concise public-documentation follow-up using the existing approved progressive-documentation chain. It does not authorize changes to Explorer behavior, the already captured dashboard candidate, commit-bound verification, push, pull request, merge, release, package publication, or deployment.

After reviewing the completed and verified documentation change, the owner explicitly instructed `commit, push to PR #35, prepare validation record` on 2026-08-13. This separately authorizes selecting this bounded change as a descendant candidate commit on the existing dashboard branch, pushing that commit to PR #35, and preparing one new ready aggregate verification record covering both `WO-DST-007` and `WO-DOC-011`, both applicable verification contracts, and both retained evidence files. The new record must bind the new clean candidate rather than reinterpret `VREC-DST-007`. This authorization does not permit committing the prepared record, transitioning either VREC, superseding `VREC-DST-007`, merging the pull request, releasing, tagging, publishing, or deploying.

The objective is to let a public reader see the Overview, focused Lineage, and Readiness views without making the root README a second dashboard manual.

## In scope

- Store the three supplied PNG screenshots under a stable repository-owned documentation path with descriptive names.
- Add a compact gallery immediately after the existing practical workflow and diagram in `README.md`.
- Present the screenshots in the reader's natural order: Overview, Lineage, then Readiness.
- Use relative Markdown image links and meaningful alternative text.
- Add a short caption for what each view helps a reader answer while preserving the dashboard's derived, non-authoritative boundary.
- Add a focused automated assertion that the three links are relative, resolve inside the repository, and refer to valid PNG files.
- Retain verification evidence in `docs/engineering/harness-distribution/evidence/WO-DOC-011-verification.md`.

## Out of scope

Changing the dashboard implementation, data model, screenshots, image content, formal artifact vocabulary, lifecycle rules, managed templates, CLI behavior, package version, package data, historical records, external hosting, or PR #35 beyond the explicitly authorized bounded addition and accurate summary update. This work does not claim that screenshots are formal evidence or that a displayed readiness observation grants approval, verification, or release authority.

## Authorized decision envelope

The implementation agent may choose concise captions, stable filenames, and the smallest README heading structure that keeps all three images understandable. It may not introduce an external image host, absolute repository URL, generated documentation site, or detailed dashboard manual in the root README.

## Constraints

- Preserve the accepted root README order and its concise public-entry responsibility under `SPEC-DST-006`.
- Preserve the internal expertise comments and the existing public wording outside the bounded insertion.
- Use repository-relative Markdown paths so the source remains portable.
- Do not crop, annotate, recompress, or otherwise alter the supplied screenshots.
- Keep screenshots illustrative and label Explorer observations as derived rather than authoritative.
- Preserve unrelated user changes and historical VREC/RLS facts.

## Expected change surface

- `README.md`
- `docs/images/harness-explorer-overview.png`
- `docs/images/harness-explorer-lineage.png`
- `docs/images/harness-explorer-readiness.png`
- `tests/test_public_onboarding.py`
- this work order and its retained evidence

## Required verification

Run start and review preflight, focused public-onboarding tests, the complete standard-library suite, formal validation, doctor, Markdown local-link checks, PNG signature and dimension inspection, protected-path inspection, and `git diff --check`. Manually review the README in source form and confirm the captions do not imply governance authority.

## Evidence to record

Record source filenames, repository paths, byte sizes, dimensions, SHA-256 hashes, README placement and relative links, focused and complete test results, validation and doctor results, preflight results, link resolution, protected-path result, changed files, and residual rendering limits.

## Stop and escalate conditions

Stop if image integration requires changing Explorer behavior, using an external image host, changing package or release metadata, rewriting candidate `52e713a9b041a0c8355f2ad8ad8f71c7dd65d1f2`, or editing the already captured `VREC-DST-007` facts. A new descendant candidate and separately prepared aggregate VREC are expected under the later authorization.

## Completion report format

Report the three stored image paths, README placement, focused and complete verification, unchanged behavior and authority surfaces, the new candidate commit and push, and the separately prepared ready VREC. Do not claim accountable verification, supersession, release, publication, or merge.

## Implementation result

The root README now presents the supplied Overview, Lineage, and Readiness screenshots directly after its compact practical workflow. Each unchanged repository-owned PNG has a descriptive stable path, meaningful alternative text, a one-line reader-oriented caption, and a relative Markdown link. The surrounding copy states that Explorer views are derived and read-only and cannot approve work, verify a commit, or authorize release.

A focused onboarding assertion protects image ordering, relative repository containment, file presence, PNG signatures, and the authority boundary. Focused and complete tests, formal validation, doctor, start and review preflight, deterministic real-repository Explorer generation, exact source/destination image hashes, dimensions, local links, protected paths, and diff hygiene are retained in `docs/engineering/harness-distribution/evidence/WO-DOC-011-verification.md`. Dashboard runtime, managed templates, package data, versioning, historical records, candidate `52e713a9b041a0c8355f2ad8ad8f71c7dd65d1f2`, and `VREC-DST-007` remain unchanged.
