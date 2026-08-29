+++
id = "WO-ECP-006"
type = "work_order"
title = "Remove the Phase 4 envelope, bundle and broker; keep the journaled apply; retire the stubbed skills"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The work deletes an execution model reachable from the CLI and from every consumer's installed skills, and keeps its crash-safe apply as retained code; the removal is the largest single deletion since this domain began and later decisions rely on exactly which bytes left, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/delegated_workflow.py",
  "se_harness/delegated_authority.py",
  "se_harness/change_bundle.py",
  "se_harness/repository_state.py",
  "se_harness/runtime_state.py",
  "se_harness/agent_contract.py",
  "se_harness/agent_contract.json",
  "se_harness/effect_contract.json",
  "se_harness/skill_contract.py",
  "se_harness/effect_broker.py",
  "se_harness/journaled_apply.py",
  "se_harness/cli.py",
  "se_harness/mutation_guard.py",
  "pyproject.toml",
  "MANIFEST.in",
  "templates/repository/standard/.agents/skills/harness-draft-change/",
  "templates/repository/standard/.agents/skills/harness-execute-work-order/",
  "templates/repository/standard/.agents/skills/harness-prepare-assurance/",
  "templates/repository/standard/.claude/skills/harness-draft-change/",
  "templates/repository/standard/.claude/skills/harness-execute-work-order/",
  "templates/repository/standard/.claude/skills/harness-prepare-assurance/",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/notes/agentic-execution-host-adapters.md",
  "docs/engineering/agentic-execution/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/verification/VER-ECP-014.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-008.md",
]

