+++
id = "ARCH-REB-005"
type = "architecture"
title = "Dual-plane hosted predecessor assessment boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
addresses = ["REQ-REB-013", "REQ-REB-014"]
conforms_to = ["SPEC-REB-006"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction changes which hosted observation qualifies an immutable predecessor after its schema can no longer parse the complete graph, while preserving an expected failed workflow and preventing candidate orchestration from becoming root authority."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "technical-owner"
+++

# Architecture: Dual-plane hosted predecessor assessment boundary

## Context and scope

C4 implemented a secure preparation view but left hosted released-governor assessment on the full checkout. Hosted run `32558379907` consequently reproduced exact 0.5.0 `E009`. Run `32558379908` separately exposed process-global fault injection on Linux. This architecture extends the existing view boundary to assessment and narrows the test seam without changing root-managed state or history.

## System decomposition

- **Complete candidate plane:** validates every artifact, including all rejected history, with candidate semantics.
- **Legacy observation plane:** executes unchanged released 0.5.0 on the full checkout and retains its exact single refusal.
- **Predecessor assessment plane:** runs the same released evaluator on the contract-derived exact view and produces canonical hosted evidence.
- **Shared view core:** supplies pair derivation, Git/blob/raw identity, materialization, isolation, and rechecks to both preparation and assessment.
- **Fault seam:** exposes only adapter-owned exclusive creation for deterministic rollback tests.

## Trust boundaries

Candidate code may orchestrate and report but cannot select omissions, alter commands, change the evaluator, or assert lifecycle authority. Git and independent candidate validation prove the complete source; the exact released runtime proves predecessor behavior within its declared view. The expected full-checkout failure stays visible so the boundary cannot be confused with full predecessor acceptance.

## Data flow

```text
exact C5 + released 0.5 identity
  -> full candidate validation
  -> exact legacy E009 observation
  -> shared closed-pair derivation
  -> detached two-omission assessment view
  -> released-0.5 doctor/validate/dashboard
  -> canonical hosted assessment evidence
  -> full candidate replay + checkout no-change proof
```

## Required patterns

- One shared derivation for preparation and assessment.
- Separate labels and hashes for full-checkout refusal, view acceptance, and complete candidate acceptance.
- Fixed commands, exact runtime, read-only source, runner-temporary outputs, and closed evidence schema.
- Adapter-local exclusive-create test seam with unchanged production flags.
- Exact diagnostic matching rather than generic failure tolerance.

## Prohibited patterns

- Modifying or disabling the managed Engineering Harness workflow.
- Marking the legacy failure successful, suppressing `E009`, or changing branch protection/external policy.
- Editing rejected history, upgrading root 0.5.0, or using candidate validation as predecessor evidence.
- Separate or caller-controlled omission algorithms.
- Process-global standard-library mocks.

## Quality attributes

- Integrity: every view and output is commit/blob/raw-hash bound.
- Auditability: the red legacy and green replacement observations are both retained.
- Portability: failure injection and canonical evidence behave identically on Linux and Windows.
- Fail safety: any unexpected diagnostic or state change blocks qualification.
- Maintainability: preparation and assessment share one compatibility core.

## Conformance checks

Execute `VER-REB-005`, including exact hosted-log replay, altered-diagnostic negatives, view equivalence with preparation, Linux/Windows cleanup tests, candidate/package lanes, and zero root-managed diff.

## Related ADRs

`ADR-REB-005` records the decision to add an explicit exact-view hosted assessment lane while leaving the obsolete full-checkout workflow visibly failed and unchanged.
