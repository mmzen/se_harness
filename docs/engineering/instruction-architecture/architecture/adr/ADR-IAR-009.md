+++
id = "ADR-IAR-009"
type = "adr"
title = "Use closed non-executable guidance instead of inferred advice"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
decides = ["ARCH-IAR-009"]
+++

# ADR: Use closed non-executable guidance instead of inferred advice

## Status

Accepted on 2026-08-15 through the repository owner's instruction `ok i approve`.

## Context

Operators benefit from knowing what to review after `inspect` surfaces an item such as `W-REV-004`. The harness can provide that help through static governed guidance, repository-configurable policy, natural-language inference, or executable remediation. Each alternative carries a different authority and safety profile.

## Decision drivers

- Keep inspection deterministic, offline, read-only, and easy to verify.
- Prevent untrusted repository text from steering advice.
- Preserve the distinction between an observation, a suggested review path, and an accountable decision.
- Avoid expanding the first inspection command into a policy engine or remediation framework.
- Keep the public JSON contract useful to humans and coding agents.

## Considered options

1. Generate advice from artifact prose or finding messages. Rejected because repository-controlled text is untrusted and natural-language inference is not a stable governance rule.
2. Let each repository configure suggestions. Rejected for this increment because configuration schema, policy ownership, migration, and conflict handling require a separate design.
3. Emit runnable remediation commands. Rejected because a displayed observation does not establish eligibility or authorization to mutate state.
4. Add a closed catalog keyed only by existing queue action classes and selected actionable derived warning rule IDs. Preferred because it is deterministic, reviewable, and incapable of inventing a new trigger.

## Decision

Choose option 4. Emit structured suggestions with static guidance, copied subject IDs, one accountable role, and `automatic = false`. Do not map validator findings, informational observations, or unknown rules in the first catalog. Do not include executable commands or target lifecycle states.

Keep suggestions separate from source observations. They cannot alter validation, severity, finding identity, queue membership, exit status, or lifecycle state. A future catalog change that affects trigger or authority meaning requires governed specification and verification.

## Consequences

- Common observations gain concise next-step guidance without adding a rule engine.
- New findings remain safe by default because they receive no inferred advice.
- Some useful guidance remains absent until explicitly governed.
- Human output can remain compact by grouping repeated catalog advice, while JSON retains exact source traceability.
- IAR-008's broad recommendation exclusion must be explicitly narrowed before both work orders are verified at one candidate commit.

## Rejected implications

This decision does not authorize automatic fixes, model-generated advice, plugin or network calls, repository-configurable guidance, command execution, lifecycle transitions, evaluator-independence changes, or resolution of GitHub issue #46.
