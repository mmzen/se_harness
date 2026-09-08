+++
id = "REQ-CIP-008"
type = "requirement"
title = "Qualify and test each pull-request commit once"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN a pull request is pushed, THE PIPELINE SHALL run the complete-candidate qualification and the full test suite once for that commit."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #380 (code health assessment 2026-09-07, section 2.2 and the wave 5 plan), re-measured on main at a68caf70 on 2026-09-08: candidate-evidence.yml lines 63 to 74 and release-qualification.yml lines 115 to 128, called by publication-rehearsal.yml lines 82 to 89"
measure = "the pull request's run list shows one qualify complete-candidate invocation and one full-suite run for the head commit, both in candidate-evidence; the rehearsal's candidate leg replays the recipe only"

[relations]
derives_from = ["CAP-CIP-001"]
+++

# Requirement: Qualify and test each pull-request commit once

## In plain words

Every pull request runs its longest check twice on the same commit. After
this change it runs once, and the release path keeps its own copy.

## Why

The candidate-evidence lane qualifies the complete candidate and runs the
suite. The publication rehearsal then invokes the release qualification in
candidate mode, which repeats both on the same commit. `ADR-CIP-001` keeps
the qualification inside the definition the release executes, so the
release-record leg must keep it. The candidate leg only needs the recipe
replay, which no other lane performs.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a pull request is pushed | the candidate-evidence lane qualifies the candidate and runs the suite once; the rehearsal's candidate leg replays the build recipe only | a suite test names the second lane that qualifies or tests |
| a release record is qualified | the release-record leg still qualifies the candidate, runs the suite and replays the bound recipe | the lane fails as it does today |

## Examples

### Normal

**Given** a pull request at commit C,

**When** its lanes finish,

**Then** the run list shows one qualification and one suite run for C, and
the candidate leg's log holds a replay and no test run.

### Failure

**Given** a scratch copy where the release-record condition is removed from
the qualification step,

**When** the suite runs,

**Then** the one-run test fails and names the qualification workflow.
