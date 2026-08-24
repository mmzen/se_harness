+++
id = "REQ-RLO-015"
type = "requirement"
title = "Rehearse the credential-free publication path on every runner platform"
status = "approved"
owners = ["release-owner", "quality-owner", "engineering-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "BEFORE release approval, THE SYSTEM SHALL execute every credential-free publication mechanic on both the Linux and the Windows runner type using the same shells, virtual-environment layouts, temporary paths, build commands, tests, bundle checks, and teardown behavior the publication orchestrator uses, and SHALL create no tag, release, package, deployment, or lifecycle record."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-RLO-003"]
+++

# Requirement: Rehearse the credential-free publication path on every runner platform

## Rationale

The credential-free portion of `.github/workflows/publish-pypi.yml` is split across two jobs that each run on exactly one platform. `resolve` runs only on `ubuntu-latest` and proves evaluator identity through the POSIX virtual-environment layout `evaluator-env/bin/python` and `evaluator-env/bin/harnessctl`. `qualify` runs only on `windows-2022` and performs candidate export, build, sdist normalization, and bundle verification through `cygpath` path conversion and a re-pointed `TEMP`/`TMP` pair. `cygpath` does not exist on Linux, and the POSIX layout does not exist on Windows, so neither half is ever exercised on the other platform.

`RC-060-11` records the consequence: local Windows qualification missed POSIX virtual-environment and cleanup behavior, while Ubuntu-oriented workflow work missed Git Bash path conversion, Windows short-name aliases, and temporary-path identity. Incidents `I-15` and `I-16` are the observed failures — Windows publication could not open export paths, and seven Windows tests failed on two spellings of the same temporary path. Both surfaced during a live release because no earlier run exercised those boundaries.

## Preconditions and trigger

A candidate commit exists in the repository. No released release record, publication credential, protected environment, or accountable release decision is required. The rehearsal is triggered by ordinary candidate integration and may additionally be dispatched by the release owner against a prepared release record before approving it.

## Required response

Run one rehearsal lane on the Linux runner type and one on the Windows runner type. On each platform, execute the credential-free mechanics with platform-correct handling of virtual-environment layout, path form, temporary-path identity, and teardown, and report per-mechanic outcomes for both platforms. Prove build determinism by producing two independent distribution sets from the same candidate and comparing them byte for byte. Remove every derived tree the rehearsal created and prove no residue remains outside it. Report the condition of the inherited checkout alongside the outcomes, because a mechanic that a dirty worktree makes impossible must be attributable to the checkout rather than read as a defect in the publication path.

## Failure and boundary behavior

A failure on either platform fails the rehearsal visibly and names the platform, the mechanic, and the observed divergence. A mechanic that cannot run on a platform must fail rather than be silently skipped; a deliberately excluded mechanic must be declared and reported as excluded with its reason. The rehearsal must never acquire a publication credential, request a protected environment, create or move a ref, upload a distribution to an index, deploy a site, or transition a formal artifact.

## Constraints

- This is policy of the `mmzen/se_harness` implementation repository only.
- Do not modify `.github/workflows/publish-pypi.yml` or any behavior of the authorized release transaction.
- Drive the same underlying tools the orchestrator drives rather than reimplementing their behavior.
- Do not change `harnessctl`, packaged `se_harness` modules, portable artifact schemas, the managed validator, standard templates, consumer workflows, or consumer documentation.
- Rehearsal output is derived operational evidence and grants no formal authority.
- Keep the rehearsal runnable by an engineer on one platform locally, so a defect can be reproduced without a hosted run.

## Acceptance examples

### Example: Windows exercises the POSIX-shaped evaluator stage

**Given** the rehearsal runs on the Windows runner type

**When** it reaches the evaluator identity mechanic that publication performs only on Linux

**Then** it resolves the `Scripts` virtual-environment layout, proves evaluator identity, and reports the mechanic as executed on Windows.

### Example: Linux exercises the Windows-shaped build stage

**Given** the rehearsal runs on the Linux runner type

**When** it reaches candidate export, deterministic build, sdist normalization, and bundle verification, which publication performs only on Windows

**Then** it completes each mechanic without `cygpath`, and the two independent distribution sets compare byte-identical.

