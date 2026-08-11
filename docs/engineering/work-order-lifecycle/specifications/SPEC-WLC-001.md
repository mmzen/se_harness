+++
id = "SPEC-WLC-001"
type = "specification"
title = "Work-order lifecycle consistency rules"
status = "implemented"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
+++

# Specification: Work-order lifecycle consistency rules

## Lifecycle model

The normal work-order path is `draft -> approved -> in_progress -> implemented`. `approved` grants bounded execution authority. `implemented` records completion and retained evidence. `verified` is optional work-order projection of a separate commit-bound assurance decision and is valid only when a verified or released VREC includes that work order under a repository policy requiring verified-work provenance. `released` additionally requires release provenance.

Governance-only work orders terminate at `implemented` unless independently selected into a later VREC. A work order that authorizes a VREC transition does not become verified merely because the target VREC does; this prevents unbounded governance recursion.

## Validator behavior

The validator reads `.engineering-harness.toml` using UTF-8 with an optional BOM and the standard-library TOML parser. Missing, invalid, non-table, missing-key, or non-boolean revision-provenance configuration defaults `required_for_verified_work` to `false` for compatibility.

When the policy is true, build the union of `verifies_work_order` relations from VRECs whose status is `verified` or `released`. For every work order whose status is `verified` or `released`, emit blocking revision-consistency diagnostic `E010` when its ID is absent from that union. `ready` and `superseded` VRECs never satisfy the invariant.

## Explorer behavior

Explorer consumes the validator report as the authoritative blocking result. Remove derived rule `W-REV-001` to avoid reporting the same condition twice. Continue to derive checkout-drift, unavailable-commit, release-provenance, and stale-ready findings according to their existing authority boundaries.

## Distribution and normalization

Change root managed files through the supported self-upgrade mechanism after updating the canonical standard template. Normalize exactly `WO-PUB-001` through `WO-PUB-004`, `WO-PYP-002`, `WO-PYP-003`, and `WO-REV-002` through `WO-REV-006` to `implemented`. Preserve all other front matter and bodies except an explicit retained normalization note if needed. Do not edit any VREC or RLS.

## Failure behavior

Validation fails closed for an uncovered verified or released work order only when the configured policy is true. It does not infer work completion, mutate files, approve evidence, or create provenance records.
