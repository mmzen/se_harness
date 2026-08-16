+++
id = "REQ-OCA-002"
type = "requirement"
title = "Enforce evidence-backed operating assurance scope"
status = "implemented"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN an operating contract is validated, SE Harness SHALL enforce requirement-only assurance targets and SHALL reject every active assurance claim that lacks an active requirement, completed implementing work, or configured commit-bound verification coverage."
verification_method = "automated target-type, lifecycle, reachability, policy, migration, parity, and regression tests"

[relations]
derives_from = ["CAP-OCA-001"]
+++

# Requirement: Enforce evidence-backed operating assurance scope

## Rationale

The authoritative catalog declares `OPS.assures -> REQ`, but validation currently checks only that `assures` is non-empty and its targets exist. A release contract can therefore be accepted as an assurance target. An approved OPS also proves only that owners accepted prose; validation does not confirm that the claimed requirement is active or has any completed, independently evidenced implementation path.

## Preconditions and trigger

The rule runs during normal repository validation. Target typing applies to every operating contract. Implementation-readiness checks apply when an OPS is in an active lifecycle state.

## Required response

1. Reject every `assures` target whose formal artifact type is not `requirement`.
2. For an active OPS, require every assured requirement to be active.
3. Require at least one completed work order whose `implements` relation selects that requirement.
4. When `revision_provenance.required_for_verified_work = true`, require at least one such work order to be covered by a `verified` or `released` VREC.
5. Accept one eligible path when several work orders implement the same requirement; do not require unrelated later maintenance work to be verified merely because it reuses that requirement.
6. Keep lifecycle authority human: passing reachability checks does not approve an OPS or prove continuing operational conformance.

## Failure and boundary behavior

- Unknown targets continue to fail through the existing missing-target diagnostic.
- A known target of the wrong type fails structurally.
- An inactive requirement or missing completed implementation path fails governance validation for an active OPS.
- Missing eligible VREC coverage fails configured-policy validation only when commit-bound verified-work provenance is enabled.
- Draft or ready OPS records do not claim active assurance, but their relation targets must still be correctly typed.

## Constraints

- Preserve the current meanings of `ACTIVE_COVERAGE_STATUSES`, completed/releasable work, and eligible VREC states.
- Do not infer implementation from filenames, prose, evidence files, commits, release records, or transitive text references.
- Do not add an `RLS -> OPS` relation, change the traceability diagram, add an operational assessment artifact, or formalize recurring evidence.
- Do not broaden an older operating contract beyond the requirements its accepted prose and original packet actually cover.

## Acceptance examples

### Example: verified implementation path

**Given** an approved OPS assuring an implemented requirement, an implemented WO selecting that requirement, and a verified VREC covering the WO

**When** commit-bound provenance is enabled

**Then** the assurance readiness rule passes.

### Example: prose-only assurance

**Given** an approved OPS assuring an active requirement with no completed implementing work

**When** the repository is validated

**Then** validation fails even if the OPS body is complete.

### Example: unconfigured VREC requirement

**Given** an approved OPS, an active requirement, and a completed implementing WO without an eligible VREC

**When** commit-bound verified-work provenance is disabled

**Then** implementation readiness passes without inventing a VREC requirement.

## Open decisions

None for the two approved controls. Release applicability and continuing operational assessment remain explicitly unapproved and out of scope.
