+++
id = "WO-CIP-006"
type = "work_order"
title = "Let the pull-request rehearsal select a record the base already holds"
status = "draft"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "The change decides which record every pull request's rehearsal lane replays, a gate the owner reads before every merge; its selector and workflow are trusted engineering state."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/scripts/publish_release.py",
  ".github/workflows/publication-rehearsal.yml",
  "tests/test_ci_pipeline.py",
  "docs/notes/release-publication-rehearsal.md",
  "docs/engineering/ci-pipeline/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-007.md",
  "docs/engineering/ci-pipeline/specifications/SPEC-CIP-002.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-002.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-CIP-007"]
specifications = ["SPEC-CIP-002"]
verification = ["VER-CIP-002"]
+++

# Work Order: Let the pull-request rehearsal select a record the base already holds

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

Close issues #305 and #193: on a pull-request event the publication
rehearsal's `select` job fetches the base branch head and the selector
chooses the newest ready or released schema-2 record present there
(`CIP-REH-001` to `CIP-REH-004`), so a release pull request rehearses the
previous published record and its record-mode lane can be green before its
own merge; pushes to `main` and dispatches select as today. Tests bind the
selector and the workflow (`CIP-REH-005`); the note and the header comment
state the rule (`CIP-REH-006`).

## In scope

- `.github/scripts/publish_release.py`: the optional `base_ref` of
  `select_rehearsal_record`, read through `_release_records_at`, and the
  `--base-ref` option of the `select-rehearsal-record` command.
- `.github/workflows/publication-rehearsal.yml`: the base fetch and the
  `--base-ref` argument, both conditioned on the pull-request event; the
  header comment.
- `tests/test_ci_pipeline.py`: the temporary-repository selection test and
  the workflow assertions.
- `docs/notes/release-publication-rehearsal.md`: the selection rule.
- The evidence packet with the delegated lifecycle events quoted back; the
  domain index.

## Out of scope

- `release-qualification.yml`, `publish-pypi.yml`,
  `release-candidate-replay.yml`, `publish_release.py resolve`, the
  Pages workflows, any managed path, any release or publication.
- Making the rehearsal a required check (the owner's ruleset decision).

## Authorized decision envelope

The exact fetch command and step name; the wording of the reason string,
the test names and the note sentence.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The suite, `validate`, `doctor` and the handoff check over the
  Git-derived change set pass before completion; the pull request's own
  record-mode lane is the run observation `VER-CIP-002` names.

## Expected change surface

About twenty lines in the selector, ten in the workflow, one test extended
and one added, one note sentence, this packet.

## Required verification

Execute `VER-CIP-002` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/ci-pipeline/evidence/WO-CIP-006/`.

## Stop and escalate conditions

A record-mode lane still red at the execution pull request's head for the
selection reason; a suite failure beyond the baseline; any managed path in
the change set; any need to touch the qualification definition.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
