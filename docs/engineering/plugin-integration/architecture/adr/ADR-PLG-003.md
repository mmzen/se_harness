+++
id = "ADR-PLG-003"
type = "adr"
title = "Represent plugin ownership explicitly in the evaluator lock"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[relations]
decides = ["ARCH-PLG-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "technical-owner"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only ADR-PLG-003 approval as technical-owner. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# ADR: Represent plugin ownership explicitly in the evaluator lock

## Status

The artifact lifecycle records the technical-owner decision. Implementation and its assurance remain separate.

## Context

DEC-PLG-004 selected supported evaluator migration, including replacement of overlapping repository skills and preservation of unrelated content.
Current doctor derives its expected managed inventory from the full standard template.
Deleting retained skills alone would break that contract; ordinary upgrades would recreate them.
The first catalog is the two currently retained skills, not the already retired writing skills.

## Decision drivers

One authoritative ownership record, fail-closed old readers, safe customization handling, portable CI, recoverable file retirement, and no plugin execution during inspection.

## Considered options

| Option | Consequences |
| --- | --- |
| Manual deletion and lock editing | Loses transaction guarantees and gives ordinary upgrades no durable provider selection; incompatible with DEC-PLG-004. |
| Mark retained files as owner-controlled seeds | Does not represent external ownership or prove a provider binding; can hide deletion or duplication from integrity checks. |
| Add an ignored schema-3 metadata field | Old evaluators can ignore the ownership meaning; correctness would depend on incidental missing-file failures. |
| Explicit schema-4 binding and shared effective inventory | Makes ownership visible to every reader, forces old readers to refuse, and supports reviewed migration and restoration. |

## Decision

Select the explicit schema-4 binding and shared effective inventory for plugin ownership.
Keep schema 3 and the existing behavior for default repository ownership.
Bind portable package identities and retained-core digests; treat machine-specific roots as execution inputs.
Reuse and extend the evaluator's installer transaction with stale-input checks, exclusive acquisition, and interruption recovery.
Retain default repository behavior and all current decision rights.

## Consequences

The evaluator must be implemented, independently verified, released, and adopted before live repository migration.
The implementation must update every relevant inventory consumer, not merely the CLI and doctor output.
Existing schema-3 releases cannot operate on a plugin-owned schema-4 repository and must refuse before mutation.
Credential-free CI can inspect repository ownership without claiming external plugin availability.
WO-PLG-009 remains responsible for proving one active route in the native host, including global discovery conflicts.

## Validation

VER-PLG-020 requires matched before/after snapshots, plugin byte-mutation cases, upgrade replay, old-reader refusal, concurrent operations, and crash/recovery fault injection on Windows and Linux.
The current accepted C10/C11 limitation is not resolved or widened by this decision.

## Data and transaction interface

Both ownership CLI forms plan by default; application requires the exact reviewed plan digest.
Restoration uses the installed evaluator's retained standard skill inventory, never arbitrary replacement files.
The JSON result uses the existing command-result envelope and includes source identity, target provider, plan digest, conflicts, actual effects, and recovery state.

The binding input uses closed schema `se-harness-skill-ownership-binding-v1`, with explicit host-to-root mappings, independently expected assembly identities, and retained-core digests.
Absolute roots are local execution inputs. Only portable package identities and digests enter the committed lock.
The evaluator never treats an assembly's self-declared identity as approval or proof of native loading.

The plugin-owned lock uses schema 4 and a closed `skill_ownership` section.
Remaining file entries retain the existing managed, fragment, and seed meanings.
The migrated catalog leaves repository file entries and becomes explicitly externally owned.
Schema 3 remains supported unchanged for ordinary repository ownership.
Restoration removes the external binding and returns to the standard representation when compatible.

Names and paths follow existing portable assembly rules; selected roots must be explicit ordinary directories.
Remove only reviewed files, then prune proven-empty directories inside the repository; never recursively delete a skill directory.
The plugin's additional operator-brief Codex metadata remains provider-owned; migration creates no corresponding repository file.
Unexpected remnants of retired writing skills require separate assessment.
