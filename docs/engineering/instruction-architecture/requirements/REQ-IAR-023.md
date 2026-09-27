+++
id = "REQ-IAR-023"
type = "requirement"
title = "Instructions selected by action"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
statement = "An agent can reach the current procedure and its exact prerequisites without reading all procedures or following a chain of general indexes."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Repository owner discussion culminating in the 2026-09-20 instruction-discovery split and request to create its delivery artifacts."

[relations]
derives_from = ["CAP-IAR-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "repository-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Instructions selected by action

## Why

Splitting a long document is useful only when an agent can tell what to read and when.

## Behavior

Every action file states its read trigger, inputs, output, actions, harness commands, completion condition and later use. Each step has one outcome. Required references name a file and heading plus their condition. A general link does not require its target to be read.

## Acceptance

Map all 58 source headings and 31 main-process steps. Every step has an addressable destination. Walk new-change, execution, verification, delivery and setup cases; each reaches the needed procedure and applicable references without loading unrelated stages.

## Failure

Missing or ambiguous required destinations are reported before the affected action. The agent does not infer a missing procedure from a title or remembered state.
