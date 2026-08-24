+++
id = "REQ-RLO-013"
type = "requirement"
title = "Bind the complete release build recipe"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN the se_harness repository binds accepted Python distributions to a new ready release record, THE SYSTEM SHALL bind one complete machine-readable build recipe covering the exact producer platform, Python runtime, complete build toolchain, controlled environment, epoch derivation, normalization behavior, commands, and output contract."
verification_method = "automated-schema-binding-and-failure-test"

[relations]
derives_from = ["CAP-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "release-owner"
+++

# Requirement: Bind the complete release build recipe

## Rationale

The current release record binds the candidate epoch, source tree, filenames, and output hashes. The publication workflow separately hard-codes a runner label, Python patch, and three direct build packages. It does not bind the complete toolchain, the effective environment, or the commands that produced the accepted bytes. A later rebuild can therefore be internally repeatable yet still use a different producer and produce different bytes.

## Preconditions and trigger

A release work order has produced an exact candidate commit and accepted wheel and normalized-sdist bytes. Generic `harnessctl prepare-release` has produced an uncommitted `ready` RLS, and repository-owned binding is asked to attach the accepted distribution provenance.

## Required response

Bind a repository-relative recipe path, recipe schema, and lowercase SHA-256 of the exact recipe bytes in the repository-owned distribution table. The recipe must declare:

- one immutable producer identity: exact OCI image digest, `linux`, and `amd64`;
- the exact Python implementation and patch version;
- a hash-locked inventory covering every Python distribution in the build toolchain, including direct and transitive tools;
- a closed build environment containing fixed values and explicitly derived values, including `SOURCE_DATE_EPOCH` from the candidate commit;
- ordered commands as argument arrays with declared working directories and bounded placeholders;
- the sdist normalization implementation, parameters, and output rules; and
- the exact expected wheel, sdist, checksum, and build-evidence contract.

The recipe path must identify bytes in the candidate tree. The bundle manifest and ready RLS must agree on the candidate, version, source manifest, recipe identity, epoch, filenames, and output hashes.

## Failure and boundary behavior

Reject a missing, partial, duplicate-key, oversized, non-canonical, unsafe-path, mutable-image, wrong-platform, incomplete-toolchain, open-environment, free-form-shell, wrong-epoch, wrong-normalizer, or hash-mismatched recipe. Reject a bundle whose recipe differs from the candidate tree or ready RLS. Binding failure must leave the release record byte-for-byte unchanged.

Historical released schema-1 distribution records remain valid and replayable through their existing legacy path. A newly prepared `ready` distribution record must use the recipe-bearing schema and may not claim schema-1 compatibility.

## Constraints

- The recipe and its interpreter are repository-owned release policy. They must not enter portable `harnessctl`, the packaged `se_harness` namespace, or standard consumer templates.
- A recipe declares build mechanics and evidence; it grants no work, assurance, release, publication, deployment, or external-action authority.
- The recipe contains no credential, secret, host path, floating image tag, unbounded command, or operator-supplied expected hash.
- Updating the recipe, toolchain lock, or producer identity is an ordinary reviewed candidate change and creates a new recipe digest.

## Acceptance examples

### Example: normal behavior

**Given** a candidate-tree recipe naming one digest-pinned Linux/amd64 image, exact CPython, complete hash-locked tool inventory, controlled environment, build and normalization argument arrays, and exact output rules

**When** repository binding validates a matching accepted bundle manifest

**Then** the ready RLS receives the recipe schema, safe path, and exact SHA-256 together with schema-2 distribution identity, without changing its lifecycle state.

### Example: failure behavior

A recipe that names `ubuntu-latest`, `python:3.11`, `setuptools>=68`, inherits the host environment, omits a transitive tool, or uses a shell string is refused without modifying the ready RLS.

## Open decisions

None. The architecture and ADR select a candidate-tree declarative recipe, immutable OCI producer, complete hash-locked toolchain, closed environment, and strict repository-owned interpreter.
