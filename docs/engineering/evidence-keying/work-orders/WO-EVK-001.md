+++
id = "WO-EVK-001"
type = "work_order"
title = "Implement portable evidence-path keying"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes provenance preparation, formal governance validation, managed policy behavior, and derived assurance findings used by later engineering and release decisions; correctness therefore requires retained evidence and commit-bound independent verification."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-EVK-001", "REQ-EVK-002", "REQ-EVK-003", "REQ-EVK-004"]
specifications = ["SPEC-EVK-001"]
architecture = ["ARCH-EVK-001", "ADR-EVK-001"]
verification = ["VER-EVK-001"]
+++

# Work Order: Implement portable evidence-path keying

## Lifecycle

The accountable owners approved the governing intent, capability, requirements, specification, architecture assessment, ADR, verification contract, and this bounded work order on 2026-08-19. Start preflight passed and the governing manifest was read before implementation began. The bounded implementation and retained evidence are complete. Only a later eligible VREC may establish commit-bound verification.

## Objective

Make flat filename and directory-per-work-order evidence layouts produce the same exact work-order attribution across aggregate verification capture, formal validation, inspection, and Harness Explorer, while preserving path safety, historical provenance, managed upgrade behavior, and independent execution-plane boundaries.

## In scope

- Reconcile current active aggregate-release and Explorer definition wording that restricts evidence discovery to filenames, subject to approval by their accountable owners.
- Add the specified pure key extraction/membership behavior to installed-package provenance preparation.
- Centralize repository-local key extraction in the managed validator and reuse it from dashboard discovery; keep inspection free of a separate matcher.
- Apply the contract to current aggregate capture and validation only. Preserve current single-work-order VREC behavior.
- Update derived evidence association, readiness, `W-HEX-001` behavior, and finding-rules identity without changing snapshot shape or authority.
- Reconcile root managed validator/dashboard sources with canonical standard-template copies and authorized lock hashes.
- Add the shared cross-plane case matrix and focused capture, validator, inspection, dashboard, platform, safety, parity, and upgrade regression tests.
- Retain exact work-order-keyed verification evidence and a completion report.

## Out of scope

- Implementing issue 49 or adding keyed-evidence enforcement to single-work-order VRECs.
- Assessing evidence content quality or automatically accepting verification.
- Renaming consumer evidence, moving artifacts, or rewriting historical VREC/RLS metadata and released facts.
- Changing evidence content projection, Markdown rendering, snapshot fields, lifecycle states, release scope, Git policy, governor selection, or CI topology.
- Adding installation profiles, dependencies, external services, health scores, release builds, tags, publication, or deployment.

## Authorized decision envelope

The implementation agent may choose local helper names, exact placement within the existing provenance and validator modules, internal immutable container types, test class organization, and diagnostic wrapping. The agent may not change candidate-component scope, key grammar, multi-key association, deterministic ordering, package/repository-local dependency direction, existing path-safety outcomes, lifecycle behavior, or historical records.

## Constraints

- Follow `AGENTS.md`, `ENGINEERING_HARNESS.md`, and all managed workflow, decision-rights, quality-gate, and traceability policy.
- Treat repository paths, contents, lock data, artifact metadata, and test fixtures as untrusted.
- Preserve Python 3.11+ standard-library runtime behavior and the single standard installation.
- Keep root and canonical managed copies byte-identical and preserve content outside managed markers.
- Candidate source and candidate packages produce evidence only; they do not replace released-governor assurance.
- Do not build a promotable distribution under this work order.
- Do not invent a formatter or linter gate.

## Expected change surface

- Evidence-keying formal packet and the accountable reconciliation of affected active aggregate/Explorer definitions.
- Package provenance preparation.
- Managed validator, dashboard generator, and their canonical template copies.
- Finding-rules identity and focused provenance/validation/inspection/dashboard tests.
- Managed lock evidence, domain index, acceptance scenarios, and retained work-order evidence.

Changes to CLI options, record schema, release workflows, package version, governor controls, browser template, or historical artifacts are not expected.

## Required verification

- Run start preflight before implementation and read its complete manifest.
- Execute every case in `VER-EVK-001` and `acceptance/evidence-keying.feature`.
- Run focused provenance, revision-validation, inspection, dashboard, instruction-architecture, installer/upgrade, and self-hosting tests affected by the change.
- Run `python -m unittest discover -s tests -p "test_*.py"`.
- Run `python scripts/validate_engineering_artifacts.py --root .`.
- Run `python -m se_harness --help` and `python -m se_harness doctor .`.
- Run review preflight, inspect current attention, and generate Harness Explorer.
- Confirm root/template parity, deterministic repeated output, and a clean diff with no unexpected historical changes.

## Evidence to record

Retain `docs/engineering/evidence-keying/evidence/WO-EVK-001-verification.md` containing:

- issue-72 reproduction before and accepted behavior after;
- the shared path-case matrix and both execution-plane results;
- aggregate capture and authored-VREC validation results;
- W-HEX/readiness and Explorer association observations;
- unsafe-path and cross-platform cases;
- managed parity, upgrade, lock, doctor, and preflight results;
- full test and artifact-validation counts;
- exact changed-file inventory, historical non-mutation review, deviations, and residual risks.

## Stop and escalate conditions

Stop on missing or conflicting formal approval, preflight failure, managed integrity failure, active filename-convention definitions left unreconciled, need to change single-work-order enforcement, disagreement between execution planes, path-safety regression, platform-dependent key sets, root/template divergence, historical-record mutation, new dependency/profile/schema need, required test failure, unclassified warning, scope drift, or authority beyond this work order.

## Completion report format

Report the approved requirement and architecture coverage, exact implementation and managed-template changes, contract-case results, focused and full verification results, evidence path, candidate worktree state, deviations, residual risks, and confirmation that no lifecycle, release, publication, governor, or historical provenance action was performed.
