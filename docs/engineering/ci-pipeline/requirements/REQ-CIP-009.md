+++
id = "REQ-CIP-009"
type = "requirement"
title = "Carry no duplicated check, second tool version, mixed pin style or retired name"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE PIPELINE SHALL carry no step that repeats a script's check, no second tool version or pin style, and no retired name."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan), re-measured on main at a68caf70 on 2026-09-08: candidate-evidence.yml lines 145 to 156, 243 to 246, 259 to 375, 414 and 430 to 432; publish-pypi.yml lines 109 to 111; pages-publication.yml without a concurrency group; predecessor-evaluator-assessment.yml lines 7, 18, 25 and 154; three action-pin generations and two Python version strings across the workflows"
measure = "zero inline re-checks after a script that performs them; one python-version string across the repository-owned workflows; one pin form, a full commit with its exact tag in a comment; one literal set of integration build-tool versions; one concurrency group on Pages deployment; zero jobs, artifacts, groups or files named after the retired governor or governance-migration mechanisms; zero probes for a flag the resolved evaluator always has"

[relations]
derives_from = ["CAP-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:55:49Z"
decided_by = "product-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. The CI packet: one qualification and one suite run per pull request, one form for each pin, version and name, the Pages deployment queued behind one group."
+++

# Requirement: Carry no duplicated check, second tool version, mixed pin style or retired name

## In plain words

Some steps repeat a check a script already made, actions are pinned three
ways, and two Python versions are requested. Two jobs carry retired names and
two Pages deployments can overlap; each duplicate goes.

## Why

A check written twice drifts once. Three pin generations give three answers
about what runs. A floating tag lets an action move under a required check
unnoticed. A retired name sends a reader to code that no longer exists. Two
callers with different groups can deploy at once.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the candidate package is checked | the surface script is the one check of forbidden members and commands | the suite names the inline copy |
| a workflow pins an action or a Python version | one pin form, a full commit with its tag; one version string | the suite names the line |
| the Pages definition is called | deployments queue behind one group, whichever caller | two callers deploy at once |
| a reader looks for a job | no job, artifact, group or file carries a retired name | the suite names the residue |

## Examples

### Normal

**Given** the repository-owned workflows after this change,

**When** the pin, version and name tests run,

**Then** every pin, version and name is in its one form.

### Failure

**Given** a new step that greps the command list for a forbidden command,

**When** the suite runs,

**Then** the duplicate-check test names the step.
