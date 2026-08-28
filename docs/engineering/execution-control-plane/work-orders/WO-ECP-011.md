+++
id = "WO-ECP-011"
type = "work_order"
title = "Delete the retired governance-migration stage machine now that the root is 0.8.0"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The work deletes product files that the wheel still ships, removes a registered interpreter-safety boundary from the declaration every evaluator loads, and moves the retired members to the forbidden set of the portable-surface check that gates every release; each is trusted engineering state that later release decisions depend on, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/governance_migration.py",
  "se_harness/governance_migration_contract.py",
  "se_harness/governance_migration_contract.json",
  "se_harness/interpreter_safety.json",
  "tests/fixtures/governance_migration/",
  "tests/test_interpreter_safety.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_upgrade_rehearsal.py",
  "tests/test_standard_repository_lifecycle.py",
  "pyproject.toml",
  "scripts/check_portable_release_surface.py",
  ".gitattributes",
  "docs/notes/",
  "docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-010.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-012"]
specifications = ["SPEC-ECP-007"]
verification = ["VER-ECP-007"]
+++

# Work Order: Delete the retired governance-migration stage machine now that the root is 0.8.0

## Lifecycle

This work order requires the accountable engineering owner's approval before
start preflight or any declared work. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It is the follow-up `WO-ECP-010` deferred on
the owner's decision "Land the rehearsal now, delete after the root advances"
(its evidence, disclosure 1) and the last open item of issue #210.

Commit-bound verification is `required`: the deletion changes what the wheel
ships and what the portable-surface check forbids.

## Objective

Delete the four files `WO-ECP-010` retained dead, the owner-region
`.gitattributes` rules that pinned them, the interpreter-safety boundary
registered for the deleted module and the test exemptions that named the
retention, and move the retired wheel members to the forbidden set — so that
issue #210's second acceptance criterion ("no JSON in `se_harness/` embeds a
digest of a Python module") is proven without exemption and the product
carries nothing of the retired stage machine.

## Why now

Released 0.7.1, the root until today, shipped the `repository`-region
hash-bound class `governance-migration-protocol` and refused any tree where
its patterns matched no tracked file. `WO-HUP-008` moved the root to exact
public 0.8.0 (merged as `6573bd8`), which carries `WO-HBI-005` and declares no
such class. Rehearsed on 2026-08-28 on a throwaway export of `main` at
`6573bd8` with the four files, the three rules and the boundary entry
removed and the test changes below applied: 0.8.0 `doctor` 0 FAIL, `validate`
0 errors, the portable-surface repository check PASS, and the full suite
1009 tests with only the known workstation file-mode failure that passes
hosted (`test_declared_mode_set_is_what_a_posix_export_already_carries`).

## In scope

- Delete `se_harness/governance_migration.py`,
  `se_harness/governance_migration_contract.py`,
  `se_harness/governance_migration_contract.json` and
  `tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json` (with
  its now-empty directory); drop `governance_migration_contract.json` from
  `pyproject.toml`'s package data.
- Remove the three owner-region `.gitattributes` rules and the comment that
  explained their retention.
- Remove the boundary `se_harness.governance_migration.runtime_probe` from
  `se_harness/interpreter_safety.json`; the deleted module was its only
  subject. `WO-ECP-010` recorded the module as having "no importer, no
  test"; that was true of product importers and of `tests/` by module name,
  but `tests/test_interpreter_safety.py` imports it for the `MIG2xx` refusal
  map and the boundary inventory names it — both go with it. With one
  boundary left, `test_declaration_rejects_an_unsorted_boundary_registry`
  must insert an out-of-order synthetic entry instead of reversing the list.
- Amend `ARCH-REB-010` by dated amendment: its identity-boundary list names
  `se_harness/governance_migration.py`; the boundary no longer exists and the
  registry check enumerates one rule boundary (`runtime_identity`). The
  architecture's decision is unchanged.
- `scripts/check_portable_release_surface.py`: `RETIRED_MIGRATION_MEMBERS`
  joins `FORBIDDEN_MEMBERS` (wheel) and `FORBIDDEN_ACTIVE_PATHS`
  (repository); the "neither required nor forbidden" comment goes.
- `tests/test_upgrade_rehearsal.py`: `RETAINED_UNTIL_ROOT_ADVANCES` and the
  JSON exemption go; the reserved-names test asserts the four paths are
  absent and the owner rules gone, and that the surface check forbids the
  members. `tests/test_hash_bound_integrity.py`'s out-of-scope-digest test
  stops reading the deleted contract. `tests/test_standard_repository_lifecycle.py`
  asserts the owner rules present under a 0.7.1 root and absent otherwise.
- Correct the notes that still describe the retention
  (`docs/notes/` where they name the four files as retained).
- Retain evidence under `docs/engineering/execution-control-plane/evidence/WO-ECP-011/`.

## Out of scope

`se_harness/interpreter_safety.py`, its `repository_tools` copy and the rest
of the declaration apparatus (issue #220, bound by `ARCH-REB-010`); the
`governance-migration` CI job name (it names the upgrade-rehearsal lane and
stays); historical evidence, records and the retired definitions that
mention the stage machine; `WO-ECP-007`'s other evictions; anything under
`templates/`; the released 0.8.0 and the lock.

## Authorized decision envelope

The form of the identity-aware assertions, provided both root states are
still asserted; the wording of the amendment and the notes; the order of
readings.

## Constraints

- The 0.8.0 root governs: every reading is taken with the released 0.8.0
  evaluator outside the checkout in isolated mode; a refusal is a stop.
- No product behaviour changes: no CLI surface, no evaluator rule, no
  managed template byte moves.
- The rehearsal lane (`repository_tools/upgrade_rehearsal.py`) is untouched.

## Expected change surface

The four deleted files and directory, `pyproject.toml`, `.gitattributes`,
`se_harness/interpreter_safety.json`, `scripts/check_portable_release_surface.py`,
the four test modules, `ARCH-REB-010`, the notes, the domain index, this
packet and the evidence.

## Required verification

`VER-ECP-007`'s product-boundary readings that apply: `validate` 0 errors
and `doctor` 0 FAIL under 0.8.0; `check_portable_release_surface.py
--repository .` PASS and `--wheel` PASS on a locally built candidate wheel
that no longer contains the members; the full suite; the pull request's
lanes green (the candidate-evidence lane builds the wheel and runs the
surface check hosted); the handoff check over the complete changed-path set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-011/WO-ECP-011-verification.md`.

## Stop and escalate conditions

A 0.8.0 `doctor` or `validate` failure after the deletion, a wheel that still
carries a member, a test that cannot assert both root states, any change
needed under `templates/` or to `interpreter_safety.py`, or a need for
authority beyond the approved stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
