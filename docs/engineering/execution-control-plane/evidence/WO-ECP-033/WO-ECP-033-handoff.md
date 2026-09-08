```toml
artifact = "WO-ECP-033"
checkpoint = "handoff"
formal_snapshot_sha256 = "d4991b4391f7bf148248c589365b5f4007d47e63e6a2d8671ce3702a287711a3"
rebound_at = "2026-09-08T13:34:09Z"
```

# WO-ECP-033 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Every diagnostic code the package raises is named once in
`se_harness/codes.py`; `CodedError` is the one base of a coded refusal, and
every refusal class that is not one exposes the same two attributes; no
package module spells a code, the standard-library-only loader excepted; the
CLI reads the two attributes and keeps one split for bare text; the index
reads the registry through the parser and the page is regenerated. The four
declarative contract sections drive the code at run time: `agentic_operations`
the delegation gate, the transition planner and the mutation guard;
`restitution_fields` the result validator; `aggregation` the predicate
aggregator; the declared hash mode the record writer and the lock writer. Each
section is validated at load and a missing or malformed one refuses with
`WEX-ECP-031`. The Python copies are gone; no recorded digest moved.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-033-codes-contract-tables`,
  stacked on the group B branch at `76dc6859`; the code commits are
  `bf3a7ed8` (the four tables), `faf7a3c2` (the registry, the index, the
  amendment record and the domain index) and `2cd0e671` (two test pins,
  disclosure 8); `DEC-ECP-002` raised at `856386a8` and disposed at `5512a698`
  with the scope amendment.
- Duplication scan: `pylint 4.0.8` in a scratch environment outside the
  checkout (`C:/Users/hok/se-harness-scan`), `--enable=duplicate-code
  --min-similarity-lines=8`, over `se_harness` and `repository_tools`.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-PRM-016` | `se_harness/codes.py`: 118 constants in 21 families, a name being its code with `-` written `_`, plus the two record-refusal tables the CLI composes from; 19 modules reference them at 270 former literal sites | `tests/test_codes_and_contract_tables.py` `RegistryTests`: `test_no_package_module_spells_a_diagnostic_code` (AST over every string constant outside docstrings), `test_every_name_is_its_code` |
