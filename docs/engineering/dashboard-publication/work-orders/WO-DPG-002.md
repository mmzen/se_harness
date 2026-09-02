+++
id = "WO-DPG-002"
type = "work_order"
title = "Let the Pages packager find its notice boundary in the designed Explorer"
status = "draft"
owners = ["engineering-owner", "quality-owner", "security-owner", "service-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "The packager decides what bytes reach the public demonstration; its boundary rule and the test that binds it to the real templates are trusted engineering state the next publication and every replay rely on."
decided_by = "repository-owner"

[execution_scope]
paths = [".github/scripts/publish_dashboard.py", "tests/test_dashboard_publication.py", "docs/notes/harness-dashboard-publication.md", "docs/engineering/dashboard-publication/README.md", "docs/engineering/dashboard-publication/evidence/", "docs/engineering/dashboard-publication/work-orders/WO-DPG-002.md"]

[relations]
implements = ["REQ-DPG-002"]
specifications = ["SPEC-DPG-001"]
architecture = ["ARCH-DPG-001", "ADR-DPG-001"]
verification = ["VER-DPG-001"]
+++

# Work Order: Let the Pages packager find its notice boundary in the designed Explorer

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Restore the release-bound Pages publication for the designed self-contained
Explorer. On 2026-09-02 the `publish-pypi.yml` run 33618394672 for
`RLS-SEH-023` (0.14.0) built the demonstration from the 0.13.0 root at
`66e71f8` (generation PASS, 1,246 artifacts, 0 errors) and then failed in
`publish_dashboard.py package` with "generated dashboard has no unique
publication notice boundary": the packager inserts its constant
demonstration notice after the hardcoded `<div class="workspace">` of the
previous page, an element the designed page (`WO-DST-023`) does not have.
The deploy was skipped; PyPI, the tag and the GitHub Release completed.
The packaging test did not catch it because it feeds the packager a
synthetic fixture that still carries the old element.

## In scope

- In `.github/scripts/publish_dashboard.py`, replace the single hardcoded
  boundary by an ordered tuple of accepted notice boundaries: the designed
  page's `<main class="hx-main">` and the previous page's
  `<div class="workspace">`, so replays of older released records keep
  working. The packager selects the one boundary that occurs exactly once
  in the generated `index.html`; zero or several matches, or matches of
  both, fail closed with the existing message. The notice text
  (`SPEC-DPG-001` rule 10, a constant) does not change.
- In `tests/test_dashboard_publication.py`: assert that the root copy
  `scripts/harness_explorer/index.template.html` and the canonical
  `templates/repository/standard/scripts/harness_explorer/index.template.html`
  each contain exactly one accepted boundary, so a future page redesign
  fails this test before it fails a publication; exercise packaging with a
  fixture carrying the designed boundary and with a fixture carrying
  neither or both; keep the existing fixture tests.
- One sentence in `docs/notes/harness-dashboard-publication.md` naming the
  boundary rule, if the note describes the notice insertion.
- This work order's evidence packet and the domain index line.

## Out of scope

- Any change to the Pages workflows, the resolver, the payload allowlist,
  the notice wording, the generator, the templates, or any managed path.
- Dispatching the recovery publication: after this work order merges, the
  repository owner authorizes `publish-dashboard-pages.yml` for
  `RLS-SEH-023` at governance commit `66e71f8` as a separate external act
  (`SPEC-DPG-001` rule 6, `OPS-DPG-001`). The release record does not move.

## Authorized decision envelope

The name and shape of the boundary registry and its helper; the fixture
layout; the wording of the test names and the note sentence. It may not
change the notice text, weaken any fail-closed check, or touch a path
outside the listed scope.

## Constraints

- The packager must keep failing closed when no accepted boundary occurs
  exactly once.
- The candidate suite, the repository checks and the handoff check over
  the Git-derived change set pass before completion.

## Expected change surface

The helper's constant and one insertion site, one test class, one note
sentence, this packet.

## Required verification

Execute `VER-DPG-001`'s automated rows for the packaging behaviour;
repository-required checks; the pull request's lanes; the handoff check
over the Git-derived change set. The public deployment itself is the
separate recovery act and its observation is recorded on it.

## Evidence to record

`docs/engineering/dashboard-publication/evidence/WO-DPG-002/`.

## Stop and escalate conditions

A boundary that is not unique in either real template; any need to change
the notice text or a workflow; a suite whose failure set differs from the
baseline beyond the tests this work order adds or changes.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
