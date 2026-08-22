+++
id = "ARCH-REB-006"
type = "architecture"
title = "Dual-plane publication validation boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
addresses = ["REQ-REB-015"]
conforms_to = ["SPEC-REB-007"]

[decision_assessment]
outcome = "adr_required"
triggers = ["security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "material-alternatives"]
rationale = "Publication authority depends on a new mediation boundary between trusted current governance semantics, an immutable predecessor, temporary Git views, and downstream privileged jobs."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "technical-owner"
+++

# Architecture: Dual-plane publication validation boundary

## Context and scope

Publication runs from trusted main after the selected RLS exists, while released 0.5.0 cannot parse retained rejected-bootstrap syntax. Direct full-checkout predecessor validation therefore fails honestly but cannot establish current-graph validity. The architecture separates those claims without weakening either.

## Components and responsibilities

- **Current complete-graph validator:** owns all current lifecycle and cardinality semantics.
- **Publication-view adapter:** replays RLS-bound view evidence, derives the exact temporary view, invokes predecessor observations, and proves zero source mutation.
- **Released predecessor:** validates every artifact materialized in its compatible view.
- **Publication resolvers/workflows:** gate privileged stages on both planes and retain bounded refusal or success evidence.
- **Git:** anchors current commit/tree and immutable rejected-history blobs.

## Dependency direction

```text
trusted main policy -> complete validation -> evidence-bound view adapter
                    -> external 0.5 observations -> privileged publication jobs
```

Candidate modules never become the root evaluator, and predecessor output never decides lifecycle or publication authority.

## Data and control flow

The adapter selects released RLS metadata, replays its canonical preparation-view binding against Git history, validates complete main, materializes an exact detached sparse view, runs predecessor `doctor` and `validate`, destroys the view, then rechecks complete main and emits canonical observation.

## Trust boundaries

Repository data, sidecars, Git configuration, sparse state, paths, executables, environment, and reports are untrusted. Main workflow code is trusted only at its exact integrated commit. Privileged credentials are unavailable to the adapter and appear only in later jobs after all validation succeeds.

## Required patterns

- Exact current commit and two independently checked validation planes.
- Omission derived from typed rejected history and matched to retained RLS evidence.
- External isolated evaluator and credential-free subprocess environment.
- One reusable implementation shared by all three workflow validation points.
- Fail-closed gating and zero mutation before privileged jobs.

## Prohibited patterns

- Generic ignored diagnostics, caller-supplied omission lists, historical edits, candidate-as-root claims, or direct 0.5 full-checkout success claims.
- Workflow-specific shell copies of security-sensitive view derivation.
- Continuing after a partial or unexpected validation result.

## Quality attributes

Integrity comes from Git/evidence hashes; auditability from canonical observations; reliability from identical shared gating; compatibility from immutable predecessor use; and least privilege from keeping credentials downstream.

## Conformance checks

Execute `VER-REB-006`, including exact current replay, all three static workflow call sites, omission/evidence/runtime/path negatives, failure-before-privilege checks, local reproduction of run `32587383130`, and successful corrected dry qualification.

## Related ADRs

`ADR-REB-006` decides the dual-plane exact-view strategy and rejects both full-checkout error waivers and root-evaluator upgrade.
