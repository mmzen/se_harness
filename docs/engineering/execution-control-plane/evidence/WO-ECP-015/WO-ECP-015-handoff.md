```toml
artifact = "WO-ECP-015"
checkpoint = "handoff"
formal_snapshot_sha256 = "6cbbe31881d82f58716602f4f80f2e67988c55f69177c2b33982f1a6fde8cc5b"
rebound_at = "2026-08-29T11:18:38Z"
```

# WO-ECP-015 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`harnessctl check --artifact ID` with no `--checkpoint` is the projection
`focus` returned: the selected rule, procedure, current step, decision
required, command or response, alternatives and background count, with no
gate evaluated and nothing written (`ECP-ONE-001`, `ECP-ONE-003`). `focus`
remains for one release with unchanged stdout and `--json` bytes and a
deprecation notice on standard error (`ECP-ONE-004`, `ECP-ONE-005`). The
five procedure steps and `WFL-003` name `check` (`ECP-ONE-006`); the
reference, the check note, the overview and the README follow
(`ECP-ONE-008`). `ECP-ONE-007` is not implemented, for the reason in the
deviations; `ECP-ONE-002` holds with one nuance recorded there.

## Evaluators

- Governing: released `se-harness 0.10.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-015-fold-focus-into-check` off
  `main` at `5e5e9d6`; the suite and the demonstrations run candidate
  source.

## Change

- `se_harness/workflow.py`: `focus()` gains an `operation` parameter
  (`"focus"` by default) and names the operation in its refusal; it is the
  one projection behind both entry points.
- `se_harness/cli.py`: `check --checkpoint` is optional; without it
  `_check_projection` refuses any checkpoint-specific option with `WEX210:
  <option> requires --checkpoint`, runs the projection with operation
  `check`, and maps a refusal to `WEX210`; `check` gains
  `--include-background`; `_focus` prints `FOCUS_DEPRECATION` on standard
  error and is otherwise unchanged; both parsers' help texts say so.
- `se_harness/workflow_contract.json` and the template `WORKFLOW.json`
  (byte-identical): the argv of `STEP-WO-START-FOCUS`,
  `STEP-WO-START-FINAL-FOCUS`, `STEP-FOCUS-SELECTED`, `STEP-FOCUS-RELATED`
  and `STEP-REMEDIATE-FOCUS` reads `harnessctl check . --artifact …`;
  identifiers and gate bindings unchanged. `WORKFLOW.md`: `WFL-003`, the
  `next`-or-`check` sentence, the procedure table, the lifecycle-decision
  steps.
- `docs/notes/harnessctl-reference.md` (command table, synopsis, the
  `next`/`check` paragraphs, the renderer list), `harnessctl-check.md`
  (the checkpoint-less form, the checkpoint table, the refusal table),
  `harness-overview.md`, `README.md` (command block and sentence).
- `tests/fixtures/focus_alias/`: `focus`'s stdout and `--json` on the
  standard fixture chain, captured before any product change (the
  fixture chain lacks an assurance classification, so the captured
  projection is a `blocked` one; the bytes are deterministic and carry no
  host path).
- No managed or hash-locked file of this repository moved; the template
  contracts move for the next release.

## Tests

`tests/test_workflow_execution.py::CheckProjectionTests`:

- in `approved`, `in_progress`, `implemented` and `verified`, the
  checkpoint-less `check` and `focus` agree in `selection`, `scope`,
  `state`, `findings`, `procedure`, `compliance` and `mutation`, and in
  `restitution` up to the one `not_done` line that names the operation;
  `operation.kind` reads `check` and `focus`; no gate, no write;
- a `ready` verification record projects `PROC-VREC-DECIDE`;
  `--include-background` is accepted;
- a requirement is refused with `WEX210: check accepts only WO, VREC, or
  RLS artifacts`; `--from-git`, `--target`, `--procedure` and
  `--changes-complete` without a checkpoint are refused with `WEX210:
  <option> requires --checkpoint`;
- the alias's stdout equals the captured fixture byte for byte and its
  `--json` equals it as JSON; standard error carries the notice;
- no contract step's argv names `focus`, the five renamed steps keep their
  identifiers, `WFL-003` names `check`, `WORKFLOW.md` names `harnessctl
  focus` nowhere, the reference names `focus` in exactly one row, and the
  orient core still invokes the alias (see deviations).

