+++
id = "REQ-DST-064"
type = "requirement"
title = "Preserve progressive and evaluator boundaries during the increase"
status = "approved"
owners = ["technical-owner", "security-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the topology acceptance target is increased, THE SYSTEM SHALL preserve all existing progressive-resource, integrity, content, publication, and released-evaluator boundaries and SHALL change only the candidate distribution contract until a later released upgrade is authorized."
verification_method = "automated-boundary-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve progressive and evaluator boundaries during the increase

## Rationale

The acceptance target belongs to candidate product behavior, while the repository root is governed by independently installed public 0.5.0. Updating the installed root generator from checkout source would again mix the developed harness with its governor. The capacity correction must remain an ordinary candidate change until release and a separately governed root upgrade.

## Preconditions and trigger

An approved implementation changes the topology acceptance target and aligns its product contract, tests, and package template.

## Required response

- Preserve the 262,144-byte `index.html`, 262,144-byte summary, 262,144-byte per-source-document, and 16,777,216-byte total-content limits.
- Preserve bundle-v2 schemas, resource roles, manifest byte/digest verification, deterministic serialization, publication exact-set validation, static hosting, and browser acquisition behavior.
- Change the canonical candidate distribution template and focused tests without editing the active root managed generator installed by public 0.5.0.
- Keep `.engineering-harness.toml`, `.engineering-harness.lock`, `ENGINEERING_HARNESS.md`, and the Engineering Harness workflow on the released 0.5.0 governor.
- Require a later release and supported standard-root upgrade before the installed governor adopts the new target.

## Failure and boundary behavior

Any candidate/root origin mixing, managed-integrity drift, schema change, removed field, weakened digest/path check, new runtime origin, publication change, or altered hard content budget stops implementation for amended authority.

## Constraints

- No topology sharding or truncation is authorized.
- No package version, release record, tag, publication, deployment, RCV artifact, or 0.5.1 release artifact is changed by this work.
- The public 0.5.0 evaluator remains authoritative for preflight, validation, doctor, and review.

## Acceptance examples

### Example: candidate distribution only

**Given** implementation raises the candidate template target to 2 MiB,

**When** public 0.5.0 runs `doctor` on the repository root,

**Then** all active managed files still match the installed public distribution.

### Example: forbidden root overwrite

**Given** checkout candidate code contains the new target,

**When** an implementation proposes copying that generator directly into the active managed root,

**Then** the operation is rejected pending a released distribution and supported root upgrade.

## Open decisions

None when approved.
