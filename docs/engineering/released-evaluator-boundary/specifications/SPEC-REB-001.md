+++
id = "SPEC-REB-001"
type = "specification"
title = "Locked released-evaluator identity and enforcement"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-REB-001", "REQ-REB-002", "REQ-REB-003", "REQ-REB-004"]
+++

# Specification: Locked released-evaluator identity and enforcement

## Scope

This contract defines the standard-lock evaluator identity, installed-runtime proof, pre-write mutation guard, repository publication resolver, release-readiness evidence binding, and active-surface absence invariant. It applies to one ordinary standard installation; it does not introduce a self-hosting profile or new decision authority.

## Actors and external systems

- Repository operators invoke lifecycle commands from an external released-evaluator environment.
- Candidate-source and candidate-package CI supply adversarial boundary cases but cannot qualify as root authority.
- PyPI or an equivalently approved immutable distribution boundary supplies exact public wheels.
- GitHub Actions executes repository-specific release and release-bound Pages workflows.
- Assurance and release owners review retained identity evidence.

## Inputs

- Resolved target repository root.
- `.engineering-harness.toml` and `.engineering-harness.lock` bytes.
- Invoking runtime version, distribution metadata, module path, template path, Python executable, entry point, isolation flags, user-site state, and `PYTHONPATH` state.
- The installed distribution's canonical payload manifest and, when present, PEP 610 archive hash.
- Operation class: read-only, ordinary installed-root mutation, or standard upgrade apply.
- For publication, an exact trusted governance snapshot and selected release record.
- For release readiness, canonical evaluator identity evidence.

All paths, lock fields, distribution metadata, environment observations, release-record text, downloaded bytes, and workflow inputs are untrusted until validated.

## Outputs

- A deterministic pass/fail evaluator identity report with bounded diagnostic codes.
- A pre-write authorization result consumed only as a technical mutation precondition.
- A standard publication evaluator plan containing version, archive identity, expected digest, and external environment boundary.
- Canonical normalized evaluator identity evidence and its SHA-256 binding.
- Active-surface invariant diagnostics for retired executable contracts.

None of these outputs approves work, verifies a VREC, releases an RLS, publishes, deploys, or exercises an accountable decision.

## State model

An installed repository evaluator identity has one of these technical states:

- `legacy-unbound`: valid schema-2 installation without a standard evaluator payload identity;
- `locked`: standard lock contains a valid evaluator identity;
- `verified`: the current runtime matches the lock and applicable archive proof;
- `transition-planned`: a separately published target evaluator has produced a reviewed standard upgrade plan from a valid old root;
- `rejected`: identity, origin, integrity, or active-surface checks failed.

Ordinary mutation requires `verified`. Upgrade apply requires a valid old-root integrity report plus `transition-planned` for the target released evaluator. Failure never changes state or target bytes.

## Behavioral rules

1. **Standard identity ownership.** Schema 3 of `.engineering-harness.lock` owns an `evaluator` object in addition to managed-file entries. No second descriptor may duplicate this identity.
2. **Payload identity.** Every schema-3 identity contains `version` and `payload_sha256`, where the payload digest is computed over a versioned canonical manifest of installed `se_harness` package files and standard templates. The algorithm and manifest version are explicit constants.
3. **Archive identity.** `archive_name` and `archive_sha256` are optional only as a pair for general consumers. Repository policy requiring release publication makes the pair mandatory. The `se_harness` root and its publication workflows require both.
4. **Runtime proof.** The runtime version, canonical payload digest, distribution root, module, templates, executable, and entry point must agree with one environment. Candidate checkout containment, `PYTHONPATH`, enabled user site, editable source, or unresolved entry point rejects the identity when required by root policy.
5. **Archive proof.** When archive identity is present, the PEP 610 installed archive hash must equal the lock digest, or the operator must supply the exact archive to a verifier that hashes it and proves the installed payload corresponds to it. Caller text alone is insufficient.
6. **Mutation inventory.** The guarded installed-root mutations are `upgrade --apply`, non-dry-run `scaffold-domain`, non-dry-run `create-artifact`, `renumber-artifacts --apply`, `capture-verification`, and `prepare-release`, plus any later command or public API that writes managed controls or formal lifecycle state.
7. **Authoritative placement.** Every public mutation implementation invokes the shared guard internally before its first exclusive create, temporary file, directory creation, replacement, or recovery-state write. CLI-only wrapping is insufficient.
8. **Read-only behavior.** Doctor, validate, inspect, preflight, identity, dashboard generation, dry-run authoring, renumber plan, and upgrade plan remain observations. They may report identity failure but cannot convert it into authority.
9. **Upgrade transition.** A legacy-unbound or older locked root may migrate only through a reviewed standard upgrade driven by an already-published target evaluator outside the checkout. The plan shows lock-schema and identity changes; apply validates old managed integrity and target runtime/archive identity before one recoverable transaction.
10. **Publication resolution.** Repository publication and release-bound Pages workflows read the standard config and lock from the exact governance snapshot, require archive identity, acquire those exact public bytes, verify SHA-256, install outside the snapshot, and invoke `identity --role released-evaluator` with supported option names.
11. **One active vocabulary.** Active runtime APIs and workflow outputs use `evaluator_*`; `governor_*` is permitted only in historical evidence and isolated migration fixtures.
12. **Readiness evidence.** A canonical `se-harness-evaluator-evidence-v1` object records the lock identity and normalized origins relative to `<evaluator-root>` and `<checkout-root>`, plus Boolean isolation, user-site, `PYTHONPATH`, entry-point, and checkout-exclusion results.
13. **Release binding.** `prepare-release` requires passing evaluator evidence when repository policy enables it, revalidates the evidence, hashes its canonical UTF-8 JSON bytes, and writes the repository-relative evidence path and SHA-256 into the ready release record.
14. **Publication replay.** The publisher rechecks the ready/released record's evidence binding and evaluator archive identity before building or promoting candidate distributions.
15. **Active-surface invariant.** Candidate-source and package checks inspect the built package, standard template, active root workflows, active repository scripts, and CLI help for retired executable self-hosting contracts. Historical paths are allowed only through an explicit closed allowlist.
16. **Zero-write failure.** Every guard failure occurs before mutation. Tests compare recursive target snapshots, including absent paths and recovery files, before and after every negative case.

