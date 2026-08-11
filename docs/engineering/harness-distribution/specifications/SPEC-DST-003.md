+++
id = "SPEC-DST-003"
type = "specification"
title = "PyPI-first onboarding and public metadata contract"
status = "implemented"
owners = ["technical-owner", "documentation-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-DST-009", "REQ-DST-010", "REQ-DST-011", "REQ-DST-012", "REQ-DST-013"]
+++

# Specification: PyPI-first onboarding and public metadata contract

## Scope

Define the public root README and static project metadata required for a user to install the released package, find its environment-local CLI, initialize or adopt a repository, upgrade safely, understand the principal governance capabilities, and locate immutable release and provenance information.

The README remains explanatory evidence. Formal artifacts, managed installed policy, VREC/RLS records, and accountable decisions retain their existing authority.

## Public information architecture

The README shall use this high-level order:

1. concise purpose, Python support, PyPI, repository, and release links;
2. PyPI installation and environment-local command discovery;
3. a short new/existing-repository quick start;
4. feature and safety overview;
5. agent instruction ownership and the five-minute governed workflow;
6. artifact model, Explorer questions, provenance, command reference, and installed layout;
7. two-stage upgrade guidance;
8. CI assurance, release integrity, and distribution-development guidance.

Deep governance explanations already present in the README shall be retained unless they are duplicated, stale, or contradicted by an approved requirement. Source and editable installation belong only in distribution-development guidance.

## Installation interface

The primary path is a local virtual environment using the selected interpreter:

```text
python -m venv .venv
<platform activation>
python -m pip install --upgrade pip
python -m pip install se-harness
harnessctl --version
```

The README shall also show an exact `se-harness==VERSION` example synchronized with `[project].version`. Windows guidance uses `.\.venv\Scripts\Activate.ps1` and `.\.venv\Scripts\harnessctl.exe`; POSIX guidance uses `source .venv/bin/activate` and `.venv/bin/harnessctl`. `python -m se_harness` is the interpreter-scoped fallback. Documentation shall not require the Windows `py` launcher.

## Quick-start interface

The first operational examples are:

- `harnessctl init TARGET --project-name NAME` for an absent or empty target;
- `harnessctl adopt TARGET --project-name NAME` for an existing repository;
- `harnessctl doctor TARGET` to inspect installed integrity;
- `harnessctl dashboard TARGET` to generate Harness Explorer.

The quick start shall state that repository context and formal authority still require accountable curation after installation or adoption.

## Upgrade state model

Public guidance distinguishes two independently visible states:

1. **Environment distribution state**: changed only by pip installation or upgrade; provides CLI code and canonical templates.
2. **Target repository state**: unchanged until an explicit target-local `harnessctl upgrade TARGET --apply` succeeds.

An upgrade plan is read-only. Apply remains transactional and may stop for customization or conflict. `doctor` observes the resulting installed state.

## Package metadata contract

`pyproject.toml` shall declare:

- `readme = "README.md"`;
- license metadata referencing the retained `LICENSE` file in a form supported by the current setuptools build-system floor;
- Homepage, Repository, Issues, and Releases project URLs rooted at `https://github.com/mmzen/se_harness`;
- the existing Python requirement, no runtime dependencies, and the `harnessctl` console script unchanged.

The implementation shall not introduce dynamic metadata or fetch content during build. Existing PyPI versions remain immutable; the new long description and URLs become externally observable only in a later release.

## Release and assurance language

The README may describe the production publication design: a separately authorized protected GitHub OIDC workflow verifies and promotes exact GitHub release artifacts without rebuilding them, and PyPI exposes attestations. It shall not describe that mechanism as approval or proof of arbitrary repository correctness.

Conceptual CI text shall say "the exact configured released baseline" and direct readers to `.github/workflows/engineering-harness.yml` for the current pin. It shall retain the bootstrap-lag explanation and shall not modify or claim to modify that workflow.

## Deterministic checks

Focused tests shall parse `pyproject.toml` with the standard library and inspect README text to prove:

- required readme, license, URL, Python, dependency, and script metadata;
- primary unpinned and synchronized exact-version PyPI installation examples;
- Windows and POSIX environment-local launcher guidance and module fallback;
- the two-stage upgrade sequence and explicit non-mutation boundary;
- quick-start command coverage and canonical external links;
- absence of a hardcoded historical baseline version in conceptual CI prose;
- absence of source-checkout installation from the primary install section;
- stable UTF-8 text without placeholder or broken-encoding markers.

These tests must not access the network or build release distributions. Wheel, sdist, package-index rendering, and published metadata inspection remain required later under an approved release work order.

## Compatibility and migration

No CLI behavior, installed template, runtime dependency, ownership mode, existing target repository, publication workflow, action pin, CI baseline pin, version, VREC/RLS record, tag, release asset, or PyPI file changes in this implementation. Existing README anchors may change; repository-relative links and common direct section references must remain reviewable.

## Explicitly unspecified decisions

Implementation may choose concise wording, badge use, and exact placement of retained detailed sections, provided the ordering, commands, authority boundaries, metadata fields, and deterministic checks above remain satisfied.
