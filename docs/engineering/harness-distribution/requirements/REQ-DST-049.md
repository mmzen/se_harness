+++
id = "REQ-DST-049"
type = "requirement"
title = "Generate a deterministic integrity-addressed dashboard bundle"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN dashboard generation completes successfully, THE SYSTEM SHALL emit one deterministic versioned manifest that identifies the exact bounded resource set, byte size, media role, and SHA-256 of every progressively loadable data resource."
verification_method = "automated-test-and-security-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Generate a deterministic integrity-addressed dashboard bundle

## Rationale

Moving data out of `index.html` creates more trust-bearing files. Static sharding is acceptable only if generation, publication, and browser consumption can prove which files belong to one observed repository revision and reject substitution, omission, addition, collision, and partial output.

## Preconditions and trigger

The generator has parsed and validated one repository checkout and has built the canonical in-memory dashboard projection.

## Required response

- Emit a versioned manifest with the observed revision and deterministic descriptors for summary, topology, readiness, artifact-detail, and retained-content resources.
- Construct generated data paths from controlled constants or computed lowercase SHA-256 values, never from untrusted repository paths.
- Serialize and order resources deterministically so identical repository state produces byte-identical output.
- Bind the small HTML bootstrap to the expected manifest digest without creating a cyclic self-hash.
- Promote the complete bundle transactionally only after the exact recursive file set and every declared digest have been verified.

## Failure and boundary behavior

Unknown schema versions, unsafe paths, duplicate paths, conflicting content, digest mismatch, missing or additional data files, capacity failure, or incomplete promotion fail generation or publication closed and preserve the prior valid output.

## Constraints

- SHA-256 is the content-integrity algorithm.
- Generation time stays outside canonical deterministic data.
- Manifest integrity is distinct from formal artifact authority and is never an assurance score.

## Acceptance examples

### Example: repeatable bundle

**Given** the same validated checkout is generated twice,

**When** both recursive bundles are compared,

**Then** their paths, bytes, manifest, and digests are identical.

### Example: undeclared file

**Given** an additional JSON file appears in a candidate publication bundle,

**When** publication validation runs,

**Then** it rejects the bundle without publishing a partial site.

## Open decisions

None when approved.
