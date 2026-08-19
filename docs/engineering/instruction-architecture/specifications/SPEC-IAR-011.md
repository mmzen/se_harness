+++
id = "SPEC-IAR-011"
type = "specification"
title = "Stage-aware conversational handoff contract"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
specifies = ["REQ-IAR-019"]
+++

# Specification: Stage-aware conversational handoff contract

## Lifecycle

Approved and implemented on 2026-08-19 through `WO-IAR-011` after the repository owner's instruction `ok go implement` established this as the behavioral contract for `REQ-IAR-019`.

## Scope

Define the managed instruction contract that coding agents follow when yielding control after a completed lifecycle stage, failed check, or stop condition. The managed router owns the stable reporting obligation, and managed `WORKFLOW.md` owns the stage-specific recommendations and ordered procedure.

This specification changes distributed instruction content and public interaction examples. It does not change a command, validator rule, Inspector suggestion, artifact schema, lifecycle transition, or accountable decision right.

## Actors and external systems

- Coding agents operating through the installed managed instruction route.
- Product, technical, engineering, assurance, release, and service owners receiving handoffs.
- Repository owners installing or upgrading managed router and workflow content.
- The installer and schema-2 lock that distribute and protect managed files.

## Inputs

- The lifecycle stage and scope actually completed in the current authorized turn.
- Current formal artifact statuses and typed relations.
- Applicable work-order, VREC, RLS, evidence, and exact commit identities.
- Results of required checks, preflight, validation, inspection, and managed-integrity assessment.
- Applicable authority and stop conditions from managed policy and owner instructions.

Repository prose, guessed ownership, branch names, source diffs, and generic user intent do not independently establish lifecycle state or authority.

## Outputs

One conversational handoff containing these semantic fields:

1. `Completed`
2. `Current lifecycle state`
3. `Recommended next step`
4. `Human decision or approval required`
5. `Command or suggested response`
6. `Alternative next steps`, only when more than one valid governed path exists

The exact visual formatting may adapt to the client, but every applicable semantic field must remain explicit and quickly distinguishable.

## State model

The handoff observes and reports existing state; it does not transition state. The recommendation is selected from the final state actually reached when the agent yields.

| Observed state or boundary | Primary recommendation | Accountable authority |
| --- | --- | --- |
| governing definition and bounded work order are `draft` | review and approve or request revisions | applicable product, technical, assurance, and engineering owners |
| selected work order is `approved` and execution has not begun | run start preflight, read its manifest, and implement only authorized scope | engineering owner has approved the work; any additional requested scope requires new authority |
| implementation, checks, evidence, and honest work-order state are complete but no clean candidate commit exists | run review checks, resolve findings, and obtain authority for a clean candidate commit | actor authorized to create the candidate commit |
| clean candidate commit exists for work requiring commit-bound verification | prepare a `ready` VREC with exact work, verification, evidence, and commit identity | preparation is bounded automation; assurance judgment remains separate |
| VREC is `ready` | accountable evidence review and decision to verify, reject, or request remediation | assurance owner |
| VREC is `verified` | prepare a pull request or, when separately authorized, prepare a release record | repository/hosting owner for PR action; release owner for release scope |
| RLS is `ready` | accountable release review and decision to release, reject, or request remediation | release owner |
| RLS is `released` | perform only separately authorized tag, publication, deployment, or operating actions | applicable release, publication, deployment, or service owner |
| a check fails or a stop condition applies | retain current state and remediate within scope or escalate the named blocker | owner of the affected scope or decision |

## Behavioral rules

