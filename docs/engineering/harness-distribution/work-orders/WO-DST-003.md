+++
id = "WO-DST-003"
type = "work_order"
title = "Add cross-agent instructions and repository-owned context"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-007", "REQ-DST-008"]
specifications = ["SPEC-DST-002"]
architecture = ["ARCH-DST-002", "ADR-DST-002"]
verification = ["VER-DST-002"]
+++

# Work Order: Add cross-agent instructions and repository-owned context

## Objective

Extend the single standard installation with a non-duplicating Claude Code adapter and an explicitly repository-owned context scaffold.

## In scope

- New standard-template fragments and seed content.
- Installer planning, lock, application, upgrade, and diagnostics behavior.
- Self-installation integration in this distribution repository.
- Deterministic tests, packaging metadata, acceptance scenarios, README, and verification evidence.

## Out of scope

- Automatic inference of repository commands, architecture, or product authority.
- Agent-specific contracts that duplicate `AGENTS.md`.
- New installation profiles, external services, commits, tags, pushes, package publication, verification approval, or release authorization.

## Authorized decision envelope

The implementation agent may select bounded internal names and helpers consistent with `SPEC-DST-002`, preserve schema-1 lock compatibility, and add deterministic tests. It may not weaken safe-write, customization-preservation, or authority boundaries.

## Expected change surface

Canonical standard template, installer control plane, doctor command, distribution tests, packaging metadata, self-installed root integrations, distribution documents, and retained evidence.

## Required verification

Run the artifact validator, full unit suite, CLI help smoke test, and targeted init/adopt/upgrade/doctor scenarios from `VER-DST-002`.

## Evidence to record

Retain exact commands, results, requirement mapping, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DST-003-verification.md`.

## Stop and escalate conditions

Stop if compatibility requires duplicated authoritative contracts, unsafe target replacement, inferred product facts, a lock migration that cannot preserve old installations, or a new installation profile.
