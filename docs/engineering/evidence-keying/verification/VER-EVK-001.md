+++
id = "VER-EVK-001"
type = "verification"
title = "Verify portable evidence attribution"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
verifies = ["REQ-EVK-001", "REQ-EVK-002", "REQ-EVK-003", "REQ-EVK-004"]
+++

# Verification Contract: Verify portable evidence attribution

## Independence

Expected path grammar, component scope, compatibility behavior, dependency direction, and authority boundaries come from `REQ-EVK-001..004`, `SPEC-EVK-001`, `ARCH-EVK-001`, and `ADR-EVK-001`, not from implementation helper names or existing regexes. Temporary repositories and direct function contracts provide isolated observations. Quality and security owners assess evidence independently from the implementation agent.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-EVK-001` | pure contract cases and filesystem discovery fixtures | flat, directory, nested, duplicate, multi-key, misleading ancestor, wrong case, boundary collision | exact expected unique keys and associations are produced |
| `REQ-EVK-002` | CLI integration, authored-record validation, snapshot, and inspection tests | mixed-layout aggregate candidate, valid/invalid VREC, W-HEX and readiness output | capture, validator, inspection, and Explorer agree for every equivalent path |
| `REQ-EVK-003` | regression, security, upgrade, and historical-diff review | current flat fixtures, unsafe paths, customized managed files, existing VREC/RLS/evidence | old valid behavior remains; unsafe paths still fail; no historical fact changes; upgrade preserves ownership |
| `REQ-EVK-004` | parity, platform-semantic, static dependency, and self-hosting tests | one shared case table on package and portable predicates; Windows/POSIX path semantics | ordered results match; validator/dashboard remain standard-library-only and do not import target `se_harness` |

## Acceptance scenarios

The executable scenarios in `acceptance/evidence-keying.feature` are the minimum external behavior contract. Run them through focused unit/integration fixtures rather than accepting prose inspection alone.

## Property and invariant tests

- Reordering discovery or CLI inputs does not change extracted key sets, association maps, diagnostics, or serialized dashboard output.
- Adding irrelevant ancestors before `evidence` does not create or change a directory-derived key.
- Adding a repeated occurrence of the same exact key does not duplicate associations.
- Every key ends in the existing three-digit formal suffix and is followed in its component by `-`, `.`, or end.
- Flat filename results are identical before and after the change.
- Package and portable predicates return exactly the same ordered result for the shared case table.
- A path match never changes the result of independent normalization, containment, symlink, existence, or file-type checks.

## Static and architecture checks

- Confirm the dashboard imports the repository-local predicate through its existing validator dependency.
- Confirm inspection does not add a separate matcher.
- Confirm validator/dashboard scripts do not import `se_harness` or execute artifact/evidence bodies.
- Confirm provenance does not dynamically import target repository scripts.
- Confirm `ARCH-EVK-001` addresses the significant requirements, conforms to `SPEC-EVK-001`, records `adr_required`, and is decided by selected `ADR-EVK-001` before approval.
- Confirm active aggregate and Explorer definitions are reconciled from filename-only wording before the work order records implementation completion.

## Security and privacy checks

Exercise absolute paths, drive paths, backslashes, empty/dot/traversal components, repository escape, symlinks and junctions, directories, missing files, nonregular files, misleading absolute ancestors, embedded IDs, lowercase IDs, four-digit suffixes, and hostile-looking path text. Matching text must never bypass the existing safe-path result or cause content execution or network access.

## Performance and resilience checks

Exercise long normalized paths at supported filesystem bounds, many evidence files, repeated keys, and bounded multi-key paths. Assert linear completion, deterministic order, no network, no unbounded subprocess, and no partial record or dashboard output after failure.

## Manual assessments

- Review wording so “keyed” remains structural attribution rather than evidence sufficiency or verification.
- Review the issue-72 directory layout and confirm it clears only the false finding/failure.
- Review Explorer evidence and readiness presentation for the exact path and work-order association.
- Review the diff to confirm no historical evidence, VREC, RLS, release, or governor fact changed.

## Evidence retention

Retain the contract-case table and results, focused test output, aggregate capture/validator fixture results, W-HEX/readiness observations, security cases, managed parity and upgrade results, full regression count, artifact validation, doctor, preflight, and diff review in `docs/engineering/evidence-keying/evidence/WO-EVK-001-verification.md`.

## Residual uncertainty

Structural attribution cannot establish that one evidence document substantively supports every associated work order. Quality owners retain that decision. Issue 49 may later strengthen single-work-order enforcement, but only under its own approved definition and work authorization after this convention is settled.
