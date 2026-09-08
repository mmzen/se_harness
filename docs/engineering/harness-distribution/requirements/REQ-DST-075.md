+++
id = "REQ-DST-075"
type = "requirement"
title = "Name every environment variable the harness reads in a specification"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE HARNESS SHALL name every environment variable it reads in the specification of the behaviour that variable changes."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #380 (code health assessment 2026-09-07, section 4): SE_HARNESS_REHEARSAL is read at se_harness/gate_source.py line 112 and named in no specification; measured on main at a68caf70, the package reads two variables, that one and GITHUB_TOKEN"
measure = "every environment name read under se_harness/ occurs in at least one specification under docs/engineering; a test pins the inventory of two names beside the specification that names each"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:56:54Z"
decided_by = "product-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. The managed-template packet: the workflow's failure surface, header and pins, the gitignore markers, the environment inventory."
+++

# Requirement: Name every environment variable the harness reads in a specification

## In plain words

The harness reads two environment variables. One is documented, the other
changes a warning and is written down nowhere a consumer would look.

## Why

A rehearsal marker that silences a warning is a behaviour switch. An
operator who meets the warning cannot find the switch. A reviewer who meets
the switch in code cannot find the rule that allows it. The
specification that defines the exemption should name the variable that
grants it. A test should keep the inventory honest as variables come and go.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a module reads an environment variable | a specification names the variable and the behaviour it changes | the inventory test names the variable |
| a variable leaves the code | the inventory test is updated with it | a stale name remains pinned |

## Examples

### Normal

**Given** the candidate after this change,

**When** the inventory test runs,

**Then** it finds the two names in the package and each in a specification.

### Failure

**Given** a new module reading a third variable,

**When** the suite runs,

**Then** the inventory test fails and names the variable.
