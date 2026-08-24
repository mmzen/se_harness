+++
id = "REQ-RLO-014"
type = "requirement"
title = "Fail closed when publication mechanics diverge from the rehearsal"
status = "approved"
owners = ["quality-owner", "release-owner", "engineering-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN the credential-free mechanics declared by the publication orchestrator and the mechanics covered by the cross-platform rehearsal differ in either direction, THE SYSTEM SHALL fail a required check that names the divergence, and SHALL NOT treat an uncovered or stale mechanic as rehearsed."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-RLO-003"]
+++

# Requirement: Fail closed when publication mechanics diverge from the rehearsal

## Rationale

The accountable repository owner chose to leave `.github/workflows/publish-pypi.yml` unchanged, so the rehearsal is a second lane rather than a shared implementation. A second lane can drift. Drift is worse than no rehearsal, because a green rehearsal that no longer matches publication is a false assurance signal on exactly the path `RC-060-11` says was trusted too early.

Sameness therefore has to be enforced by a check rather than assumed. Divergence matters in both directions. If publication gains a credential-free step the rehearsal does not exercise, that step reaches a release unexercised — the original defect. If the rehearsal keeps exercising a mechanic publication no longer performs, the rehearsal reports coverage that protects nothing and hides the shrinking real surface.

## Preconditions and trigger

The publication orchestrator and the rehearsal both exist in the repository. The check runs whenever either is changed and on every ordinary candidate integration, with no credential and no dispatch of the release workflow.

## Required response

Parse the publication orchestrator strictly, identify its credential-free jobs, and extract the mechanics they invoke. A job is credential-free only if it is credential-free itself *and* depends on no excluded job, because a job that consumes state produced by a credential-bearing job runs after a credential has been used. Compare the resulting set against a data-only declaration of the mechanics the rehearsal covers. Report each mechanic as covered, uncovered, or stale. Fail when any mechanic is uncovered or stale, naming the mechanic, the orchestrator location, and the direction of the divergence. Compare each credential-free step by a digest of its script as well, so a change inside an already-declared step cannot pass. Classify the action surface of those jobs too, refusing an undeclared action and an action not pinned to a full commit. Confirm that the orchestrator's credential-free jobs still declare the platforms the rehearsal claims to complement, and that the rehearsal lane declares both platforms.

## Failure and boundary behavior

An unparseable orchestrator, an unrecognized job permission shape, a job that cannot be classified as credential-bearing or credential-free, or a declaration that is not data-only fails the check. The check must never repair the divergence, edit either side, weaken its comparison to make a change pass, or downgrade a divergence to a warning. A mechanic must not be treated as covered because its name is similar to a covered one.

## Constraints

- The declaration of covered mechanics must be data only, with no executable logic, so it cannot silently satisfy itself.
- The check must classify jobs by their declared permissions, environments, secret or token use, use of actions that mutate external state, and dependencies on excluded jobs, rather than by job name. An absent permission block is an excluding attribute, not a permissive default.
- The check must run from a bare interpreter, so it may not add a parsing dependency to the repository. An independent second parser may be cross-checked when it happens to be available, and the check must fail rather than fall back silently when that cross-check is requested and the parser is absent.
- Do not modify the publication orchestrator to make the comparison easier.
- Do not change portable `se_harness`, managed templates, the managed validator, or consumer surfaces.
- A passing check is not release authority and not evidence that publication succeeds.

## Acceptance examples

### Example: publication gains an unrehearsed credential-free step

**Given** a credential-free job in the orchestrator invokes a mechanic absent from the declaration

**When** the divergence check runs

**Then** it fails, names the mechanic and its orchestrator location, and reports the divergence as uncovered.

### Example: the rehearsal declares a mechanic publication dropped

**Given** the declaration names a mechanic the orchestrator no longer invokes

**When** the divergence check runs

**Then** it fails and reports the declaration entry as stale.

### Example: a credential-bearing job is not required to be rehearsed

**Given** a job declares `contents: write`, an `id-token` permission, a protected environment, secret or token use, or an action that mutates external state

**When** the check classifies jobs

**Then** that job's mechanics are excluded from the required rehearsal set, and the exclusion is reported together with the attribute that caused it, never silently dropped.

### Example: exclusion reaches a job that holds no credential of its own

**Given** a job declares only `contents: read` but `needs` a job that was excluded

**When** the check classifies jobs

**Then** that job is excluded too, and the reported attribute names the excluded dependency.

### Example: a declared step changes without changing any command

**Given** a declared credential-free step gains an argument, so every command it invokes is still declared

**When** the divergence check runs

**Then** it fails because the step's script digest no longer matches the declared digest, naming the job, the step, and both digests.

### Example: platform claims are checked

**Given** the orchestrator's credential-free jobs declare the Linux and Windows runner types

**When** the check inspects the rehearsal lane

**Then** it confirms the rehearsal declares both platforms, and fails if either is missing.

### Example: the declaration cannot be executable

**Given** the declaration of covered mechanics

**When** it is inspected

**Then** it contains only data, and a declaration containing executable logic fails the check.

## Open decisions

Whether the divergence check should eventually be satisfied by refactoring the orchestrator to share one implementation, which would make sameness structural instead of checked, remains open. The owner explicitly deferred that refactor to avoid changing the live release path in this work; `ADR-RLO-004` records the trade.

## Approval

Approved by the accountable repository owner on 2026-08-24 through the statement `OK go for #111` together with the selected `Parallel lane + drift check` design, which makes this fail-closed check the condition of that choice. This approves the requirement definition and the bounded implementation in `WO-RLO-004`; it authorizes no release, publication, deployment, or external action.

## Amendments during implementation

Three amendments were made while implementing `WO-RLO-004`, each stated for owner acceptance or rejection. All three narrow what passes the check.

- **Transitive exclusion.** The required response and the constraints now state that exclusion propagates through `needs`, and a new acceptance example covers it. Classifying the real orchestrator found that `observe` declares only `contents: read` and would have been treated as a rehearsal obligation although it runs only after `github_release` has used a credential. A fixture that omitted `permissions` entirely showed the same gap from the other side, so an absent permission block is now named as excluding.
- **Step-digest comparison.** The required response now compares a digest of each credential-free step's script. Command-level comparison alone is blind inside a declared step: a new flag or a reordered command leaves every command already declared, so the check would have reported coverage of an orchestrator it no longer matched.
- **No new parsing dependency.** The constraints now state that the check runs from a bare interpreter with an optional independent cross-check, because `pyproject.toml` declares no dependencies and the check must not be the first to add one. The statement's word "strictly" is unchanged; a bounded reader restricted to the Actions subset satisfies it, and both parsers were confirmed to agree about the orchestrator.

The `statement` field is unchanged. These amendments describe how the required response detects divergence, not what divergence means.
