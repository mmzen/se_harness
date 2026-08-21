+++
id = "SPEC-IAR-013"
type = "specification"
title = "Route operational facts to the owner region and withdraw context actions"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-IAR-021"]
+++

# Specification: Route operational facts to the owner region and withdraw context actions

## Scope

This specification defines the managed instruction-surface and workflow-procedure behavior that satisfies `REQ-IAR-021`. It covers the candidate `ENGINEERING_HARNESS.md` template, the packaged instruction fragment, the workflow-contract reference-step schema, the procedure resolver, and the governed artifacts that describe the withdrawn document as a live obligation.

It excludes the installer, the lock, and the readiness evaluator, which `SPEC-DST-021` owns. It excludes this repository's own `AGENTS.md` owner region, which `SPEC-IAR-012` owns. It excludes the root managed copies of policy modules, which lag the candidate templates until publication and are reconciled only through the separate upgrade workflow.

## Actors and external systems

- The coding agent, which loads `CLAUDE.md` and `AGENTS.md` before task selection and reads the managed router on demand.
- The repository owner, who owns the region the installer preserves.
- The workflow-contract validator and the procedure resolver.
- The released evaluator, executed from outside the checkout.

## Inputs

- `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`, the candidate managed router.
- `templates/repository/standard/AGENTS.md.fragment`, the packaged instruction fragment.
- The active machine-readable workflow contract and its reference-step schema.
- Governed artifacts that name the withdrawn document.

## Outputs

- A revised candidate router that names the owner-controlled region and no scaffolded document.
- A reference-step schema and resolver that accept only a procedure identifier.
- Revised governed artifacts with no active description of the withdrawn obligation.

## State model

The instruction surface has no persistent state. Two transitional states exist during the release cycle and must not be conflated:

- **Candidate revised, root unpublished.** The candidate template names the owner region; the root managed copy still names the withdrawn document. In-tree `doctor` reports this as drift. That is the designed self-hosting state, not a defect.
- **Published.** The root managed copies are reconciled through the upgrade workflow and the two agree.

## Behavioral rules

1. Revise `HRN-002` in place. It states that repository facts and commands belong in the owner-controlled region of `AGENTS.md`, and retains the existing prohibition on that content granting product, engineering, assurance, release, or external-action authority.
2. Do not delete or renumber `HRN-002`. The `HRN-*` identifiers are an ordered published rule vocabulary; removing one renumbers every successor. The rule has no machine references today, and that is not a licence to renumber a published document.
3. Revise the routing-table row whose subject is repository-specific facts and commands so its normative owner is the owner-controlled region of `AGENTS.md`. Retain the row; the subject still has an owner.
4. Remove the stop-condition bullet "repository context is incomplete" from the candidate router. Retain every other stop condition, including managed-integrity failure, invalid graph, missing governing artifact or gate, failing required check, owner-instruction conflict, scope overrun, and absent decision right.
5. Make no change to `templates/repository/standard/AGENTS.md.fragment`. It names exactly one harness destination and continues to do so; this specification adds no second destination and adds no owner-region content requirement to the tracked block.
6. Do not edit the repository-root managed copies of `ENGINEERING_HARNESS.md` or any managed policy module. They belong to the released version and are reconciled at publication.
7. Withdraw the reference-step action form from the contract schema. A reference step declares exactly one `procedure_id`. An `action_id` key is rejected with an explicit diagnostic identifying the withdrawn form, rather than falling through as an unrecognized field.
8. Remove the context-action resolver: the action-marker pattern, the `context_actions` function, the `repository_context` parameter of `resolve_procedure`, the action branch of reference-step resolution, and the action-specific restitution response. Retain `WEX220` for unknown, cyclic, and over-depth procedure references.
9. Revise `SPEC-WEX-002` rules 20 and 22 and its reference-grammar note so a reference step admits only a procedure identifier, and revise the corresponding `VER-WEX-002` matrix row. Revise the `REQ-WEX-010` reference-step definition and its repository-operations constraint.
10. Do not retain a general-purpose mechanism for executing content from an ungoverned file. Repository-specific operations are stated as owner prose, not bound as executable steps.
11. Revise every active governed artifact that describes the withdrawn document as a live obligation, listed in the implementing work order. Do not modify historical evidence, verification records, or release records.
12. Set `REQ-IAR-005` and `REQ-DST-008` to `superseded`, and remove `REQ-IAR-005` from the `assures` relation of `OPS-IAR-001`. Measurement of the current graph shows this is the single validator consequence of the two supersessions.
13. Revise the `REQ-IAR-003` acceptance criterion so it illustrates seed presence-tracking with `docs/engineering/README.md` alone. `REQ-IAR-003` remains active; only its example changes.
14. Preserve the tracked block of every fragment-mode file byte-for-byte. `utf8-text-lf-v1` canonicalizes line endings only; any other whitespace change breaks the digest.

