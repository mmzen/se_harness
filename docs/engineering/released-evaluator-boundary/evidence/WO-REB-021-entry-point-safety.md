# WO-REB-021 Entry-Point Safety Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one platform at one commit. Commit-bound assurance for this work order remains a separate `VREC` decision, and this file is not that decision. After accountable review of this evidence the engineering owner accepted the implementation and transitioned `WO-REB-021` to `implemented` at `2026-08-24T14:43:03Z`. The two coverage gaps in section 7 remain explicit inputs to independent assurance review.

artifact: WO-REB-021
checkpoint: handoff
formal_snapshot_sha256: 2fea33ef7bcefd766d2362187ba31c2909cfe3dc26ee88a340049f08be54690e

## 1. Governing packet and preflight

`WO-REB-021` implements `REQ-REB-023`, `REQ-REB-024`, `REQ-REB-025` and `REQ-REB-026` under `SPEC-REB-011`, `ARCH-REB-010`, `ADR-REB-010` and `VER-REB-010`. All ten packet artifacts and the work order were transitioned `draft` to `approved` by the engineering owner at `2026-08-24T13:01:45Z`, and the work order `approved` to `in_progress` at `2026-08-24T13:04:22Z`. The owner holds the requirements-steward, technical-owner, quality-owner, security-owner, repository-owner and engineering-owner roles in this repository and recorded the approval as one act.

Preflight was run from the released 0.6.0 evaluator installed in a virtual environment outside this checkout:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness preflight . --work-order WO-REB-021
Harness preflight: PASS
Phase: start
Work order: WO-REB-021 (in_progress)
Assurance classification: commit-bound verification required, decided by engineering-owner
WARN count: 0
exit code 0
```

The same evaluator reports `0.6.0` on Python `3.14.6`. Full-graph validation from that evaluator:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness validate . --json
artifact_count 784 | error_count 0 | warning_count 50 | valid true
taxonomy se-harness-validation-taxonomy-v1
```

The repository-owned gate scripts agree from the development interpreter:

```text
python scripts/validate_engineering_artifacts.py --root .
PASS | Artifacts: 784 | Errors: 0 | Warnings: 50

python scripts/validate_release_distributions.py --root .
PASS (1 distribution-bearing record)

python scripts/check_portable_release_surface.py --repository .
PASS

python -m se_harness --help
exit code 0
```

All 50 warnings are maintenance-plane `W013` canonical-location notices on retained release-directory artifacts. They are the same 50 the packet inherited, so this work order added none.

## 2. Base commit and independently captured baseline

The branch `feat/reb-safe-venv-identity` was rebased onto the merged `WO-HBI-002` work before implementation began. The pre-rebase base was `1431df5`; the post-rebase base is `7248822`. `git merge-base --is-ancestor 7248822 HEAD` succeeds, so the rebase is a fact of the tree rather than a claim. The three commits between the base and the implementation working tree are documentation and lifecycle only:

```text
6979859 Approve the entry-point safety packet and start WO-REB-021
e7146be Record the owner sequencing decision in WO-REB-021
e1aebdf Propose the declared entry-point safety packet for issue #106
```

The baseline was captured independently, in a clean detached worktree at the base commit, not by reasoning about the current tree:

```text
git worktree add --detach <throwaway> 7248822
python -m unittest discover -s tests -p "test_*.py"
Ran 681 tests in 317.418s
FAILED (failures=4, skipped=12)
```

The four base-commit failures, by name:

- `test_agentic_execution.SkillContractTests.test_contract_rejects_duplicate_and_unknown_fields`
- `test_agentic_execution.SkillContractTests.test_manifest_normalizes_line_endings_and_detects_content_changes`
- `test_hash_bound_integrity.DeclarationShapeTests.test_declaration_is_data_only`
- `test_release_build.DeterministicSdistTests.test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core`

All four are the known Windows line-ending reds: this checkout has `core.autocrlf` behaviour that gives CRLF in the working copy for paths `.gitattributes` does not pin, and each of these four compares bytes read back from such a path. They are platform facts of the base commit, not regressions from this work order. The throwaway worktree was removed after capture; `git worktree list` shows only the working checkout.

## 3. Changed-path manifest

Measured with `git diff --numstat 7248822` plus `git ls-files --others --exclude-standard`. Twenty-six tracked paths changed and four new source files were added. This evidence file is the fifth new file; it is declared in the work order's `[execution_scope]` and carries no front matter, as retained evidence does not.

