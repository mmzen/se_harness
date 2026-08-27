# WO-AEX-006 implementation evidence

This file records the implementation handoff checkpoint for `WO-AEX-006`.
It is implementer-generated evidence, not an assurance decision, verification
record, lifecycle transition, commit authorization, release decision, or
activation of Phase 4. The work order is `in_progress` at this checkpoint and
requires later independent commit-bound verification.

artifact: WO-AEX-006
checkpoint: handoff
formal_snapshot_sha256: 8a40043751fd8914682fe97ac7dd63e60d652f2298fc19ed176b57a52b29f942
pre_evidence_formal_snapshot_sha256: 8a40043751fd8914682fe97ac7dd63e60d652f2298fc19ed176b57a52b29f942
candidate_base_commit: 74df7b531eb0379b5b00cdcb1cc615f62b61abd7

## Candidate, dependency, and evaluator identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate branch: `feat/wo-aex-006-effect-broker`.
- Exact dependency/base commit:
  `74df7b531eb0379b5b00cdcb1cc615f62b61abd7`, containing the accepted
  `WO-AEX-005` result.
- This evidence does not identify a later commit containing the
  `WO-AEX-006` implementation or this file.
- Exact released evaluator used for lifecycle, preflight, doctor, formal
  validation, and checkpoint evaluation: `se-harness 0.6.0` from the isolated
  external launcher.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

Candidate code receives released-evaluator identity and authority evidence. It
does not claim that candidate source can establish its own authority.

## Implemented result

- Added the closed, canonical `se-harness-change-bundle-v1` transport schema.
  Its identity contains only the work-order ID, envelope digest, and
  repository-state-before digest. It contains no copied owners, scope,
  lifecycle, approval, or decision-right data.
- Added evaluator-owned baseline/proposed workspace comparison plus explicit
  intended deletions. Construction emits ordered create/replace/delete deltas
  and immutable, deduplicated `objects/<sha256>` content objects outside the
  target repository.
- Added the packaged `se-harness-effect-contract-catalog-v1` catalog for bundle,
  journal, receipt, operations, diagnostics, and bounds.
- Registered `change-bundle-apply` as the only Phase 4 mutation operation.
  Mutation-guard authority is checked before target writes, then the broker
  uses the verified `WO-AEX-005` live observer and fresh envelope-admission
  path. There is no alternate admission path.
- Added complete bundle/envelope/live-state foreign-key checks, envelope scope,
  default managed deny paths, expected-before states, object digest/size
  revalidation, and complete preflight/re-observation drift checks.
- Added pre-resolution rejection for supplied repository, workspace, object
  store, and runtime root aliases. Regular-file reads use descriptor identity
  checks and `O_NOFOLLOW` where supported; links, reparse points, hard-link
  aliases, special objects, case collisions, and preexisting planned temporary
  names fail closed.
- Added OS-backed session and effect locks, released automatically by process
  exit, while retaining external session and nonce state.
- Added a checksum-bound external journal containing the complete plan,
  manifests, parent and temporary inventory, applied paths, receipt identity,
  and bounded uncertainty. Prior bytes and receipt material stay outside the
  target checkout.
- Added canonical UTF-8 path-order application with exclusive temporary files
  and same-filesystem single-path replacement. Whole-bundle instantaneous
  visibility is not claimed.
- Added reverse ordinary rollback with exact prior-manifest proof, restart
  recovery to proved prior or proved committed result, durable receipt recovery,
  recovery-only nonce finalization, and explicit `human-recovery-stop` for
  corrupt or ambiguous material.
- Added the closed, canonical `se-harness-effect-receipt-v1` evidence schema.
  Receipts bind exact bundle, envelope, nonce digest, evaluator, work order,
  ordered effects, before/after state, prior receipt, transaction, timing,
  gates, deviations, and evidence. Authority or approval fields are prohibited.
- Added Phase 4 design and roadmap guidance. The documentation states that
  activation still requires a successor released evaluator, independent
  commit-bound assurance, and a separately governed disposable pilot.

## Operation and bound matrix

