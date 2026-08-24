+++
id = "WO-RLO-005"
type = "work_order"
title = "Rehearse the credential-free last mile on both runner platforms"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "A green rehearsal becomes a pre-release assurance signal for both runner platforms, and the divergence seam becomes a required check whose failure blocks integration; both must be bound to the exact candidate that produced them."
decided_by = "repository-owner"

[relations]
implements = ["REQ-RLO-015", "REQ-RLO-016"]
specifications = ["SPEC-RLO-005"]
verification = ["VER-RLO-005"]
architecture = ["ARCH-RLO-005", "ADR-RLO-005"]

[execution_scope]
paths = [
  ".github/scripts/rehearse_publication.py",
  ".github/scripts/publication_rehearsal_mechanics.json",
  ".github/workflows/publication-rehearsal.yml",
  "tests/test_publication_rehearsal.py",
  "tests/fixtures/publication_rehearsal/",
  "docs/engineering/release-orchestration/README.md",
  "docs/engineering/release-orchestration/capabilities/CAP-RLO-003.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-015.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-016.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-005.md",
  "docs/engineering/release-orchestration/architecture/ARCH-RLO-005.md",
  "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-005.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-005.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-005.md",
  "docs/engineering/release-orchestration/acceptance/publication-rehearsal.feature",
  "docs/engineering/release-orchestration/evidence/WO-RLO-005-implementation.md",
  "docs/notes/release-publication-rehearsal.md",
  "docs/notes/README.md",
]
+++

# Work Order: Rehearse the credential-free last mile on both runner platforms

## Lifecycle