1. Emit the handoff whenever the agent yields after completing a lifecycle stage or encountering a boundary that prevents completion.
2. Report all work completed in the turn, but derive the recommendation from the final lifecycle state actually reached.
3. Identify formal objects with their actual stable IDs and identify an exact commit with its full hash when commit identity is applicable and known.
4. Select one primary next step from managed `WORKFLOW.md`. Do not substitute a generic `What would you like to do next?` when a bounded recommendation exists.
5. Name the accountable role and distinguish an already-granted authority from a new human decision still required.
6. Include an exact safe command when the managed workflow defines one and its arguments are known. Otherwise include a suggested user response. Do not invent a command for approval or lifecycle judgment.
7. If multiple valid paths exist, list bounded alternatives and state the additional authority each path requires. Alternatives must not obscure the primary recommendation.
8. A recommendation never performs or implies approval, implementation authorization, commit, push, pull-request creation, verification, release, tag, publication, deployment, or operation.
9. A failed check, invalid graph, damaged managed installation, incomplete context, missing authority, or stop condition keeps the lifecycle state unchanged and produces remediation or escalation guidance tied to the exact blocker.
10. If one authorized turn completes adjacent stages without yielding, do not invent intermediate approval prompts. Summarize the completed stages and recommend from the final state.
11. `ENGINEERING_HARNESS.md` states the stable handoff obligation and routes stage-specific procedure to `WORKFLOW.md`; it must not duplicate the ordered lifecycle procedure.
12. `WORKFLOW.md` owns the stage mapping, command placement, failure behavior, and alternative paths. `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` retain their existing authority, evidence, and provenance responsibilities.
13. The managed `AGENTS.md` fragment remains a thin single-route gate and does not duplicate the handoff contract.
14. Public README examples demonstrate at least a draft-packet handoff, a failed or incomplete-stage handoff, and a later-stage handoff with alternatives while preserving the existing bounded human entry point.
15. `harnessctl inspect` and its structured suggestions remain unchanged. Conversational handoffs may contain exact commands because they report known completed work; Inspector suggestions remain a separate, non-executable observation projection.

## Error and recovery behavior

- If current formal state cannot be established, say that it is unavailable, name the failed source of truth, and recommend validation or accountable clarification.
- If an ID or command argument is unknown, do not fabricate it. Provide the known next decision and state what information is missing.
- If suggested wording could be mistaken for an exercised decision, explicitly label it as a suggested response.
- If remediation would exceed the selected work order, stop and recommend a new or revised authorization rather than extending scope.

## Data and interface contracts

No JSON, command-line, artifact-metadata, Python API, or Inspector schema changes. The contract is managed UTF-8 Markdown distributed through the existing standard template and protected by schema-2 canonical-text hashes.

## Security and privacy properties

- Do not reproduce secrets, credentials, untrusted pull-request content, or unsafe shell fragments in a recommendation.
- Commands use known repository IDs and paths without executing repository-provided prose.
- Treat target content, artifact metadata, lock data, and user-supplied text as untrusted.
- Preserve all existing authority and external-side-effect prohibitions.

## Performance and capacity

No runtime performance requirement beyond preserving deterministic installation, upgrade, doctor, validation, and preflight behavior. The handoff should remain compact enough to be useful at every stage.

## Observability

- Fresh-install tests inspect the distributed router and workflow rather than only source constants.
- Focused assertions identify reporting-field, stage-mapping, authority, failure, and responsibility-boundary drift.
- README tests retain the bounded public entry shape and verify the expected interaction examples.
- Upgrade, doctor, validation, and preflight expose managed parity and graph consistency.

## Compatibility and migration

- This is a normal managed-template upgrade of `ENGINEERING_HARNESS.md` and `WORKFLOW.md`.
- Unmodified prior managed content upgrades transactionally; customized, ambiguous, or damaged content blocks without partial writes.
- Owner content outside managed markers remains byte-for-byte preserved.
- No repository-owned formal artifact, Inspector configuration, or historical record is migrated automatically.
- The single standard installation and Python 3.11+ standard-library runtime remain unchanged.

## Examples and counterexamples

- **Conforming:** `WO-ABC-001 implementation and evidence are complete; status is implemented. Recommended next step: authorize a clean candidate commit, then prepare VREC-ABC-001. Human authority required: commit authority. Suggested response: "Create the candidate commit for WO-ABC-001; do not push."`
- **Conforming:** `VREC-ABC-001 is ready at illustrative commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa. Recommended next step: the assurance owner reviews the evidence and decides whether to transition it to verified. No verification decision was performed.`
- **Conforming alternative:** after verification, distinguish pull-request preparation from separately authorized release preparation.
- **Nonconforming:** `Everything is done. What would you like to do next?`
- **Nonconforming:** running `prepare-release` merely because a VREC is ready.
- **Nonconforming:** reporting `verified` after tests pass without an accountable VREC transition.
- **Nonconforming:** adding executable remediation commands to Inspector's generic suggestion catalog to satisfy this conversational requirement.

## Explicitly unspecified decisions

Minor prose, headings, compact formatting, illustrative IDs, and test-helper organization are delegated to implementation. The implementation may not remove a semantic handoff field, move ordered procedure into the router, alter Inspector behavior, or broaden authority.
