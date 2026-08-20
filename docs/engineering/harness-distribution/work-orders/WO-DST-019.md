+++
id = "WO-DST-019"
type = "work_order"
title = "Implement safe explicit artifact renumbering"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[assurance]
commit_bound_verification = "required"
rationale = "Future repository and assurance decisions will rely on a mutating control that rewrites formal identities, relations, and tracked paths, reports remaining manual references, and claims transactionality and historical preservation."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-DST-061"]
specifications = ["SPEC-DST-019"]
architecture = ["ARCH-DST-012", "ADR-DST-012"]
verification = ["VER-DST-019"]
+++

# Work Order: Implement safe explicit artifact renumbering

## Lifecycle

On 2026-08-20, after reviewing the broader prevention proposal for issue 80, the repository owner chose a narrower recovery mechanism and authorized creation of this artifact packet. That instruction authorizes drafting `REQ-DST-061`, `SPEC-DST-019`, `ARCH-DST-012`, `ADR-DST-012`, `VER-DST-019`, and this bounded work order for review. It does not approve the artifacts, authorize implementation, transition lifecycle state, create evidence, commit, push, open a pull request, build a distribution, verify, release, tag, publish, or deploy.

On 2026-08-20, after reviewing the packet refinement that keeps semantic hard-reference changes manual and makes them explicit in command output, the repository owner stated `I approve the issue-80 renumbering packet for implementation`. That instruction approves the complete governing chain and this bounded work order and authorizes implementation after passing start preflight. It does not authorize a commit, push, pull request, candidate verification, release, tag, publication, deployment, or external mutation.

Start preflight passed on 2026-08-20 using the exact released 0.5.0a1 evaluator, and the implementation actor read its complete manifest before beginning work. The `in_progress` status records execution within the approved scope; it does not claim completion or verification.

Implementation completed on 2026-08-20 with retained evidence at `docs/engineering/harness-distribution/evidence/WO-DST-019-verification.md`. The command, focused transaction and boundary tests, advanced command reference, and governing packet agree on structured-only automatic edits plus explicit manual-reference disposition. The `implemented` status records completion of the authorized work only; commit-bound verification remains required, Python 3.11 was not available locally for execution, and no commit, VREC, release, or external action is implied.

After review preflight, inspection, retained evidence, and the completed verification report, the repository owner explicitly instructed `OK: commit the reviewed candidate under WO-DST-019` on 2026-08-20. This authorizes one local candidate commit containing the bounded reviewed change set. It does not authorize push, pull-request mutation, VREC preparation or transition, release, tag, publication, deployment, or external action.

Commit-bound verification is classified `required` because implementation will add a repository-mutating control whose correctness affects formal identity, graph integrity, evidence interpretation, filesystem recovery, and future assurance decisions.

## Objective

Implement the approved `renumber-artifacts` contract, if and only if the complete governing packet is separately approved, so the mechanical portion of an explicitly selected pre-assurance collision can be repaired through a deterministic reviewed plan and recoverable transaction, with semantic hard references handed off for manual disposition, without falsifying evidence or rewriting commit-bound history.

## In scope

- Add the plan-by-default `harnessctl renumber-artifacts` CLI with repeated explicit `OLD=NEW` mappings, optional JSON, and explicit `--apply`.
- Implement clean-Git inventory, strict mapping and artifact validation, lifecycle and VREC/RLS blockers, parsed identity/relation planning, tracked path planning, deterministic manual-reference reporting with file/line locations, unsupported-content reporting, immutable evidence-content classification, bounded output, recoverable application, rollback, and postcondition validation.
- Support canonical and valid legacy artifact paths plus work-order evidence directory and filename moves.
- Add deterministic boundary, security, capacity, failure-injection, rollback, package, CLI, documentation, and regression tests required by `VER-DST-019`.
- Update the advanced command reference and concise operator/agent guidance needed to explain the new recovery command without adding it to the root human six-command surface.
- Keep candidate package behavior, the single standard installation, and installed evaluator isolation coherent.
- Retain implementation evidence under `docs/engineering/harness-distribution/evidence/WO-DST-019-verification.md` after authorized execution.

## Out of scope

