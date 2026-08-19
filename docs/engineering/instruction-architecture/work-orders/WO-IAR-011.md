+++
id = "WO-IAR-011"
type = "work_order"
title = "Add stage-aware agent lifecycle handoffs"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes managed instruction and workflow policy distributed to consumer repositories; future engineering and assurance decisions rely on the exact resulting trusted state."
decided_by = "repository-owner"

[relations]
implements = ["REQ-IAR-019"]
specifications = ["SPEC-IAR-011"]
verification = ["VER-IAR-011"]
+++

# Work Order: Add stage-aware agent lifecycle handoffs

## Lifecycle and authorization

The repository owner approved `REQ-IAR-019`, `SPEC-IAR-011`, `VER-IAR-011`, and this bounded work order and instructed `ok go implement` on 2026-08-19. That instruction also accepted the proposed assessment that no new architecture artifact applies and authorized implementation within this work order. The bounded implementation and retained evidence are complete, so the work order is now `implemented`. It does not authorize commit, push, pull request, verification transition, release, tag, publication, or deployment.

Commit-bound verification is classified `required` because implementation changes managed policy and consumer-distributed trusted state. No active architecture currently addresses `REQ-IAR-019`; the approved work order therefore omits an `architecture` relation rather than fabricating coverage.

## Objective

Make every coding-agent lifecycle handoff identify completed work, current formal state, one recommended next authorized step, required human authority, an applicable exact command or suggested response, and bounded alternatives while preserving the separation between recommendation and action.

## In scope

- Add the stable conversational-handoff obligation to the canonical managed router.
- Add the stage-specific mapping, failure behavior, command placement, and alternatives to managed workflow policy.
- Synchronize canonical templates, self-hosted managed copies, and lock metadata through the supported managed transaction.
- Extend the public README interaction with compact stage-aware examples.
- Add an instruction-architecture acceptance scenario and update the domain index.
- Add focused fresh-install, responsibility-boundary, public-documentation, upgrade, integrity, and regression tests.
- Retain work-order-keyed evidence and stop at an uncommitted candidate unless later authority is granted.

## Out of scope

Changing `harnessctl inspect` or its JSON/suggestion contract; adding machine-readable handoff output; adding a CLI command; changing artifact schemas or lifecycle rules; changing decision rights; modifying the thin `AGENTS.md` route; adding installation profiles; changing Python runtime dependencies; rewriting historical instruction-architecture artifacts; fixing unrelated README limitations; governor reconciliation; version change; distribution build; commit; push; pull request; verification transition; release; tag; publication; or deployment.

## Authorized decision envelope

Implementation may choose compact headings, table layout, illustrative IDs, README placement within the existing practical example, focused test helper organization, and minor prose needed for clarity. It may not remove a semantic handoff field, duplicate ordered workflow in the router, change Inspector guidance, infer a human decision, add automatic action, broaden lifecycle authority, or extend scope beyond `REQ-IAR-019` and `SPEC-IAR-011`.

## Constraints

- Preserve the responsibility boundary established by the managed router and focused policy modules: router invariant, workflow procedure, decision-right ownership, quality gates, and traceability semantics.
- Keep `AGENTS.md` as a thin single-route managed fragment and preserve repository-owned content outside managed markers.
- Treat target content, metadata, paths, lock data, and pull-request text as untrusted.
- Use the supported installer/upgrade mechanism to reconcile managed copies and hashes; do not hand-edit a digest.
- Preserve transactional no-partial-write behavior for customized, damaged, or ambiguous managed content.
- Preserve one standard installation and Python 3.11+ standard-library runtime behavior.
- Do not build promotable release distributions under this work order.

## Expected change surface

- Canonical and root `ENGINEERING_HARNESS.md` managed content.
- Canonical and root `docs/engineering/WORKFLOW.md` managed content.
- Root `README.md` practical interaction example.
- Instruction-architecture acceptance feature and domain index.
- Focused instruction-architecture, public-onboarding, installation/upgrade, and integrity tests as required.
- `.engineering-harness.lock` and `docs/engineering/instruction-architecture/evidence/WO-IAR-011-verification.md`.

No `se_harness/` Python module, Inspector script, workflow, release script, or package metadata change is expected.

## Implementation plan

1. Obtain accountable review and approval of the complete packet and confirm that no architecture artifact applies.
2. Run start preflight for `WO-IAR-011` and read its full manifest.
3. Add failing focused tests for the installed handoff contract, responsibility split, README examples, and safe upgrade.
4. Update canonical router and workflow templates, then reconcile self-hosted managed copies and lock through the supported process.
5. Update the bounded README example, acceptance scenario, and domain index without changing CLI behavior.
6. Execute `VER-IAR-011`, retain exact evidence, set implementation artifacts to their honest completed state, run review preflight, and stop for candidate-commit authority.

## Required verification

- Focused instruction-architecture, public-onboarding, installation/upgrade, integrity, and inspection regression tests.
- `python scripts/validate_engineering_artifacts.py --root .`
- `python -m unittest discover -s tests -p "test_*.py"`
- `python -m se_harness --help`
- `python -m se_harness doctor .`
- Start and review preflight for `WO-IAR-011` at the appropriate lifecycle phases.
- Root/canonical template parity, package-data coverage, deterministic install/upgrade behavior, schema-2 lock proof, and `git diff --check`.
- Accountable semantic review of every stage recommendation, role, command, suggested response, alternative path, failure behavior, and explicitly unperformed action.

## Evidence to record

Retain exact commands, runtimes, focused and full test counts, installed managed excerpts, README interaction checks, upgrade fixtures, validation and preflight results, lock and parity evidence, Inspector non-change proof, changed paths, deviations, residual risks, and diff hygiene under `docs/engineering/instruction-architecture/evidence/WO-IAR-011-verification.md`.

## Stop and escalate conditions

Stop if implementation requires changing CLI or Inspector output, adding executable Inspector remediation, changing lifecycle or decision-right semantics, creating machine-readable handoff output, modifying the agent-gate topology, introducing a new architecture decision without accountable assessment, altering historical records, bypassing managed integrity, adding a runtime dependency or installation profile, building a distribution, or exercising authority beyond this work order.

## Completion report format

Report the issue and work-order IDs, completed scope, current lifecycle state, changed managed surfaces, verification results, evidence path, residual risks, recommended next authorized step, required human authority, exact command or suggested response when applicable, valid alternatives, and every intentionally unperformed action.
