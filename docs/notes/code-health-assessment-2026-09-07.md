# Code health assessment, 2026-09-07

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Read-only assessment of the `se_harness` code base at `main` `5e02039` (root
> evaluator 0.16.0, candidate 0.17.0), requested by the repository owner on
> 2026-09-07. It creates no formal artifact and authorizes no work; every
> remediation below is a proposal for a work order. Findings are labelled
> **Fact** (verified against source, a tool run, or a command run) or
> **Inference** (a judgment drawn from facts).

## Summary

The core of the product is sound: one lifecycle engine, one contract file,
commit-bound records, deterministic outputs. The maintenance cost sits at the
edges, and it has three shapes.

1. **Duplicated primitives.** The same small things are written many times
   with small differences: 13 Git launchers with five timeout policies, 8
   TOML front-matter parsers with three line-ending rules, 16 SHA-256 helpers,
   9 duplicate-key JSON hooks, 6 atomic-write routines, 20 inlined CRLF
   normalizations of two different semantics, a 32-line layout table copied
   verbatim between the package and the engine. None of this is wrong today;
   each copy is a place the next fix can miss.
2. **Dead and dormant surface that still ships.** About 300 lines of
   unreferenced code in the core, a 462-line module nothing imports, a
   1,316-line command and a 304-line command never used operationally, 7 of
   13 keys in the operator's policy file that nothing reads, two contract
   entries no checkpoint can reach, 8 orphan test fixtures, a 21 % test
   re-run rate from `TestCase` inheritance.
3. **Conventions stated but not enforced.** The exit-code rule, the
   one-code-per-line rule, and the `--json` envelope are each broken in a
   handful of places the tests do not cover, most visibly a live doubled code
   in `check --checkpoint` and a `transition` refusal that exits 1 where every
   sibling exits 2.

Measured size: 13,777 lines in `se_harness/`, 7,010 in `se_harness/engine/`,
1,797 in `scripts/`, 2,204 in `repository_tools/`, 28,236 in `tests/`;
1,607 commits since 2026-08-11. Maintainability index below 20 (rank C) for
14 of 42 production modules; 30 functions with cyclomatic complexity of 30 or
more; 17 functions over 80 lines in the core alone.

**Inference.** A senior engineer would judge the architecture defensible and
the hygiene behind it. Roughly a fifth of the production code is removable or
foldable without behaviour change, and a third of the suite's run time is
accidental. The remediation is mechanical, low-risk, and splits into five
waves below; none requires a design decision except the four owner calls
listed at the end.

## Method

- Static tools in a scratch environment outside the checkout: `pyflakes`,
  `vulture` (confidence 60, with and without `tests/` as usage), `radon cc`
  and `radon mi`, `pylint --enable=duplicate-code` (8-line minimum).
- Six independent reviews, each reading its scope fully and grepping call
  sites across `se_harness/`, `scripts/`, `repository_tools/`, `.github/`,
  `templates/`, and separately `tests/`: core package, release and tooling
  modules, the engine, configuration and contracts, the test suite, and CLI
  conventions.
- Spot checks by running the candidate CLI read-only on this repository, and
  by counting defined versus discovered tests with `unittest`'s loader.

Counts of the form `1/0` mean "one product reference, which is the definition
itself, and no test reference".

## 1. Dead code

### 1.1 Unreferenced (definition only, no product or test caller)

**Fact.** Verified by word-boundary grep and by `vulture`.

- `se_harness/cli.py:1175` `arguments` local assigned, never read.
- `se_harness/workflow.py:100` `_finding_key`; `:635` `_status`; `:396`
  `closing_ending` local.
- `se_harness/workflow_compliance.py:1263` `focus_schema2`, docstring "kept
  for its Phase 4 caller" (Phase 4 removed under WO-ECP-006); `:1304`
  `_DEFINITION_TYPES` (third copy); `:54` `CheckpointContext.report` written
  at `:789`, never read.
- `se_harness/workflow_procedures.py:223` `ensure_validated`.
- `se_harness/workflow_contract.py:639` `OPERATING_CARD_PATH`; `:112-117`
  `LifecycleState.transitionable`, `.must_remain_visible`,
  `.predecessor_adapter` validated and stored, never read afterwards.
- `se_harness/decisions.py:20-26` `DECISION_KINDS`, `DEVIATION_OPTIONS`,
  `BLOCKABLE_TYPES`, `OPTION_ID`, `DISPOSITION_FIELDS`; the engine validator
  defines its own at `engine/validate_engineering_artifacts.py:267-268`.
- `se_harness/runtime_identity.py:377` `assert_runtime_identity`; `:64-66`
  three dataclass fields never populated.
- `se_harness/interpreter_safety.py:66` `InterpreterSafetyError` never raised;
  its only `except` at `runtime_identity.py:178` is unreachable. `:32`
  `OUTCOMES`, `:51-63` `EVALUATION_ORDER` unused. Residue of the JSON
  declaration loader WO-REB-030 removed.
- `se_harness/release_unit.py:101-117` `_catalog_lookup` and the
  `lookup is None` branch at `:137`: both product callers pass `lookup=`.