| Surface | Implemented bound or invariant | Result |
| --- | --- | --- |
| Operations | `create`, `replace`, `delete` only | Passed exact invariant and application tests |
| Bundle bytes | 1 MiB canonical JSON | Oversize rejected before semantic use |
| Bundle changes | 1 through 1,024 | Exact maximum accepted; 1,025 rejected |
| File content | 16 MiB per before/after object | Exact maximum accepted; overflow rejected before copy |
| Proposed content total | 64 MiB | Exact maximum accepted; overflow rejected |
| Effect journal | 4 MiB canonical JSON | Above 1 MiB accepted/read/archived; above 4 MiB rejected before persistence |
| Paths | Portable UTF-8, canonical order, unique and case-unique | Traversal, duplicate, case collision, alias, and noncanonical order rejected |
| Content objects | `objects/<sha256>`, exact size and digest, unaliased regular file | Sharing accepted; path substitution and corruption rejected |
| Writers | One OS-backed session writer and one effect writer | Nested/concurrent acquisition rejected; process exit releases locks |
| Visibility | Atomic replacement for one path | No cross-file atomicity claim |

## Failure, rollback, and restart observations

The in-process fault matrix injects an `OSError` at every public broker hook:
before journal creation; after prepared journal; after parent creation; after
each temporary; after each of the three applied entries; before result
observation; before receipt; and before commit. Every case reproduced the exact
prior complete manifest, archived a terminal rollback when a journal existed,
left no active journal or receipt, and consumed the admitted nonce.

Additional observations:

- faults before journal persistence do not invoke journal rollback;
- result-observer and receipt-validation failures restore the exact prior state;
- a real Windows locked destination fails replacement after earlier entries and
  rolls those entries back exactly;
- a preexisting deterministic temporary-name collision is preserved and
  rejected before journaling;
- `SystemExit` after prepared, after each durable applied-entry update, and
  after result-observed leaves an active journal and recovers the exact prior
  state;
- a child process using `os._exit(0)` releases both OS locks; a new store resumes
  the journal-bound session and recovers prior state;
- interruption after committed journal state recovers the exact durable receipt
  and complete result;
- an ordinary post-commit finalization fault marks recovery required, then
  proved committed recovery finalizes the nonce, archives the journal, clears
  the recovery block, and permits a new session;
- corrupt backup material and a checksum-mismatched journal stop at
  `human-recovery-stop` or recovery-required state without guessing;
- direct target change during preflight is detected and is never converted into
  an effect receipt.

## Retained working-tree identities

| Item | SHA-256 |
| --- | --- |
| Effect-contract catalog | `8386791c989d496dcc0cf225320eb4f7a987d61b1716c65af5da738c16a9f411` |
| Phase 4 canonical vector fixture | `e008abf37d216147c2bf3a1a3ad3928134c50584ddf3b9165ae760d40624c74d` |
| `change_bundle.py` | `60a7ad5ac445c0f8b07858a1e1ee37b687854d343178af08dbbf6098b6193c09` |
| `effect_broker.py` | `9a48831cfe06ac48d54498dd6676809b58a210089e5892ef308308736d2631d2` |
| `runtime_state.py` | `01ea34138036a38a6f84c13a9c366509f23ad61b7c7c37d3b5b83b25d10a2bfe` |
| Independent bundle canonical identity | `1f248a687d30bf62d191ca8e82dfaebe9dcab2b2a6697b59a3c7177f3d254c74` |
| Independent receipt canonical identity | `c50898b05446fcd5f7d427bbb1d48d446dded7b4e848da18cf7b4f67bb7ccf3f` |

These are working-tree identities, not commit-bound assurance identities.

## Verification observations

