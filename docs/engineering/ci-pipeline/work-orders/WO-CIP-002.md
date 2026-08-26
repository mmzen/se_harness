+++
id = "WO-CIP-002"
type = "work_order"
title = "One qualification definition for the rehearsal and the release; one Pages job; one schema leg"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The work replaces the rehearsal mechanism that WO-RLO-005 introduced and restructures the privileged publication workflow; release decisions depend on the exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/release-qualification.yml",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/publication-rehearsal.yml",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/publish-dashboard-pages.yml",
  ".github/scripts/",
  "repository_tools/",
  "se_harness/workflow_contract.py",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/release-orchestration/evidence/",
  "docs/notes/release-publication-rehearsal.md",
  ".github/workflows/candidate-evidence.yml",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "tests/",
]

[relations]
implements = ["REQ-CIP-003", "REQ-CIP-005"]
specifications = ["SPEC-CIP-001"]
architecture = ["ARCH-CIP-001", "ADR-CIP-001", "ADR-CIP-002"]
verification = ["VER-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T16:38:04Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: you can start WO-CIP-002; ADR-CIP-001 is approved."
+++

# Work Order: One qualification definition for the rehearsal and the release; one Pages job; one schema leg

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.
`ADR-CIP-001` must be accepted before start.

## Objective

P3 and P5: `release-qualification.yml` and `pages-publication.yml` as
`workflow_call` definitions; both lanes as callers; the divergence
mechanism and `rehearse_publication.py` removed; scripts importing the
package's helpers; the idle schema leg removed; `classify-pypi` used or
deleted.

## In scope

`CIP-QLF` 1–5; `CIP-LEG` 1–2; `CIP-DOC`: `ci-pipeline.md`,
`developing-se-harness.md` "Release sequences" (rehearsal paragraph, the
schema-1 note), `harnessctl-reference.md` only if a command changes; a
note in `release-orchestration/evidence/` recording how `CAP-RLO-003` is
now evidenced.

## Scope amendment, 2026-08-26

Owner decision 2026-08-26, taken interactively during implementation: add
`docs/notes/release-publication-rehearsal.md` to the execution scope. The
note describes the rehearsal mechanism this work order removes (the Python
copy of the qualification, the YAML reader and the digest declaration) and
must describe the reusable definition instead; the handoff check refused the
rewrite as out of scope. The amendment is a direct edit of `execution_scope`
under `CIP-DOC`; it adds a documentation path and no code path.

## Scope amendment, 2026-08-26 (second)

Owner decision 2026-08-26, taken interactively: add
`.github/workflows/candidate-evidence.yml` to the execution scope so that this
work order corrects a defect the hosted run of pull request #172 found in
`WO-CIP-003`'s implemented change: the `governance-migration` job did not
list `candidate-source` in its `needs`, so the derived predecessor outputs it
consumes resolved to empty strings and its guard refused to run. The fix is
the `needs` list and a test that every `needs.<job>.outputs` reference names a
job in the consumer's `needs`. `WO-CIP-003` stays implemented and
`VREC-CIP-003` stays the record of its commit; both evidence files disclose
the correction.

## Out of scope

Trigger policy (WO-CIP-001), the release contract (WO-CIP-004), the
predecessor derivation (WO-CIP-003), any change to what the qualification
asserts, the `pypi` environment.

## Authorized decision envelope

The engineering owner chooses between calling `classify-pypi` and deleting
it, and may keep `publish-dashboard-pages.yml` as a thin caller or delete
it in favour of a `workflow_dispatch` input on `publish-pypi.yml`; the
evidence records the choice.

## Constraints

The reusable workflows carry `permissions: contents: read` and no secrets
input. The release run on a real record is not exercised here; the
rehearsal in `release-record` mode against the latest released record is.

## Expected change surface

Two new workflows, three edited, two files deleted, four scripts reduced,
helpers added to `repository_tools`, notes, tests, evidence.

## Required verification

`VER-CIP-001` rows 3 and 5 and scenario 3; the rehearsal green on both
platforms in both modes on the pull request; repository-required checks;
full suite; handoff check.

## Evidence to record

Under `docs/engineering/ci-pipeline/evidence/WO-CIP-002/`: the line count
before and after, the rehearsal runs, the grep proving no digest artefact
and no duplicated helper.

## Stop and escalate conditions

Stop if a privileged job would need anything the reusable workflow cannot
give it without a secret, or if the rehearsal in `release-record` mode
cannot run credential-free.

## Completion report format

The `harnessctl check . --artifact WO-CIP-002 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
