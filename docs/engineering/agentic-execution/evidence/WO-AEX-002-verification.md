# WO-AEX-002 implementation evidence

This file records implementation-phase evidence for `WO-AEX-002`. It is not an
assurance decision, verification record, release record, authoritative envelope,
effect admission, or authorization for an external action. The work order is
`implemented`; its repository owner requires later commit-bound verification.

artifact: WO-AEX-002
checkpoint: handoff
formal_snapshot_sha256: a29b8932d892ee71b03470c227c7c7addde58c82ca0c97d27ac57a4a32d271a7
candidate_base_commit: 7248822bfe45874badf7b0694b1c965960556171

## Candidate and evaluator identity

- Candidate source version: `0.6.0`.
- Candidate runtime: CPython `3.14.6` on Windows.
- Candidate base commit observation:
  `7248822bfe45874badf7b0694b1c965960556171`, the refreshed `origin/main`
  head used before the final implementation candidate commit. The later ready
  VREC binds the exact clean candidate commit; this evidence file does not
  attempt to contain the hash of its own commit.
- Exact released evaluator: `se-harness 0.6.0`, invoked through
  `../se-harness-eval/Scripts/python.exe -I` outside the checkout.
- Released identity result: passed with isolated Python, disabled user site,
  absent `PYTHONPATH`, exact checkout boundary, and no diagnostics.
- Released wheel: `se_harness-0.6.0-py3-none-any.whl`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

Candidate source, candidate package fixtures, and the exact released evaluator
were kept as distinct identities. No candidate module was used as the governing
released evaluator.

## Implemented result

- Added canonical `se-harness-agent-contract-catalog-v1` data covering the
  eight approved schema roots, 144 referenced definitions, closed field sets,
  compatibility unions, collection semantics, bounds, and diagnostics
  `AEXCON001` through `AEXCON018`.
- Added a standard-library pure contract module with bounded UTF-8 JSON parsing,
  duplicate-key detection, unknown-field rejection, canonical JSON and digest
  functions, portable-path validation, and strict schema dispatch.
- Added supplied-observation construction for worktree state and repository
  binding candidates, including exact deleted, executable, symlink, gitlink,
  untracked, object-format, work-order, formal-snapshot, managed-lock, and
  digest relations.
- Added envelope request/managed-scope intersection, parent-digest validation,
  monotonic child checks, and pure operation assessment across identity,
  operation, path, profile, writer, retry, evidence, and stop dimensions.
- Added workflow-result-v2 plus packet-context-v1 projection to decision packet
  v2, packet v1 validation-only compatibility, and deterministic human heading
  order without an invented decision or recommendation.
- Added Phase 2 receipt validation and independent `ReceiptExpectations`
  comparison while retaining the Phase 1 operation and `AEXORI` deviation
  variants.
- Added provider-neutral logical-profile validation with mandatory accountable
  stops and single-agent fallback.
- Added no dependency, CLI command, workflow rule, live repository observer,
  mutation-guard integration, skill, worker orchestration, runtime adapter, or
  provider configuration.

Successful pure outcomes remain `constructed` and `admissible`. The module has
no effect callback and cannot return `derived` or `admitted`.

## Contract and vector identities

| Item | SHA-256 or observation |
| --- | --- |
| Canonical catalog | `ed1c741009f209aaec98aac0bf7473cefaea1b7fb5d2b3041ce8b0d8ddef181a` |
| Canonical catalog size | 58,396 bytes |
| Worktree-state vector | `98ff4f3b430294dec297527ff138b9afc72e5575945988e3b62ea8fb881e3663` |
| Repository-state-binding vector | `e86f9218f23abbb356523041e05ff9b80e2094dba1c670e35ad36d9b84285855` |
| Autonomy-envelope vector | `f0adb71510d80c0692f11af7f05b600b5ee65722426340baf37405f27412087d` |
| Logical-profile vector | `0f96bfcf7693d3ec506f85561db7e826a504fe59d9d632a3928e0a8abefbeef6` |
| Unchanged Phase 1 portable core | `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea` |
| Unchanged Phase 1 receipt vector | `96701a0b7b7c0d7fa15decd2cec59f49a46ce730317644a07e2c6aff90c845b0` |

The catalog validator proved that source bytes already equal canonical bytes,
all named references resolve once, all definitions are used, schema records are
ordered, and the diagnostic and bounds tables equal the approved v1 contract.

## Focused contract, compatibility, and package verification

| Check | Result |
| --- | --- |
| `python -B -m unittest tests.test_agent_contract -v` | Passed: 13 tests |
| `python -B -m unittest tests.test_agent_contract tests.test_agentic_execution tests.test_release_build -v` | Passed after rebase: 37 tests in 19.611 s; 2 Windows capability skips |
| Canonical catalog source/package declaration | Passed; `pyproject.toml` names `agent_contract.json` and `MANIFEST.in` already includes `se_harness/*.json` |
| Non-promotable ephemeral wheel and fresh install | Passed; the wheel contains canonical `se_harness/agent_contract.json` and the unchanged one-copy Phase 1 skill core |
| Phase 1 receipt compatibility | Passed with byte-identical canonical bytes and digest |
| Phase 1 portable-core identity | Passed unchanged |
| Static import/effect scan | Passed; standard library only and no filesystem, Git, process, network, credential, lifecycle, or callback API |

