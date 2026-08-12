+++
id = "REQ-DST-027"
type = "requirement"
title = "Safe installation and upgrade discoverability"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a reader installs or updates SE Harness, THE SYSTEM SHALL distinguish Python-package installation from repository-managed-content upgrade and require explicit owner-controlled application of repository changes."
verification_method = "automated-documentation-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Safe installation and upgrade discoverability

## Rationale

Putting the entire safe-upgrade procedure into Quick Start overloads first use, but omitting it can make users assume that `pip install --upgrade` also updates an adopted repository. It does not.

## Preconditions and trigger

A reader is either installing the package for first use or already owns a repository initialized by an older released harness.

## Required response

The README uses one compact `Install or upgrade` area that separates:

1. fresh package installation and repository initialization/adoption; and
2. an existing-installation notice stating that package upgrade and repository upgrade are separate, with a link to the detailed safe procedure.

The detailed note explains that repository upgrade first produces a read-only plan and that `--apply` is a distinct, explicitly owner-authorized transactional mutation followed by `doctor`.

## Failure and boundary behavior

Documentation must not imply automatic migration, silent overwrite of repository customization, or equivalence between a newer virtual-environment package and updated repository-managed files.

## Constraints

- Keep released PyPI installation primary.
- Preserve exact-version installation and Python 3.11-or-later requirements.
- Keep platform-specific activation and launcher paths out of the root information budget unless essential to a working minimal example.

## Acceptance examples

### Example: fresh installation

**Given** a new user,

**When** they follow the root installation block,

**Then** they can create a virtual environment, install the released package, and choose `init` or `adopt`.

### Example: existing installation

**Given** a repository already contains the harness,

**When** its owner reads the upgrade notice,

**Then** they do not assume that updating the wheel mutated the repository and can reach the planned/apply procedure.

## Open decisions

The root may show a single platform-neutral command block and route platform-specific activation differences to the note.
