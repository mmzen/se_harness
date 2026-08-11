+++
id = "REQ-DST-018"
type = "requirement"
title = "Preserve valid legacy artifact layouts"
status = "implemented"
owners = ["product-owner", "technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an installed repository contains valid artifacts outside the canonical type directories, THE SYSTEM SHALL preserve their validity, report deterministic advisory guidance, and SHALL NOT move or rewrite repository-owned artifacts during upgrade."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve valid legacy artifact layouts

## Rationale

Existing repositories may already contain approved and actively edited artifacts in a flat domain layout. Making the new convention immediately mandatory or moving those files automatically would create noisy diffs, conflict with concurrent work, and confuse an organizational convention with graph authority.

## Required response

- Continue recursively discovering supported artifacts independently of canonical placement.
- Emit a stable, nonblocking diagnostic when a formal artifact has a safe, unambiguous canonical location different from its current path.
- Report the expected canonical path so owners can plan an explicit repository change.
- Keep graph validation, typed relations, lifecycle checks, Explorer answers, and command selection based on artifact metadata.
- Permit intentional repository-wide aggregate verification and release records.
- Keep upgrade operations bounded to their existing managed-file ownership rules and never relocate repository-owned artifacts.

## Failure and boundary behavior

The advisory must not change the validator exit status, manufacture a relation, modify a file, or claim that migration is safe while another actor may be editing the repository. Invalid metadata or relations remain errors for their own reasons regardless of path.

If a domain or canonical destination cannot be determined safely and unambiguously, omit the path advisory rather than guessing.

## Constraints

- A layout migration is a separately authorized owner change, normally performed with reviewable `git mv` operations after concurrent work is quiescent.
- Fresh-install guidance may describe the canonical layout, but upgrades must preserve existing repository-owned guidance and domain indexes under the current ownership model.
- Tests must use temporary fixtures representative of legacy installations, never modify a live consumer repository.

## Acceptance examples

A valid `docs/engineering/simulation/REQ-MOK-001.md` remains part of the graph and validation succeeds while diagnostics suggest `docs/engineering/simulation/requirements/REQ-MOK-001.md`. Running `harnessctl upgrade` leaves the file at its existing path and retains its bytes.

## Open decisions

The diagnostic code and wording are implementation details provided they are deterministic, actionable, nonblocking, and covered by the verification contract.
