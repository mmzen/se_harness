```toml
artifact = "WO-ECP-006"
checkpoint = "handoff"
formal_snapshot_sha256 = "ef269cd3a31c54d26524a816fde87c0b009ea6f6eaa44900b63ff908c07f14fd"
rebound_at = "2026-08-29T13:54:52Z"
```

# WO-ECP-006 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The Phase 4 envelope, bundle and broker are out of the product: eight
modules and two contract catalogs deleted, the `delegated-workflow`
subcommand and its four delegated operation names gone, the two catalogs
out of package data (`REQ-ECP-018`, `ECP-DLG-008`). The journaled apply
survives as `se_harness/journaled_apply.py` with its fault matrix
re-pointed (`ADR-ECP-002`). The three writing skills that stubbed the
evaluator are retired from the template with their `.claude` adapters and
packaging entries (`REQ-ECP-014`, `ECP-SKL-001` to `ECP-SKL-004`). The
`[agentic_delegation]` table and its validator leave the candidate template.
Amendment records sit on `ADR-AEX-006`, `ADR-AEX-007`, `ARCH-AEX-002` and
the `agentic-execution` README. Audit item P0.

## Evaluators

- Governing: released `se-harness 0.10.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-006-remove-phase4` off `main`
  at `78306e0`; the suite, the wheel and the demonstrations run candidate
  source.

## Change

- Deleted: `se_harness/delegated_workflow.py`, `delegated_authority.py`,
  `change_bundle.py`, `repository_state.py`, `runtime_state.py`,
  `agent_contract.py`, `agent_contract.json`, `effect_contract.json`,
  `effect_broker.py` (8,876 lines with the two catalogs).
- Added: `se_harness/journaled_apply.py` (`Target`, `apply_journaled`,
  `recover_journaled`, `read_journal`): journal before the first replace,
  replace in journal order, rollback to backed-up pre-images,
  `human-recovery-stop` with `WEX-ECP-041`, refusal of any apply while a
  stop journal exists with `WEX-ECP-042`, the stale-input check of
  `ECP-JNL-005`; over explicit `(path, pre-image, post-image)` targets and a
  caller-chosen journal directory; no bundle, envelope, token, receipt or
  session. Not wired into any command (that is `REQ-ECP-017`).
- `se_harness/cli.py`: the `delegated-workflow` parser, its handlers and
  JSON helpers, seven imports and five exception-tuple entries removed.
- `se_harness/mutation_guard.py`: `change-bundle-apply`,
  `delegated-vrec-prepare`, `delegated-work-order-complete`,
  `delegated-work-order-start` removed from `PUBLIC_MUTATION_OPERATIONS`.
- `pyproject.toml`: the two catalogs out of package data; the three skills'
  and adapters' data-file entries removed.
- `templates/repository/standard/.agents/skills/{harness-draft-change,
  harness-execute-work-order,harness-prepare-assurance}` and their
  `.claude/skills` adapters deleted (15 files); `harness-orient` and
  `harness-operator-brief` stay.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `validate_agentic_delegations`, `E021`, the delegation constants and
  `_path_is_within` removed (147 lines in three blocks, declared against
  the 0.10.0 root in `tests/test_predecessor_bootstrap_retirement.py`);
  `WORK_ORDER.template.md` loses the table and its guidance (declared in
  `tests/test_artifact_catalog.py`).
- `se_harness/skill_contract.py` → `tests/skill_contract_support.py`
  (test-only): the contract and manifest validator the two retained skills'
  tests use.
- Tests: `test_change_bundle`, `test_delegated_authority`,
  `test_delegated_workflow`, `test_effect_broker`, `test_repository_state`,
  `test_agent_contract` removed (68 tests); `test_journaled_apply` added
  (13 tests); `test_agentic_execution`, `test_mutation_guard`,
  `test_release_build`, `test_artifact_authoring_policy`,
  `test_standard_repository_lifecycle`, `test_hash_bound_integrity`,
  `test_instruction_architecture`, `test_fixture_support`,
  `test_artifact_catalog`, `test_predecessor_bootstrap_retirement` updated.
