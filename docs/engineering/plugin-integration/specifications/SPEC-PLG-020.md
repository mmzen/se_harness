+++
id = "SPEC-PLG-020"
type = "specification"
title = "Explicit evaluator ownership migration for retained plugin skills"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-12"
updated = "2026-09-12"
contract = "Explicit evaluator transactions transfer retained skill ownership while preserving repository content, integrity, recovery, and all existing governance authority."

[relations]
specifies = ["REQ-PLG-028", "REQ-PLG-029", "REQ-PLG-030", "REQ-PLG-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "technical-owner"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only SPEC-PLG-020 approval as technical-owner. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Specification: Explicit evaluator ownership migration for retained plugin skills

## In plain words

Move the two retained skills through a reviewed evaluator operation. Preserve their content and behavior while recording their selected provider.

## Scope

Default installation keeps repository-owned skills under the single standard governance contract.
Start with a clean 0.17.0 standard installation, upgraded to the eventual migration-capable evaluator first.
WO-PLG-009 supplies native connection and discovery.

## Terms

- **Provider binding:** portable host, package, version, inventory digest, and retained-skill identities stored in the repository lock.
- **Plan digest:** SHA-256 of a canonical operation description and its exact reviewed inputs.
- **Repository integrity:** consistency of governed repository files and its ownership record.
- **Plugin availability:** a separate observation of external package bytes and native host loading.

## Rules

**PLG-OWN-001.** Migration MUST require an explicit repository, provider selection, host set, expected plugin identity, and reviewed plan digest before application.

**PLG-OWN-002.** Planning MUST be read-only and list exact file removals, additions, ownership changes, input digests, conflicts, and effects outside the transaction.

**PLG-OWN-003.** The first migration catalog MUST contain only harness-orient and harness-operator-brief and their currently installed standard host surfaces.

**PLG-OWN-004.** Removal MUST require an ordinary, currently managed, catalog-listed file whose canonical digest matches both its lock and the selected evaluator distribution.

**PLG-OWN-005.** Customized, missing, unowned, linked, escaping, case-colliding, or ambiguous selected inputs MUST block the entire transaction before writes.

**PLG-OWN-006.** The transaction MUST preserve unrelated skills, owner content, governance documents, artifact history, evaluator identity, and all files outside its exact plan.

**PLG-OWN-007.** Applying MUST revalidate the plan digest, source files, lock, evaluator, plugin identity, and complete inventory before the first write.

**PLG-OWN-008.** Concurrent ownership operations MUST serialize or refuse without allowing either operation to apply a stale plan.

**PLG-OWN-009.** File retirement and the new ownership record MUST succeed together, with verified rollback on write failure or failed postconditions.

**PLG-OWN-010.** Interrupted transactions MUST be detected and recovered before another mutation; unresolved recovery MUST remain an explicit integrity failure.

**PLG-OWN-011.** A successful replay MUST be a no-op for identical inputs, including unchanged lock bytes and no additional evidence overwrite.

**PLG-OWN-012.** Plugin ownership MUST use an explicit versioned lock representation that migration-unaware released evaluators reject before mutation.

**PLG-OWN-013.** Integrity checking MUST validate the selected ownership record and reject unexpected repository copies of plugin-owned retained skills.

**PLG-OWN-014.** Ordinary init, upgrade, and direct installer entry points MUST preserve plugin ownership or refuse unsupported operations without recreating retired copies.

**PLG-OWN-015.** An evaluator upgrade MUST explicitly prove ownership-format compatibility before preserving an existing plugin binding.

**PLG-OWN-016.** Provider restoration MUST use the same reviewed transaction and restore current selected-distribution files without overwriting unrelated or customized content.

**PLG-OWN-017.** Missing external plugin files MUST remain unavailable observations and MUST NOT trigger automatic rebinding, repository restoration, or approval.

**PLG-OWN-018.** Plugin identity MUST include host, package identity, version, assembly inventory digest, and the exact retained-skill file digests.

**PLG-OWN-019.** Expected plugin identity MUST be supplied independently of the inspected directory; its self-declared manifest MUST NOT establish trust.

**PLG-OWN-020.** Plugin inspection MUST parse bounded data without imports, subprocess execution, network requests, extraction, or writes to the external installation.

**PLG-OWN-021.** Unknown schemas, duplicate keys, unsafe paths, excess input size, inventory discrepancies, or incompatible retained-skill identities MUST cause explicit refusal.

**PLG-OWN-022.** The binding MUST preserve retained core versions, digests, invocation policies, and evaluator boundaries established by SPEC-PLG-012.

**PLG-OWN-023.** A plugin update, changed root, changed host selection, or changed evaluator compatibility MUST require a new validated plan and explicit binding application.

**PLG-OWN-024.** Repository integrity MUST remain evaluable in credential-free CI without a plugin installation or machine-specific absolute paths in the committed lock.

**PLG-OWN-025.** Repository integrity success MUST NOT claim plugin availability, native discovery, hook enforcement, host qualification, or external-action authority.

**PLG-OWN-026.** Mutation guards MUST continue enforcing the exact released evaluator and all existing governance gates for either ownership selection.

**PLG-OWN-027.** Retained transaction evidence MUST distinguish planned, applied, rolled-back, recovery-required, and unchanged outcomes using observed identities and actual effects.

**PLG-OWN-028.** The first implementation MUST refuse older unsupported repository baselines and direct operators through an existing supported upgrade before migration.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Local customization or unknown skill ownership | No writes | Exact conflicting path and cause |
| Plan, lock, evaluator, or plugin changed | No writes | Stale reviewed input |
| Write or postcondition fails | Restore complete prior state | Failure and recovery outcome |
| Process interrupted during application | Detect pending recovery before mutation | Recovery required |
| External plugin unavailable in a clone | Check repository integrity independently | Plugin availability unobserved |
| Old evaluator reads plugin-owned lock | Refuse mutation | Unsupported ownership format |
| Duplicate retained skill appears locally | Fail integrity | Unexpected repository discovery surface |

## Examples

**Given** unchanged managed orientation files and a verified package inventory, **when** a reviewed migration applies, **then** PLG-OWN-004 and PLG-OWN-009 bind their retirement atomically.

**Given** a plugin-owned clone without external plugin files, **when** CI checks repository integrity, **then** PLG-OWN-024 allows that check without claiming availability.

**Given** a customized file in a retained skill directory, **when** migration is planned, **then** PLG-OWN-005 refuses the complete transaction.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-PLG-028 | PLG-OWN-001, PLG-OWN-002, PLG-OWN-003, PLG-OWN-004, PLG-OWN-005, PLG-OWN-006, PLG-OWN-028 |
| REQ-PLG-029 | PLG-OWN-011, PLG-OWN-012, PLG-OWN-013, PLG-OWN-014, PLG-OWN-015, PLG-OWN-024, PLG-OWN-025, PLG-OWN-026 |
| REQ-PLG-030 | PLG-OWN-007, PLG-OWN-008, PLG-OWN-009, PLG-OWN-010, PLG-OWN-016, PLG-OWN-017, PLG-OWN-027 |
| REQ-PLG-031 | PLG-OWN-018, PLG-OWN-019, PLG-OWN-020, PLG-OWN-021, PLG-OWN-022, PLG-OWN-023 |

## Not decided here

- Release and adoption.
- Native discovery under WO-PLG-009.
- Qualification under WO-PLG-015.
- Internal decomposition within approved scope.

## Data and interface contracts

Selected CLI contract, unavailable in 0.17.0:

`harnessctl skill-ownership TARGET --provider plugin --binding-input FILE [--apply --expected-plan-sha256 HASH] [--json]`

`harnessctl skill-ownership TARGET --provider repository [--apply --expected-plan-sha256 HASH] [--json]`

Application requires the exact plan digest; otherwise the command is read-only.
ADR-PLG-003 defines the binding representation and transaction interface.
Limits: 1 MiB/control document, 2,000 inventory files, 16 MiB/file, 128 MiB/aggregate payload.
Only reviewed regular files are removed; only proven-empty repository directories are pruned.

## Compatibility and migration

The baseline has seven managed files: three per retained core and one Claude orientation adapter.
Retired writing skills are excluded.
The [packet review](../../../notes/plugin-ownership-migration-2026-09-12.md) records the eight approved location and schema-floor amendments; DEC-PLG-007 selects the narrow schema-4 exception.
DEC-PLG-004 and DEC-PLG-006 remain unchanged.


## Approved legacy-reader reconciliation — 2026-09-12

The operator approved this exact appendix as `technical-owner` with the instruction "i approve the 4 amendements". The approval was recorded at `2026-09-12T18:28:18Z` under WO-PLG-020. Its reviewed proposal and decision receipt are retained in that work order's governance evidence. The original definition text, approvals and historical observations remain preserved. This approval does not establish passing acceptance, completion or verification.

### Approved applicability: migration-unaware evaluator boundary

For PLG-OWN-012 and its old-evaluator failure row, rejection before mutation applies to installed-file or lock changes and creation or state changes of formal governance artifacts through migration-unaware evaluator interfaces. Each applicable interface MUST refuse a plugin-owned schema-4 target before those mutations and identify unsupported lock format or evaluator incompatibility as the cause. An unrelated input, lifecycle or policy refusal is not evidence of that boundary. No such refusal may be replaced by a usage error, a mocked authority failure, or an observation of a different interface.

Released 0.17 has a narrower observed boundary than rejection of every filesystem-writing command: artifact-graph inspection, evidence-packet generation and derived reporting do not universally consult the installation lock parser. Retained check-result generation is an additional source-inspection concern whose actual behavior remains to be separately probed; no dynamic result for it is claimed here. They may read a schema-4 repository or write their specific evidence/report outputs. This is an explicit compatibility limitation, not installation support or governing authority. An evidence/report command's successful exit MUST NOT be treated as proof that the old evaluator accepts the installed ownership format, can govern the target, or supplies matching evaluator-bound assurance.

The candidate MUST preserve the selected ownership binding and installed bytes through the operations it supports. The distinction above grants no exception for modification of the lock, installed files, formal artifact creation or lifecycle decisions by an incompatible evaluator. PLG-OWN-013 through PLG-OWN-028 retain their existing obligations.
