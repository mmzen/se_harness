+++
id = "SPEC-REB-003"
type = "specification"
title = "Contract-bound predecessor evaluator bootstrap"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-REB-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "technical-owner"
+++

# Specification: Contract-bound predecessor evaluator bootstrap

## Scope

This contract defines one transition mechanism for the release that first ships schema-3 evaluator-evidence enforcement while its repository is still authoritatively governed by released 0.5.0 and a schema-2 lock. It adds a repository-owned evidence binder and narrow validator/publication resolution. It does not change the operational root, create a second installation profile, or make candidate code an evaluator.

## Actors and external systems

- The released 0.5.0 evaluator prepares and validates the ready RLS from outside the checkout.
- A repository-owned binder records a bounded observation of that evaluator after verifying exact public wheel bytes.
- Candidate validator and publication resolver enforce the approved bootstrap contract.
- Assurance and release owners separately decide VREC and RLS lifecycle transitions.
- GitHub and PyPI supply immutable public 0.5.0 bytes and later perform external promotion only after separate authorization.

## Inputs

- One active approved release contract with a `[bootstrap]` table.
- Exact root `.engineering-harness.toml` and raw `.engineering-harness.lock` bytes.
- A `ready` RLS created by the predecessor evaluator.
- The exact public predecessor wheel and its external installation.
- Released-evaluator identity JSON, candidate identity, aggregate VREC, work-set relations, distribution bundle, and repository Git state.

All paths, TOML, JSON, Git content, wheel bytes, distribution metadata, environment observations, and workflow inputs are untrusted.

## Outputs

- One canonical evaluator-evidence sidecar below `docs/engineering/**/evidence/`.
- An RLS binding containing `evaluator_evidence_path`, `evaluator_evidence_sha256`, and `preparation_schema = "se-harness-predecessor-bootstrap-v1"`.
- Deterministic candidate-validation and publication-resolution results.
- Retained zero-write diagnostics on every rejected case.

No output approves, verifies, releases, commits, tags, publishes, deploys, or upgrades the root.

## State model

```text
undeclared
  -> contract-declared
  -> predecessor-prepared-ready
  -> canonical-evidence-bound
  -> dual-validator-ready
  -> separately decided release
```

Every transition through `canonical-evidence-bound` is preparatory. Only the release owner's later lifecycle decision can enter the final state.

## Behavioral rules

1. **Closed declaration.** Bootstrap behavior is disabled unless the selected active `release_contract` is approved and declares every field in `se-harness-release-bootstrap-v1`.
2. **Exact cardinality.** The contract declares exactly one release-record ID and one target version. No prefix, glob, branch, current-date, or “latest” selection is permitted.
3. **Old-root binding.** The contract declares `from_lock_schema = 2`, `from_lock_tool_version`, and the lowercase SHA-256 of the lock's canonical `utf8-text-lf-v1` bytes. Config version, lock version, lock schema, and canonical digest must all agree at binding and publication resolution. CRLF and LF serialization of identical UTF-8 lock content therefore have one identity; any other content change fails.
4. **Public evaluator binding.** The contract declares predecessor version, safe wheel basename, and wheel SHA-256. The binder and publisher hash exact acquired bytes before installation or evidence use.
5. **Predecessor authority.** The RLS must already exist as `ready`, have been prepared through the exact external predecessor `prepare-release`, and pass predecessor validation. The binder cannot create the RLS.
6. **Immutable captured facts.** Binding cannot change RLS ID, type, status, owners, version, candidate, object format, tag value, release contract, included VRECs, released-work set, legacy preparation timestamp/actor, body bytes, or lifecycle events.
7. **Preparation marker.** The binder adds the exact preparation schema marker. While status is `ready`, legacy `released_at` and `authorized_by` are interpreted only as predecessor preparation facts when this marker and contract validation pass; they do not represent a release decision.
8. **Canonical evidence.** Evidence uses the existing strict schema, complete predecessor archive identity, installed-payload digest derived from exact public bytes and installed files, normalized evaluator-root origins, isolated Python, disabled user site, absent `PYTHONPATH`, resolved predecessor entry point, checkout exclusion, and no diagnostics.
9. **Atomic binding.** The sidecar exclusive-create and RLS binding update form one rollback-capable transaction. Failure leaves the RLS and evidence destination exactly as observed before the attempt.
10. **No generic exception.** Normal ready RLS validation continues to require schema-3 current-lock equality. A bootstrap record still requires evidence and qualifies only through exact contract, lock, evaluator, record, version, status, and preparation-schema equality.
11. **Released-history behavior.** After a separately authorized release transition, the retained predecessor evidence remains bound. Later schema-3 root upgrades do not require it to match the new current lock.
12. **Publication resolution.** Only for the declared bootstrap RLS, publication resolves the predecessor evaluator from the approved contract, rechecks the canonical schema-2 lock and evidence at the governance commit, reacquires exact public wheel bytes, and validates externally before build or credentials.
13. **Candidate separation.** Candidate source/package may implement the binder and checks but cannot satisfy the evidence role, supply expected evaluator digests from runtime claims, execute root lifecycle mutations, or replace predecessor validation.
14. **One-shot terminality.** After the declared RLS becomes released or rejected, the same contract cannot authorize a second record or a different candidate. Re-execution is idempotent only for identical bytes.
15. **Promotion agreement.** Candidate commit, aggregate VREC, RLS, release contract, work set, version, tag, bundle, distribution hashes, and hosted candidate evidence must agree before promotion.
16. **Zero-write rejection.** Binder, validator, and publisher negative cases stop before target mutation, root mutation, branch/tag mutation, or credential-bearing work.

