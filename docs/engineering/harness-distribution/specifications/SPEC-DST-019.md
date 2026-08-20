+++
id = "SPEC-DST-019"
type = "specification"
title = "Explicit transactional artifact renumbering contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
specifies = ["REQ-DST-061"]
+++

# Specification: Explicit transactional artifact renumbering contract

## Scope

Add one portable `harnessctl renumber-artifacts` command for repairing explicitly identified pre-assurance collisions in a clean Git checkout. The command plans or applies one all-or-nothing mapping across formal artifact identities, typed relations, and tracked paths. It inventories free-form hard references for manual repair and treats retained evidence content as immutable historical observation.

This contract is a recovery mechanism. It does not allocate identifiers, inspect other refs, coordinate writers, detect pull-request collisions, or replace accountable review.

## Actors and external systems

- A coding agent or repository maintainer supplies and reviews the complete old-to-new mapping.
- Git supplies the exact current `HEAD`, tracked path inventory, file modes, and clean-worktree observation.
- The released SE Harness evaluator parses formal artifacts, constructs the plan, performs the bounded transaction, and validates the resulting graph.
- Accountable owners authorize renumbering and later lifecycle decisions; the command exercises none of those rights.
- No network service or external runtime dependency participates.

## Inputs

```text
harnessctl renumber-artifacts TARGET \
  --map OLD=NEW [--map OLD=NEW ...] \
  [--json] [--apply]
```

- `TARGET` defaults to `.` and must resolve to a non-bare Git working tree containing a valid installed harness.
- At least one `--map` is required.
- Each mapping contains exactly one old and one new identifier in the existing formal identifier grammar.
- Mapping order has no semantic effect.
- `--json` selects the public machine-readable representation.
- Without `--apply`, the command is read-only and returns the complete plan.

## Outputs

Human and JSON results expose:

- schema and command version;
- mode: `plan` or `apply`;
- resolved repository root and full original `HEAD`;
- normalized mappings sorted by old identifier;
- selected artifacts with type, lifecycle state, and source path;
- structured identifier and typed-relation changes plus path moves in deterministic order;
- `manual_references`, containing each exact old-identifier occurrence in non-evidence free-form UTF-8 text with repository path, one-based line, identifier, and occurrence count;
- evidence paths moved without content modification;
- `preserved_evidence_references`, containing old-identifier occurrences intentionally preserved inside evidence;
- `unsupported_references`, containing binary or non-UTF-8 paths and bounded occurrence counts that require manual inspection;
- `manual_action_required`, true whenever either manual or unsupported references remain, with prominent human text that names the required follow-up;
- blockers, warnings, before/after SHA-256 values, rollback outcome, and formal-validation outcome;
- `automatic = false` and a statement that success does not approve, verify, release, commit, or reserve an identifier.

Repository-controlled values are escaped and bounded in human output. JSON contains structured values rather than preformatted commands.

When manual work remains, the human apply result uses an unmistakable separation such as:

```text
STRUCTURED RENUMBERING: APPLIED
MANUAL ACTION REQUIRED: 3 free-form references must be reviewed
  docs/.../REQ-MOK-011.md:42  REQ-MOK-040 -> REQ-MOK-041
  src/.../feature.py:18         WO-MOK-010 -> WO-MOK-011
PRESERVED EVIDENCE REFERENCES: 7 occurrences; do not rewrite captured evidence
UNSUPPORTED REFERENCES: 1 binary path requires manual inspection
REPOSITORY REPAIR COMPLETE: no
```

The exact wording may be concise, but the manual-action status, actionable locations, preserved-evidence warning, and incomplete-repair status are required.

## State model

```text
request
  -> inventory exact clean HEAD and tracked files
  -> parse and normalize explicit mappings
  -> resolve artifacts, relations, references, and destinations
  -> validate complete plan
  -> report plan
  -> [--apply] stage recovery data and structured replacements
  -> perform deterministic structured replacements and moves
  -> validate resulting graph and postconditions
  -> remove recovery state and report success

any apply failure
  -> restore original paths, bytes, and modes
  -> verify restoration
  -> report failure
```

No lifecycle field changes as part of this state model.

## Behavioral rules

