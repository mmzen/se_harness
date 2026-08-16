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

## Implemented validation diagnostic taxonomy

The `IAR-007` packet proposes one small reporting improvement: every existing validator finding states whether it concerns `structure`, `governance`, configured `policy`, or `maintenance`. It preserves all current rules, codes, severities, messages, pass/fail results, and exit behavior. Profiles, new inspection rules, evaluator identity, pending/orphan heuristics, and aggregate scores remain follow-on ideas outside this packet.

### Validation-taxonomy packet index

- Requirement: `REQ-IAR-015`
- Specification: `SPEC-IAR-007`
- Architecture: `ARCH-IAR-007`
- Approved decision: `ADR-IAR-007`
- Verification contract: `VER-IAR-007`
- Implemented work order: `WO-IAR-007`

## Implemented repository inspection command

The `IAR-008` packet implements a first read-only `harnessctl inspect` command. It reuses the current validator and Harness Explorer snapshot to present formal validity, lifecycle attention queues, and existing derived findings in deterministic human or JSON output. It adds no validation rule, finding heuristic, score, remediation, lifecycle authority, or independent-governor claim.

### Inspection-command packet index

- Requirement: `REQ-IAR-016`
- Specification: `SPEC-IAR-008`
- Architecture: `ARCH-IAR-008`
- Approved decision: `ADR-IAR-008`
- Verification contract: `VER-IAR-008`
- Implemented work order: `WO-IAR-008`

## Implemented bounded inspection guidance

The implemented `IAR-009` packet adds deterministic next-step suggestions for the existing inspection queues and a closed set of actionable derived warning rules. Guidance remains separate from its source observation, carries `automatic = false`, identifies an accountable review role, and never infers eligibility or emits executable remediation. Unknown, informational, and validator-owned findings remain visible without guessed advice.

This proposal also makes the aggregate-candidate boundary explicit: if approved and implemented on the current branch, `WO-IAR-008` and `WO-IAR-009` will retain separate evidence and may be covered by one later VREC bound to their shared clean candidate commit.

### Inspection-guidance packet index

- Requirement: `REQ-IAR-017`
- Specification: `SPEC-IAR-009`
- Architecture: `ARCH-IAR-009`
- Approved decision: `ADR-IAR-009`
- Verification contract: `VER-IAR-009`
- Implemented work order: `WO-IAR-009`

## Implemented typed temporal reassessment

The `IAR-010` packet narrows the existing `W-HEX-003` inspection observation to supported declared dependencies whose source remains meaningfully reassessable. Completed work orders, commit-bound verification and release records, inactive definitions, supersession lineage, derived projections, and unknown extension relations no longer receive generic date-based reassessment advice. The finding remains a derived warning and its existing suggestion remains non-automatic and non-authoritative.

### Temporal-reassessment packet index

- Requirement: `REQ-IAR-018`
- Specification: `SPEC-IAR-010`
- Architecture: `ARCH-IAR-010`
- Approved decision: `ADR-IAR-010`
- Verification contract: `VER-IAR-010`
- Implemented work order: `WO-IAR-010`

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
- Approved operating contract: `OPS-IAR-001`
- Acceptance scenarios: `acceptance/instruction-architecture.feature`

`OPS-IAR-001` was separately reviewed and approved through `WO-OCA-001` on 2026-08-16. It accepts continuing operation of the implemented instruction and enforcement requirements, including released-governor separation, managed integrity, preflight, layered validation, inspection, and bounded guidance. `REL-IAR-001` remains a draft release proposal; operating approval does not imply release authority.
