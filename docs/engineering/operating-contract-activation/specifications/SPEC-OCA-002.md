+++
id = "SPEC-OCA-002"
type = "specification"
title = "Operating assurance type and reachability validation"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-OCA-002"]
+++

# Specification: Operating assurance type and reachability validation

## Scope

Extend the existing validator with one typed relation entry and two active-assurance readiness checks. Migrate the only two current active OPS records that would fail the new type rule. Preserve all other validation, lifecycle, release, and operating semantics.

## Definitions

- **Active OPS:** an operating contract whose status is in the existing `ACTIVE_COVERAGE_STATUSES` set.
- **Active requirement:** a requirement whose status is in the same existing set.
- **Completed implementing work:** a work order in `implemented`, `verified`, or `released` whose declared `implements` relation selects the requirement.
- **Eligible VREC coverage:** a `verified` or `released` verification record whose `verifies_work_order` relation selects a completed implementing work order.

## Behavioral rules

1. Add `("operating_contract", "assures"): {"requirement"}` to `RELATION_TARGET_TYPES`. The existing `E011` structure diagnostic reports a known wrong-type target for every OPS lifecycle state.
2. For each active OPS and assured requirement, emit new governance diagnostic `E017` when the requirement is inactive or no completed implementing work exists.
3. Load the existing revision-provenance policy once. When `required_for_verified_work` is true, emit new policy diagnostic `E018` unless at least one completed implementing work order for the requirement is covered by a verified or released VREC.
4. One eligible implementation path satisfies the requirement. Extra incomplete, unverified, governance-only, or later maintenance work neither satisfies nor invalidates that path.
5. A ready, superseded, draft, or rejected VREC never satisfies commit-bound coverage.
6. A VREC covering a different work order never satisfies the path, even when it conforms to the same verification contract.
7. Deterministic diagnostics identify the OPS, assured requirement, and missing boundary without naming guessed remediation.

## Current-repository migration

- Change `OPS-DST-001.assures` from `REL-DST-001` to exactly `REQ-DST-001..006`. Those are the requirements covered by the contract's original distribution packet and accepted prose; later DST requirements are not added by inference.
- Change `OPS-REV-001.assures` from `REL-REV-001` to exactly `REQ-REV-001..008`.
- Preserve both records' `approved` status and owners. Update their dates and domain indexes only as needed to explain the relation migration.
- Correct the overbroad sentence in `WO-OCA-001` evidence so it says the six contracts activated by that work order—not every OPS in the repository—used requirement-only targets.

All selected DST and REV requirements are currently active, have completed implementing work, and have at least one verified/released VREC path. The migration and validator may therefore land atomically with no intended validation failure.

## Error and recovery behavior

Validation remains read-only and reports all deterministic failures in one run. It does not modify OPS relations, select an implementation path, create evidence, or transition lifecycle state. Repository owners correct failures through separately authorized artifacts and work.

## Compatibility and migration

- Root and canonical validators, managed integrity, package data, and standard installations remain synchronized.
- Update the one legacy test fixture that creates an approved OPS assuring a release contract; add focused fixtures for every new boundary.
- Existing repositories with a wrong-type or unsupported active OPS fail closed after upgrade and must explicitly migrate the contract rather than receiving an automatic rewrite.
- Repositories without commit-bound verified-work policy retain the completed-work check but do not acquire a VREC requirement.

## Explicitly excluded

No release-record relation, release-contract semantics, traceability-diagram redesign, operational assessment record, recurring-evidence schema, staleness rule, automatic remediation, approval action, or aggregate score.
