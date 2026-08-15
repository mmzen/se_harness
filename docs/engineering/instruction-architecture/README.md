# Instruction Architecture Rationalization

This packet defines the implemented instruction architecture for repositories installed or adopted by SE Harness. `WO-IAR-001` retains exact evidence for the bounded implementation. Commit-bound verification and release authority remain separate.

## Implemented policy-responsibility refinement

The incremental `IAR-002` packet addresses residual procedural duplication between `ENGINEERING_HARNESS.md` and `WORKFLOW.md`. It reuses the approved `INT-IAR-001` and `CAP-IAR-001` authority because the change refines the already selected one-router, focused-policy architecture rather than introducing a new product outcome.

The implemented boundary keeps stable provenance, authority, and side-effect invariants visible in the managed router while assigning ordered verification and release procedure to `WORKFLOW.md`. It changes no command behavior, lifecycle rule, historical record, or accountable decision right.

### Incremental packet index

- Requirement: `REQ-IAR-010`
- Specification: `SPEC-IAR-002`
- Architecture: `ARCH-IAR-002`
- Decision: `ADR-IAR-002`
- Verification contract: `VER-IAR-002`
- Implemented work order: `WO-IAR-002`

## Implemented review-routing refinement

The `IAR-003` packet applies the same responsibility boundary to review and visualization. The router retains evidence and authority invariants; `WORKFLOW.md` becomes the single owner of exact review-preflight, dashboard, and candidate-inspection procedure.

### Review-routing packet index

- Requirement: `REQ-IAR-011`
- Specification: `SPEC-IAR-003`
- Architecture: `ARCH-IAR-003`
- Decision: `ADR-IAR-003`
- Verification contract: `VER-IAR-003`
- Implemented work order: `WO-IAR-003`

## Implemented conditional-ADR assurance

The `IAR-004` packet responds to observed usage where significant first-design choices were recorded in architecture without an ADR. It makes applicability assessment mandatory while keeping ADR creation conditional: significant decisions require related ADR coverage; routine conformance requires an explicit accountable no-ADR rationale.

### Conditional-ADR packet index

- Requirement: `REQ-IAR-012`
- Specification: `SPEC-IAR-004`
- Architecture: `ARCH-IAR-004`
- Decision: `ADR-IAR-004`
- Verification contract: `VER-IAR-004`
- Implemented work order: `WO-IAR-004`

## Implemented typed architecture-traceability change

The `IAR-005` packet resolves the overloaded `architecture.constrains` relation. It preserves direct traceability to architecturally significant requirement drivers through `addresses`, adds explicit specification contracts through `conforms_to`, and keeps direct declarations distinct from transitive graph projections. Routine requirements do not receive artificial architecture coverage, and completed historical relations remain read-only under a bounded compatibility classifier.

### Typed-traceability packet index

- Requirement: `REQ-IAR-013`
- Specification: `SPEC-IAR-005`
- Architecture: `ARCH-IAR-005`
- Decision: `ADR-IAR-005`
- Verification contract: `VER-IAR-005`
- Implemented work order: `WO-IAR-005`

## Implemented authoritative artifact applicability catalog

The `IAR-006` packet gives humans and coding agents one normative source for every standard artifact type's objective, applicability, omission or reuse, accountable owner, and primary relations. `TRACEABILITY.md` owns the catalog; the managed router points to it; progressive notes and authoring templates retain focused responsibilities without becoming competing authority.

The implementation also resolves the documented routine-work contradiction. A work order may omit its `architecture` relation when no active architecture addresses an implemented requirement. Applicable architecture and required deciding ADRs remain mandatory, and a present empty relation remains invalid. A structural test keeps the twelve-type registry and catalog membership synchronized.

### Artifact-applicability packet index

- Requirement: `REQ-IAR-014`
- Specification: `SPEC-IAR-006`
- Architecture: `ARCH-IAR-006`
- Decision: `ADR-IAR-006`
- Verification contract: `VER-IAR-006`
- Implemented work order: `WO-IAR-006`

## Implemented instruction route