### Example: temporary-path identity is the same on both platforms

**Given** a temporary root reached through an alias such as a Windows 8.3 short name or a symlinked POSIX parent

**When** the rehearsal resolves its working root

**Then** it canonicalizes the root before creating a virtual environment, and the path it reports equals the path the tools observe.

### Example: teardown does not escape the derived tree

**Given** a rehearsal tree containing a POSIX virtual environment with symlinks, or a Windows environment with linked entries

**When** teardown runs

**Then** every derived tree is removed, no link target outside the tree is followed or deleted, and the repository worktree remains clean.

### Example: no external state is created

**Given** any rehearsal outcome, successful or failed

**When** repository and external state are inspected

**Then** no tag, branch, GitHub Release, index upload, Pages deployment, environment approval, or artifact lifecycle transition exists as a result of the rehearsal.

## Open decisions

Whether the rehearsal should additionally reproduce an already-published release byte for byte as a standing regression is not settled by this requirement. The dispatchable release-record mode makes that possible for an operator; making it a required gate would bind candidate CI to historical distribution bytes and requires later governed work.

## Approval

Approved by the accountable repository owner on 2026-08-24 through the statement `OK go for #111` together with the selected `Parallel lane + drift check` design. This approves the requirement definition and the bounded implementation in `WO-RLO-005`; it authorizes no release, publication, deployment, or external action.

## Amendments during implementation

Two amendments were made while implementing `WO-RLO-005`, both accepted by the accountable repository owner on 2026-08-24 through the statement `Accept all seven`, which covers the seven amendments recorded across `SPEC-RLO-005`, this requirement, and `VER-RLO-005`. Neither relaxes the required response; both add to it. The `statement` field is unchanged, and the acceptance authorizes no release, publication, deployment, or other external action.

**The required response now reports the condition of the inherited checkout.** The constraint on line 43 keeps the rehearsal runnable locally, and a local run inherits whatever worktree the engineer is in. Two shakedown runs measured the consequence on the same mechanic, the predecessor-view qualification. It requires a clean worktree, so while the packet under construction was uncommitted it failed with `PV001`, "predecessor preparation requires a clean Git worktree". After the packet was committed it failed again under the same `PV001` identifier and an entirely different message, "evaluator wheel differs from the released RLS contract", which `SPEC-RLO-005` amendment A7 traces to the subject the rehearsal chose rather than to the checkout. One identifier covering two unrelated causes is why the two were initially conflated. Without the inherited condition on the result neither is distinguishable from a real defect in the publication path, which is the false signal this requirement's sibling `REQ-RLO-016` exists to prevent.

**The reported condition includes line-ending conversion, not only worktree cleanliness.** The orchestrator runs the unit suite inside a `git worktree add` checkout and the rehearsal does the same, so that checkout inherits `core.autocrlf` from the repository it was created in. Measured on this implementer's Windows checkout with `core.autocrlf=true`, the candidate unit suite reports four failures whose assertions are on exact bytes; the same commit and the same mechanic are green in a `core.autocrlf=false` clone. That is a property of the checkout, not of the publication path, and it is reported for the same reason worktree cleanliness is.

**A third amendment came later and from a different cause, so it was accepted separately rather than under that statement.** `main` advanced while this branch was open and added a recipe-bound build replay to the orchestrator's credential-free surface. That mechanic cannot be executed by this rehearsal on either runner type: it pulls and runs an immutable `linux/amd64` container producer, which the Windows runner type cannot run at all, and it requires a released distribution-schema-2 record with a bound recipe, which the repository does not yet have. It is therefore declared and reported `excluded` with a measured reason in both modes, under the failure-and-boundary sentence above that already requires a deliberately excluded mechanic to be declared and reported with its reason. The repository's dedicated credential-free replay lane, added by the same change to `main`, is what exercises it. This narrows what "every credential-free publication mechanic" achieves in practice without relaxing the required response. It was put to the accountable repository owner separately, because the earlier acceptance predates it, and they accepted it on 2026-08-24 through the statement `Accept A8 and A9`; `SPEC-RLO-005` amendment `A9` records the measurement in full and the framing that decision was taken over.
