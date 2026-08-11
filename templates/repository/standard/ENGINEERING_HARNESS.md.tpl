# Engineering Harness for {{PROJECT_NAME}}

This repository uses SE Harness {{HARNESS_VERSION}}. Formal engineering memory lives in `docs/engineering/`; approved artifacts are authoritative for product intent and work authorization.

## Start work

1. Read `docs/engineering/README.md`.
2. Read the repository-owned facts in `docs/engineering/REPOSITORY_CONTEXT.md`.
3. Run `python scripts/validate_engineering_artifacts.py --root .`.
4. Select one approved work order and read its complete linked artifact chain.
5. Inspect the affected code, tests, and documentation.
6. Implement only the bounded authorized change and retain verification evidence.

## Visual review

```powershell
python scripts/generate_harness_dashboard.py --root .
```

Open `target/harness-dashboard/index.html`. The dashboard is derived, read-only evidence; it does not approve work or releases.

## Commit-bound verification and release

Use `harnessctl capture-verification` after committing a clean candidate and its evidence. The ready verification record is committed later and reviewed by the assurance owner. Use `harnessctl prepare-release` only after that governance record is cleanly committed. Release records copy the verified candidate commit and remain `ready` until an accountable release owner acts.

The commands never create commits, tags, approvals, releases, or publications.

## Core rule

> Code is not the source of product intent. Approved requirements and specifications are. Code and tests are evidence that approved intent was implemented.
