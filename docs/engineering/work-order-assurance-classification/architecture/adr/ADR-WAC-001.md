+++
id = "ADR-WAC-001"
type = "adr"
title = "Record commit-bound assurance applicability on each work order"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
decides = ["ARCH-WAC-001"]
+++

# ADR: Record commit-bound assurance applicability on each work order

## Status

Accepted on 2026-08-16 through the repository owner's `ok go` instruction after review of the complete ready packet.

## Context

Inspection can see lifecycle and VREC relations but cannot know whether an implemented work order should receive commit-bound assurance. Requiring all implemented work would create many false positives and recursively require verification of verification-transition work. Leaving applicability to agent judgment hides genuine assurance debt.

## Decision drivers

- Explicit accountable intent rather than inference.
- No recursive verification chain.
- Deterministic, useful inspection output.
- Compatibility with completed legacy work.
- Minimal model and operational complexity.
- Safe consumer installation and upgrade.

## Considered options

1. **Infer from work-order status, title, relations, or changed files.** Rejected because existing governance-only work has the same statuses and verification relations as assurance-bearing work.
2. **Require a VREC for every implemented work order.** Rejected because it creates noise and an endless chain for work that records assurance decisions.
3. **Maintain a repository-level allowlist or exemption list.** Rejected because ownership moves away from the work boundary, lists drift, and review loses local rationale.
4. **Record explicit applicability on each work order with bounded legacy compatibility.** Selected because the decision sits beside scope and authority, can be reviewed before execution, and supports deterministic inspection without inference.

## Decision

Adopt option 4. Add an assurance table with `commit_bound_verification`, `rationale`, and `decided_by`. Require exact values and a valid declaration for actionable work and selected preflight. Derive assurance follow-up only for explicitly required implemented work without an active VREC proposal.

Treat missing completed-legacy declarations as unknown and non-actionable, not as exemptions. Permit explicitly non-required governance work to remain implemented. Preserve later explicit VREC selection, release coverage, and all human decision boundaries.

## Consequences

Positive consequences are visible assurance debt, fewer false positives, a clear non-recursive exception, and a stable decision point before implementation. Costs are new metadata, a versioned inspection report, managed-template migration, additional tests, and the continuing need for humans to judge rationale honestly.

Existing completed artifacts remain heterogeneous until separately maintained. This is intentional and more truthful than a bulk inferred migration.

## Validation

Apply `VER-WAC-001`. Verify exact metadata, lifecycle compatibility, preflight projection, VREC-state coverage, deterministic suggestions, authority text, managed parity, installation and upgrade behavior, and full regression.
