+++
id = "CAP-DPG-001"
type = "capability"
title = "Publish a release-bound Explorer demonstration"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
derives_from = ["INT-DPG-001"]
+++

# Capability: Publish a release-bound Explorer demonstration

## Actor and need

An SE Harness maintainer needs to make the project's own governed development graph easy to inspect after a release, while a visitor needs an understandable demonstration that does not imply formal authority.

## Capability statement

`An SE Harness maintainer can publish or replay a static GitHub Pages Explorer for a completed SE Harness release from an immutable, validated governance snapshot.`

## Boundaries

- The capability applies only to this repository's public demonstration site.
- It does not add Pages files or settings to the standard consumer template.
- It does not change `harnessctl dashboard`, the canonical snapshot schema, formal lifecycle rules, release eligibility, or self-hosting governor selection.
- It publishes a complete generated output directory, not repository source files or retained evidence bodies outside the existing Explorer contract.
- GitHub Pages availability and the optional 3D CDN are external dependencies; non-3D evidence remains usable under the existing Explorer contract.

## Outcomes

- A visitor can explore the latest selected released governance state.
- The page identifies the release, candidate commit, and observed governance revision.
- A maintainer can reproduce a deployment from explicit immutable inputs.
- Invalid or ambiguous provenance cannot silently replace the public demo.

## Candidate requirements

- Bind every deployment to one completed SE Harness release and immutable governance snapshot.
- Preserve canonical Explorer semantics and a safe public-data boundary.
- Make publication least-privilege, observable, replayable, and non-mutating.
