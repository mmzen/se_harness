+++
id = "REQ-AUT-009"
type = "requirement"
title = "Keep no compatibility window for a migrated corpus"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-09"
updated = "2026-09-09"
statement = "THE VALIDATOR SHALL refuse a legacy constrains relation, an unassessed completed architecture, a header-less evidence packet and a v1 quality-gates contract, with no warning path tolerating any of them."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #381 owner decision 3 of 2026-09-07 (migrate the corpus, then close the windows) and SPEC-AUT-003 AUT-MIG-012; re-measured on main at 4ea947be on 2026-09-09: 0 architectures with constrains, 0 completed architectures without a decision assessment, W014 and W015 at 0 under the released 0.16.0 evaluator"
measure = "W014, W015, W019 and W-ECP-002 absent from the package and from the diagnostic-code index; validate on the candidate 0 errors with every other count at the baseline; each of the four refusals named by a test"

[relations]
derives_from = ["CAP-AUT-001"]
+++

# Requirement: Keep no compatibility window for a migrated corpus

## In plain words

Four places still accept a shape the corpus no longer holds, with a
warning. Each warning becomes the refusal that already exists beside it.

## Why

`WO-AUT-005` migrated the corpus on 2026-09-08, so the legacy architecture
warnings `W014` and `W015` have had nothing to report since. The
one-release grace for packets bound by substring has served its release.
The v1-schema hint names a contract no installed repository carries. A
window with no end is a second code path. On 2026-09-07 the owner decided to
close the windows once the corpus was clean and to keep two historical
gaps, written down as permanent.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| an architecture declares the retired relation | an error naming it | a warning, or silence |
| a completed architecture lacks its decision assessment | the assessment is required | a warning naming a window |
| an evidence packet has no machine header | not assessable, naming the corrective command | the substring fallback passes it |
| a quality-gates contract carries the retired schema | the loader's own schema error | a hint naming a retired schema |
| a record lacks its preparation timestamp, a work order its scope | unchanged, documented as permanent | closed, or left undocumented |

## Examples

### Normal

**Given** the candidate after this change,

**When** the validator runs on this repository,

**Then** it reports no error and every count equals the baseline.

### Failure

**Given** an approved architecture with the retired relation added,

**When** the validator runs,

**Then** it reports an error naming the relation.
