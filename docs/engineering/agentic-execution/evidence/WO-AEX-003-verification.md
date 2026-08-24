# WO-AEX-003 implementation evidence

This file records implementation-phase evidence for `WO-AEX-003`. It is not an
assurance decision, verification record, lifecycle transition, delivery choice,
release record, Git authorization, or external-action authorization. The
engineering owner accepted the implementation and transitioned the work order
to `implemented` at `2026-08-24T14:23:12Z`; independent commit-bound assurance
is still required.

artifact: WO-AEX-003
checkpoint: handoff
formal_snapshot_sha256: 04b636bc94517054b8736abd925e202b2cef0e007e2609662a724a4a010a47b5
candidate_base_commit: cda8a10f5e2534e6a24eff415ccedcbaf954d47c

## Candidate and evaluator identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate base commit observation:
  `cda8a10f5e2534e6a24eff415ccedcbaf954d47c` (`origin/main` after the clean
  Phase 3 rebase). This evidence is part of the implementation commit; the
  later VREC must bind that exact clean candidate commit.
- Exact released evaluator: `se-harness 0.6.0`, invoked through
  `../se-harness-eval/Scripts/python.exe -I` outside the checkout.
- Released identity: passed with isolated Python, disabled user site, absent
  `PYTHONPATH`, exact checkout boundary, and no diagnostics.
- Released wheel: `se_harness-0.6.0-py3-none-any.whl`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

Candidate source, verifier-owned ephemeral package fixtures, and the exact
released evaluator remain distinct.

## Implemented result

- Preserved the exact `harness-orient` v1 core, contract bytes, behavior,
  canonical vectors, manifest digest, and inline receipt behavior.
- Extended `se_harness.skill_contract` to validate both the closed v1 contract
  and exactly three `se-harness-skill-contract-v2` instances. V2 validation
  rejects duplicate and unknown fields, implicit activation, profile drift,
  lifecycle transitions, incomplete prohibitions, delegation, invalid
  checkpoint/effect/evidence/output declarations, and unsupported skills.
- Added canonical managed cores for `harness-draft-change`,
  `harness-execute-work-order`, and `harness-prepare-assurance` under the
  standard template. Each contains one `SKILL.md`, one strict contract, and one
  standard-library guard helper.
- Added injectable plan/effect boundaries. Draft effects require selected
  current drafts and declared destinations; implementation effects require an
  `in_progress` work order and current execution scope; assurance preparation
  requires an unused VREC ID, named preparer, and exact ready candidate.
- Added component-aware portable path admission, case-ambiguity checks, stale
  recheck rejection, closed effect classes, and zero-callback failure behavior.
- Added explicit source and wheel distribution metadata. The existing generic
  recursive installer required no source change: verifier cases prove it
  discovers, installs, locks, replays, upgrades, preserves customization, and
  rolls back every nested core.
- Added operator guidance explaining that skills complement `harnessctl`, use
  the exact released evaluator, remain single-agent, and stop before every
  accountable completion, assurance, delivery, release, Git, credential,
  network, and external-action boundary.

No CLI command, workflow operation, lifecycle state, authority rule, managed
policy, dependency, provider adapter, runtime profile, autonomy-envelope effect
API, subagent path, Git mutation, credential interface, network behavior, or
external integration was added.

## Portable identities

| Skill | Contract schema | Contract SHA-256 | Portable-core SHA-256 |
| --- | --- | --- | --- |
| `harness-orient` | `se-harness-skill-contract-v1` | `2c73e513c4b0b9189e32e6cfd485fe3148acb07014882f760cf2b2f2c67c72a3` | `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea` |
| `harness-draft-change` | `se-harness-skill-contract-v2` | `fec156c7c07d97e6a25eed06acdca54c622dd26aa1b14f72ce23e65e3f20f9f1` | `e04c232791b817a4138d5659a37dff11136a3a2937d90e26ba9c8fbca18ead78` |
| `harness-execute-work-order` | `se-harness-skill-contract-v2` | `0f93a7960174846125849052fa690e4d1c1899828e02b1febfc394c034e8c3b5` | `a34c7fa136c8a533c6e7abb1729ca36ad599521b012df18d5c624b413d03a8e2` |
| `harness-prepare-assurance` | `se-harness-skill-contract-v2` | `e004d2cecf29668ee249c94d02f3b830630dc8819fcd3a420625f0252f3e0f03` | `7075e1a42f264d7289e5a82bda04ec0e93bf9103389af22a07b235e87b7c4f24` |

The retained verifier vector at
`tests/fixtures/agentic_execution/phase3/portable_vectors.json` independently
binds all four contract and core identities. Existing Phase 1 vectors also
remain byte-identical.

## Focused behavior and distribution verification