## Error and recovery behavior

- A candidate router still naming the withdrawn document fails the routing-content check, which reports the exact line.
- A contract declaring a reference step with `action_id` is rejected at validation, before resolution, with a diagnostic naming the withdrawn form.
- A resolver reached with a reference step it cannot resolve raises `WEX220` and reports the unresolved identifier without substituting another step.
- A managed-fragment digest mismatch fails `doctor`, preflight `I001`, and the required CI check. Recovery is to restore the exact tracked bytes, not to regenerate the lock.
- Superseding a requirement while an active operating contract still assures it produces `E017`. Recovery is to revise the operating contract within this work order, never to leave the error or to reactivate the requirement.

## Data and interface contracts

- `HRN-*` rule identifiers are a stable published vocabulary. Text may change; identity and order may not.
- The reference-step schema is a versioned public interface. Withdrawing the action form is a breaking change and belongs in the release migration note.
- The routing table is a documented contract between the router and the focused policy modules. Its subject column is unchanged; one owner value changes.

## Security and privacy properties

- The change removes an execution path that read step bodies from a repository-authored, presence-only-tracked file and inlined them into a resolved procedure. Measurement shows the path is unreachable in the shipped product: no caller supplies `repository_context`, so any action step raises rather than resolving. Removing unreachable execution of untrusted content eliminates a latent injection surface rather than a live one.
- No new file is read or executed. The owner region is never parsed, validated, or hashed by this change.
- Withdrawing an unenforceable stop condition does not weaken any enforceable one.

## Performance and capacity

No performance expectation. The removed code path is unreachable and the router changes are textual.

## Observability

- The routing table continues to show one owner per subject, so an agent can still answer "where do repository commands live" from the router alone.
- Contract validation gains one explicit diagnostic for the withdrawn reference form.
- In-tree `doctor` will report candidate-versus-root drift on `ENGINEERING_HARNESS.md` until publication. Evidence must label that as the designed self-hosting state and quote the released evaluator for any assurance claim.

## Compatibility and migration

- Breaking for any consumer whose workflow contract declares a `CTX-ACT-*` reference step. Measurement finds zero such steps across the seventeen procedures in both the released contract and the candidate template, and the form is unreachable regardless.
- Breaking for a consumer relying on the withdrawn stop condition to halt agents. Such a consumer must state the condition in their own owner region, where it is theirs to enforce.
- The migration note covers the revised `HRN-002` text, the changed routing owner, the removed stop condition, and the withdrawn reference form.

## Examples and counterexamples

- Example: `HRN-002` reads that repository facts and commands belong in the owner-controlled region of `AGENTS.md` and grant no authority. The rule ID and its position are unchanged.
- Example: a contract with a reference step declaring `procedure_id` resolves as before, with unchanged ordering and output.
- Counterexample: deleting `HRN-002` and renumbering. Rule 2 forbids it.
- Counterexample: adding `AGENTS.md` as a second destination inside the tracked fragment block. Rule 5 forbids it and it would break the fragment digest.
- Counterexample: replacing the removed stop condition with "the owner region is incomplete". That reintroduces an unenforceable condition over content the harness does not track, and fails `REQ-IAR-021` response item 8.
- Counterexample: editing the repository-root `ENGINEERING_HARNESS.md` so in-tree `doctor` stops reporting drift. Rule 6 forbids it; it would break the lock and the required CI check.

## Explicitly unspecified decisions

- The exact wording of the revised `HRN-002`, the routing-table owner cell, and the rejection diagnostic, subject to the required content above.
- Whether the withdrawn reference form is rejected by the schema validator, the contract loader, or both, provided rejection occurs before resolution.
- Test module names and placement, subject to `VER-IAR-013`.
- The order in which the governed-artifact revisions are applied within the work order.