- `se_harness/artifact_layout.py:445-446` unreachable `raise` (set equality
  of `_REF_PREFIX` and `ARTIFACT_DIRECTORIES` verified); `:424` unused
  parameter `artifact_type`.
- `se_harness/integrity.py:139` `compare_lock_entry(lock, …)`: `lock` unused
  at all five call sites; `:91` `if schema == LOCK_SCHEMA` always true after
  `:85` raised, so `:92-117` sit under a dead conditional.
- `se_harness/candidate_acceptance.py:437-449` `write_acceptance_manifest`
  never called, so the `se-harness-functional-acceptance-v1` manifest is
  never emitted anywhere; the "second acceptance framework" exists only as a
  digest input.
- `se_harness/engine/generate_harness_dashboard.py:915-962` `compute_impact`
  never called (no `direct_inbound`/`transitive_outbound` in the template).
- `se_harness/engine/validate_engineering_artifacts.py:187-191`
  `ALLOWED_STATUSES` never read; `:45` `"risk_acceptance": "RISK-"` a type
  that exists nowhere else; `:3271` and `dashboard:2663` `--artifact-root`
  flag never passed by any caller.
- `se_harness/engine/inspect_engineering_artifacts.py:366-379` the
  `validation_report is None` fallback is unreachable from `main` and would
  raise on a real snapshot (the dashboard never emits `plane`).
- `repository_tools/release_distribution.py:24` `DISTRIBUTION_SCHEMA`;
  `repository_tools/json_bytes.py:31,37,41,85` four helpers no sibling
  imports (see 2.1).
- `pyflakes`: 8 unused imports and 3 unused locals in production code, 20 in
  tests, one invalid escape sequence at `tests/test_artifact_authoring.py:365`
  that Python already warns about.

### 1.2 Used only by tests

**Fact.**

- `se_harness/hash_bound.py:26-28, 210-289` the declared-digest chain
  (`MATCH_*`, `pattern_specificity`, `resolve_class`, `resolve_mode`,
  `_digest`, `declared_digest`, `compare_declared_digest`): no product path
  hashes through the declared mode; producers hard-code `hashlib.sha256`
  (`provenance.py:406`, `installer.py:550`). About 70 lines.
- `se_harness/workflow_contract.py:638-687` `render_operating_card` and its
  constants: the managed card ships as a template file, never generated.
- `se_harness/interpreter_safety.py:356-381` `refusal_case`,
  `normalized_origin`; `se_harness/workflow.py:49-57` `TRANSITIONS`;
  `se_harness/preflight.py:62-74` `POLICY_PATHS`;
  `se_harness/release_qualification.py:55` `RETIRED_CHECK_CODES`;
  `repository_tools/evaluator_facts.py:40,128` two retained aliases.

### 1.3 Shipped but never imported

**Fact.** `se_harness/journaled_apply.py` (462 lines) has zero importers in
`se_harness/`, `repository_tools/`, `scripts/`, `.github/`, `templates/`. It
is in the wheel (`tests/test_release_build.py:313` asserts it) and has 13
tests. Its docstring says wiring it in is REQ-ECP-017's work; that
requirement is `approved` and WO-ECP-018 lists the shared journaled write
path as deferred. **Inference.** Either wire it into the installer, renumber
and provenance writers, or retire it with an amendment; shipping it unused
makes REQ-ECP-017 read as satisfied when it is not.

### 1.4 Dormant commands

**Fact.**

- `harnessctl rehearse-recovery` (`se_harness/recovery_rehearsal.py`, 304
  lines): no workflow invokes it, no rehearsal report is retained under
  `docs/`, and its `STANDARD_WORKFLOWS` (`:29-33`) names repository-owned
  workflows as if they were standard; `:251` asserts the absence of a file
  that has never existed. Two earlier assessments recommended removal.
- `harnessctl renumber-artifacts` (`se_harness/renumber.py`, 1,316 lines,
  81 `REN` codes, complexity 73 in `build_renumber_plan`): never applied in
  this repository, no retained output. Second-largest module in the package.
- `scripts/migrate_verification_methods.py`: a one-shot migration left
  half-applied. 271 of 347 requirements still carry a string
  `verification_method`, 76 an array. It exits 0 with unmatched values, so it
  cannot gate.
- Schema-1 bundle creation: `scripts/create_release_bundle_manifest.py:28-32`
  can still emit a schema-1 manifest that `bind_distribution:521` and
  `replay_release_build.py:66` both refuse. Reading schema 1 must stay for
  history; creating it is dead.

### 1.5 Compatibility windows with no end condition

**Fact.** Each is live code that protects only this repository's past.

- `engine/validate_engineering_artifacts.py:254,2369-2497` legacy
  `constrains` relation (W015): 15 architecture files still use it, all
  `implemented`; the template offers only `addresses`/`conforms_to`.
- `:2515-2523,2845-2863` `legacy_missing` decision assessment (W014): 14 of
  82 architectures in the window. No end date anywhere.