New files, with measured bytes and SHA-256 as committed (all LF, CR count zero):

| Path | Lines | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `se_harness/interpreter_safety.json` | 317 | 11193 | `04cd0de61eeca6590e8368e6bdd08e2d3adbc697a526ab74b3695f4d6972a378` |
| `se_harness/interpreter_safety.py` | 555 | 22156 | `9dd9dbf76e21892baed1bf66d8f8e78f70f113ad123aa1701558373da541eb09` |
| `repository_tools/interpreter_safety.py` | 554 | 22095 | `afce85c19d7e5f36de515e2b56e5888b2d998e966d3920c32f181a5797765f8c` |
| `tests/test_interpreter_safety.py` | 1221 | 56619 | `7866569cf64e4217781af1d3d7aa1715b7ac6a74d4a0a9e4088e61279e01ea90` |

Production and script changes, added/removed lines:

| Path | + | - |
| --- | --- | --- |
| `pyproject.toml` | 1 | 0 |
| `repository_tools/predecessor_assessment.py` | 53 | 26 |
| `repository_tools/predecessor_preparation.py` | 31 | 35 |
| `repository_tools/predecessor_publication.py` | 8 | 4 |
| `repository_tools/release_bootstrap.py` | 72 | 7 |
| `scripts/check_portable_release_surface.py` | 11 | 1 |
| `se_harness/governance_migration.py` | 49 | 9 |
| `se_harness/governance_migration_contract.json` | 6 | 6 |
| `se_harness/release_qualification.py` | 9 | 14 |
| `se_harness/runtime_identity.py` | 46 | 2 |

Test changes, added/removed lines:

| Path | + | - |
| --- | --- | --- |
| `tests/test_context_routing_retirement.py` | 2 | 0 |
| `tests/test_mutation_guard.py` | 3 | 0 |
| `tests/test_release_orchestration.py` | 2 | 0 |

Artifact and note changes: `README.md` 8/0; `ARCH-REB-010.md` 158/0; `ADR-REB-010.md` 121/0; `REQ-REB-023.md` 71/0; `REQ-REB-024.md` 86/0; `REQ-REB-025.md` 88/0; `REQ-REB-026.md` 91/0; `SPEC-REB-011.md` 177/0; `VER-REB-010.md` 171/0; `WO-REB-021.md` 272/0; `docs/notes/developing-se-harness.md` 15/0; `docs/notes/evaluator-recovery-runbook.md` 4/0; `docs/notes/harnessctl-reference.md` 4/0.

Every changed path is listed in the work order's `[execution_scope]`, including the two paths added by the second scope amendment recorded in section 15. One in-scope path was deliberately left unchanged: `se_harness/evaluator_evidence.py`. The lexical normalization the sidecars needed was placed in `repository_tools/release_bootstrap._lexical_origin`, at the boundary that produces the origin, so the sidecar writer required no change. Section 11 proves the sidecar bytes did not move.

## 4. Declared cases and the bidirectional corpus comparison

The declaration is `se_harness/interpreter_safety.json`, schema `se-harness-interpreter-safety-v1`, with top-level keys `boundaries`, `cases`, `corpus`, `outcomes`, `position_classes`, `schema`. Its SHA-256 is `04cd0de6…2378`. Both loaders return identical `declaration_bytes()` and an identical `EVALUATION_ORDER`:

```text
('EPS010', 'EPS011', 'EPS001', 'EPS002', 'EPS003', 'EPS004',
 'EPS005', 'EPS006', 'EPS007', 'EPS008', 'EPS009')
```

Eleven cases, all with outcome `refused`, in declared evaluation order:

| Case | Refusal |
| --- | --- |
| `EPS010` | the lexical path has fewer than two parent components, so no environment root can be derived from it |
| `EPS011` | the runtime cannot classify a path as a symbolic link or a directory junction, so link safety cannot be decided |
| `EPS001` | an enclosing directory of the lexical path is a symbolic link |
| `EPS002` | an enclosing directory of the lexical path is a directory junction |
| `EPS003` | the lexical path does not resolve strictly |
| `EPS004` | the lexical path or its resolved target is not an ordinary file |
| `EPS005` | the final component traverses a link without being a symbolic link |
| `EPS006` | the resolved target's own path traverses a link |
| `EPS007` | the lexical path lies inside the supplied checkout root |
| `EPS008` | the resolved target lies inside the supplied checkout root |
| `EPS009` | the lexical path does not lie lexically inside the supplied declared environment root with a non-empty remainder |

