# WO-TCM-001 and WO-TCM-002 combined implementation evidence

artifact: WO-TCM-001
artifact: WO-TCM-002
checkpoint: handoff
formal_snapshot_sha256: f7237913fdaf27dc50d67ff923d174abdd672ca691e527dbd19acd2892709cf1

Date: 2026-08-25

This file records implementation-phase evidence for `WO-TCM-001` and the
accepted combined-evidence arrangement for companion `WO-TCM-002`. It is not a
verification record, assurance decision, completion decision, release record,
or authorization for Git, network, delivery, or other external action. Both
work orders remain `in_progress` until the engineering owner makes a separate
decision for each work order.

## Candidate and evaluator identity

- Source branch: `proposal/technical-communication-packet-7d1c52`.
- Source base commit: `45dea98574eefd9118fa930dc3631f149d0219e5`.
- The source candidate is uncommitted and is not commit-bound assurance
  evidence.
- Exact external released evaluator: `se-harness 0.6.0`.
- Runtime used for implementation tests: CPython `3.14.6` on Windows.
- Released-evaluator `doctor .` passed managed integrity. It reported only the
  existing `W013` placement advisories.
- Released-evaluator validation passed with 818 artifacts, zero errors, and 50
  pre-existing maintenance warnings.
- Released review preflight passed for both `WO-TCM-001` and `WO-TCM-002` while
  each was `in_progress`.

## Implemented result

### REQ-TCM-001: managed policy

- Added one canonical managed policy at
  `templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`.
- Added one direct route to the candidate managed router. The self-hosting root
  router remains the released 0.6.0 copy.
- Added the installed policy path to required and policy preflight inputs.
- Added explicit wheel data declarations while preserving recursive sdist
  inclusion.
- The policy permits only the claim that its principles are based on
  ASD-STE100. It explicitly rejects compliance, certification, approval, and
  endorsement claims.
- The policy and skill prohibit downloading, searching for, bundling,
  reproducing, parsing, or strictly implementing the external standard.

### REQ-TCM-002: protected content

- Exact protected spans are bound by UTF-8 byte offsets and SHA-256 values.
- The helper rejects malformed, duplicate, overlapping, unordered,
  out-of-range, excessive, or digest-mismatched spans.
- Output bindings must contain the same exact bytes and digest as the source
  span.
- A canonical restitution block must be returned alone and byte-identically.
- The helper accepts at most 262,144 source bytes and 256 protected spans.
- Validation is deterministic, standard-library-only, and reports stable
  bounded `TCM` diagnostics.

### REQ-TCM-003: communication profiles

- `operator-communication` leads with the outcome or one action, names the
  accountable actor, states non-effects, and preserves one canonical next
  action.
- `technical-artifact-writing` applies only to eligible draft narrative. It
  does not authorize automatic rewriting of metadata, normative statements,
  semantic tables, exact results, evidence, approved artifacts, or historical
  artifacts.
- Protected semantics include actor, condition, force, scope, qualification,
  threshold, and result.

### REQ-TCM-004: explicit read-only skill

- Added exactly three portable-core files for `harness-operator-brief` version
  `1.0.0`: `SKILL.md`, `skill-contract.json`, and
  `scripts/check_brief.py`.
- The strict v2 contract permits only explicit activation and the
  `inline-brief-render` effect.
- Delegation is disabled with a complete single-agent fallback.
- Lifecycle transitions, changed paths, target retention, Git, credentials,
  network, release, deployment, and external action are prohibited.
- A current-state brief requires a current structured evaluator result. The
  skill otherwise stops and routes to `harness-orient` instead of inferring
  state.

### WO-TCM-002: router contract tests

- `tests/test_artifact_catalog.py` now proves that the root released router has
  no technical-communication row and that the candidate is exactly the root
  router plus the one approved direct route. This exact whole-router comparison
  preserves every prior owner and rejects any other candidate change.
- `tests/test_context_routing_retirement.py` now compares the complete ordered
  `(subject, owner)` routing table, including
  `Eligible operator and technical-artifact English prose` owned by
  `docs/engineering/TECHNICAL_COMMUNICATION.md`.