- `:1538-1554` records without `prepared_at`: 85 of 213.
- `:2751-2756` work orders without `execution_scope`: 111 of 240.
- `se_harness/workflow_compliance.py:597,617-633` the header-less evidence
  packet grace (`W-ECP-002`, "compatibility for one release").
- `se_harness/workflow_contract.py:15,218-232` the retired
  `QUALITY_GATES.json` v1 hint (`WEX-ECP-030`).
- `se_harness/integrity.py:79-84` the friendlier message for lock schema 1/2.
- `se_harness/cli.py:855-864` the `adopt` alias, documented "for the 0.16.0
  release only"; the package is 0.17.0 and the 0.16.0 verifier no longer
  calls it.

## 2. Duplicate execution paths

### 2.1 Primitives

**Fact.** Locations verified; behaviour differences noted.

| Primitive | Copies | Where | Divergence |
| --- | --- | --- | --- |
| Git launcher | 13 | `artifact_layout.py:379`, `gate_source.py:116`, `hash_bound.py:292`, `provenance.py:75,89`, `release_qualification.py:260,294`, `release_unit.py:70`, `renumber.py:241,268`, `workflow_compliance.py:161,417`, `preflight.py:271`, `candidate_acceptance.py:193`, `cli.py:247-343`, `engine/generate_harness_dashboard.py:201-299`, `repository_tools/release_build.py:266`, `release_distribution.py:333`, `repository_tools/upgrade_rehearsal.py:80`, `scripts/validate_governor_transition.py:74,100` | timeouts {none, 30, 60, 120, 180}; three with none (`gate_source`, the four engine launches in `cli.py`, `upgrade_rehearsal`); three decode with the locale encoding; `gate_source._git` catches no start failure, so a missing `git` is a traceback through the delegated transition path |
| TOML front matter | 8 | `engine/validate…:883`, `provenance.py:119,195`, `release_qualification.py:584`, `workflow.py:381`, `gate_source.py:149`, `hash_bound.py:381`, `renumber.py:552`, `repository_tools/evaluator_facts.py:43` | BOM: some `utf-8-sig`, some not; delimiter: `gate_source.py:149` `split("+++", 2)` is not line-anchored; `artifact_layout.py:370` and `workflow_compliance.py:1322` match only `+++\n`, so a CRLF checkout reports "no existing artifact"; `evaluator_facts.py:43` fails outright on CRLF (executed: `TOMLDecodeError`) |
| SHA-256 helper | 16 | `integrity.raw_sha256` plus 15 private copies | none, pure duplication |
| Canonical JSON bytes | 7 compact + 6 indent-2 | `evaluator_evidence.py:60`, `evaluator_identity.py:133`, `installer.py:516`, `journaled_apply.py:134`, `recovery_rehearsal.py:41`, `release_qualification.py:104`, `engine/validate…:1213`, `repository_tools/json_bytes.py:21`, `release_build.py:70` | `ensure_ascii` True in the package, False in `repository_tools`; `release_build.canonical_json_bytes` and `json_bytes.canonical_json_bytes` share a name and produce different bytes, and recipe digests depend on the former |
| Duplicate-key JSON hook | 9 definitions, 16 call sites | `integrity.py:58`, `hash_bound.py:81`, `workflow_compliance.py:67`, `workflow_contract.py:190`, `github_ci.py:31`, `evaluator_identity.py:32`, `evaluator_evidence.py:51`, `json_bytes.py:66`, `release_build.py` | exception class only |
| Atomic write | 6 | `installer.py:412`, `provenance.py:315,334`, `artifact_layout.py:214`, `workflow.py:929`, `workflow_compliance.py:498,556,572` | the three inline copies in `workflow_compliance` use a fixed `.tmp` name and no fsync, and they write governance evidence |
| CRLF canonicalization | 20 inlined | 10 full CR+CRLF (`integrity.canonical_text_bytes` form), 10 CRLF-only (lone CR survives) | two notions of "a line" where bytes are compared |
| `.engineering-harness.toml` reader | 4 | `installer.py:264`, `mutation_guard.py:78`, `workflow.py:525`, validator `load_revision_policy` | `utf-8` vs `utf-8-sig`; `plan_transition` reads the revision policy twice by two implementations |
| Layout registry | 2 | `artifact_layout.py:18-176` vs `engine/artifact_layout_registry.py:9-82` | tables identical (pinned by a test); functions diverge: only the package copy carries the PurePath-to-POSIX fix and validates domain/type/id |
| Lifecycle contract loader | 2 | `workflow_contract.py:112-184` vs `engine/validate…:74-177` | same nine checks, different exception type; a third hand-written copy in `tests/test_lifecycle_state_contract.py:25-62` |
| Evaluator-evidence validator | 2 | `evaluator_evidence.py` vs `engine/validate…:1121-1314` | one raises, one emits E012 |
| Definition-type set | 4 | `workflow.py:35`, `workflow_contract.py:58`, `workflow_compliance.py:1304`, contract selectors | no sync test |
| Checkpoint-name set | 5 | `workflow_contract.CHECKPOINTS`, `workflow_compliance.py:446,875`, `cli.py:918,959` | no sync test |
| Status literal `{implemented, verified, released}` | 4 names | validator `:67,238`, dashboard `:63`, `provenance.py:33` | only one is derived from the contract |
| Artifact-ID regex | 4 | `provenance.py:26`, `artifact_layout.py:68`, `workflow_procedures.py:12`, validator `:47` | `artifact_layout.py:375` `REF_ARTIFACT_PATTERN` omits `OPS` and `DEC` although `_REF_PREFIX` declares both, so id allocation cannot see operating-contract or decision ids on other refs (verified) |
| Markdown body parsers | 2 | validator `:334-392` vs dashboard `:613-668` | near byte-identical; dashboard hard-codes section names the validator takes from a constant |
| Release-unit `lookup` closure | 3 | `cli.py:728`, `workflow_compliance.py:1418`, `release_unit.py:107` | third unreachable |
| Standing deviations | 2 | validator `:2899-2946` vs `provenance.py:139-163` | provenance re-reads every decision's TOML because the validator's JSON exposes only four fields per artifact |
| "Find the released record" | 5 | `release_qualification.py:600`, `evaluator_facts.py:59`, `validate_governor_transition.py:283`, `release_distribution.py:589`, `publish_release.py:364` | different directory and filename assumptions |
| Wheel metadata parse | 2 | `candidate_acceptance.py:101` vs `release_qualification.py:612` | strict `X.Y.Z` vs suffix allowed: a pre-release wheel passes `public-install` and fails `candidate-package` |
| `VERSION_PATTERN` | 9 | four grammars | see above |
| Subprocess environment builder | 4 | `candidate_acceptance.py:122`, `release_qualification.py:237`, `upgrade_rehearsal.py:68`, `validate_governor_transition.py:528` | allow-list vs deny-list; one sets `PYTHONPATH=""`, one pops it |