The comparison with the test-owned corpus is bidirectional and both directions are exhaustive equality, not containment. `DeclarationShapeTests` and `BidirectionalCorpusTests` assert that every declared case has at least one corpus entry expecting it, that every corpus `expected` value is either `accepted` or a declared case identifier, that the set of case identifiers reachable from the corpus equals the declared set, and that `RuleEvaluationTests` contains exactly one `test_isc0NN_*` method per corpus entry with no extra and no missing method. A case added to the declaration without a corpus entry fails, and a corpus entry added without a test method fails.

## 5. Boundary registry and the independent inventory

The declaration registers eight boundaries: seven of kind `rule` across six modules, and one of kind `delegating`.

| Identifier | Kind | Module | Runtime | Purpose |
| --- | --- | --- | --- | --- |
| `repository_tools.predecessor_assessment.external_interpreter` | rule | `repository_tools/predecessor_assessment.py` | `repository_tools` | accept the released-evaluator interpreter before each hosted assessment command |
| `repository_tools.predecessor_assessment.interpreter_origin` | rule | `repository_tools/predecessor_assessment.py` | `repository_tools` | normalize a verified released-evaluator interpreter origin for retained evidence |
| `repository_tools.predecessor_preparation.external_interpreter` | rule | `repository_tools/predecessor_preparation.py` | `repository_tools` | validate an externally supplied predecessor interpreter |
| `repository_tools.predecessor_publication.external_interpreter` | delegating | `repository_tools/predecessor_publication.py` | `repository_tools` | reach the rule for a published predecessor interpreter (delegates to `repository_tools.predecessor_preparation.external_interpreter`) |
| `repository_tools.release_bootstrap.released_evaluator` | rule | `repository_tools/release_bootstrap.py` | `repository_tools` | bind a released evaluator to a release record |
| `se_harness.governance_migration.runtime_probe` | rule | `se_harness/governance_migration.py` | `se_harness` | probe a predecessor or successor migration runtime |
| `se_harness.release_qualification.external_evaluator` | rule | `se_harness/release_qualification.py` | `se_harness` | locate an external predecessor evaluator environment |
| `se_harness.runtime_identity.installed_interpreter` | rule | `se_harness/runtime_identity.py` | `se_harness` | observe the running interpreter for a declared runtime role |

The registry was checked against an inventory the test module owns rather than reads from the declaration. `BoundaryRegistryTests` compares the declared registry against `EXPECTED_RULE_BOUNDARIES`, a literal mapping of six module paths to their rule-boundary counts — `repository_tools/predecessor_assessment.py` two, each of the other five one — and against `EXPECTED_DELEGATING_BOUNDARIES`, the single entry `repository_tools/predecessor_publication.py`. The comparison is equality in both directions, so an unregistered boundary and a registered-but-absent one both fail. `StaticArchitectureTests.test_every_rule_boundary_reaches_the_loader_instead_of_deciding_for_itself` additionally requires the string `interpreter_safety` to appear in every registered rule module, so a module cannot be registered while quietly keeping its own decision.

## 6. Per-boundary before and after

The rule replaced six independently written checks. Before, each boundary derived the environment root from `interpreter.parent.parent.resolve(strict=True)` or an equivalent, which leaves a POSIX virtual environment through its `bin/python` symbolic link; each accepted or refused link forms on its own terms; and none detected a Windows directory junction. After, each calls one loader and reports the declared case identifier in its own error vocabulary.

