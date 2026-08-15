+++
id = "SPEC-SHB-002"
type = "specification"
title = "Protected upgrade, governor reconciliation, and replayable acceptance contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
+++

# Specification: Protected upgrade, governor reconciliation, and replayable acceptance contract

## Scope

Correct the standard-upgrade defect without creating a second consumer profile, define a safe way to reconcile the implementation repository with an exact published governor release, and define the replayable functional contract required to separate released-governor assessment from candidate source and package evidence. This specification extends `SPEC-SHB-001`; its governor, candidate-source, candidate-package, exact-identity, and deferred-promotion rules remain in force.

## Actors and external systems

- Repository owner and approved work-order owner.
- Released governor installed from one immutable, checksum-verified publication.
- `se-harness` implementation checkout.
- Candidate source and exact candidate package.
- Ordinary consumer repository.
- GitHub Actions or an equivalent isolated CI runner.
- Disposable governor and candidate acceptance repositories.

## Inputs

- Target repository and operation mode.
- Current schema-1 or schema-2 lock, governor descriptor, and protected file bytes.
- Standard rendered consumer template and the current accepted self-hosting baseline.
- Self-hosting configuration, project metadata, source-layout facts, and governor descriptor.
- Selected work-order identifier and explicit policy decisions for reconciliation.
- Current governor version, release asset, wheel digest, and acceptance-contract identity.
- Target published version, release commit, immutable asset identities and digests, data-only schema and migration declarations, role-specific configuration material, and role-specific workflow material.
- Candidate full commit, wheel, wheel digest, Python runtime, scenario inputs, and expected invariant identifiers.

## Outputs

- Deterministic upgrade plan with `protected`, `unchanged`, `update`, `add`, `customized`, or conflict-equivalent dispositions.
- Transactional normal-upgrade result or fail-closed diagnostics.
- Read-only governor-reconciliation plan and, only with `--apply`, a transactionally updated governor descriptor, repository configuration, role-correct workflow, and corresponding lock metadata.
- Bounded canonical functional-acceptance manifest plus non-canonical execution summary.

## State model

Self-hosting classification is one of:

1. `consumer`: no self-hosting declaration is present and normal standard-template rules apply.
2. `self-hosting`: the target is the exact implementation repository, its role declaration is complete, and its governor descriptor is valid.
3. `ambiguous`: any partial, malformed, inconsistent, or spoofed self-hosting signal exists; planning stops.

A protected control is `locked`, `missing`, or `modified` relative to its current root lock. Only `locked` is eligible for preservation by normal upgrade or as the accepted starting point for automatic reconciliation.

A target governor is `unresolved`, `eligible`, `decision-required`, `conflicted`, or `invalid`. It is `eligible` only when its immutable publication and data-only migration contract are verified, the currently selected governor understands that contract, every repository-owned value is preserved or explicitly supplied, the self-hosting workflow variant is selected, and the complete write set passes validation.

## Behavioral rules