[relations]
implements = ["REQ-ECP-018", "REQ-ECP-014"]
specifications = ["SPEC-ECP-006", "SPEC-ECP-007"]
architecture = ["ARCH-ECP-001", "ADR-ECP-002"]
verification = ["VER-ECP-014", "VER-ECP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T13:30:36Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-ECP-006', as a decision distinct from the approval of VER-ECP-014 in the same transaction, on the work order revised in place the same day to the removal of the Phase 4 envelope, bundle, broker path, delegated-workflow command, contract catalogs and skill-contract validator (REQ-ECP-018), the retirement of the three stubbed writing skills taken over from WO-ECP-008 (REQ-ECP-014), and the retention of the journaled apply with its fault matrix. Authorizes start preflight and then only the declared scope. It authorizes no change to a hash-locked root file, no contract file, no supersession transition, no verification record, no release and no publication; the shared write path (REQ-ECP-017) and the delegation class (REQ-ECP-011) remain for later work orders. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T13:30:42Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-ECP-006'. Start preflight PASS with no diagnostics over the approval commit 62a8d42 carrying unmoved main 78306e0, run with the governing exact public 0.10.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no supersession transition, no verification record, no release and no publication."
+++

# Work Order: Remove the Phase 4 envelope, bundle and broker; keep the journaled apply; retire the stubbed skills

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Revised in place on 2026-08-29, before any lifecycle event, from the
2026-08-27 draft that carried removal, the shared journaled write path and
the delegation class together: this work order now carries the removal
(`REQ-ECP-018`, `ECP-DLG-008`) and the retirement of the stubbed skills
(`REQ-ECP-014`, `ECP-SKL-001` to `ECP-SKL-004`, taken over from
`WO-ECP-008`), and *retains* the journaled apply as code with its fault
matrix without yet wiring it into every harness-owned write. The shared
write path (`REQ-ECP-017`, `ECP-JNL-001` to `ECP-JNL-006`) and the
delegation class (`REQ-ECP-011`, `ECP-DLG-001` to `ECP-DLG-007`,
`ECP-DLG-009`) follow under later work orders; `SPEC-ECP-006` is not
amended, its rules are implemented in three steps. Its predecessors
`WO-ECP-003` (`VREC-ECP-014`) and `WO-ECP-009` (`VREC-ECP-009`) are
verified and merged.

## Objective

Execute the decision of `ADR-ECP-002` (and `ADR-AEX-008`): the ephemeral
envelope, the nonce ledger, the content-addressed change bundle, the
proposed-workspace broker path, `harnessctl delegated-workflow`, the agent
and effect contract catalogs, the skill-contract validator and the three
writing skills that only stub the evaluator leave the product; the journaled
apply with rollback and `human-recovery-stop` survives as
`se_harness/journaled_apply.py` with its fault matrix, over explicit
`(path, pre-image, post-image)` targets and without any bundle, envelope or
receipt. Audit item P0 of 2026-08-29.

## Why now

The decision is three days old and nothing has started it; every cycle since
has run the command-driven kernel by hand while 8,876 lines (39 % of the
package, three CLI tests) sit beside it as a second execution model that
every agent must recognise and ignore, and three consumer-installed skills
print `"evaluator_invoked": false`. The gate that replaces the broker
(`WO-ECP-003`, `WO-ECP-013`, `WO-ECP-016`) is on `main` and governs this
repository.

## In scope

- Deletion of `se_harness/delegated_workflow.py`, `delegated_authority.py`,
  `change_bundle.py`, `repository_state.py`, `runtime_state.py`,
  `agent_contract.py`, `agent_contract.json`, `effect_contract.json` and
  `skill_contract.py`; `cli.py` loses the `delegated-workflow` subparser,
  its handlers and the Phase 4 entries of its exception tuple;
  `mutation_guard.PUBLIC_MUTATION_OPERATIONS` loses the four delegated
  operation names; `pyproject.toml` package data loses the two JSON mirrors
  (`ECP-DLG-008`).
- `se_harness/effect_broker.py` reduced to `se_harness/journaled_apply.py`:
  the journal written before the first replace, replace in journal order,
  rollback to pre-images, `human-recovery-stop` on a rollback failure, and
  recovery from a journal; no authority guard, object store, bundle,
  envelope, nonce or receipt. `tests/test_effect_broker.py`'s eleven
  fault-matrix tests are re-pointed at it in `tests/test_journaled_apply.py`,
  the Windows held-open case included; no command is wired to it yet.
- Removal of `harness-draft-change`, `harness-execute-work-order` and
  `harness-prepare-assurance` from `templates/repository/standard/.agents/skills/`
  and `.claude/skills/`; `harness-orient` and `harness-operator-brief`
  stay; a test over the template tree asserts `ECP-SKL-003`; the installer
  needs no change because it walks the template tree (`ECP-SKL-004` holds
  by construction; `doctor` in an upgraded consumer reports `remove`).
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `validate_agentic_delegations` and `E021` removed with the
  `[agentic_delegation]` table; `WORK_ORDER.template.md` names no such
  table; the root copy stays at 0.10.0 and the divergence is declared in
  `tests/test_validation_taxonomy.py`.
- Tests: the six Phase 4 modules (68 tests) removed; the seven partially
  dependent modules updated; the skill-manifest helper the orientation
  vectors need moves into `tests/fixture_support.py`; the phase-3 and
  phase-4 vector fixtures stay byte-unchanged as history and the tests that
  asserted the three writing skills' live cores are removed with the skills.
- Amendment records, each a trailing `## Amendment record` with no
  front-matter change, on `ADR-AEX-006`, `ADR-AEX-007`, `ARCH-AEX-002` and
  the `agentic-execution` README, stating what `ADR-ECP-002` supersedes and
  what is retained. Formal supersession transitions of the `AEX` artifacts
  with an `ECP` successor (`REQ-AEX-002` by `REQ-ECP-018`; `REQ-AEX-010`,
  `REQ-AEX-011`, `REQ-AEX-012`, `SPEC-AEX-003`, `SPEC-AEX-006`,
  `SPEC-AEX-007`, `SPEC-AEX-008` by `SPEC-ECP-006`'s rules as they land)
  are the requirements steward's and technical owner's separate acts, taken
  by name at this work order's completion or later; this work order writes
  the amendment records only.
- `docs/notes/harnessctl-reference.md` loses the `delegated-workflow` row;
  the two skill notes describe what remains.
- The packet, this domain's index (its stale "every artifact is draft"
  paragraph included), and `WO-ECP-008` revised to drop the skill item it
  hands over.

## Out of scope

The shared journaled write path for `transition`, `evidence`,
`capture-verification`, `prepare-release`, `create-artifact` and
`upgrade` (`REQ-ECP-017`); `harnessctl recover`; the delegation class and
the CI check-run reader (`REQ-ECP-011`); any root managed copy (the root
`.agents/skills/`, `.claude/skills/` and `scripts/` move at the next root
adoption); any contract file (`workflow_contract.json`,
`quality_gates_contract.json`); front matter of any amended artifact;
`WO-ECP-008`'s manifest and snapshot items; the release carrying this
change.

## Authorized decision envelope

The internal shape and name of the retained journal module and its target
representation; which private helpers of `effect_broker.py` survive; test
names and the layout of the re-pointed fault matrix; the amendment prose;
the wording of the notes. It may not keep any envelope, bundle, nonce,
receipt or `delegated-workflow` symbol reachable from the CLI or the
package's public modules, keep a skill whose script stubs the evaluator,
apply any supersession transition itself, edit a hash-locked root file, or
write outside the listed paths.

## Constraints

- The exact released evaluator, se-harness 0.10.0, outside the checkout
  with `-I`, for identity, integrity, graph, preflight and every transition.
- Stage every deletion before any preflight or check run (`hash_bound`
  reads index-tracked paths).
- The phase-1, phase-3, phase-4 and phase-5 vector fixtures are
  byte-unchanged.
- The Windows held-open fault case runs on Windows, not skipped; the Linux
  lane runs the whole matrix.
- `check`'s stdout and `--json` bytes are unchanged.

## Expected change surface

Nine product files deleted and one reduced-and-renamed, the CLI and the
mutation guard, packaging metadata, fifteen skill files deleted, the
template validator and work-order template, thirteen test modules (six
deleted, one added, six updated) and one fixture helper, four amendment
records, three notes, the index, the packet, and `WO-ECP-008`.

## Required verification

Execute `VER-ECP-014` in full and `VER-ECP-007`'s scenarios 5 and 6;
repository-required checks; the whole suite on Linux and Windows with
figures labelled per platform; the pull request's lanes; the handoff check
over the Git-derived change set.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-006/`: the
fault-matrix figures per platform, the wheel `RECORD` and symbol walk
showing no removed name, the `harnessctl --help` walk, the template-tree
skill census, the amendment diffs, per-platform suite figures, and the
complete changed-path set.

## Stop and escalate conditions

Stop if the journaled apply cannot be separated from the broker without
losing a fault-matrix case; if a retained module or script still needs a
removed symbol; if the released evaluator refuses the edited template
validator; if an amended artifact's front matter would have to change; or
if any path outside scope must change.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
