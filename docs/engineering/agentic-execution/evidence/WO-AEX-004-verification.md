# WO-AEX-004 implementation evidence

This file records implementation-phase evidence for `WO-AEX-004`. It is not an
assurance decision, verification record, lifecycle transition, delivery choice,
release record, Git authorization, or external-action authorization. The work
order remains `in_progress`, and its repository owner requires later
commit-bound verification.

artifact: WO-AEX-004
checkpoint: handoff
formal_snapshot_sha256: 66675c6ef296261e620f683c9b0c082964326cb483b963662f01c1db7f45bbe0
candidate_base_commit: b77dbdc86fc00c0bc053e2b19c203fc0dc1dee62

## Candidate, evaluator, and host identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate base commit observation:
  `b77dbdc86fc00c0bc053e2b19c203fc0dc1dee62`. This file does not bind a
  later commit that contains itself; the required VREC must bind the exact
  clean candidate commit.
- Exact released evaluator: `se-harness 0.6.0`, invoked through
  `../se-harness-eval/Scripts/python.exe -I` outside the checkout.
- Released identity: passed with isolated Python, disabled user site, absent
  `PYTHONPATH`, exact checkout boundary, and no diagnostics.
- Released wheel: `se_harness-0.6.0-py3-none-any.whl`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Claude Code CLI: `2.1.241`. Its installed version and current official
  front-matter reference support project `.claude/skills`, free-form
  `metadata`, user invocation by default, and
  `disable-model-invocation: true`.
- Codex desktop package observed at `26.818.5229.0`; its bundled CLI reports
  `codex-cli 0.149.0-alpha.4.1`. The Windows application boundary denied direct
  execution in place, so the signed CLI and required sibling helpers were
  copied only into the disposable smoke-test directory and removed after the
  run. The installed Codex skill-authoring contract confirms `.agents/skills`,
  `agents/openai.yaml`, and the exact false implicit-invocation policy.

Candidate source, verifier-owned ephemeral package fixtures, both host
surfaces, and the exact released evaluator remain distinct identities. Three
authenticated, ephemeral Codex model sessions and one unauthenticated Claude
Code launch were attempted under the separately authorized bounded smoke test
described below. No repository effect, Git action, publication, or remote
mutation was performed.

## Implemented result

- Preserved every byte, retained vector, version, and manifest digest of the
  exact `harness-orient` v1 canonical core.
- Added only `agents/openai.yaml` to each writing core. The document contains
  exactly `policy.allow_implicit_invocation: false` and grants no dependency,
  tool, model, permission, hook, network, or external capability.
- Incremented only the three writing skill versions from `1.0.0` to `1.0.1`
  and rebound their canonical contract and portable-manifest vectors.
- Added one same-named `.claude/skills/<name>/SKILL.md` adapter for each of the
  four canonical cores. The adapters contain discovery, fixed canonical
  binding, loading, and fail-closed instructions only.
- Set `disable-model-invocation: true` only on the three Claude writing
  adapters. The orientation adapter omits that field and remains eligible for
  normal read-only matching.
- Added no copied canonical procedure, contract, helper, `allowed-tools`,
  model, context, agent, hook, shell command, dynamic substitution, remote
  reference, or argument transformation under `.claude`.
- Extended explicit source and wheel inventory for three Codex policy files
  and four Claude adapters. The existing recursive installer required no code
  change and lock-manages the complete surface atomically.
- Added verifier-owned mapping vectors and tests for exact names, paths,
  activation classes, malicious mapping changes, fresh installation, replay,
  `.agents`-only upgrade, customization, package inventory, and fresh
  non-promotable wheel installation.
- Updated bounded operator and contributor guidance. Skills continue to
  complement `harnessctl`; discovery changes no harness authority.

No installer module, portable manifest algorithm, root instruction, managed
workflow, lifecycle rule, decision right, quality gate, authority source,
dependency, public version, global skill location, plugin, profile, envelope,
subagent, Git operation, credential interface, network behavior, or external
integration was added or changed.

## Portable and host identities

