+++
id = "REQ-DST-015"
type = "requirement"
title = "Organize each engineering domain with one canonical artifact layout"
status = "implemented"
owners = ["product-owner", "technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN engineering artifacts are authored for a product domain, THE SYSTEM SHALL prescribe one canonical domain-and-type directory layout while retaining stable artifact metadata and typed relations as the only governance authority."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Organize each engineering domain with one canonical artifact layout

## Rationale

The harness currently validates artifacts recursively, so a repository can place every artifact directly below a business-domain directory and still obtain a valid graph. That compatibility is valuable, but the absence of a canonical authoring convention makes repositories harder to navigate, compare, review, and explain.

## Required response

- Define one canonical directory for every formal artifact type below `docs/engineering/<domain>/`.
- Keep supporting work-order evidence, Gherkin acceptance scenarios, and the domain index in predictable domain-local locations.
- Publish the mapping in installed guidance and make all harness-generated paths use it.
- Treat the path as an organization, generation, and diagnostic convention only.
- Continue to identify artifacts by their declared `id` and `type` and to establish authority through typed relations and lifecycle state.

## Failure and boundary behavior

A valid artifact in a noncanonical path must not become invalid solely because of its path. Path position must not imply approval, change an artifact type, create a relation, or repair missing metadata.

The domain component is untrusted input. It must be a lowercase ASCII kebab-case slug, must remain within `docs/engineering/`, and must not collide with reserved repository-wide or implementation directories.

## Constraints

- Preserve valid repositories produced by SE Harness 0.2.1 and earlier supported installations.
- Preserve repository-wide locations for aggregate verification and release records that intentionally span domains.
- Do not infer business domains from arbitrary path text when the result is ambiguous.
- Do not require empty directories to be committed to Git.

## Acceptance examples

For a domain named `simulation`, a requirement is authored at `docs/engineering/simulation/requirements/REQ-MOK-012.md`, an ADR at `docs/engineering/simulation/architecture/adr/ADR-MOK-001.md`, and a verification record for work wholly inside that domain at `docs/engineering/simulation/verification-records/VREC-MOK-001.md`.

An older valid requirement at `docs/engineering/simulation/REQ-MOK-001.md` still participates in the graph. Diagnostics may explain its canonical destination, but validation does not reject it.

## Open decisions

The accompanying specification proposes the exact type-to-directory mapping and reserved names. Accountable owners must approve those conventions before implementation.
