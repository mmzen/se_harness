+++
id = "REQ-DST-074"
type = "requirement"
title = "Pin the managed workflow's actions and describe only the steps it runs"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE MANAGED WORKFLOW SHALL pin each action it uses to a commit digest and describe in its header only the steps it runs."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #380 (code health assessment 2026-09-07, section 4): the managed template engineering-harness.yml lines 1 to 7, 33, 34 and 161 at main a68caf70"
measure = "three uses lines pinned to 40-hex digests with exact tag comments; every step the header names exists in the file, and doctor or validate, which the file no longer runs, are not named"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:56:54Z"
decided_by = "product-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. The managed-template packet: the workflow's failure surface, header and pins, the gitignore markers, the environment inventory."
+++

# Requirement: Pin the managed workflow's actions and describe only the steps it runs

## In plain words

The header of the workflow every consumer installs still describes checks
the file stopped running, and its three actions float on major tags. The
header tells the truth and the actions are pinned.

## Why

A consumer reading the header expects a doctor and a validate step that
never occur, and looks for their output in vain. A floating tag lets an
action change under every consumer's required check with no change in any
repository. The repository-owned workflows already pin by commit; the one
file the harness ships to everyone should not be the exception.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a consumer reads the header | it names the evaluator install, the live body read, the selection, the review preflight, the scope and handoff check, the released-root qualification, the Explorer and its upload | it names a step the file does not run |
| the lane resolves an action | the reference is a full commit with its exact tag in a comment | a moving tag is resolved |

## Examples

### Normal

**Given** the template after this change,

**When** the header test compares the header's step list with the file's
steps,

**Then** every named step exists and no step is missing.

### Failure

**Given** a scratch copy where one action is pinned to `v4`,

**When** the pin test runs,

**Then** it names the line.