| Boundary | Before | After |
| --- | --- | --- |
| `predecessor_assessment.external_interpreter` | `_released_identity` computed `evaluator_python.parent.parent.resolve(strict=True)`; no link or junction judgment on the entry itself | calls `_safe_interpreter`, uses `safe.environment_root` and spawns `safe.entry_point`; additionally cross-checks the reported `python_entry_is_link`, `python_binary_position` and `python_binary_sha256` against the locally observed facts |
| `predecessor_assessment.interpreter_origin` | `_normalize_interpreter_origin` resolved the declared root, then applied its own file, parent-link and terminal-link tests through `bootstrap._path_has_link` | delegates the whole decision to `_safe_interpreter(..., declared_root=evaluator_root)` and renders the accepted lexical entry point; the recorded origin can no longer be a resolved system binary |
| `predecessor_preparation.external_interpreter` | `_ordinary_external_interpreter` hand-wrote parent-link, strict-resolve, ordinary-file, target-link and checkout-containment tests, each with its own prose message | `_safe_interpreter` calls the loader; `_ordinary_external_interpreter` remains as a thin accessor returning `.entry_point`, so existing callers keep their signature |
| `predecessor_publication.external_interpreter` | called `preparation._ordinary_external_interpreter`, then recomputed `python.parent.parent` in four places, including two evidence-redaction replacements | calls `preparation._safe_interpreter` once and threads the accepted `evaluator_root` through `_run_predecessor`, so the evidence marker and the payload root come from the same accepted derivation |
| `release_bootstrap.released_evaluator` | `_prepare` accepted the interpreter as `_ordinary_external_file`, which resolves the path, and `_run_released_evaluator` recomputed `parent.parent.resolve(strict=True)`; `_normalize_origin` resolved the interpreter origin, which refuses a POSIX venv | `_safe_interpreter` accepts it; `_lexical_origin` normalizes the interpreter origin without resolving; the identity cross-check requires the reported `python_executable` to equal the accepted lexical entry point and compares the three new facts |
| `governance_migration.runtime_probe` | `_runtime_identity` required an existing file, called `_assert_external`, took `lexical.parent.parent` unchecked, and refused only when `environment_root` or `lexical.parent` was a symbolic link — a junction passed | `_safe_interpreter` calls the loader and maps each declared case onto the migration diagnostic that already reported that class of refusal, through the total mapping `INTERPRETER_REFUSAL_CODES`: `MIG202` for the three containment and root cases, `MIG204` for the three existence and shape cases, `MIG205` for the five link cases |
| `release_qualification.external_evaluator` | `_external_evaluator_files` resolved the path, required a file, then tested containment by resolving `parent.parent` and comparing to the checkout | calls the loader and takes `entry.environment_root`; the entry-point candidate search below it is unchanged |
| `runtime_identity.installed_interpreter` | no interpreter-safety judgment at all; the role checks tested runtime prefix and origins only | observes the launcher through the loader for every role, records `python_entry_is_link`, `python_binary_position` and `python_binary_sha256`, and emits `RID024` only for an environment-bounded role |

`ENVIRONMENT_BOUNDED_ROLES` is `{"released-evaluator", "candidate-package"}`. `candidate-source` deliberately has no environment boundary, because its expected root is the checkout itself, so a refusal there would contradict `EPS007`. The observation is still recorded for `candidate-source`; only the diagnostic is withheld. `RID004` and `RID006` keep their existing meanings; the new refusal has its own code `RID024`, so no existing diagnostic changed meaning.

The three new `RuntimeIdentity` fields are additive under the unchanged schema `se-harness-runtime-identity-v3`. Identity consumers test `required.issubset(identity)` rather than an exact field set, so a consumer holding the previous field list still validates. `tests/test_mutation_guard.py` gained the three fields in its passing-identity fixture, which is the only place an exact identity had to be extended; its eleven tests pass.

One acceptance narrowed rather than widened. `EPS010` refuses an interpreter path with fewer than two parent components, so an interpreter sitting directly below a filesystem root — `C:\python.exe`, `/python` — is now refused where several boundaries previously computed a meaningless root from it. Such a path cannot be a virtual environment, and no supported configuration produces one, but the change is a refusal that did not exist before and is recorded here as an exception to acceptance monotonicity rather than buried.

## 7. Adversarial corpus results

Eighteen corpus entries. `constructable_on` is declared per entry, and each unconstructable combination carries an `unconstructable_reason` in the declaration itself rather than a bare skip in the test.

