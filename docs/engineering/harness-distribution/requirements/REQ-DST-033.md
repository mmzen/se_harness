+++
id = "REQ-DST-033"
type = "requirement"
title = "Distribute one managed Explorer implementation"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"
statement = "WHEN the standard harness is used from source or installed into a repository, THE SYSTEM SHALL provide the same managed Explorer generator, template, assets, and integrity behavior."
verification_method = "automated-package-parity-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Distribute one managed Explorer implementation

## Rationale

The source checkout, canonical standard template, built package, and installed repository must not carry divergent dashboards. `harnessctl dashboard` already dispatches to the target repository's managed generator, so the integration must preserve that ownership boundary.

## Required response

Root candidate files and canonical standard-template copies must remain equivalent where the distribution contract requires parity. Package metadata and managed integrity must include every required local asset. Init, adopt, safe upgrade, doctor, direct generator execution, and `harnessctl dashboard` must agree on the installed file set and behavior.

The CLI must continue to invoke the managed target-local generator and preserve its exit code. No separate hosted service, installation profile, JavaScript build tool, or runtime package manager may be required.

## Failure and boundary behavior

Missing, customized, ambiguous, or integrity-mismatched managed files must follow existing transactional installation and upgrade rules. Integration must not overwrite repository-owned customizations or partially install an Explorer asset set.

## Acceptance examples

### Example: fresh installed repository

**Given** a wheel installs the standard harness into a temporary repository

**When** the repository passes doctor and runs `harnessctl dashboard`

**Then** the generated Explorer uses the same canonical snapshot and local interface as the source candidate.
