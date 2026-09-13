+++
id = "SPEC-PLG-021"
type = "specification"
title = "Simple plugin installation and explicit checks"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

contract = "The plugin uses disposable skill replacement, repeatable setup, explicit governed checks, and lightweight development assembly while preserving ordinary repository boundaries."

[relations]
specifies = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-PLG-035", "REQ-PLG-036", "REQ-PLG-037"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "technical-owner"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the technical-owner approval of SPEC-PLG-021 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Specification: Simple plugin installation and explicit checks

## In plain words

Replace the old skills, retry setup normally, and run the checker when it is needed.

## Scope

This is the new plugin design for the owner's single development installation.
The compatibility table makes each replacement explicit. It does not retroactively change earlier work.

## Terms

- **Disposable directories:** the four old harness skill directories named in PLG-KIS-002.
- **Provider choice:** the portable record that selects plugin skills instead of repository copies.
- **Development package:** a local build with no publication or release claim.

For harness-orient, require `SKILL.md`, `skill-contract.json`, and `scripts/orient.py` under the plugin's `skills/harness-orient` directory.
For harness-operator-brief, require `SKILL.md`, `skill-contract.json`, and `scripts/check_brief.py` under `skills/harness-operator-brief`.
Either .codex-plugin/plugin.json or .claude-plugin/plugin.json supplies the native manifest.
This presence check does not execute plugin code or prove native discovery.

The existing seven-file repository catalog remains the inventory source. The extra Claude briefing directory is cleanup-only.
Lock schema 3 represents repository ownership; schema 4 represents plugin ownership.
Other installation integrity remains unchanged. A file-cleanup result grants no lifecycle authority.

## Rules

**PLG-KIS-001.** On approval, this contract MUST govern the changed plugin behavior selected by WO-PLG-021 according to the applicability table below.

**PLG-KIS-002.** Plugin migration MUST delete harness-orient and harness-operator-brief directories under .agents/skills and .claude/skills, including their edits and extra contents.

**PLG-KIS-003.** Migration MUST accept missing old directories, missing old catalog entries, and unrelated managed-file differences when the existing lock remains readable.

**PLG-KIS-004.** Before deletion, migration MUST require a verity-plane native manifest and the six nonempty replacement files listed below.

**PLG-KIS-005.** Migration MUST reject destinations redirected through symlinks or junctions and replacement plugins located inside a directory selected for deletion.

**PLG-KIS-006.** Migration MUST read current inputs on application; a preview is optional and has no approval-digest prerequisite.

**PLG-KIS-007.** Migration MUST use ordinary file operations and atomic lock replacement last; repeating the command finishes an interrupted attempt.

**PLG-KIS-008.** Migration MUST NOT require a journal, migration mutex, rollback protocol, file-identity tracking, plugin inventory digest, or exact evaluator identity for file cleanup.

**PLG-KIS-009.** The schema-4 skill_ownership record MUST select provider="plugin" without retaining plugin paths, versions, catalogs, self-checksums, or package fingerprints.

**PLG-KIS-010.** Doctor and upgrade MUST derive the excluded seven-file inventory from the provider choice without accessing the installed plugin.

**PLG-KIS-011.** Repository restoration MUST copy the current repository skill templates over existing disposable copies and restore ordinary managed entries.

**PLG-KIS-012.** Existing schema-4 bindings MUST remain readable; applying migration again replaces their extra metadata with the simple provider record.

**PLG-KIS-013.** Migration MUST preserve unrelated skills, repository content outside the four selected directories, and ordinary report destination protections.

**PLG-KIS-014.** Setup MUST create or reuse one documented private environment outside the checkout and repair it by reinstalling the selected evaluator wheel.

**PLG-KIS-015.** Setup MUST report missing Python prerequisites without installing Python or silently changing repository configuration.

**PLG-KIS-016.** Setup MUST install the supplied wheel offline, invoke its isolated checker once, and report its actual result without a separate observation receipt.

**PLG-KIS-017.** Governed work MUST use the repository-selected released evaluator; plugin code MUST NOT duplicate its version or hash as a runtime allowlist.

**PLG-KIS-018.** Plugin instructions MUST direct normal reading of repository instructions on entry, after compaction, and after switching repositories.

**PLG-KIS-019.** Plugin instructions MUST invoke the normal selected-work check when beginning governed work and follow its results at required lifecycle checkpoints.

**PLG-KIS-020.** The plugin MUST NOT register automatic before-tool checks or blocking session hooks; ordinary edits remain subject to the host permissions.

**PLG-KIS-021.** Host support MUST depend on the capabilities used for skill discovery and explicit commands, rather than exact host or Python patch versions.

**PLG-KIS-022.** Optional diagnostic logging failures MUST leave the actual operation result unchanged.

**PLG-KIS-023.** Plugin execution MUST NOT require custom process-tree containment, Windows Jobs, suspended child startup, or layered hook deadlines.

**PLG-KIS-024.** Local assembly MUST support current source and an explicitly selected local wheel without release records, immutable commits, or independently supplied payload digests.

**PLG-KIS-025.** Local assembly MUST label its output as development-only and validate the required package contents once.

**PLG-KIS-026.** Rebuilding MUST replace only the output directory owned by the build command, preserving unrelated directories.

**PLG-KIS-027.** Publication MUST retain the existing released-wheel identity and publication checks; development output cannot establish release eligibility.

**PLG-KIS-028.** CI MUST run the full candidate-source suite once and the small installed migration acceptance once per existing Windows and Ubuntu package environment.

**PLG-KIS-029.** Ownership acceptance MUST NOT add a second Python version, separate source-archive proof, recursive state archives, or investigation-only runner diagnostics.

