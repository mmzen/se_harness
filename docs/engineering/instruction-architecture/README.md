# Instruction Architecture Rationalization Proposal

This packet defines the implemented instruction architecture for repositories installed or adopted by SE Harness. `WO-IAR-001` retains exact evidence for the bounded implementation. Commit-bound verification and release authority remain separate.

## Proposed instruction route

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

| File | Proposed installation mode | Responsibility |
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

## Implementation plan

1. Update canonical standard templates and document the ownership-mode contract.
2. Add safe installer migrations, including managed-to-seed transitions and self-hosting lock reconciliation.
3. Add the read-only preflight command with deterministic text and JSON output.
4. Update the installed GitHub workflow to use an exact external harness pin and an explicit pull-request work-order input, including the self-hosting bootstrap rule.
5. Update the self-hosted operational copies only through the supported upgrade path.
6. Add adoption, upgrade, conflict, preflight, CI-template, parity, and full-regression tests.
7. Retain work-order-keyed evidence; commit and capture verification only under later explicit authority.

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
- Draft work order: `WO-IAR-001`
- Draft release contract: `REL-IAR-001`
- Draft operating contract: `OPS-IAR-001`
- Acceptance scenarios: `acceptance/instruction-architecture.feature`
