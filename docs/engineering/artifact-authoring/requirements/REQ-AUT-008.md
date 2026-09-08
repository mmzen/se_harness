+++
id = "REQ-AUT-008"
type = "requirement"
title = "Hold no legacy relation, unassessed completed architecture or string verification method"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE FORMAL ARTIFACTS SHALL hold no legacy constrains relation, no completed architecture without a decision assessment, and no string verification method."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #381 owner decision 3 of 2026-09-07 (migrate the corpus, then close the windows) and issue #380 (finish or delete the verification-method migration); re-measured on main at a68caf70 on 2026-09-08: 15 architectures with constrains, 14 without decision_assessment, 271 of 359 requirements with a string verification_method"
measure = "validator W014 and W015 counts 0 on the candidate; 0 requirements with a string verification_method; the migration script absent from scripts/"

[relations]
derives_from = ["CAP-AUT-001"]
+++

# Requirement: Hold no legacy relation, unassessed completed architecture or string verification method

## In plain words

Three compatibility windows in the validator stay open because the corpus
still holds what they tolerate. This requirement moves the corpus so the
windows can close.

## Why

Fifteen implemented architectures still declare the retired relation and
fourteen carry no decision assessment. Two maintenance warnings therefore
fire on every validation, and two code branches exist for them alone. The
closed verification vocabulary was approved, but its migration was never
applied because the root evaluator then required strings; it does not now.
A window with no end date is a permanent second code path. The owner decided
on 2026-09-07 to migrate first and close afterwards.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the validator runs on the candidate | `W014` and `W015` are absent, and every requirement's verification method is an array from the vocabulary | the validator names the file |
| a later candidate closes the windows | no artifact needs to change for it | the closing work order stops |

## Examples

### Normal

**Given** the candidate after this change,

**When** the released 0.16.0 evaluator validates it,

**Then** the maintenance plane carries neither legacy warning, and a scan
finds no string verification method.

### Failure

**Given** a scratch copy where one architecture keeps its legacy relation,

**When** the validator runs,

**Then** the legacy-relation warning names that architecture and the corpus
test fails.
