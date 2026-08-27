+++
id = "ADR-ECP-003"
type = "adr"
title = "Accountable decisions are authenticated records consumed by `transition`"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
decides = ["ARCH-ECP-001"]
+++

# ADR: Accountable decisions are authenticated records consumed by `transition`

## Status

Proposed.

## Context

`DECISION_RIGHTS.md` declares seven roles and twelve decision rights, and
every transition requires `--decision <ID>=<actor>`. The actor is validated
for length and control characters only (`se_harness/workflow.py:606`); no
Git-author, `GITHUB_ACTOR`, `CODEOWNERS`, or signature check exists in
`se_harness/` or `scripts/` (`docs/notes/agentic-execution-review-2026-08.md`,
section 3, "Human control"; section 5, weakness 1). The mutation guard proves
which evaluator wrote, never who decided. "Accountable humans retain
authority" is therefore a documentation claim. The delegated route of
`ADR-ECP-002` needs the same verifier, since a delegated actor is one more
identity holding one more role.

## Decision drivers

- `HRN-005`: automation prepares and never decides; the deciding identity
  must be provable.
- Principle 2: authority is enforced by signature or actor, at the Git
  boundary.
- One verifier for humans and delegated actors.
- Fail closed: no default identity source.
- Portability: a consumer without signing infrastructure must still have a
  configurable, explicit source.

## Considered options

### Option A: Git commit signature

The decision is bound to a signed commit; `git verify-commit HEAD` and the
committer identity verify the signer. Consequences: strongest binding, works
offline, survives host changes; requires key management in every consumer;
a CI job cannot sign on an owner's behalf.

### Option B: `GITHUB_ACTOR` in a hosted job

The workflow identity is the signer, mapped to roles by a
`CODEOWNERS`-shaped table. Consequences: zero key management; only valid
inside a GitHub-hosted job; trusts the platform's actor assertion; useless on
a developer machine.

### Option C: honour-based role string (today)

Keep `--decision ID=actor`. Consequences: no cost; no authority; the review's
most consequential finding stays open; the delegated route of `ADR-ECP-002`
would be a string too.

### Option D: a structured record with a configured identity source

A JSON decision record names artifact, target, role, right, reason, signer,
and time; `.engineering-harness.toml` selects the source (`git-signature`,
`github-actor`, or `configured-identity`) and carries the role map;
`transition --apply` verifies signer against source and role against right,
and retains the record's digest in the lifecycle event. Consequences: Options
A and B become interchangeable sources behind one contract; a consumer
without either still has an explicit list; the record is an artifact of
evidence, not a command-line string.

## Decision

Select Option D with A and B as its sources (`SPEC-ECP-004`, `ECP-DEC-001`
to `ECP-DEC-010`). Reject C. `transition --apply` consumes only decision
records; a repository without `[decision_identity]` cannot apply a
transition. The delegated actor of `SPEC-ECP-006` is a `github-actor`
record with role `delegated-executor`, verified by the same rules and
limited to three rights.

## Consequences

- Positive: every lifecycle event names a verified identity and a record
  digest; the delegated route inherits the verifier; the honour-based
  channel closes.
- Negative: one more file per decision; consumers must configure a source
  before their first `--apply`; a `configured-identity` list is only as
  strong as repository write access.
- Operational: the template `.engineering-harness.toml.tpl`,
  `DECISION_RIGHTS.md`, and `WORKFLOW.md` gain the record contract;
  installed copies regenerate on upgrade; a one-release window accepts the
  typed actor only where no table exists.
- Security: no default source; a record signed under a different kind than
  the configured one is refused; the record digest in the event makes a
  later edit of the record detectable.
- Migration: `WO-ECP-004` ships the verifier and the new
  `se_harness/decision_record.py`; historical `[[lifecycle_events]]` rows
  without `decision_record_sha256` stay valid; no approved artifact needs an
  amendment for this decision.

## Validation

`ECP-DEC-007` refusal without a table; `ECP-DEC-004` and `ECP-DEC-005` tests
per source, including a wrong-kind record; `ECP-DEC-006` role-map tests;
`ECP-DEC-008` event-digest test; the typed-actor refusal after the window;
a Windows lane test that `git verify-commit` is invoked through the shared
Git wrapper.