### 2.2 Repeated work per command

**Fact.**

- The validator is loaded two ways, contradicting `engine/__init__.py:5-8`
  ("not an import surface"): in-process by path
  (`preflight.py:238-257`, used by `workflow.py:125`) and as a subprocess
  (`cli.py:240-354`, `provenance.py:166,394`, `release_qualification.py:325`,
  `renumber.py:384`). The subprocess path yields dicts, so `provenance`
  re-parses every artifact's TOML the validator already parsed.
- `check --checkpoint start` validates the repository two or three times
  (`workflow_compliance.py:885`, then `run_preflight` at `preflight.py:332`,
  which also re-renders every template through `plan_install`); `check
  --checkpoint handoff --from-git` a third time at `cli.py:443`.
- `capture-verification` and `prepare-release` run the validator subprocess,
  then the dashboard subprocess, which runs the validator again
  (`provenance.py:170,398`; `dashboard:2691`).
- `doctor` runs the whole graph validation to keep one code (`cli.py:301-314`).
- `inspect` builds the full Explorer snapshot, three Git subprocesses
  included, to derive four queues (`inspect:833`).
- `preflight` and `check --checkpoint start` filter diagnostics differently
  (`cli.py:357-364` prints all and exits 1 on any; `workflow_compliance.py:
  308-343` drops candidate-versus-released skew), and `AGENTS.md` asks for
  both.
- Per pull request, CI runs `qualify complete-candidate` plus the full test
  suite twice on the same commit: `candidate-evidence.yml:63-74` and
  `release-qualification.yml:125-137` via `publication-rehearsal.yml:82-89`.
  The longest step in the pipeline runs twice.
- `candidate-evidence.yml:151-162` re-implements inline the forbidden-member
  list of `scripts/check_portable_release_surface.py` right after running
  that script; `:249-252` repeats a `--help` grep the script already does.
- Scope classification is written twice with a behavioural difference:
  `workflow.project_selected:271-303` lets an escaping path raise where
  `workflow_compliance._classify:268-305` relabels it `WEX200`.

## 3. Inconsistencies

### 3.1 Exit codes against the stated 0/1/2 rule

**Fact.** Rule at `docs/notes/harnessctl-reference.md:40-47`.

- `transition` treats a mutation-guard refusal and a `--set` syntax error as
  a failed result, exit 1 (`cli.py:597-604`); `decide`, `capture-verification`
  and `prepare-release` re-raise the same refusal to exit 2 by
  `str(exc).startswith("mutation guard ")` (`:522,549,627`); `upgrade`,
  `renumber-artifacts`, `scaffold-domain`, `create-artifact` let it propagate
  to 2. No test pins the `transition` case. (Reported by code reading; the
  spot check reached an illegal-edge result rather than the guard.)
- `renumber-artifacts` prints its human failed result to stderr (`cli.py:
  710`); the rule says stdout in both renderings.
- `dashboard --json` collapses the engine's 2 into 1 and discards the
  engine's stderr (`cli.py:350-354`).
- An unknown artifact id exits 2 from `pr-body` (`cli.py:481`) and 1 from
  `check --checkpoint` and `evidence` (`:427,463`). Confirmed by running all
  three.
- `qualify` never exits 2: every `HarnessError`, `OSError`, `ValueError`
  becomes an `RQ001`/`RQ002` failed result (`cli.py:814-835`).