| Check | Result |
| --- | --- |
| Final focused Phase 4, live-authority, canonical-contract, and mutation-guard suite | Passed: 58 tests in 12.371 s; 1 privileged symlink-creation skip |
| Final exact complete repository suite | Passed: 982 tests in 306.835 s; 23 skips |
| Independent canonical public-byte vectors | Passed for bundle and receipt canonical bytes and SHA-256 |
| Descriptor, path, alias, and temporary attacks | Passed hard-link, managed `.git`, scope, traversal, duplicate, case, object corruption, root inspection, and temp-collision cases |
| Ordinary failure matrix | Passed every exposed pre-journal, journal, parent, temp, apply, observation, receipt, and pre-commit hook |
| Restart matrix | Passed every noncommitted durable phase plus committed receipt recovery |
| Lock and process behavior | Passed nested writer exclusion, child `os._exit` lock release, resume, and recovery |
| Windows locked destination | Passed exact rollback of earlier entries after replacement denial |
| Candidate bytecode compilation | Passed for `se_harness` and `tests` |
| Non-promotable ephemeral wheel acceptance | Passed: 1 test in 9.760 s |
| Release-distribution consistency | Passed for 1 distribution-bearing record |
| Exact 0.6.0 doctor | Passed required, distribution, managed, seed, lock, and Python checks |
| Exact 0.6.0 formal graph | Passed: 860 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Exact 0.6.0 review preflight | Ready: `WO-AEX-006` is `in_progress` with 0 diagnostics |
| Exact released CLI help | Passed for root, doctor, validate, and preflight surfaces |
| Whitespace and final-newline checks | Tracked `git diff --check` passed with informational Windows LF warnings only; all untracked files passed an independent final-newline/trailing-whitespace scan |
| Changed-path audit | 16 implementation/evidence paths are within declared exact/prefix scope; the separate work-order file change is only the released-evaluator lifecycle transition |
| Root managed-file integrity | Passed exact doctor; no root managed file changed |

## Changed-path audit

Implementation and evidence paths:

- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-006-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-phase4-effects.md`
- `docs/notes/agentic-execution-roadmap.md`
- `pyproject.toml`
- `se_harness/agent_contract.py`
- `se_harness/change_bundle.py`
- `se_harness/effect_broker.py`
- `se_harness/effect_contract.json`
- `se_harness/mutation_guard.py`
- `se_harness/runtime_state.py`
- `tests/fixtures/agentic_execution/phase4/broker/canonical-vectors.json`
- `tests/test_change_bundle.py`
- `tests/test_effect_broker.py`
- `tests/test_mutation_guard.py`

The released evaluator separately changed
`docs/engineering/agentic-execution/work-orders/WO-AEX-006.md` only to record
the approved-to-in-progress lifecycle event. It is not counted as an
implementer execution-scope change.

`MANIFEST.in`, `se_harness/agent_contract.json`,
`tests/mutation_guard_support.py`, and `tests/test_agent_contract.py` were
authorized but did not require changes. Existing `MANIFEST.in` wildcard
packaging plus the `pyproject.toml` package-data entry carries the new catalog.

## Deviations and residual uncertainty

- The Windows host did not permit creating the symlink used by one adversarial
  fixture, so that one case skipped. Static rejection, hard-link rejection,
  root pre-resolution checks, reparse checks, and descriptor identity checks
  ran; privileged symlink and junction cases still require independent
  supported-host execution.
- POSIX `O_NOFOLLOW` and permission behavior were not executed on this Windows
  host. Windows OS locks, locked-file replacement failure, and recovery were
  executed. POSIX assurance remains required.
- The fault matrix deterministically injects write/finalization exceptions; it
  does not claim a real hardware power-loss or exhausted-volume experiment.
  Hardware durability, disk-full behavior, and filesystem-specific guarantees
  remain independent-assurance work.
- The broker re-observes complete state, opens regular files by checked
  descriptors, rejects aliases, rechecks before each effect, uses exclusive
  temporaries, and serializes cooperating writers. Independent hostile-process
  stress is still required for parent-swap timing on every supported platform.
- Candidate unit tests, vectors, and this document are implementer-generated.
  They cannot satisfy `VER-AEX-004` independent assurance or replace a
  commit-bound `VREC`.

## Intentionally not performed

No transition to `implemented`, candidate commit, push, pull request,
verification record, assurance decision, release, installation, publication,
deployment, credential access, network effect, external-system action, real
target pilot, skill change, workflow-contract change, or root managed-file
change was performed by this implementation checkpoint.
