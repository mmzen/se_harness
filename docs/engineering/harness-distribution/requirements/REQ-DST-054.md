+++
id = "REQ-DST-054"
type = "requirement"
title = "Preserve portable static hosting and publication authority"
status = "approved"
owners = ["product-owner", "release-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a progressive Explorer bundle is generated or selected for publication, THE SYSTEM SHALL remain a self-contained static HTTP site whose exact declared resources are validated before publication and whose generation alone performs no transmission or deployment."
verification_method = "automated-publication-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve portable static hosting and publication authority

## Rationale

Progressive fetches must work on GitHub Pages and ordinary static HTTP hosting without converting Explorer into an application service or weakening the explicit demonstrator publication action. Local generation must remain nonpublishing.

## Preconditions and trigger

The dashboard generator writes an output bundle, or the repository-specific Pages action selects a generated bundle associated with an authorized governance snapshot.

## Required response

- Use only origin-relative immutable bundle resources; require no server computation, database, authentication service, or source-repository endpoint.
- Make the supported HTTP-serving requirement explicit for local review and offer a documented standard-library serving command; a future convenience flag may wrap that behavior separately.
- Validate the manifest schema, observed revision, exact recursive file set, path containment, declared sizes, and SHA-256 before Pages packaging.
- Publish only manifest-declared resources and retain publication provenance and generation-summary bindings.
- Preserve the existing explicit action trigger and human publication authority boundary.

## Failure and boundary behavior

Direct `file://` opening receives a clear serving instruction rather than a misleading empty dashboard. Unsupported hosting, cross-origin substitution, redirect outside the generated origin, incomplete resources, or publication mismatch fails closed without an implicit fallback to GitHub repository content.

## Constraints

- The accepted exact `3d-force-graph@1.79.0` CDN URL remains the only existing runtime network exception and receives no repository data.
- Generation, viewing, verification, release, package publication, and Pages deployment remain separate actions.
- No service worker or persistent browser cache is required by this packet.

## Acceptance examples

### Example: static Pages site

**Given** an exact validated progressive bundle,

**When** the authorized Pages action packages it,

**Then** every declared relative resource is published and no undeclared repository file is included.

### Example: direct file opening

**Given** a reader opens `index.html` through `file://`,

**When** browser fetch policy prevents resource loading,

**Then** Explorer explains that the bundle must be served over HTTP and does not describe the repository as empty or invalid.

## Open decisions

None when approved.