| Entry | Form | Expected | Constructable on | Result on this lane (Windows 11, Python 3.14.6) |
| --- | --- | --- | --- | --- |
| ISC001 | ordinary-file-entry | accepted | linux, windows | ran, accepted |
| ISC002 | terminal-symlink-entry | accepted | linux | skipped: symbolic-link creation needs a privilege the ordinary Windows developer and CI accounts do not hold (WinError 1314) |
| ISC003 | hardlink-entry | accepted | linux, windows | ran, accepted |
| ISC004 | symlink-parent | `EPS001` | linux | skipped, WinError 1314 |
| ISC005 | junction-parent | `EPS002` | windows | ran, refused `EPS002` |
| ISC006 | dangling-terminal-symlink | `EPS003` | linux | skipped, WinError 1314 |
| ISC007 | absent-entry | `EPS003` | linux, windows | ran, refused `EPS003` |
| ISC008 | directory-entry | `EPS004` | linux, windows | ran, refused `EPS004` |
| ISC009 | terminal-junction-entry | `EPS004` | windows | ran, refused `EPS004` |
| ISC010 | file-position-non-symbolic-link | `EPS005` | neither | recorded unconstructable on both platforms |
| ISC011 | chained-resolved-target | `EPS006` | neither | recorded unconstructable on both platforms |
| ISC012 | entry-inside-checkout | `EPS007` | linux, windows | ran, refused `EPS007` |
| ISC013 | target-inside-checkout | `EPS008` | linux | skipped, WinError 1314 |
| ISC014 | outside-declared-root | `EPS009` | linux, windows | ran, refused `EPS009` |
| ISC015 | rootless-entry | `EPS010` | linux, windows | ran, refused `EPS010` |
| ISC016 | no-link-classification-capability | `EPS011` | linux, windows | ran, refused `EPS011` |
| ISC017 | relative-entry | accepted | linux, windows | ran, accepted |
| ISC018 | parent-component-entry | accepted | linux, windows | ran, accepted |

The two cases constructable on neither platform are documented rather than asserted away. `ISC010` cannot be built because a junction is always a directory and is refused by `EPS004` before the final-component rule is reached, and the only file-position reparse point Windows offers is an application execution alias, which fails strict resolution with WinError 1920 and so is refused by `EPS003` first. `ISC011` cannot be built because strict resolution is fully transitive on both platforms: a chain of junctions or symbolic links resolves to a path traversing none. `EPS006` is therefore retained as a defence against a partially resolvable path rather than as a reachable form. Both facts are declared, so a future runtime that does make one constructable will fail the shape test rather than silently pass.

Junction detection is exercised for real on this lane, because creating a directory junction on Windows needs no special privilege. Both routes are exercised on this lane as well, by withdrawing the capability from the loader rather than by finding a runtime that lacks it: `_without_routes` patches `JUNCTION_PREDICATE` to an absent attribute name and `REPARSE_CONSTANTS` to absent constant names, so the `stat` reparse-point route is executed with the `pathlib` route withdrawn, the `pathlib` route with the `stat` route withdrawn, and `EPS011` is proved when both are withdrawn — for both loaders. `pathlib.Path.is_junction` exists only from Python 3.12, `requires-python` is `>=3.11`, and every CI lane pins `3.11`, so the `stat` fallback is the route that actually runs in CI; withdrawal is what lets a 3.14 development lane execute it.

Two coverage gaps remain and are disclosed rather than implied closed. The four Linux-only corpus forms were not executed anywhere in this evidence, because this lane is Windows and no Linux run was performed; only the hosted `3.11` Linux lane can execute them. And no genuine Python 3.11 interpreter ran the module here; capability withdrawal proves the fallback logic, not the 3.11 runtime.

## 8. Purity, cost, and import instrumentation

`PurityAndCostTests` instruments the evaluation directly rather than asserting about it:

- Every filesystem entry under the fixture is compared by `st_mtime_ns` before and after an evaluation. Evaluation mutates nothing.
- `subprocess.Popen` and `socket.socket` are patched to raise. An accepted evaluation and a refused one both complete, so the rule performs no spawn and opens no socket. This is the property that matters for the boundary: the refusal happens strictly before any interpreter is executed.
- `Path.resolve`, the module's `_digest`, and the module's `_traverses_link` are wrapped with counters. One observation resolves the entry once, digests exactly the resolved target once, and walks exactly twice — `(entry, include_self=False)` and `(resolved_target, include_self=True)`. A regression that resolved or digested twice per observation fails.
- Where two declared cases both match, the declared order decides. A path that is simultaneously inside the checkout and under a symbolic-link parent reports `EPS001`, not `EPS007`, so the identifier in a diagnostic is stable.
- The environment root never depends on the resolved target: an entry symbolically linked to a deep system path still reports its own lexical grandparent as the root. This is the defect from RC-060-06, asserted directly. It is one of the skips on this lane, for the WinError 1314 reason above.

Import instrumentation is static and exhaustive. `ImportBarrierTests` parses every module in both packages with `ast`:

- `repository_tools` may import from `se_harness` only the five names under `se_harness.hash_bound` pinned in `PERMITTED_PACKAGE_IMPORTS`. That crossing is pre-existing.
- `se_harness` may import from `repository_tools` only the two names pinned in `PERMITTED_TOOLS_IMPORTS`: `predecessor_publication.PredecessorPublicationError` and `predecessor_publication.validate_predecessor_publication`. Both directions are exhaustive equality against a pinned inventory, so a new crossing in either direction fails.
- That second crossing is also pre-existing, and this work order neither created nor widened it. `git show 7248822:se_harness/release_qualification.py` shows it at line 637 in the same shape. A separate test proves the shape rather than trusting it: `release_qualification.py` has no module-level `ImportFrom` naming `repository_tools`, and exactly one `try` block whose body holds the import and whose handler names `ImportError`, raising `HarnessError("the fixed predecessor-view service is unavailable")`. The package therefore installs and runs without `repository_tools` present.
- A third test proves neither permitted crossing carries an interpreter-safety name, so the two loaders remain independent implementations of one declaration and the conformance check remains meaningful rather than tautological.

Two static architecture tests replaced earlier over-broad prohibitions with exhaustive retained-form inventories, because two legitimate pre-existing uses exist and an absolute ban was simply wrong:

- `RETAINED_INLINE_JUNCTION_FUNCTIONS` pins the one function that still names the junction predicate inline — `repository_tools/release_bootstrap._path_has_link` — with the reason it may: it walks repository files, installed-payload members and record directories, none of which is an interpreter entry point. The test compares the pinned set against the AST-derived set by equality, then checks all seven call sites of that function and requires none to pass an interpreter-named first argument.
- `RETAINED_GRANDPARENT_DERIVATIONS` pins the three surviving `<x>.parent.parent` expressions — `contract_path.parent.parent`, `record_path.parent.parent`, `Path(__file__).parent.parent` — again by equality, and additionally requires each retained expression to contain none of `python`, `interpreter`, `executable`, and no `resolve()`. A new interpreter-derived root therefore fails even though the shape itself is still permitted for contract, record and package paths.

## 9. Recorded-facts matrix

Measured on this lane against the real released 0.6.0 evaluator environment at `C:\Users\mathi\se_harness_eval_060`, entry point `Scripts\python.exe`, with both loaders, and with the target digest computed independently of the loader:

| Fact | `se_harness.interpreter_safety` | `repository_tools.interpreter_safety` |
| --- | --- | --- |
| `entry_point` | `<evaluator-root>\Scripts\python.exe` | identical |
| `environment_root` | `<evaluator-root>` | identical |
| `environment_root == entry_point.parent.parent` | true | true |
| `entry_is_link` | false | false |
| `binary_position` | `within-expected-root` | `within-expected-root` |
| `binary_sha256` | `199ce15a9f0d4f9522edba59338e4879d28cf61f88e377b8164bcb716275ed22` | identical |
| equals independently computed digest | true | true |
| `normalized_origin` | `<evaluator-root>/Scripts/python.exe` | identical |

`link_classification_available()` is true here and both routes are present on 3.14. The declared `position_classes` are exactly `outside-declared-roots`, `within-checkout-root`, `within-expected-root`, and the declared `outcomes` are exactly `accepted`, `refused`.

Three live refusals were measured against real paths on this lane, both loaders agreeing on every one:

| Probe | Case |
| --- | --- |
| a path lexically inside this checkout, offered with `checkout_root` set to the checkout | `EPS007` |
| `C:/python.exe`, an interpreter directly below a filesystem root | `EPS010` |
| the valid evaluator entry point offered against this checkout as its declared root | `EPS009` |

The Windows shape above is the normal one. A POSIX virtual environment normally reports `entry_is_link` true and `binary_position` `outside-declared-roots`, because `bin/python` points at the system interpreter; that is the accepted shape and not a finding. What fails on either platform is a target inside the operational checkout.

## 10. Governance-migration and package-data digests

`se_harness/governance_migration_contract.json` pins the SHA-256 of `se_harness/governance_migration.py` in six adapter entries, and `_implementation_identity()` raises `MIG215` on mismatch. The implementation changed, so the pin was re-measured, not assumed:

```text
measured sha256 of se_harness/governance_migration.py:
  e8cdadd36e74494d793e98c9c70a718a87fd062a4929d51096da23238279fddc
implementation_sha256 pins found in the contract: 6
all six equal the measured digest: true
previous pinned value: bcdaf2078e4161b4f18749f48560d9f3045a6cbab10363da9c8ca154179c6231
```

