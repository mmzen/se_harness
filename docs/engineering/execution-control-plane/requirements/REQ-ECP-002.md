+++
id = "REQ-ECP-002"
type = "requirement"
title = "The change set is derived from Git"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN `harnessctl check` is run with `--from-git <base>`, THE SYSTEM SHALL derive the changed-path set from the Git difference between `<base>` and the working tree, including untracked files, before evaluating execution-scope predicates."
verification_method = ["test"]
priority = "must"
source = "review section 5, weakness 2"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The change set is derived from Git

## Rationale

Execution scope is enforced only by `check --changed-path ... --changes-
complete` from paths the agent types by hand; they are never compared to `git
diff` (docs/notes/agentic-execution-review-2026-08.md:108-111;
se_harness/workflow_compliance.py:156-165, :316-322). `WO-REB-027` needed
twenty-two hand-typed paths, and an incomplete change set is unobservable by
design (docs/notes/agentic-execution-review-2026-08.md:209-213, :288-293). Scope
therefore rests on self-declaration, which the 2026-08 agentic execution review
classes as a severe architectural weakness (section 5, weakness 2). Git already
knows the change set; the harness must read it rather than ask.

## Behavior

- Trigger: `harnessctl check` is invoked with `--from-git <base>`, where
  `<base>` is any resolvable Git revision.
- Response: the changed-path set is the union of tracked paths differing between
  `<base>` and the working tree and of untracked, non-ignored paths; it is
  sorted, reported in the result block, and used as the input of `QGP-G4I-PATHS`
  and every other execution-scope predicate, with completeness asserted by the
  harness.
- On failure: when `<base>` does not resolve, the working tree is not a Git
  checkout, or `--from-git` is combined with `--changed-path`, the command fails
  closed with a coded predicate and evaluates no scope predicate.

## Assumptions and dependencies

- A Git executable is reachable; outside a checkout the predicates are
  `not_assessable`, never `pass`.
- The scope predicates keep their identifiers (`QGP-G4I-PATHS`, `WEX201`).
- `--changed-path` may remain as an explicit alternative; it is never merged
  with a Git-derived set.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-002.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` declares `src/a.py` and `tests/`; the branch modified
`src/a.py` and added the untracked `tests/test_a.py`.

**When** `harnessctl check . --artifact WO-X-004 --checkpoint handoff --from-git
origin/main` runs.

**Then** the result lists exactly `src/a.py` and `tests/test_a.py` as the
changed-path set, marks it complete, and `QGP-G4I-PATHS` is `pass`.

### Example: failure behavior

**Given** the same work order, and the branch also rewrote `README.md`, which is
outside the declared scope.

**When** the same command runs.

**Then** the changed-path set includes `README.md`, `QGP-G4I-PATHS` is `fail`
with `WEX201` naming `README.md`, and the corrective is not the evaluated
command.

## Open decisions

None.
