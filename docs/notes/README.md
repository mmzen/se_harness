# SE Harness learning notes

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

These notes explain SE Harness in progressively greater detail. They are human-readable guidance, not formal engineering artifacts, and they grant no approval, verification, or release authority.

## Suggested path

| Step | Guide | Question answered |
| --- | --- | --- |
| 1 | [Tier-0 overview](harness-overview.md) | What is SE Harness and what does it control? |
| 2 | [Simplified UML model](harness-uml-model.md) | What are the main concepts and relationships? |
| 3 | [Operational phasing](harness-operational-phasing.md) | When does each concept or operation occur? |
| 4 | [Illustrative branching model](harness-branching-model.md) | How could one repository map the lifecycle onto Git? |
| 5 | [Practical lineage example](harness-lineage-example.md) | What does a complete change look like in practice? |

The repository [README](../../README.md) is the concise public entry point.

## Operator and contributor routes

| Guide | Question answered |
| --- | --- |
| [Installation and safe upgrades](harness-installation-and-upgrades.md) | How do I install the tool and safely update an existing repository? |
| [Read-only agent orientation](harness-orient.md) | How can an agent understand installed harness state and return the next accountable decision without changing anything? |
| [Single-agent workflow skills MVP](agentic-execution-skills-mvp.md) | How do the three explicit-only writing skills complement `harnessctl` and stop at accountable decision points? |
| [Clear technical communication](technical-communication.md) | How do agents apply the two clarity profiles, preserve protected content, and use the explicit read-only operator-brief skill? |
| [Repository host adapters](agentic-execution-host-adapters.md) | How do Codex and Claude Code discover the same four canonical repository skills without duplicating workflow authority? |
| [Phase 4 live authority implementation](agentic-execution-phase4-authority.md) | How do live observation, formal delegation, envelope v2, external nonce state, and receipt chaining fit together without performing a target effect? |
| [Phase 4 change bundles and transactional effects](agentic-execution-phase4-effects.md) | How does the evaluator build byte-only bundles, apply them through one journaled writer, and recover after interruption? |
| [Phase 4 delegated workflow coordination](agentic-execution-phase4-workflow.md) | How are start, brokered effects, completion proof, the Git stop, and undecided VREC preparation composed without adding authority? |
| [Migration: the repository-context scaffold is withdrawn](harness-migration-repository-context-retirement.md) | What breaks when repository facts move to the owner-controlled region of `AGENTS.md`, and what must I do? |
| [Agentic execution roadmap](agentic-execution-roadmap.md) | How could SE Harness move toward skill-driven, delegated execution with humans at accountable decision points? |
| [Phase 1 Agentic Execution definition-review packet](agentic-execution-phase-1-definition-review.md) | Which decisions, revisions, accountable reviews, and read-only transition previews govern the Phase 1 proposal? |
| [Phase 1 Agentic Execution accountable review checklist](agentic-execution-phase-1-accountable-review-checklist.md) | What must each accountable role review before the revised Phase 1 packet can leave draft? |
| [Phase 1 Agentic Execution approval decision](agentic-execution-phase-1-approval-decision.md) | Is the reviewed 16-artifact packet ready for one atomic lifecycle approval? |
| [Phase 2 Agentic Execution contract-closure proposal](agentic-execution-phase-2-contract-closure.md) | Which core-contract gaps and decisions must be closed before `WO-AEX-002` can be approved? |
| [Phase 2 Agentic Execution accountable content review](agentic-execution-phase-2-accountable-review.md) | Which exact revisions are required before the Phase 2 contract drafts can be accepted? |
| [Phase 2 Agentic Execution definition-approval decision packet](agentic-execution-phase-2-definition-approval-decision.md) | Is the accepted three-artifact Phase 2 packet ready for lifecycle compatibility assessment and a later approval decision? |
| [Phase 2 Agentic Execution consistency-correction proposal](agentic-execution-phase-2-consistency-correction-proposal.md) | How can stale draft-time prose in the approved ADR and work order be corrected without changing semantics or lifecycle state? |
| [Runtime-neutral Agentic Execution contracts](agentic-execution-contracts.md) | How do the Phase 2 catalog and pure Python API validate envelopes, packets, receipts, and profiles without granting authority or performing effects? |
| [Bounded evaluator recovery](evaluator-recovery-runbook.md) | How do maintainers rehearse and, only after separate action-time authority, recover a governance deadlock? |
| [`harnessctl` command reference](harnessctl-reference.md) | Which commands exist, who normally runs them, and what can they change? |
| [Developing SE Harness](developing-se-harness.md) | How does the implementation repository use the standard lifecycle while keeping candidate evidence separate? |
| [Testing a current commit with an integration package](integration-packages.md) | How do I safely download, verify, install, test, and remove an expiring non-release build? |
| [Integration Package definition-review packet](integration-package-definition-review.md) | Which exact accountable approvals govern the proposed installable current-commit testing lane? |
| [Publishing the SE Harness development dashboard](harness-dashboard-publication.md) | How is the repository's release-bound public Explorer demonstration deployed and replayed? |
| [Rehearsing the credential-free publication path](release-publication-rehearsal.md) | How is the last mile exercised on both runner platforms before release approval, and how is drift from the orchestrator caught? |

## Know what is authoritative

- **SE Harness guarantees and managed policy:** start at [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md), which routes to workflow, decision-rights, quality-gate, and traceability policies.
- **Configurable harness policy:** `.engineering-harness.toml` selects supported enforcement settings.
- **Repository-specific control:** the owner-controlled region of [`AGENTS.md`](../../AGENTS.md), product artifacts, build commands, Git strategy, hosting controls, and local agent instructions belong to the repository and its accountable owners.
- **Illustrations:** the notes in this directory help readers understand the model but do not authorize work or override managed policy.

If explanatory prose, policy, and executable checks disagree, stop and report the discrepancy. Do not assume that whichever file is executable automatically has governance authority.
