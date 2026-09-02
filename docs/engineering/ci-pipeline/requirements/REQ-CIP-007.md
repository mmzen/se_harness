+++
id = "REQ-CIP-007"
type = "requirement"
title = "The pull-request rehearsal selects a record the base branch already holds"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN the publication rehearsal runs for a pull request, THE SYSTEM SHALL rehearse the release-record leg only against a schema-2 ready or released record present at the base branch head, so that the lane can be green before the pull request merges."
verification_method = ["test", "inspection"]
priority = "must"
source = "issue #305 and RCA issue #193: the release-record rehearsal lane was red on every release pull request (#270, #304, #313, #315) because the selector chose the record the pull request itself carries and the resolver then required it at the main head"
measure = "on a pull-request event the selector reads the records at refs/remotes/origin/BASE, where BASE is the pull request's base branch; the newest ready or released schema-2 record there is rehearsed, or the leg is skipped when none exists; on a push to main and on dispatch the selection is unchanged; the record-mode lane of a release pull request is green at its head"

[relations]
derives_from = ["CAP-CIP-001"]
+++

# Requirement: The pull-request rehearsal selects a record the base branch already holds

## Rationale

`publication-rehearsal.yml` runs the one release-qualification definition in
`release-record` mode against the newest ready or released schema-2 record.
On a release branch that record is the one the pull request itself carries,
and `publish_release.py resolve` then requires it at the `main` head: the
record cannot be there until the merge the red check gates. The lane failed
on every release pull request since the mechanism exists (#270, #304, #313,
#315) and passed only on the post-merge push, when nobody reads it as a
gate. The owner merged over a known-red check four times. With branch
protection in place, making the rehearsal a required check would turn the
annoyance into a deadlock.

A pull request should rehearse what its merge cannot invalidate: the
previous published record, replayed with the candidate's own workflow
definition. The new record is rehearsed by the push to `main` that carries
it, and by the dispatched `release-candidate-replay.yml` on the review ref
before the release decision, as the release sequence already requires.

## Behavior

- Trigger: `publication-rehearsal.yml` runs on a `pull_request` event.
- Response: the selector reads the release records at the base branch head
  (`refs/remotes/origin/BASE, where BASE is the pull request's base branch`), chooses the newest ready or released
  schema-2 record among them, and the record-mode leg rehearses that record;
  when the base holds none, the leg is skipped with the reason reported, as
  it is today for an empty repository.
- On failure: a base ref that cannot be fetched or resolved fails the
  select job with its reason; the candidate-mode leg is unaffected.

## Assumptions and dependencies

- Pushes to `main` and `workflow_dispatch` keep the current selection over
  the checkout, which is `main` itself in both cases.
- `release-qualification.yml` in `release-record` mode keeps reading the
  record at `refs/remotes/origin/main` and replaying its bound recipe.

## Acceptance examples

### Example: normal behavior

**Given** a release pull request whose branch carries the ready record
`RLS-SEH-023` and whose base `main` holds the released `RLS-SEH-022`,

**When** the publication rehearsal runs for the pull request,

**Then** the select job outputs `RLS-SEH-022` with the reason naming the
base ref, the record-mode leg replays `RLS-SEH-022`'s bound recipe and
passes, and the candidate-mode leg qualifies the pull request's commit.

### Example: failure behavior

**Given** the same pull request on a runner where the base ref cannot be
fetched,

**When** the select job runs,

**Then** it fails with the fetch error; no record is guessed from the
pull request's own tree.