Both files are `text eol=lf` in `.gitattributes` and both are CR-free in the worktree, so the digest is the same on either platform.

The declaration is new package data. `pyproject.toml` gained `interpreter_safety.json` to `[tool.setuptools.package-data] se_harness`, and `scripts/check_portable_release_surface.py` gained `REQUIRED_INTERPRETER_SAFETY_MEMBERS` covering `se_harness/interpreter_safety.json` and `se_harness/interpreter_safety.py`, so a wheel missing either member now fails the portable-surface check rather than shipping a package whose loader cannot read its own policy.

The declaration is deliberately not byte-pinned in `.gitattributes`, and `.gitattributes` was not edited — it is outside this work order's scope. Nothing digests the declaration bytes: the loaders parse it as JSON and the conformance check compares parsed structures, so a line-ending difference between platforms cannot break a digest. The measured `04cd0de6…2378` above is a fact of this worktree, not a pinned invariant, and section 4's assertions are about structure rather than bytes.

## 11. Evaluator-evidence sidecars before and after

All fourteen JSON evidence sidecars under `docs/engineering/**/evidence/` were digested in the worktree and compared against `git show 7248822:<path>`. Every one is unchanged:

| Digest prefix | Paths |
| --- | --- |
| `fcfc14471cc373fc` | the ten `VREC-*-evaluator.json` sidecars: `VREC-AEX-001`, `VREC-HBI-001`, `VREC-HBI-002`, `VREC-IPK-001`, `VREC-LRE-001`, `VREC-REB-016`, `VREC-HUP-003`, `VREC-HUP-004`, `VREC-HUP-005`, `VREC-VSP-002` |
| `11a4aec338f1da10` | `RLS-SEH-009-evaluator.json`, `RLS-SEH-012-evaluator.json` |
| `77474d1e22422371` | `RLS-SEH-012-preparation-view.json` |
| `83398eb76d73a96a` | `WO-HUP-002-evaluator-upgrade.json` |

The ten `VREC` sidecars sharing one digest is expected and not a defect: the same evaluator environment yields the same evidence bytes, and the candidate binding lives in the record's commit and dashboard snapshot rather than in the sidecar. `git status --porcelain` lists none of these paths, which is the same fact by a second route.

## 12. Non-change proofs

- Managed hash-locked paths: `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, `.github/workflows/engineering-harness.yml`, the seven managed documents under `docs/engineering/`, all of `docs/engineering/templates/`, and the eight managed scripts are absent from `git status --porcelain`, so all are byte-unchanged. `scripts/check_portable_release_surface.py` is repository-owned, not managed, and is the only script touched.
- Lock: `.engineering-harness.lock` is unchanged. No fragment digest moved, and `tests/test_context_routing_retirement.py::test_fragment_digests_equal_their_lock_entries` passes against it.
- Owner regions: `AGENTS.md`, `CLAUDE.md` and `.gitignore` are unchanged, so no tracked fragment block was touched.
- `.gitattributes` is unchanged, as its exclusion from scope requires.
- History: the three commits between `7248822` and the implementation tree are listed in section 2. No commit was amended and no history was rewritten; `git merge-base --is-ancestor 7248822 HEAD` holds.
- Refs and tags: 47 refs and 9 tags — `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.3.0`, `v0.4.0`, `v0.4.1`, `v0.5.0`, `v0.5.0a1`, `v0.6.0` — unchanged. No tag was created, moved, or deleted.
- Distributions: `scripts/validate_release_distributions.py --root .` passes with one distribution-bearing record, unchanged. No wheel or sdist was built. No `VREC` or `RLS` artifact was created, transitioned, or edited.

## 13. Focused and full suite

Focused, this lane:

```text
python -m unittest -v tests.test_interpreter_safety
Ran 83 tests in 1.035s
OK (skipped=10)
```

All ten skips carry an explicit reason and all ten are the Windows symbolic-link privilege (WinError 1314) or a declared Linux-only corpus form: `ISC002`, `ISC004`, `ISC006` and `ISC013` from the corpus, and six behavioural tests that need a symbolic link — junction-versus-symlink disjointness, the lexical-root proof, first-refusal-wins, the repointed-link fact change, the `outside-declared-roots` position class, and the link-cycle refusal. None is a skipped assertion about the rule's Windows behaviour, and none hides a failure: the same forms run on the Linux lane, which reports no skips for this module.

Full suite, this lane:

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 764 tests
FAILED (failures=4, skipped=22)
```

