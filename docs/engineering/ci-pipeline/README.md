# CI Pipeline Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain follows the 2026-08-26 assessment of the repository's continuous
integration and release path (`docs/notes/ci-pipeline.md`). The assessment
found that runner time is not the cost: every run finishes in under five
minutes. The cost is multiplication — the same commit built, tested and
attested many times per push — and a release contract whose frozen
work-order allow-list is invalidated by ordinary merges to `main`. The packet
removes the multiplication and changes what the release contract freezes,
and it makes the documentation of the pipeline part of every increment.

## Draft definition packet

- `INT-CIP-001`: run each check once, and freeze something that stays frozen.
- `CAP-CIP-001`: produce candidate evidence and a release from one execution of each check.
- `REQ-CIP-001`: one run per commit — push filtered to protected lines, cancelling concurrency (P1).
- `REQ-CIP-002`: build the candidate wheel once and hand it to every consumer; collapse reconcile-only jobs (P2).
- `REQ-CIP-003`: one definition of release qualification, invoked by the rehearsal and the release; no digest declaration; scripts reuse package code (P3).
- `REQ-CIP-004`: the release unit is a candidate commit; the work-order census is derived from trailers (P4).
- `REQ-CIP-005`: run only the qualification leg the record's schema needs; one Pages job (P5).
- `REQ-CIP-006`: derive the predecessor evaluator facts from the repository's declared governor, failing closed (P6).
- `SPEC-CIP-001`: triggers, artifacts, the reusable qualification workflow, the release-unit derivation, and the documentation each increment owes.
- `ARCH-CIP-001` / `ADR-CIP-001` / `ADR-CIP-002`: rehearse by invoking, not by digesting; freeze by commit, not by list.
- `VER-CIP-001`: independent evidence.
- `WO-CIP-001`: P1 and P2 (REQ-CIP-001, 002).
- `WO-CIP-002`: P3 and P5 (REQ-CIP-003, 005).
- `WO-CIP-003`: P6 (REQ-CIP-006).
- `WO-CIP-004`: P4 (REQ-CIP-004).
- `WO-CIP-005`: follow-up to WO-CIP-004's deviation 1 — the approval-time predicate that refuses a release contract whose census differs from the derivation (REQ-CIP-004). Draft.
- `REQ-CIP-007`, `SPEC-CIP-002`, `VER-CIP-002`, `WO-CIP-006` (drafted 2026-09-02, issues #305 and #193): the pull-request rehearsal selects the newest schema-2 record the base branch already holds, so a release pull request's record-mode lane can be green before its own merge; delegated route.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action.
