+++
id = "REQ-CIP-010"
type = "requirement"
title = "Name the rehearsal job by its current name in the approved pipeline definitions"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-10"
updated = "2026-09-10"
statement = "THE APPROVED PIPELINE DEFINITIONS SHALL name the upgrade rehearsal job by its current name and record the removal of the reconcile job by amendment."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #433 finding 2; WO-CIP-007 handoff disclosure 4 and its retired-names.md; measured on main at f0a3a223: ARCH-CIP-001 line 43 and REQ-CIP-002 lines 27, 29, 41 and 49 still name governance-migration, renamed upgrade-rehearsal by WO-CIP-007 (PR #419, VREC-CIP-007) whose scope admitted specifications/, REQ-CIP-008 and REQ-CIP-009 only"
measure = "grep governance-migration over docs/engineering/ci-pipeline/architecture and requirements returns only lines inside an amendment record, and a test pins it"

[relations]
derives_from = ["CAP-CIP-001"]
+++

# Requirement: Name the rehearsal job by its current name in the approved pipeline definitions

## In plain words

Two approved pipeline definitions still call a job by a name it lost. Each
gets a dated amendment that gives the current name and explains the change.

## Why

`WO-CIP-007` renamed the rehearsal job `upgrade-rehearsal` with its artifact,
needs entry and outputs, and the reconcile job had already left the workflow.
Its scope admitted the specifications directory and its own two requirements,
so the architecture and the earlier requirement kept the old name. Both carry
lifecycle events, so the fix is an amendment on each, in prose, under a
bounded repair work order. No identifier, statement or relation moves.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a reader consults either definition | the prose names the job by its current name and an amendment record dates the change | a test names the stale line |
| the old name is searched under the domain's architecture and requirements | every hit is inside an amendment record | the test names the file and line |

## Examples

### Normal

**Given** the repaired definitions,

**When** the old name is searched under the two directories,

**Then** only the two amendment records answer.

### Failure

**Given** one definition still naming the job in its components section,

**When** the suite runs,

**Then** the definitions test fails naming the file and line.
