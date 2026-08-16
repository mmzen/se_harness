+++
id = "SPEC-WAC-001"
type = "specification"
title = "Explicit commit-bound assurance applicability and follow-up"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-WAC-001", "REQ-WAC-002", "REQ-WAC-003", "REQ-WAC-004", "REQ-WAC-005"]
+++

# Specification: Explicit commit-bound assurance applicability and follow-up

## Scope

Add one structured applicability declaration to work orders, validate and expose it at controlled boundaries, and derive an assurance-follow-up inspection queue. Preserve all existing VREC, release, lifecycle, evidence, and decision authority.

## Data contract

The work-order front matter may contain exactly one table:

```toml
[assurance]
commit_bound_verification = "required"
rationale = "Future engineering and release decisions rely on this candidate behavior."
decided_by = "quality-owner"
```

`commit_bound_verification` accepts only `required` or `not_required`. `rationale` and `decided_by` are trimmed non-empty strings, each bounded by the validator's existing safe metadata limits or new equivalent constants. Unknown assurance-table keys are rejected so misspellings cannot silently disable enforcement.

The canonical work-order template contains placeholders for all three fields and explains the decision test. `relations.verification` remains mandatory and retains its current meaning independently of this table.

## Validation rules

1. A present assurance table must be a table with exactly the supported keys and valid values for every work-order lifecycle state.
2. An approved or in-progress work order must contain a valid declaration. Use a new deterministic governance-plane diagnostic when it does not.
3. Draft work may remain incomplete and is not executable. Completed or disposed legacy work in `implemented`, `verified`, `released`, `rejected`, or `superseded` may omit the table for compatibility.
4. Validation never judges whether the rationale is substantively correct and never maps a role string to an authenticated human identity.
5. No requirement is inferred from dates, titles, paths, relations, VREC coverage, or Git state.

## Preflight rules

1. Start and review preflight project the classification, rationale, and deciding role in a dedicated assurance section.
2. A selected work order without a valid declaration fails preflight, including completed legacy work selected for renewed controlled execution or review.
3. Failure is read-only and explains that an accountable decision is required; it does not insert a default.
4. Existing phase, manifest, repository-command, and authority output remains intact.

## Inspection rules

1. Extend the inspection report contract with an `assurance_pending` queue. Version the inspection JSON schema because the public report shape changes.
2. Select a work order only when its type is `work_order`, status is `implemented`, and its explicit value is `required`.
3. Remove it from `assurance_pending` when any directly covering VREC is `ready`, `verified`, or `released`. A superseded, draft, or rejected record is not active coverage.
4. A ready covering VREC continues to appear only in `decision_required` with `assurance-review`; verified or released coverage produces no queue item.
5. Add one non-automatic suggestion action, `prepare-commit-bound-verification`, owned by `engineering-owner`: after selected work is retained in one clean candidate commit, prepare a ready VREC without inferring aggregate membership or exercising assurance authority.
6. Human and JSON rendering remain deterministic, control-character safe, repository-local, and non-gating.

## Lifecycle and command semantics

- `implemented` continues to mean completed work and retained evidence, not correctness.
- The declaration does not change a work-order status.
- `capture-verification` retains its explicit repeated selectors, exact-commit binding, clean-worktree boundary, and ready-only output. It may explicitly select a `not_required` work order; that later accountable scope decision is permitted but was not obligatory.
- VREC `ready -> verified`, supersession, RLS preparation, release authorization, and external promotion remain unchanged.
- Release selection receives no exemption: existing exact VREC coverage and release checks continue to apply.

## Accountable decision rule

Classify `required` when future engineering, assurance, operational, or release decisions will rely on the correctness of changed executable behavior, managed policy, CI, requirement/specification/architecture content, operating or release definitions, traceability, or other trusted engineering state.

Classify `not_required` only when the sole purpose is to record or transport an already authorized verification, release, supersession, publication, or deployment decision. Mixed scope is split or classified `required`. Uncertainty defaults procedurally to `required` and escalation; automation still records only the explicit value.

## Compatibility and migration

- Do not bulk-edit existing completed work orders.
- Do not change the repository artifact-schema version or implement the deferred general schema-versioning proposal.
- Newly created artifacts use the updated template. Existing actionable work is classified before preflight.
- Inspection ignores missing completed-legacy classification instead of manufacturing a false obligation or exemption.
- Update managed root and canonical policy, templates, validator, inspector, and any distributed helper needed for preflight behavior through canonical-first reconciliation.

## Error and recovery behavior

Malformed declarations fail validation or preflight with stable diagnostics. Missing assurance follow-up is inspection attention, not a validation error. Correction requires governed artifact edits; no command automatically changes work orders or creates a VREC.

## Security and authority

Repository text is untrusted input. Existing parsing, size, Unicode, terminal escaping, path safety, and deterministic ordering controls remain. The declaration and `decided_by` field are recorded claims, not authentication. Automation never grants the exception, assurance, release, or external-action authority.

## Explicit exclusions

Evidence-completeness enforcement, automatic VREC scope selection, automatic record creation, work-order status mirroring, historical bulk classification, branch-policy inference, release-policy redesign, recursive governance verification, aggregate scoring, and general artifact-schema versioning.
