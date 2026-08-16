+++
id = "REL-VSP-001"
type = "release_contract"
title = "Release verification-supersession support"
status = "rejected"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
gates = ["WO-VSP-001"]
+++

# Release Contract: Release verification-supersession support

## Release unit

The versioned `se-harness` wheel, source tag, canonical standard template, validator, dashboard, Explorer, and lifecycle documentation implementing VREC supersession.

## Required evidence

Complete `VER-VSP-001` evidence; valid artifact graph; passing full tests, CLI help, doctor, dashboard, init/adopt/upgrade, wheel inspection, and fresh-install verification; source/canonical parity; and a verified aggregate candidate record for the exact release commit.

## Compatibility and migration

Existing VRECs remain valid and unchanged. No automatic lifecycle migration occurs. Customized installed files are preserved. The known stale record is transitioned only through later separate governance after compatible support is present.

## Security and provenance

Typed targets, lifecycle, work coverage, cycles, active release references, exact candidate metadata, authority evidence, and immutable-field review must pass. Derived findings do not authorize transitions.

## Promotion policy

Promotion requires zero blocking validation errors, complete deterministic verification, retained evidence, a reproducible wheel and checksum, fresh-environment smoke success, and explicit release-owner authorization.

## Human approval triggers

Quality owners approve implementation verification. Release owners approve version, payload, tag, and publication. Assurance owners separately approve each concrete VREC supersession. Any exception to source state, successor eligibility, or active-release protection requires a new decision.

## Rollback criteria and procedure

Do not publish if existing records regress, invalid supersession passes, release exclusion fails, dashboard authority is ambiguous, installation changes overwrite customization, or source and wheel differ. If published, preserve affected records, withdraw or mark the version affected where possible, and ship a separately verified correction without moving an existing tag.

## Post-release observation window

Observe the first real governance supersession, validation, dashboard rendering, upgrade, and subsequent release preparation before broad lifecycle extension.

## Disposition

This per-feature proposal was never selected as release authority. `WO-VSP-001` was released in `0.2.0` under aggregate contract `REL-DST-001` and released record `RLS-SEH-001` at tag `v0.2.0`. The rejected status disposes of this unused proposal; it does not reject the released implementation.