Issue [#111](https://github.com/mmzen/se_harness/issues/111) records `RC-060-11` from the immutable `0.6.0` release recovery analysis. Its authority boundary states that creating the issue authorizes no implementation, so the issue alone granted nothing.

On 2026-08-24 the accountable repository owner stated `OK go for #111`, and in the same turn selected `Parallel lane + drift check` over a refactor of the release orchestrator, and `Fourth release-orchestration packet` as the governance home. That statement approves the complete `RLO-005` definition packet, authorizes this work order, and transitions it to `in_progress`. Completed work will transition only to `implemented`; release or operational reliance requires a later clean candidate, a ready VREC, an accountable assurance decision, and a governance commit. No production tag, branch, release, package publication, deployment, environment approval, push, or pull request is authorized by this transition.

The implementation is complete at candidate commit `cfca2f350bd9aede69c336605d2b68fc50ffc29c`, and this work order moves to `implemented` in the following commit together with `evidence/WO-RLO-005-implementation.md`. That evidence records seven amendments to already-approved artifacts made during implementation; none changes an approved `statement` field.

On 2026-08-24 the accountable repository owner took three decisions on that evidence. They accepted all seven amendments, `A1` through `A7`, which is recorded in the amendments section of `SPEC-RLO-005`, `REQ-RLO-015`, and `VER-RLO-005`. They ruled that `excluded` is the correct report for the predecessor-view mechanic in `candidate` mode, because ordinary integration offers no valid subject while `release-record` mode still fails on a real mismatch; `SPEC-RLO-005` rule 37 and `VER-RLO-005` carry that ruling. And they authorized pushing this branch and opening a pull request carrying a `Harness-Work-Order: WO-RLO-005` trailer, which is the rehearsal lane's first hosted run on both runner types.

`commit_bound_verification` remains `required` and unmet: no `VREC` exists. Nothing above authorizes a workflow dispatch of the release orchestrator, a tag, a release, a publication, a deployment, or an environment approval.

## Objective

Exercise every credential-free publication mechanic on both the Linux and the Windows runner type before release approval, and make divergence between that rehearsal and the release orchestrator a fail-closed check, without modifying the release orchestrator or any publication behavior.

## In scope

- A repository-owned rehearsal program that resolves the platform virtual-environment layout, canonicalizes its root, establishes and asserts temporary-path identity, exports the candidate twice, drives the same qualification, test, build, normalization, manifest, and verification tools publication drives, compares the two distribution sets byte for byte, and tears down its derived trees without following links.
- A `candidate` mode over the current candidate and a `release-record` mode a release owner can dispatch against a prepared record before approving it, with the result stating which mode produced its verification.
- A data-only declaration of the mechanics the rehearsal covers, and a divergence checker that classifies orchestrator jobs by declared attributes and fails closed on an uncovered or stale mechanic.
- A repository-owned rehearsal workflow with a Linux and Windows matrix, `contents: read` only, pull-request and `main` triggers, and the release-owner dispatch input.
- The negative matrix and boundary tests required by `VER-RLO-005`, with fixtures.
- Repository-owned documentation of the rehearsal for human readers, the release-orchestration domain index, and retained evidence.

## Out of scope

- Any change to `.github/workflows/publish-pypi.yml`, including its input surface, permissions, job structure, ordering, or behavior.
- Any change to `harnessctl`, packaged `se_harness` modules, portable artifact schemas, the managed validator, the eight managed `scripts/` files, managed policy documents, standard templates, `.engineering-harness.lock`, consumer workflows, or consumer documentation.
- Refactoring the orchestrator's credential-free mechanics into a shared implementation; `ADR-RLO-005` defers that with a recorded revisiting condition.
- Reimplementing normalization, manifest, plan, verification, or qualification behavior rather than invoking it.
- Extending the integration-package lane, which `REQ-IPK-003` bars from release authority, or adding a dry-run input to the orchestrator.
- Rehearsing credential-bearing stages: tag creation, GitHub Release materialization, PyPI promotion, Pages deployment, and public-install observation.
- Building a promotable release distribution, preparing or transitioning a release record, creating a tag, branch, release, index object, or deployment, approving an environment, or changing hosting settings as implementation evidence.
- Committing, pushing, or opening a pull request beyond what the owner separately authorizes.

## Authorized decision envelope

The implementation agent may choose the rehearsal program's module layout and subcommand names, mechanic identifier spelling, result schema field names, workflow and job names, step naming, and fixture organization.

The agent may not modify the release orchestrator, add a credential, token, environment, or write permission anywhere, hardcode a platform virtual-environment layout, invoke `cygpath` or a POSIX-only utility, allow a silent skip, match a mechanic by name similarity, downgrade a divergence to a warning, let the declaration contain logic, delete outside the rehearsal root, or change portable, managed, or consumer surfaces.

## Constraints

- `.github/workflows/publish-pypi.yml` must remain byte-identical to its merge-base content.
- Candidate code must execute with no credential, preserving the property `INT-RLO-001` requires of publication.
- Preserve the `RLO-001` through `RLO-003` guarantees and the portable boundary from `ADR-RLO-002`.
- Treat orchestrator YAML, declaration data, downloaded bytes, subprocess output, filesystem state, and link targets as untrusted.
- Keep the rehearsal runnable locally on a single platform so a hosted failure is reproducible.
- The implementer can directly execute only one of the two platforms; the other must be covered by injected platform state and reported as such, never claimed as measured.
- Preserve unrelated changes and historical artifacts.

## Expected change surface

- `.github/scripts/rehearse_publication.py` and its data-only mechanic declaration.
- `.github/workflows/publication-rehearsal.yml`.
- `tests/test_publication_rehearsal.py` and `tests/fixtures/publication_rehearsal/`.
- Formal `RLO-005` artifacts, the acceptance feature, the domain index, and retained evidence.
- Repository-owned notes describing the rehearsal for human readers.

## Required verification

- Approved start and review preflight for `WO-RLO-005`.
- Every case, property, and static check in `VER-RLO-005`, including both divergence directions, the data-only declaration property, link-escape refusal, and the byte-unchanged orchestrator.
- A full local rehearsal run on the implementer's platform, with its complete per-mechanic result retained.
- Full repository unit suite, compared by failure name against a baseline measured in a clean worktree at the same commit.
- Root frozen validator, candidate validator, `validate_release_distributions.py`, `python -m se_harness --help`, `doctor`, and the governing released evaluator from outside the checkout.
- `git diff --check`, and changed-path, built-wheel, and standard-template boundary inspection.
- Hosted pull-request checks, without dispatching the release workflow.

## Evidence to record

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-005-implementation.md` with the candidate under measurement, changed surfaces, the mechanic table with per-platform outcomes and the explicit distinction between measured and injected platform coverage, the complete negative-case matrix with exact diagnostic text, both divergence verdicts, the byte-unchanged orchestrator proof, local transcripts, before-and-after test and validator counts, preflight and graph results, boundary inspection, warnings, residual risks, and every production and external action not performed.

## Stop and escalate conditions

Stop for an invalid graph, a need to modify the release orchestrator, a need for a credential, token, environment, or write permission, an orchestrator job that cannot be classified, a mechanic that cannot be rehearsed on a platform without a silent skip, a determinism failure in the current candidate, a required managed-file or portable-surface change, an inability to tear down without leaving residue or following a link, or a need for production or external mutation as evidence.

## Completion report format

Report the implemented requirements; exact program, declaration, workflow, test, fixture, documentation, and evidence paths; the per-mechanic outcome table with measured versus injected platform coverage; both divergence verdicts; the byte-unchanged orchestrator proof; test counts against the measured baseline; validator and preflight results; warnings and residual risk; the evidence path; the candidate and VREC plan; and every commit, push, pull request, tag, branch, release, publication, deployment, and environment action not performed.