- Amendment records (trailing sections, front matter untouched) on
  `ADR-AEX-006`, `ADR-AEX-007`, `ARCH-AEX-002`; a "Removed" paragraph in
  the `agentic-execution` README; the reference note loses the
  `delegated-workflow` row and block; the two skill notes carry a status
  line; `WO-ECP-008` hands its skill item over; the domain index follows.

## Tests

`tests/test_journaled_apply.py` (13):

- create/replace/delete commit as a whole; stale target aborts before the
  journal (`JNL007`);
- injected apply failure restores the prior state; every in-process fault
  stage (`before-journal`, `after-journal-prepared`, `after-parent`,
  `after-temp` ×2, `after-apply` ×3, `before-commit`) restores it;
- post-commit fault → recovery keeps the result; interruption
  (`SystemExit`) at each durable stage → recovery restores the prior;
  a separate process interrupted mid-apply → a new process recovers;
- a corrupt backup → `human-recovery-stop` (`WEX-ECP-041`), a later apply
  refused (`WEX-ECP-042`); interruption after commit → recovered result;
  a checksum-mismatched journal blocks recovery (`JNL005`);
- **Windows held-open destination** rolls back prior entries (run, not
  skipped, on this workstation); untrusted paths and case-collisions
  refused (`JNL001`).

`RetiredSkillCensusTests` (`ECP-SKL-003`): the template ships exactly
`harness-operator-brief` and `harness-orient`, no script contains
`"evaluator_invoked": False` or `client=lambda`, no contract names
`delegated-workflow`. `test_release_build`: the wheel carries none of the
ten removed names and carries `journaled_apply.py`.

## Suite readings