| Skill | Version | Contract SHA-256 | Portable-core SHA-256 | Codex policy | Claude model invocation |
| --- | --- | --- | --- | --- | --- |
| `harness-orient` | `1.0.0` | `2c73e513c4b0b9189e32e6cfd485fe3148acb07014882f760cf2b2f2c67c72a3` | `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea` | absent | eligible |
| `harness-draft-change` | `1.0.1` | `6a14303b9349a55b34b11ab106451e541235e143c342a1a5e2a8261b3afd37d6` | `9622fdd52ba7bd8c74ed5eba973629c6070a760f1ea1363ba3099d6736d82525` | implicit disabled | disabled |
| `harness-execute-work-order` | `1.0.1` | `766ecfe61c995a5581c30635eb6f21bb111caf972687f00c6908cdbeb5915949` | `112b3dfdc36b319d33f75a0f495346f6c3e3a932ffdf2228a70eba0f2ff49ea0` | implicit disabled | disabled |
| `harness-prepare-assurance` | `1.0.1` | `53038af2c77dfbd31db59a67cae23953e5f0246acd950f4e195e94939f207609` | `9f732ebebf63765fc43e44504704c687c152c422d1c4631d59847efa676aaadc` | implicit disabled | disabled |

The standard template contains 15 canonical-core files and four thin Claude
adapter files. There is one authoritative `SKILL.md` body and one helper set per
skill under `.agents`; `.claude` contains only four adapter files.

## Verification observations

| Check | Result |
| --- | --- |
| Codex skill-authoring validation | Passed for all three modified writing cores; the exact explicit-only policy shape is accepted |
| Claude Code front-matter compatibility | Passed by static comparison with the current `2.1.241` CLI and official field contract |
| Focused host, AEX, instruction, public, lifecycle, and package suite | Passed: 96 tests in 46.799 s; 2 platform skips |
| Canonical and adapter inventories | Passed: four same-named cores, three Codex policy files, four adapter-only Claude directories, no import-package duplicate |
| Fresh install and managed lock | Passed: all 19 files are installed in `managed` mode |
| No-op replay | Passed: every installed host-surface file reports `unchanged` |
| `.agents`-only upgrade | Passed: seven host additions are atomic and the complete orientation core is unchanged |
| Customized host files | Passed: canonical, policy, and adapter changes report `customized` and preserve bytes |
| Non-promotable ephemeral wheel and fresh install | Passed: source, wheel fixture, and installed normalized content contain the exact inventory once |
| Exact released evaluator identity | Passed with the wheel and payload identities above |
| Exact released evaluator doctor | Passed all installed integrity checks |
| Exact released evaluator validation | Passed: 798 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Exact released handoff checkpoint | Passed all 8 implementation-evidence predicates; all 27 declared implementation paths are within the 24 exact/prefix scope entries |
| Full shared-checkout suite | Observed: 709 tests in 404.343 s; 6 failures, 21 errors, 13 skips, limited to pre-existing Windows LF and sandbox Git-ownership assumptions |
| Real PEP 517 candidate build | Not assessable: the environment has no `build` module and dependency installation was not authorized |
| Codex model-backed root explicit invocation | Passed for all four names with `codex-cli 0.149.0-alpha.4.1`: every explicit invocation resolved its same-named canonical core, the three writing policies reported implicit activation disabled, stop conditions were honored, and no effect occurred |
| Codex natural-language writing activation | Passed: no project skill loaded implicitly, no effect-capable writing skill auto-loaded, and no effect occurred |
| Codex nested non-Git discovery and orientation | Failed in the authorized non-Git fixture: the session resolved the intended repository root from the prompt but reported no available ancestor project skills and did not load `harness-orient`; exact Git-root behavior was not tested because Git mutation was prohibited |
| Claude Code model-backed root/nested sessions | Not assessable: CLI `2.1.241` reported `loggedIn: false`, no API key or OAuth token was present, and the launch made no API call; login was not attempted because it would change user authentication state |
| Host-smoke repository state boundary | Passed: the 84-entry before/after manifest remained `23599d0073c2ebe92d852f1a405bbd18fcd1ee29fa1b2960599b56556c745dd1`, no `.git` directory appeared, and no helper effect occurred |
| Host-smoke user-state boundary | Did not fully pass: `.codex/auth.json` and general `.claude.json` state/cache data changed during the observation window; `.codex/config.toml`, `.claude/settings.json`, and `.claude/settings.local.json` remained byte-identical, process attribution was not independently proven, and testing stopped after detection |
| Codex nested Git-root rerun | Passed: explicit invocation from `components/demo` discovered all four repository-root canonical cores, reported orientation implicit eligibility and all three writing skills explicit-only, and performed no effect |
| Claude Code Bedrock operator rerun | Passed for reported root discovery, all four explicit invocations, writing non-activation, and matched orientation with CLI `2.1.241`, Amazon Bedrock `eu-west-1`, and `global.anthropic.claude-opus-5`; the operator did not separately transcribe the nested `/` menu inventory |
| Git-root rerun state boundary | Passed: the 111-entry manifest remained `dfa809c9da3023f7c13d54ceca5e91d8e4f48ab3b03492887c6e5675ec503299`; the disposable repository remained on unborn `main` with no index, commit, or remote |
| Git-root rerun settings boundary | Passed: Claude settings, Codex settings, Git configuration, and the observed AWS configuration paths remained byte-identical or absent as initially observed |

