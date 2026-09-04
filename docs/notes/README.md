# SE Harness learning notes

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

These notes explain SE Harness in progressively greater detail. They are human-readable guidance, not formal engineering artifacts, and they grant no approval, verification, or release authority.

## Suggested path

| Step | Guide | Question answered |
| --- | --- | --- |
| 0 | [Getting started](getting-started.md) | How do I install the evaluator and run my first `check`? |
| 0 | [Glossary](../../GLOSSARY.md) | What does each project-specific term mean? |
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
| [`harnessctl check` explained](harnessctl-check.md) | What does `check` evaluate at each checkpoint, how does an artifact's state select the rule and gates, and why does it refuse? |
| [Diagnostic code index](diagnostic-codes.md) | Which diagnostic codes exist, which component speaks each prefix, and what message text comes with a code? (generated from source; a test pins it) |
| [Functional assessment, 2026-08-30](functional-assessment-2026-08-30.md) | What does the tool do today, how easy is it to operate, and what should change first? (point-in-time, issues #280 to #287) |
| [Assessment of the instruction chain, 2026-09-02](assessment-instruction-chain-2026-09-02.md) | How effective, clear, redundant and heavy is the chain of documents a human or agent is told to read, and what should change first? (point-in-time, `19b6819`, one day of governed work as the field test) |
| [An automated test bench for effectiveness](effectiveness-test-bench-2026-09-02.md) | How could the promise of the harness be measured automatically, on which axes, with which scenarios and drivers, and what can a bench not measure? (proposal, 2026-09-02) |
| [Proposal: the decision artifact](decision-artifact-proposal-2026-09-03.md) | How could open decisions and implementation deviations become first-class, blocking artifacts, and how would one influence the requirement, specification, work order and records around it? (proposal, 2026-09-03) |
| [Assessment of requirement readability, 2026-09-04](assessment-requirement-readability-2026-09-04.md) | How long, dense and consistent are the 328 requirements for the reader they exist for, which standards apply, and what shorter template, advisories and migration would help? (point-in-time, `bceb7b5`, proposal) |
| [Assessment of capability readability, 2026-09-04](assessment-capability-readability-2026-09-04.md) | How long, dense and consistent are the 36 capabilities, what do they say that the intent above and the requirements below do not, and why is their requirement list stale in 22 of 30 files? (point-in-time, `fef29a4`) |
| [The delegation class](delegation-class.md) | How does one table on a work order let a non-human actor start it, complete it and prepare its record while the required pull-request check is green, and what stays human? |
| [Read-only agent orientation](harness-orient.md) | How can an agent understand installed harness state and return the next accountable decision without changing anything? |
| [Artifact authoring](artifact-authoring.md) | How is each formal artifact type written, and which rules does the tool enforce? |
| [Lifecycle state contract](lifecycle-state-contract.md) | Which lifecycle states does each artifact family admit, and what does each state's contract row grant? |
| [Clear technical communication](technical-communication.md) | How do agents apply the two clarity profiles, preserve protected content, and use the explicit read-only operator-brief skill? |
| [Repository host adapters](agentic-execution-host-adapters.md) | How do Codex and Claude Code discover the same canonical repository skills without duplicating workflow authority? |
| [Distributing the skills as a coding-agent plugin](agentic-execution-plugin-distribution.md) | What would shipping the harness skills as a host plugin involve, and why is it not a roadmap phase yet? |
| [Agentic execution roadmap](agentic-execution-roadmap.md) | How could SE Harness move toward skill-driven, delegated execution with humans at accountable decision points? |
| [Agentic execution review, 2026-08](agentic-execution-review-2026-08.md) | How has the agentic execution model evolved, how does it work today, and where is it heading? (point-in-time, `992fd73`) |
| [Complexity audit, 2026-08](complexity-audit-2026-08.md) | Which machinery accumulated for past, temporary, or circumstantial situations and should not become permanent? (point-in-time, `f0ecd9b`) |
| [Runtime-neutral Agentic Execution contracts](agentic-execution-contracts.md) | How do the Phase 2 catalog and pure Python API validate envelopes, packets, receipts, and profiles without granting authority or performing effects? |
| [Bounded evaluator recovery](evaluator-recovery-runbook.md) | How do maintainers rehearse and, only after separate action-time authority, recover a governance deadlock? |
| [Rehearsing the root-evaluator handover](evaluator-migration-rehearsal.md) | How does the candidate-evidence lane rehearse the real root-evaluator upgrade before a release, and what does one run prove? |
| [`harnessctl` command reference](harnessctl-reference.md) | Which commands exist, who normally runs them, and what can they change? |
| [Decision artifacts](decision-artifacts.md) | How does a pending question or an implementation deviation become an artifact that blocks work until a named role answers it? |
| [Developing SE Harness](developing-se-harness.md) | How does the implementation repository use the standard lifecycle while keeping candidate evidence separate? |
| [The CI pipeline and the release path](ci-pipeline.md) | Why does the pipeline feel slow when every run finishes in minutes, and what does each simplification increment change? |
| [Testing a current commit with an integration package](integration-packages.md) | How do I safely download, verify, install, test, and remove an expiring non-release build? |
| [Release qualification roles](release-qualification-roles.md) | Which evaluator-target relationship does each `qualify` operation fix, and what does a pass prove? |
| [Publishing the SE Harness development dashboard](harness-dashboard-publication.md) | How is the repository's release-bound public Explorer demonstration deployed and replayed? |
| [Rehearsing the credential-free publication path](release-publication-rehearsal.md) | How does the rehearsal invoke the one release-qualification definition the release itself runs, and what does a rehearsal prove? |

## History

Dated review packets, decision aids, and superseded guidance, kept for the decision trail. Each opens with a banner naming its date and commit; it describes the tool as it was then. The last three stay at their original paths because tests resolve them there; they carry the same banner.

- [Phase 1 Agentic Execution definition-review packet](history/agentic-execution-phase-1-definition-review.md) — the decisions, revisions, and accountable reviews over the Phase 1 proposal.
- [Phase 1 Agentic Execution accountable review checklist](history/agentic-execution-phase-1-accountable-review-checklist.md) — what each accountable role reviewed before the Phase 1 packet left draft.
- [Phase 1 Agentic Execution approval decision](history/agentic-execution-phase-1-approval-decision.md) — the atomic approval of the reviewed 16-artifact packet.
- [Phase 2 Agentic Execution contract-closure proposal](history/agentic-execution-phase-2-contract-closure.md) — the core-contract gaps closed before `WO-AEX-002` could be approved.
- [Phase 2 Agentic Execution accountable content review](history/agentic-execution-phase-2-accountable-review.md) — the revisions required before the Phase 2 contract drafts were accepted.
- [Phase 2 Agentic Execution definition-approval decision packet](history/agentic-execution-phase-2-definition-approval-decision.md) — the decision over the accepted three-artifact Phase 2 packet.
- [Phase 2 Agentic Execution consistency-correction proposal](history/agentic-execution-phase-2-consistency-correction-proposal.md) — the correction of stale draft-time prose in the approved ADR and work order.
- [Phase 3 Agentic Execution skills-MVP contract-closure proposal](history/agentic-execution-phase-3-contract-closure.md) — the contract closure before the single-agent skills MVP.
- [Agentic Execution host-activation contract-closure proposal](history/agentic-execution-host-activation-contract-closure.md) — the contract closure before the Codex and Claude Code skill surfaces were installed.
- [Integration Package definition-review packet](history/integration-package-definition-review.md) — the accountable approvals over the installable current-commit testing lane.
- [Assessment of issue #208 against pull requests #206 and #230](history/assessment-issue-208-prs-206-230-2026-08-28.md) — a read-only assessment of whether the stacked pair resolved the issue.
- [Phase 4 live authority implementation](history/agentic-execution-phase4-authority.md) — live observation, delegation envelopes, nonce state, and receipt chaining, since removed.
- [Phase 4 change bundles and transactional effects](history/agentic-execution-phase4-effects.md) — byte-only bundles and the effect broker, since removed; the journaled apply remains.
- [Phase 4 delegated workflow coordination](history/agentic-execution-phase4-workflow.md) — how the removed `delegated-workflow` command composed start, effects, and completion proof.
- [Single-agent workflow skills MVP](agentic-execution-skills-mvp.md) — the three retired writing skills; `harness-orient` remains.
- [Phase 4 writing-skill integration](agentic-execution-phase4-skills.md) — how the retired writing skills became fail-closed evaluator clients.
- [Migration: the repository-context scaffold is withdrawn](harness-migration-repository-context-retirement.md) — the retirement of the repository-context document and what adopters had to do.

## Know what is authoritative

- **SE Harness guarantees and managed policy:** start at [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md), which routes to workflow, decision-rights, quality-gate, and traceability policies.
- **Configurable harness policy:** `.engineering-harness.toml` selects supported enforcement settings.
- **Repository-specific control:** the owner-controlled region of [`AGENTS.md`](../../AGENTS.md), product artifacts, build commands, Git strategy, hosting controls, and local agent instructions belong to the repository and its accountable owners.
- **Illustrations:** the notes in this directory help readers understand the model but do not authorize work or override managed policy.

If explanatory prose, policy, and executable checks disagree, stop and report the discrepancy. Do not assume that whichever file is executable automatically has governance authority.
