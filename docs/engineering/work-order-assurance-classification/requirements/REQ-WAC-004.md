+++
id = "REQ-WAC-004"
type = "requirement"
title = "Preserve legacy and non-recursive governance semantics"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN assurance classification is introduced into an existing repository, SE Harness SHALL preserve completed legacy work without inferred classification and SHALL allow governance-only verification, release, supersession, and publication work to terminate without recursive VREC obligations."
verification_method = "legacy repository, lifecycle, governance-only, and no-inference regression tests"

[relations]
derives_from = ["CAP-WAC-001"]
+++

# Requirement: Preserve legacy and non-recursive governance semantics

## Rationale

The current repository contains completed work orders created before explicit classification. Bulk inference would silently manufacture decisions, while requiring a VREC for every operation that records a VREC decision creates an infinite assurance chain.

## Required response

- Accept completed or disposed legacy work orders that omit the new table.
- Do not infer `required` or `not_required` for those artifacts.
- Require classification when a legacy work order is selected for new preflight-controlled execution.
- Permit explicitly non-required governance-only work to remain `implemented`.
- Preserve existing VREC coverage as authoritative even when a covered work order remains `implemented` or is historically `verified`.

## Failure and boundary behavior

Legacy omission grants no exemption for new work and produces no claim that assurance was unnecessary. If historical classification is desired, it requires separately authorized maintenance rather than automatic migration.

## Constraints

Do not use creation dates, path prefixes, titles, Git authors, or current coverage to synthesize the missing decision. General artifact-schema versioning remains deferred.

## Acceptance examples

The existing completed repository validates unchanged. A historical governance work order is not reported as pending merely because it lacks the new table. Reopening it through preflight requires an explicit governed classification.

## Open decisions

None.