The complete-suite failures are in `test_hash_bound_integrity` and the
unmodified build-recipe cases of `test_release_build`. Git subprocesses reject
the sandbox checkout as dubious ownership, and raw canonical JSON tests observe
the checkout's CRLF materialization. None exercises or reports a defect in a
changed canonical skill, adapter, installer, package inventory, or onboarding
path. The focused suite includes every changed test module and the
non-promotable wheel fixture and passes.

## Authorized model-backed host-smoke addendum

On 2026-08-24, the repository owner authorized bounded model-backed Codex and
Claude Code smoke tests with authenticated network access in a disposable local
repository, while prohibiting Git mutation, publication, push, and global or
user configuration changes.

The candidate source initialized a fresh standard installation containing all
four canonical `.agents` cores and all four same-named `.claude` adapters. The
fixture had no `.git` directory, validated with 0 artifacts, 0 errors, and 0
warnings, and had a fixed 84-entry file-and-directory manifest before the host
runs. All prompts prohibited file writes, Git, helper execution, network tools,
and external action. Codex used `--ephemeral`, `--ignore-user-config`, and the
`read-only` sandbox. Claude Code used `--no-session-persistence`, `plan`
permission mode, project-only settings, an empty MCP configuration, and a
`Read,Glob,Grep` tool allowlist.

Codex explicitly loaded `harness-orient`, `harness-draft-change`,
`harness-execute-work-order`, and `harness-prepare-assurance` from the fixture
root. It reported all four in the project inventory, resolved each same-named
canonical `.agents/skills/<name>/SKILL.md`, preserved orientation eligibility,
reported implicit invocation disabled for every writing skill, and stopped
before effects because required evaluator, actor, work-order, and authorization
inputs were absent. A separate natural-language drafting request loaded no
project skill and performed no effect.

The nested Codex session exposed an important boundary of this fixture: without
Git metadata, Codex treated the nested directory as its discovery root. Its
read attempts were denied by execution policy, it reported an empty project
skill inventory, and `harness-orient` did not load. Creating Git metadata only
to make that case pass would have violated the explicit no-Git-mutation limit,
so the result is retained as a failed non-Git nested scenario rather than
rewritten as a pass.

Claude Code could not reach a model. The CLI reported no active login and no
available API-key or OAuth-token environment variable. No login, token setup,
or configuration change was attempted. The failed launch reported zero API
duration and zero tokens.

The disposable repository manifest was byte-identical after all attempts and
remained non-Git. A separate user-state comparison found that the Codex
authentication store and Claude general CLI state/cache store changed during
the observation window. Those changes are consistent with host-managed refresh
or startup metadata, but process attribution was not independently proven. The
actual Codex and Claude settings files remained byte-identical. No credential
value was inspected or recorded. Further host calls stopped immediately after
this deviation was detected.

## Authorized Git-root and Bedrock rerun addendum

On 2026-08-24, the repository owner separately authorized `git init` only in a
new disposable test repository, expected Claude and Codex authentication or
session-cache updates, and authenticated model access. Commits, remotes,
settings edits, real-repository mutation, push, and publication remained
prohibited.

The candidate initialized another complete standard installation, then Git
created only an empty local repository on unborn branch `main`. No index,
commit, or remote was created. The installed candidate contained the same four
canonical `.agents` cores and four Claude adapters. Formal validation passed
with 0 artifacts, 0 errors, and 0 warnings. Candidate `doctor` reported the
expected hash-bound tracked-path failures because the authorization prohibited
`git add`; no attempt was made to manufacture an index merely to clear that
fixture condition.

The Codex nested natural-language session resolved the Git root and exposed
only `harness-orient` in implicit model context; no writing skill loaded. A
separate nested explicit invocation named all four skills and proved that each
resolved from `components/demo` to its same-named repository-root canonical
core. Orientation remained implicitly eligible, all three writing skills
reported exact explicit-only activation, and no effect occurred.

