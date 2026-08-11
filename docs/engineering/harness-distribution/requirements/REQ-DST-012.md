+++
id = "REQ-DST-012"
type = "requirement"
title = "Expose complete public package metadata"
status = "implemented"
owners = ["product-owner", "release-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a se-harness distribution is built, THE SYSTEM SHALL identify the root README as its Markdown long description and SHALL expose the project license and canonical project, source, issue, and release URLs in package metadata."
verification_method = "automated-test-and-release-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Expose complete public package metadata

## Rationale

The current project metadata provides name, version, short description, Python requirement, dependencies, and console entry point, but it does not publish the root README, license file, or canonical project URLs as package metadata.

## Required response

- Declare `README.md` as the Markdown project readme in `pyproject.toml`.
- Identify the repository's GPL version 3 license through metadata compatible with the configured build backend and retain `LICENSE` in the source distribution.
- Declare canonical Homepage, Repository, Issues, and Releases URLs under `[project.urls]`.
- Preserve `requires-python = ">=3.11"`, the `harnessctl` entry point, and the empty runtime dependency set.
- Make the README valid as both a GitHub entry point and a package-index long description.

## Failure and boundary behavior

The existing PyPI 0.2.1 metadata is immutable. This change must not claim to update that release, mutate its files, or take effect on PyPI before a later separately verified version is published.

## Constraints

Do not add a runtime dependency, dynamic network-derived metadata, duplicated package-index-only README, credential, publisher change, or version bump under this requirement alone.

## Acceptance examples

Static metadata inspection identifies the README, license, and four canonical URLs. A later authorized release inspection confirms that the built wheel and source distribution expose the same values.

## Open decisions

None when approved.
