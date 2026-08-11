+++
id = "REQ-DST-009"
type = "requirement"
title = "Present the released PyPI package as the primary installation path"
status = "implemented"
owners = ["product-owner", "documentation-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a prospective user reads the public project entry point, THE SYSTEM SHALL present installation of the released se-harness package from PyPI as the primary path and SHALL distinguish source-checkout installation as a development path."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Present the released PyPI package as the primary installation path

## Rationale

The current README begins with installation from a repository checkout even though a verified production package is now available from PyPI. That makes normal adoption appear to require cloning and building the distribution repository.

## Required response

- State the Python 3.11-or-later prerequisite before installation commands.
- Use `python -m pip install se-harness` as the primary installation command.
- Provide an exact-version example whose version matches the repository package version.
- Link the canonical PyPI project and GitHub release pages.
- Move local and editable source installation to distribution-development guidance.
- Lead from installation into `init`, `adopt`, `doctor`, and `dashboard` without requiring knowledge of the artifact model.

## Failure and boundary behavior

Documentation must not imply that an unreleased checkout, editable installation, latest branch, or locally rebuilt wheel is an independently released distribution. It must not promise that every package-index version is suitable without explicit user selection.

## Constraints

The README is public guidance and package description, not product authority, release authorization, or evidence that an external service is available.

## Acceptance examples

An ordinary user can create a virtual environment, install `se-harness` from PyPI, confirm the CLI version, and initialize or adopt a repository without cloning this repository.

## Open decisions

None when approved.