- The routing test also requires unique subjects, so one subject cannot acquire
  two owners.

## Portable identities

- `harness-operator-brief` canonical portable-core SHA-256:
  `53d32d3bed34242a12ea8a77d33a26c312baec285da09d33f994b9220310718b`.
- Policy current-byte SHA-256:
  `aa9abf0915271c4916a17237d885013415805d9b11d5fcb89eb26c458c2a4dcd`.
- Skill instruction current-byte SHA-256:
  `15d4672d882aaf6dc155dce2aa79b41fe3d3c3a3ab3374567a17fa716e1a0eb8`.
- Skill contract current-byte SHA-256:
  `c2922ec37f6cb2898e7afe62456cf37d40da385ded40fc1b5c00a749c96a86b7`.
- Helper current-byte SHA-256:
  `7b06a52eb94da78d23d6a753c6230682db5ec11cb58e8a63d7d21b3e420775f0`.
- Review corpus current-byte SHA-256:
  `8b7b98f25c1af95b6b64a1b2c2ba4723b64846c1ec318a6a96cb6b389256f3fa`.

The four existing skill directories have no Git diff. Their canonical
portable-core digests remain:

| Skill | SHA-256 |
| --- | --- |
| `harness-orient` | `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea` |
| `harness-draft-change` | `e04c232791b817a4138d5659a37dff11136a3a2937d90e26ba9c8fbca18ead78` |
| `harness-execute-work-order` | `a34c7fa136c8a533c6e7abb1729ca36ad599521b012df18d5c624b413d03a8e2` |
| `harness-prepare-assurance` | `7075e1a42f264d7289e5a82bda04ec0e93bf9103389af22a07b235e87b7c4f24` |

## Commands and results

| Check | Result |
| --- | --- |
| released `se-harness` distribution identity | Passed: `0.6.0` |
| released `doctor .` | Passed managed integrity; existing placement warnings only |
| released `validate .` | Passed: 818 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| released review preflight for `WO-TCM-001` | Passed; status `in_progress`; commit-bound verification required |
| released review preflight for `WO-TCM-002` | Passed; status `in_progress`; commit-bound verification required |
| skill-creator `quick_validate.py` | Passed: `Skill is valid!` |
| `python -B -m unittest tests.test_artifact_catalog tests.test_context_routing_retirement` in the source worktree | Passed: 16 tests, 0 skips |
| five focused modules in a canonical-byte candidate | Passed: 112 tests, 2 Windows platform-capability skips |
| complete suite in an independent history-aware canonical Git candidate | Passed: 810 tests in 299.555 s, 22 platform/environment skips |
| `python -B scripts/validate_release_distributions.py --root .` | Passed: 1 distribution-bearing record; no distribution was built |
| candidate `python -B -m se_harness --help` | Passed; command surface rendered |
| canonical policy, contract, helper, installation, upgrade, offline, package, and effect-sentinel tests | Passed in the focused and complete suites |
| existing skill byte/digest comparison | Passed: four existing directories have no Git diff and retain their recorded manifests |
| static ASD claim and retrieval scan | Passed: matches are the permitted based-on statement, explicit negations, prohibitions, and general product text; no positive compliance claim or retrieval implementation was found |
| `git diff --check` | Passed; Windows line-materialization warnings only |
| root `ENGINEERING_HARNESS.md` and `.engineering-harness.lock` diff | Empty |

The final complete-suite run used an independent local clone with its own refs,
index, and worktree. It had read-only access to the source object store so the
retained predecessor commit used by the repository tests remained available.
The canonical candidate was committed only inside that disposable clone as
`1d5d800766a483f2a9e2e8aaf77e63b8486b816c`. Its `HEAD` was unchanged after
the run, and the clone was deleted. This hash is a disposable test-fixture
identity, not a delivery candidate or source-repository commit.

The 22 complete-suite skips are existing platform or optional-environment
conditions. The two router tests, protected-content tests, contract tests,
policy tests, installation tests, upgrade tests, package inventory tests, and
effect-sentinel tests were not skipped.

## Review corpus and human assessment status