The delta against the independently captured base-commit baseline is exactly the work: 764 − 681 = 83 tests, which is the new module in full, and 22 − 12 = 10 skips, which are the ten enumerated above. The four failures are the same four names as the baseline, listed in section 2, so this work order introduced no failure and repaired none.

Two failures encountered during implementation were repaired inside the amended scope and are green in the run above: `tests/test_release_orchestration.py` failed with `SurfaceError: wheel is missing required package member: se_harness/interpreter_safety.json`, because the wheel fixture built its member list from the two pre-existing required sets, and `tests/test_context_routing_retirement.py::test_only_recorded_files_name_the_retired_path` failed with two extra mentions, because `ADR-REB-010.md` and `REQ-REB-023.md` name this repository's owner-owned engineering context document as an affected operator path. Section 15 records the owner decision that authorized both fixes.

Seven mutation-guard errors earlier in implementation were repaired by adding the three new identity fields to the passing-identity fixture in `tests/test_mutation_guard.py`; its eleven tests pass.

No Linux run is recorded here. The hosted `3.11` lanes are the only place the Linux corpus forms and a genuine 3.11 runtime execute, and this evidence does not stand in for them.

## 14. WO-HBI-002 sequencing, as decided by the owner

The disclosed overlap with `WO-HBI-002` was put to the engineering owner, who decided that `WO-HBI-002` goes first. It was merged as `7248822` (pull request #130), and this branch was rebased onto it before implementation, which is why the base commit in section 2 is `7248822` and not the earlier `1431df5`. The decision is recorded in the work order itself, in commit `e7146be`.

A consequence worth stating plainly: a verified `VREC` binds an exact commit, and a branch rebase orphans that commit. This work order's implementation commits therefore must not be rebased once a `VREC` binds one of them, and no `VREC` has been prepared here.

## 15. Amendments

Three amendments were taken during implementation, all by the engineering owner and all recorded in `WO-REB-021` itself before being applied.

1. **Scope amendment.** Recorded in the work order as `## Scope amendment, 2026-08-24`, keeping the fix rather than narrowing it.
2. **Rule 4 amendment.** The specification's own rule 4 was amended to name the fallback route explicitly, because `pathlib.Path.is_junction` is unavailable on the pinned `3.11` CI runtime and a rule that named only the pathlib predicate would have described an unreachable implementation.
3. **Second scope amendment.** The work order's stop-and-escalate condition "Another file … is required" fired for two test files outside `[execution_scope]`. Both remedies were measured first, by applying and reverting each: `tests/test_release_orchestration.py` needed two added lines and none removed, `tests/test_context_routing_retirement.py` needed two added lines and none removed, and both modules were green with the change and red without it. The alternative — stripping those references from `ADR-REB-010` and `REQ-REB-023`, which are approved artifacts — was put to the owner and rejected. The owner amended the scope to add both files. The amendment authorizes those four lines and nothing else. No assertion was weakened: both inventories remain exhaustive equality checks, and the mention inventory gained two named entries with recorded reasons rather than a wildcard.

The second scope amendment deliberately does not spell the retired path itself, so the mention inventory needs exactly the two authorized entries and no third.

## 16. Actions not performed

Nothing in this file authorizes any of the following, and none was performed:

- no push, no branch publication, no pull request opened, edited, or merged;
- no hosted workflow dispatch, and no CI run triggered by this work;
- no `VREC` or `RLS` artifact created, transitioned, edited, or superseded, and no capture-verification run;
- no lifecycle transition beyond the packet approval and the work order's `approved` to `in_progress` start already recorded in section 1;
- no release, no tag, no wheel or sdist build, promotable or ephemeral, and no distribution binding;
- no publication, no credential use, no network mutation, no deployment;
- no root-evaluator adoption, no governor adoption, no lock or managed-path write, no upgrade transaction, and no recovery rehearsal;
- no external policy change, and no change to any artifact outside this work order's amended `[execution_scope]`;
- no history rewrite, no ref or tag mutation, and no edit to `.gitattributes`.

The one next accountable act this evidence supports is a decision by the engineering owner on whether the implementation is ready to be offered for commit-bound verification, given the two disclosed coverage gaps in section 7.