The operator exercised Claude Code `2.1.241` through Amazon Bedrock in
`eu-west-1` with model `global.anthropic.claude-opus-5`. The root `/` inventory
showed all four skills. Explicit `/harness-orient` loaded canonical contract
version `1.0.0` and stopped at unavailable evaluator identity. Explicit
`/harness-draft-change`, `/harness-execute-work-order`, and
`/harness-prepare-assurance` each loaded the same-named canonical core and
contract version `1.0.1`, then stopped at the explicit-activation and missing-
input gates before helpers or effects. The natural-language drafting request
loaded no project skill. This demonstrates that an explicit-only writing skill
can remain available in the `/` menu while absent from implicit model context.

The operator-provided orientation-match result showed Claude loading
`harness-orient`, resolving `.agents/skills/harness-orient/`, and stopping
before helper execution because evaluator inputs were intentionally absent.
The output named all three writing skills as explicit-only. The operator did
not separately transcribe the nested `/` menu inventory, so that single UI
observation remains distinct from the successful nested match and canonical-
binding observation.

Claude reported read, directory-list, and shell activity used to resolve the
canonical path, but reported no helper or write. Independent before/after
measurement confirmed that all 111 repository and Git entries were byte-
identical. Git still had no index, commit, or remote. Hashes for Claude
settings, Codex settings, Git configuration, and observed AWS configuration
paths were also unchanged. Authentication/session-cache writes were permitted
and were not treated as settings changes; no credential value was inspected or
recorded.

## Changed implementation paths

- `MANIFEST.in`
- `README.md`
- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-004-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-host-adapters.md`
- `docs/notes/agentic-execution-roadmap.md`
- `docs/notes/agentic-execution-skills-mvp.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `pyproject.toml`
- `templates/repository/standard/.agents/skills/harness-draft-change/agents/openai.yaml`
- `templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/agents/openai.yaml`
- `templates/repository/standard/.agents/skills/harness-execute-work-order/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/agents/openai.yaml`
- `templates/repository/standard/.agents/skills/harness-prepare-assurance/skill-contract.json`
- `templates/repository/standard/.claude/skills/harness-draft-change/SKILL.md`
- `templates/repository/standard/.claude/skills/harness-execute-work-order/SKILL.md`
- `templates/repository/standard/.claude/skills/harness-orient/SKILL.md`
- `templates/repository/standard/.claude/skills/harness-prepare-assurance/SKILL.md`
- `tests/fixtures/agentic_execution/host_activation/expected_surfaces.json`
- `tests/fixtures/agentic_execution/phase3/portable_vectors.json`
- `tests/test_agentic_execution.py`
- `tests/test_instruction_architecture.py`
- `tests/test_public_onboarding.py`
- `tests/test_release_build.py`
- `tests/test_standard_repository_lifecycle.py`

Every implementation path is admitted by `WO-AEX-004`. The separately
authorized Phase 3 host-activation formal packet, planning note, approval
events, and work-start event are governance changes and are not counted as
implementation paths.

## Deviations and residual uncertainty

1. Claude's root `/` inventory, all four explicit invocations, writing non-
   activation, and orientation matching were observed. The operator did not
   separately transcribe the nested `/` menu inventory, although the nested
   orientation match and same-root canonical binding were observed.
2. The first non-Git Codex fixture did not provide nested ancestor discovery;
   the separately authorized Git-root rerun closed that representative case for
   all four explicitly named skills.
3. Authentication or general CLI state files changed during the first launch
   window, with process attribution unavailable. The authorized rerun proved
   the actual settings files and complete disposable repository stayed byte-
   identical.
4. A real candidate source distribution and wheel were not built. Explicit
   packaging metadata and the fresh-installed non-promotable wheel fixture pass,
   but a later commit-bound assessment should inspect real candidate archives.
5. The full shared-checkout suite is not globally green because of the two
   pre-existing environment conditions described above. No out-of-scope Git
   configuration or canonical-file rewrite was performed to mask them.
6. Repository-local instructions cannot prove that a hostile or future host
   obeys loaded text. Support is bounded to exact tested host versions and the
   later actual-host observations.
7. This evidence is implementer-generated and cannot satisfy the required
   independent, commit-bound assurance decision by itself.

## Intentionally not performed

No work-completion transition, VREC preparation, assurance decision, delivery
selection, commit, remote creation, push, pull request, merge, package
publication, global installation, consumer upgrade, settings edit, deployment,
or external action beyond the authorized model calls and disposable `git init`
was performed. The authentication and CLI-state observations described above
do not authorize any later credential or configuration change.