Adjusted: `test_focus_implemented_work_with_ready_vrec_recommends_assurance`
expects `STEP-FOCUS-RELATED`'s argv as `check`;
`test_fenced_harness_subcommands_use_the_exact_allowlist` no longer lists
`focus`, which the README no longer fences;
`test_command_reference_exactly_covers_current_cli` is satisfied by the
literal `harnessctl focus` in the reference's deprecation row.

## Suite readings

- Windows 11 workstation (CPython 3.12, CRLF checkout, `7ec98b6`): 1117
  tests, 2 failing names, both present on `main` and outside this work
  order (`test_artifact_authoring…test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  `test_instruction_architecture…test_owner_region_stays_within_the_size_bound`).
- Linux (WSL Ubuntu 24.04, CPython 3.12.3, LF clone at `7ec98b6`): in the
  ledger section.

## Demonstration on this repository

With candidate source on this checkout: `check . --artifact WO-ECP-015`
completes and names `PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-CHECK`; its stdout
equals `focus . --artifact WO-ECP-015`'s byte for byte, with the notice on
standard error; `--json` reads `operation.kind` `check` against `focus`,
`compliance.gates []` and `mutation.writes []` on both; `check . --artifact
REQ-ECP-022` is refused with `WEX210`.

## Readings under the 0.10.0 root

- `validate .`: PASS; maintenance E0/W477.
- `doctor .`: 0 FAIL.
- Review preflight for `WO-ECP-015`: PASS.

## Deviations, recorded for the completion decision

1. **`ECP-ONE-007` is not implemented.** The `harness-orient` core
   (`SKILL.md`, `scripts/orient.py`, `skill-contract.json`) is a frozen,
   digest-pinned surface: its manifest digest is retained history in the
   phase-3 vectors that `test_agentic_execution` and `test_agent_contract`
   hold byte-exact. Changing `orient.py` to invoke `check` moved that
   digest (`73d94b02…` to `97fb7a77…`) and failed three retained-history
   tests, so the edit was reverted. The skill keeps invoking `focus`,
   whose bytes are unchanged inside the alias window, so orientation is
   unaffected; the skill moves to `check` with the alias-removal work
   order, which must re-baseline the vectors in any case. The rule stands
   in `SPEC-ECP-011` and its disposition — accept the deferral by record
   or amend the rule — is the owner's at completion.
2. **`ECP-ONE-002` nuance.** The restitution's `not_done` line names the
   operation ("The selected check operation remains incomplete."), so on a
   blocked projection that one line differs between the two commands by
   the name only; and `result_sha256` is computed over the canonical block,
   which does not carry `operation.kind`, so on a completed projection the
   two digests are equal rather than differing "only through
   operation.kind". The test asserts the identity as it actually holds.
3. `WORKFLOW.md`'s lifecycle-decision step 1 says "no checkpoint: the
   projection" in parentheses, one clause beyond the rule's wording, so a
   reader of the managed document knows which form of `check` it means.

## Complete changed-path set

Every path this work order changed since `main` at `5e5e9d6`, packet
included, as Git derived it (23 paths); the handoff check completed at its
fixed point with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing,
run by the released 0.10.0 evaluator on this Windows checkout:

```
docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-007.md
docs/engineering/execution-control-plane/architecture/ARCH-ECP-001.md
docs/engineering/execution-control-plane/evidence/WO-ECP-015/handoff.json
docs/engineering/execution-control-plane/evidence/WO-ECP-015/WO-ECP-015-handoff.md
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/requirements/REQ-ECP-022.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-011.md
docs/engineering/execution-control-plane/verification/VER-ECP-011.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-015.md
docs/notes/harness-overview.md
docs/notes/harnessctl-check.md
docs/notes/harnessctl-reference.md
README.md
se_harness/cli.py
se_harness/workflow.py
se_harness/workflow_contract.json
templates/repository/standard/docs/engineering/WORKFLOW.json
templates/repository/standard/docs/engineering/WORKFLOW.md
tests/fixtures/focus_alias/human.txt
tests/fixtures/focus_alias/result.json
tests/test_public_onboarding.py
tests/test_workflow_execution.py
```

Linux reading at `7ec98b6` (WSL Ubuntu 24.04, CPython 3.12.3, LF clone):
`python3 scripts/run_tests.py --scale full` OK, 4 skips.