1. The shared self-hosting policy owns the exact protected set: `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`.
2. Classification occurs before desired consumer content can determine a protected-file action.
3. Ordinary consumer repositories retain the existing render, lock-compare, safe-update, customization, and transactional behavior.
4. In a valid self-hosting target, normal upgrade compares protected current bytes with their current lock entries using the applicable integrity schema. It does not compare them for replacement against consumer desired bytes.
5. A protected lock match yields a visible `protected` disposition. Apply preserves current bytes and an equivalent protected digest while allowing unrelated eligible updates.
6. A missing, malformed, untracked, or mismatched protected control yields a blocking diagnostic; apply writes nothing, including the lock.
7. A consumer-template difference is reported as an expected self-hosting boundary. It is never an automatic merge source.
8. `doctor`, preflight, normal upgrade, `reconcile-governor`, and focused tests consume one shared classification and protected-path definition.
9. `harnessctl reconcile-governor TARGET --to VERSION --work-order WO-... [--apply]` is available only for the exact implementation repository, is plan-first, and requires one explicitly selected work order. The work order must pass start preflight and include this specification, its architecture, ADR, and verification contract.
10. The command itself executes from the currently selected checksum-verified released governor outside the checkout. It resolves the exact target version to an immutable published release, full release commit, artifact digest, and data-only migration contract; it never imports or executes target release code.
11. If the current governor does not understand the target migration-contract version or schema jump, reconciliation fails closed and requires a separately published compatible bridge release.
12. The bounded reconciliation set contains `.self-hosting/governor.toml`, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and their deterministic lock metadata. This does not expand the two-file protected set used by normal upgrade.
13. Reconciliation treats TOML as structured data. The target schema declares each field as release-managed, repository identity, or repository policy, together with its migration rule and any safe default.
14. Release-managed fields may be deterministically migrated. Repository identity and policy values are preserved. A new or changed policy field without a safe default yields `decision-required` until an explicit value authorized by the selected work order is supplied.
15. Unknown keys are preserved only when the applicable schema declares an extension namespace. Duplicate keys, ambiguous ownership, lossy conversion, undocumented deletion, or a target request to reinterpret repository policy blocks all writes.
16. Workflow reconciliation selects the target release's self-hosting variant and rejects the consumer variant. Release-managed mechanics are replaced as a whole or through explicitly delimited generated material; no generic YAML merge is allowed.
17. Repository-specific workflow behavior is preserved only through documented inputs or extension points. Changes to triggers, permissions, secrets, environments, deployment authority, required jobs, or trust-plane dependencies require explicit governed decisions; an unrecognized local delta is a conflict.
18. Before apply, reconciliation validates implementation-repository identity, descriptor and release identities, configuration schema, workflow pins, three non-substitutable CI roles, dependency order, runtime isolation, declared permissions, all non-protected managed integrity, and the exact complete write set.
19. Apply stages the descriptor, TOML migration, workflow replacement, and lock update as one recoverable transaction. A failure or interruption cannot leave a mixed target and prior governor state.
20. Reconciliation performs only the mechanics selected by an authorized work order. It emits no approval claim and cannot replace human review, VREC verification, release authorization, publication, or the separate accountable decision to promote the published target.
21. Candidate-source qualification runs the complete candidate suite from the exact checkout and records runtime identity and full commit.
22. Candidate-package qualification installs the exact wheel in a fresh external environment and excludes editable source, checkout search paths, governor packages, and inherited candidate import paths.
23. The black-box functional contract is supplied by the released governor or another immutable verifier artifact selected by that governor, not solely by candidate source.
24. Required functional scenarios cover installation, adoption, validation, visualization, safe and failing upgrades, protected controls, governor reconciliation, schema migration, integrity corruption, origin substitution, determinism, and authority denial.
25. The canonical replay manifest contains schema version, governor and verifier identity, candidate full commit, candidate wheel digest, Python identity, ordered scenario IDs, per-scenario outcome, and canonical output digests. Runtime durations, temporary paths, and wall-clock generation time remain non-canonical.
26. Two equivalent executions over the same retained inputs produce byte-equivalent canonical manifests. Platform-dependent values are normalized or explicitly excluded from equality.
27. A skip, missing scenario, identity ambiguity, nonzero required command, unexpected checkout write, secret-bearing diagnostic, or canonical-manifest disagreement fails acceptance.
28. The new reconciler and verifier implementation remain candidate evidence in their creation release. Only after immutable publication and a separate governor-promotion change may that published release reconcile or govern later candidates.

## Error and recovery behavior

- Classification and integrity errors identify bounded paths and stable diagnostic codes without exposing file bodies.
- Normal upgrade and reconciliation validate their complete write set before staging writes. Reconciliation uses a bounded transaction and recovery marker so descriptor, configuration, workflow, and lock either reach one validated target state or restore the prior state.
- Failure preserves or recoverably restores the prior descriptor, controls, and lock byte-for-byte.
- Acceptance failures retain bounded logs and the incomplete non-authoritative execution summary; they do not emit a success manifest.
- Rerun uses a fresh environment and the same pinned inputs. It never mutates formal artifacts or captured governance records.

## Data and interface contracts