- `main()` catches only `ContractError` and `HarnessError` (`cli.py:1179`).
  `ProcedureError` and the `WEX230` `ValueError` from `build_result` are
  caught only in `_check`; from `transition`, `decide`, `evidence`,
  `capture-verification`, `prepare-release` they are tracebacks. A missing
  `git` binary inside `gate_source._git` is a traceback too.
- Scripts: "cannot run" is exit 1 in half of `scripts/` and
  `repository_tools/` and exit 2 in the other half (listed in the tooling
  review).

### 3.2 Diagnostic codes

**Fact.**

- A doubled code is live and violates "a code appears once per line":
  `harnessctl check . --artifact WO-ZZZ-999 --checkpoint scope --json`
  renders `WEX210: WEX210: unknown artifact ID` (run on this repository).
  `_check` splits only `WEX-ECP-0*` prefixes (`cli.py:430-431`); the
  ECP-CLI-006 test covers the projection path only. Same latent path in
  `_transition` (`WEX201: WEX210: …`).
- Five idioms carry a code on an exception (message prefix, `.code`,
  `.predicate_id`, class-level `.cause` mapped by `cli._record_code`, the
  `"mutation guard MG00x"` text pattern) and five idioms split it back
  (`_split_code`, two `startswith` variants, an attribute lookup, none).
- No runtime registry: 55 distinct literals in the validator, more in the
  dashboard, preflight, workflow modules; codes shared by two or three modules
  as literals (`WEX210`, `WEX200`, `WEX220`, `WEX-ECP-002/-010/-014`);
  `WEX301-304`/`WEX401-404` composed at run time, which forced a bespoke AST
  parser in `repository_tools/diagnostic_code_index.py:128-160`. The index
  attributes `W001-W005`, `E-CIP`, `W-ADS` to the validator; they live in
  `preflight.py`.
- Two naming schemes coexist in one file (`E0xx` and `X-FAM-nnn`); `E013`
  is absent.

### 3.3 Result envelopes

**Fact.** A `--json` caller can receive 11 top-level shapes for 23 commands,
with 12 spellings of pass/fail (`outcome`, `operation.outcome`,
`compliance.status`, `passed`, `ready`, `valid`, `complete`, `result`,
`mode`, `applied`, `written`, `dry_run`). `validate --json` is the only
output without a `schema` member. Two commands mutate a child's JSON after
the fact (`inspect` injects `mode`/`selection` and re-serializes with
`ensure_ascii=False`, `cli.py:281-283`; `release-unit` injects `contract`,
`:750`). Diagnostics come in five record shapes. Serializer flags differ per
site; `workflow_result.render_json` is the one pretty serializer without
`sort_keys`.

### 3.4 Naming

**Fact.**

- `--output` means four things (a directory, a repository-relative record
  path, an external file, a positional directory); `--target` on `check` is
  a lifecycle state in the parser whose positional `target` is the
  repository; `--decision` takes `ID=ACTOR` repeatable on `transition` and a
  bare `ROLE` on `decide`; `--contract` on `release-unit` names the relation
  `prepare-release` calls `--release-contract`; `prepare-release --version`
  shadows the top-level `--version` in meaning.
- Across `scripts/` and `repository_tools/`: the repository is `target`,
  `--repository`, `--root` or `--root-dir`; the wheel is `--wheel`,
  `--candidate-wheel`, `--public-wheel` or `--evaluator-wheel`; the commit is
  `--commit`, `--candidate-commit` or `--base-revision`.
- Untyped string enums: `plan_install(mode=)`, `TemplateFile.mode`,
  `Change.mode`, `Change.action` (8 literal values, compared by string in
  `cli.py:141,174`); `integrity.py:15-16` already defines `MANAGED_MODES`
  that the installer never imports.
- Nine cross-module imports of underscore-private names (`_catalog`,
  `_validation`, `_family`, `_load_validator_module`).
- Schema versioning uses three grammars (`-v1`, `/v1`, bare integers) and one
  unprefixed name (`harness-dashboard-bundle-v2`).

### 3.5 I/O

**Fact.** Two decoders for the same artifact classes (`utf-8` at 20 sites,
`utf-8-sig` at 8); two `write_text` calls in the package disagree on
`newline=` (`candidate_acceptance.py:350` vs `:390`); 48 `print` calls in
`cli.py` go through the text layer, so every `--json` output is CRLF on
Windows except `pr-body`, which writes bytes; a library module prints a
warning from inside a config loader (`gate_source.py:101-106`).

### 3.6 Structure

**Fact.**

- Complexity over 60: `dashboard.build_findings` 105, `dashboard.
  normalize_artifacts` 97, `validator.validate_revision_consistency` 80,
  `dashboard.build_dashboard_bundle` 74, `renumber.build_renumber_plan` 73,
  `preflight.run_preflight` 69, `workflow_compliance.check_workflow` 68,
  `validator.validate_decisions` 66, `validator._validate_evaluator_evidence_
  binding` 66, `dashboard.build_readiness` 65, `dashboard.build_explorer_
  metrics` 62.
