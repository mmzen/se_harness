+++
id = "VER-REB-006"
type = "verification"
title = "Publication predecessor-view assurance"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
verifies = ["REQ-REB-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "quality-owner"
+++

# Verification Contract: Publication predecessor-view assurance

## Independence

Verification independently recomputes Git blobs, raw hashes, sparse bytes, RLS sidecar digests, candidate/current reports, predecessor reports, checkout maps, and workflow reachability. It does not accept adapter-selected omissions or success flags without replay.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-015` | Exact live-failure reproduction | Run/job `32587383130` and local full-checkout 0.5 report | Identity passes; exact E009/two-E010 boundary is retained; no privileged state exists |
| `REQ-REB-015` | Dual-plane positive integration | Current released `RLS-SEH-012` main graph and external 0.5 | Complete current graph passes; exact two-omission predecessor view passes doctor/validate; source is unchanged |
| `REQ-REB-015` | Evidence and omission negatives | Changed/missing/extra path, blob, raw hash, sparse digest, sidecar, RLS, candidate, or version | Every case fails before predecessor execution or privilege |
| `REQ-REB-015` | Runtime/path/environment negatives | In-tree evaluator, linked path, contaminated environment, alternate Git state, malformed output, timeout | Every case fails closed with bounded diagnostics and cleanup |
| `REQ-REB-015` | Workflow policy | Initial resolver, release Pages build, standalone Pages recovery | All three use the same adapter; no direct full-checkout predecessor validation remains |
| `REQ-REB-015` | Hosted resolution replay | Corrected workflow on trusted main | Resolution and qualification pass before any separately authorized privilege is exercised |

## Acceptance scenarios

1. Reproduce the unchanged failed command and exact diagnostics without external mutation.
2. Validate 647-artifact complete current main and the exact 645-artifact predecessor view with zero errors.
3. Prove both omitted artifacts match current Git blobs and retained preparation evidence byte-for-byte.
4. Prove all three workflow gates call one adapter with no omission or expected-error input.
5. Inject each bounded failure and prove source, tag, RLS, history, root, maintenance, GitHub Release, PyPI, and Pages remain unchanged.

## Property and invariant tests

Omission order does not affect sparse bytes or observation. Only one closed rejected pair is accepted. Candidate/current validation always brackets predecessor execution. Output is canonical and host-normalized. Plan/replay is deterministic and idempotent.

## Static and architecture checks

Trace `REQ-REB-015` through `SPEC-REB-007`, `ARCH-REB-006`, `ADR-REB-006`, and `WO-REB-008`. Confirm no managed root file, portable template, candidate source, RLS/VREC/REL, tag, or distribution change. Confirm privileged permissions remain in downstream jobs only.

## Security and privacy checks

Exercise path traversal, symlink/junction, alternate Git configuration, duplicate JSON, digest substitution, environment credentials, executable replacement, sparse contamination, source dirtiness, TOCTOU, and cleanup failure. Logs and evidence contain no secrets or persistent host paths.

## Performance and resilience checks

Use existing timeouts and size ceilings. Run focused tests, full Python 3.11 suite, graph/distribution/portable-surface checks, exact local external-0.5 replay, and one hosted resolution replay.

## Manual assessments

Technical/security owners accept the dual-plane boundary; assurance owner reviews failure reproduction, exact omissions, negative matrix, full results, and hosted resolution; release owner separately decides whether to resume external publication.

## Evidence retention

`WO-REB-008` evidence retains the failed run/job/log identities, absent external-state checks, approved preflight manifest, exact changed paths, local/hosted reports, omitted identities, before/after maps, test results, commit identity, and actions not performed.

## Residual uncertainty

Future predecessor formats and unrelated hosting outages remain outside scope. A downstream publication failure after validation is reconciled by the existing release workflow.
