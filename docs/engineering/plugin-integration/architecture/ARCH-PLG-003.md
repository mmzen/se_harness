+++
id = "ARCH-PLG-003"
type = "architecture"
title = "Evaluator-owned transactions for external skill ownership"
status = "draft"
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
+++

# Architecture: Evaluator-owned transactions for external skill ownership

## Context and scope

The evaluator owns repository installation and its lock. Native plugins own their external packages.
The migration bridges those ownership records without transferring governance authority to plugin code.
The proposed design is subject to technical-owner approval through ADR-PLG-003.

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
The four prior-contract applicability amendments listed in the packet review must be accepted before implementation starts.