- `cli.py:build_parser` is 329 lines; `cli.py` also holds a Markdown report
  generator (`_scan_repository:92-129`) that belongs with the installer.
- `workflow_compliance.py` (1,466 lines) holds seven separable concerns:
  change-set normalization and Git derivation, snapshot digest, diagnostic
  classification, evidence-packet I/O, predicate evaluators, gate
  evaluation, result builders. `workflow.py` and `workflow_compliance.py`
  are one module split in two, held together by about 30 lazy imports.
- The validator (3,301 lines) is a sequence of pure passes coupled only by
  the orchestrator at `:3181-3216`; eight clean seams are listed in the
  engine review (lifecycle, authoring, evidence, revision, architecture,
  decisions, layout, report).
- `workflow.py:47` and `provenance.py:34` each parse and validate the
  contract JSON at import (`import se_harness.cli` measured at 0.165 s).

## 4. Unused configuration

**Fact.** Every key checked against every reader.

- `.engineering-harness.toml` and its template: 7 of 13 keys are inert.
  `schema_version` (no reader), `artifact_root` (path hard-coded in four
  modules), `dashboard_output` (hard-coded in three), `require_full_commit`
  (the rule is unconditional at `provenance.py:101`), `require_clean_worktree`
  (unconditional at `provenance.py:113`; `REQ-SHB-009.md:60` describes a
  policy value that has no effect), `verification_record_status`,
  `release_record_status` (`ready` hard-coded in the validator). The file is
  managed and hash-locked, so the fix is a template edit shipped by release.
- `quality_gates_contract.json`: gate `QG-G0-INTENT` with `QGP-G0-GRAPH` and
  `QGP-G0-INTEGRITY` is reachable from no rule, step, or binding, and
  `check_workflow` refuses the artifact types that could select it. The
  `aggregation` section is asserted equal to a literal and never drives
  behaviour (order hard-coded at `workflow_compliance.py:684-691`).
- `workflow_contract.json`: `PROC-CANDIDATE-COMMIT` and its step are
  unreachable; `agentic_operations` is compared once to `DELEGATED_OPERATIONS`
  and never read again while five Python copies of the table exist;
  `restitution_fields` duplicates `workflow_result.py:33-43` with no
  cross-check; `must_remain_visible`, `transitionable`, `predecessor_adapter`
  are fully derivable; seven lifecycle states have no inbound edge and zero
  artifacts.
- `hash_bound_classes.json` `classes[].mode` is consistency-checked but no
  producer hashes through `declared_digest` (see 1.2).
- Template copies `QUALITY_GATES.json` and `WORKFLOW.json` are byte-equal to
  the package copies, installed and hash-locked, and never read at runtime;
  only their presence is checked.
- `pyproject.toml`: `[tool.unittest]` has no consumer;
  `include-package-data` is redundant with the explicit `package-data`; 40
  template files listed, 40 on disk, none missing. The "44" files include
  four gitignored `.pyc` leftovers under `templates/…/scripts/__pycache__/`.
- `MANIFEST.in:4` `*.yaml` matches zero tracked files.
- Workflows: nine declared outputs no job consumes (`release-qualification.yml:
  43-49`, `publish-pypi.yml:48-51,185`, `pages-publication.yml:27-30`,
  `candidate-evidence.yml:35`); `pages-publication.yml:49,223,263` reads
  `snapshot_sha256`, which the script never emits, so an empty string reaches
  the run summary; the template `engineering-harness.yml:1-3` header
  describes steps the file no longer runs; `publish-pypi.yml` runs `python`
  in two jobs with no `setup-python`; `engineering-harness.yml:98,132` `||
  true` turns a guard refusal into a `JSONDecodeError` traceback; three
  action-pin generations coexist; Python `"3.11"` in 12 places and `"3.11.9"`
  in 2.
- Environment: `SE_HARNESS_AGENT_HOST` is set by one test and read by nothing
  (the test is vacuous); `SE_HARNESS_REHEARSAL` is read by `gate_source.py:
  100` and documented nowhere.
- `.gitignore:10,15` uses HTML-comment markers, which in gitignore syntax are
  literal patterns; `.gitattributes` already uses `#` markers and the
  extractor accepts both. Owner lines `:7-8` duplicate the managed fragment.
- Orphan fixtures (no reference anywhere): `tests/fixtures/publication_
  rehearsal/` (4 files; its consumer was deleted and a test asserts the
  consumer stays deleted) and four `phase4`/`contracts` vector files left by
  the Phase 4 removal.

## 5. Test suite

**Fact.** 56 test modules plus 4 support modules; 999 test methods defined,
1,265 discovered (verified with the loader).

