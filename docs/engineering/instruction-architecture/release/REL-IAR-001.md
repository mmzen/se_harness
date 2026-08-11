+++
id = "REL-IAR-001"
type = "release_contract"
title = "Release instruction architecture rationalization"
status = "draft"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
gates = ["WO-IAR-001"]
+++

# Release Contract: Release instruction architecture rationalization

## Entry criteria

- `WO-IAR-001` is implemented with complete retained evidence and no unresolved migration conflict.
- A separately captured and human-verified VREC binds the work order, `VER-IAR-001`, evidence, and one clean full candidate commit.
- Graph, full suite, CLI help, fresh install, adoption, upgrade, doctor, preflight, dashboard, package, and independent-CI checks pass.
- Canonical template, packaged content, and self-hosted operational copies have validated integrity and parity.
- Evidence distinguishes last-release independent baseline results from candidate verification and defines the separately governed post-publication pin update.
- Release notes call out the README ownership-mode transition, required CI pin, structured work-order declaration, and any manual host-protection steps.

## Compatibility constraints

Customized instruction and context files must remain preserved. An ambiguous upgrade must stop with an actionable report. Repositories are not silently enrolled in remote branch protection, and no additional installation profile is introduced.

## Authority boundary

This draft does not authorize a release record, tag, package build, publication, deployment, or host-governance change.
