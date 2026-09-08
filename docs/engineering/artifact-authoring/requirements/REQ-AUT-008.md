+++
id = "REQ-AUT-008"
type = "requirement"
title = "Hold no legacy relation, unassessed completed architecture or string verification method"
status = "approved"
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

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:58:19Z"
decided_by = "product-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. The corpus-migration packet: typed relations and decision assessments for the fifteen legacy architectures, the vocabulary verification method for 271 requirements, the one-shot script retired."
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
