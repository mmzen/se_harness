+++
id = "SPEC-DST-022"
type = "specification"
title = "Retirement of managed paths that leave the managed set"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-DST-066"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:06:36Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'I approve the definitions packet', for the repair of issue #271: the DST-UPR-001..008 retirement rules over plan_install and apply_changes, with amendment records on SPEC-DST-001 and SPEC-ECP-007. Measured before this transition over branch state 6f1fd05 carrying unmoved main d3b5a3f: validate reads 0 errors; start preflight reads only the draft signature. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Specification: Retirement of managed paths that leave the managed set

## Scope

The upgrade planning and application rules of `se_harness/installer.py` for
prior-lock entries whose paths the installed evaluator's managed set no
longer names. Issue #271. `SPEC-DST-001`'s upgrade contract is amended by
record to add `remove` to the action vocabulary; `SPEC-ECP-007`'s
`ECP-SKL-004` is amended by record to name `upgrade`, not `doctor`, as the
reporter of the removals. The conflict, evidence and transaction rules of
`SPEC-REB-002` and `SPEC-REB-012` stay.

## Terms

- **Managed set:** the deterministic manifest `template_files()` derives from
  `templates/repository/standard/`, keyed by target path.
- **Leaving-set entry:** a `files` entry of the prior lock whose path is not
  a managed-set target path.

## Behavioral rules

**DST-UPR-001:** In `upgrade` mode, after classifying the managed set,
`plan_install` classifies every leaving-set entry of mode `managed` or
`fragment`: tracked content on disk that matches the entry's recorded digest
under the lock-schema-aware canonical comparison (admitting the schema-1
legacy newline variant) plans as `remove`; tracked content that differs
plans as `customized`; a path with no file on disk plans nothing and its
entry leaves the written lock. A leaving-set `seed` entry plans nothing and
its file is never touched: seed content is owner-owned from installation.
Every leaving-set path resolves through the same containment checks as a
template destination and fails closed.

**DST-UPR-002:** Applying a `remove` of a `managed` path deletes the file
and removes the directories the deletion leaves empty, ascending no further
than the target root. Applying a `remove` of a `fragment` path rewrites the
file with the managed block spliced out, and deletes the file only when the
remainder is empty or whitespace.

**DST-UPR-003:** `apply_changes` executes `remove` actions only when updates
are allowed, inside the same pre-write-snapshot transaction as the writes;
any failure restores every deleted or rewritten file.

**DST-UPR-004:** The written lock contains no entry for a removed path, and
the transition replay postcondition — a second plan reads as a no-op —
holds after an apply that removed files.

**DST-UPR-005:** A `customized` leaving-set copy stops `--apply` before any
write, exactly as an in-set customization does, and the CLI lists its path
in the same manual-review report.

**DST-UPR-006:** With `--evidence-output`, `remove` actions are recorded in
the evidence document's `plan` alongside `add`, `integrate`, and `update`;
the document keeps the `se-harness-evaluator-upgrade-evidence-v1` schema and
its canonical form (`SPEC-REB-012` rule 4), the new action value being
additive.

**DST-UPR-007:** A conformance test in
`tests/test_standard_repository_lifecycle.py` builds a root whose lock
manages the fifteen 0.10.0 skill paths that 0.11.0 retired
(`.agents/skills/harness-draft-change/`,
`.agents/skills/harness-execute-work-order/`,
`.agents/skills/harness-prepare-assurance/`, four files each, and the three
`.claude/skills/<name>/SKILL.md` adapters) and asserts the `remove` plan,
the deletion with directory pruning, the lock omission, the `customized`
refusal for an edited copy, and the restoration after an interrupted apply.

**DST-UPR-008:** `docs/notes/harness-installation-and-upgrades.md` states
that an upgrade removes byte-identical managed files that left the managed
set, and lists the fifteen retired 0.10.0 skill paths for consumers that
already upgraded to 0.11.0 and must delete the orphans by hand.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-DST-066 | DST-UPR-001 to DST-UPR-008 |

## Inputs and outputs

Inputs: the prior `.engineering-harness.lock`, the installed managed set,
the bytes on disk, `--apply`, `--evidence-output`. Outputs: the plan with
`remove` entries, the deletions, the rewritten lock, the evidence document,
the manual-review refusal.

## Error and recovery behavior

A leaving-set path that escapes the target or traverses a symlink refuses
the plan (`safe_destination`); unreadable or non-UTF-8 tracked content
refuses with the existing bounded messages; a failed transaction restores
the pre-write snapshot, including deleted files.

## Compatibility and migration

A consumer on a 0.10.0 root upgrading with a fixed evaluator loses the
fifteen retired files mechanically. A consumer already on 0.11.0 carries a
lock that no longer names them; no evaluator can retire them mechanically,
and the note of `DST-UPR-008` is the remediation. Locks and evidence keep
their schemas; no stored digest moves.

## Explicitly unspecified decisions

The helper structure inside `installer.py`; the exact wording of the plan
line, the note, and the amendment records; the fixture bytes the tests use.
