+++
id = "SPEC-EVK-001"
type = "specification"
title = "Portable work-order evidence attribution"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
specifies = ["REQ-EVK-001", "REQ-EVK-002", "REQ-EVK-003", "REQ-EVK-004"]
+++

# Specification: Portable work-order evidence attribution

## Scope

Define one backward-compatible structural contract for attributing normalized retained-evidence paths to work-order IDs. Apply the contract to aggregate `capture-verification`, verification-record validation, derived inspection findings, and Harness Explorer evidence/readiness projection.

This specification resolves directory-position attribution before any separately governed extension of keyed-evidence enforcement to single-work-order VRECs. It does not authorize that enforcement itself.

## Actors and external systems

Repository engineers supply evidence paths and layouts. Quality owners assess evidence and verification records. The installed package prepares records. Managed repository-local scripts validate and project repository state. The filesystem supplies untrusted path and file observations. No external service is required.

## Inputs

- Normalized repository-relative evidence path strings supplied to `capture-verification` or retained in `evidence_paths`.
- Repository-relative paths derived by evidence discovery below `docs/engineering`.
- Explicit selected work-order IDs for capture and validation.
- Existing path-safety and repository policy results.

Paths containing backslashes, absolute roots, empty or dot traversal components, unsafe resolution, disallowed links, or missing/nonregular targets remain governed by existing checks and do not become safe through key attribution.

## Outputs

The pure attribution result is a lexically ordered duplicate-free set of exact work-order IDs. Consumers use it as follows:

- capture and validation test whether each selected work-order ID occurs in at least one safe evidence path's key set;
- discovery maps each eligible evidence path to every extracted key;
- inspection and Explorer consume the same repository-local mapping for `W-HEX-001`, readiness, and evidence projection.

No new formal metadata field, snapshot field, lifecycle state, or authority claim is emitted.

## State model

Attribution is stateless and read-only:

1. Normalize or derive a repository-relative path through the existing caller boundary.
2. Complete existing safety checks appropriate to that caller.
3. Select candidate path components under the rules below.
4. Extract, deduplicate, and sort exact work-order keys.
5. Apply the resulting associations without mutating source files, records, Git, or lifecycle state.

## Behavioral rules

1. Metadata-path parsing uses forward-slash repository-relative semantics independent of host path separator. Filesystem discovery converts a safely contained path to repository-relative POSIX form before attribution.
2. The filename is always a candidate component. This preserves current behavior for paths both inside and outside an `evidence` directory.
3. If the path contains a component equal to lowercase `evidence`, every component after its first occurrence, including the filename, is a candidate component. Components before `evidence` do not create directory-based attribution.
4. A candidate component contributes a key only when it starts with a syntactically valid work-order ID and the next character is `-`, `.`, or the end of the component. Matching is ASCII case-sensitive.
5. A valid extracted ID uses the `WO-` prefix and the existing formal ID shape ending in a three-digit suffix. A longer numeric suffix, embedded prefix, wrong case, or unsupported boundary does not match.
6. Repeated occurrences of one key produce one association. Distinct exact keys produce distinct associations in lexical order. One explicit path may therefore support multiple work orders without nondeterministic component precedence.
7. `capture-verification` first retains all existing normalization, containment, existence, type, symlink, destination, artifact, lifecycle, clean-worktree, and atomic-output checks. For aggregate selection, every selected work order must occur in at least one normalized evidence path's key set.
8. Formal validation applies the same extraction contract to `evidence_paths` after its existing metadata and safe-path checks. Current aggregate coverage remains blocking on the governance plane.
9. Repository-local discovery remains bounded to regular files below `docs/engineering` whose path contains a literal `evidence` component. It does not discover similarly named files elsewhere merely because their filename contains a work-order ID.
10. Discovery associates one eligible file with every unique key extracted from its repository-relative path and emits work-order maps and path lists in stable lexical order.
11. Inspection and Explorer do not reimplement path matching. They consume the repository-local extraction or discovery result. An implemented work order with at least one directory-keyed evidence path no longer receives `W-HEX-001`; genuinely unkeyed work retains the finding.
12. The installed-package and repository-local implementations remain separate execution planes. They execute an identical contract-case matrix; parity disagreement is a verification failure.
13. Root managed scripts and `templates/repository/standard/scripts` remain byte-identical after the authorized change. Standard upgrade preserves customized files and makes no repository-owned evidence move.
14. `harness-dashboard-snapshot-v1` remains unchanged because its representation does not change. Increment the finding-rules identity because `W-HEX-001` behavior intentionally changes for directory-keyed layouts.
15. No command or derived view judges evidence content, transitions a record, approves verification, or authorizes release.

