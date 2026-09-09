+++
id = "WO-ECP-038"
type = "work_order"
title = "Retire the canonical_json_bytes alias of release_build"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "not_required"
rationale = "One import line and two calls in a repository-owned lane script move to the name WO-ECP-032 gave the function, and the alias line goes; the function's bytes are unchanged, every recipe digest on record stays, and the two hosted lanes that run the script exercise the change on the pull request."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/release_build.py",
  "scripts/replay_release_build.py",
  "tests/test_release_build.py",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-038.md",
  "docs/engineering/execution-control-plane/evidence/WO-ECP-038/",
]

[relations]
implements = ["REQ-ECP-034"]
specifications = ["SPEC-ECP-023"]
verification = ["VER-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T12:48:33Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-09 by selecting the presented option 'Approve; start, change and complete on this branch (Recommended)' after reviewing PR #430: an import rename in the replay lane script and the alias line removed, no byte of output changing, commit-bound verification not required; the same decision covers the start and the completion on this branch, each recorded as its own event."
+++

# Work Order: Retire the canonical_json_bytes alias of release_build

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `not_required`:
the change is a name, not a byte of output.

## Objective

`ECP-PRM-009` of `SPEC-ECP-023` renamed `release_build.canonical_json_bytes`
to `recipe_json_bytes` so that the recipe form (sorted keys, two-space
indent, non-ASCII kept) and the integrity primitive of the same name (compact
separators) stop sharing one name. `WO-ECP-032` kept a one-line alias
because `scripts/replay_release_build.py`, a lane script outside its scope,
imports the old name; its evidence packet's disclosure 2 left the removal
to a later work order. Move the script's import and its two calls to
`recipe_json_bytes`, delete the alias, and prove that no byte of any recipe
or replay document changes.

## In scope

- `scripts/replay_release_build.py`: the import and its two calls read
  `recipe_json_bytes`.
- `repository_tools/release_build.py`: the alias line and its comment go;
  the function, its docstring and its bytes are unchanged.
- `tests/test_release_build.py`: one test that the module no longer exposes
  the old name and that the replay script names the new one.
- This domain's index and the evidence packet.

## Out of scope

Any change to the recipe form, the replay document, the build recipe, the
toolchain lock or any digest; any other name of `release_build`; the
`canonical_json_bytes` of `repository_tools/json_bytes.py` and of
`.github/scripts/build_integration_package.py`, which are the integrity
primitive and its local wrapper, correctly named.

## Authorized decision envelope

The test's name and placement.

## Constraints

- `recipe_json_bytes` is byte-identical before and after: no line of its
  body changes.
- `repository_tools` keeps importing only the standard library and its own
  package (`ARCH-REB-013`).
- No workflow file changes; the two lanes that run the script
  (`release-qualification.yml`, `release-candidate-replay.yml`) are the
  reading, not the change.

## Expected change surface

Three code lines in the script, two lines removed from the module, one
test, the domain index, this work order and its evidence packet.

## Required verification

`tests/test_release_build.py` and the full suite on Windows; the released
evaluator's `validate` and `preflight`; the Publication Rehearsal lane at
the pull request head, whose candidate leg runs the script; the handoff
check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-038/`: the
handoff packet the gate requires at the handoff checkpoint.

## Stop and escalate conditions

A change to any byte `recipe_json_bytes` writes; a lane that fails on the
renamed import; any other caller of the old name found in the package or
the tools.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
