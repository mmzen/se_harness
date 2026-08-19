+++
id = "VER-RLO-002"
type = "verification"
title = "Verify portable and repository release-policy separation"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
verifies = ["REQ-RLO-009", "REQ-RLO-010", "REQ-RLO-011"]
+++

# Verification Contract: Verify portable and repository release-policy separation

## Independence

Verification inspects built wheel contents, installed disposable consumers, CLI help, managed templates, repository scripts, workflow YAML, and independently generated malformed fixtures. Consumer-boundary expectations do not import the repository distribution helper under test. The released governor remains separate from candidate source and package evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-009 | package, CLI, validator, template, init/adopt/upgrade inspection | built wheel listing; installed help; disposable consumers; managed-file reconciliation | no packaged or installed consumer surface contains the SE Harness distribution contract; generic RLS preparation and validation remain correct |
| REQ-RLO-010 | repository binder unit/integration and atomicity tests | exact, replay, absent, partial, duplicate, unsafe, wrong-version, wrong-commit, wrong-epoch, wrong-hash, and write-failure fixtures | only exact input binds; failure leaves the ready RLS unchanged; lifecycle and core identity never change |
| REQ-RLO-011 | workflow static, state-machine, deterministic-build, and failure tests | one-input trigger; import origins; permissions; exact/missing/mismatched RLS extension; two builds; GitHub/PyPI/Pages replay | publication behavior and trust boundaries remain unchanged; invalid local provenance blocks before candidate execution or credentials |

## Acceptance scenarios

Executable scenarios are retained in `acceptance/release-policy-boundary.feature`. Tests must implement each scenario or name equivalent fixture coverage in the retained evidence.

## Property and invariant tests

- No file inside the wheel or standard consumer template contains `python-wheel-sdist`, SE Harness distribution filenames, or a distribution-specific `prepare-release` option.
- The generic RLS produced before and after the correction is identical for the same core inputs when the removed option is not used.
- A repository binder operation changes only one complete distribution table in one ready RLS.
- Binder failure preserves the original file hash.
- Every repository release path uses one distribution schema implementation outside `se_harness*`.
- The normal publication workflow exposes exactly one required `release_record` input.
- Candidate code never executes in a job with GitHub write, PyPI OIDC, or Pages write permissions.
- Historical RLS files without a distribution table remain valid graph artifacts.

## Static and architecture checks

- Assert `harnessctl prepare-release --help` omits `--distribution-manifest`.
- Inspect wheel RECORD/content and import discovery for absence of `se_harness.release_distribution`.
- Inspect initialized, adopted, and upgraded consumer validators and release templates for repository-specific terms.
- Confirm root and managed validator/template copies remain byte-identical and lock hashes are reconciled.
- Confirm repository scripts are excluded from the wheel and standard template.
- Parse workflow YAML strictly and assert triggers, inputs, permissions, environments, full action pins, checkout placement, and trusted repository import origins.
- Validate the formal graph and architecture/specification/work-order overlap.

## Security and privacy checks

Treat manifest, TOML, RLS paths, filenames, Git output, workflow expressions, downloaded artifacts, and external responses as untrusted. Review safe destination resolution, duplicate-key handling, size limits, atomic replacement, symlink behavior, expression-to-shell transport, and the no-candidate-code credential boundary. Confirm no new secret, PAT, publisher identity, or environment permission is introduced.

## Performance and resilience checks

Measure binder and repository-policy validation over representative bounded records. Inject read, parse, fsync/replace, and workflow-state failures. Prove there is no unbounded retry, partial record update, redundant candidate build, or additional production call.

## Manual assessments

- The technical owner confirms the packaged/repository dependency direction matches `ADR-RLO-002`.
- The release owner confirms two agent-run preparation commands remain operationally acceptable and the normal production workflow still needs only one RLS input.
- The security owner confirms trusted-main distribution validation remains outside candidate and privileged execution boundaries.
- The product owner confirms consumer installations contain no repository-specific release promise.

## Evidence retention

Retain implementation evidence at `docs/engineering/release-orchestration/evidence/WO-RLO-002-verification.md`. Record exact commands, test counts, candidate/governor/package origins, wheel content, disposable installation observations, before/after CLI and template surfaces, binder fixture matrix and unchanged-file hashes, workflow policy matrix, documentation changes, deviations, and every unperformed governance or production action.

## Residual uncertainty

Static and fixture tests cannot prove future GitHub, PyPI, or Pages behavior. The first separately authorized release using repository binding remains an operational confirmation. Core validation intentionally will not assess the semantic truth of repository-owned distribution metadata; repository CI and resolver checks are mandatory.

## Approval

Approved as an independent definition by the accountable repository owner on 2026-08-18 through the statement `I approve this plan, you can create the artifact pack for it`. This does not verify any future candidate.
