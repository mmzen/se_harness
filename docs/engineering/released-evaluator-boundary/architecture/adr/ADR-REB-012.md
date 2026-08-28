+++
id = "ADR-REB-012"
type = "adr"
title = "Retirement of the predecessor-bootstrap release path"
status = "approved"
owners = ["technical-owner", "repository-owner", "release-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
decides = ["ARCH-REB-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: option 3 of four is chosen: retire the machinery and keep the closed history as digest-verifiable facts. The owner accepts the stated negative consequence, that the 0.6.0 preparation and publication evidence becomes digest-verifiable but no longer reproducible. Option 4, deleting the closed history, is rejected outright."
+++

# ADR: Retirement of the predecessor-bootstrap release path

## Status

Accepted on 2026-08-27 by the accountable owner; decides `ARCH-REB-012`.

## Context

Released 0.5.0 does not recognise `status = "rejected"` on a release record;
it emits `E009`. When the 0.6.0 release retained its own failed attempt —
`REL-SEH-008` and `RLS-SEH-009`, both rejected — the repository became
unparseable by the very evaluator that had to judge it. History could not be
deleted, a published evaluator could not be changed, and 0.6.0 could not
judge itself.

`WO-REB-004` and its successors answered with two things: a nine-key
`[bootstrap]` tuple in the release contract naming and pinning the
predecessor evaluator, and a compatibility view — a temporary clone with a
sparse specification omitting exactly the rejected pair — in which 0.5.0
could both produce a verdict and author the successor record `RLS-SEH-012`.
It worked. `RLS-SEH-012` exists because of it.

0.6.0 then removed the cause. `REQ-REB-011` made a rejected record valid but
inert. 0.7.0 was the first ordinary release under that rule and needed none of
the machinery: `RLS-SEH-014` rejected, `RLS-SEH-015` released, `REL-SEH-017`
declaring no `[bootstrap]` block.

The machinery stayed, and cost. The 0.6.0 recovery record predicted it
plainly — "the current compatibility code is strongly tied to the exact
rejected 0.6.0 pair. It solves this release but is not yet a general
version-migration framework." Issue #190, on 2026-08-27, recorded three
defects in it, fixed by `WO-REB-024`, `WO-REB-025` and `WO-REB-026`. All three
had one cause: leftover assumptions that the repository still held exactly one
rejected release record, or that a view still applied. Two of the three could
only surface on `workflow_dispatch`, during a live release.

Meanwhile the general framework arrived by another route. `RC-060-01`
delivered `se_harness/governance_migration.py`, a no-network dual-runtime
rehearsal of a predecessor-to-successor handover. It ships in the package and
`check_portable_release_surface.py` already pins its command in the installed
surface.

A read-only sweep on 2026-08-27 measured the remaining path: 6,393 lines
across twelve files deletable whole — 3,851 of them, 63%, of the
`repository_tools` package — plus eight files to edit.

## Decision drivers

- One mechanism for one job. Two mechanisms for the same job is where the
  #190 defects lived.
- The path is already dead for real releases: both remaining call sites take
  their exclusion branch for every ordinary record.
- Defects on a `workflow_dispatch`-only path cannot be caught by
  pull-request CI, so they arrive during a release.
- The closed history must stay verifiable whatever is decided.
- A release freeze forbids `tests/` bytes, which is how the 0.7.0 release
  produced four "no new test" deviations against this same code.

## Considered options

1. **Keep it and fix it forward.** Add the tests the three #190 fixes were
   forbidden from adding, generalize the rejected-record selection, and keep
   both mechanisms. Rejected: it pays maintenance and review cost forever for
   a path with no remaining occasion, and it leaves the structural trap —
   `workflow_dispatch`-only code, frozen during releases — exactly as it is.
2. **Keep the modules, delete only the release-path wiring.** Leave
   `repository_tools` intact but unreferenced. Rejected: 3,851 unreferenced
   lines with a passing test suite read as supported code, and the next
   release freeze would still forbid changing them.
3. **Retire the machinery; keep the history as digest-verifiable facts;
   governance-migration is the sole handover mechanism** — chosen.
4. **Retire the machinery and delete the closed 0.6.0 history with it.**
   Rejected outright: `RLS-SEH-012` is a released record and `REL-SEH-008` and
   `RLS-SEH-009` are the retained record of a real failure. Audit history is
   not deletable, and `REQ-REB-010` and `REQ-REB-011` exist to keep it.

## Decision

Option 3. Delete `release_bootstrap`, `predecessor_preparation`,
`predecessor_publication` and `predecessor_assessment` with their four entry
points and four test modules. Retire the `predecessor-view` qualification
operation and reserve `PV001` and `PV002`. Remove the view branch from the
authorized last mile and the release-bound Pages build, which read the
complete governance snapshot unconditionally. Retire the three schema names
and never reuse them. Supersede `REQ-REB-012` and `REQ-REB-015` and
`SPEC-REB-007`; amend `SPEC-REB-003` and the predecessor-view rules of
`SPEC-REB-005`.

Keep the six closed 0.6.0 artifacts byte-for-byte, and keep
`se_harness/hash_bound_classes.json` unmodified so their evidence digests stay
bound.

Do not touch `scripts/validate_engineering_artifacts.py`. It is a hash-locked
managed copy of released 0.6.0. Its two bootstrap entry points are already
conditional and change no verdict for any active artifact, so they are left in
place; removing them from `templates/repository/standard/`, and retiring
`REQ-REB-010` with them, is a later work order that a release must carry to
the root.

## Consequences

**Positive.** One handover mechanism. 6,393 lines and 48 tests gone. A class
of release-time defect that pull-request CI structurally cannot catch is gone
with the path that produced it. A packaged product module stops lazily
importing an unpackaged repository package. The most complex temporary-clone
and sparse-checkout code in the repository, and the refusals it needed for
symbolic-link traversal, sparse-policy substitution and credential leakage,
all go together.

**Negative, and the reason this is an ADR.** The 0.6.0 preparation and
publication evidence becomes digest-verifiable but no longer reproducible.
Anyone asking "re-run 0.6.0's release under 0.5.0 and show me" will be told
the digests match and the machinery is gone. This is the deliberate,
difficult-to-reverse part of the decision.

**Operational.** Adopters lose one `harnessctl qualify` operation that could
never work from an installed evaluator anyway. Pages and publication behavior
is unchanged in output — the exclusion branch `WO-REB-026` shipped already
produces exactly what the unconditional path will.

**Security.** Net reduction. The removed boundary crossing — a published
evaluator executing against a constructed projection in a temporary clone — is
the surface, and it goes. Isolation (`RID018`), payload proof (`RID021`) and
the hash-bound digests are unchanged.

**Migration.** None for consumers; `repository_tools` is not packaged. For
this repository: two work orders, the second gated on a release, and the
release notes recording the retirement.

**Timing.** `REL-SEH-018` (0.7.1) is in flight as PR #199. A release freeze
forbids `tests/` bytes, which is what forced the four "no new test"
deviations during 0.7.0 against this same code. Approving after 0.7.1 lands
avoids repeating that.

## Validation

`VER-REB-012`: absence of every deleted path and of every import of it;
governor verdict invariance over the closed 0.6.0 history with its evidence
digests still verifying; the publication and Pages lanes green with no
reference to a deleted path; the installed qualification surface without
`predecessor-view` and with `rehearse-migration`; `PV001` and `PV002`
unemitted and reserved.