- Windows 11 workstation (CPython 3.14, CRLF checkout, `8bfd00c`): 1128
  tests, 26 skipped, 2 failing names, both present on `main` and outside
  this work order (`test_artifact_authoring...test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  `test_instruction_architecture...test_owner_region_stays_within_the_size_bound`);
  the Windows held-open fault case ran.
- Linux: the pull request's suite lane, in the hosted-lanes section.

## Demonstrations on this repository

- Candidate CLI: `harnessctl --help` lists 24 commands and no
  `delegated-workflow`; `harnessctl delegated-workflow catalog` is an
  argument error (exit 2).
- Wheel (VER-ECP-014 scenario 1): `se_harness-0.11.0-py3-none-any.whl` built
  outside the checkout, non-promotable; `RECORD` carries none of
  `agent_contract.py`, `change_bundle.py`, `delegated_authority.py`,
  `delegated_workflow.py`, `effect_broker.py`, `repository_state.py`,
  `runtime_state.py`, `skill_contract.py`, `agent_contract.json`,
  `effect_contract.json`, and carries `journaled_apply.py`; shipped skills
  `harness-operator-brief`, `harness-orient`; `.claude` adapter
  `harness-orient`. Installed into a disposable venv with `-I`: 25 public
  submodules import, no removed module importable, 29 `--help` pages walked
  (root, every command, every `qualify` operation) name no
  `delegated-workflow`, `envelope`, `nonce` or `change-bundle`.
- Vocabulary grep over `se_harness/`, the template scripts and skills:
  `nonce|MAX_ENVELOPE_LIFETIME|retry_ordinal|revoked=|agentic_delegation|delegated-workflow`
  is empty; `change-bundle` survives in two places, deviation 2.

## Readings under the 0.10.0 root

- `validate .`: 1141 artifacts, 0 errors, 479 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (7 records).
- Start preflight for `WO-ECP-006`: PASS over `62a8d42`.
- `git diff --stat main -- tests/fixtures/agentic_execution/canonical_vectors.json phase3 phase4 phase5`: empty.

## Deviations, recorded for the completion decision

1. **`resolve_delegation` is not retained as code.** `ECP-DLG-009` keeps it
   for the delegation class; this work order deletes `delegated_authority.py`
   whole, because the function's only callers were the removed broker path.
   It is in Git history at `main` `78306e0` and returns, or is replaced in
   one module, with `REQ-ECP-011`'s work order (`VER-ECP-006` allows "or its
   replacement in one module").
2. **`change-bundle-apply` survives as a transition-binding row** in
   `se_harness/workflow_contract.json` and `workflow_contract.py` (and the
   template `WORKFLOW.json`): contract files are out of this scope. The row
   binds an operation no command offers; it is inert and goes with the
   delegation-class work order, which touches the contract anyway.
3. **`ECP-SKL-002` names skills that do not exist** (`harness-prepare-
   verification`, `harness-guard`); the retired directories are
   `harness-prepare-assurance` and `harness-draft-change`. The rule's
   intent (retire the stubbed writing skills, keep `harness-orient`) is
   implemented; the name drift is recorded for an amendment record on
   `SPEC-ECP-007` under a later work order.
4. **Formal supersessions not applied.** The eight `AEX` artifacts with
   `ECP` successors keep their `approved` status; the amendment records
   state the supersession in prose. The transitions are the steward's and
   technical owner's acts (`WO-ECP-006`'s own text), taken by name when the
   successor rules are all implemented.

## Complete changed-path set

Every path this work order changed since `main` at `78306e0`, packet
included, as Git derived it (61 paths); the handoff check completed at
its fixed point with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE`
passing, run by the released 0.10.0 evaluator on this Windows checkout:

```
docs/engineering/agentic-execution/README.md
docs/engineering/agentic-execution/architecture/ARCH-AEX-002.md
docs/engineering/agentic-execution/architecture/adr/ADR-AEX-006.md
docs/engineering/agentic-execution/architecture/adr/ADR-AEX-007.md
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/evidence/WO-ECP-006/WO-ECP-006-handoff.md
docs/engineering/execution-control-plane/evidence/WO-ECP-006/handoff.json
docs/engineering/execution-control-plane/verification/VER-ECP-014.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-006.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-008.md
docs/notes/agentic-execution-host-adapters.md
docs/notes/agentic-execution-skills-mvp.md
docs/notes/harnessctl-reference.md
pyproject.toml
se_harness/agent_contract.json
se_harness/agent_contract.py
se_harness/change_bundle.py
se_harness/cli.py
se_harness/delegated_authority.py
se_harness/delegated_workflow.py
se_harness/effect_broker.py
se_harness/effect_contract.json
se_harness/journaled_apply.py
se_harness/mutation_guard.py
se_harness/repository_state.py
se_harness/runtime_state.py
templates/repository/standard/.agents/skills/harness-draft-change/SKILL.md
templates/repository/standard/.agents/skills/harness-draft-change/agents/openai.yaml
templates/repository/standard/.agents/skills/harness-draft-change/scripts/guard.py
templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json
templates/repository/standard/.agents/skills/harness-execute-work-order/SKILL.md
templates/repository/standard/.agents/skills/harness-execute-work-order/agents/openai.yaml
templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py
templates/repository/standard/.agents/skills/harness-execute-work-order/skill-contract.json
templates/repository/standard/.agents/skills/harness-prepare-assurance/SKILL.md
templates/repository/standard/.agents/skills/harness-prepare-assurance/agents/openai.yaml
templates/repository/standard/.agents/skills/harness-prepare-assurance/scripts/check_prepare.py
templates/repository/standard/.agents/skills/harness-prepare-assurance/skill-contract.json
templates/repository/standard/.claude/skills/harness-draft-change/SKILL.md
templates/repository/standard/.claude/skills/harness-execute-work-order/SKILL.md
templates/repository/standard/.claude/skills/harness-prepare-assurance/SKILL.md
templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md
templates/repository/standard/scripts/validate_engineering_artifacts.py
tests/skill_contract_support.py
tests/test_agent_contract.py
tests/test_agentic_execution.py
tests/test_artifact_authoring_policy.py
tests/test_artifact_catalog.py
tests/test_change_bundle.py
tests/test_delegated_authority.py
tests/test_delegated_workflow.py
tests/test_effect_broker.py
tests/test_fixture_support.py
tests/test_hash_bound_integrity.py
tests/test_instruction_architecture.py
tests/test_journaled_apply.py
tests/test_mutation_guard.py
tests/test_predecessor_bootstrap_retirement.py
tests/test_release_build.py
tests/test_repository_state.py
tests/test_standard_repository_lifecycle.py
```

## Hosted lanes

Read on the pull request at its heads; recorded in the pull-request body
and the verification record.
