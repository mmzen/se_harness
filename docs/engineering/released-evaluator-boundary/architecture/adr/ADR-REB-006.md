+++
id = "ADR-REB-006"
type = "adr"
title = "Evidence-bound dual-plane validation for publication"
status = "approved"
owners = ["technical-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
decides = ["ARCH-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "technical-owner"
+++

# ADR: Evidence-bound dual-plane validation for publication

## Status

Accepted.

## Context

Release run `32587383130` failed before privileged work because exact 0.5.0 directly validated current main. Ignoring its errors would weaken the gate; changing history or root evaluator would violate established release authority; manually reproducing publication would bypass the trusted workflow.

## Decision drivers

- Preserve honest current and predecessor validation claims.
- Reuse the already approved exact rejected-pair trust model.
- Keep candidate C6, tag, RLS, distribution, history, and root evaluator immutable.
- Keep credentials and external mutation strictly downstream.
- Make initial publication and Pages recovery behavior identical.

## Considered options

1. Accept E009/E010 and continue: rejected because diagnostic allowlists cannot prove the remaining graph.
2. Upgrade the root/released evaluator before publication: rejected because it reverses the approved predecessor trust direction and changes release scope.
3. Rewrite or remove rejected history: rejected because historical governance is immutable.
4. Validate current main completely and run 0.5.0 against the exact evidence-bound compatibility view: selected.

## Decision

Introduce one read-only repository adapter implementing option 4. All three publication validation points invoke it. The adapter derives no authority and exposes no omission or expected-error input.

## Consequences

Positive: publication remains fail-closed, auditable, retryable, and compatible without changing release identity. Negative: validation runs additional Git and validator operations, and the post-release workflow correction needs separate commit-bound assurance. Operational: the failed transaction remains immutable evidence and the corrected workflow must start a new run. Security: credential-bearing jobs remain unreachable until both validation planes pass. Migration: no consumer, package, root, tag, RLS, or distribution migration occurs.

## Validation

`VER-REB-006` proves exact view replay, complete validation, predecessor success, all failure boundaries, three-site workflow adoption, zero source/external mutation, and corrected hosted resolution before publication resumes.
