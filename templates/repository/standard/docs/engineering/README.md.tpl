# Engineering Artifacts for {{PROJECT_NAME}}

This directory is the machine-readable engineering memory of the repository. It separates intent, capability, requirements, specification, architecture decisions, verification, bounded work authorization, release conditions, and operating assurance.

## Workflow

1. Copy the required starting points from `templates/` into a product or domain subdirectory.
2. Allocate stable IDs and complete every metadata field and body section.
3. Keep new artifacts in `draft` until accountable humans review them.
4. Approve a complete intent-to-verification chain and one bounded work order.
5. Validate before and after implementation.
6. Retain work-order-keyed verification evidence before marking work verified.

## Commands

```powershell
python scripts/validate_engineering_artifacts.py --root .
python scripts/generate_harness_dashboard.py --root .
```

Formal artifacts use TOML front matter delimited by `+++`. IDs, rather than paths, are stable references. Templates and evidence are excluded from active-artifact parsing.

## Commit-bound provenance

After committing a clean candidate and its retained evidence, prepare a reviewable verification record:

```powershell
harnessctl capture-verification . --id VREC-001 --work-order WO-001 --verification VER-001 --evidence docs/engineering/DOMAIN/evidence/WO-001-verification.md
```

Commit the ready `VREC-*` in a later governance commit. After assurance review, prepare a release record with `harnessctl prepare-release`. Both commands create only `ready` records and never commit, tag, approve, release, or publish.

Read `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` before approving the first artifact chain.
