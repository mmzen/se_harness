+++
id = "WO-DOC-008"
type = "work_order"
title = "Condense the public README and relocate operational detail"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-DST-024", "REQ-DST-025", "REQ-DST-026", "REQ-DST-027", "REQ-DST-028"]
specifications = ["SPEC-DST-007"]
architecture = ["ARCH-DST-007", "ADR-DST-007"]
verification = ["VER-DST-007"]
+++

# Work Order: Condense the public README and relocate operational detail

## Lifecycle

The repository owner agreed with the concise-README proposal and instructed `go for the artifact packet` on 2026-08-12. After reviewing the resulting chain, the owner explicitly instructed `go for implementation`, approving `REQ-DST-024` through `REQ-DST-028`, `SPEC-DST-007`, `ARCH-DST-007`, `ADR-DST-007`, `VER-DST-007`, and this bounded work order. Use `implemented` only after the authorized changes and retained evidence are complete.

`WO-DOC-007` remains implemented historical work and must not be reopened or rewritten to absorb this refinement.

The concise root, three relocated reference notes, notes-index routes, focused tests, complete regression checks, formal validation, installed integrity, preflight, CLI help, Explorer generation, link and content scans, reader assessments, protected-path audit, and retained evidence were completed on 2026-08-12. This `implemented` state records execution completion only; commit-bound verification remains a later VREC decision.

## Objective

Reduce the root README from a comprehensive manual to a concise, persuasive, human-facing entry point of at most 200 lines, while preserving useful detail in expertise-labeled notes and retaining explicit human/agent/repository authority boundaries.

## In scope

- Reclassify every current root section as essential public knowledge, relocated operator/agent/contributor detail, authoritative-policy link, duplication, or obsolete content.
- Rewrite `README.md` under the structure, line budget, command allowlist, value graph, responsibility, limitations, and cross-link contract in `SPEC-DST-007`.
- Create `docs/notes/harness-installation-and-upgrades.md`, `docs/notes/harnessctl-reference.md`, and `docs/notes/developing-se-harness.md` with required expertise labels.
- Update `docs/notes/README.md` and make bounded cross-link or deduplication edits to existing notes.
- Update focused public and progressive-documentation tests, adding a dedicated concise-root test module if that yields clearer ownership.
- Update the harness-distribution owner index with this packet's lifecycle when implementation is authorized.
- Retain implementation evidence at `docs/engineering/harness-distribution/evidence/WO-DOC-008-verification.md` and transition this work order to `implemented` only after all checks pass.

## Out of scope

- Changing runtime, CLI behavior, installer, validator, preflight, provenance, runtime identity, Explorer computation, templates, workflows, locks, package metadata/version, dependencies, build normalization, or release behavior.
- Editing managed policy to match explanatory prose.
- Resolving the two current 0.2.2 policy/checker limitations; this work keeps their disclosure.
- Rewriting `WO-DOC-007`, its evidence, completed formal artifacts, historical VREC/RLS records, release evidence, tags, GitHub Releases, PyPI files, or governor selection.
- Adding a second README, generated documentation build, remote diagram dependency, interactive website, or installation profile.
- Configuring GitHub, branch protection, required checks, CODEOWNERS, environments, publishing, deployment, or external services.
- Reading or changing any consumer repository.
- Committing, pushing, opening a pull request, capturing a VREC, preparing a release, tagging, publishing, or deploying.

## Authorized decision envelope

After explicit implementation approval, the agent may choose exact concise prose, section names within the nine-section cap, diagram styling, local link placement, and how to deduplicate existing notes while satisfying `SPEC-DST-007`.

The agent may retire root content only when it is duplicated, obsolete, or preserved by a clearly linked owner; the evidence ledger must record the disposition. It may not omit material safety or authority boundaries merely to meet the line limit. If the 200-line ceiling conflicts with truthful required content after reasonable editing, stop and request a governed requirement decision.

## Constraints

- Work only in the current `C:\Users\mathi\RustroverProjects\se_harness` checkout and preserve the current staged/unstaged user work.
- Keep `README.md` at target expertise 6/10 and every new note at its specified level.
- Use only current CLI syntax and current repository/release facts.
- Keep GitHub/PyPI links usable from the published root README and local links valid in repository notes.
- Preserve managed and self-hosting control files byte-for-byte.
- Do not run a distribution build under this work order.

## Expected change surface

- `README.md`
- `docs/notes/README.md`
- existing and new files under `docs/notes/` needed by the relocation map
- `tests/test_public_onboarding.py`
- `tests/test_progressive_documentation.py`
- optionally one focused concise-root test under `tests/`
- `docs/engineering/harness-distribution/README.md`
- this packet's lifecycle metadata and `evidence/WO-DOC-008-verification.md`

## Required verification

Apply every automated and manual check in `VER-DST-007`. At minimum: focused documentation tests; complete unit suite on supported/local runtimes when available; exact CLI-reference comparison; formal artifact validation; `doctor`; start and review preflight after approval; CLI help for all subcommands; deterministic Explorer generation; link, control-character, and fence inspection; line/section/graph/command budgets; `git diff --check`; protected-path audit; and a manual 6/10 reader walkthrough.

## Evidence to record

Retain the initial 523-line/16-section baseline, content disposition ledger, final information budget, exact command inventory, new-note expertise and ownership, source-of-truth inspections, link graph, value/authority review, upgrade scenario, CLI synchronization, test and diagnostic outputs, warning classification, dashboard snapshot, changed/protected paths, deviations, and residual risks.

## Stop and escalate conditions

Stop if implementation lacks explicit approval; a useful removed responsibility has no safe owner; a required fact cannot fit without becoming misleading; command behavior or public facts are ambiguous; notes would need to override managed policy; a protected file changes; current user edits conflict; tests, validation, doctor, or preflight fail; or scope expands into behavior, release, external configuration, or another repository.

## Completion report format

Report the root line and section reduction, retained public responsibilities, human command surface, relocation ledger, new and reused notes, authority and upgrade outcomes, verification results, known limitations, protected surfaces, deviations, and residual risks. State that documentation changes neither approve work nor alter SE Harness behavior.
