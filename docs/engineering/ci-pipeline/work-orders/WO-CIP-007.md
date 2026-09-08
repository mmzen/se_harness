+++
id = "WO-CIP-007"
type = "work_order"
title = "Wave 5, CI: one qualification per pull request, one form for each pin, version and name"
status = "approved"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "The change decides which lane qualifies and tests every pull request, renames jobs the owner reads before every merge, and pins the actions every lane runs; the lanes are trusted engineering state that every later handoff, verification and release reading relies on."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/candidate-evidence.yml",
  ".github/workflows/release-qualification.yml",
  ".github/workflows/publication-rehearsal.yml",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/publish-dashboard-pages.yml",
  ".github/workflows/predecessor-evaluator-assessment.yml",
  ".github/workflows/release-candidate-replay.yml",
  "scripts/create_release_bundle_manifest.py",
  "repository_tools/release_distribution.py",
  "tests/",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-publication-rehearsal.md",
  "docs/engineering/ci-pipeline/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "docs/engineering/ci-pipeline/verification-records/",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-008.md",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-009.md",
  "docs/engineering/ci-pipeline/specifications/",
  "docs/engineering/ci-pipeline/verification/VER-CIP-003.md",
  "docs/engineering/ci-pipeline/work-orders/WO-CIP-007.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-CIP-008", "REQ-CIP-009"]
specifications = ["SPEC-CIP-003"]
verification = ["VER-CIP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:55:49Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-08 by selecting the presented option 'Approve all three (Recommended)', as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request. It authorizes only the declared scope: the eight repository-owned workflows, the manifest script and its module, the tests, the three notes, the amendment record on SPEC-CIP-001, the domain index and the evidence packet. It authorizes no change to the managed template or any managed path, no verification decision, no release and no publication; the merges remain the owner's decisions."
+++

# Work Order: Wave 5, CI: one qualification per pull request, one form for each pin, version and name

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`; the gate configuration is the owner-content
`.engineering-harness.delegation.toml`). The class is read at the base of
the pull request, so the approved packet merges to `main` first and the
execution follows on a second branch. The approval below, the verification
of the record it prepares, and every merge stay human decisions.
Commit-bound verification is `required`.

## Objective

Execute rules `CIP-ONE-001` to `CIP-ONE-017` of `SPEC-CIP-003`: the
rehearsal's candidate leg replays the recipe and no longer repeats the
qualification and the suite that `candidate-evidence.yml` already ran on the
same commit; the two inline re-checks go; every pin, Python version and
integration tool version takes one form; the Pages deployment queues behind
one group; the dead probe goes; the two retired names leave the workflows;
the manifest script stops producing schema-1 bundles; the note and
`SPEC-CIP-001` say so.

## In scope

- `release-qualification.yml`: the release-record condition on the
  qualification, suite and smoke step (`CIP-ONE-001`); the pin form and the
  one Python version.
- `candidate-evidence.yml`: the inline forbidden-member assertion and the
  `reconcile-governor` grep (`CIP-ONE-003`, `CIP-ONE-004`); the `env` block
  for the integration tool versions (`CIP-ONE-007`); the `upgrade-rehearsal`
  rename with its artifact, `needs` and outputs (`CIP-ONE-012`); the pin
  form; the header.
- `predecessor-evaluator-assessment.yml`: the rename of the workflow, job,
  group, artifact and temporary files (`CIP-ONE-011`); the pin form.
- `pages-publication.yml`: the `deploy` job's concurrency group
  (`CIP-ONE-008`) and the probe comment (`CIP-ONE-010`).
- `publish-pypi.yml`: the unconditional payload flag (`CIP-ONE-009`).
- `publication-rehearsal.yml`, `publish-dashboard-pages.yml`,
  `release-candidate-replay.yml`: the pin form and the one Python version
  (`CIP-ONE-005`, `CIP-ONE-006`); headers where they change.
- `scripts/create_release_bundle_manifest.py` and
  `repository_tools/release_distribution.py`: the required recipe
  (`CIP-ONE-013`).
- `tests/`: the pins of `CIP-ONE-016`; every test that names a retired
  workflow name, job or artifact, measured on `main` at `a68caf70` in
  `test_ci_pipeline.py`, `test_integration_package.py`,
  `test_standard_repository_lifecycle.py`, `test_release_build.py` and
  `test_release_orchestration.py`.
- `docs/notes/ci-pipeline.md` (`CIP-ONE-014`), and the sentences of
  `developing-se-harness.md` and `release-publication-rehearsal.md` that
  describe the candidate leg; the amendment record on `SPEC-CIP-001`
  (`CIP-ONE-015`); the domain index; the evidence packet.

## Out of scope

- The managed template `engineering-harness.yml` and every hash-locked root
  file: `WO-DST-026` changes the template, the root adoption of the carrying
  release changes the root.
- Renaming `scripts/validate_governor_transition.py` or any script, module
  or test file; only workflow-level names change.
- The trigger policy, the artifact handoff and the qualification steps that
  run in release-record mode; the migration rehearsal's two runs per
  platform; any release, publication or deployment.
- The repository ruleset: if a renamed job is a required status check, the
  owner updates the ruleset before the merge.

## Authorized decision envelope

The exact digests and tags of the pin form; the new step titles, temporary
file names and env variable names; whether the rehearsal artifact keeps its
platform suffix; the wording of the header comments, the note's figures and
the amendment record.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The suite, `validate`, `doctor` and the handoff check over the
  Git-derived change set pass before completion; the pull request's own
  lanes are the run observation `VER-CIP-003` names.
- Every `python-version` is the one string; every public action carries
  the pin form; no retired name remains in any workflow.

## Expected change surface

About sixty lines across eight workflows, most of them pins and renames;
ten lines in the manifest script and its module; about fifteen test
assertions changed or added; two note sections; one amendment record; this
packet.

## Required verification

Execute `VER-CIP-003` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/ci-pipeline/evidence/WO-CIP-007/`: the run-list readings
before and after, the pin and version inventories, the retired-name grep,
the manifest-script refusal, the `validate` and `doctor` readings, and the
lane results at the head.

## Stop and escalate conditions

A pull-request lane still running the suite twice at the head; a renamed job
missing as a required check on the pull request; a suite failure beyond the
baseline; any managed path in the change set; any need to touch the
qualification steps of release-record mode or the template workflow.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
