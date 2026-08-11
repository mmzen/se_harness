+++
id = "REQ-DST-011"
type = "requirement"
title = "Distinguish CLI distribution upgrades from repository upgrades"
status = "implemented"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a user updates se-harness, THE SYSTEM SHALL distinguish updating the installed Python distribution from planning and applying managed-file changes in a harness-enabled repository."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Distinguish CLI distribution upgrades from repository upgrades

## Rationale

Updating the installed package changes the CLI and canonical templates available to the environment, but intentionally does not rewrite repositories. Conflating the two steps obscures safe planning, ownership checks, and explicit mutation.

## Required response

Document this ordered sequence:

1. update the environment with `python -m pip install --upgrade se-harness`;
2. inspect a repository-specific plan with `harnessctl upgrade TARGET`;
3. explicitly apply a safe transactional plan with `harnessctl upgrade TARGET --apply`;
4. confirm the result with `harnessctl doctor TARGET`.

State that the package update alone never modifies an initialized or adopted repository and that `upgrade --apply` remains subject to customization and conflict checks.

## Failure and boundary behavior

Do not describe package installation as an automatic repository migration. Preserve the existing fail-closed and no-partial-write behavior for customized or ambiguous managed content.

## Constraints

No background updater, automatic mutation, alternate upgrade profile, or external service is introduced.

## Acceptance examples

A user can update the CLI while leaving a target repository byte-for-byte unchanged, inspect the target plan separately, and decide whether to apply it.

## Open decisions

None when approved.
