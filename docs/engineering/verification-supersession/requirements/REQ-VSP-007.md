+++
id = "REQ-VSP-007"
type = "requirement"
title = "Preserve compatibility and standard distribution"
status = "implemented"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN verification supersession support is distributed, THE SYSTEM SHALL preserve existing records, the single standard installation, safe upgrades, deterministic validation, and separate verification and release authority."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Preserve compatibility and standard distribution

## Rationale

The lifecycle extension must not break installed repositories or broaden automation authority.

## Preconditions and trigger

A repository without supersession relations is validated, installed, adopted, upgraded, packaged, or inspected.

## Required response

Keep existing ready, verified, and released VRECs valid. Update source and canonical validator, dashboard, Explorer, workflow, artifact template, lock metadata, tests, and wheel contents consistently. Preserve customized target files and one standard installation.

## Failure and boundary behavior

Unsupported or malformed supersession fails closed without target mutation. Upgrade preserves customized managed content for manual review.

## Constraints

Python 3.11 or later and the standard library remain the runtime contract. No new profile, network service, automatic status change, commit, tag, or publication is introduced.

## Acceptance examples

A fresh installation understands supersession; an older unmodified installation upgrades safely; a customized installation is preserved; existing VRECs without `superseded_by` still validate.

## Open decisions

None when approved.
