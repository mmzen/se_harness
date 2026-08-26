# WO-AEX-008 implementation evidence

This file records the implementation handoff checkpoint for `WO-AEX-008`.
It is implementer-generated evidence, not an assurance decision, verification
record, lifecycle transition, candidate-commit authorization, release decision,
or activation of Phase 4. The work order remains `in_progress` at this
checkpoint and requires later independent commit-bound verification.

artifact: WO-AEX-008
checkpoint: handoff
formal_snapshot_sha256: 9225dc6e868d4b2a00ecdd618cc7afeff7e0ddabe6f118070e47695eac62c2b4
pre_evidence_formal_snapshot_sha256: 9225dc6e868d4b2a00ecdd618cc7afeff7e0ddabe6f118070e47695eac62c2b4
candidate_base_commit: 8406289ce03bb7ff009510df6271cd7b9af78cda

## Candidate, dependency, and evaluator identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate branch: `feat/wo-aex-008-phase4-skills`.
- Exact merged `WO-AEX-005` dependency line:
  `74df7b531eb0379b5b00cdcb1cc615f62b61abd7`.
- Exact verified `WO-AEX-006` candidate:
  `61c6880ea8799fb397baf3b8ae3c2f080e0d2199`.
- Exact `WO-AEX-007` implementation candidate:
  `71efd2ae62befcb1d48d81f2cf184e85d5e1d324`.
- Exact verified `WO-AEX-007` stacked base:
  `8406289ce03bb7ff009510df6271cd7b9af78cda`.
- This evidence does not identify a later commit containing the
  `WO-AEX-008` implementation or this file.
- Exact released evaluator used for lifecycle start, doctor, formal
  validation, identity, and help checks: `se-harness 0.6.0` from
  `C:\Users\mathi\Documents\Codex\ev4b-01a037e8\Scripts\python.exe`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

The payload value above is intentionally the exact evaluator-reported identity,
not a candidate-source assertion. The candidate remains non-promotable and
cannot govern its own work order.

## Implemented result

- Added the closed `se-harness-skill-contract-v3` profile for exactly the three
  writing skills and versioned each portable core from `1.0.0` to `2.0.0`.
- Converted all three writing helpers into non-authoritative clients of the
  verified workflow-v4 evaluator boundary. No injected target-write callback
  or direct governed-target write remains.
- Bound each client request to the exact four-row operation catalog, explicit
  activation, valid delegation identity, work-order state, target path, and
  `se-harness-evaluator-client-request-v1` / result schemas.
- Preserved single-agent execution, no child delegation, no parallel writer,
  evaluator-owned bundle construction and application, receipt continuity,
  canonical restitution, and the existing Phase 4 lifecycle stops.
- Kept `harness-orient` v1 byte-identical and read-only. Its contract, manifest,
  helper, prose, vector, policy, and host behavior were not changed.
- Kept each Claude surface as a one-file, same-name, explicit-only adapter that
  loads the canonical `.agents` core. No evaluator workflow, permission, hook,
  model, or script was copied into an adapter.
- Added current-v3 and retained-v2 portable vectors plus closed client attack
  and success cases. Updated source, wheel, install, host, lifecycle, rollback,
  public-onboarding, and instruction-architecture qualification.
- Added bounded Phase 4 operator and installation documentation while retaining
  the public package version at `0.6.0`.

## Contract and evaluator-client matrix

| Skill | Prior portable contract | Candidate contract | Evaluator client | Terminal boundary |
| --- | --- | --- | --- | --- |
| `harness-draft-change` | v2 / `1.0.0` | v3 / `2.0.0` | `delegated-workflow execute` using start, bundle, complete | Canonical evaluator restitution; no target write |
| `harness-execute-work-order` | v2 / `1.0.0` | v3 / `2.0.0` | `delegated-workflow execute` using start, bundle, complete | `completed-at-git-stop` |
| `harness-prepare-assurance` | v2 / `1.0.0` | v3 / `2.0.0` | `delegated-workflow prepare-vrec` | Git stop or independent assurance stop |

