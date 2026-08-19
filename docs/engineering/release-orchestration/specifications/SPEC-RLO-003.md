+++
id = "SPEC-RLO-003"
type = "specification"
title = "Repository maintenance-line reconciliation contract"
status = "approved"
owners = ["engineering-owner", "release-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
specifies = ["REQ-RLO-012"]
+++

# Specification: Repository maintenance-line reconciliation contract

## Scope

Extend only the `mmzen/se_harness` repository release orchestrator so every authorized release creates or verifies its `release/MAJOR.MINOR` maintenance line. This contract is repository policy layered after portable release governance; it is not installed, packaged, or imposed on consumers.

## Actors and external systems

- The release owner dispatches the existing one-input workflow after accountable RLS release authority exists.
- Trusted-main GitHub Actions derives and reconciles the branch using the GitHub API token scoped to repository contents.
- GitHub stores the mutable maintenance ref and immutable tag.
- Maintainers later authorize bounded patch work separately on the established line.

## Inputs

- Canonical version and exact candidate commit already derived by the trusted-main resolve job.
- Exact published GitHub Release state for the corresponding tag.
- Current GitHub branch-ref state.

## Outputs

- Derived branch name `release/MAJOR.MINOR`.
- A branch created at the candidate, or an unchanged existing branch proven to contain it.
- A bounded workflow summary containing branch name and reconciliation outcome.

## State model

1. **Unresolved:** no trusted release plan exists; no branch action is permitted.
2. **Eligible:** exact tag and GitHub Release exist for the authorized candidate.
3. **Absent:** the derived maintenance ref does not exist and may be created at the candidate.
4. **Existing-compatible:** the ref tip equals or descends from the candidate and is retained unchanged.
5. **Existing-conflicting:** the ref does not contain the candidate; reconciliation fails without mutation.

## Behavioral rules

1. Preserve exactly one required workflow input, `release_record`.
2. Accept only the already validated canonical `MAJOR.MINOR.PATCH` version emitted by release resolution.
3. Derive exactly `release/MAJOR.MINOR`; never accept operator-supplied ref text.
4. Run reconciliation only after the GitHub tag and non-draft Release are verified exact.
5. Use the existing contents-write job and GitHub token; introduce no PAT, app credential, environment, action, or package dependency.
6. When the branch ref is absent, create `refs/heads/release/MAJOR.MINOR` at the exact candidate commit through the GitHub API.
7. When the ref exists, require it to identify a commit and independently compare its tip with the candidate.
8. Treat equality or candidate-to-tip ancestry as an exact replay-compatible outcome; do not write the ref.
9. Treat a behind, diverged, malformed, inaccessible, or non-commit ref as blocking and leave it unchanged.
10. Never use force update, delete, rewind, merge, checkout-and-push, or an operator-selected branch name.
11. Emit a concise summary and job outputs for branch name and `created` or `existing` state.
12. A failure after immutable GitHub Release creation is replayable: a later rerun verifies prior exact state and retries only the missing or failed reconciliation.
13. Do not change formal artifact lifecycle state or imply authorization for maintenance work.
14. Do not edit portable code, managed installation content, consumer workflows, or consumer documentation to promise this repository policy.

## Error and recovery behavior

| Condition | Required behavior |
|---|---|
| Version does not match canonical release form | fail before branch lookup or mutation |
| Branch absent | create once at candidate; verify returned ref |
| Concurrent creator produces the same compatible branch | refetch, prove containment, and accept as existing |
| Existing tip equals candidate | accept unchanged |
| Existing tip descends from candidate | accept unchanged |
| Existing tip is behind or diverged | fail unchanged with candidate and tip identities |
| GitHub API unavailable or response malformed | fail visibly; safe workflow replay remains possible |

## Data and interface contracts

The external ref is `refs/heads/release/MAJOR.MINOR`. Candidate and tip are full repository-format commit IDs. API request bodies are generated structurally rather than interpolated as shell JSON. The workflow continues to expose only `release_record` to operators.

## Security and privacy properties

All ref names are derived from validated numeric version components. Candidate code does not execute in the contents-write job. The existing job token is the only write credential. Existing refs are never moved, and comparison occurs before accepting replay state.

## Performance and capacity

Reconciliation uses a bounded number of GitHub API requests and no repository rebuild. It adds no retry loop and no persistent service.

## Observability

The job summary records the maintenance branch, candidate prefix, and `created` or `existing` result. Failure diagnostics distinguish malformed input, missing access, and incompatible history without printing credentials.

## Compatibility and migration

Existing `release/0.2.2`, `release/0.3.0`, or `release/0.4.0` branches are historical manually named refs and are not renamed or deleted by this change. The next release automatically establishes its canonical `release/MAJOR.MINOR` line. Any desired cleanup or aliasing of legacy refs is separate repository administration.

## Examples and counterexamples

- Valid: `0.5.0` creates `release/0.5` at candidate `C`.
- Valid: a rerun sees `release/0.5` still at `C` and performs no write.
- Valid: `0.5.1` sees `release/0.5` at a descendant of candidate `P` and performs no write.
- Invalid: create `release/0.5.1`.
- Invalid: reset a conflicting `release/0.5` to `P`.
- Invalid: add maintenance-branch behavior to a standard consumer workflow or `harnessctl`.

## Explicitly unspecified decisions

The implementation agent may choose exact step names, helper decomposition inside repository-owned `.github` code, result wording, and fixture organization. Branch protection, supported-line retirement, backport policy, patch governance, and cleanup of legacy branch names remain owner-managed and outside this work.

## Approval

Approved by the accountable repository owner on 2026-08-19 through the statement `go implement` as part of the complete RLO-003 packet. Implementation authority is limited to `WO-RLO-003` and grants no production release or branch mutation.
