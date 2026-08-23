+++
id = "ADR-REB-008"
type = "adr"
title = "Make the workflow contract the lifecycle semantics authority"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
decides = ["ARCH-REB-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "technical-owner"
+++

# ADR: Make the workflow contract the lifecycle semantics authority

## Status

Proposed.

## Context

Workflow contract v2 declares legal transitions, while validator code separately declares global and per-record-type state sets and separately decides which RLS states reserve a version. Candidate 0.6 currently agrees with the intended policy, but the duplicated representation can drift again. The design must remove that drift without importing candidate code into a released predecessor validator.

## Decision drivers

- One reviewable source for lifecycle edges and the semantics that determine authority and version reuse.
- Independent execution across package and installed standalone validator roles.
- Strict fail-closed handling of malformed or partially upgraded contracts.
- Preservation of valid rejected history and corrected same-version succession.
- No root upgrade, predecessor patch, diagnostic allowlist, or compatibility-view expansion.

## Considered options

1. **Keep hand-maintained transition and validator constants with more parity tests.** Rejected because tests compare copies after drift has already become possible; they do not create one source.
2. **Make the standalone validator import lifecycle constants from `se_harness`.** Rejected because a managed predecessor validator could then execute candidate package policy and become a hybrid evaluator.
3. **Generate Python constants into each consumer at build time.** Rejected because generated outputs become additional policy-bearing copies and require a code-generation trust path.
4. **Put complete state rows in workflow contract v3 and let each isolated consumer build a strict index from its role-appropriate byte-identical contract copy.** Selected because one data model drives behavior without crossing runtime authority boundaries.
5. **Hard-code only rejected as a special case.** Rejected because it fixes the incident symptom while leaving the broader drift mechanism intact.

## Decision

Select option 4.

Advance the workflow machine contract to `se-harness-workflow-v3`. Replace its standalone transition map with the complete lifecycle registry defined by `SPEC-REB-009`. Package consumers use one strict loader/index implementation. The managed standalone validator implements an independent parser over the adjacent managed copy because it must remain executable without candidate imports. Byte equality, semantic matrix conformance, and adversarial contract tests prove the two runtime roles interpret the same source data.

Transition planning reads `transitions_to`. Type validation reads family state keys. Authority-sensitive selection reads `grants_authority`. Release preparation and E010 uniqueness read `reserves_version`. Terminality and visibility are asserted against outgoing edges and retained graph behavior. `predecessor_adapter` is a compatibility fact only; it cannot construct or authorize a view.

The approved compatibility amendment adds terminal definition `ready`,
`in_progress`, `verified`, `released`, and `superseded` rows and terminal
work-order `ready` and `superseded` rows. These rows preserve validator behavior
that previously came from the global status vocabulary. They add no transition
edge, version reservation, or predecessor adapter. Authority matches the
existing active-coverage rule exactly.

## Consequences

### Positive

- A new state or semantic change is reviewed in one complete registry row.
- The tool cannot write a state that its same-version validator rejects because the edge and vocabulary share one source.
- Rejected records cannot accidentally reserve a version or regain authority through a forgotten status set.
- Package and predecessor roles remain isolated.

### Negative

- Workflow contract v3 is a public schema change and needs migration, package, install, and hostile-input tests.
- The standalone validator still needs parsing code because importing package code would violate the evaluator boundary; parity must therefore be proven at the data and semantic-result levels.
- Existing v1/v2 fixtures must be explicitly classified rather than silently accepted by v3 consumers.

## Reversal

Reversal requires a new contract version and governed migration. Reintroducing independent status sets, a candidate import into the predecessor, or a rejected-state special case is not a compatible rollback.
