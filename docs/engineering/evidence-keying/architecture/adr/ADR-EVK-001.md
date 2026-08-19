+++
id = "ADR-EVK-001"
type = "adr"
title = "Align independent evidence-keying planes by contract"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
decides = ["ARCH-EVK-001"]
+++

# ADR: Align independent evidence-keying planes by contract

## Status

Accepted.

## Context

Issue 72 exposes three filename-only assessments with disagreeing operational consequences: package record preparation can fail, formal validation can reject aggregate records, and Explorer/inspection can report missing evidence. A literal shared import could remove duplication, but the installed package and portable repository-local scripts intentionally occupy separate trust and availability boundaries. The validator must run with Python 3.11 standard library before a repository toolchain is available and must not execute target checkout package code.

## Decision drivers

- One observable definition of a keyed evidence path.
- Backward compatibility for flat evidence filenames.
- Support for one-directory-per-work-order layouts.
- No weakening of path safety or provenance.
- Standalone repository-local validation and self-hosting isolation.
- Deterministic cross-platform behavior.
- Prevention of future drift between capture, validation, inspection, and Explorer.

## Considered options

1. Retain filename-only behavior and document it more strongly. Rejected because established directory-keyed repositories cannot safely rename evidence already bound into commit-specific records.
2. Match a work-order-like component anywhere in the absolute path. Rejected because repository and ancestor names could create false attribution.
3. Put one helper in `se_harness` and import it from managed validator/dashboard scripts. Rejected because standalone validation would depend on installed or candidate package code and weaken the execution-plane boundary.
4. Keep all existing independent call-site regexes and add examples. Rejected because tests would not prevent semantic drift among preparation, governance validation, and derived views.
5. Use one portable predicate for validator/dashboard/inspection, retain one equivalent package predicate for provenance, and compare both through one contract-case matrix. Selected.

## Decision

Adopt option 5. Expand the convention to exact work-order keys in the existing filename position or in components at or below a literal lowercase `evidence` directory. Preserve current filename matching for paths without an `evidence` component. Extract every unique exact key deterministically.

The managed validator owns the portable repository-local predicate. The dashboard imports it through its existing validator dependency, and inspection consumes dashboard findings rather than matching paths. Package provenance retains an independent pure predicate and does not import target scripts. One shared test case table executes against both predicates and is the conformance boundary.

Existing path normalization, containment, file-type, symlink, clean-worktree, record, and authority checks remain independent and mandatory.

## Consequences

Directory-per-work-order layouts become compatible without historical rewrites, and the four harness surfaces can agree. Repository-local regex duplication is removed. Two small pure implementations remain because the assurance planes stay isolated; the parity suite becomes a required maintenance control.

The evidence mapping may associate one explicit path with several exact work-order keys. This is deterministic and visible, but assurance owners still judge whether the evidence is substantively adequate for each work order. Finding-rules identity changes because derived missing-evidence behavior changes for affected repositories.

Managed validator and dashboard files, their canonical template copies, lock hashes, tests, and active product definitions require coordinated change. Customized consumer files remain blocked for manual upgrade review.

## Validation

Verify exact component grammar, flat and directory layouts, multi-key paths, misleading ancestors, prefix collisions, stable ordering, aggregate capture and validation, W-HEX/readiness behavior, cross-plane case parity, Windows/POSIX semantics, unsafe-path preservation, managed parity, doctor, artifact validation, preflight, and the complete regression suite.
