+++
id = "VER-LRE-002"
type = "verification"
title = "Independent evidence for the evaluator-evidence floor"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-31"

[relations]
verifies = ["REQ-LRE-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T05:25:01Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable owner by selecting the presented option 'Approve, start, complete on green' for WO-LRE-002: unbound, partial, bound, upgrade, inert-key, deletion-sweep and repository rows; readings from the exact released 0.11.0 evaluator outside the checkout."
+++

# Verification Contract: Independent evidence for the evaluator-evidence floor

## Independence

Expected values derive from `REQ-LRE-003` and the `LRE-FLR-` rules of
`SPEC-LRE-002`, never from the changed files. Validator behavior is read
through the template script loaded as a module over fixture repositories
and over this repository's own tree; installer behavior through the
upgrade transaction on fixtures; the repository readings through the exact
released evaluator.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-LRE-003` unbound | test | a fixture released record with both fields absent; this repository's six pre-enforcement records | zero errors, warnings and advisories for them; no `W024` anywhere in the template validator's report |
| `REQ-LRE-003` partial | test | a released record with exactly one field | the existing partial-binding error, unchanged |
| `REQ-LRE-003` bound | existing tests | fully bound and `ready` records | every existing binding check passes unchanged |
| `REQ-LRE-003` upgrade | test | an evaluator upgrade over a fixture holding unbound released records | the transaction proceeds; no refusal; the evidence JSON carries no declaration key |
| `LRE-FLR-005` inert key | test | a work order carrying `legacy_releases_without_evaluator_evidence` | the packet validates; the value changes nothing |
| `LRE-FLR-003`/`-004` deletion | test + sweep | `se_harness/`, `templates/repository/standard/scripts/`, `.github/scripts/` | no `legacy_release_evidence` module, resolver, frozen set, `RLS-SEH` identifier, or `W024` emission survives |
| `SPEC-LRE-002` this repository | reading | the template validator over this tree; the released 0.11.0 evaluator | template: 0 errors and exactly six fewer warnings than the root validator's count; root: `doctor` 0 FAIL, `validate` 0 errors, distributions PASS |

## Acceptance scenarios

1. Run the template validator over this repository: the six `RLS-SEH-*`
   records raise nothing; the report contains no `W024`.
2. Add one evidence field to a fixture copy of such a record: validation
   fails with the partial-binding error.
3. Grep the package, the template scripts and `.github/scripts/` for
   `legacy_release_evidence`, the frozen set and hard-coded `RLS-SEH`
   identifiers: zero hits, enforced by the sweep test.

## Evidence retention

Under `docs/engineering/legacy-release-evidence/evidence/WO-LRE-002/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.11.0, installed outside the
checkout.

## Residual uncertainty

The root validator keeps the resolver and its six `W024` warnings until
the next root adoption, so this repository's own gate reading is unchanged
until then. Whether any external consumer carries a declaration cannot be
measured from here; LRE-FLR-005 keeps such a packet valid either way.