- **266 redundant executions (21 %)** from subclassing `TestCase`s that carry
  tests: `tests/test_workflow_execution.py:950,1271,1497,1554` re-run the
  base's 37 tests four times (221 run for 73 defined); `tests/test_workflow_
  compliance.py:296-868` a three-level chain (145 for 42);
  `test_decision_management.py` 18 for 7; `test_artifact_authoring_policy.py`
  8 for 4. The runner's own timings put the five workflow-execution classes
  at a third of total class time.
- **Duplicated helpers:** 22 `invoke` definitions, 20 byte-equivalent and one
  correct one (`test_delegation_class.py:124` also catches `SystemExit`);
  9 `write`; 12 `git`/`_git` with accidental divergence in encoding,
  identity handling and `check=`; 5 `formal` in two lineages; the
  mutation-authority patch block in 19 modules; by-path module loading in 12.
- **A test module used as a library:** 10 modules import helpers from
  `tests/test_revision_provenance.py`. Because `tests/` is a namespace
  package, discovery and the importers load two distinct module objects
  (verified), so its import-time side effects run twice and a `mock.patch`
  on one copy misses the other.
- **Prose and count pins that no specification cites:** about 45 sentence
  pins on `docs/notes/*.md` in `tests/test_progressive_documentation.py:
  121-203`, 18 in `tests/test_public_onboarding.py:156-194`, router sentences
  with hard line breaks in `test_workflow_documentation_contract.py:165-193`;
  `managed_count_by_root` (`test_instruction_architecture.py:982`) and the
  `41` file count (`test_fixture_support.py:37`) must be edited on every
  release; three tests assert the length of a tuple defined in the same file.
  The README budget, the expertise labels, and the reference-covers-parser
  test are spec-backed and should stay.
- **Tombstones:** 61 `assertFalse(exists())` and 31 `assertNotIn(name,
  source)` sites across about 20 modules assert the absence of names that
  exist nowhere; 22 source-reading assertions on product code; two tests read
  other tests' source.
- **Structure:** `tests/test_public_onboarding.py:221` has `unittest.main()`
  mid-file, so a class defined after it never runs directly; `tests/
  skill_contract_support.py` (1,090 lines) validates three contract versions
  for two shipped skills and has no tests of its own; `tests/test_mutation_
  guard.py` imports from 12 product modules; CI YAML is pinned as prose by
  three modules.
- **Runtime:** the fixture cache is keyed by project name, so 8 workers and
  about 12 distinct names re-fill it per pair; 41 uncached direct `init`
  calls, 27 in `test_harnessctl.py` alone; CI runs the parallel runner with
  `--timings ""`, so longest-first ordering never benefits the lane that
  matters.

## 6. Remediation plan

Waves are ordered by value per unit of risk. Each item is a candidate work
order; none changes a public behaviour except where marked.

**Wave 0, correctness, one work order (S).**

- Route every checkpoint and transition error through `_split_code`
  (`cli.py:430,466,597`): removes the live doubled code.
- Introduce `MutationGuardError(HarnessError)` and catch it uniformly;
  `main()` catches `ProcedureError` and `WEX`-prefixed `ValueError`; move
  `_assignments` above the `try` in `_transition`. Public behaviour: exit 2
  where 1 or a traceback was returned.
- `renumber` human failure to stdout; `dashboard --json` passes 2 through and
  carries the engine's stderr; `pr-body` unknown artifact to exit 1 like its
  siblings. Add the missing `timeout` to `gate_source._git`, the four engine
  launches, `upgrade_rehearsal.run`; catch start failures in `gate_source`.
- Fix `REF_ARTIFACT_PATTERN` to include `OPS|DEC`; fix `evaluator_facts.
  _front_matter` on CRLF; fix `dashboard:404` projecting an array
  `verification_method` to `None`; `snapshot_sha256` in `pages-publication.
  yml`; `setup-python` in the two `publish-pypi.yml` jobs.

**Wave 1, delete (S each, one or two work orders).**

- Section 1.1 and 1.2 in full (about 300 lines in the core plus the engine
  items), the eight orphan fixtures, `MANIFEST.in:4`, `[tool.unittest]`, the
  stale `.pyc` residue, the vacuous `SE_HARNESS_AGENT_HOST` test, the nine
  unconsumed workflow outputs, the two unreachable contract entries with
  their documentation rows, `QG-G0-INTENT`'s predicates.
- The `adopt` alias (the follow-up WO-ECP-026 already anticipates; the
  0.16.0 verifier runs `init`).
- The three self-referential `len()` pins, `test_fixture_support.py:37`, the
  mid-file `unittest.main()`.

**Wave 2, one primitive each (M, one work order per row or grouped).**

- `se_harness/_process.py`: `run_git(root, *args, timeout=60)` and
  `run(argv, …)` with `shutil.which`, `stdin=DEVNULL`, an output cap,
  `(OSError, SubprocessError)` caught, an `error=` class parameter so each
  caller keeps its exception type. Replaces 13 launchers.
- `se_harness/front_matter.py`: one parser (BOM-tolerant, CR and CRLF
  normalized, line-anchored delimiters), returning the metadata and the body
  bytes. Replaces 8. Behaviour change only where a copy was wrong (CRLF).
- `integrity.py` gains `canonical_json_bytes`, `pretty_json_bytes`, the one
  duplicate-key hook, `atomic_write_bytes` with fsync; `repository_tools/
  json_bytes.py` re-exports them; rename `release_build.canonical_json_bytes`
  so recipe digests are unaffected. Replaces 16 SHA helpers, 9 hooks, 13
  serializers, 6 writers, 20 inlined normalizations.
- `se_harness/codes.py`: named constants for every diagnostic code, one
  `CodedError` base; `diagnostic_code_index.py` reads one module.
- `Literal`/`StrEnum` for `mode`, `action`, `checkpoint`, `phase`; export the
  checkpoint and definition-type sets from `workflow_contract.py` only.

**Wave 3, one engine (M to L).**

- Make `se_harness/engine/` an import surface (its own `__init__.py` names
  this as audit item #225). Then: one layout registry, one lifecycle loader,
  one evaluator-evidence validator, one status set derived from the contract,
  one body parser; `preflight`'s path loader and the four `cli.py`
  command-line assemblies go.
- Widen the validator's JSON report or pass its `ValidationReport` in-process
  so `provenance`, `release_qualification` and `renumber` stop re-parsing
  TOML; pass the report into `run_preflight` and `_generate_snapshot`; let
  `doctor` ask for `W013` without a full run. Halves the cost of every
  governance command.
- Split the validator along its eight seams and the dashboard at
  `build_snapshot` / `build_dashboard_bundle`; split `workflow_compliance.py`
  into change-set, evidence-packet and predicates modules and give
  `_classify`/`_diagnostic`/`project_scope` one home, which removes the
  `workflow ↔ workflow_compliance` cycle.

**Wave 4, tests (S to M, one work order).**

- Mixins instead of `TestCase` inheritance: removes 266 re-runs, about a
  third of class time.
- `tests/artifact_support.py` from `test_revision_provenance.py:98-312`;
  `cli_support.invoke` (SystemExit-safe); `git_support.git` (UTF-8, identity
  by env, gpgsign off); `patch_mutation_authority(case)`;
  `load_evaluator_module(name)` in `root_identity_support.py`.
- One table-driven `test_retired_surface.py` replacing 92 tombstone sites;
  derive `managed_count_by_root` from `template_files()`; replace un-cited
  prose pins with structural checks (headings exist, commands parse, links
  resolve, as `test_progressive_documentation.py:65-73,205-226` already do);
  a default fixture project name so the cache collapses; `--timings` on in
  CI.

**Wave 5, CI and configuration (S to M).**

- Drop the candidate-mode duplicate of `qualify complete-candidate` plus the
  suite in `release-qualification.yml` (per ADR-CIP-001 the release-record
  leg is the one that must stay); drop the inline re-checks in
  `candidate-evidence.yml:151-162,249-252`; consume `candidate_version`
  instead of re-deriving it; one Python version string; one action-pin
  style; a `concurrency` group on Pages deploys.
- Template edits shipped by release: prune the seven inert keys from
  `.engineering-harness.toml.tpl` and amend `REQ-SHB-009`; `#` markers in the
  `.gitignore` fragment; the `engineering-harness.yml` header and its
  `|| true`; document `SE_HARNESS_REHEARSAL` in SPEC-ECP-006.
- Finish or delete `scripts/migrate_verification_methods.py`; stop creating
  schema-1 bundles; put an end date on each compatibility window in 1.5 or
  migrate the 15 `constrains` architectures.

## 7. Decisions that are the owner's

1. **`journaled_apply.py`:** wire it in under REQ-ECP-017 or retire it with
   an amendment. Shipping it unused misstates the requirement's status.
2. **`renumber-artifacts` and `rehearse-recovery`:** remove, freeze (out of
   `--help`, module kept), or keep. Two assessments have recommended removal;
   together they are about 1,600 lines and 81 codes on the hash-bound
   surface.
3. **Compatibility windows:** an end condition for `constrains` (15 files),
   `legacy_missing` (14), missing `prepared_at` (85 records), missing
   `execution_scope` (111 work orders), or an explicit decision to keep them
   open.
4. **Declarative contract sections:** whether `agentic_operations`,
   `restitution_fields`, `aggregation` and `classes[].mode` should drive
   behaviour (wire) or be documented as declarative (and the Python copies
   kept as the operative truth).

## Appendix: measurements

| Measure | Value |
| --- | --- |
| Production lines (`se_harness`, `engine`, `scripts`, `repository_tools`) | 24,788 |
| Test lines | 28,236 |
| Modules with maintainability index rank C | 14 of 42 |
| Functions with cyclomatic complexity ≥ 30 | 30 |
| Functions over 80 lines (core package) | 17 |
| `pyflakes` findings (production / tests) | 11 / 23 |
| `vulture` findings at confidence 60 (production, tests as usage) | 41 |
| Cross-file duplicate blocks ≥ 8 lines (`pylint`) | 7 |
| Test methods defined / discovered | 999 / 1,265 |
| Most-changed production file (all history) | `se_harness/cli.py`, 50 commits |
| Diagnostic-code literal prefixes in `se_harness/` | 25 |
| Inert keys in `.engineering-harness.toml` | 7 of 13 |

Tools ran from `C:/Users/mathi/se-harness-lint` (a scratch environment
outside the checkout). The six review reports this note condenses were
produced on 2026-09-07 against `5e02039` and are not retained; every claim
above carries its own `path:line` for re-verification.
