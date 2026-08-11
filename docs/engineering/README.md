# Engineering Artifact System

This directory is the machine-readable engineering memory of SE Harness. Formal artifacts use TOML front matter between `+++` delimiters; stable IDs establish typed traceability independent of file paths.

The distribution packet is under `harness-distribution/`. Commit-bound intent-to-revision traceability is governed by `revision-provenance/`. Draft aggregate multi-work-order release behavior is specified under `aggregate-release/`. Templates and evidence are excluded from active-artifact parsing.

Repository-specific commands, entry points, and constraints are curated in `REPOSITORY_CONTEXT.md`. It is repository-owned operating context, not a formal artifact or source of approval authority.

Validate and visualize with:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python scripts/generate_harness_dashboard.py --root .
```

The governing order is intent, capability, requirement, specification, architecture and ADR, verification, approved work order, implementation evidence, release contract, and operating contract.

Commit-bound instance records extend that chain: a `VREC-*` binds a work order and verification contract to a clean candidate commit and evidence; an `RLS-*` binds a release contract to that same commit. These later governance records must not claim the hash of the commit containing themselves.