## Error and recovery behavior

- Contract incompleteness or ambiguity reports a stable bootstrap-policy diagnostic and disables the special path.
- Existing sidecar or partially bound metadata that is not byte-identical fails without overwrite.
- Interrupted binding restores original RLS bytes and removes only a temporary or exclusively created sidecar from that transaction.
- Publication mismatch reports the exact bounded subject and stops before OIDC or write permissions.
- A change to candidate source after aggregate capture invalidates the candidate and requires a new VREC/RLS sequence; it never repoints records.

## Data and interface contracts

The replacement release contract declares:

```toml
[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-SEH-009"
version = "0.6.0"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"
```

Unknown, missing, duplicate, incorrectly typed, unsafe, noncanonical, or extra bootstrap fields fail closed. The RLS binds the ordinary canonical evidence fields plus `preparation_schema`; no alternate evidence schema or absolute path is introduced.

The repository-owned binder's exact CLI spelling is delegated, but it must require explicit repository, release-record, release-contract, public-wheel, evaluator-interpreter/entry-point, and apply intent. Its plan mode is read-only, and apply prints exact changed destinations and digests.

## Security and privacy properties

- Expected lock and archive identities come from an approved formal contract, not candidate runtime output.
- The public wheel is hashed before use; installed files and origins are independently reconciled.
- Evidence contains normalized bounded origins and Boolean environment facts only—no usernames, home paths, tokens, environment dumps, or repository bodies.
- The binder rejects symlinks, traversal, case ambiguity, existing nonidentical files, current-directory import, editable installs, and cross-environment entry points.
- Publication acquires and validates evaluator bytes before credentials or external writes.

## Performance and capacity

Binding scans only the bounded public wheel and installed package/template payload. Evidence remains below 64 KiB. Negative cases and full integration remain within existing release qualification timeouts.

## Observability

Human and JSON output name the bootstrap schema, contract, RLS, old-lock digest, evaluator archive digest, candidate, evidence digest, pass/fail result, and whether any write occurred. They never describe technical success as approval or release.

## Compatibility and migration

- Released 0.5.0 retains operational authority and its installed root remains byte-identical.
- Existing historical releases and their allowlist are unchanged.
- The current stopped C/VREC/RLS chain remains historical evidence and is not repointed.
- After 0.6.0 publication, a separate approved upgrade may establish schema 3 from the exact public 0.6.0 evaluator.
- Every ordinary 0.6.0 consumer and every later release uses the normal schema-3 evidence rule.

## Examples and counterexamples

- **Conforming:** 0.5.0 prepares `RLS-SEH-009`; the binder verifies the declared lock and public 0.5.0 wheel, binds canonical evidence atomically, and both validators pass.
- **Conforming:** after release and later root upgrade, the historical RLS retains 0.5.0 evidence while new ready records match the 0.6.0 schema-3 lock.
- **Non-conforming:** add `RLS-SEH-009` to the missing-evidence allowlist.
- **Non-conforming:** accept any schema-2 lock whose tool version merely says `0.5.0`.
- **Non-conforming:** run candidate `prepare-release` or candidate identity as the root evaluator.
- **Non-conforming:** derive expected archive identity from the sidecar being validated.

## Explicitly unspecified decisions

- Internal helper, dataclass, and stable diagnostic suffix names.
- Temporary-file naming and rollback-journal representation.
- Whether public-wheel payload comparison streams directly or uses a bounded temporary extraction.
- Human-readable table layout, provided JSON and exit behavior remain deterministic.

## Canonical-LF correction

On 2026-08-21 at `2026-08-21T16:31:42Z`, the accountable owners authorized replacing the platform-smudged CRLF observation with canonical `utf8-text-lf-v1` SHA-256 `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`. This correction preserves approved status, the closed tuple, trust direction, mutation boundary, and all other scope constraints.
