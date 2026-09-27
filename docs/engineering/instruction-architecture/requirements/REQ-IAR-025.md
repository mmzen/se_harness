+++
id = "REQ-IAR-025"
type = "requirement"
title = "Repository-owned AGENTS.md"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
statement = "The harness no longer creates, tracks or requires harness instructions in AGENTS.md, and a supported migration removes the complete legacy harness block while preserving owner content."
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

# Repository-owned AGENTS.md

## Why

Repository instructions and harness instructions have different owners. Agent discovery must work without a managed gate in AGENTS.md.

## Behavior

Clean installation does not scaffold AGENTS.md. Upgrade retires the recognized block and its lock entry. Existing owner bytes outside that block remain unchanged. Harness prose previously copied into this repository’s owner region is removed only through a separately reviewed owner edit during adoption, with its applicable destination recorded.

## Acceptance

Test absent AGENTS.md, owner-only content, a recognized fragment, customized or ambiguous fragments, and repeated migration. Inspect all fragments, locks, doctor/preflight requirements and host adapters for dependence on the retired AGENTS gate.

## Failure

Customized or ambiguous legacy fragments cause a refusal before partial writes. The installer does not classify or delete arbitrary owner prose by keyword.