**PLG-KIS-030.** Current plugin acceptance MUST exercise setup, skill discovery, explicit checks, and ordinary failure cases without repeating historical host qualification matrices.

**PLG-KIS-031.** Historical decisions, verification records, releases, and their retained evidence MUST remain unchanged.

**PLG-KIS-032.** Removed behavior MUST have its obsolete tests and current documentation removed or rewritten in the same work order.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing or malformed repository lock | Stop before deletion | Lock path and problem |
| Wrong plugin name or missing replacement | Stop before deletion | Manifest or missing file |
| Redirected destination or nested replacement | Stop before deletion | Unsafe path |
| File operation or lock save fails | Report failure; allow rerun | Failed operation and retry command |
| Setup fails | Keep the private path available for repair | Actual prerequisite or installer error |
| Required explicit check fails | Follow the checker result | Actual checker output |
| Optional diagnostic write fails | Keep the operation result | Diagnostic warning |
| Unrelated build output exists | Leave it untouched | Choose the documented build output |

## Examples

**Given** edited old skills, **when** the switch runs, **then** PLG-KIS-002 deletes them.

**Given** an interrupted switch, **when** it runs again, **then** PLG-KIS-007 finishes without journal recovery.

**Given** a new host patch version, **when** explicit checking works, **then** PLG-KIS-021 accepts those capabilities.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-PLG-032 | PLG-KIS-002, PLG-KIS-003, PLG-KIS-004, PLG-KIS-006, PLG-KIS-008 |
| REQ-PLG-033 | PLG-KIS-005, PLG-KIS-007, PLG-KIS-011, PLG-KIS-013 |
| REQ-PLG-034 | PLG-KIS-009, PLG-KIS-010, PLG-KIS-012 |
| REQ-PLG-035 | PLG-KIS-014, PLG-KIS-015, PLG-KIS-016, PLG-KIS-017 |
| REQ-PLG-036 | PLG-KIS-017, PLG-KIS-018, PLG-KIS-019, PLG-KIS-020, PLG-KIS-021, PLG-KIS-022, PLG-KIS-023 |
| REQ-PLG-037 | PLG-KIS-001, PLG-KIS-024, PLG-KIS-025, PLG-KIS-026, PLG-KIS-027, PLG-KIS-028, PLG-KIS-029, PLG-KIS-030, PLG-KIS-031, PLG-KIS-032 |

### Previous contract coverage

This table is part of the definition decision for this packet.
Upon approval, its replacement clauses apply to WO-PLG-021 and the behavior it delivers.
Earlier contracts still describe earlier candidates and unaffected behavior. Their historical lifecycle metadata remains unchanged.
Unfinished older work orders are not automatically started, completed, or widened by this delivery.

| Previous contract | Change for this delivery | Preserved boundary |
| --- | --- | --- |
| REQ-PLG-028–031; SPEC-PLG-020; ARCH-PLG-003; ADR-PLG-003; VER-PLG-020 | Replace the ownership transaction and binding design with this packet. | Earlier WO-PLG-020 and VREC-PLG-015 retain their original meaning. |
| REQ-PLG-001–005; SPEC-PLG-001/002; ARCH-PLG-001; ADR-PLG-001; VER-PLG-001/002 | Repair the private environment; remove plugin-only identity ceremonies; allow a development assembly route. | Shared host source, isolated released checker for governed work, supplied wheel installation, and publication provenance remain. |
| REQ-PLG-006–014; SPEC-PLG-003–008; ARCH-PLG-002; ADR-PLG-002; VER-PLG-003–008 | Replace automatic session/tool enforcement and frozen qualification profiles with explicit checks and current capability smoke tests. | Historical probe results and DEC-PLG-001/002/006 remain facts about their tested versions. |
| REQ-PLG-020/021; SPEC-PLG-012; VER-PLG-012 | The plugin supplies the retained skills without evaluator-byte equality or mandatory session delivery receipts. | Orientation stays read-only; operator briefing stays explicit. Existing requested brief output semantics remain. |
| REQ-AEX-009; SPEC-AEX-005, especially AEX-HST-001/003/007/009/012 | The portable provider choice replaces the previous validated external binding for the retained skill locations. | Default repository skill installation and unrelated host surfaces remain governed by their existing rules. |
| REQ-TCM-004; SPEC-TCM-001, TCM-SKL-001 and its PLG-020 amendment | The selected plugin supplies skill locations without frozen retained-core byte identity. | Technical communication and explicitly requested briefing behavior remain. |
| REQ-HUP-024; SPEC-HUP-012, HUP-LSF-001/003/008; VER-HUP-012; SPEC-PMI-001 | The schema-4 exception reads the simple provider record and accepts previous binding fields. | Schema-3 default, pre-3 floor, digest canonicalization and the separate governor-transition assessor remain. |
| REQ-ECP-027; SPEC-ECP-016, ECP-CLI-001/003 and its PLG-020 amendment | Keep explicit repository target and the command result envelope; replace reviewed-plan/recovery fields with provider, changes and errors. | Existing exit-code conventions and lifecycle authority remain. |
| REQ-CIP-009; SPEC-CIP-003, CIP-ONE-002/005 and its PLG-020 amendment; VER-CIP-003 | Retire the ownership-only Python 3.13 and expanded fault matrix exception; use the existing package environments. | The normal source suite, candidate-wheel build, release and predecessor upgrade checks remain. |
| Candidate template WORKFLOW.md ownership amendment | Describe the simple schema-4 provider exception and file-only cleanup without a recovery gate. | The installed root policy is unchanged; general governed mutations retain the selected evaluator requirement. |


## Not decided here

- General lifecycle decisions and release eligibility stay with the existing evaluator.
- Actual plugin installation and migration of the owner's projects require their selected execution requests.
- Internal function names and test organization belong to the implementation.
