+++
id = "REQ-DST-066"
type = "requirement"
title = "An upgrade retires managed files that leave the managed set"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN `upgrade` finds a lock-managed path absent from the installed evaluator's managed set, THE SYSTEM SHALL retire it — planned as `remove`, deleted on apply in one transaction, omitted from the written lock — so that no orphaned managed copy survives the upgrade."
verification_method = ["test"]
priority = "must"
source = "issue #271; upgrade rehearsal of 2026-08-29 on a clone of main 896f8fa with the published 0.11.0 evaluator"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: An upgrade retires managed files that leave the managed set

## Rationale

`plan_install(mode="upgrade")` classifies only the paths of the installed
evaluator's own managed set (`se_harness/installer.py`, the `_templates()`
loop). A path the prior lock manages that the new set no longer names appears
in no plan, is never written or deleted, and silently leaves the rewritten
lock. Rehearsed on 2026-08-29 on a throwaway clone of `main` `896f8fa` (root
0.10.0, 61 managed files) with the published 0.11.0 evaluator installed
outside the checkout: `upgrade .` plans 46 files with 9 updates; the fifteen
files of the three skills 0.11.0 retired appear nowhere; `--apply` writes a
46-file lock and leaves the fifteen on disk; `doctor` reads 0 FAIL and
`qualify released-root` passes 113/113. Every consumer that upgrades
0.10.0 to 0.11.0 keeps three orphaned skill directories whose `SKILL.md`
tells an agent to run a `delegated-workflow` command that no longer exists,
and whose `.claude` adapters still register with Claude Code. `SPEC-ECP-007`
`ECP-SKL-004` states the removed skill files are reported as `remove`; no
code implements that today.

## Behavior

- Trigger: `harnessctl upgrade` plans or applies against a root whose lock
  `files` name a `managed` or `fragment` path that is not in the installed
  evaluator's managed set.
- Response: the plan classifies the path as `remove` when its tracked bytes
  still match the lock's recorded digest; apply deletes the managed content
  inside the one pre-write-snapshot transaction and writes a lock without the
  entry; the replay postcondition still reads as a no-op.
- On failure: tracked bytes that differ from the recorded digest are reported
  as `customized` and stop `--apply` before any write, exactly as an in-set
  customization does; a path with no file on disk retires silently as its
  entry leaves the lock; prior `seed` entries are owner content and are never
  deleted.

## Assumptions and dependencies

- The prior lock's `files` digests are trustworthy for equality comparison;
  their paths are untrusted input and resolve through the same containment
  checks as template destinations.
- Consumers already upgraded to 0.11.0 carry a lock that no longer names the
  orphaned paths; no later evaluator can see them mechanically, so their
  remediation is documented manual deletion.

## Acceptance examples

### Example: normal behavior

**Given** an installed root whose lock manages the fifteen 0.10.0 skill files
that 0.11.0 retired, with bytes matching their recorded digests.

**When** `upgrade` plans and then applies.

**Then** the plan lists the fifteen paths as `remove`, apply deletes them and
prunes the directories they leave empty, the written lock does not name them,
and a replay plans no change.

### Example: failure behavior

**Given** the same root with one of the fifteen files carrying an owner edit.

**When** `upgrade . --apply` runs.

**Then** the path is reported as `customized`, the transaction refuses before
any write, and every file keeps its bytes.

## Open decisions

None.
