+++
id = "ARCH-PLG-003"
type = "architecture"
title = "Evaluator-owned transactions for external skill ownership"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-12"
updated = "2026-09-12"
[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "public-interface-or-protocol"]
rationale = "External package ownership changes the lock protocol, trusted inventory boundary, and installer recovery behavior."
assessed_by = "implementation-planner"

[relations]
addresses = ["REQ-PLG-028", "REQ-PLG-029", "REQ-PLG-030", "REQ-PLG-031"]
conforms_to = ["SPEC-PLG-020", "SPEC-PLG-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "technical-owner"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only ARCH-PLG-003 approval as technical-owner. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Architecture: Evaluator-owned transactions for external skill ownership

## Context and scope

The evaluator owns repository installation and its lock. Native plugins own their external packages.
The migration bridges those ownership records without transferring governance authority to plugin code.
ADR-PLG-003 records the technical-owner choice of this design.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Ownership CLI | Parse explicit provider and identity inputs; plan, apply, restore, and report recovery. |
| Data-only binding verifier | Validate expected package identities, bounded inventories, retained-core contracts, and ordinary paths. |
| Shared effective-inventory resolver | Derive repository-managed paths from the versioned ownership record for installation, doctor, and mutation checks. |
| Installer transaction | Revalidate inputs, serialize application, retain recovery information, update files and lock, verify postconditions, and recover failures. |
| Existing evaluator authority guard | Require the exact installed released evaluator and existing governed mutation authority. |
| Plugin setup under WO-PLG-009 | Select the installed provider, invoke the released operation, and observe real native discovery. |

## Dependency direction

CLI calls the ownership planner and existing installer transaction.
Installer, doctor, and authority checks consume one shared ownership inventory; none implements a competing catalog.
The binding verifier reads package data without importing plugin modules or evaluator code from the target repository.
The evaluator remains usable in CI without a live host or external plugin files.

## State and recovery

Repository ownership becomes plugin ownership only after a complete successful transaction.
A transaction records its source, reviewed plan, temporary snapshots, and progress before irreversible file changes.
The recovery record is private to the repository and protected by ordinary-path checks and exclusive acquisition.
No new mutation may proceed while recovery is pending.
Success removes temporary recovery data only after file/lock postconditions hold.
Observed failed rollback remains an explicit failure with retained recovery inputs.

Restoration is a new explicit transaction, not an automatic response to missing plugin files.
The first implementation does not combine evaluator-version upgrade with skill migration in one operation.
The eventual migration-capable evaluator must already govern the target before its ordinary mutation authority is used.

## Trust boundaries

Locks, binding documents, local paths, package manifests, and inventory entries are hostile inputs.
Caller-supplied expected hashes provide selection, not authentication or approval by themselves.
Native host activation is observed later; an inventory cannot prove it.
Root paths are local inputs and are neither executed nor retained as portable trust anchors.
The transaction never writes outside the selected repository, changes host configuration, installs a plugin, or edits credentials.

## Compatibility

Schema 3 keeps the current standard repository path contract.
Schema 4 represents plugin ownership explicitly so old released evaluators fail closed.
All default installation and upgrade tests remain applicable to repository ownership.
No optional governance profile, reduced integrity mode, or implicit host support is introduced.

## Required decision

ADR-PLG-003 selects the ownership representation, effective-inventory boundary, and transactional recovery architecture.
The eight approved prior-contract applicability amendments listed in the packet review reconcile the selected locations and schema-floor exception, including DEC-PLG-007.


## Approved legacy-reader reconciliation — 2026-09-12

The operator approved this exact appendix as `technical-owner` with the instruction "i approve the 4 amendements". The approval was recorded at `2026-09-12T18:28:18Z` under WO-PLG-020. Its reviewed proposal and decision receipt are retained in that work order's governance evidence. The original definition text, approvals and historical observations remain preserved. This approval does not establish passing acceptance, completion or verification.

### Approved applicability: old-reader compatibility

The Compatibility section's statement that schema 4 makes old released evaluators fail closed applies to the complete class of interfaces that modify installed files/the lock or create/change formal governance artifacts, as defined in SPEC-PLG-020 and VER-PLG-020. It is not a universal filesystem write barrier. Released 0.17 can still inspect an artifact graph and generate evidence/report outputs without accepting schema 4 as an installation format. Those outputs carry no inferred authority to govern a plugin-owned target. SPEC-PLG-020's explicit legacy-reader boundary and VER-PLG-020's separately observed interface census govern this distinction.


## Approved exclusion of released-0.17 migration acceptance — 2026-09-12

The operator instructed "we don't care about 0.17, just ignore" after review of the old-tool acceptance issue. This instruction authorizes the following scope decision as `technical-owner`. The receipt was recorded at `2026-09-12T20:57:40.552684+00:00` under WO-PLG-020. Earlier approvals and observations are preserved.

This appendix supersedes the Compatibility section and preceding legacy-reader appendix only where they require already distributed 0.17 to refuse operations on plugin-owned schema 4. The supported migration architecture depends on the migration-capable evaluator. A versioned lock describes and validates that evaluator's ownership boundary; it does not harden an executable already distributed without those checks.

Released 0.17 behavior on migrated targets is outside this work order's acceptance scope, as selected by the operator. Preserve the old observations without a supported-compatibility claim. Schema-3 defaults, schema-4 ownership, candidate refusal/preservation rules, transactions, recovery and all other architectural decisions remain unchanged. The root-pinned development governor and ordinary predecessor upgrade rehearsal retain their separate roles.