Every v3 profile is explicit-only, has `max_parallel_writers = 1`, prohibits
child delegation and direct target writes, identifies the evaluator as bundle
owner and target writer, requires the workflow-v4 catalog, and fails closed
when only the public 0.6.0 command surface is available.

The client catalog remains exactly:

| Operation | Decision right | Required state | Result state | Gate |
| --- | --- | --- | --- | --- |
| `delegated-work-order-start` | `DR-WO-START` | `approved` | `in_progress` | G3 work authorization |
| `change-bundle-apply` | none | `in_progress` | `in_progress` | G4 implementation evidence |
| `delegated-work-order-complete` | `DR-WO-COMPLETE` | `in_progress` | `implemented` | G4 implementation evidence |
| `delegated-vrec-prepare` | `DR-VREC-PREPARE` | `implemented` | `implemented` | G4 candidate ready |

## Portable and host identities

The manifest identities below are computed portable-core identities rather
than paths to stored manifest files.

| Skill | Contract identity | Manifest identity |
| --- | --- | --- |
| `harness-orient` v1 | `2c73e513c4b0b9189e32e6cfd485fe3148acb07014882f760cf2b2f2c67c72a3` | `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea` |
| `harness-draft-change` v3 | `318ddf054dc14407ef586df79dea52d03510bd2423f2f91cb90d87a45c04d3a6` | `c37e706a356f6ad506f5b0ca30f13727ead596a7a651b6c3be3e8994cf314343` |
| `harness-execute-work-order` v3 | `dd7eebb0be2f0af680f27c5e9bb645d9662bffd6003f2a380832f9924eb92f38` | `1fc827f6985b08fb0320aed188ff5506e8979e563bc11012c640edddd92eff2d` |
| `harness-prepare-assurance` v3 | `f957b423db8355e0a9c9d95ea55a9859c2dc39659f9df44c7fbd41564b2634b7` | `29b3da990f5747b069e2d89b9de81c419986406ff9503a3797040a8dd7763402` |

Retained historical v2 contract/manifest pairs are:

- draft: `6a143cbdfd958ac64e72d20c37db8dc0789cb4e94d436b1a54548736846a37d6` /
  `9622908238967d8813164467390fd3ff42de1c86923dd2462a4942ef01142525`;
- execute: `766ed39615c044f659db6141c34952b1b48cd76377eb42d39932ac4375de5949` /
  `112bf6b1c6d56b061727c44fa3ba7aa15d8492b8b7f0003889e42741ee509ea0`;
- prepare: `5303a574db8dd79c4bd73577aa94763a647af2d67bf4a9b5918e84a9649d7609` /
  `9f73d2b2699f4c0fa31b9e700af9b3fdbe7240ac69867a909064f299e33b8adc`.

Retained working-tree file identities:

| Item | SHA-256 |
| --- | --- |
| Orientation helper | `02adac90805941f2efc2e667faf3849e3bfc0b05e8ab4a80260595b8e253ee04` |
| Orientation contract file | `8e51bcc50b00edbd834a443f134835e04b655ccfaf02a3953c03a45287386627` |
| Orientation core prose | `487216696f211d6668f5131df354189bb39dea29dc5e738ae90fca77d912c386` |
| Draft client helper | `bb7fd59305675df915160b4cf6c05a0d9d74383f13597744927911fada2db7d0` |
| Execute client helper | `b3067d4b73b1a408882bf215b00bce33db3049fdd73c9582cdbf3aa58b892ccb` |
| Assurance client helper | `056f627408f76483b0fdd7a5223b002e5d1f61830b4527b8013cc3e96e3c3f92` |
| Draft Claude adapter | `33c1376e2533c55070d811cdad2c45a4a071ecfcc378ff98358ba4eb6ae33245` |
| Execute Claude adapter | `6e738fb90d090c5f2806aa7c21a2a29b94fd98681e756fe07de824796737b1f0` |
| Assurance Claude adapter | `5c6a9bf4e4fec439293deb1413eb126cbfef6ea45dcfa22747d7d0dcc1013a1a` |
| Phase 4 portable vectors | `2bd369b0f9e980f123b54089871b9dac07b9dc342d2d7e106bb1e8e063ca6ad1` |
| Phase 4 client cases | `df8b232a74af112d1b476801f67a905f2372284c7b296c35307581c5fc9898d8` |
| Phase 4 skill note | `c902d9e654268ef9e3e1fd366223044a78b58c27196aef73ed68d6e6a22b4302` |

