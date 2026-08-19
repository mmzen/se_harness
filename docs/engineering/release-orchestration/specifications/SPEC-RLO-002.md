+++
id = "SPEC-RLO-002"
type = "specification"
title = "Portable release-governance boundary contract"
status = "approved"
owners = ["engineering-owner", "release-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
specifies = ["REQ-RLO-009", "REQ-RLO-010", "REQ-RLO-011"]
+++

# Specification: Portable release-governance boundary contract

## Scope

Correct the RLO-001 implementation boundary without changing its authorized one-input publication outcome. Portable SE Harness prepares and validates format-neutral release authority. The `se_harness` repository separately owns its Python distribution manifest, RLS extension, publication workflow, and channel recovery policy.

This specification refines the responsibility split in `SPEC-RLO-001`; it does not rewrite that verified historical artifact. Where `SPEC-RLO-001` assigns Python distribution parsing to `harnessctl`, this newer contract assigns it to repository-owned tooling.

## Actors and external systems

- Coding agents use generic `harnessctl prepare-release` to prepare core RLS governance.
- Release maintainers use repository-owned scripts to build, validate, and bind SE Harness distribution identity.
- The released governor validates portable artifact structure and lifecycle rules without interpreting repository publication formats.
- Trusted-main GitHub Actions validates the repository distribution extension before GitHub, PyPI, or Pages mutation.
- Accountable assurance and release owners retain all verification and release decisions.

## Inputs

- Generic preparation: RLS ID, release contract, eligible VRECs, exact work orders, version, authorized role, optional tag, domain, and output path.
- Repository binding: path to one uncommitted `ready` RLS and one `se-harness-release-bundle/v1` JSON manifest.
- Publication: exactly one released RLS ID selected from `main`, unchanged from `SPEC-RLO-001`.

## Outputs

- A generic ready RLS containing only core release-governance fields and relations.
- After repository binding, the same ready RLS plus a complete repository-owned `[distribution]` table.
- The existing canonical release plan, qualified byte bundle, GitHub Release, PyPI files, Pages demonstration, and stage-specific result document.

## State model

1. **Core prepared:** generic `harnessctl` creates a ready RLS with no package assumptions.
2. **Bundle retained:** repository build tooling emits one exact candidate bundle manifest.
3. **Distribution bound:** repository tooling atomically validates and adds the complete distribution table without changing core fields or status.
4. **Release decided:** an accountable owner may later transition the RLS through the existing governed process.
5. **Publication resolved:** trusted-main repository tooling validates the released RLS and its distribution extension before qualification or credentials.

A record at state 1 remains a valid generic RLS but is not sufficient input for the `se_harness` publication workflow.

## Behavioral rules

1. `harnessctl prepare-release` must retain its current core commit, VREC, work-coverage, release-contract, owner, version, tag, domain, path-safety, and all-or-none write checks.
2. The portable CLI and Python API must remove `--distribution-manifest` and its corresponding parameter and code path.
3. The packaged `se_harness*` namespace, managed validator, and standard consumer templates must contain no `se_harness` wheel/sdist, `python-wheel-sdist`, `SHA256SUMS`, PyPI, Pages, or repository publication semantics.
4. Portable validation must continue validating the complete core RLS and must not present repository metadata as core-assessed provenance.
5. One repository-owned standard-library implementation must define the existing bundle and distribution schemas for all SE Harness build, bind, resolve, and test paths.
6. Repository distribution tooling must be excluded from the wheel and standard consumer installation.
7. The binder must require an existing ready RLS, validate its candidate, object format, version, and candidate commit epoch against the manifest, and preserve all pre-existing core bytes except the insertion of the complete distribution table.
8. Binder validation and replacement must be atomic. Existing distribution metadata is accepted only as an exact replay; partial or conflicting state blocks.
9. The repository-specific distribution table retains schema 1 and kind `python-wheel-sdist` so the current orchestrator and retained evidence do not need a format migration.
10. The trusted-main resolver must import only repository-owned distribution logic, require the complete table for publication, and reject missing or invalid identity before candidate execution or external mutation.
11. The normal workflow must continue accepting only `release_record`, deriving every other identity, and preserving credential-free qualification and separate GitHub, PyPI, and Pages permissions.
12. Historical and consumer RLS files without a distribution table remain valid. No historical artifact, VREC, RLS, tag, release, or evidence is rewritten.
13. Standard installation and upgrade must remove the leaked template and validator behavior transactionally when the managed files are unmodified, while continuing to block customized destinations.
14. This correction must not introduce a plugin system, general payload framework, new installation profile, new runtime dependency, or support for additional packaging ecosystems.
15. No command or workflow change may approve, verify, release, commit, push, merge, tag, publish, deploy, or approve an environment without separate authority.

## Error and recovery behavior

| Condition | Required behavior |
|---|---|
| Generic RLS inputs invalid | `harnessctl prepare-release` fails without an output record |
| Repository manifest invalid or mismatched | binder fails and leaves the ready RLS byte-for-byte unchanged |
| Distribution table already exact | binder reports an exact replay without changing identity or status |
| Distribution table partial or conflicting | binder fails; no replacement or normalization |
| Released RLS lacks repository distribution provenance | publication resolver blocks before candidate execution and credentials |
| Consumer repository uses another release format | portable harness validates only core RLS governance and imposes no SE Harness package policy |

## Data and interface contracts

The generic RLS interface remains the existing TOML metadata and relations minus the distribution option. The repository bundle remains UTF-8 JSON schema `se-harness-release-bundle/v1`; the repository table remains schema 1, kind `python-wheel-sdist`, with the current epoch, wheel, sdist, checksum, and source-manifest fields. Repository tools treat paths, JSON, TOML, Git output, and filenames as untrusted and use safe bounded parsing.

## Security and privacy properties

- Dependency direction is repository tooling to portable governance; portable code never imports repository publication code.
- Candidate-controlled content cannot reach write, OIDC, or Pages jobs without independent validation.
- Binding cannot change accountable RLS state or core release identity.
- No stored publication credential, new external identity, or secret field is introduced.
- Repository-owned metadata is not advertised as portable core assurance.

## Performance and capacity

The correction adds at most one local atomic binding operation and reuses existing bounded manifest parsing. Publication build count, artifacts, concurrency, and external calls remain unchanged.

## Observability

The binder reports the RLS, manifest, candidate, version, and exact/rejected outcome without emitting secrets. Repository CI records the distribution-policy check separately from core graph validation. The publication result schema and workflow summaries remain unchanged.

## Compatibility and migration

The leaked portable surface is present only on unreleased `main`: no tag contains the RLO-001 candidate and no current RLS contains `[distribution]`. Therefore the correction removes the CLI flag and module before public release rather than maintaining a deprecated product API.

All existing released RLS artifacts remain valid. The managed template and validator changes follow normal safe upgrade rules. `VREC-RLO-001` remains the immutable assurance record for the original candidate; this corrective work receives its own later VREC if implemented.

## Examples and counterexamples

- Valid: generic preparation creates `RLS-SEH-008`, then a repository script binds an exact SE Harness bundle before review.
- Valid: a Rust consumer prepares an RLS without encountering wheel, PyPI, or `SHA256SUMS` rules.
- Invalid: portable `harnessctl` imports a module that derives `se_harness-VERSION-py3-none-any.whl`.
- Invalid: the binder changes `status`, `commit`, relations, or an existing conflicting distribution table.
- Invalid: a privileged workflow job imports or executes candidate release tooling.

## Explicitly unspecified decisions

The implementation agent may choose the exact repository-owned module and binder filenames, bounded result wording, atomic temporary-file mechanics, and test decomposition. It may not change the ownership boundary, schema-1 repository payload, generic RLS identity, single workflow input, action identities, permission separation, protected environments, or immutable-state rules.

## Approval

Approved as definition work by the accountable repository owner on 2026-08-18 through the statement `I approve this plan, you can create the artifact pack for it`. Implementation remains unauthorized until `WO-RLO-002` is separately approved.