- Ref-aware authoring checks, `next-id`, identifier allocation, reservation ledgers, distributed locking, PR merge-base comparison, workflow collision detection, automatic fetch, or remote coordination.
- Inferring a chain or replacement identifier from graph reachability, filenames, branch names, prose, or numeric maxima.
- Renumbering, modifying, superseding, rejecting, deleting, or recreating verification records or release records.
- Repairing a claimant already referenced by commit-bound provenance.
- Automatic commit, branch, push, pull request, merge, version, release build, release record, tag, publication, deployment, or external repository mutation.
- Automatically rewriting free-form artifact bodies, documentation, source, tests, captured evidence content, unrelated artifact migration, maintenance-warning remediation, or new installation profiles.

## Authorized decision envelope

After separate packet approval, the implementation agent may choose internal module boundaries, conservative capacity limits, recovery-file names and layout, stable diagnostic codes, JSON field grouping, concise human wording, and test fixture organization. Those choices must preserve the exact public command, mapping semantics, lifecycle and provenance refusal, evidence-byte immutability, clean-worktree requirement, deterministic plan, transactional recovery, postcondition checks, and authority boundary in `SPEC-DST-019`.

The agent may not add an escape hatch that bypasses blockers, infer additional mappings, make evidence editable, support VREC/RLS renumbering, weaken rollback, introduce network access or dependencies, or perform Git authority actions. Any platform limitation that prevents the required safety or restoration proof is a stop condition, not delegated risk acceptance.

## Constraints

- Use Python 3.11+ standard-library runtime behavior only.
- Treat all repository and Git inputs as untrusted and never execute target content.
- Preserve all free-form owner content, protected managed content, file encodings, line endings, modes, and evidence bytes; change only selected identity fields, parsed typed relations, and mapped paths.
- Require a clean repository and a complete blocker-free plan before mutation.
- Preserve historical VREC/RLS and release facts byte-for-byte.
- Make no distribution build and do not update version, released evaluator selection, workflow identity, release orchestration, or credentials.
- Preserve unrelated user changes and stop if the worktree or reviewed packet changes underneath implementation.

## Expected change surface

- Portable package CLI and a focused repository-renumbering planning/transaction component.
- Existing safe-path, artifact-layout, graph-validation, and Git-boundary integration points where reuse preserves their current contracts.
- Focused CLI, authoring, provenance, standard-lifecycle, installer/package, security, and transaction tests using disposable repositories.
- Advanced command reference and any managed/package parity assertions required by the new command.
- This packet's domain index entry and later retained work-order evidence.

## Required verification

- Start and review preflight for `WO-DST-019` at their phase-appropriate times.
- Every matrix, acceptance, property, architecture, security, capacity, resilience, manual, and evidence requirement in `VER-DST-019`.
- Focused tests for CLI parsing, mapping normalization, structured relation repair, path moves, complete manual/preserved/unsupported reference classification, non-editing of free-form content, evidence preservation, VREC/RLS blockers, deterministic output, hostile inputs, and rollback at every mutation phase.
- Candidate-source and fresh installed-candidate command checks without checkout contamination.
- Python 3.11 and the available local supported runtime.
- Complete unit suite, formal artifact validation, release-distribution validation, CLI help, managed-integrity doctor, package/template parity where applicable, and final diff hygiene.
- Exact confirmation that no release distribution, ref update, commit, push, PR mutation, lifecycle transition, publication, deployment, or external configuration change occurred.

## Evidence to record

Record the accountable approval, preflight manifests, files read, implementation decisions within the delegated envelope, exact changed paths, mapping and capacity fixtures, complete manual/preserved/unsupported reference inventories and accountable dispositions, before/after evidence and rollback hashes, injected failure phases, hostile-input cases, human/JSON samples, focused and full commands with exit codes and test counts, Python and Git versions, validation warning counts, doctor and package results, final diff review, deviations, residual risks, and every unperformed authority action under `docs/engineering/harness-distribution/evidence/WO-DST-019-verification.md`.

## Stop and escalate conditions

Stop if the packet remains draft or is revised after approval; start preflight fails; any manifest file is unread; a safe reusable boundary is unavailable; implementation would execute target content, alter evidence bytes, rewrite VREC/RLS facts, weaken clean-state or rollback guarantees, introduce a dependency or network behavior, change another public contract, exceed declared capacity without deterministic failure, fail a required check, overlap unrelated changes, require a release build, or need authority beyond this work order.

## Completion report format

Report the implemented command and exact public interface, mapping behavior, structured automatic changes, manual-reference output and dispositions, evidence-preservation behavior, transaction and rollback proof, changed components, retained evidence path, focused and full verification results, final work-order lifecycle state, residual uncertainty, unchanged governance and external-action boundaries, and the one next separately authorized lifecycle step.