These are working-tree identities and cannot substitute for the later exact
candidate commit required by independent assurance.

## Verification observations

| Check | Result |
| --- | --- |
| Five declared skill/instruction/onboarding/build/lifecycle modules | Passed: 122 tests in 38.859 s; 2 skips |
| Phase 4 authority/bundle/broker/workflow dependency suite | Passed: 72 tests in 74.417 s; 1 skip |
| Complete candidate-source repository suite | Passed: 1,004 tests in 394.326 s; 23 skips |
| Scale qualification | Passed at 100, 500, and 1,000 formal artifacts; largest validate/focus/plan path 0.989 s |
| Candidate formal graph | Passed: 862 artifacts, 0 errors; formal snapshot retained above |
| Exact 0.6.0 doctor and root integrity | Passed all installation, distribution, managed-file, lock, and Python checks |
| Exact 0.6.0 formal validation | Passed: 862 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Exact 0.6.0 command boundary | Passed expected stop: public help has no `delegated-workflow`; help SHA-256 `45cde4b406d8aafc5482b0f326d31499ed9f973cdd155b426c2ae7dc4984e125` |
| Candidate operation catalog | Passed exact ordered four-row comparison and client capability checks |
| Explicit/implicit and attack matrix | Passed explicit success; implicit, old evaluator, invalid delegation, active conflict, direct-write, path/state, missing-commit, and assurance-stop cases |
| Codex/Claude parity | Passed canonical/adapter static identity, policy, naming, loading, root/nested fixture, source, wheel, and fresh-install tests |
| Fresh install and repository lifecycle | Passed fresh init (59 files), doctor, validate, adopt/replay/upgrade, managed lock, customization conflict, and rollback suites |
| Whitespace and scope | `git diff --check` passed; all implementation/evidence changes fall within exact or prefix scope |

The `agents/openai.yaml` policy bytes remain identical across writing skills and
retain `allow_implicit_invocation: false`. The installed-wheel test observed all
three writing skills at `2.0.0` and the unchanged orientation core at v1.

## Non-promotable package qualification

The environment had no `build` frontend, so the bundled offline Python runtime
invoked `setuptools.build_meta` directly in a disposable copy outside the Git
worktree. This exercised the same declared package metadata without network
access.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `se_harness-0.6.0-py3-none-any.whl` | 467,475 | `0a065bea8d2997809d9da5606aef2b0de7f531f8606c7aeec01b507643d3a4a2` |
| `se_harness-0.6.0.tar.gz` | 671,377 | `7481e4c99d4decbb8a757c2e0aefeb5ccf4cc8c97c1767525776019a15a7a58a` |

The wheel contains `delegated_workflow.py`, `skill_contract.py`, all 18 files
of the four canonical cores, and all four Claude adapters. The source archive
contains every WO-AEX-008 test module plus the retained Phase 3 vector and both
Phase 4 skill vectors. A real fresh virtual-environment install from the wheel
passed init, doctor, formal validation, and exact installed contract-version
checks. The artifacts remain outside the repository and are not promotable.

## Changed-path audit

Implementation and evidence paths:

