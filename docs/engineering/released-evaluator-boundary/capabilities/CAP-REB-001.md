+++
id = "CAP-REB-001"
type = "capability"
title = "Operate a provable released-evaluator boundary"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
derives_from = ["INT-REB-001"]
+++

# Capability: Operate a provable released-evaluator boundary

## Actor and need

Repository maintainers, assurance owners, and release owners need to know that root lifecycle observations and mutations came from the exact independently released evaluator selected by the standard installation, while candidate source and packages remained bounded to candidate evidence.

## Capability statement

`An accountable repository operator can perform installed-root lifecycle and release-readiness operations with machine-assessable proof of the selected released evaluator, fail-closed candidate exclusion, and a bounded recovery path.`

## Boundaries

- The capability produces technical evidence and enforces configured policy; it grants no human decision right.
- Initial `init` or `adopt` of a repository without an installed lock is outside the installed-root mutation gate, but the resulting installation must establish standard identity data when configured policy requires it.
- Historical documentation and fixtures may name the retired governor model but cannot be executable inputs to current lifecycle or publication behavior.
- Recovery remains maintainer-only and requires separate emergency and external-action authority.

## Outcomes

- Candidate substitution is rejected before repository mutation.
- Publication and Pages validation use the same standard evaluator vocabulary and identity source as root lifecycle commands.
- Release readiness exposes the complete evaluator observation needed for accountable review.
- Upgrade sequencing, conflicting drafts, and recovery obligations are visible and testable.

## Candidate requirements

`REQ-REB-001` through `REQ-REB-007` define the observable obligations for mutation gating, standard publication resolution, identity evidence, legacy-surface exclusion, upgrade separation, draft-chain observation, and recovery rehearsal.
