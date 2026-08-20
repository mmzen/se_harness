+++
id = "ARCH-DST-012"
type = "architecture"
title = "Evidence-preserving repository renumbering transaction"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
addresses = ["REQ-DST-061"]
conforms_to = ["SPEC-DST-019"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "A new repository-mutating public command must choose the transaction and rollback boundary, distinguish editable references from immutable retained evidence, protect commit-bound provenance, and decide between explicit mapping and inferred graph migration. Those choices materially affect trust, consistency, recovery, and governance history."
assessed_by = "technical-owner"
+++

# Architecture: Evidence-preserving repository renumbering transaction

## Context and scope

Identifier collision recovery spans formal metadata, graph relations, prose and code references, filesystem paths, evidence namespaces, Git state, and historical assurance boundaries. Treating the operation as a collection of independent text replacements would permit partial writes and could falsify captured evidence or rewrite commit-bound facts.

This architecture defines one portable, local transaction for the mechanical portion of explicit pre-assurance recovery and a deterministic handoff for semantic hard-reference repair. It does not introduce distributed allocation, a reservation service, ref-aware prevention, or a second artifact authority.

## Components and responsibilities

- **CLI adapter:** parses `renumber-artifacts`, explicit mappings, mode, and JSON selection without choosing identifiers or authority.
- **Repository inventory:** proves the exact clean Git boundary, enumerates tracked paths and modes, and supplies the full original `HEAD` without executing repository content.
- **Artifact and provenance guard:** resolves selected formal artifacts, lifecycle eligibility, typed relations, and any VREC/RLS reference that makes renumbering ineligible.
- **Reference classifier:** separates parsed mutable identity/relation fields, non-evidence free-form references requiring manual review, unsupported binary or non-UTF-8 occurrences, and byte-immutable content under exact evidence paths.
- **Mapping planner:** validates one-to-one type-preserving maps and produces the complete deterministic structured-field and path plan plus the manual-reference inventory.
- **Safe transaction engine:** stages recovery data, performs exclusive replacements and two-phase moves, preserves bytes and modes, and rolls back on failure.
- **Postcondition assessor:** verifies new graph identity, absence of old identifiers in parsed identity and relation fields, complete classification of remaining occurrences, evidence hashes, planned Git changes, and formal validation.
- **Renderers:** expose bounded human and JSON plan/apply results as derived evidence with no authority claim.

## Dependency direction

```text
explicit caller mapping -----> CLI adapter
Git tracked inventory -------> repository inventory --------+
installed artifact graph ----> artifact/provenance guard ----+--> mapping planner
tracked bytes and paths -----> reference classifier ---------+
                                                               |
                                                               v
                                                     immutable complete plan
                                                               |
                                               +---------------+---------------+
                                               |                               |
                                               v                               v
                                         plan renderer                transaction engine
                                                                               |
                                                                               v
                                                                  postcondition assessor
                                                                               |
                                                                               v
                                                                       apply renderer
```

Planning owns no write capability. The transaction engine consumes only a complete validated plan and cannot expand its scope during application. Postcondition assessment observes the result but does not authorize a commit or lifecycle transition.

## Data and control flow

1. Resolve and attest the installed repository and clean Git boundary.
2. Normalize and validate all explicit mappings.
3. Parse the current formal graph and provenance records.
4. Classify tracked paths, text, evidence, modes, links, and destinations.
5. Freeze the sorted plan with source hashes, `HEAD`, status, and expected postconditions.
6. Return the plan, or re-attest it immediately before `--apply`.
7. Stage private same-filesystem recovery material and replacements.
8. Perform collision-safe path moves and exclusive structured-field replacements.
9. Validate the graph and every byte/path postcondition.
10. Remove recovery material and return success, or restore and prove the original inventory before returning failure.

## Trust boundaries

- Mappings, repository files, artifact metadata, relation targets, evidence, Git output, path casing, encodings, file modes, links, and concurrent filesystem activity are untrusted.
- The released evaluator and its packaged artifact parser and validator are the executable boundary; target code, hooks, filters, attributes, and scripts are never imported or run.
- Evidence path location classifies preservation behavior but does not make evidence formal authority.
- VREC/RLS metadata is historical governance input. The command may inspect it only to block rewriting and may not reinterpret or transition it.
- Human or JSON output is derived evidence and must not be confused with approval, verification, release, or identifier reservation.

## Required patterns

- One explicit normalized mapping model shared by validation, planning, application, output, and tests.
- One immutable plan built before mutation and re-attested before apply.
- Git-tracked inventory rather than recursive traversal of arbitrary generated or external content.
- Parsed identity and typed-relation replacement with byte preservation outside the selected fields.
- Deterministic reporting of free-form hard references with path and line where available, without semantic auto-editing.
- Path-aware immutable evidence-content classification.
- Exclusive destinations, same-filesystem recovery state, deterministic two-phase moves, and verified rollback.
- Formal validation plus independent byte/path postconditions before success.
- Stable bounded diagnostics and deterministic human/JSON ordering.

## Prohibited patterns

- Regex-only repository-wide replacement without parsed artifact and provenance checks.
- Automatic graph traversal that selects related artifacts on the caller's behalf.
- Editing evidence contents, VREC/RLS records, candidate commits, snapshots, or release facts.
- Best-effort continuation after a failed write or move.
- Overwriting destinations, following links, normalizing line endings, automatically changing free-form references, or silently omitting them from the manual-action report.
- Fetching refs, contacting a coordinator, reserving identifiers, running repository code, or invoking Git authority actions.
- Reporting success before graph validation and postcondition checks complete.

## Quality attributes

- **Safety:** unsafe paths, ambiguous mappings, provenance involvement, and incomplete recovery fail closed.
- **Consistency:** one transaction covers every explicitly mapped identity, parsed typed relation, and affected tracked path; every remaining occurrence is classified for manual review, evidence preservation, or unsupported-content inspection.
- **Auditability:** plans and results expose exact paths, mappings, hashes, manual references, preserved evidence, unsupported references, and original `HEAD`.
- **Determinism:** mapping order, filesystem enumeration order, and platform path presentation do not change semantic output.
- **Portability:** Python 3.11+ standard library and Git behavior are supported on Windows, Linux, and macOS.
- **Compatibility:** repositories not invoking the command and valid legacy artifact layouts retain current behavior.
- **Boundedness:** files, bytes, mappings, diagnostics, and recovery data use declared conservative limits.

## Conformance checks

Apply `VER-DST-019`, including exact mapping cases, parsed relation repair, deterministic manual-reference reporting, non-editing of free-form content, evidence-byte immutability, lifecycle and provenance blockers, hostile repository inputs, deterministic plans, failure injection at every mutation phase, verified rollback, canonical/legacy path handling, dual-runtime tests, package/CLI/documentation parity, and the complete regression suite.

## Related ADRs

`ADR-DST-012` proposes explicit mappings and a transactionally applied structured-identity/path plan, with manual hard-reference reporting and immutable evidence contents, instead of inferred-chain migration, entirely manual recovery, or prevention infrastructure.
