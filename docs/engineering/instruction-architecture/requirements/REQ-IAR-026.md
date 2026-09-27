+++
id = "REQ-IAR-026"
type = "requirement"
title = "Fresh startup and compaction context"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
statement = "Each host advertised as supporting automatic harness discovery supplies the selected repository’s current ENGINEERING_HARNESS.md at startup and after compaction."
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

# Fresh startup and compaction context

## Why

A skill description or a remembered filename does not prove that required instructions are in the current context.

## Behavior

The integration establishes the repository and selected release, delivers the root entry, and exposes the current reading route. After compaction the agent recovers selected IDs and the pending action, obtains fresh evaluator context for supported records, rereads instructions lost from context, and checks uncertain effects before retrying.

## Acceptance

Retain real host traces for Codex and Claude Code where automatic support is claimed. Cover startup, compaction, repository switch, missing root, mismatched release and uncertain prior write. Record the host version and observed payload. Mocked traces alone do not establish native support.

## Failure

If a host cannot provide the required delivery event, mark that integration unsupported for automatic discovery and report the gap. An explicit manual read is a disclosed fallback, not a passing automatic-injection result.
