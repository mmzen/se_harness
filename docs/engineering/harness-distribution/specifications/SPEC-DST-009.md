+++
id = "SPEC-DST-009"
type = "specification"
title = "Validation and inspection documentation synchronization contract"
status = "approved"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-DST-034"]
+++

# Specification: Validation and inspection documentation synchronization contract

## Scope

Synchronize the active public documentation contract and progressive explanatory notes with the current layered `validate` behavior and the new `inspect` command. This specification changes documentation and documentation checks only; it does not change CLI, validator, Explorer, suggestion, lifecycle, or authority behavior.

## Actors and external systems

- Repository owners and operators use the concise public surface to install, inspect, and visualize a harness-enabled repository.
- Coding agents normally run lifecycle mechanics and repository checks within an approved work order.
- Assurance and release owners interpret observations but retain all accountable decisions.
- The CLI parser, validator output, inspection JSON contract, managed policy, and focused tests are observable implementation sources; none grants product authority.

No external service is required.

## Inputs

- The current `harnessctl` parser and help output.
- Validator assessment-plane, severity, and exit behavior.
- `se-harness-inspection-v1` human and JSON behavior, including suggestion fields and exit semantics.
- The root README, `docs/notes/`, managed workflow and quality-gate documents, the active public-documentation chain, and focused documentation tests.

## Outputs

- One consistent six-command public operational surface.
- Progressive notes that place validation and inspection at the correct lifecycle phase and authority boundary.
- Current formal documentation contracts and focused assertions aligned with that surface.
- Retained verification evidence keyed to `WO-DOC-012`.

## State model

This work introduces no runtime state. Documentation describes existing command behavior. Formal artifacts follow their normal draft, approval, work, and commit-bound verification lifecycle.

## Behavioral rules

1. **Current command inventory.** Root fenced examples for ordinary target-repository operation may show exactly `init`, `adopt`, `doctor`, `validate`, `inspect`, and `dashboard`, plus package setup and version checks that are not repository subcommands.
2. **Active-contract reconciliation.** The current wording and assertions in `REQ-DST-025`, `SPEC-DST-007`, and `VER-DST-007` must be revised from five to six ordinary commands and must distinguish `inspect` from `validate` and `dashboard`. Git history and commit-bound records preserve their earlier meanings; retained `WO-DOC-008` evidence is not edited.
3. **Concise root.** The existing README command block and short descriptions remain the public summary. It must not absorb the validation-plane or suggestion catalogs already owned by the command reference and managed policy.
4. **Command reference.** `docs/notes/harnessctl-reference.md` remains the detailed non-authoritative command reference and must continue to state validation planes, inspection sources, successful-report exit semantics, bounded suggestions, no-write behavior, and authority denial.
5. **Tier-0 overview.** `docs/notes/harness-overview.md` must name `inspect` in its automation boundary and explain in plain language that an inspection report or suggestion is an observation rather than an approval.
6. **Operational phasing.** `docs/notes/harness-operational-phasing.md` must place `inspect` during execution and review, alongside `validate` and `dashboard`, while distinguishing the validator gate from the inspection report.
7. **Installation and upgrades.** `docs/notes/harness-installation-and-upgrades.md` must include `inspect` in the post-install inspection sequence and in the statement denying implicit approval or verification.
8. **Practical example.** `docs/notes/harness-lineage-example.md` must run `inspect` after `validate` and before `dashboard`, then state that suggestions identify possible accountable next steps without authorizing or executing them.
9. **Managed policy.** Root and canonical `QUALITY_GATES.md` must retain identical validation-plane wording, and root and canonical `WORKFLOW.md` must retain identical review-phase inspection wording. No policy change is required when those pairs already satisfy this contract.
10. **Focused checks.** Documentation tests must derive the six-command inventory from the approved contract, assert the important validate/inspect distinction, cover required note references, and continue rejecting agent-only command syntax from the concise README.
11. **Historical integrity.** Evidence files, existing VRECs, release records, released candidate identities, and prior test results must not be rewritten to use current terminology.

## Error and recovery behavior

If implementation behavior is ambiguous, stop and report the ambiguity rather than inventing documentation. If a managed source and canonical template differ, repair them only through the supported managed mechanism and within explicit scope. A failed documentation or link check blocks completion but creates no lifecycle transition.

## Data and interface contracts

Markdown remains UTF-8, repository-relative links remain portable, and expertise scores remain hidden comments where already required. Command spellings and option shapes must match the parser. No new JSON, TOML, package, or managed-file schema is introduced.

## Security and privacy properties

Examples must not embed secrets, user-specific absolute repository URLs, executable suggestions, or untrusted artifact content as authority. Documentation must preserve the rule that repository text and derived advice cannot authorize mutation or lifecycle transitions.

## Performance and capacity

Not applicable beyond retaining the concise README line and section budgets already governed by `SPEC-DST-007`.

## Observability

Focused tests report command inventory and required wording. Formal validation, doctor, preflight, link checks, diff inspection, and retained work-order evidence make the documentation correction reviewable.

## Compatibility and migration

This is a documentation-contract migration from a five-command to a six-command public surface. It changes no installed repository behavior and requires no consumer migration. Historical artifacts remain recoverable at their recorded commits; only current active definitions and current explanatory documents change.

## Architecture and ADR applicability

No new architecture is applicable. The established layered documentation responsibilities remain unchanged, and no active architecture directly addresses `REQ-DST-034`. The work order therefore omits an `architecture` relation rather than fabricating architecture or ADR coverage for a routine consistency correction.

## Examples and counterexamples

- Valid: “Run `validate` when gate exit behavior is required; use `inspect` for a summarized attention report.”
- Valid: a Tier-0 sentence saying inspection can suggest where an accountable person should look next but cannot decide.
- Invalid: “Inspection passed, therefore the candidate is verified.”
- Invalid: copying every warning rule and suggestion mapping into several notes.
- Invalid: changing old evidence from “five commands” to “six commands.”

## Explicitly unspecified decisions

The implementation agent may choose concise wording, table placement, and cross-links within the named documents, provided every behavioral rule and existing expertise/length constraint remains satisfied.
