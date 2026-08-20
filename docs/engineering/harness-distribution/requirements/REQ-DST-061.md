+++
id = "REQ-DST-061"
type = "requirement"
title = "Repair pre-assurance artifact identifier collisions safely"
status = "approved"
owners = ["product-owner", "engineering-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN an unrelated engineering artifact chain collides on identifiers before commit-bound assurance or release facts exist for the selected claimant, THE SYSTEM SHALL provide a deterministic transactional renumbering operation that updates explicitly mapped identities, parsed typed relations, and mapped paths, identifies hard references for manual repair, and preserves retained evidence bytes and established governance history."
verification_method = "automated-boundary-failure-and-transaction-tests"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Repair pre-assurance artifact identifier collisions safely

## Rationale

Concurrent branches can independently create unrelated artifacts with the same identifiers while every checkout-local authoring and validation check passes. The collision may become visible only during integration, after identifiers have spread through formal relations, source comments, tests, documentation, filenames, and large work-order evidence trees. Manual correction is expensive and risks partial graph changes, stale references, altered captured output, or accidental rewriting of assurance history.

This requirement provides bounded recovery rather than distributed allocation. It does not claim that an offline checkout can prevent or observe identifiers chosen in another unshared checkout.

## Preconditions and trigger

The operation applies only when:

- the target is a non-bare Git working tree with no staged, tracked, untracked, merge, rebase, or other in-progress repository changes;
- every old and new identifier is supplied explicitly by the caller;
- each old identifier resolves to exactly one non-record formal artifact in the current checkout;
- each new identifier is absent from the current checkout, matches the selected artifact type, and is not reused elsewhere in the requested mapping;
- every selected artifact is in `draft`, `approved`, `in_progress`, or `implemented` state; and
- no verification record or release record references any selected artifact or its old identifier.

The command may repair several related artifacts in one transaction, but it never infers which artifacts form a chain or chooses the replacement identifiers.

## Required response

- Provide `harnessctl renumber-artifacts TARGET --map OLD=NEW [--map OLD=NEW ...] [--json] [--apply]`.
- Treat omission of `--apply` as a read-only plan using the same discovery and validation path as application.
- Build a complete deterministic plan before writing, including declared-identifier changes, typed-relation changes, path moves, evidence-path moves, hard references requiring manual review, preserved evidence-content references, unsupported-content references, blockers, and resulting validation expectations.
- Update only each selected artifact's declared identifier, every parsed formal relation to the old identifier, and affected tracked path names. Do not automatically rewrite free-form artifact bodies, documentation, source, tests, or other repository text.
- Rename affected tracked paths, including canonical or legacy artifact filenames and work-order evidence directories or filenames, without changing retained evidence file bytes.
- Preserve UTF-8 BOM presence, line terminators, file mode, and every unaffected byte.
- Produce deterministic human output and optional JSON that record the mapping, original `HEAD`, changed and moved paths, hard references requiring manual review and change with path and line where available, preserved evidence occurrences, unsupported binary or non-UTF-8 occurrences requiring inspection, before/after SHA-256 values, validation result, and authority boundary.
- Set and prominently render `manual_action_required = true` whenever reported references remain. A successful apply must say that structured renumbering succeeded but repository repair is not complete until the reported hard references are reviewed and changed or explicitly documented.
- Apply the complete plan as one recoverable transaction, validate the resulting formal graph before reporting success, and restore the original paths and bytes if any write, move, or validation step fails.
- Leave the repository with reviewable uncommitted changes and never commit, push, approve, verify, release, publish, or delete Git history.

## Failure and boundary behavior

Refuse without partial writes when the repository is dirty; a mapping is malformed, duplicated, chained, cyclic, type-incompatible, missing, or colliding; a destination exists; an affected path is unsafe, linked, unreadable, or outside the repository; a selected artifact has an ineligible lifecycle state; a VREC or RLS references selected work; structured-field or evidence-byte preservation cannot be proved; the reference inventory cannot be completed within declared bounds; the plan changes between validation and application; or post-application graph validation fails.

Free-form occurrences outside evidence can be semantic hard references, historical narrative, or unrelated text. The command reports them for manual review rather than guessing which should change. Evidence contents may truthfully retain the old identifiers because captured program output and contemporaneous observations must not be falsified; those occurrences are reported separately and only their repository paths move when mapped. Binary and non-UTF-8 occurrences are reported as requiring manual inspection.

If a colliding artifact already participates in commit-bound verification or release provenance, recovery requires separate accountable disposition; this command must not rewrite that history.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and the single standard installation.
- Treat mappings, Git output, repository paths, file content, front matter, relations, encodings, links, and filesystem behavior as untrusted input.
- Preserve artifact type, lifecycle state, owner, dates, requirement statements, decision content, artifact-body content, and every semantic field other than selected identifiers and parsed typed relations.
- Preserve evidence content byte-for-byte; renaming a path does not authorize editing the file it contains.
- Preserve managed-file ownership and refuse a plan that would rewrite a protected managed file outside its permitted marker or lock contract.
- Do not fetch or scan other refs, allocate an identifier, infer a chain, rewrite VREC/RLS facts, create a commit, or promise collision prevention.

## Acceptance examples

### Example: normal multi-artifact repair

**Given** one clean branch contains unrelated draft or implemented `REQ-MOK-040`, `SPEC-MOK-010`, `VER-MOK-010`, and `WO-MOK-010`, with no VREC or RLS referencing them

**When** an operator explicitly maps them to unused type-compatible identifiers and applies the validated plan

**Then** the artifacts, typed relations, and evidence paths use the new identifiers; the output identifies each free-form hard reference that must be reviewed and changed manually, separately identifies preserved evidence and unsupported-content occurrences, states whether manual action remains, and formal validation passes without changing evidence bytes.

### Example: immutable assurance boundary

**Given** `VREC-MOK-010` references `WO-MOK-010`

**When** an operator requests `WO-MOK-010=WO-MOK-011`

**Then** the command reports the commit-bound record as a blocker and writes nothing.

### Example: transaction failure

**Given** a valid plan spanning multiple files and directories

**When** an injected failure occurs after at least one staged replacement or move

**Then** the original repository paths, bytes, and index/worktree state are restored and the command reports failure without claiming completion.

## Open decisions

The packet proposes the explicit-mapping, evidence-preserving recovery boundary above. Accountable product, technical, assurance, and engineering owners must approve or revise that boundary before implementation; no identifier-allocation or collision-prevention decision is implied.