- `harnessctl upgrade` remains backward compatible for consumer targets and adds an observable protected disposition only for the exact implementation repository.
- `harnessctl reconcile-governor TARGET --to VERSION --work-order WO-... [--apply]` is the bounded interface. `VERSION` resolves to an immutable published release identity rather than a mutable tag or local path.
- The target release provides a versioned data-only migration manifest that declares supported source schemas, field ownership, safe defaults, configuration transformations, self-hosting workflow identity, workflow digest, and compatibility protocol. The current governor parses this manifest without importing target modules.
- TOML policy choices that require human input use a bounded, documented reconciliation input contract; shell-shaped free-form interpolation is prohibited.
- Workflow reconciliation consumes the self-hosting variant. Consumer workflow material is never a fallback for the implementation repository.
- The functional runner may be an internal governor module plus a narrow CLI or script. It accepts explicit candidate-wheel and output locations and does not discover authority from the current directory.
- Canonical evidence is UTF-8 JSON with sorted keys and deterministic list ordering. It records identifiers and hashes rather than file bodies.

## Security and privacy properties

- Repository configuration, workflow text, work-order input, package archive, paths, subprocess output, and environment values are untrusted.
- Work-order identifiers are validated as data and never interpolated into a shell command.
- Symlinked targets, path escape, checkout import fallback, user-site substitution, inherited `PYTHONPATH`, entry-point mismatch, mutable target identity, migration-manifest substitution, and workflow-role substitution fail closed.
- Diagnostics allowlist versions, hashes, bounded paths, scenario IDs, and stable codes. Secrets and complete environments are prohibited.
- The candidate cannot supply or rewrite the sole verifier contract used to qualify its package.

## Performance and capacity

- Planning remains linear in the standard template manifest and lock size.
- Reconciliation examines the exact governor descriptor, two protected controls, their accepted baseline and target release data, plus existing managed-integrity entries.
- Functional scenarios use bounded disposable repositories and complete within the existing CI timeout envelope. Performance timings are observations, not canonical acceptance data.

## Observability

- Plan output distinguishes protected self-hosting controls from unchanged consumer-aligned content.
- JSON modes expose classification, per-field ownership and migration dispositions, workflow role, decision requirements, stable diagnostic code, authority source, and canonical hashes.
- CI names and summaries identify `released-governor assessment`, `candidate-source evidence`, and `candidate-package evidence` without relabeling one as another.

## Compatibility and migration

- Existing ordinary installations and their lock behavior remain unchanged.
- The current implementation repository starts with two valid lock-matching controls; the first corrected normal-upgrade plan must change their disposition from `update` to `protected` without changing their bytes.
- Release A implements protection, the data-driven reconciler, role-specific workflow material, and the replayable contract but cannot use its candidate-owned implementation as retroactive independent proof or to rewrite its own controls.
- After Release A is immutably published, a separate approved promotion may select its exact release commit, wheel, and digest using the previously trusted process. Release B and later may use the promoted Release A reconciler and runner.
- Governance-schema changes not understood by the selected governor use a staged compatible bridge release before activation; reconciliation never executes target code to bypass compatibility.

## Examples and counterexamples

- Valid: normal self-hosting upgrade protects the root workflow while safely updating an unrelated managed guide.
- Invalid: normal upgrade overwrites the three-plane workflow because its bytes match the old root lock but not the consumer template.
- Valid: explicit reconciliation preserves repository policy, adds a release-managed TOML property with a safe default, selects the target self-hosting workflow, and updates descriptor, controls, and lock as one planned transaction.
- Invalid: reconciliation silently chooses a value for a new permission-bearing policy field.
- Invalid: reconciliation applies a generic YAML merge or substitutes the consumer workflow for the three-plane self-hosting workflow.
- Valid: a released governor runs its published black-box tests against a future candidate wheel.
- Invalid: a candidate deletes a failing test and treats its reduced candidate-owned suite as independent verification.

## Explicitly unspecified decisions

Implementation may choose internal enum names, stable diagnostic codes, module boundaries, transaction-journal representation, documented reconciliation-input syntax, temporary-directory layout, evidence-schema field names, and whether the functional runner has a public or internal subcommand. It may not expand the normal-upgrade protected set, generically merge YAML, substitute the consumer workflow, infer repository policy, execute target release code during reconciliation, refresh mismatched controls during normal upgrade, let candidate source own the sole verifier contract, weaken exact identities, or activate a candidate reconciler or verifier before separate publication and governor promotion.
