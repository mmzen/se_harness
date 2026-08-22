+++
id = "WO-REB-008"
type = "work_order"
title = "Correct publication validation for rejected bootstrap history"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Publication and privileged external mutations will rely on new security-sensitive Git view mediation and trusted workflow gating after the original release transaction failed closed."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T17:29:45Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T19:41:50Z"
decided_by = "engineering-owner"
+++

# Work Order: Correct publication validation for rejected bootstrap history

## Lifecycle

The bounded correction is implemented and exact local and hosted qualification is retained in `../evidence/WO-REB-008-publication-view.md`. Commit-bound assurance remains required before the corrected workflow may reach privileged publication jobs. This lifecycle state records completed work; it does not itself grant verification or release authority.

## Objective

Replace three invalid direct full-checkout predecessor validations with one evidence-bound dual-plane adapter so authorized `RLS-SEH-012` publication can resume without changing release identity or weakening validation.

## In scope

- Retain exact failed workflow/run/job/step diagnostics and prove no partial external state.
- Implement one read-only publication-view adapter conforming to `SPEC-REB-007`.
- Validate complete committed governance state with current semantics before and after exact predecessor-view `doctor`/`validate`.
- Reuse and replay the exact rejected-pair derivation, Git/path/isolation core, and RLS preparation-view evidence.
- Replace the three direct predecessor full-checkout validations in initial resolution, release Pages build, and standalone Pages recovery.
- Add deterministic positive, omission/evidence/path/runtime/environment/TOCTOU/cleanup/workflow tests and operator documentation.
- Retain `WO-REB-008` evidence and qualify one clean corrective commit for commit-bound assurance.

## Out of scope

- Changing candidate C6, `v0.6.0`, `RLS-SEH-012`, any VREC/RLS/REL status or bytes, rejected history, distribution bytes, root lock/configuration/managed files, released 0.5.0, or portable consumer templates.
- Ignoring E009/E010, accepting arbitrary omissions, moving/deleting history, upgrading the root evaluator, or manually bypassing the trusted release workflow.
- Creating or moving a maintenance branch, GitHub Release, PyPI file, Pages deployment, tag, or external policy during implementation/qualification.
- Resuming publication before a separately reviewed commit-bound VREC covers this work.

## Authorized decision envelope

After approval, implementation may choose internal helper/dataclass names, temporary names, and exact workflow step labels. It may not change the dual-plane trust split, exact omission derivation, evidence equality, three required call sites, credential boundary, fail-closed behavior, or release identities.

## Constraints

- Python 3.11+ standard library only; treat Git, paths, evidence, metadata, processes, reports, and environment as untrusted.
- Use no credential or network in the adapter; bound subprocess time/output and reject links, escapes, alternate Git state, dirtiness, and ambiguity.
- Preserve all stopped user-owned untracked content, especially `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md`.
- Never report the compatibility view as full predecessor validation.

## Expected change surface

- One repository-owned publication-view module and CLI script.
- `.github/workflows/publish-pypi.yml` and `.github/workflows/publish-dashboard-pages.yml`.
- Focused predecessor-publication, release-orchestration, dashboard-publication, and security/failure tests.
- Repository/operator documentation and `docs/engineering/released-evaluator-boundary/evidence/WO-REB-008-publication-view.md`.
- This governing packet only; no managed root or package candidate surface.

## Required verification

- Execute every method in `VER-REB-006` plus unchanged `VER-REB-004`/`VER-REB-005` regressions.
- Run full tests, graph, release-distribution, portable-surface, help, diff, and candidate complete validation.
- Reproduce exact released-0.5 full-checkout refusal and prove exact view success locally.
- Prove the complete source and stopped untracked RLS remain unchanged outside authorized paths.
- Commit only after review preflight/inspection; capture a ready commit-bound VREC in later governance history; obtain assurance acceptance before integration and publication retry.

## Evidence to record

Exact run `32587383130`, job `97065733491`, failure command/E009/E010 output, absence checks, preflight manifest, changed paths, current/view commits/trees/counts, omitted blobs/raw hashes, evaluator tuple, canonical observation hashes, all negative maps, complete tests, candidate commit, hosted results, and actions not performed.

## Stop and escalate conditions

- Any solution needs an omission beyond exact `REL-SEH-008`/`RLS-SEH-009`, a diagnostic waiver, candidate/RLS/tag/distribution/history/root mutation, credential inside the adapter, or manual publication bypass.
- Complete-current or predecessor-view validation, canonical replay, cleanup, test, hosted, or commit-bound assurance fails.
- External publication or maintenance mutation would occur before separate resumed-release authority.

## Completion report format

Report failed-run identity, selected dual-plane behavior, exact omissions and commands, changed surfaces, local/hosted results, preserved release/root/history identities, candidate/VREC state, actions not performed, and one next accountable decision.
