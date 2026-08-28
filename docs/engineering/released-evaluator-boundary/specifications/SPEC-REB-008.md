+++
id = "SPEC-REB-008"
type = "specification"
title = "Governance migration contract and rehearsal protocol"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
specifies = ["REQ-REB-016", "REQ-REB-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "technical-owner"
+++

# Specification: Governance migration contract and rehearsal protocol

## Retirement amendment of 2026-08-28

Retired on 2026-08-28 under `WO-ECP-010` (`REQ-ECP-012`, `SPEC-ECP-007` `ECP-PRD-008`), together with `REQ-REB-016` and `REQ-REB-017` which it specified, on the repository owner's approval for issue #210. The contract schema `se-harness-governance-migration-v1`, the closed stage and role catalogs, the scenario format and its digests, `harnessctl rehearse-migration`, and the `MIG` diagnostic family are withdrawn from the product; the names are reserved and never reused. The rules below are retained as history of what 0.6.0 and 0.7.x rehearsed; the one retained property, that the released predecessor governs the root until a separately authorized adoption, is enforced by `mutation_guard` and the lock and is now exercised by the real upgrade rehearsal.


## Scope

This specification defines a versioned machine-readable contract and a read-only/disposable runner for proving how released evaluator N-1 governs a successor N that introduces incompatible governance behavior. It covers classification, preparation, complete successor validation, rejected-proposal retention, corrected succession, hosted assessment, release/publication planning, rendering, and later standard-root adoption.

The contract is generic. The first mandatory regression fixture reproduces the material 0.5.0-to-0.6.0 boundaries without modifying historical release records or treating release-specific corrective adapters as universal policy.

## Actors and external systems

- **Released predecessor:** the exact independently released evaluator selected by the starting root.
- **Successor candidate:** exact source or a non-promotable candidate package that may validate successor behavior and produce evidence only.
- **Accountable decision fixture:** immutable test input replaying an already attributed approval, rejection, verification, release, publication, or upgrade decision; it is not an automated decision.
- **Migration runner:** unprivileged orchestrator that validates the contract, creates disposable state, invokes isolated actors, enforces stage boundaries, and writes one factual result.
- **Current complete-graph validator:** validates all artifacts under successor semantics without replacing predecessor authority.
- **Compatibility adapter:** optional exact read-only view or translation declared by identity for one stage.
- **Publication and rendering planners:** resolve inputs and render disposable output without credentials or external mutation.
- **Upgrade simulator:** exercises the ordinary separately governed root-upgrade transaction only after simulated immutable publication.

## Inputs

1. A canonical `se-harness-governance-migration-v1` scenario document.
2. A disposable repository fixture identified by a complete content digest.
3. Exact local predecessor interpreter, entry point, version, payload manifest digest, and archive digest when archive identity is required.
4. Exact local successor interpreter or candidate package, version, candidate commit/tree or package digest, and checkout-exclusion observation.
5. Every selected adapter identified by contract ID, implementation digest, input view rule, and permitted stage.
6. Immutable decision fixtures containing decision type, artifact ID, accountable role, timestamp, and exact permitted effect.
7. A new absent or empty output directory outside the operational source checkout.

All paths, packages, manifests, repository bytes, decision fixtures, process reports, Git data, and environment values are untrusted until validated.

## Outputs

The runner writes canonical UTF-8/LF JSON with schema `se-harness-governance-migration-result-v1`. It records:

- scenario and contract digests;
- exact predecessor, successor, fixture, adapter, commit/tree, and package identities;
- compatibility classification and affected operations;
- one ordered result per required stage, including evaluator role, input-view digest, command identity, decision fixture if applicable, permitted and observed mutations, authority effect, report digest, duration, and result;
- before/after digests for the operational source, disposable root, formal graph, evaluator selection, and simulated external state;
- the final selected evaluator in the disposable root;
- explicit false values for credential use and real tag, publication, maintenance, deployment, lifecycle, or root mutation outside the fixture;
- overall pass/fail and the first failed stage.

## State model

```text
contract validated
  -> predecessor prepares
  -> successor validates complete graph read-only
  -> attributed rejection fixture is replayed
  -> corrected successor replaces active proposal, not history
  -> predecessor/successor assessment claims are checked
  -> release and publication are planned read-only
  -> exact governance snapshot is rendered
  -> simulated immutable successor publication exists
  -> separate disposable root upgrade is planned/applied
  -> standard controls and final identities are reconciled
```

Every arrow is fail-closed. No later stage runs after a failure. Before the explicit final upgrade, the selected root evaluator remains the predecessor.

## Behavioral rules

1. **Compatibility classification.** Compare the predecessor contract capabilities with the successor-required operations. A missing operation, schema, state, evidence form, or rendering behavior yields `migration-required`; uncertainty never yields `compatible`.
2. **Closed stage catalog.** A conforming scenario contains exactly these stage IDs in order: `prepare`, `validate-complete`, `reject`, `replace`, `assess`, `release-plan`, `publish-plan`, `render`, and `adopt`.
3. **Closed role catalog.** Each stage selects one declared technical role and, where a decision is replayed, one separately declared accountable role. Technical execution cannot satisfy a missing decision fixture.
4. **Exact identities.** Resolve predecessor and successor outside the target checkout. Require versions, payload identities, archive identities when configured, entry points, environment isolation, and checkout exclusion before stage execution.
5. **Predecessor preparation.** The preparation stage runs with the released predecessor or an explicitly declared predecessor-compatible preparation adapter. Its output and mutation set are exact and bounded to the disposable fixture.
6. **Complete successor claim.** Successor validation runs against the complete fixture graph, is read-only, and cannot change root evaluator selection or lifecycle state.
7. **Rejection semantics.** Rejection is applied only from an exact accountable fixture. The rejected tuple remains immutable, terminal, visible, non-authoritative, and unavailable for later reuse.
8. **Corrected succession.** Replacement creates a distinct proposal, preserves rejected history, and proves that rejected records neither reserve active version authority nor satisfy active gates.
9. **Assessment claims.** Complete successor validation and any predecessor-compatible view claim are recorded separately. A compatibility view is derived from declared evidence, hash-bound, read-only, and never described as complete predecessor validation.
10. **Planning only.** Release and publication stages may resolve and validate candidate, record, tag name, distribution, maintenance, and rendering inputs. They cannot create or move refs, releases, packages, environments, deployments, or lifecycle state.
11. **Rendering identity.** Rendering uses the evaluator/view pair declared for the selected governance snapshot and verifies that links and selected release facts refer to the corrected proposal.
12. **Adoption separation.** Adoption requires a distinct decision fixture and a simulated immutable public successor identity. It uses the ordinary upgrade transaction, proves rollback and no-op replay, and is the only stage allowed to change evaluator selection in the disposable root.
13. **Source immutability.** Snapshot the operational checkout and Git refs before and after the run. Any source, history, ref, lock, configuration, or tracked-byte change outside the disposable fixture fails the run.
14. **Credential and network boundary.** Strip credential-bearing environment variables. The core runner opens no network connection. Hosted acquisition of a public predecessor is an earlier unprivileged digest-verifying step and is outside runner execution.
15. **No diagnostic waiver.** Success depends on structured zero-error or explicitly modeled negative-stage results. Substring allowlists, ignored exit codes, caller-supplied omissions, and `continue-on-error` success conversion are prohibited.
16. **Determinism and replay.** Set-like values are sorted, paths are logical and host-normalized, volatile times are excluded from the result digest, and repeated runs from identical inputs produce the same semantic result and digest.

## Error and recovery behavior

Contract syntax, unknown fields, duplicate stages, invalid order, missing identities, linked/escaped paths, mutable input, environment contamination, unexpected mutation, malformed report, timeout, cleanup ambiguity, or result disagreement fails with a stable stage/code diagnostic. The runner attempts cleanup only within its disposable directory and retains the bounded failure report. It never tries an alternate evaluator, inferred adapter, reduced graph, ignored diagnostic, or operational repair.

## Data and interface contracts

The candidate provides one read-only command:

```text
harnessctl rehearse-migration <operational-root>
  --scenario <canonical-json>
  --predecessor-python <external-python>
  --successor-python <external-python>
  --output <external-absent-directory>
  [--json]
```

The scenario may identify adapters and fixture-relative inputs but may not provide accepted diagnostics, arbitrary omissions, credential names, operational output paths, or authority overrides. The CLI is an evidence producer and never mutates the operational root.

The packaged contract document defines closed schemas, stage IDs, role IDs, required identity fields, required result fields, and authority/non-authority statements. Package-data and source-contract conformance tests require byte-identical contract availability in source and built wheels.

## Security and privacy properties

- Reject symlink/junction/path escapes, alternate Git state, current-directory imports, editable/candidate substitution for the predecessor, user-site or `PYTHONPATH` contamination, executable replacement, decision-fixture tampering, and adapter-digest mismatch.
- Child processes receive a minimal environment with no known credential variables and bounded time/output.
- Permanent output contains no usernames, home paths, temporary absolute paths, tokens, environment dumps, or repository body content.
- The runner has no mechanism to approve, verify, release, publish, deploy, adopt, or waive a failure.

## Performance and capacity

The hermetic fixture must complete within the existing candidate CI budget on supported Windows and Linux runners. Each child process has a declared timeout and output ceiling. Contract validation is linear in stages and declared artifacts; snapshot work is linear in fixture size.

## Observability

Human output names the current stage, technical actor, target view, result, and first failure. JSON retains all structured identities and proofs. Failure evidence is written even when a child command fails, and later stages are explicitly marked `not-run`.

## Compatibility and migration

- The first scenario preserves exact 0.5.0 and 0.6.0 historical facts while running only on disposable copies and already public/local package bytes.
- Existing recovery rehearsal remains for emergency deadlock restoration; normal migration rehearsal is a separate command and contract.
- Existing predecessor preparation, assessment, publication-view, rendering, and upgrade components may be adapted behind typed stage interfaces without changing their production behavior.
- Future successors add scenario data or a new versioned contract when semantics change; they do not edit completed historical scenarios.

## Examples and counterexamples

- **Conforming:** N-1 prepares a legacy-compatible proposal, N validates the full graph, a fixture-attributed rejection is retained, a distinct corrected proposal succeeds, and N is adopted only after simulated immutable publication and a separate upgrade fixture.
- **Conforming:** predecessor validation uses an exact evidence-bound view while successor validation independently covers the complete graph; both claims are named honestly.
- **Non-conforming:** candidate N runs root lifecycle mutations because it knows the new schema.
- **Non-conforming:** the runner removes files until N-1 passes without a declared view contract and digest.
- **Non-conforming:** a successful rehearsal tags a commit, uploads a package, changes the operational root lock, or treats a fixture as a real human decision.

## Explicitly unspecified decisions

- Python module, class, helper, and stable diagnostic suffix names.
- Internal temporary directory names and process-wrapper decomposition.
- Whether hermetic stage fixtures use subprocess shims or minimal local packages, provided the exact historical hosted lane uses the declared real predecessor and successor identities.