- `MANIFEST.in`
- `README.md`
- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-008-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-phase4-skills.md`
- `docs/notes/agentic-execution-roadmap.md`
- `docs/notes/agentic-execution-skills-mvp.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `pyproject.toml`
- `se_harness/skill_contract.py`
- `templates/repository/standard/.agents/skills/harness-draft-change/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-draft-change/scripts/guard.py`
- `templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/scripts/check_prepare.py`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/skill-contract.json`
- `templates/repository/standard/.claude/skills/harness-draft-change/SKILL.md`
- `templates/repository/standard/.claude/skills/harness-execute-work-order/SKILL.md`
- `templates/repository/standard/.claude/skills/harness-prepare-assurance/SKILL.md`
- `tests/fixtures/agentic_execution/host_activation/expected_surfaces.json`
- `tests/fixtures/agentic_execution/phase4/skills/client-cases.json`
- `tests/fixtures/agentic_execution/phase4/skills/portable-vectors.json`
- `tests/test_agentic_execution.py`
- `tests/test_instruction_architecture.py`
- `tests/test_public_onboarding.py`
- `tests/test_release_build.py`
- `tests/test_standard_repository_lifecycle.py`

The exact released evaluator separately changed
`docs/engineering/agentic-execution/work-orders/WO-AEX-008.md` from `approved`
to `in_progress`. It is not counted as an implementer execution-scope change.
The declared Phase 3 vector and every orientation-core file are unchanged.

## Deviations and residual uncertainty

- Qualification ran on Windows. POSIX launcher and filesystem behavior remains
  for independent assurance on a supported POSIX host.
- The installed Claude Code host reported `2.1.245`. The installed Codex app
  launcher path was discoverable, but Windows denied a nested `codex --version`
  process from this worktree. No live provider-backed Codex or Claude model
  session was opened because network, credentials, and external host effects
  are outside this work order. Root/nested discovery and activation were
  therefore proved by deterministic host fixtures, installer tests, and prior
  verified host-activation surfaces; independent assurance should repeat the
  exact commit on actual fresh host sessions where permitted.
- The exact public 0.6.0 evaluator correctly lacks `delegated-workflow`. This is
  a required fail-closed boundary, not a regression. A successor exact evaluator
  must exist before a real Phase 4 writing client can advance lifecycle state.
- Exact 0.6.0 non-promotable candidate acceptance requires an exact candidate
  commit. No such commit is authorized at this checkpoint, so that gate remains
  intentionally pending for the candidate-commit stage.
- The first released-evaluator identity invocation omitted the required
  checkout-root argument and returned `RID005`; the corrected invocation passed
  and produced the retained identities above.
- The offline package backend emitted the pre-existing setuptools notice that
  the table form of `project.license` will be deprecated in 2027. Changing
  unrelated release metadata is outside this work order.
- Unit tests, fixture vectors, package hashes, and this document are
  implementer-generated. They cannot satisfy `VER-AEX-004`, replace
  commit-bound independent assurance, activate Phase 4, or authorize a pilot.

## Intentionally not performed

No transition to `implemented`, exact candidate commit, VREC creation,
independent assurance decision, branch rewrite, merge, push, pull request,
release, publication, deployment, successor installation, real consumer
installation, target pilot, credential access, network effect, external-system
action, provider configuration, child-agent execution, parallel writer, or root
managed-file change was performed by this implementation checkpoint.

## Handoff result

Outcome: The approved `WO-AEX-008` implementation and implementer evidence are
complete.

Done: Writing-skill contract-v3 integration, evaluator-client boundaries,
direct-write denial, receipt and stop behavior, canonical/adapter parity,
orientation preservation, package inventory, fresh-wheel installation,
lifecycle/rollback qualification, complete-suite verification, documentation,
and exact scope audit.

Not done: Work-order completion transition, exact candidate commit,
commit-bound independent assurance, VREC decision, successor release, or
activation.

Current lifecycle state: `in_progress`.

Decision required: The accountable engineering owner must decide whether this
evidence is sufficient to transition `WO-AEX-008` to `implemented`.

Next: Authorize the released evaluator to mark `WO-AEX-008` implemented.

Command or response: `Mark WO-AEX-008 implemented.`

Alternatives: Request a bounded correction while the work order remains
`in_progress`, or stop without lifecycle effect.
