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
| [Migration: the repository-context scaffold is withdrawn](harness-migration-repository-context-retirement.md) | What breaks when repository facts move to the owner-controlled region of `AGENTS.md`, and what must I do? |
| [Agentic execution roadmap](agentic-execution-roadmap.md) | How could SE Harness move toward skill-driven, delegated execution with humans at accountable decision points? |
| [Phase 1 Agentic Execution definition-review packet](agentic-execution-phase-1-definition-review.md) | Which decisions, revisions, accountable reviews, and read-only transition previews govern the Phase 1 proposal? |
| [Phase 1 Agentic Execution accountable review checklist](agentic-execution-phase-1-accountable-review-checklist.md) | What must each accountable role review before the revised Phase 1 packet can leave draft? |
| [Phase 1 Agentic Execution approval decision](agentic-execution-phase-1-approval-decision.md) | Is the reviewed 16-artifact packet ready for one atomic lifecycle approval? |
| [Bounded evaluator recovery](evaluator-recovery-runbook.md) | How do maintainers rehearse and, only after separate action-time authority, recover a governance deadlock? |
| [`harnessctl` command reference](harnessctl-reference.md) | Which commands exist, who normally runs them, and what can they change? |
| [Developing SE Harness](developing-se-harness.md) | How does the implementation repository use the standard lifecycle while keeping candidate evidence separate? |
| [Testing a current commit with an integration package](integration-packages.md) | How do I safely download, verify, install, test, and remove an expiring non-release build? |
| [Integration Package definition-review packet](integration-package-definition-review.md) | Which exact accountable approvals govern the proposed installable current-commit testing lane? |
| [Publishing the SE Harness development dashboard](harness-dashboard-publication.md) | How is the repository's release-bound public Explorer demonstration deployed and replayed? |

## Know what is authoritative

- **SE Harness guarantees and managed policy:** start at [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md), which routes to workflow, decision-rights, quality-gate, and traceability policies.
- **Configurable harness policy:** `.engineering-harness.toml` selects supported enforcement settings.
- **Repository-specific control:** the owner-controlled region of [`AGENTS.md`](../../AGENTS.md), product artifacts, build commands, Git strategy, hosting controls, and local agent instructions belong to the repository and its accountable owners.
- **Illustrations:** the notes in this directory help readers understand the model but do not authorize work or override managed policy.

If explanatory prose, policy, and executable checks disagree, stop and report the discrepancy. Do not assume that whichever file is executable automatically has governance authority.
