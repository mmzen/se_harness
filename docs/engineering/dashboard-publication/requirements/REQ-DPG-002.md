+++
id = "REQ-DPG-002"
type = "requirement"
title = "Preserve a safe non-authoritative public demonstration"
status = "implemented"
owners = ["product-owner", "security-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a release dashboard is published publicly, THE SYSTEM SHALL preserve canonical Explorer semantics, identify the site as a derived SE Harness development demonstration, and deploy only the bounded generated static payload."
verification_method = "automated-content-boundary-and-manual-semantic-review"

[relations]
derives_from = ["CAP-DPG-001"]
+++

# Requirement: Preserve a safe non-authoritative public demonstration

## Rationale

A public site is useful for promotion only if it is truthful about what it proves. The Explorer must demonstrate the actual SE Harness development graph without becoming an approval surface, a consumer service, or an alternate data model. Public repository content is still untrusted input to HTML rendering.

## Preconditions and trigger

The exact governance checkout passes validation and canonical dashboard generation. The repository is the public `mmzen/se_harness` development repository.

## Required response

- Reuse `harness-dashboard-snapshot-v1` and the existing safe rendering, CSP, bounded traversal, accessibility, and fallback obligations in `SPEC-DST-008`.
- Present the site as a demonstration of SE Harness governing its own development and label its data as derived and non-authoritative.
- Deploy only `index.html`, `dashboard-data.json`, `generation-summary.json`, and the deterministic `publication-manifest.json` produced for the Pages payload.
- Publish no secrets, credentials, workflow tokens, arbitrary workspace files, build distributions, retained evidence file bodies, or private external data.
- Preserve the exact `3d-force-graph` CDN exception and fallback accepted by `ADR-DST-008`; publication grants no broader network permission.

## Failure and boundary behavior

Unexpected files, unsafe links, malformed output, unsupported schemas, validation errors, or content that would imply approval or release authority must block the new deployment. The previous successful site may remain available.

## Constraints

The feature must not alter the managed standard repository template, init/adopt/upgrade behavior, `.engineering-harness.toml` schema, or consumer CI workflow.

## Acceptance examples

### Example: public visitor

**Given** a visitor opens the Pages site

**When** the visitor explores Overview, Lineage, or Readiness

**Then** the actual released repository graph is inspectable and the page does not offer or imply an authoritative transition.

### Example: unexpected payload file

**Given** the staging directory contains a credential file or an unrecognized artifact

**When** publication validates the upload manifest

**Then** deployment fails before upload.

## Open decisions

None.
