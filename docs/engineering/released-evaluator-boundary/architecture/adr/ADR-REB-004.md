+++
id = "ADR-REB-004"
type = "adr"
title = "Exact-commit sparse view for predecessor release preparation"
status = "approved"
owners = ["technical-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
decides = ["ARCH-REB-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "technical-owner"
+++

# ADR: Exact-commit sparse view for predecessor release preparation

## Status

Accepted for bounded local implementation under `WO-REB-006`. Candidate, verification, release, commit, credential, and external actions remain separately governed.

## Context

The predecessor-format preparation command validates the repository before writing. Released 0.5.0 stops on the deliberately retained rejected `RLS-SEH-009`, while C3 would reject a second `0.6.0` record because its uniqueness check does not distinguish terminal history from an active claim. The history cannot be deleted or edited, the version has not been published, and upgrading the root before release would reverse the bootstrap trust model.

## Decision drivers

- Preserve the exact released evaluator as RLS generator.
- Preserve every historical candidate, VREC, RLS, contract, and evidence byte.
- Avoid a root upgrade or arbitrary validation bypass.
- Make every omitted input explicit, minimal, deterministic, reviewable, and hash-bound.
- Prevent competing active records for one version.
- Fail before credentials or external mutation.

## Considered options

1. **Upgrade the root evaluator before release.** Rejected because it reverses the approved predecessor trust direction and creates a self-approval dependency.
2. **Delete, relocate, rename, or change rejected history.** Rejected because it rewrites audit facts.
3. **Change the successor to 0.6.1.** Rejected because 0.6.0 is unpublished and the predecessor still cannot parse rejected history.
4. **Hand-author or candidate-generate the RLS.** Rejected because released 0.5.0 would no longer own predecessor-format preparation.
5. **Teach released 0.5.0 the new state locally.** Rejected because a modified predecessor is not the released evaluator.
6. **Use an exact-commit sparse compatibility view plus full-graph candidate replay.** Selected because it keeps the predecessor immutable, makes the unsupported pair the only omission, preserves Git identity, and records the boundary honestly.

## Decision

Introduce a repository-owned adapter that derives one exact rejected predecessor-bootstrap RLS/contract pair from the complete candidate-valid graph, records their Git/raw identities, and creates a detached sparse worktree at the same governance commit with only those two paths omitted. Run external released 0.5.0 in isolated mode to create the successor RLS, verify its exact output, and import it together with canonical view evidence. Apply the existing evaluator binder separately and validate the full graph after each durable step.

Change release-version uniqueness so valid rejected records are terminal history and only ready/released records claim a version. Continue allowing at most one active claim and preserve all publication immutability checks.

## Consequences

### Positive

- The root evaluator and historical bytes remain unchanged.
- The predecessor still generates the RLS.
- The unsupported syntax boundary is explicit rather than silently bypassed.
- Repeated rejected attempts can remain audit history without permanently consuming an unpublished version.

### Negative

- Preparation gains a repository-specific adapter and a second retained evidence object.
- The final complete graph is not parseable by released 0.5.0; reports must distinguish compatibility-view preparation from full candidate validation.
- C3 cannot be promoted after the implementation change; C4 and a new aggregate are required.

### Operational and security consequences

- Sparse-worktree construction, Git executable/object resolution, output import, and rollback become security-sensitive and require adversarial tests.
- Any extra omission, environment contamination, history drift, or partial destination stops the process.
- Publication, credentials, tags, maintenance, and root adoption remain later separate actions.

## Validation

Execute `VER-REB-004`. Require deterministic sparse-view bytes, exact predecessor command/output, arbitrary-omission and TOCTOU failures, lifecycle/version matrices, complete-graph replay, Windows/LF parity, full dual-runtime regression, exact C4 builds, candidate package acceptance, released-evaluator evidence, and hosted lanes.