## Error and recovery behavior

- An unkeyed aggregate path set identifies every uncovered work-order ID and produces no partial verification record.
- An authored aggregate VREC missing a selected work-order key receives the existing blocking governance diagnostic.
- Unsupported component shapes contribute no key; callers continue with their existing uncovered/finding behavior.
- Unsafe filesystem paths retain their existing, more specific failures regardless of a matching component.
- Contract disagreement, root/template divergence, platform-dependent output, or required formal-definition conflict stops implementation for accountable resolution.

Recovery corrects the draft definition, explicit input, implementation, or managed installation. It never renames historical evidence automatically.

## Data and interface contracts

The conceptual interface is:

```text
evidence_work_order_keys(normalized_repository_path) -> sorted unique work-order IDs
evidence_is_keyed_to(normalized_repository_path, work_order_id) -> membership result
```

Exact helper names and container types are delegated. The observable key grammar, component selection, ordering, and call-site results are not delegated.

Repository-local validation owns the portable predicate used by validator, inspection, and Explorer. The package owns an independent implementation used by provenance preparation. Test fixtures, not a runtime import across the boundary, establish parity.

## Security and privacy properties

- Attribution never makes an unsafe path safe and never reads evidence content.
- Only exact case-sensitive component-prefix matches with accepted boundaries contribute keys.
- Ancestors before `evidence`, repository names, and branch or commit text cannot create directory-based attribution.
- Repository-local scripts do not import or execute target checkout package code.
- No path, key, record body, or evidence content is sent to a network service.

## Performance and capacity

Key extraction is linear in the number and length of path components. Discovery remains linear in eligible engineering files plus path length. No recursion beyond existing bounded filesystem discovery, network access, or unbounded subprocess is introduced.

## Observability

Capture and validator diagnostics continue to identify uncovered work-order IDs. Inspection and Explorer expose exact evidence paths and affected work orders. Finding-rules identity makes the changed derived behavior visible without changing formal authority or inventing a health score.

## Compatibility and migration

- Every path accepted by the current filename convention remains accepted.
- Directory-per-work-order paths become additionally accepted.
- Historical evidence, VREC/RLS metadata, candidate commits, and released records remain unchanged.
- Existing consumer customizations remain owner-controlled during upgrade.
- Issue 49 remains separate and may later apply this already-settled predicate to single-work-order VRECs through its own approved work.
- Current active references to a “filename convention” in aggregate and Explorer definitions are reconciled within the authorized work order before implementation completion.

## Examples and counterexamples

| Path | Extracted keys |
|---|---|
| `docs/engineering/x/evidence/WO-ABC-001-check.md` | `WO-ABC-001` |
| `docs/engineering/x/evidence/WO-ABC-001/check.md` | `WO-ABC-001` |
| `docs/engineering/x/evidence/archive/WO-ABC-001/check.md` | `WO-ABC-001` |
| `docs/engineering/x/evidence/WO-ABC-001/WO-ABC-001-check.md` | `WO-ABC-001` |
| `docs/engineering/x/evidence/WO-ABC-001/WO-XYZ-002-check.md` | `WO-ABC-001`, `WO-XYZ-002` |
| `docs/engineering/WO-ABC-001/evidence/check.md` | none |
| `docs/engineering/x/evidence/X-WO-ABC-001/check.md` | none |
| `docs/engineering/x/evidence/WO-ABC-0010/check.md` | none |
| `reports/WO-ABC-001.md` | `WO-ABC-001` |

## Explicitly unspecified decisions

Local helper names, placement within the existing validator/provenance modules, exact internal regex construction, test class names, and diagnostic line wrapping are delegated. Implementations may not alter the selected components, key grammar, multi-key behavior, ordering, execution-plane boundary, or compatibility semantics.