## Error and recovery behavior

- Identity errors name a stable code, failed subject, and bounded message without dumping environment data.
- Missing standard archive identity in a publication-enabled root instructs maintainers to perform a separately governed evaluator-identity upgrade; it never reconstructs a digest from an arbitrary candidate.
- A failed upgrade plan or apply preserves the old lock and managed content through the existing recoverable transaction.
- A partial or inconsistent schema-3 identity is an integrity error, not legacy compatibility.
- Publication failure stops before credential-bearing jobs and Pages deployment.

## Data and interface contracts

The standard lock extension is:

```json
{
  "schema": 3,
  "tool_version": "0.5.1",
  "evaluator": {
    "version": "0.5.1",
    "payload_manifest": "se-harness-installed-payload-v1",
    "payload_sha256": "<lowercase-sha256>",
    "archive_name": "se_harness-0.5.1-py3-none-any.whl",
    "archive_sha256": "<lowercase-sha256>"
  },
  "files": {}
}
```

`archive_name` and `archive_sha256` are either both absent or both valid. When present, the archive name is a safe basename matching normalized project name, selected version, and supported wheel tag. Unknown evaluator fields fail closed.

The canonical evidence object contains only schema, role, evaluator identity, normalized origins, bounded Boolean environment checks, target object format when relevant, and ordered diagnostics. Absolute host prefixes, environment values, credentials, and repository contents are excluded.

## Security and privacy properties

- Identity proof uses independently selected expected values and verified bytes; candidate claims are not trusted.
- Path containment uses resolved and lexical checks appropriate to symlink and virtual-environment launcher behavior.
- Digest comparison is constant-form lowercase SHA-256 and rejects duplicate JSON keys or unknown security-critical fields.
- Download precedes credential availability; digest verification precedes installation; evaluator validation precedes candidate promotion.
- Diagnostics and retained evidence reveal no secrets, tokens, arbitrary environment variables, or personal absolute paths.

## Performance and capacity

- The canonical payload digest scans only installed package and template files listed by the bounded manifest and must remain below existing candidate-acceptance file and byte budgets.
- One identity check per mutating command and workflow job is sufficient; repeated file hashing inside one operation is avoided by an immutable in-process result.
- Evidence JSON remains below 64 KiB.

## Observability

Human and JSON output identify role, version, archive digest, normalized origins, pass/fail status, diagnostic codes, and the target operation. Workflow summaries retain the evaluator evidence digest and never describe it as approval.

## Compatibility and migration

- Schema-1 and schema-2 locks remain readable for doctor, validation, inspection, and a separately governed upgrade plan.
- Ordinary lifecycle mutation from `legacy-unbound` is rejected after the enforcing release, except the single standard upgrade apply that establishes schema 3 from an exact external published evaluator.
- Existing consumer repositories retain owner content and managed-marker behavior; migration changes only the standard lock and managed files in the reviewed plan.
- Historical release and verification records are never rewritten to add evaluator evidence.
- Windows, Linux, and macOS path and launcher behavior receive deterministic coverage.

## Examples and counterexamples

- **Conforming:** download official wheel, verify expected SHA-256, install the local wheel in an external environment, prove PEP 610/archive and payload identity, then create a draft artifact.
- **Conforming:** run a read-only upgrade plan from an external target evaluator against a schema-2 root, review the identity migration, then separately authorize apply.
- **Non-conforming:** run candidate source with the same `__version__` and pass the official digest as text.
- **Non-conforming:** publish using `.self-hosting/governor.toml`, `--role governor`, or an unverified `pip install se-harness==VERSION` result.
- **Non-conforming:** bind absolute temporary-directory paths into a permanent RLS.

## Explicitly unspecified decisions

- Internal helper and dataclass names.
- Whether the payload manifest is materialized as a file or generated deterministically from installed metadata.
- Exact diagnostic code numbers, provided they are stable and separately testable.
- Workflow step names and temporary-directory layout.
