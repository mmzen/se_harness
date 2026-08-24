# WO-WEX-003 implementation evidence

artifact: WO-WEX-003
checkpoint: handoff
formal_snapshot_sha256: 097858b454d795caded696d1e5ada5920c51c5b525936702062533c462ca6fc2

## Status

Implementation evidence retained on 2026-08-24. `WO-WEX-003` is
`implemented`. The engineering owner approved adding the two directly affected
test paths identified by the first complete-suite run, and the expanded focused
suite is green. The complete suite passes in a clean LF checkout; the original
Windows checkout's CRLF and sandbox-Git observations are retained below. No
assurance claim is made.

## Governing evaluator

- Role: released evaluator
- Version: `0.6.0`
- Installation: isolated external virtual environment outside the checkout
- Wheel: `se_harness-0.6.0-py3-none-any.whl`
- Wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
- Installed payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`
- Isolated identity check: passed
- Released-evaluator start preflight: passed with `ready = true`
- Released-evaluator review preflight: passed with `ready = true`
- Released-evaluator validation: `818` artifacts, `0` errors, `50`
  maintenance warnings, `valid = true`
- Released-evaluator `doctor`: passed; root distribution and managed hashes
  remain unchanged

## Lifecycle observations

- The six-artifact definition packet was explicitly transitioned from `draft`
  to `approved` in one atomic packet.
- `WO-WEX-003` was explicitly transitioned from `approved` to `in_progress`
  after focus, a passing start preflight, and the engineering-owner start
  instruction.
- The engineering owner explicitly expanded the execution scope on 2026-08-24
  with `tests/test_artifact_catalog.py` and
  `tests/test_context_routing_retirement.py` after the first complete-suite
  result identified their directly affected assertions.
- Related definition states did not change during the work-order start.
- After the passing handoff gate, the engineering owner explicitly decided to
  complete `WO-WEX-003`; the released evaluator atomically changed only that
  work order from `in_progress` to `implemented`.
- The implementation has not been verified or released.

## Implemented behavior

- Candidate `ENGINEERING_HARNESS.md`, `WORKFLOW.md`, `AGENTS.md`, and
  `CLAUDE.md` templates now treat schema-2 structured data as authoritative.
- Adaptive agent handoffs may change wording, order, headings, explanation, and
  empty-field presentation while preserving the closed lifecycle semantics and
  exactly one next action.
- Exact-format consumers are directed to the existing deterministic renderer;
  model transcription is explicitly excluded as an exactness mechanism.
- The schema-2 contract, workflow JSON, quality gates, procedures, runtime
  renderer, dependencies, and root managed files were not changed.
- Public overview and command-reference notes distinguish structured authority,
  direct exact rendering, and adaptive presentation.
- Tests now identify fixed heading assertions as direct-renderer guarantees and
  reject the old verbatim-model instruction across all candidate entry points.

## Changed implementation paths so far

- `templates/repository/standard/AGENTS.md.fragment`
- `templates/repository/standard/CLAUDE.md.fragment`
- `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`
- `templates/repository/standard/docs/engineering/WORKFLOW.md`
- `tests/test_instruction_architecture.py`
- `tests/test_artifact_catalog.py`
- `tests/test_context_routing_retirement.py`
- `tests/test_workflow_documentation_contract.py`
- `tests/test_workflow_restitution.py`
- `docs/notes/harness-overview.md`
- `docs/notes/harnessctl-reference.md`
- `docs/engineering/workflow-execution/evidence/WO-WEX-003-verification.md`

Every path above is admitted by `WO-WEX-003`. The six new governing formal
artifacts are separately attributable definition and lifecycle effects; they
are not implementation paths.

## Verification results

### Baseline focused suite

Command:

```text
python -m unittest tests.test_instruction_architecture tests.test_public_onboarding tests.test_standard_repository_lifecycle tests.test_workflow_documentation_contract tests.test_workflow_restitution
```

Result before implementation: `73 tests`, passed.

### Focused implementation suite

Same command after implementation: `75 tests`, passed in `30.234s`.

The narrower instruction/documentation/renderer selection ran `39 tests` and
passed in `23.509s` after one test assertion was corrected to compare normalized
policy prose rather than Markdown line wrapping.

### Complete repository suite

Command:

```text
python -m unittest discover -s tests -p "test_*.py"
```

Initial result before the scope expansion: `708 tests` in `390.164s`; `11
failures`, `24 errors`, `13 skipped`. The run was not a pass.

The directly affected findings were:

1. `tests.test_artifact_catalog.ArtifactCatalogTests.test_released_policy_copies_match_while_candidate_router_remains_isolated`
   still requires the released root router and candidate router to be equal.
   The approved architecture requires intentional candidate-only divergence
   until a later governed upgrade.
2. `tests.test_context_routing_retirement.ContextRoutingRetirementTests.test_packaged_fragment_block_matches_the_recorded_baseline`
   retained the pre-change digest of the candidate `AGENTS.md` fragment.
3. The initially affected progressive-documentation assertion was corrected
   within the admitted overview path and now passes independently.

The engineering owner approved both scope additions. The obsolete equality
assertion now proves deliberate released/candidate isolation, and the recorded
fragment digest now binds the changed candidate fragment.

A second complete-suite run used a process-local Git `safe.directory` setting
to permit repository discovery in this sandbox:

```text
python -m unittest discover -s tests -p "test_*.py" -b
```

Result: `712 tests` in `409.627s`; `7 failures`, `6 errors`, `12 skipped`. The
run is not a pass. None of the remaining failures is in a changed test or
candidate instruction/documentation component. They concern checkout CRLF
canonical-byte requirements, agent/release JSON canonicality, hash-bound
integrity, line-ending normalization, and test helpers that reject inherited
Git configuration. They are retained as complete-suite observations and were
not remediated by widening this work order.

To distinguish implementation behavior from checkout byte conversion, the
baseline commit was cloned from a local Git bundle into a disposable checkout
with `core.autocrlf = false`. The 11 tracked implementation-file changes were
applied as one Git patch; the formal packet and evidence remained separately
validated in the primary checkout. The complete suite was then repeated with
the same command:

```text
python -m unittest discover -s tests -p "test_*.py" -b
```

Result: PASS. `712 tests` in `452.103s`; `OK (skipped=12)`. This run includes
the candidate installation, package, distribution, workflow, direct-renderer,
instruction, and routing tests. The skips are platform- or fixture-conditional.
Advisory Git messages about possible future CRLF conversion in temporary test
repositories did not fail an assertion.

After the implementation commit was rebased onto upstream main commit
`5fb6a0c`, which adds the Phase 4 Claude/Codex Skill surfaces and evaluator
boundary changes, the same clean-LF complete suite was repeated. Result: PASS.
`804 tests` in `448.916s`; `OK (skipped=22)`. This is the final integrated
complete-suite result for the candidate prepared for commit-bound verification.

### Scope-expanded focused verification

Command:

```text
python -m unittest tests.test_progressive_documentation.ProgressiveDocumentationTests.test_validation_and_inspection_documentation_is_synchronized tests.test_artifact_catalog.ArtifactCatalogTests.test_released_policy_copies_match_while_candidate_router_remains_isolated tests.test_context_routing_retirement.ContextRoutingRetirementTests.test_packaged_fragment_block_matches_the_recorded_baseline
```

Result after the scope expansion and corrections: `3 tests`, passed.

The complete expanded focused command was:

```text
python -m unittest tests.test_instruction_architecture tests.test_artifact_catalog tests.test_context_routing_retirement tests.test_progressive_documentation tests.test_public_onboarding tests.test_standard_repository_lifecycle tests.test_workflow_documentation_contract tests.test_workflow_restitution
```

Result: `108 tests`, passed in `27.199s`.

After rebasing onto `5fb6a0c`, the expanded focused suite passed `109 tests` in
`33.993s` with no skips.

### Candidate and governing diagnostics

Candidate source reports version `0.6.0`. Candidate-source `validate . --json`
passed after integration with `818` artifacts, `0` errors, and `50` maintenance
warnings.
Candidate-source `doctor .` exited `1` as expected for the unreleased candidate:
candidate distribution files differ from the released root installation and
the candidate expects portable Skill files that are not installed in that
root. Its root managed-hash checks still passed. This candidate diagnostic is
not the governing released-evaluator result.

The isolated released 0.6.0 evaluator validated the same formal graph with
`818` artifacts and `0` errors. Its `doctor .` command passed all required,
distribution, lock, managed, script, seed, and Python checks; only existing
legacy-location `W013` advisories were emitted.

## Static observations

- No tracked implementation path has trailing-whitespace diagnostics from
  `git diff --check`.
- The old phrases `block verbatim` and `restitution verbatim` are absent from
  the four candidate instruction templates.
- Direct renderer tests still verify exact ordered headings, blockers, shared
  schema semantics, command arguments, invalid-result rejection, and repeated
  deterministic output.
- No runtime Python module, workflow JSON, quality-gate JSON, dependency,
  package metadata, CI workflow, Skill core, or root managed file was edited.

## Manual semantic assessment

- Completed case: the new policy permits a concise outcome-first explanation
  while requiring observed effects, remaining work, material non-effects,
  lifecycle state, accountable decision, and one next action.
- Blocked case: exact blockers and unchanged state remain mandatory even when
  headings and order change.
- Decision-required case: the accountable role and decision remain mandatory;
  the agent cannot claim to have exercised them.
- Command case: argument values and boundaries remain authoritative and must
  not be converted into shell syntax.
- Exact consumer case: only direct deterministic renderer output qualifies as
  exact; a model-generated imitation does not.
- The candidate Codex and Claude adapters were reviewed as thin presentation
  adapters for completed, blocked, and decision-required cases. The detailed
  policy owner preserves the same closed semantic projection for both. No live
  external Claude Code host was invoked, so assurance must treat this as static
  supported-adapter evidence rather than universal host-output proof.

## Review readiness

Released-evaluator review preflight passed with `ready = true`, no diagnostics,
and honest pre-completion `in_progress` status. The final handoff check passed all eight
`QGP-G4I-*` predicates, admitted all 12 declared implementation/evidence paths
within the 14-path execution scope, found no scoped or repository blocker, and
confirmed fresh evidence bound to formal snapshot
`5ff38a8d604debd6d3f9b6fa7793c6d95177db85c7dca702f249029aeecec202`.
It selected `PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-DECIDE` without writing. The
subsequent explicit completion decision changed only `WO-WEX-003` to
`implemented`. Candidate-ready pre-action then passed all three
`QGP-G4C-*` predicates and produced post-completion formal snapshot
`1a13ef6466a1d36961a01188cfbbc0acda9044ec3944f3d8e5f8f7e167cf7399`.
After rebasing onto upstream main, candidate-ready passed again and the current
integrated formal snapshot is
`097858b454d795caded696d1e5ada5920c51c5b525936702062533c462ca6fc2`.

## Non-effects

- The completion decision did not verify or release the implementation.
- No VREC assurance decision was exercised.
- The candidate commit, ready-VREC preparation, and authorized push occur after
  this retained implementation-evidence snapshot and are bound separately by
  the verification record and Git history.
- No pull request, merge, tag, release, publication, deployment, credential
  use, or operational external action occurred.
- The current root managed harness remains the released 0.6.0 installation;
  candidate template behavior is not yet active there.

## Residual uncertainty

External model hosts cannot be universally forced to preserve arbitrary final
prose. The structured result remains the authority, direct rendering remains
available for exact consumers, and supported-agent review supplies bounded
evidence rather than a universal enforcement claim.
