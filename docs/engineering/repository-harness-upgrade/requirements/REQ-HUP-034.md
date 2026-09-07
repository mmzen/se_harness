+++
id = "REQ-HUP-034"
type = "requirement"
title = "Prove complete-graph operation under the 0.16.0 root and retire the last root-script consumers"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "THE SYSTEM SHALL pass validation, doctor, qualification, identical Explorer generations, the suite at baseline and the managed lane under the new root, with no consumer of a root script copy."
verification_method = ["test", "inspection"]
priority = "must"
source = "REQ-HUP-032's proof pattern for the previous adoption; SPEC-DST-025 rules DST-ENG-015 and DST-ENG-016, which bind the root-adoption work order to the owner-region lines, the SPEC-IAR-012 count and the three release workflows; the rehearsal of 2026-09-07 on the moved root"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.16.0 root and retire the last root-script consumers

## In plain words

A root move is proven by what the new evaluator reads over the whole graph
and by the test suite staying where it was. This move also takes eight
files away, so every workflow, instruction and test that read them must
read the evaluator instead.

## Why

The 0.16.0 gate read the rehearsal clone as 0.15.0 did: no error, no
advisory, the same warnings, an identical Explorer twice. Before any edit
the suite on the moved root lost six modules and read 27 failing names,
every one a read of a removed copy or of a sentence naming the eight. The
candidate must move to 0.17.0, or the derivation fails closed.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The moved root | Exact 0.16.0 validation, doctor, qualification, inspection, two generations and the review preflight pass. The derivation yields the 0.16.0 to 0.17.0 pair. The three workflows invoke the evaluator. The owner region and the specification name no managed scripts path. The suite's failure set equals the control's beyond the named edits. | The work order stops; the branch is amended or abandoned under the owner's decision |

## Examples

### Normal

**Given** the moved root, the candidate at 0.17.0 and the edits applied,

**When** the readings and the suite run,

**Then** every reading passes and the suite reads 1,265 tests with one
workstation baseline error and 26 skips.

### Failure

**Given** the candidate still at 0.16.0,

**When** the evaluator facts are derived,

**Then** the derivation fails closed with `PRE008`.

## Open decisions

None.
