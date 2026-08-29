```toml
artifact = "WO-ECP-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "9611832861c34815c90b2fa76367538ee14a4b3a8a257124edc820282fbae843"
rebound_at = "2026-08-29T12:39:44Z"
```

# WO-ECP-017 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`harnessctl` has no `focus` subcommand; a script still calling it exits 2
with one line on standard error naming `harnessctl check --artifact ID`
(`ECP-RMV-001`, `ECP-RMV-002`). The projection is one function under one
name (`ECP-RMV-003`). The template `harness-orient` core invokes `check`
where it invoked `focus` - the `ECP-ONE-007` rule of `SPEC-ECP-011`
deferred at the completion of `WO-ECP-015` - and probes for an optional
`--checkpoint` first (`ECP-RMV-004`). A phase-5 vector row records the new
orientation identity with the phase-4 and phase-1 identities as its
`previous`; those fixtures are byte-unchanged (`ECP-RMV-005`). The alias
tests and captured fixture are gone (`ECP-RMV-006`); the notes, the
template README seed and the owner region of this repository's `AGENTS.md`
say `check` (`ECP-RMV-007`).

## Evaluators

- Governing: released `se-harness 0.10.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-017-remove-focus-alias` off
  `main` at `01f648f`; the suite and the demonstrations run candidate
  source.

## Change

- `se_harness/cli.py`: `_focus`, `FOCUS_DEPRECATION` and the parser branch
  deleted; `main()` guards `focus` before parsing.
- `se_harness/workflow.py`: `focus()` is `project_selected()`, without the
  `operation` parameter; refusals name `check`.
- `se_harness/workflow_compliance.py`: the `focus_schema2` wrapper delegates
  to `project_selected` (its name is kept; see deviation 1).
- `templates/.../harness-orient/scripts/orient.py`, `SKILL.md`: probe
  `check --help` for `--json`, `--artifact` and `[--checkpoint`; invoke
  `check TARGET --artifact ID --json`; operation identifiers unchanged.
- `tests/fixtures/agentic_execution/phase5/portable-vectors.json` (new):
  `orientation.{previous,current}`, `portable_core.{previous,current}`;
  `previous` manifest `73d94b02...`, `current` `0ce5d5a1...`.
- `tests/fixtures/focus_alias/` removed; `fake_evaluator.py` advertises
  `check`, mode `no-check`.
- `tests/test_workflow_execution.py`, `test_agentic_execution.py`,
  `test_agent_contract.py`: alias tests removed, projection tests renamed
  to `check`, the three "current" pins moved to the phase-5 row, a refusal
  test and a word-census test added.
- Notes, `README.md.seed`, the `AGENTS.md` owner region; the packet; the
  domain index.

## Tests

- `CheckProjectionTests.test_focus_is_refused_with_its_replacement_named`:
  `--help` lists no `focus`; `focus ... --artifact WO-001 --json` exits 2
  with empty stdout and stderr naming `harnessctl check --artifact WO-001`;
  bare `focus` names `--artifact ID`.
- `test_every_state_projects_with_no_gate_and_no_write`: four states through
  `check`, no gate, no write.
- `test_nothing_names_focus_but_the_note_that_records_its_removal`: no
  contract step argv, no reference row, one `focus` in the check note beside
  "removed", `orient.py` invokes `check` and never `["focus"`.
- `test_exact_0_5_without_check_degrades_only_selected_scope`: the fake
  evaluator without `check` degrades with `AEXORI030` / `focus-json`.
- `test_canonical_harness_orient_contract_and_manifest_validate`,
  `test_retained_phase3_vectors_are_preserved_and_orientation_is_byte_exact`,
  `test_phase1_receipt_bytes_and_portable_core_identity_remain_compatible`:
  phase-1 `portable_core` and phase-4 `orientation` equal the phase-5
  `previous`; the live core equals the phase-5 `current`.
- `test_projection_digest_equals_the_released_evaluator_golden`: the
  `result_sha256` pin `b8ccd288...` holds through `check` (the digest never
  carried `operation.kind`).

## Suite readings

