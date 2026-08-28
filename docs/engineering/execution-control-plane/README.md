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
- `WO-ECP-006`: reduce Phase 4 to its guarantee and introduce the delegation class.
- `WO-ECP-007`: evict the bootstrap bridge and this repository's identifiers from the product.
- `WO-ECP-008`: retire stubbed skills, trim the manifest, scope the handoff snapshot.
- `WO-ECP-009`: one precondition engine: transition evaluates the contract's gates (split from `WO-ECP-005` on 2026-08-28).

## Work-order ordering

- `WO-ECP-001` first; no dependency.
- `WO-ECP-002` after `WO-ECP-001`.
- `WO-ECP-003` after `WO-ECP-001` and `WO-ECP-002`; it needs `--from-git`
  and the widened digest.
- `WO-ECP-004` independent.
- `WO-ECP-005` independent, and before `WO-ECP-009`.
- `WO-ECP-009` after `WO-ECP-005`, and before `WO-ECP-006`.
- `WO-ECP-006` after `WO-ECP-003` and `WO-ECP-009`.
- `WO-ECP-007` independent.
- `WO-ECP-008` after `WO-ECP-001`.

Every artifact in this domain is `draft`. This packet authorizes no
implementation, lifecycle transition, Git action, release, or external
action; the amendments it names on `agentic-execution`,
`released-evaluator-boundary`, and `legacy-release-evidence` artifacts are
carried by `WO-ECP-006` and `WO-ECP-007` only after those work orders are
approved and started by their accountable owners.
