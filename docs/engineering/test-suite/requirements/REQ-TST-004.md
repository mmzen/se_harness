+++
id = "REQ-TST-004"
type = "requirement"
title = "Run each test once, share one helper per fixture need, and pin only cited wording"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE TEST SUITE SHALL run each defined test once, share one helper per fixture need, and pin only wording a specification cites."
verification_method = ["test", "inspection", "analysis"]
priority = "should"
measure = "the loader's discovered count equals the defined count; one invoke, one git, one write and one formal definition under tests/; no test module imports another; the Linux-lane wall time recorded before and after and lower; every specification-cited pin present"
source = "issue #379 (code health assessment 2026-09-07, section 5 and the wave 4 plan), re-measured on main at 50f9cda5 on 2026-09-08"

[relations]
derives_from = ["CAP-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T12:53:14Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all four (Recommended)', given after the wave 4 packet for issue #379 (code health assessment 2026-09-07, section 5 and the wave 4 plan) was presented: one run per test, shared support modules, one retired-surface table, cited pins. Approval of a definition authorizes no work."
+++

# Requirement: Run each test once, share one helper per fixture need, and pin only cited wording

## In plain words

The suite re-runs a fifth of its tests by accident, copies its helpers
across modules, and freezes sentences that no rule fixes. This requirement
removes all three.

## Why

About two hundred and fifty re-runs cost a third of the parallel run's class
time and add no verdict. Twenty-two copies of one helper drift, and only one
converts an exit into a code. Thirteen modules import a test module as a
library, so its side effects run twice. About sixty prose pins break on every
wording change and protect no rule.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the loader discovers the suite | the discovered count equals the defined count | a suite test names the class that re-runs inherited tests |
| a test needs the command line, Git, a formal chain or a fresh repository | it calls the one shared helper in a support module | the duplication readings name the copy |
| a test pins wording of a note or a router | it names the specification rule that fixes that wording | the pin becomes a structural check instead |

## Examples

### Normal

**Given** the candidate after this change,

**When** the loader discovers `tests/`,

**Then** every defined test runs once and the failure set equals the
baseline.

### Failure

**Given** a new test class that subclasses a class carrying tests,

**When** the suite runs,

**Then** the loader-count test fails and names the class.