| `ECP-PRM-017` | `codes.CodedError(HarnessError)` with `code`, `message`, `str` as `code: message`; `DelegationError`, `ProcedureError`, `ContractRefusal`, `RestitutionError`, `SelectionRefusal` and `MutationGuardError` derive from it; `PreconditionError` and `InterpreterSafetyRefusal` expose the two attributes and keep their wire forms | `CodedErrorTests`: eight classes, code, message and wire form each; `tests/test_cli_shape.py` (the CLI's exit-2 and result forms unchanged) |
| `ECP-PRM-018` | `repository_tools/diagnostic_code_index.py` `registry()` parses `codes.py` (`NAME = "CODE"` assignments), `_named_codes` attributes a raise site to the name it passes (`CodedError(WEX210, "…")`, `f"{WEX201}: …"`), the engine is still scanned as literals; the composed-code reader is gone with the cause table | `IndexTests`; `tests/test_diagnostic_code_index.py` 11 OK; `--check` matches; the page reading below |
| `ECP-PRM-019` | `workflow_contract.delegated_operations()` reads `agentic_operations` once; `gate_source.DELEGATED_RIGHTS` and `DELEGATED_TRANSITIONS` are derived from it, the overlay's argv from `result_status`; `mutation_guard.PUBLIC_MUTATION_OPERATIONS` joins the three `mutation_operation` values to the seven human ones; `provenance` takes the prepare operation from the rights; `workflow_contract.DELEGATED_OPERATIONS` is gone | `ContractTableTests.test_the_delegated_operations_are_the_contract_section`; `tests/test_delegation_class.py`, `tests/test_mutation_guard.py` |
| `ECP-PRM-020` | `workflow_result._validate_restitution` compares to `restitution_fields()`; the literal set in `workflow_result` and in `validate_contracts` is gone; `STATUSES` is the contract module's `RESULT_STATUSES` | `test_the_result_validator_reads_the_contract_field_set`; `tests/test_workflow_restitution.py` |
| `ECP-PRM-021` | `workflow_compliance._aggregate` takes the first present status of `aggregation_order()`; the `fail`, `not_assessable`, `pass` chain is gone | `test_the_restitution_fields_and_the_aggregation_are_the_contract_sections` (a reordered contract reorders the verdict) |
| `ECP-PRM-022` | `provenance._evidence_digest(relative, bytes)` hashes the evidence under its declared class for both record builders; `installer` hashes the prior lock through `declared_digest(LOCK_NAME, …)`; both were `raw_sha256` decided locally | `test_the_two_writers_hash_through_the_declared_digest`; `tests/test_revision_provenance.py` (the recorded evidence digest equal), `tests/test_hash_bound_integrity.py` |
| `ECP-PRM-023` | `delegated_operations_of`, `restitution_fields_of`, `aggregation_of` validate shape, grammar, uniqueness and, in `validate_contracts`, the lifecycle edges; each refusal is `ContractRefusal(WEX_ECP_031, …)` | `test_a_missing_or_malformed_section_refuses_with_one_code`: five throwaway contracts and the combined validation, one code |
| `ECP-PRM-024`, `-025`, `-028` | `CONTRACT_SHA256` equal (`a443e93d…`); no contract JSON, template, recipe or lock byte changed; the evidence digest under the declared `raw` mode equals the recorded raw digest; the lock digest under `utf8-text-lf-v1` equals the raw one for the LF lock the installer writes | `tests/test_revision_provenance.py` `RELEASED_EVALUATOR_EVIDENCE_SHA256`; `tests/test_hash_bound_integrity.py` `ProducerNewlineTests`; `git diff --name-only` names no contract, template, recipe or lock |
| `ECP-PRM-026` | `SPEC-ECP-006` carries a dated amendment record naming `SPEC-ECP-023`: the three rights are read from `agentic_operations`, and its Compatibility sentence that the block is dropped is superseded | `validate --advisories` 0 errors; disclosure 2 on the specifications that needed none |
| `ECP-PRM-027` | not met as written: three of the seven blocks remain and every one has a side inside `se_harness/engine/`; `DEC-ECP-002` (deviation) accepted by the technical owner on 2026-09-08, revisit at the merge of wave 3 (#378) | disclosure 1; `DEC-ECP-002` |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| code literals in the package outside docstrings (the index tool's grammar, registered prefixes) | AST, base `76dc6859` vs branch | 270 to 0 outside `codes.py` and `interpreter_safety.py` (11 `EPS` literals stay behind the barrier) |
| distinct codes | registry | 118 named; 99 spelled by the package before, 11 by the loader, 8 composed by the CLI (`WEX301` to `WEX304`, `WEX401` to `WEX404`) |
| carriage idioms | reading of the raise sites | one class and its constructor; the guard's wire form and the precondition's bare message kept as subclass renderings |
| splitting idioms | grep | `partition(": ")` in `workflow.plan_transition` gone (the refusing predicate is carried as a pair); `cli._split_code` is the one split, reached only for text that carries no attributes |
| `python -m repository_tools.diagnostic_code_index --check` | candidate | matches; 196 codes across 30 prefixes, 195 before: `WEX-ECP-031` is the one new code; 97 rows re-attributed from bare literals to `code: message` text |
| `python -m repository_tools.diagnostic_code_index --write` | candidate | the committed page equals the regeneration (`tests/test_diagnostic_code_index.py`) |
| throwaway refusals | candidate | a missing `agentic_operations`, an entry without `gate_ids`, a repeated decision right, `restitution_fields` without `outcome`, an `aggregation` of two statuses, and an edge the `work_order` lifecycle lacks: each `WEX-ECP-031` |
| `validate --advisories` | exact 0.16.0 | 1,399 artifacts (with `DEC-ECP-002`), 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-033 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git 76dc6859` | exact 0.16.0 | Completed; all nine `QGP-G4I-*` predicates pass, every changed path inside the amended scope; `complete: true`; the schema-2 result is retained beside this packet as `handoff.json`. The dry run before the packet read `QGP-G4I-EVIDENCE: not_assessable` and eight passes |
| `CONTRACT_SHA256` | candidate, `main` vs branch | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` both |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment | 4 blocks at the base, 3 on this branch: the restitution-fields block (`workflow_contract` and `workflow_result`) is gone; the three left pair an engine copy with a package copy (disclosure 1) |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,324 tests, 1 error, 26 skipped: the workstation baseline (`errors=1, skipped=26`), at `2cd0e671` in a detached worktree; 1,309 before this group, 15 tests added |

### The Windows suite

The one error is the standing Windows baseline,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
whose teardown removes a read-only `.git` tree; it fails the same way on
`main` and on the group A and B branches. The 26 skips are the platform set.
The run at `faf7a3c2` read `failures=3`: the two `PV` reservation cases and
the preflight pin of disclosure 8, and nothing else.

## Behaviour changes, each where a copy was wrong or a form was inconsistent

- A `ProcedureError` that escapes a handler prints its code on the exit-2
  line (`harnessctl: WEX220: …`); every `ProcedureError` the package raises
  already carried its code in its text, so only a test that built one without
  a code saw the change.
- `harnessctl` labels a refusal from its `code` and `message` attributes
  before splitting text; for the package's refusals the two agree by
  construction, so no result or exit-2 line changed.
- A contract whose `restitution_fields` carries an extra field is a policy,
  not a malformation: the loader accepts it where the copy refused it; a
  field set without `outcome`, `done` or `current_lifecycle_state`, a repeated
  field or a non-name refuses. The pinned card test of
  `tests/test_workflow_execution.py` moved with the rule.
- An `agentic_operations` entry naming a status outside the `work_order`
  lifecycle or an edge it lacks refuses at load; the copy compared field by
  field against itself.
- The installer refuses with a `HarnessError` when the prior lock cannot be
  hashed under its declared mode (invalid UTF-8); it hashed any bytes raw.

## Disclosures

1. `ECP-PRM-027` reads three blocks after this group, not none: `artifact_layout`
   with `engine/artifact_layout_registry` (the layout registry), `provenance`
   with `engine/validate_engineering_artifacts` (the standing deviations),
   and two engine modules with each other (the body parser). Every one pairs
   a copy inside `se_harness/engine/` with another; the specification's Scope
   and this work order's Out of scope leave the engine to wave 3 (#378), so
   the rule cannot be met by this wave as written. `DEC-ECP-002` records the
   deviation for the technical owner's disposition.
2. `ECP-PRM-026` produced one amendment record, on `SPEC-ECP-006`. `SPEC-ECP-018`
   `ECP-GAT-004` and `SPEC-WEX-002` state the rights and the aggregation order
   in prose without naming a Python table, and `SPEC-HBI-001` rule 5 already
   requires every caller to take the mode from the class; none names a copy as
   operative, so none is amended. `SPEC-ECP-006`'s Compatibility note that
   the contract drops `agentic_operations` was wrong since `WO-ECP-006`; the
   record supersedes it.
3. `se_harness/interpreter_safety.py` keeps its eleven `EPS` literals and
   spells no import of the registry: `SPEC-REB-015` rule 2 binds it to the
   standard library. The registry names the eleven for the index and the
   refusal class exposes `code` and `message` without importing anything.
4. The `agentic_operations` section carries no family; the derived
   transitions bind `work_order`, the family `SPEC-ECP-006` `ECP-DLG-001`
   fixes for the delegation class, named once as
   `workflow_contract.DELEGATED_FAMILY`.
5. The lock writer's per-file entries hash managed files at arbitrary paths
   under the lock's own `hash_mode`; no hash-bound class covers them, so
   `declared_digest` has nothing to declare there and they are unchanged. The
   lock's own digest (the `prior_lock_sha256` binding) is the site the rule
   names and it now goes through the declaration.
6. The index page changes on 97 rows: the message column now shows the
   `code: message` text of each raise site where it showed the bare literal;
   one code is added (`WEX-ECP-031`); no code is removed. The two `_composed_codes`
   readers of `provenance.CAUSE_SUFFIX` and `cli._record_code` are retired
   with the table they read, the eight composed codes being registry entries.
7. `tests/test_cli_shape.py` built two refusals with a bare message; they now
   pass a code, as every package site does.
8. `tests/test_predecessor_bootstrap_retirement.py` held the retired `PV`
   codes to one file and `tests/test_hash_bound_integrity.py` pinned a preflight
   literal; both pins moved with the registry (`2cd0e671`), after the first full
   run at `faf7a3c2` read them as the only failures beyond the baseline.
9. `DEC-ECP-002` was raised in `decisions/`, which the scope did not name; the
   accountable engineering owner widened the scope on 2026-09-08 under
   DR-REMEDIATION-SCOPE by the same decision that accepted the deviation, and
   the work order carries the dated amendment. Nothing else was widened.
