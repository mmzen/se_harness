+++
id = "WO-DST-025"
type = "work_order"
title = "Remove the inert keys from the installed configuration"
status = "in_progress"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters a hash-locked file that the installer writes into every governed repository, so every consumer upgrade rewrites it, and it amends two approved definitions; the next release and this repository's own root adoption rely on its correctness."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "tests/",
  "docs/engineering/harness-distribution/",
  "docs/engineering/revision-provenance/specifications/SPEC-REV-001.md",
  "docs/engineering/self-hosting-boundary/requirements/REQ-SHB-009.md",
]

[relations]
implements = ["REQ-DST-071"]
specifications = ["SPEC-DST-026"]
verification = ["VER-DST-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T18:41:35Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-07 by selecting the presented option 'Approve and start immediately', after the owner instructed that all unused configuration items be removed and DEC-DST-001 was disposed as remove-marker. Seven of the twelve keys in the installed configuration have no reader anywhere in the evaluator; the packet removes them from the standard template, pins the installed key set with its reader inventory, and amends the two definitions whose prose names a removed key."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-07T18:41:49Z"
decided_by = "engineering-owner"
reason = "Started by the accountable engineering owner on 2026-09-07 by selecting the presented option 'Approve and start immediately' in the same sitting as the approvals. Implementation proceeds on branch packet/dst-025-configuration-surface under the approved execution scope: the standard configuration template, tests, this domain, SPEC-REV-001 and REQ-SHB-009."
+++

# Work Order: Remove the inert keys from the installed configuration

## Lifecycle

Drafted on 2026-09-07 after the repository owner instructed that all unused
configuration items be removed, following a reading that found seven of the
twelve keys in `.engineering-harness.toml` with no reader anywhere in the
evaluator. The complexity audit of 2026-08 had already recorded one of them as
item P2-10. Every approval below is the owner's; nothing here is approved by
implication.

## Objective

Make the installed configuration honest: five keys, each read by a named part
of the harness, so that an owner who reads the file learns what they can
actually change, and the integrity check stops defending bytes that promise a
policy the tool never had.

## In scope

- Remove `artifact_root`, `dashboard_output` and `schema_version` from the
  template's `[harness]` table (`SPEC-DST-026` DST-CFG-001, DST-CFG-003,
  DST-CFG-005).
- Remove `require_full_commit`, `require_clean_worktree`,
  `verification_record_status` and `release_record_status` from the template's
  `[revision_provenance]` table (DST-CFG-002, DST-CFG-004).
- Add the key-set and reader-inventory test, and the upgrade cases
  `VER-DST-026` names, including the fixture installed by released 0.16.0 and
  the customized-configuration case (DST-CFG-008 to DST-CFG-013).
- Amend `SPEC-REV-001`'s compatibility sentence and `REQ-SHB-009`'s acceptance
  example, each with an amendment record naming this work order (DST-CFG-006).
- Add the packet's chain to the harness-distribution domain index and retain
  evidence under `docs/engineering/harness-distribution/evidence/`.

## Out of scope

- Any byte of this repository's root `.engineering-harness.toml` or its lock;
  they move at the root adoption of the carrying release (DST-CFG-014,
  DST-CFG-015).
- Making any removed setting work, and adding a strict-key refusal to any
  loader (DST-CFG-011).
- The duplication of the tool version between the configuration and the lock,
  which is the second half of audit item P2-10.
- The divergent handling of a non-boolean value by the two provenance loaders.
- Any change to the installer's transaction rules, the lock schema, the
  managed CI workflow, or the skills under `.agents/`.
- Building, releasing, publishing or adopting anything.

## Authorized decision envelope

The implementation agent may choose where the key-set test lives, the shape of
the upgrade fixture, the form of the reader inventory, and the wording of the
two amendment records. It may not remove a key the harness reads, keep a key it
does not, widen the execution scope, touch the root configuration or the lock,
or change a provenance diagnostic.

## Constraints

- Read `ENGINEERING_HARNESS.md` and run the review preflight with the released
  0.16.0 evaluator from its venv outside the checkout before completion.
- The candidate suite must pass on the hosted Linux lane; the local Windows
  suite is a control whose skips are labelled.
- The amendments to the two definitions change prose only; neither statement,
  rule identifier nor relation moves.
- Keep the diff free of unrelated changes, and list every test file touched in
  the completion report.

## Expected change surface

One template file; one new or extended test module plus the upgrade fixture;
two amended definitions; this domain's index and evidence.

## Required verification

`VER-DST-026` in full: the key-set, reader-inventory, install, upgrade,
customized, tolerance and behaviour-parity tests; the three inspections;
scenarios A to C run from a wheel installed outside the checkout, with outputs
retained.

## Evidence to record

`docs/engineering/harness-distribution/evidence/WO-DST-025-verification.md`:
the rendered configuration before and after, the upgrade plan, the scenario
outputs, the reader inventory, the hosted lane's test report, the local control
reading, the list of test files changed, and the review preflight result.

## Stop and escalate conditions

- A reader of a key listed for removal is found anywhere in the evaluator, a
  workflow, a skill, or a consumer-facing document.
- The upgrade classifies the unmodified configuration as anything but a safe
  rewrite, or loses the recorded project name or installation date.
- An amendment to either definition would need more than prose.
- The scope check reports a path outside `[execution_scope]`.

## Completion report format

List the keys removed and the five that remain, each with its reading module;
give the upgrade plan's classification and the before-and-after key counts;
give scenario A to C outcomes; give the hosted lane result and the local
control reading, each labelled; state that the root configuration and lock are
byte-identical to `main`; name the adoption obligation DST-CFG-015 carried
forward to the next root-adoption work order.
