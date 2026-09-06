+++
id = "WO-ECP-026"
type = "work_order"
title = "Merge adopt into init: one installation command keyed by the target"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the public CLI and the installer every consumer runs first, retires a command name, and closes approved rules by amendment; the release after it ships the result to every consumer."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "tests/test_cli_shape.py",
  "tests/test_harnessctl.py",
  "tests/test_glossary.py",
  "tests/test_repository_context_retirement.py",
  "tests/test_public_onboarding.py",
  "README.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-031.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-020.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-022.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-026.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-003.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-002.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-025.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-034.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-056.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-012.md",
]

[relations]
implements = ["REQ-ECP-031"]
specifications = ["SPEC-ECP-020"]
verification = ["VER-ECP-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:51:57Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-06 by the accountable owner with the words 'i approve', given after the packet PR #359 and its summary were presented, as a decision distinct from the approval of its definitions in the same transaction. Authorizes bounded execution of the declared scope only: the merged init in cli.py and installer.py, the integrity.py diagnostic, the four test modules and one new test, the three notes, the seven amendment records, the domain index, the evidence packet and the verification record. Every decision stays human: no delegation table. It authorizes no release, no publication, no root adoption and no merge; the merges remain the owner's decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-06T10:57:50Z"
decided_by = "engineering-owner"
reason = "Started on 2026-09-06 by the accountable engineering owner with the words 'merged you can start' (DR-WO-START), after PR #359 merged the approved packet to main. Start preflight passed at the approval commit. Execution on branch wo/ecp-026-merge-init-adopt within the declared scope only."
+++

# Work Order: Merge adopt into init: one installation command keyed by the target

## Lifecycle

Draft. Approval is the engineering owner's decision and authorizes bounded
execution of the scope below; it approves no definition, which each
accountable owner approves separately. The owner may add
`[delegation] class = "execution"` before approval to route `DR-WO-START`,
`DR-WO-COMPLETE` and `DR-VREC-PREPARE` through the delegated executor, as
`WO-ECP-025` did; without the table every decision stays human.
Commit-bound verification is `required`: the work ends with a verification
record bound to the candidate commit, verified by the owner before the
merge.

## Objective

Make `init` the one installation command (`ECP-INS-001` to `ECP-INS-005`),
remove `adopt` without a guard (`ECP-INS-006`), reword the one diagnostic
that names it (`ECP-INS-007`), give `--dry-run` its help text
(`ECP-INS-008`), update the three notes with a live reader (`ECP-INS-009`),
close the definitions that name `adopt` by dated amendment record
(`ECP-INS-010`), and move the tests (`ECP-INS-011`).

## In scope

- `se_harness/cli.py`: one `init` parser in place of the two-name loop;
  `_install` decides on the target's content; the help sentence on
  `--dry-run` for `init`, `scaffold-domain` and `create-artifact`.
- `se_harness/installer.py`: `plan_install` without the empty-directory
  refusal and the init/adopt distinction; `upgrade` untouched.
- `se_harness/integrity.py`: the lock-floor diagnostic.
- The four test modules named in `ECP-INS-011` and one new test.
- `README.md`, `docs/notes/harnessctl-reference.md`,
  `docs/notes/harness-installation-and-upgrades.md`.
- The seven amendment records of `ECP-INS-010`; the domain index; this
  work order's evidence packet and its verification record.

## Out of scope

- Any change to `upgrade`, `doctor`, the managed templates, the lock
  format, the adoption report's content or path, the result schema, the
  skills or the workflows.
- Unifying the plan/apply and dry-run conventions across the eight writing
  commands; the reference states the convention, the flags do not move.
- Any release or publication; the root adoption of the release that
  carries this change.

## Authorized decision envelope

The wording of the note sentences and the amendment records; the name and
placement of the new test; whether the human rendering adds one line naming
the report path.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The `candidate-evidence` workflow's bare `init` keeps working.
- The suite, `validate`, `doctor` and the handoff check over the
  Git-derived change set pass before completion.
- No active architecture addresses `REQ-ECP-031`: the requirement is a
  routine command-surface change, not an architecturally significant one,
  so this work order carries no `architecture` relation, as `WO-ECP-025`
  did for `REQ-ECP-030`.

## Expected change surface

About thirty lines net out of `cli.py` and `installer.py`, one string in
`integrity.py`, one set literal and eleven invocations in tests plus one new
test, three note passages, seven short amendment records, this packet.

## Required verification

Execute `VER-ECP-022` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set; a
verification record bound to the candidate commit.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-026/`: the suite
reading on both platforms, `validate` and `doctor` readings, the
`--help` output, the `adopt` refusal, the two target-state plans.

## Stop and escalate conditions

A suite failure beyond the baseline that the change does not explain; any
need to touch a managed path, the lock format or `upgrade`; any consumer
found to invoke `adopt` from automation.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.

## Scope amendment, 2026-09-06

`tests/test_public_onboarding.py` is added to `[execution_scope].paths`. Its
test `test_quick_start_commands_parse_against_the_current_cli` pins the
README quick-start command set to exactly `init`, `adopt` and `doctor`, so
it fails once the README reads as `ECP-INS-009` states; the path was missed
when the scope was drafted. The one purpose of the widening is that
assertion (the set becomes `init` and `doctor`, and the stale search for a
backticked `harnessctl adopt` goes). Decided by the accountable engineering
owner on 2026-09-06 by selecting the presented option "Widen the scope by
amendment". Nothing else is widened.
