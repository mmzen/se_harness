# Agent Directive Surface Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes that every behavioural guarantee the managed harness asks
of a coding agent either becomes a predicate the released evaluator computes,
or is stated once, in a bounded reading set, with an explicit scope. It follows
a read-only review of the directive surface at commit `0276dd7` on 2026-08-25.

## Draft definition packet

- `INT-ADS-001`: make agent directives enforced, bounded, and consistent.
- `CAP-ADS-001`: give a coding agent one tool-computed next step and one bounded reading set.
- `REQ-ADS-001`: a blocked or failed checkpoint names a distinct corrective step.
- `REQ-ADS-002`: one selected state yields one canonical next step in one restitution dialect.
- `REQ-ADS-003`: the phase reading manifest and a generated operating card are the mandatory read.
- `REQ-ADS-004`: recurring traps become evaluator diagnostics.
- `REQ-ADS-005`: a restitution block carries a recomputable digest.
- `REQ-ADS-006`: the managed router states the scope of its own obligations.
- `SPEC-ADS-001`: define the failure-rendering, next-step, manifest, diagnostic, digest, and scope contracts.
- `ARCH-ADS-001`: move prose guarantees into the workflow contract, result renderer, preflight, and CI verifier.
- `ADR-ADS-001`: carry failure renderings in `WORKFLOW.json`, not in prose or skills.
- `VER-ADS-001`: verify self-loop absence, dialect equality, manifest completeness, diagnostics, digest recomputation, and scope wording.
- `WO-ADS-001`: implement the bounded first increment after approval and an explicit start decision.

## Second increment (draft)

- `REQ-ADS-007`: keep the reading surface bounded and free of retired files; supersedes the pointer clause of `REQ-IAR-020`.
- `SPEC-ADS-002`: closed manifest, minimal card, owner region without the retired context file.
- `VER-ADS-002`: evidence for the bounded reading surface.
- `WO-ADS-002`: close the manifest, minimise the card, retire the repository-context file.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action.

Owner-region changes that need no chain (release sequences folded into
`AGENTS.md`, the declared ungoverned paths) are carried by `WO-ADS-001` only
where a test inventory binds them; otherwise they are owner content.
