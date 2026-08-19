+++
id = "WO-RLO-003"
type = "work_order"
title = "Automate the SE Harness maintenance line"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[assurance]
commit_bound_verification = "required"
rationale = "Future releases will rely on changed credentialed repository workflow behavior, mutable-ref conflict handling, replay safety, and preservation of the portable-product boundary."
decided_by = "repository-owner"

[relations]
implements = ["REQ-RLO-012"]
specifications = ["SPEC-RLO-003"]
verification = ["VER-RLO-003"]
architecture = ["ARCH-RLO-003", "ADR-RLO-003"]
+++

# Work Order: Automate the SE Harness maintenance line

## Lifecycle

The accountable repository owner requested automated maintenance-branch creation and explicitly constrained it to the `se_harness` repository, with no change to the SE Harness governance tool. That statement authorized preparation of this definition packet but did not authorize executable workflow changes.

On 2026-08-19 the accountable repository owner stated `go implement`. This approves the complete RLO-003 definition packet, authorizes `WO-RLO-003`, and transitions it to `in_progress`. Completed work will transition only to `implemented`; release or operational reliance requires a later clean candidate, ready VREC, accountable assurance decision, and governance commit. No production branch, release, publication, deployment, environment approval, commit, push, or PR is authorized by this transition.

On 2026-08-19 the bounded repository implementation and local verification completed successfully, so this work order transitioned to `implemented`. Retained evidence is `docs/engineering/release-orchestration/evidence/WO-RLO-003-verification.md`. No commit-bound VREC, assurance decision, release, production branch, publication, deployment, environment approval, commit, push, or PR is implied.

## Objective

Complete the repository-specific release last mile by deterministically creating or verifying `release/MAJOR.MINOR` from the authorized candidate while preserving one-input operation, safe replay, and the strict boundary around portable SE Harness.

## In scope

- Derive the canonical maintenance-line name from the resolved release version.
- Create an absent line at the exact released candidate after exact GitHub release materialization.
- Accept an existing line without mutation only when it equals or descends from the candidate.
- Fail visibly and non-destructively for conflicts, malformed state, or API failure.
- Report branch identity and reconciliation outcome in repository workflow results or summaries.
- Add isolated repository-policy tests and acceptance coverage.
- Update only repository-specific release context, domain guidance, and development documentation needed to describe the behavior.

## Out of scope

- Any change to `harnessctl`, packaged `se_harness` modules, portable artifact schemas, managed validator, standard templates, consumer workflows, installation, adoption, upgrade, or governor reconciliation.
- Adding workflow inputs, per-patch branch names, general branching automation, consumer policy, a plugin, or a reusable product feature.
- Force-updating, deleting, rewinding, merging, repairing, protecting, retiring, or backporting a maintenance branch.
- Renaming/deleting historical `release/0.2.2`, `release/0.3.0`, or `release/0.4.0` branches.
- Preparing or transitioning a release record, creating a production branch/tag/release, publishing packages, deploying Pages, approving an environment, or modifying hosting settings as implementation evidence.

## Authorized decision envelope

After separate work-order approval, the implementation agent may choose whether the bounded logic remains inline in the repository workflow or uses a repository-owned `.github` helper, exact output names, and test fixture organization.

The agent may not add an operator-controlled branch input, use a `release/x.y.z` name, update an existing ref, expand credential scope, execute candidate code with write authority, or change portable/consumer surfaces.

## Constraints

- Preserve `.github/workflows/publish-pypi.yml` as the stable repository-specific PyPI identity and its single `release_record` input.
- Preserve exact candidate, tag, distribution, GitHub Release, PyPI, Pages, and result guarantees from RLO-001/RLO-002.
- Use only the existing job-scoped GitHub token and contents permission.
- Treat all hosting responses as untrusted and keep calls bounded.
- Preserve unrelated changes and historical artifacts.
- Implementation verification must not mutate production refs or other external release state.

## Expected change surface

- Repository-specific release workflow and, only if needed, `.github` release helper logic.
- Release-orchestration workflow-policy/state tests and acceptance scenarios.
- Repository context, release-orchestration domain index, and implementation-repository development guidance.
- Formal RLO-003 artifacts and retained evidence.

## Required verification

- Approved start/review preflight for `WO-RLO-003`.
- Every fixture and invariant in `VER-RLO-003`, including concurrent-create recovery and zero-write conflict behavior.
- Strict workflow YAML parsing, one-input/permission/action/ordering/candidate-execution checks, and regression of RLO-001/RLO-002 publication behavior.
- Full repository unit suite on default Python and Python 3.11 where available.
- Formal graph validation, doctor, repository release-policy validation, `git diff --check`, and changed-path/package/template boundary checks.
- Hosted PR checks without dispatching the production release workflow.

## Evidence to record

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-003-verification.md` with approval, changed surfaces, state/API matrix, test commands and counts, workflow trust comparison, portable-boundary proof, graph/preflight results, deviations, residual risks, and every production action not performed.

## Stop and escalate conditions

Stop for an invalid graph, ambiguous support-line policy, need for another workflow input, need to move an existing ref, candidate execution in a write job, new credential/environment, package or managed-template change, unbounded API behavior, inability to distinguish compatible history, regression of publication guarantees, or production mutation needed as evidence.

## Completion report format

Report implemented requirement; exact workflow/helper/documentation paths; absent/equal/descendant/conflict/concurrency outcomes; one-input and permission comparison; portable surfaces proven unchanged; test counts; graph/preflight result; warnings and residual risk; evidence path; candidate/VREC plan; and every commit, push, PR, production branch/tag/release/publication/deployment/environment action not performed.