| Check | Result |
| --- | --- |
| Phase 3 contract and effect-guard tests | Passed: all three closed v2 profiles, explicit activation, lifecycle matrix, path attacks, stale-state rejection, exact candidate/actor checks, and effect-sentinel counts |
| Phase 1 orientation regression | Passed: exact v1 manifest/vector and all black-box orientation cases |
| Five declared AEX/install/package/public test modules | Passed: 93 tests in 48.797 s; 2 platform skips |
| Fresh standard install | Passed: one byte-identical managed copy of all four cores and managed lock entries |
| No-op replay and safe upgrade | Passed: deterministic inventory; customized v1 and v2 skill bytes reported without overwrite |
| Interrupted installer apply | Passed: complete transaction restoration still covers nested managed skills |
| Explicit source distribution metadata | Passed: each canonical skill file selected once; no `se_harness/skills/` duplicate |
| Non-promotable ephemeral wheel fixture and fresh environment install | Passed: all 12 skill files present exactly once and installed byte-identically |
| Provider and authority scan | Passed: no provider-native file or provider name in skill instructions; contracts disable delegation and declare no lifecycle transitions |
| Python compilation and TOML parsing | Passed; Python 3.11-compatible standard-library source and valid `pyproject.toml` |
| Real build backend | Not assessable: the isolated workspace has neither `build` nor `setuptools`; no dependency installation or network action was authorized |

Effect sentinels were invoked exactly once for valid admitted plans and zero
times for implicit activation, non-`in_progress` states, non-draft revisions,
stale rechecks, path traversal, absolute/wildcard/URI paths, scope expansion,
dirty candidates, missing actors, and VREC collisions.

## Repository and exact-evaluator gates

| Check | Result |
| --- | --- |
| Exact released `identity` | Passed with the wheel and payload identities above |
| Exact released `doctor .` | Passed all installed integrity checks |
| Exact released `validate . --json` | Passed: 792 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| `git diff --check` | Passed; Windows line-materialization warnings only |
| Changed-path comparison | Passed for implementation paths: every implementation path is inside `WO-AEX-003`; the separately authorized Phase 3 artifact packet and lifecycle event are identified separately below |
| Exact released handoff checkpoint | Passed all 8 implementation-evidence predicates with a complete 24-path change set inside the 19-entry exact/prefix scope; recommended the engineering-owner completion decision without applying it |

## Complete repository-suite observation

The exact rebased candidate commit was checked out into an isolated detached
Git worktree with `core.autocrlf=false` and no injected process-level Git
configuration. `python -m unittest discover -s tests -v` ran 710 tests in
356.816 seconds: all passed, with 12 platform skips. This includes the Phase 3
skills, agent contract, installer, source/wheel distribution, lifecycle,
release-build, and predecessor-publication suites inherited from current
`origin/main`.

For transparency, the same command in the shared Windows checkout ran 710 tests
in 453.966 seconds and reported 6 failures, 3 errors, and 12 skips. Those
failures were limited to two host-materialization conditions: Git's system
`core.autocrlf=true` converted raw LF inputs used by hash-bound, release-build,
and packaged-skill byte tests; and the shared clone required injected
`safe.directory` process variables that predecessor-publication tests
intentionally reject. The isolated exact-commit run removed both conditions and
passed. No tracked file or Git configuration was changed to obtain that result.

## Changed implementation paths

- `MANIFEST.in`
- `README.md`
- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-003-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-skills-mvp.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `pyproject.toml`
- `se_harness/skill_contract.py`
- `templates/repository/standard/.agents/skills/harness-draft-change/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-draft-change/scripts/guard.py`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/scripts/check_prepare.py`
- `tests/fixtures/agentic_execution/phase3/portable_vectors.json`
- `tests/test_agentic_execution.py`
- `tests/test_instruction_architecture.py`
- `tests/test_public_onboarding.py`
- `tests/test_release_build.py`
- `tests/test_standard_repository_lifecycle.py`

Every listed path is admitted by `WO-AEX-003`. `se_harness/installer.py` did
not require a change because its existing recursive standard-template inventory
already manages arbitrary nested core files; the new install, upgrade,
customization, lock, and rollback tests prove the required Phase 3 behavior.

The five approved Phase 3 formal artifacts, their preceding proposal note, and
the `WO-AEX-003` start lifecycle event were separately authorized governance
changes made before implementation. They are not counted as implementation
paths or helper-controlled skill effects.

## Deviations and residual uncertainty

1. The shared checkout cannot itself provide a clean byte-level suite result
   because of the two Windows host conditions described above; the exact commit
   passed in the isolated LF worktree.
2. The real PEP 517 backend was unavailable without installing a dependency.
   The verifier-owned wheel fixture proves the explicit installed inventory but
   does not replace a later commit-bound real-build assessment.
3. Windows cannot create unprivileged symlink and case-collision hostile
   filesystem cases. Those tests remain active on capable hosts; platform-
   neutral path and case-boundary tests passed.
4. The helpers expose an injectable controlled-effect boundary and the skill
   procedure requires current released-evaluator rechecks. Phase 3 does not
   claim enforcement against a hostile runtime that ignores the skill.
5. This implementer-generated evidence is not independent assurance and cannot
   bind the commit that will contain itself. The later VREC must assess the
   exact clean candidate commit and real packaged bytes.

## Intentionally not performed

The explicitly authorized work-completion transition was applied. No VREC
preparation, assurance decision, delivery selection, commit, branch, push, pull
request, merge, tag, credential access, network action, publication,
deployment, operation, or other external action was performed during the
implementation stage. No autonomy envelope admitted an effect, and no
subagent, worker, runtime adapter, or provider profile was created or invoked.
