+++
id = "REQ-RSK-002"
type = "requirement"
title = "Raise a risk when its score reaches the acceptance level"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a risk is created or its score changes, THE SYSTEM SHALL compare the score with the repository's configured [risk].acceptance_level, defaulting to 1 when unconfigured, and SHALL set the risk to raised when the score is greater than or equal to the level and to identified otherwise, recording the comparison as a computed event and not as a decision."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "requirements-steward"
+++

# Requirement: Raise a risk when its score reaches the acceptance level

## Rationale

Whether a risk needs a human is repository policy, not the raiser's opinion.
The comparison is mechanical so that neither an agent nor an owner can keep a
risk below the bar by choosing not to raise it. The default is to raise
everything: the harness fails closed everywhere else, and a repository lowers
the bar deliberately in its hash-locked installation file.

## Preconditions and trigger

`harnessctl raise-risk`, or validation of a risk whose stored score differs
from its stored level comparison.

## Required response

- `[risk].acceptance_level` in `.engineering-harness.toml`; absent means 1.
- `score >= acceptance_level` yields `raised`; otherwise `identified`.
- The lifecycle event `identified -> raised` is recorded with
  `decided_by = "harnessctl"` and the level used; it exercises no decision
  right.
- The level in force is copied into the artifact so later policy changes do
  not silently re-classify history.

## Failure and boundary behavior

A risk stored as `identified` whose score meets the level it carries is a
governance error. A level outside 1-25 is a configuration error reported by
`doctor`.

## Constraints

Raising never edits any other artifact.

## Acceptance examples

### Example: normal behavior

**Given** `acceptance_level = 6` and a risk scored 12

**When** it is raised

**Then** its status is `raised` and the event names level 6.

### Example: failure behavior

**Given** no `[risk]` section and a risk scored 1

**When** it is raised

**Then** its status is `raised`.

## Open decisions

None. Default 1 by owner decision on 2026-08-25.
