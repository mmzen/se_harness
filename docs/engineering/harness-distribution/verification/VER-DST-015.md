+++
id = "VER-DST-015"
type = "verification"
title = "Verify simplified consumer GitHub CI installation and upgrade"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
verifies = ["REQ-DST-056", "REQ-DST-057", "REQ-DST-058", "REQ-DST-059"]
+++

# Verification Contract: Verify simplified consumer GitHub CI installation and upgrade

## Independence

Expected workflow structure, version/origin invariants, target-file preservation, and failure outcomes are asserted from the approved requirements and specification rather than copied from production render helpers. Disposable repositories and isolated environments separate consumer, adversarial checkout, and self-hosting roles.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-056 | installer/adoption fixtures and YAML inspection | no CI, several existing workflows, missing parents, exact-path conflict | one dedicated workflow is added; unrelated bytes are unchanged; conflict writes nothing; external-enforcement boundary is explicit |
| REQ-DST-057 | runtime identity and workflow execution | exact release, wrong version, checkout shadow, missing wheel, self-hosting root | one exact external runtime assesses consumers; ambiguity fails; protected self-hosting remains separate |
| REQ-DST-058 | adversarial integration and command-spy tests | valid/ambiguous PR field, modified checkout scripts, graph pass/fail, dashboard | every harness semantic is package-owned; checkout scripts are never the CI oracle; status is preserved |
| REQ-DST-059 | schema-2 upgrade and migration fixtures | package-only update, plan, apply, rerun, customized workflow, interrupted transaction | version and lock synchronize only on apply; result is atomic/idempotent; customization is preserved; no consumer reconciliation command is needed |

## Acceptance scenarios

- Initialize an empty repository and prove GitHub workflow discovery inputs are complete.
- Adopt repositories containing zero, one, and several unrelated workflow files and compare their exact pre/post bytes.
- Reject a conflicting or symlinked dedicated workflow with a no-write snapshot.
- Execute the generated consumer workflow contract against a disposable valid repository with one work-order declaration.
- Reject missing, duplicated, malformed, or injected work-order declarations through package-owned parsing.
- Add misleading checkout package and script paths and prove the evaluator origin remains outside the checkout or fails closed.
- Modify each installed checkout script and prove CI does not execute it as assessment authority while managed integrity remains visible.
- Upgrade an exact unmodified 0.4.0 consumer workflow to the candidate template, then rerun for byte- and plan-idempotence.
- Customize the old workflow and prove the complete upgrade transaction is blocked without partial writes.
- Run normal upgrade against the exact implementation repository and prove both protected controls remain byte-identical.

## Property and invariant tests

- Every rendered consumer workflow contains exactly one evaluator version equal to `se_harness.__version__` and the installed configuration version.
- It contains one primary consumer job, no `GOVERNOR_*` fields, no bootstrap target, and no source-versus-consumer conditional branch.
- No consumer workflow command names checkout validator, selector, inspector, or dashboard scripts directly.
- All evaluator command paths resolve inside the runner-temporary environment and outside the checkout.
- Install and upgrade plans are deterministically ordered; failed plans and applications preserve complete target snapshots.
- Repeated safe apply produces no content or lock change.

## Static and architecture checks

Inspect dependency direction so package-owned evaluator modules do not import target scripts and the standard installer does not depend on self-hosting reconciliation. Assert canonical template/package parity, workflow syntax, read-only permissions, stable check identity, exact triggers, and absence of generic YAML merge. Assert `ARCH-DST-011`/`ADR-DST-011` selection and unchanged protected self-hosting workflow semantics.

## Security and privacy checks

Exercise traversal, symlinks, hostile repository names, malformed events, terminal escapes, import shadowing, environment manipulation, fake executables, workflow content conflicts, and oversized bounded inputs. Confirm no repository code is imported as evaluator, no secret permission is requested, no target body is logged, and no hosting policy or external action is mutated.

## Performance and resilience checks

Confirm the consumer workflow has removed one full bootstrap job and does not duplicate package installation. Inject package-install, identity, selection, validation, and dashboard failures and verify dependent behavior stops without fallback or partial authority. Timing is reported only as observation.

## Manual assessments

- Confirm the workflow and documentation make the one consumer version obvious.
- Confirm separate workflows running in parallel is understandable and that branch protection remains explicitly owner-managed.
- Confirm the simplified consumer design has not weakened the implementation repository's released-governor boundary.
- Review the exact-version PyPI trust dependency and ensure no stronger checksum or attestation claim is made.
- Confirm application tests remain repository-owned and are not implied by successful harness validation.

## Evidence retention

Retain rendered workflows; parsed job/step/permission summaries; package and module identities; disposable repository trees and hashes; unrelated workflow before/after hashes; conflict/no-write snapshots; event fixtures; command-spy traces; migration plans; configuration and lock diffs; self-hosting protected hashes; test commands/counts/runtimes; deviations; residual risks; and external actions not performed under `docs/engineering/harness-distribution/evidence/WO-DST-016-verification.md`.

## Residual uncertainty

Local fixtures cannot prove future GitHub runner, PyPI, ruleset, or fork-approval behavior. Hosted CI provides environment evidence but not proof of branch-protection configuration. Stronger artifact attestation, other CI providers, and cross-workflow deployment ordering remain separate concerns.