The focused tests cover duplicate keys, unknown fields, invalid UTF-8, BOM,
floats, non-finite and oversized values, unsafe paths, case collisions, invalid
worktree field combinations, catalog tampering, canonical order permutations,
all eight public schemas, packet source conflicts, receipt coverage and hidden
authority, provider-bound profiles, and the complete envelope widening and
admission-denial matrix. A caller-side sentinel received zero calls for every
denied, stale, or accountable-stop assessment.

## Capacity observations

One deterministic envelope containing the stated count in each operation,
path, profile, and retry collection produced:

| Entries | Canonical bytes | Validation time |
| ---: | ---: | ---: |
| 100 | 6,038 | 0.001903 s |
| 500 | 27,638 | 0.024498 s |
| 1,000 | 54,638 | 0.082171 s |

A separate test proves that worktree observations admit 1,025 entries under
their 100,000-entry/64 MiB observation bound while ordinary arrays still fail
above 1,024 entries. No repository entry was silently omitted.

## Repository and exact-evaluator gates

| Check | Result |
| --- | --- |
| `python -B scripts/validate_engineering_artifacts.py --root .` | Passed after rebase: 778 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released `validate . --json` | Passed after rebase: 778 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released `doctor .` | Passed all installed integrity checks |
| exact released runtime `identity` | Passed with the wheel and payload identities above |
| exact released review preflight | Passed with no diagnostics; commit-bound verification remains required |
| exact released handoff checkpoint | Passed all 8 predicates with a complete 10-path change set inside the 13-path scope before the explicit completion transition; the checkpoint itself had no lifecycle effect |
| `python -B scripts/validate_release_distributions.py --root .` | Passed: 1 distribution-bearing record; used a process-local Git `safe.directory` entry because the sandbox account does not own the checkout |
| `python -B -m se_harness --help` | Passed |
| candidate `doctor .` | Expected forward-skew failure: candidate templates and the current managed root differ, and the managed Phase 1 skill copy is absent in this checkout; no root refresh was authorized or performed |

The exact released evaluator is the governing installed contract. Candidate
doctor skew is retained as boundary evidence and was not used to overwrite
managed root content. After rebasing, the exact released formal snapshot is
`a29b8932d892ee71b03470c227c7c7addde58c82ca0c97d27ac57a4a32d271a7`.

## Complete repository-suite observation

The final complete discovery command executed 694 tests in 442.620 seconds with
12 platform skips and one failure. It ran as the checkout owner so Git-based
tests did not inherit a sandbox `safe.directory` override. The only failure,
`test_hash_bound_integrity.DeclarationShapeTests.test_declaration_is_data_only`,
found 79 CRLF line endings in `se_harness/hash_bound_classes.json`.

The CRLF file is outside `WO-AEX-002`, has no Git status or numeric diff, and
was not edited. Correcting its checkout materialization would exceed this work
order. The focused AEX, Phase 1 regression, distribution, and package suites
pass after the final implementation changes.

## Changed implementation paths

- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-002-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-contracts.md`
- `pyproject.toml`
- `se_harness/agent_contract.json`
- `se_harness/agent_contract.py`
- `tests/fixtures/agentic_execution/contracts/canonical-vectors.json`
- `tests/test_agent_contract.py`
- `tests/test_release_build.py`

Every implementation path is admitted by the `WO-AEX-002` execution scope.
`MANIFEST.in` already distributes `se_harness/*.json`, so it did not require a
change. `se_harness/skill_contract.py`, `tests/test_agentic_execution.py`, and
the remaining declared paths did not require changes. The work-order lifecycle
event is a separate governed start transition and is not counted as an
implementation path.

## Deviations and residual uncertainty

1. The complete suite is not globally green on this Windows materialization
   because of the one untouched CRLF-sensitive test described above. No
   out-of-scope repair was attempted.
2. The host Git configuration uses `core.autocrlf=true`. The rebase initially
   materialized the tracked catalog's terminal LF as CRLF, and three focused
   tests rejected those non-canonical working-tree bytes. The tracked Git blob
   was already the 58,396-byte canonical LF form; the final focused run used
   those exact tracked bytes and passed. A future Windows checkout that ignores
   the catalog's canonical-byte requirement can reproduce this local
   materialization issue.
3. Windows could not create two unprivileged hostile skill filesystem cases;
   those tests remain active on capable hosts. Contract path and case-collision
   tests are platform-neutral and passed.
4. The capacity measurements use deterministic supplied values, not a live
   repository observation. Phase 2 intentionally contains no live observer.
5. This evidence is implementer-generated and is retained in the candidate
   commit. It cannot satisfy the required later independent, commit-bound
   assurance decision by itself.
6. Repository-local contracts cannot authenticate a real-world actor, prove a
   human judgment is substantively correct, or prove that undisclosed work did
   not occur outside the observation boundary.

## Intentionally not performed

No outcome-oriented skill was added or invoked. No live autonomy envelope was
derived or persisted, no effect was admitted, and no mutation guard, workflow
command, worker, subagent, worktree, adapter, model default, permission change,
credential, assurance decision, merge, release record, tag, publication, or
deployment was performed. Local branch and candidate-commit preparation are
repository-integration steps and do not verify or release the work.