The versioned corpus contains 11 bounded English cases at the declared 5/10
technical level: four operator cases and seven technical-artifact, safety, or
project-terminology cases. Every case records the expected actor, action,
condition, normative force, qualification, result, and protected tokens.
Automated tests confirm the corpus structure and exact token presence.

Implementation review found no policy contradiction, copied standard content,
positive compliance claim, hidden authority, or automatic approved-artifact
rewrite. The policy also makes the limits of deterministic checking explicit.

The two independent reviewer judgments over actual rendered corpus outputs are
not yet recorded. This remains required input to assurance under `VER-TCM-001`.
It must be completed before a verification record can claim that the semantic
and operator-comprehension acceptance conditions passed. No readability score
or implementation-agent judgment substitutes for that review.

## Exact implementation paths

### WO-TCM-001

- `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`
- `templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`
- `templates/repository/standard/.agents/skills/harness-operator-brief/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-operator-brief/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-operator-brief/scripts/check_brief.py`
- `se_harness/skill_contract.py`
- `se_harness/preflight.py`
- `pyproject.toml`
- `tests/test_agentic_execution.py`
- `tests/test_instruction_architecture.py`
- `tests/test_standard_repository_lifecycle.py`
- `tests/test_release_build.py`
- `tests/test_public_onboarding.py`
- `tests/fixtures/technical_communication/review_corpus.json`
- `docs/notes/technical-communication.md`
- `docs/notes/README.md`
- `docs/engineering/technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md`

Every path is admitted by the `WO-TCM-001` execution scope.

### WO-TCM-002

- `tests/test_artifact_catalog.py`
- `tests/test_context_routing_retirement.py`

These are exactly the two paths admitted by `WO-TCM-002`. No production,
policy, skill, package, managed-root, lock, formal-definition, or third test
path was changed by the companion implementation.

The approved definition packet, domain index, work-order lifecycle events, and
`docs/engineering/README.md` update are governed preparation and lifecycle
changes that preceded implementation. They are not relabeled as implementation
paths.

## Recovered verification-infrastructure incident

The first attempt to provide a canonical candidate with Git context used a
temporary `.git` pointer to the source worktree. A repository test then created
an unintended local commit `0d09566f4baab9968ec8e4a8b21afd4287779eda`
with message `canonical evidence` in the source worktree.

The incident was detected before evidence retention. Nothing was pushed. The
branch was moved back to its exact prior commit
`45dea98574eefd9118fa930dc3631f149d0219e5` with a mixed reset that preserved
all working files. The index was rebuilt and the exact TCM paths were unstaged.
The temporary directory was deleted. Final checks show the prior branch head,
an empty staged diff, the expected TCM working-tree paths only, and no root
router or lock diff. The local reflog retains the recovery audit trail.

The invalid run is not used as final full-suite evidence. The complete suite was
rerun successfully in the independent clone described above. This incident is
not evidence of a product or skill mutation, but it is retained here because it
was a source-repository Git action during verification.

## Deviations and residual uncertainty

1. The two independent manual reviewer judgments remain open. Automated byte
   preservation cannot prove that every semantically protected boundary was
   selected or that every reader will understand the rendered prose.
2. Windows platform-capability skips remain active on hosts that provide the
   relevant symlink, case-collision, or optional tool capability. None hides a
   failed router or technical-communication assertion.
3. A later commit-bound verification record must bind the exact delivery
   candidate. The disposable verification commit does not satisfy this need.
4. Both work-order narrative `Lifecycle` sections still describe their original
   draft preparation, while authoritative front matter and lifecycle events say
   `in_progress`. The released evaluator uses the structured state and all gates
   pass. Revising that historical narrative is outside both implementation
   scopes and would require separate governed authority.
5. The recovered Git incident left a local reflog audit entry but no branch,
   index, working-tree, remote, or external effect beyond the intended TCM
   candidate files.

## Intentionally not performed

No standard content was downloaded, searched, bundled, reproduced, or parsed.
No promotable distribution was built. No delivery commit, push, pull request,
merge, verification record, assurance decision, release record, tag,
publication, deployment, credential use, network use, or external workflow was
performed. No lifecycle completion transition was applied. Both work orders
remain `in_progress` for separate engineering-owner decisions.