```text
CLAUDE.md (managed adapter inside owner content)
                    |
                    v
AGENTS.md (owner instructions + short managed gate)
                    |
                    v
ENGINEERING_HARNESS.md (single managed contract and router)
          |                    |                    |
          v                    v                    v
repository context      formal artifact chain    policy modules
(owner facts)           (product authority)      (workflow and gates)
```

The managed block in `AGENTS.md` has exactly one harness destination: `ENGINEERING_HARNESS.md`. `CLAUDE.md` imports `AGENTS.md`. Other tool adapters may use the same pattern later, but no additional adapter is required by this packet.

## Ownership model

| File | Current installation mode | Responsibility |
| --- | --- | --- |
| `AGENTS.md` | managed fragment in owner-controlled file | Repository-specific instructions plus the short non-waivable harness gate |
| `CLAUDE.md` | managed fragment in owner-controlled file | Tool adapter importing `AGENTS.md` |
| `ENGINEERING_HARNESS.md` | fully managed | Single harness contract, stage-aware router, and authority boundary |
| `docs/engineering/REPOSITORY_CONTEXT.md` | owner-owned seed | Confirmed repository facts and commands; never product authority |
| `docs/engineering/README.md` | owner-owned seed | Repository/domain artifact index; no duplicated harness policy |
| `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md` | fully managed | Focused policy modules directly indexed by the router |

Owner instructions may be more restrictive and may describe repository-specific practices. They cannot waive approved work-order scope, formal validation, human decision rights, commit-bound provenance, or release controls. Structural checks can detect missing or modified managed content; semantic conflicts still require human review and fail-closed escalation.

## Enforcement model

1. Thin managed fragments make the same harness entry visible to supported agents without replacing repository-owned instructions.
2. `harnessctl preflight . --work-order WO-...` performs a read-only implementation-readiness check and prints the exact governing files and commands.
3. A required CI baseline check invokes a separately installed, exactly pinned released harness so a pull request cannot silently weaken both previously released policy and its checker.
4. Formal artifacts and accountable humans remain the only sources of product, verification, and release authority.

Documentation alone is not treated as enforcement. Branch protection, protected review ownership, and the external pinned checker are repository-host controls and must be configured by an accountable owner.

The harness repository has an unavoidable one-release bootstrap lag: the last released distribution independently enforces the prior baseline, while candidate tests and human verification assess new checker behavior. After publication, a separate governed pin update activates that new behavior as the independent baseline. The proposal does not claim that unreleased code independently verifies itself.

## Implemented delivery

1. Canonical standard templates document the ownership-mode contract.
2. Safe installer migrations cover managed-to-seed transitions and self-hosting lock reconciliation.
3. Read-only preflight provides deterministic text and JSON output.
4. The installed GitHub workflow uses an exact external harness pin and an explicit pull-request work-order input, including the self-hosting bootstrap rule.
5. Self-hosted operational copies are updated through the supported upgrade path.
6. Adoption, upgrade, conflict, preflight, CI-template, parity, and regression tests retain executable evidence.
7. Work-order-keyed evidence and later commit-bound records preserve the decision boundary.

## Approved decisions

- `ENGINEERING_HARNESS.md` is the single managed router.
- `docs/engineering/README.md` becomes a repository-owned seed rather than managed policy.
- Preflight blocks when repository context retains unresolved seed placeholders.
- Independently pinned CI is the enforceable baseline boundary; repository-host protection remains an owner responsibility.

## Packet index

- Intent: `INT-IAR-001`
- Capability: `CAP-IAR-001`
- Requirements: `REQ-IAR-001` through `REQ-IAR-009`
- Specification: `SPEC-IAR-001`
- Architecture: `ARCH-IAR-001`
- Decision: `ADR-IAR-001`
- Verification contract: `VER-IAR-001`
- Implemented work order: `WO-IAR-001`
- Draft release contract: `REL-IAR-001`
- Draft operating contract: `OPS-IAR-001`
- Acceptance scenarios: `acceptance/instruction-architecture.feature`
