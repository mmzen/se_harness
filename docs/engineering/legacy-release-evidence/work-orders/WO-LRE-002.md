+++
id = "WO-LRE-002"
type = "work_order"
title = "Enforce the evaluator-evidence floor"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-31"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters which release records validation assesses and removes an upgrade refusal; later release decisions rely on the exact candidate behaviour, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/legacy_release_evidence.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  ".github/scripts/publish_dashboard.py",
  "tests/test_legacy_release_evidence.py",
  "tests/fixtures/legacy_release_evidence/",
  "tests/test_predecessor_bootstrap_retirement.py",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/README.md",
  "docs/engineering/legacy-release-evidence/evidence/",
  "docs/engineering/legacy-release-evidence/requirements/REQ-LRE-001.md",
  "docs/engineering/legacy-release-evidence/requirements/REQ-LRE-002.md",
  "docs/engineering/legacy-release-evidence/requirements/REQ-LRE-003.md",
  "docs/engineering/legacy-release-evidence/specifications/SPEC-LRE-001.md",
  "docs/engineering/legacy-release-evidence/specifications/SPEC-LRE-002.md",
  "docs/engineering/legacy-release-evidence/verification/VER-LRE-002.md",
  "docs/engineering/legacy-release-evidence/architecture/adr/ADR-LRE-001.md",
]

[relations]
implements = ["REQ-LRE-003"]
specifications = ["SPEC-LRE-002", "SPEC-LRE-001"]
architecture = ["ARCH-LRE-001", "ADR-LRE-001"]
verification = ["VER-LRE-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T05:25:01Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner by selecting the presented option 'Approve, start, complete on green', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the package module deletion, the installer refusal and declaration-write removal, the CLI notice removal, the template validator's floor gate with the resolver and frozen set deleted, the dashboard script, the rewritten tests and deleted fixture, the note, the domain-index line, the four amendment records and the evidence packet; and authorizes marking the work order implemented once the declared evidence is green. Implementation waits for pull request #296 to merge and merges main forward first. It authorizes no change to a hash-locked root file, no edit to any release record, no verification record, no release and no publication; the pull request's merge remains the owner's decision. Start preflight has not been run."
+++

# Work Order: Enforce the evaluator-evidence floor

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Assess the evaluator-evidence binding only on release records that carry
at least one evidence field (`LRE-FLR-001`, `LRE-FLR-002`); delete the
validator's resolver, frozen set and `W024` emission from the template
copy with the code retired and reserved (`LRE-FLR-003`); delete the
package module, the installer refusal, the declaration write and the
plan-time notice (`LRE-FLR-004`); keep the packet's optional key inert
(`LRE-FLR-005`); apply the same both-absent rule in the dashboard script
(`LRE-FLR-006`); re-pin the tests with a deletion sweep (`LRE-FLR-007`);
and record the retirement on `REQ-LRE-001`, `REQ-LRE-002`, `SPEC-LRE-001`
and `ADR-LRE-001` with dated amendment records. Issue #285 item #285a, on
the owner's floor decision of 2026-08-30: "releases without evaluator
evidence are not assessed", taken literally by the owner's selection of
the same day.

## Why now

Six of this repository's own identifiers are hard-coded into a validator
installed into every consumer, kept equal with a package copy through a
vector fixture and sixteen specification rules, warned about on every
validation, and guarded by an upgrade refusal — all to protect history
that the floor decision says validation should simply not assess.

## In scope

- `se_harness/legacy_release_evidence.py`: deleted.
- `se_harness/installer.py`: the pre-apply enumeration and refusal, the
  declaration write into upgrade evidence, and the module imports removed.
- `se_harness/cli.py`: the plan-time undeclared-legacy notice removed.
- The template validator: resolver, frozen set, state, `W024` emission and
  declaration errors removed; the binding requirement gated on at least
  one evidence field being present.
- `.github/scripts/publish_dashboard.py`: the frozen set replaced by the
  both-absent rule.
- `tests/test_legacy_release_evidence.py` rewritten to the floor tests and
  the sweep; the vector fixture directory deleted;
  `tests/test_predecessor_bootstrap_retirement.py` only if its
  root-versus-candidate validator ledger must declare the removed lines.
- The installation note's declaration section; the domain line in
  `docs/engineering/README.md`; the four amendment records; the evidence
  packet.

## Out of scope

The workflow gates that force evidence onto the path to `released`; the
hash-locked root validator and every other hash-locked file; retained
release records (never edited); the release carrying this change.

## Authorized decision envelope

Test names; the wording of the note and the domain-index line; whether the
retired-`W024` comment sits beside the binding gate or a code registry;
how `tests/test_legacy_release_evidence.py` is renamed or reorganized.

## Constraints

- The six pre-enforcement `RLS-SEH-*` records keep their bytes.
- The partial-binding and full-binding failure paths are unchanged.
- No hash-locked root file moves.

## Expected change surface

Three product modules (one deleted), one template script, one repository
script, up to two test modules and one fixture tree, one note, one index
line, four amendment records, the packet and the domain evidence.

## Required verification

Execute `VER-LRE-002` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/legacy-release-evidence/evidence/WO-LRE-002/`.

## Stop and escalate conditions

Any need to edit a release record; any hash-locked file in the change
set; any test that can only pass by keeping a resolver or identifier set;
any behavior change to a record carrying one or both evidence fields.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
