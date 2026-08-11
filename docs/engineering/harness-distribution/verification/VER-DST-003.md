+++
id = "VER-DST-003"
type = "verification"
title = "Verify PyPI onboarding and public package metadata"
status = "approved"
owners = ["quality-owner", "documentation-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-DST-009", "REQ-DST-010", "REQ-DST-011", "REQ-DST-012", "REQ-DST-013"]
+++

# Verification Contract: Verify PyPI onboarding and public package metadata

## Independence

Verification derives assertions from approved requirements and parses public files independently of the README implementation structure where practical. Static tests do not execute documentation commands, access external services, or treat an editable installation as released proof. A later approved release independently inspects built and published metadata.

## Requirement-to-evidence matrix

| Requirement | Method | Case or evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-009` | deterministic text inspection and manual onboarding review | primary install and quick-start sections | PyPI is primary, exact version matches metadata, and source installation is development-only |
| `REQ-DST-010` | deterministic platform-command inspection | Windows, POSIX, direct-path, and module examples | launcher ownership and activation semantics are complete and do not assume global installation or `py` |
| `REQ-DST-011` | ordered command and boundary inspection | pip update, plan, apply, doctor | package update and target mutation are explicitly separate |
| `REQ-DST-012` | standard-library TOML and file inspection | readme, license, URLs, Python, dependencies, script | all static metadata is present, canonical, and compatible with the current build contract |
| `REQ-DST-013` | cross-file synchronization and assurance-language review | package version, README exact pin, CI prose, workflow reference | versions agree, baseline prose is configuration-neutral, and authority boundaries remain truthful |

## Automated checks

- Add focused standard-library tests for every deterministic rule in `SPEC-DST-003`.
- Parse `pyproject.toml` rather than matching metadata solely as unstructured text.
- Confirm the exact-version README example equals both `[project].version` and `se_harness.__version__`.
- Confirm primary install, environment paths, quick-start commands, upgrade sequence, project URLs, license reference, and source-development placement.
- Confirm conceptual baseline prose contains no pinned historical package version and points to the workflow as current configuration.
- Confirm UTF-8 decoding and reject unresolved placeholders, broken-encoding markers, duplicate primary install sections, and malformed local links.
- Run the complete unit suite on Python 3.11 and the available local runtime.
- Run formal graph validation, `harnessctl doctor`, start and review preflight as phase-appropriate, CLI help, and deterministic dashboard generation.
- Confirm the artifact packet, README, metadata, tests, and evidence do not modify canonical installed templates or `.engineering-harness.lock`.

## Manual assessments

- Review the first screen as a new adopter: prerequisite, install, launcher discovery, and new/existing repository choice must be discoverable without reading the artifact model.
- Confirm retained governance, lifecycle, provenance, Explorer, safety, and agent-ownership explanations still match implemented behavior.
- Confirm external links name the production PyPI project, repository, issues, and immutable release collection without claiming availability as authority.
- Confirm the license description matches the retained `LICENSE` text.

## Deferred release checks

Under the next approved release work order, build the candidate wheel and normalized sdist, inspect core metadata and included README/license files, install the exact wheel in a clean Python 3.11 environment, inspect the package-index rendering after publication, and verify external URLs and attestations. These actions are not authorized by `WO-DOC-003`.

## Pass criteria

All locally authorized automated and manual checks pass, the graph has zero diagnostics, public commands and metadata are internally consistent, no historical record or external release changes, and the deferred release checks are explicitly carried into the next release contract rather than reported as already satisfied.

## Evidence retention

Retain exact commands, runtime versions, focused and full test counts, parsed metadata values, README review observations, graph and doctor results, changed paths, deferred checks, deviations, and residual risks under `WO-DOC-003`.

## Residual uncertainty

PyPI rendering and final distribution metadata cannot be proven before an authorized future build and publication. Static conformance reduces but does not replace that release inspection.
