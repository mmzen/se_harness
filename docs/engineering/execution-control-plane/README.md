# Execution Control Plane Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes that the harness become an execution control plane:
it owns state (selection, scope, identifiers, evidence binding, the next
command) and enforces at Git boundaries (the diff, the pull-request gate,
the signer), and it ships to consumers only what a consumer repository
needs. It follows the 2026-08 agentic execution review at commit `992fd73`
(`docs/notes/agentic-execution-review-2026-08.md`) and the complexity audit
at `f0ecd9b` (`docs/notes/complexity-audit-2026-08.md`).

## Draft definition packet

- `INT-ECP-001`: make the harness an execution control plane: state and boundary, not instructions.
- `CAP-ECP-001`: an agent obtains its complete execution context in one call and works against a Git-derived, enforced change set.
- `CAP-ECP-002`: accountable decisions are authenticated, structured records.
- `CAP-ECP-003`: the shipped product carries only machinery a consumer repository needs.
- `REQ-ECP-001`: one call returns the complete execution context.
- `REQ-ECP-002`: the change set is derived from Git.
- `REQ-ECP-003`: the harness writes and rebinds evidence packets.
- `REQ-ECP-004`: identifiers are allocated across every local ref.
- `REQ-ECP-005`: the pull-request body is generated.
- `REQ-ECP-006`: the pull-request gate enforces scope unconditionally.
- `REQ-ECP-007`: the restitution digest covers the change set and gates.
- `REQ-ECP-008`: decisions are authenticated records.
- `REQ-ECP-009`: transitions evaluate the contract's gates.
- `REQ-ECP-010`: one result schema and one rule selector.
- `REQ-ECP-011`: a delegation class unlocks transitions behind the gate.
- `REQ-ECP-012`: a fresh consumer repository passes `doctor`.
- `REQ-ECP-013`: no product code names this repository's records.
- `REQ-ECP-014`: a shipped skill invokes the evaluator it describes.
- `REQ-ECP-015`: the reading manifest carries a generated command block, not the owner narrative.
- `REQ-ECP-016`: handoff evidence binds a chain-scoped snapshot.
- `REQ-ECP-017`: harness-owned multi-file writes are journaled.
- `REQ-ECP-018`: no envelope apparatus in the product surface.
- `REQ-ECP-019`: evaluator-derived artifact paths resolve on every host (issue #254; drafted 2026-08-29 with `SPEC-ECP-008`, `VER-ECP-008` and `WO-ECP-012`).
- `REQ-ECP-020`: scope is enforced on the pull request in every lifecycle state (issue #255; drafted 2026-08-29 with `SPEC-ECP-009`, `VER-ECP-009`, `ADR-ECP-006`, an amendment record on `SPEC-ECP-003`, and `WO-ECP-013`).
- `REQ-ECP-021`: the formal snapshot is independent of the checkout's line endings (issue #256; drafted 2026-08-29 with `SPEC-ECP-010`, `VER-ECP-010`, an amendment record on `SPEC-ECP-001`, and `WO-ECP-014`).
- `REQ-ECP-022`: one read-only evaluator command projects and checks a selected artifact (fold `focus` into `check`; drafted 2026-08-29 with `SPEC-ECP-011`, `VER-ECP-011`, `ADR-ECP-007`, an amendment record on `SPEC-ECP-001`, and `WO-ECP-015`).
- `REQ-ECP-023`: the change set admits the selected work order's own verification and release records by construction (issue #264; drafted 2026-08-29 with `SPEC-ECP-012`, `VER-ECP-012`, an amendment record on `SPEC-ECP-001`, and `WO-ECP-016`).
- `REQ-ECP-024`: the projection has exactly one command name — the `focus` alias is removed and `harness-orient` moves to `check` (audit P1; drafted 2026-08-29 with `SPEC-ECP-013`, `VER-ECP-013`, and `WO-ECP-017`).
- `REQ-ECP-025`: the execution context is the `check` projection and no closed alias stays on the command list: `next` folds into `check` behind a one-release alias, `accept-candidate` is retired (audit P2 and P3; drafted 2026-08-29 with `SPEC-ECP-014`, `VER-ECP-016`, an amendment record on `SPEC-ECP-001`, and `WO-ECP-019`). Amended 2026-08-29 under `WO-ECP-020`: the `next` alias is removed before it ships.
- `REQ-ECP-026`: the managed lane reads the `Harness-Work-Order` and `Harness-Restitution` declarations from the live pull-request body, so a corrected body needs a re-run, not a push (issue #280 part c; drafted 2026-08-30 with `SPEC-ECP-015`, `VER-ECP-017`, and `WO-ECP-021`).
- `REQ-ECP-027`: one command shape across `harnessctl` (target, artifact naming, `--json` everywhere, the 0/1/2 exit rule, one code per line, one cause per code; issue #282, drafted 2026-08-30 with `SPEC-ECP-016`, `VER-ECP-018` and `WO-ECP-022`).
- `REQ-ECP-028`: the Git-derived handoff check declares its result in one run — the run binds the packet to the current formal snapshot and closes the change set over its own retained result (issue #280 part b; drafted 2026-08-31 with `SPEC-ECP-017`, `VER-ECP-019`, and `WO-ECP-023`).
- `SPEC-ECP-001`: the next command, Git-derived change sets, the chain-scoped snapshot, and the trimmed manifest.
- `SPEC-ECP-002`: evidence packets, identifier allocation, and pull-request body generation.
- `SPEC-ECP-003`: the mandatory scope-aware pull-request gate and digest coverage.
- `SPEC-ECP-004`: authenticated decision records.
- `SPEC-ECP-005`: one kernel: schema 2, one selector, one precondition engine.
- `SPEC-ECP-006`: delegation at the Git boundary and the retained journaled apply.
- `SPEC-ECP-007`: the consumer product boundary.
- `ARCH-ECP-001`: the execution control plane: state in the harness, enforcement at Git boundaries.
- `ADR-ECP-001`: state and boundary over instructions; `next` is a projection of the existing kernel.
- `ADR-ECP-002`: enforce scope at the Git boundary, not through a proposed-workspace broker; supersedes the write-boundary decision of `ADR-AEX-007` and the envelope decision of `ADR-AEX-006` once accepted.
- `ADR-ECP-003`: accountable decisions are authenticated records consumed by `transition`.
- `ADR-ECP-004`: one result schema, one rule selector, one precondition engine.
- `ADR-ECP-005`: evict self-hosting machinery from the shipped product; supersedes `ADR-REB-009`'s five-operation `qualify` decision and amends `SPEC-LRE-001` rule 11 and `SPEC-REB-002` rule 14.
- `VER-ECP-001`: verify the next command, Git-derived change sets, the trimmed manifest, and the chain-scoped snapshot.
- `VER-ECP-002`: verify evidence packets, identifier allocation, and pull-request body generation.
- `VER-ECP-003`: verify the mandatory scope-aware gate and digest coverage.
- `VER-ECP-004`: verify authenticated decision records.
- `VER-ECP-005`: verify the single kernel.
- `VER-ECP-006`: verify the delegation class, the journaled apply, and the absence of envelope apparatus.
- `VER-ECP-007`: verify the consumer product boundary.
- `WO-ECP-001`: ship `harnessctl next` and Git-derived change sets.
- `WO-ECP-002`: harness-authored evidence, identifier allocation, and pull-request bodies.
- `WO-ECP-003`: make the pull-request gate mandatory and scope-aware, and widen the digest.
- `WO-ECP-004`: authenticated decision records.
- `WO-ECP-005`: one result schema and one rule selector.
- `WO-ECP-006`: remove the Phase 4 envelope, bundle and broker, keep the journaled apply as retained code, retire the stubbed skills (revised 2026-08-29 from the 08-27 draft; `REQ-ECP-018`, `REQ-ECP-014`, new `VER-ECP-014`; the shared write path `REQ-ECP-017` and the delegation class `REQ-ECP-011` follow under later work orders).
- `WO-ECP-007`: evict the bootstrap bridge and this repository's identifiers from the product.
- `WO-ECP-008`: retire stubbed skills, trim the manifest, scope the handoff snapshot.
- `WO-ECP-009`: one precondition engine: transition evaluates the contract's gates (split from `WO-ECP-005` on 2026-08-28).
- `WO-ECP-010`: replace the governance-migration rehearsal with a real upgrade rehearsal (split from `WO-ECP-007` on 2026-08-28 for issue #210).
- `WO-ECP-011`: delete the retired governance-migration stage machine that `WO-ECP-010` kept dead until the root advanced; drafted 2026-08-28 after `WO-HUP-008` moved the root to 0.8.0 (issue #210's follow-up). Implements the accepted `REQ-ECP-012` / `SPEC-ECP-007` ECP-PRD-008 / `VER-ECP-007`; no new definition.

## Work-order ordering

- `WO-ECP-001` first; no dependency.
- `WO-ECP-002` after `WO-ECP-001`.
- `WO-ECP-003` after `WO-ECP-001` and `WO-ECP-002`; it needs `--from-git`
  and the widened digest.
- `WO-ECP-004` independent.
- `WO-ECP-005` independent, and before `WO-ECP-009`.
- `WO-ECP-009` after `WO-ECP-005`, and before `WO-ECP-006`.
- `WO-ECP-006` after `WO-ECP-003` and `WO-ECP-009` (both merged); before the work orders that wire the journal (`REQ-ECP-017`) and add the delegation class (`REQ-ECP-011`).
- `WO-ECP-007` independent.
- `WO-ECP-010` independent; `WO-HBI-005` (merged) precedes it.
- `WO-ECP-011` after `WO-ECP-010` (merged) and `WO-HUP-008` (merged).
- `WO-ECP-012` independent; repair of issue #254 under the new `REQ-ECP-019` / `SPEC-ECP-008` / `VER-ECP-008`, drafted 2026-08-29 after `WO-HUP-009` moved the root to 0.9.0.
- `WO-ECP-013` independent; the `scope` checkpoint and the state-independent gate under `REQ-ECP-020` / `SPEC-ECP-009` / `ADR-ECP-006` / `VER-ECP-009`, drafted 2026-08-29 (issue #255).
- `WO-ECP-014` independent; the line-ending-canonical formal snapshot under `REQ-ECP-021` / `SPEC-ECP-010` / `VER-ECP-010`, drafted 2026-08-29 (issue #256).
- `WO-ECP-015` independent; the checkpoint-less `check` projection and the retirement of `focus` under `REQ-ECP-022` / `SPEC-ECP-011` / `ADR-ECP-007` / `VER-ECP-011`, drafted 2026-08-29 on the owner's challenge.
- `WO-ECP-016` after `WO-ECP-013` (merged); admission of the selected work order's own records under `REQ-ECP-023` / `SPEC-ECP-012` / `VER-ECP-012`, drafted 2026-08-29 from issue #264.
- `WO-ECP-017` after `WO-ECP-015` (merged); removal of the `focus` alias and the deferred `ECP-ONE-007` under `REQ-ECP-024` / `SPEC-ECP-013` / `VER-ECP-013`, drafted 2026-08-29 from the command audit's P1.
- `WO-ECP-018` after `WO-ECP-006` (merged); the delegation class under `REQ-ECP-011` / `SPEC-ECP-006` (`ECP-DLG-001` to `-007`, `-009`) / new `VER-ECP-015` (the class subset of `VER-ECP-006`), drafted 2026-08-29; the shared journaled write path (`REQ-ECP-017`) follows.
- `WO-ECP-019` after `WO-ECP-017` (merged); the context fold, the `next` alias window and the `accept-candidate` retirement under `REQ-ECP-025` / `SPEC-ECP-014` / `VER-ECP-016`, drafted 2026-08-29 from the command audit's P2 and P3.
- `WO-ECP-020` after `WO-ECP-019` (stacked on its branch); removal of the `next` alias before the release, by amendment records on `REQ-ECP-025` / `SPEC-ECP-014` / `VER-ECP-016`, drafted 2026-08-29 on the owner's decision.
- `WO-ECP-021` independent; the managed lane reads the live pull-request body under `REQ-ECP-026` / `SPEC-ECP-015` / `VER-ECP-017`, drafted 2026-08-30 from issue #280 part c; the template only, the root lane follows on the next root adoption.
- `WO-ECP-022` after `WO-ECP-020` (merged); the command shape under `REQ-ECP-027` / `SPEC-ECP-016` / `VER-ECP-018`, drafted 2026-08-30 from the functional assessment's issue #282; head of the assessment's critical path.
- `WO-ECP-023` after `WO-ECP-022` (merged); the self-binding Git-derived handoff check under `REQ-ECP-028` / `SPEC-ECP-017` / `VER-ECP-019`, drafted 2026-08-31 from issue #280 part b; the candidate evaluator only, the root keeps the two-run behaviour until the next root adoption.
- `WO-ECP-008` after `WO-ECP-001`; its skill-retirement item moved to `WO-ECP-006` on 2026-08-29.

This index authorizes no implementation, lifecycle transition, Git action,
release, or external action; the amendments it names on
`agentic-execution`, `released-evaluator-boundary`, and
`legacy-release-evidence` artifacts are carried by `WO-ECP-006` and
`WO-ECP-007` only after those work orders are approved and started by
their accountable owners. Each artifact's own front matter is its state.
- `REQ-ECP-030`, `SPEC-ECP-019`, `VER-ECP-021` and `WO-ECP-025` are drafted (2026-09-02) to close issue #310, assessment item #285c: the `focus`, `next` and `accept-candidate` tombstone guards leave `main()` three releases after their removals shipped, argparse refuses the names as unknown, and the rules that described the guards close by dated amendment.