- Windows 11 workstation (CPython 3.14, CRLF checkout, `c1670cd`): 1194
  tests, 27 skipped, 2 failing names, both present on `main` and outside
  this work order (`test_artifact_authoring...test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  `test_instruction_architecture...test_owner_region_stays_within_the_size_bound`).
- Linux: the pull request's suite lane, in the hosted-lanes section.

## Demonstrations on this repository

- Candidate CLI: `python -m se_harness --help` lists no `focus`;
  `python -m se_harness focus . --artifact WO-ECP-017` prints
  `harnessctl: focus was removed after 0.10.0; run harnessctl check
  --artifact WO-ECP-017 (add --json for the structured result)` and exits 2.
- The moved `orient.py` against the released 0.10.0 evaluator (Windows
  paths, `-I`): `version`, `identity`, `doctor`, `validate-json`,
  `inspect-json` and `focus-help` pass; `check --help` there still requires
  `--checkpoint`, so the projection is `not_assessable` and the outcome is
  `degraded` with `AEXORI030` - the same degradation the 0.5.0 profile
  produces, and the reason the probe exists. Before the probe was added the
  same run was `blocked` on `harnessctl check: error: the following
  arguments are required: --checkpoint`.
- The moved `orient.py` against candidate source is outside the skill's
  contract (it orients through the released evaluator; a candidate launcher
  fails identity with `RID003`/`RID004`), so the candidate happy path is
  the fake-evaluator test and `CheckProjectionTests`.

## Readings under the 0.10.0 root

- `validate .`: 1139 artifacts, 0 errors, 479 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (7 records).
- Start preflight for `WO-ECP-017`: PASS over `59e130e`.
- `git diff --stat main -- canonical_vectors.json phase3 phase4`: empty.

## Deviations, recorded for the completion decision

1. **`ECP-RMV-003` names `workflow_compliance.focus_selected`, which does
   not exist.** The wrapper is `focus_schema2`, whose only caller is
   `delegated_workflow.py` (Phase 4, outside this scope). It is kept under
   its name and delegates to `project_selected`; renaming it belongs with
   the Phase 4 decision (audit P0).
2. **`ECP-RMV-004` gained a probe.** Beyond "invoke `check` where it invoked
   `focus`", the core now requires `[--checkpoint` in `check --help`, because
   a 0.10.0 evaluator accepts `--artifact` and `--json` yet refuses the
   checkpoint-less form; without the probe a consumer on 0.10.0 with the
   0.11.0 skill core would block instead of degrade. Within the decision
   envelope; recorded because the rule's text does not say it.
3. **Scope amendment** of 2026-08-29 adding `tests/test_agent_contract.py`
   (the third "current" pin), recorded on the work order.

## Complete changed-path set

Every path this work order changed since `main` at `01f648f`, packet
included, as Git derived it (24 paths); the handoff check completed at its
fixed point with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing,
run by the released 0.10.0 evaluator on this Windows checkout:

```
AGENTS.md
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/evidence/WO-ECP-017/WO-ECP-017-handoff.md
docs/engineering/execution-control-plane/evidence/WO-ECP-017/handoff.json
docs/engineering/execution-control-plane/requirements/REQ-ECP-024.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-013.md
docs/engineering/execution-control-plane/verification/VER-ECP-013.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-017.md
docs/notes/harness-orient.md
docs/notes/harnessctl-check.md
docs/notes/harnessctl-reference.md
se_harness/cli.py
se_harness/workflow.py
se_harness/workflow_compliance.py
templates/repository/standard/.agents/skills/harness-orient/SKILL.md
templates/repository/standard/.agents/skills/harness-orient/scripts/orient.py
templates/repository/standard/docs/engineering/README.md.seed
tests/fixtures/agentic_execution/fake_evaluator.py
tests/fixtures/agentic_execution/phase5/portable-vectors.json
tests/fixtures/focus_alias/human.txt
tests/fixtures/focus_alias/result.json
tests/test_agent_contract.py
tests/test_agentic_execution.py
tests/test_workflow_execution.py
```

## Hosted lanes

Read on the pull request at its heads; recorded in the pull-request body
and the verification record.
