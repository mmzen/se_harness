# WO-IAR-008 implementation and verification evidence

## Authority and scope

The repository owner approved `REQ-IAR-016`, `SPEC-IAR-008`, `ARCH-IAR-008`, `ADR-IAR-008`, `VER-IAR-008`, and `WO-IAR-008` on 2026-08-15 with the instruction `go for implementation`. Work remained within the approved first inspection increment: one read-only projection over existing validator and Harness Explorer evidence, with no new finding rule, score, lifecycle transition, remediation, configuration, evaluator-independence change, or release action.

## Baseline and red test

Before implementation:

- candidate and released CLI help contained no `inspect` command;
- validation taxonomy `se-harness-validation-taxonomy-v1` was already implemented;
- Harness Explorer already owned the derived `W-HEX-*`, `W-REV-*`, and `I-REV-*` observations;
- the first focused test failed at the intended seam with `ModuleNotFoundError: No module named 'inspect_engineering_artifacts'`.

The implementation discovered that the stable Explorer snapshot intentionally does not expose diagnostic planes. The approved dependency boundary was preserved by using the `ValidationReport` returned alongside `generate_snapshot` for plane counts; the dashboard snapshot schema was not changed.

## Delivered behavior

- Added `harnessctl inspect [TARGET] [--json]` to the candidate CLI.
- Added root and canonical managed `scripts/inspect_engineering_artifacts.py`.
- Reused `generate_harness_dashboard.generate_snapshot`, which reuses the formal validator and existing Explorer finding rules.
- Added deterministic `se-harness-inspection-v1` JSON with repository context, formal validity, taxonomy and plane counts, graph/finding counts, mechanical lifecycle queues, and every existing finding.
- Added compact human output. Repeated findings are grouped by unchanged rule, severity, and authority; complete individual findings remain in JSON.
- Added mechanical queues for `ready` decisions, `draft` definitions, and approved or in-progress work orders.
- Added explicit `authority = "derived"` and `producer = "repository-local"` boundaries.
- Preserved inspect exit zero when a report is successfully produced, including an invalid embedded formal graph; `validate` retains gate exit behavior.
- Escaped terminal control characters in human output.
- Invoked the inspection repository script with Python `-B` and proved that both human and JSON execution create no repository bytecode, output, lock, or Git change.
- Updated the managed review workflow, concise operator reference, root onboarding, canonical distribution data, package data, and lock metadata.

## Verification results

- Start preflight: passed for `WO-IAR-008` in `in_progress` with zero diagnostics.
- Review preflight: passed for `WO-IAR-008` in `implemented` with zero diagnostics after evidence retention.
- Focused inspection and CLI suite after implementation: 31 tests passed with one expected skip.
- Affected inspection, CLI, workflow, documentation, Explorer, and taxonomy suite: 83 tests passed with one expected skip.
- Complete Python 3.14.6 suite: 179 tests passed with three expected skips.
- Complete Python 3.11.9 suite: 179 tests passed with three expected skips.
- Candidate formal validation before lifecycle completion: 323 artifacts, zero errors, and the same 40 existing maintenance warnings.
- Candidate-source `doctor`: passed every required, distribution, managed-integrity, lock, script, and self-hosting-governor check; eleven historical W013 placement warnings remained nonblocking.
- Managed upgrade: 34 entries, 32 unchanged, and two protected repository-specific self-hosting controls; apply synchronized the new script and workflow lock metadata, and the following plan was idempotent.
- Root/canonical inspection-script and workflow byte parity: passed.
- CLI help exposed `inspect`; command help exposed only optional target and `--json`.
- Real editable `harnessctl.exe inspect .`: passed while reporting candidate package version 0.3.0.
- Real repository human report before lifecycle completion: 323 artifacts, 1,166 relations, 78 findings, two ready decisions, twelve draft definitions, and one active work order; 49 warnings and 29 informational findings were compacted into six transparent rule groups.
- Post-completion inspection retained the same graph and findings, with two ready decisions, twelve draft definitions, and zero active work orders.
- Two real JSON runs were identical, changed no Git-visible repository state, used schema `se-harness-inspection-v1`, and produced captured PowerShell UTF-8 hash `059c57280acd5a90625d06d8322dbf7c31abc5233c9dd1694caacfb0b65f2f55`.

## Distribution and local executable

The standard package-data declaration explicitly includes `templates/repository/standard/scripts/inspect_engineering_artifacts.py`. Fresh-install and editable-entry-point tests cover the installed command and managed script.

The documented setup command `python -m pip install --editable . --no-deps` refreshed the local development environment so `.venv\Scripts\harnessctl.exe inspect .` executes candidate source. Pip created only an ephemeral editable wheel in its temporary cache. No promotable wheel, sdist, package version change, release record, tag, or publication was produced.

## Changed components

- Formal `IAR-008` packet, domain index, and this evidence.
- Candidate CLI adapter.
- Root and canonical inspection scripts.
- Root and canonical managed workflow.
- Root onboarding and focused command reference.
- Package-data declaration and schema-2 lock.
- Inspection, CLI, instruction-architecture, onboarding, and distribution tests.

## Deliberately unperformed work

No new validator or Explorer rule, orphan definition, aging threshold, configurable inspection policy, health score, automatic remediation, lifecycle transition by automation, dashboard UI change, independent-evaluator redesign, governor reconciliation, version change, promotable distribution, commit, push, pull request, VREC, release record, tag, publication, or deployment was produced.

## Residual risks

- Inspection executes the managed script from the inspected repository and is therefore development feedback, not independent governor assurance. GitHub issue #46 tracks that evaluator boundary.
- Existing Explorer findings can be noisy. The human renderer groups repetition but does not suppress or reinterpret any finding.
- Draft release and operating contracts appear in the definition queue even when intentionally dormant; the queue is mechanical attention, not a claim that completion is currently required.
- A zero inspection exit means the report was produced, not that formal validation passed or no attention exists.
- Snapshot and finding compatibility remain dependencies; regression tests detect changes but cannot prove that every future observation is useful.