1. Resolve the repository root without following an attacker-controlled path outside the target. Require an ordinary Git worktree, a full `HEAD`, no in-progress Git operation, and empty porcelain status including untracked files.
2. Parse every map before artifact discovery. Reject empty sides, extra separators, duplicate old or new identifiers, old-equals-new mappings, mapping chains or cycles, unsupported grammar, and maps whose normalized order would change their meaning.
3. Parse the installed artifact root using the same formal front-matter identity rules as ordinary authoring and validation. Every old identifier must resolve exactly once and must not identify a `verification_record` or `release_record`.
4. Require the new identifier to use the prefix registered for the selected artifact type and to be absent from every parsed artifact and planned destination in the current checkout.
5. Accept selected lifecycle states `draft`, `approved`, `in_progress`, and `implemented`. Reject `ready`, `verified`, `released`, `superseded`, `rejected`, unknown states, and malformed metadata.
6. Discover every verification and release record before planning changes. If any record relation or commit-bound snapshot references a selected artifact or old identifier, reject the entire operation. Never rewrite, move, supersede, reject, or delete such a record.
7. Enumerate tracked files and modes from Git without executing target code. Do not traverse submodule contents, linked directories, junctions, or symlink targets. An affected linked path or unsafe destination blocks the plan.
8. In formal artifacts outside an `evidence` path component, change only the selected `id` field and exact old identifiers in parsed typed-relation fields. Preserve artifact bodies, lifecycle, owner, dates, statements, decisions, provenance, formatting, line endings, and unrelated metadata byte-for-byte.
9. Scan other tracked content for exact old-identifier occurrences but do not replace them. Classify occurrences in non-evidence UTF-8 text as `manual_references`; report repository path and one-based line so an operator can review whether each semantic hard reference should change. Classify binary or non-UTF-8 occurrences as `unsupported_references` with path and bounded occurrence count for manual inspection.
10. Treat a literal old identifier as an occurrence only when bounded by start/end or non-ASCII-alphanumeric characters. Do not report ambiguous partial matches as a current hard reference, and never change a larger identifier or arbitrary substring.
11. Rename a tracked path when its filename or path component contains an exact mapped token. Formal artifact files retain their current parent organization while adopting the new filename token. Evidence directories and filenames may move, but file contents under any `evidence` component remain byte-for-byte unchanged.
12. Scan evidence bytes only to count and report `preserved_evidence_references` and hashes. Never substitute, normalize, append a note to, or otherwise edit retained evidence content automatically. Do not combine preserved evidence occurrences with references requiring repair.
13. Reject path collisions, case-folding collisions, reserved or protected destinations, invalid Windows or POSIX components, paths outside the repository, and any plan that would overwrite or merge content.
14. Produce the entire plan before mutation. Recheck `HEAD`, status, source bytes, modes, destinations, and plan identity immediately before apply; any change invalidates the plan.
15. Apply using private same-filesystem recovery state, exclusive destination creation, and deterministic two-phase moves. Preserve file modes and bytes. Clean up only temporary resources created by the invocation.
16. After apply, prove every selected artifact resolves under its new identifier, no parsed `id` or typed relation retains an old identifier, mapped paths have moved, expected evidence bytes and hashes are unchanged, every remaining old-identifier occurrence is accounted for in exactly one of `manual_references`, `preserved_evidence_references`, or `unsupported_references`, Git reports only the planned changes, and formal artifact validation succeeds.
17. If any apply or postcondition step fails, restore every original path, byte sequence, and file mode, remove newly created destinations and temporary state, verify restoration against the pre-apply inventory, and return failure. Never delete pre-existing unplanned content during recovery.
18. Exit zero only for a blocker-free plan or a fully validated structured apply. Outstanding manual references do not turn a valid transaction into command failure, but success output must not claim complete repository repair and must prominently state that manual action remains. Plan blockers, apply failure, failed restoration, or failed graph validation return nonzero with deterministic diagnostics.
19. Never run `git add`, create a commit, update a ref, fetch, push, open a pull request, transition lifecycle state, capture a VREC, prepare a release, or imply that a replacement identifier is globally reserved.

## Error and recovery behavior

Diagnostics identify a stable code, mapping or path subject, bounded message, and phase: `input`, `inventory`, `plan`, `apply`, `postcondition`, or `rollback`. Multiple pre-write blockers are sorted and reported together when safe. Apply stops at the first mutation failure and prioritizes restoration; later diagnostics distinguish a successfully restored failure from an unresolved recovery failure.

