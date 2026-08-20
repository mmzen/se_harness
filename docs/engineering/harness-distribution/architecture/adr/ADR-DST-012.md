+++
id = "ADR-DST-012"
type = "adr"
title = "Explicit transactional renumbering with immutable evidence contents"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
decides = ["ARCH-DST-012"]
+++

# ADR: Explicit transactional renumbering with immutable evidence contents

## Status

Accepted.

## Context

Artifact identifiers propagate beyond front matter into typed relations, narrative text, source comments, tests, filenames, evidence namespaces, and retained command output. A collision discovered during integration therefore creates a choice between manual repair, inferred whole-chain migration, prevention infrastructure, or a bounded explicit recovery transaction.

The repository's authority model makes two distinctions decisive. Related artifacts may be shared, so graph reachability cannot safely select what to rename. Retained evidence must remain truthful, so captured output cannot be edited merely to appear consistent with a later identifier.

## Decision drivers

- Reduce the cost and error rate of collision recovery without claiming distributed uniqueness.
- Preserve explicit human control over which artifacts move and which identifiers replace them.
- Preserve evidence bytes and all commit-bound verification and release facts.
- Prevent partial writes across metadata, relations, and path changes while making the remaining manual text work explicit.
- Remain standard-library-only, deterministic, local, and compatible with the single installation.
- Keep plans reviewable and leave final changes uncommitted for ordinary governance.

## Considered options

1. **Continue manual renumbering.** No new product surface, but prior recovery changed dozens of files and hundreds of references, required bespoke evidence explanations, and remained vulnerable to omission and partial repair.
2. **Infer a complete chain from one work order.** Convenient, but graph reachability includes shared intent, requirements, specifications, architecture, and verification contracts that may not belong to the colliding claimant.
3. **Apply explicit maps transactionally to structured identities, relations, and paths; report free-form references for manual repair; and preserve evidence contents.** Requires the operator to choose every moved artifact and review semantic references, but makes the mechanical mutation complete, reviewable, recoverable, and honest about historical output.
4. **Implement ref-aware allocation, a next-ID command, PR collision checks, or a reservation ledger first.** May reduce future collisions, but introduces broader coordination and policy while leaving existing collisions expensive to repair.
5. **Rewrite VREC/RLS records together with the chain.** Produces superficial naming consistency by changing exact historical provenance and is incompatible with established governance authority.

## Decision

Choose option 3.

Add one plan-by-default `renumber-artifacts` command accepting repeated explicit `OLD=NEW` mappings. The command constructs one immutable plan over selected formal identities, all parsed relation targets, and affected tracked paths. It separately inventories exact old-identifier occurrences in free-form text for manual review, with file and line where available, and reports binary or non-UTF-8 occurrences for inspection. It applies the structured plan only with `--apply`, validates graph and byte/path postconditions, and rolls back on any failure.

Free-form artifact bodies, documentation, source, and tests are never rewritten automatically because an occurrence may be a current hard reference, historical narrative, or unrelated text. Content beneath an exact engineering `evidence` path is also never rewritten. Evidence directories and filenames may move to the new work-order namespace, while captured bytes and their hashes remain unchanged and old identifier occurrences are reported in a separate preserved-evidence category.

Any VREC/RLS reference to a selected artifact blocks the operation. The command does not renumber verification or release records, allocate identifiers, scan other refs, fetch, reserve, commit, or infer a chain.

## Consequences

### Positive

- Collision repair becomes reproducible and reviewable instead of an ad hoc repository-wide edit.
- Explicit mapping prevents shared artifacts from being swept into an inferred migration.
- Evidence remains truthful while its namespace can move with the selected work order.
- Hard references that need semantic judgment are visible as an explicit manual-action list instead of being guessed by a repository-wide replacement.
- Full-plan validation and rollback reduce partial graph and filesystem states.
- The narrower command can ship independently of future allocation policy.

### Negative

- Operators still choose replacement identifiers and can collide with unseen branches or clones.
- A clean worktree is required, so in-progress work must be safely committed or otherwise resolved before use.
- Ready or later provenance cannot be repaired through this command; accountable disposition and fresh assurance may still be necessary.
- Operators must review and change or explicitly document reported free-form hard references after apply; the command cannot by itself claim complete repository repair.
- Cross-platform multi-path recovery remains security-sensitive and requires substantial failure testing.

### Operational and migration effects

- Existing repositories change only when an authorized operator invokes `--apply`.
- The command leaves an ordinary uncommitted diff plus a deterministic manual-action report for review and subsequent governed evidence capture.
- Preserved evidence can contain old identifiers by design; reviewers use the command report and unchanged hashes to distinguish historical output from current graph identity.
- Future prevention work may coexist with this recovery facility without changing its authority boundary.

## Validation

Apply `VER-DST-019`. Independently verify explicit-map completeness, type and lifecycle guards, VREC/RLS refusal, structured relation and path repair, complete deterministic manual-reference reporting, no automatic free-form edits, exact evidence-byte preservation, deterministic human/JSON plans, hostile path and encoding boundaries, injected failures with verified restoration, formal validation, package and documentation parity, Python 3.11 plus the local runtime, and the full regression suite.
