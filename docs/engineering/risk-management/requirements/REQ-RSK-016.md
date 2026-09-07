+++
id = "REQ-RSK-016"
type = "requirement"
title = "A release states the risks the released work carries"
status = "draft"
owners = ["release-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHEN a release record is prepared, THE HARNESS SHALL list every accepted or unclosed risk threatening the released work, with its score and residual."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #156 REQ-RSK-005, retired with its branch, whose lists_risks projection is kept here as a release-time register"
measure = "the prepared record carries one row per accepted, mitigating or raised risk reachable from its released work; the list is derived, and a hand-written list is rejected"

[relations]
derives_from = ["CAP-RSK-010"]
+++

# Requirement: A release states the risks the released work carries

## In plain words

A release record says which threats travel with it. The list is worked out from
the graph, not typed by the person preparing the release.

## Why

The release decision is where a carried threat matters most and is least
visible. A derived list cannot be shortened by whoever is in a hurry. Someone
reading the record years later can see what was known and accepted at the time.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a release record is prepared | every accepted, mitigating or raised risk on the released work is listed | preparation refuses and names the risk it cannot read |
| a listed risk is accepted | its row carries the score, the revisit trigger and the residual | preparation refuses on a missing residual |
| the list is edited by hand | the record is rejected | the graph reports the divergence |

## Examples

### Normal

**Given** released work with one accepted risk of score twelve,

**When** the release record is prepared,

**Then** the record lists that risk with its score and residual.

### Failure

**Given** the same release with a row deleted by hand,

**When** the graph is read,

**Then** the record is rejected because the list is derived.