A failed plan writes nothing. A failed but successfully restored apply leaves the repository byte-for-byte and path-for-path equivalent to the original tracked and untracked inventory. If restoration itself cannot be proved, the command reports the recovery-state location and stops without claiming safety or completion.

## Data and interface contracts

- Public JSON uses one versioned schema with deterministic key and list ordering.
- Full Git object IDs and lowercase SHA-256 digests are retained without abbreviation.
- Paths are repository-relative forward-slash strings in output and are never reinterpreted as authority.
- Reference entries carry both original and resulting repository-relative paths when a planned path move changes the location; the human manual-action list points to the resulting path an operator can edit after apply.
- Identifier mapping is one-to-one and type-preserving; transitive maps and swaps are unsupported in the initial contract.
- Evidence classification is path-based on an exact `evidence` component below the installed artifact root.
- The command modifies only parsed identifier and typed-relation fields plus Git-tracked paths selected by the plan; free-form bodies, derived, ignored, submodule, and external content remains untouched.

## Security and privacy properties

- Invoke Git without a shell and with argument termination where supported.
- Bound mapping count, ref/output sizes, path lengths, file count, individual file bytes, aggregate planned bytes, and diagnostic samples.
- Reject duplicate JSON keys and malformed TOML through the existing strict artifact boundary.
- Never import or execute repository Python, hooks, filters, attributes, templates, or commands to discover or replace content.
- Do not expose file bodies, environment values, credentials, or unbounded evidence in output.
- Prevent link, junction, case-folding, hard-link overwrite, device-path, alternate-data-stream, traversal, and time-of-check/time-of-use escapes on supported platforms.

## Performance and capacity

Planning is linear in the bounded tracked path and byte inventory plus formal graph size. The implementation may define conservative limits and report them, but must handle repositories at least as large as the issue-80 incident: 250 evidence files and 500 exact identifier occurrences in one transaction, including a complete deterministic manual-reference inventory.

## Observability

Human and JSON output make the structured plan reviewable before application, make evidence preservation explicit, and separate manual hard-reference work from intentionally preserved evidence. Apply output records exact planned versus completed counts, original `HEAD`, hashes, graph-validation summary, whether rollback was attempted and proved, and whether manual action remains. Output is derived evidence, not formal authorization.

## Compatibility and migration

The command is additive. Existing authoring, validation, provenance, installation, and upgrade behavior remains unchanged. Repositories that never invoke it receive no file or workflow change. The command supports canonical and valid legacy artifact paths without migrating unrelated artifacts.

The packaged candidate, CLI help, command reference, tests, and standard-runtime acceptance must agree. No installation profile, runtime dependency, automatic migration, or managed rewrite of repository-owned artifacts is introduced.

## Examples and counterexamples

**Intended plan:**

```text
harnessctl renumber-artifacts . --map WO-MOK-010=WO-MOK-011 --map VER-MOK-010=VER-MOK-011
```

The command reports every affected artifact, relation, path move, non-evidence reference requiring manual review, preserved evidence occurrence, and unsupported-content occurrence without writing.

**Intended apply:** the same command with `--apply` performs exactly the reviewed structured plan, validates it, leaves uncommitted changes for review, and prominently lists any manual reference changes still required.

**Prohibited:** automatically renumber every artifact reachable from a work order. Shared intent, requirements, specifications, or verification contracts may belong to unrelated work and must not be inferred into the mapping.

**Prohibited:** replacing old identifiers inside captured test output so the evidence appears to have been produced under the new identifier.

**Prohibited:** automatically replacing an old identifier in artifact prose, documentation, source comments, or tests. Those occurrences require human semantic review and are reported with locations.

**Prohibited:** renumbering a work order already named by a VREC, even when that VREC is only `ready`.

## Explicitly unspecified decisions

The implementation agent may choose internal module names, bounded capacity constants, temporary-file names, stable diagnostic codes, JSON field grouping, and concise human wording. It may not change the public command shape, infer mappings, make evidence content editable, support record renumbering, weaken the clean-worktree or rollback contract, scan other refs, add network behavior, or perform Git authority actions.
