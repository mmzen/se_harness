+++
id = "ARCH-DST-003"
type = "architecture"
title = "Public onboarding and package-metadata boundary"
status = "implemented"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-DST-009", "REQ-DST-010", "REQ-DST-011", "REQ-DST-012", "REQ-DST-013"]
conforms_to = ["SPEC-DST-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "technology-framework-vendor-or-external-service", "material-alternatives"]
rationale = "ADR-DST-003 chose one README serving as repository entry point and PyPI long description, over a separate package README and over build-time generation. It binds public packaging metadata to an external index and its rendering."
assessed_by = "technical-owner"
+++

# Architecture: Public onboarding and package-metadata boundary

## Components and responsibilities

- **Root README**: human-oriented public entry point and package long description; explains installation, operation, governance, and trust without granting authority.
- **`pyproject.toml`**: static source of package name, version, long-description selection, license, URLs, Python compatibility, dependencies, and console entry point.
- **Virtual environment**: owns the interpreter, installed package, and platform-specific `harnessctl` launcher exposed through activation or direct path.
- **Harness-enabled repository**: receives managed and owner-controlled files only through explicit `init`, `adopt`, or `upgrade --apply` operations.
- **Formal engineering graph**: remains the authority for the documentation and metadata change.
- **Release services and evidence**: GitHub Releases and PyPI expose immutable distribution observations; retained VREC/RLS and publication evidence establish governed lineage.

## Dependency direction

```text
formal packet -> README + static project metadata + deterministic tests
project version -----------------------> exact README version example
README --------------------------------> package long description on next release
pip environment -----------------------> harnessctl launcher
harnessctl upgrade --apply ------------> target repository managed state
released artifacts + external services -> public observations only
```

The README may point toward formal and release evidence, but no documentation, badge, package-index page, or installed CLI may create formal authority.

## Trust boundaries

- Treat shell environment, interpreter selection, `PATH`, repository target, and installed version as user-controlled state.
- Do not assume a globally installed launcher or the presence of the Windows `py` command.
- Do not execute README commands in deterministic static tests.
- Do not retrieve dynamic metadata, badges, versions, or prose during package build.
- Do not infer successful release, verification, or repository compliance from a URL or package installation.

## Required patterns

- One root README serves GitHub and the next package-index long description.
- Static project metadata and standard-library tests provide deterministic synchronization.
- Public commands identify the interpreter environment explicitly.
- Package and repository upgrades are separate user decisions.
- Version-specific release facts are either synchronized or linked to immutable evidence.

## Prohibited patterns

- A second PyPI-only README.
- A globally assumed `harnessctl` binary.
- Automatic target-repository mutation after pip upgrade.
- Network-fetched build metadata or README fragments.
- Candidate or source-checkout installation described as a released baseline.
- README edits that mutate managed target templates or historical governance records.

## Quality attributes and conformance

Onboarding shall be usable in one screen before deep governance material, while the retained detail remains accurate. Metadata and version examples shall be deterministic, parseable without third-party runtime dependencies, and compatible with Python 3.11+. Conformance is checked by `VER-DST-003`, full regression tests, graph validation, doctor, preflight, and manual README review.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-003`).** The five
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-DST-003`, the active specification that specifies them. The assessment
reads the drivers and rejected options of `ADR-DST-003`, the one active ADR
that decides this architecture. Title, status, statement and ADR relations are
unchanged.
