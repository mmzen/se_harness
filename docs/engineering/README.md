# SE Harness Engineering Artifact Index

> Repository-owned index for the standard governed `se_harness` repository. Shared workflow, decision rights, quality gates, and traceability policy are routed from `ENGINEERING_HARNESS.md` and remain managed separately.

## Product and governance domains

- `evidence-keying/`: approved portable work-order evidence-attribution contract and bounded implementation work across flat and directory-organized layouts.
- `harness-distribution/`: reusable installation, adoption, documentation, and package-distribution behavior.
- `revision-provenance/`: commit-bound verification and release record preparation.
- `aggregate-release/`: exact multi-work-order release coverage.
- `portable-managed-integrity/`: portable schema-2 managed-file integrity and migration.
- `verification-supersession/`: explicit retention and supersession of stale ready VRECs.
- `pypi-publication/`: governed promotion of released artifacts to PyPI.
- `release-orchestration/`: deterministic last-mile publication from one released RLS identity.
- `dashboard-publication/`: repository-specific, release-bound Harness Explorer demonstration publication and replay controls.
- `work-order-lifecycle/`: lifecycle meanings and configured verified-work consistency.
- `instruction-architecture/`: canonical agent routing, ownership modes, preflight, and independent CI enforcement.
- `self-hosting-boundary/`: separation of the released governing harness from candidate source and candidate-package acceptance.
- `root-cause-analysis/`: governed publication of non-authoritative incident learning and prevention references.
- `released-evaluator-boundary/`: issue #81 prevention definitions for standard released-evaluator identity, pre-write mutation exclusion, release-readiness provenance, and bounded recovery.
- `repository-harness-upgrade/`: standard-root transition from the released bootstrap evaluator to exact public se-harness 0.5.0.
- `operating-contract-activation/`: accountable activation and maintenance of continuing operational assurance obligations.
- `release-contract-disposition/`: explicit disposal of unused release proposals after authoritative aggregate release.
- `work-order-assurance-classification/`: explicit work-order applicability for commit-bound verification and derived assurance follow-up.
- `workflow-execution/`: deterministic bounded workflow scope, lifecycle mutation rules, and canonical agent-independent handoffs.
- `release-0.2.0/`: historical release qualification and immutable release records for version 0.2.0.
- `release-0.2.1/`: incremental release qualification, aggregate provenance, and GitHub-to-PyPI promotion records for version 0.2.1.
- `release-0.2.2/`: integrated instruction-architecture and self-hosting qualification, aggregate provenance, and the released record for version 0.2.2.
- `release-0.3.0/`: aggregate qualification, provenance, and the released record for version 0.3.0.
- `release-0.4.0/`: aggregate qualification, provenance, and the released record for version 0.4.0.
- `release-0.4.1/`: aggregate qualification, provenance, and the released record for version 0.4.1.

## Repository-specific engineering documentation

- `REPOSITORY_CONTEXT.md`: confirmed commands, entry points, ownership, architecture, and repository constraints.
- `templates/`: non-authoritative starting points for new formal artifacts.
- `../notes/`: non-authoritative progressive explanations for human readers from conceptual overview through practical usage.

Formal artifacts use TOML front matter between `+++` delimiters. Stable IDs and declared typed relations establish authority independent of file paths. Evidence, templates, generated dashboards, source, commits, and this index remain non-authoritative unless referenced by the applicable formal record.

## Maintenance

Update this index when an engineering domain or repository-specific guide is added, moved, superseded, or retired. Do not copy managed policy or lifecycle instructions into this owner-controlled file.
