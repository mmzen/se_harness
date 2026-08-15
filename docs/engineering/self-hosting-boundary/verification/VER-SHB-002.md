+++
id = "VER-SHB-002"
type = "verification"
title = "Verify protected upgrade, governor reconciliation, and replayable acceptance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
+++

# Verification Contract: Verify protected upgrade, governor reconciliation, and replayable acceptance

## Independence

Expected protected paths, classification, field ownership, workflow role, target identity, authority sources, scenario categories, and failure behavior derive from the approved SHB requirements and specification. Tests must not infer correctness from implementation action names, accept candidate-owned tests as the sole package oracle, execute target code as its own migration authority, or use a newly implemented reconciler or runner as retroactive independent evidence for its own candidate.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-SHB-007` | planner/apply property tests, lock snapshots, static dependency inspection, CLI integration | consumer target, current implementation repository, schema-1/2 locks, missing and modified controls, malformed identity, mixed protected and ordinary updates | consumer semantics remain unchanged; valid self-hosting controls are visibly preserved; every ambiguity or mismatch blocks all writes; one shared policy owns the exact two paths |
| `REQ-SHB-008` | verifier-owned functional runner, source and wheel origin tests, deterministic replay, negative authority fixtures | exact source commit, exact wheel digest, fresh Python 3.11 environments, required command matrix, omitted/weakened candidate tests, path substitution, two-release activation | all required scenarios execute from the declared role; candidate cannot supply the sole oracle; canonical manifests replay identically; no candidate result claims verification, release, publication, or promotion |
| `REQ-SHB-009` | reconciliation protocol fixtures, TOML migration properties, workflow-role snapshots, transaction fault injection, CLI integration, manual authority review | exact published targets, mutable or corrupt targets, safe and decision-required fields, extension namespaces, schema jumps, consumer/self-hosting variants, local YAML deltas, permission changes, bridge release, interrupted apply | current governor consumes only verified target data; repository policy survives; unsafe decisions and incompatible migrations block; the self-hosting workflow is selected; descriptor, controls, and lock reach one consistent state or restore the prior state |

## Acceptance scenarios

- Current root plan changes `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` from erroneous `update` actions to `protected`, with no byte change.
- A safe unrelated managed-template change can apply while both controls remain protected.
- A customized or missing protected control blocks the entire apply and preserves the prior lock.
- A consumer initialized from the standard template remains idempotent and upgrades its workflow when the locked prior baseline is unchanged.
- Consumer workflow customization remains preserved and blocks transactional apply.
- A safe TOML schema addition preserves every repository policy and identity value, adds only the declared safe default, advances the schema, and updates exact integrity evidence.
- A new policy or permission without a safe default produces a blocking `decision-required` disposition until an explicit governed value is supplied.
- The current released governor resolves an exact published target and parses its data-only migration contract without importing or executing target modules.
- Reconciliation rejects a mutable tag-only identity, corrupt asset, unsupported migration protocol, lossy schema jump, unknown key outside an extension namespace, duplicate key, or ambiguous field ownership.
- The implementation repository selects the target self-hosting workflow. Consumer variant substitution, generic YAML merge, unrecognized local workflow delta, missing three-plane job, invalid dependency, or undeclared permission change blocks reconciliation.
- Successful apply updates the authorized governor descriptor, configuration, workflow, and matching lock metadata as one consistent set. Fault injection at every replacement boundary restores or recoverably completes the prior or target state without a mixed-governor result.
- Non-protected managed mismatch blocks reconciliation.
- Candidate source runs the complete suite from the exact checkout; candidate package runs the required black-box contract from the exact installed wheel outside the checkout.
- The released contract still runs a required scenario removed from candidate-owned tests.
- Two equivalent black-box runs produce equal canonical evidence manifests and distinct non-canonical timing summaries.
- A candidate runner is labelled candidate evidence until its published wheel is separately selected as governor.

## Property and invariant tests

- Self-hosting classification is deterministic and tri-state; untrusted repository content cannot expand the protected set.
- Protected files and prior lock bytes are identical after every failed normal upgrade. Failed reconciliation preserves or recoverably restores the complete prior descriptor/control/lock set.
- Normal upgrade never converts a protected mismatch into a new digest.
- For every supported schema, migrating the same accepted input to the same immutable target and explicit policy choices yields byte-equivalent TOML, workflow, descriptor, plan, and lock output.
- Release-managed field changes cannot alter repository-policy or identity values; safe-default insertion cannot occur for a decision-required field.
- Workflow reconciliation has exactly one role result and can never map an implementation repository to the consumer variant.
- Reordering template enumeration, lock keys, scenarios, or environment observations does not change canonical decisions.
- Consumer results match the pre-change behavior for unchanged, safe-update, customized, missing, and newline-equivalent cases.
- Runtime identity is component-aware and rejects checkout, environment, user-site, symlink, case, entry-point, and version-only substitutions.
- Every required scenario appears exactly once in the canonical manifest and has one terminal outcome.
- Candidate, governor, and verifier digests are complete lowercase SHA-256 values and candidate commit length matches the repository object format.

## Static and architecture checks

- The shared self-hosting policy has no installer, CLI, preflight, Git, or governance dependency.
- Installer, doctor, preflight, reconciler, and tests import the shared protected-path definition rather than copying it.
- The standard workflow template remains the sole consumer workflow source; the root three-plane workflow remains repository-specific and hash-locked.
- Normal upgrade contains no path that writes protected desired consumer bytes in self-hosting mode.
- The target migration reader has no import or execution path into the target wheel or checkout and accepts only the versioned data contract supported by the current governor.
- TOML migration uses the schema ownership registry rather than hard-coded preservation scattered across CLI or installer modules.
- Workflow reconciliation can select only the published self-hosting variant for the implementation repository and contains no generic YAML merge fallback.
- Reconciliation write construction rejects every destination except `.self-hosting/governor.toml`, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, bounded transaction metadata, and `.engineering-harness.lock`.
- The functional runner invokes candidate package behavior through the installed environment and never imports candidate modules into the governor process.

## Security and privacy checks

- Exercise malicious TOML and YAML, partial role declarations, spoofed package name/layout, mutable releases, invalid descriptors and migration manifests, duplicate keys, traversal paths, symlinked controls, untrusted work-order and policy strings, shell-shaped values, hostile subprocess output, and secret-bearing environments.
- Confirm an adversarial target cannot cause its code to load, select the consumer workflow, expand destinations, reinterpret repository policy, weaken permissions review, or write a digest for bytes not staged by the transaction.
- Confirm failures are bounded, stable, credential-free, and contain no file bodies or complete environment dumps.
- Confirm candidate-controlled output cannot inject canonical scenario results or authority labels.
- Confirm package archives and runtime origins are checked before executing candidate entry points.

## Performance and resilience checks

- Planner and reconciliation remain bounded by manifest, schema, workflow, and lock size and do not scan generated or dependency trees.
- Functional acceptance uses bounded fixtures, deterministic timeouts, fresh cleanup, and no mutable network dependency after pinned artifacts are acquired.
- Interrupted writes and recovery tests at every boundary leave a complete prior or complete target control set; a rerun from the same inputs reaches the same canonical result.

## Manual assessments

- Review whether any candidate-controlled executable or test is still presented as released-governor assessment.
- Confirm the two-file exception remains specific to developing `se-harness` and does not become a public profile.
- Confirm protected status does not hide drift: lock mismatch remains blocking and consumer-template divergence remains visible.
- Review the reconciliation command's authority wording, current-versus-target trust direction, exact write scope, field ownership, safe defaults, decision inputs, workflow extension boundary, and recovery behavior.
- Confirm that actual governor promotion remains separately accountable even though the command performs its authorized file mechanics.
- Challenge whether the replay manifest contains enough retained information for an independent rerun without leaking secrets.
- Confirm Release A and later governor promotion are described as separate decisions and records.

## Evidence retention

Retain exact source and package commits, current and target governor identities and hashes, target migration-contract and workflow digests, test-contract identity, planner JSON, field-ownership and decision matrices, descriptor/control/lock before-and-after bytes and digests, transaction fault snapshots and recovery results, reconciliation plans, runtime origins, scenario manifests, deterministic output hashes, test counts, runtimes, workflow results, deviations, and residual risks under `docs/engineering/self-hosting-boundary/evidence/WO-SHB-002-verification.md`.

## Residual uncertainty

Static and local fixtures cannot prove future GitHub runner behavior, every Python distribution layout, or every governance-schema evolution. GitHub CI, fresh Python 3.11 package acceptance, retained replay inputs, and post-publication governor-promotion evidence remain required before the new runner can act as an independent governor contract.
