# WO-SHB-001 Implementation Evidence

Date: 2026-08-12
Lifecycle: implementation evidence; not a VREC or release decision

## Scope and authority

The accountable owner approved `WO-SHB-001` with `go for implementation`. After PR #28 failed CI, the owner selected the recommended clean 0.2.2 recovery option. This evidence covers implementation and qualification of that recovery; it does not by itself verify a VREC, approve a release record, tag, publish, deploy, merge, or promote a governor.

The selected released governor is 0.2.1 from GitHub release `v0.2.1`, wheel `se_harness-0.2.1-py3-none-any.whl`, SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`, release record `RLS-SEH-002`, and candidate commit `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.

## Implemented boundary

- Added `.self-hosting/governor.toml` as the repository-specific exact governor descriptor.
- Added `harnessctl identity` with fail-closed role, version, origin, environment, checkout, commit/digest, Python isolation, user-site, `PYTHONPATH`, and explicit entry-point checks.
- Split the self-hosting workflow into required `governor -> candidate-source -> candidate-package` gates.
- Limited governor semantics to exact bootstrap identity, same-version disposable-target integrity, and stable candidate facts. The 0.2.1 governor does not claim to understand 0.2.2+ typed architecture semantics.
- Moved candidate `doctor`, full graph validation, tests, Explorer, fresh installation, and N-1 upgrade acceptance into candidate-owned disposable targets.
- Narrowed the root distribution-parity exception to two hash-locked repository-specific controls in the actual `se-harness` implementation repository: `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`. Every other managed checkout file retains candidate parity, the governor has its own external same-version target, and ordinary consumer repositories retain the standard invariant.
- Documented the post-publication governor-promotion procedure. Publication alone never changes the governor.
- Preserved the failed `VREC-SEH-003` and `RLS-SEH-003` attempt through closed PR #28 and its branch, excluded both files from the clean recovery tree, and reserved fresh aggregate IDs for the changed payload.

## Tests and graph

Focused identity, descriptor, workflow, parity-boundary, and failed-attempt exclusion tests passed. The complete local suite passed with 123 tests and three pre-existing conditional skips. Formal validation passed with 241 artifacts, zero errors, and 36 pre-existing legacy/location warnings. Review preflight passed for `WO-SHB-001`. `doctor` passed and reported governor 0.2.1. Explorer generated 241 artifacts and 799 relations with zero errors, 37 warnings, and observed snapshot `2f330fc5882e8ad251c3d0de1b24424f914ef6a84bdce22cdf4274d5674f27c0`.

Workflow YAML was parsed after rendering the consumer placeholders. The repository-specific workflow exposed exactly `governor`, `candidate-source`, and `candidate-package` jobs.

The first hosted recovery run exposed a Linux virtual-environment portability defect: resolving `bin/python` follows its normal symlink to the base interpreter outside the environment. The corrected identity model verifies the lexical launcher path and exact `sys.prefix`, while continuing to resolve and constrain module, distribution, template, entry-point, checkout, and import-search origins. A focused cross-platform regression test covers that distinction; a fresh hosted run remains required.

## Released governor execution

The retained 0.2.1 wheel was hash-checked before installation into a fresh temporary environment. Python ran in isolated mode outside the checkout and resolved:

- version: `0.2.1`;
- module: `...\governor-env\Lib\site-packages\se_harness\__init__.py`;
- templates: `...\governor-env\share\se-harness\templates\repository\standard`;
- wheel SHA-256: `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`.

Governor `init` and `doctor` passed against a governor-created temporary repository. Running its old graph validator against the current checkout reproduced the expected compatibility boundary: it rejected the newer typed architecture schema. The workflow therefore records stable bootstrap facts only and delegates current semantic validation to candidate source. This is an explicit limitation, not a hidden or relabeled pass.

## Candidate-package execution

An explicitly non-promotable wheel was built from the working tree in a disposable export, installed without dependencies in a fresh environment, and exercised only outside the checkout. This local worktree wheel is not a release artifact and its hash is evidence only:

- wheel: `se_harness-0.2.2-py3-none-any.whl`;
- SHA-256: `690287c9e9ad7ccdd3874b3c2ea4056ca997d15f3719c0f698d07608991d68df`;
- installed version: `0.2.2`;
- identity role: `candidate-package`;
- isolated Python: true;
- user site enabled: false;
- inherited `PYTHONPATH`: false;
- module, distribution, templates, executable, and explicit entry point: all below the candidate environment and outside the checkout.

Fresh `init`, `doctor`, `validate`, and `dashboard` passed. A separately created 0.2.1 target upgraded transactionally under the candidate wheel and passed candidate `doctor`. The candidate and governor acceptance roots were under the operating-system temporary directory; no acceptance output entered the checkout.

The identity used a synthetic 40-hex value only as a syntactically valid path-isolation input because the approved recovery tree was not yet committed. A later exact candidate commit, hosted three-plane CI, and commit-bound `VREC-SEH-004` are mandatory before any release action.

## Adversarial coverage

Automated tests reject:

- an installed role that resolves equal-version modules or templates from checkout source;
- candidate source with distribution metadata outside the checkout;
- installed execution with inherited `PYTHONPATH` or enabled user site;
- an entry point from a different environment;
- path-prefix deception such as `candidate-shadow` adjacent to `candidate`;
- malformed governor descriptors;
- activation of the self-hosting exception in a repository that is not the `se-harness` implementation source;
- a workflow that merges or skips the three required roles;
- reintroduction or reuse of the failed 0.2.2 verification and release records in the recovery tree.

## Failed-attempt audit and recovery

- Closed PR #28 and its unmerged branch retain the failed `VREC-SEH-003` and `RLS-SEH-003` attempt and its CI outcome.
- Both files are absent from the clean recovery tree.
- GitHub issue #29 retains the longer-term proposal to separate release approval from release materialization.
- The replacement candidate reserves `VREC-SEH-004` and `RLS-SEH-004`; neither failed identifier can authorize or describe it.

## Residual risks and deferred evidence

- GitHub Actions cannot be observed until the authorized recovery commit, push, and pull request exist. Local tests parse and inspect the workflow, but hosted execution remains pending.
- The exact final candidate artifact hash and commit identity cannot exist until the implementation is committed. The local wheel hash above must not be promoted.
- Full reproducible wheel/sdist release qualification is deferred to an approved release work order and replacement release contract/version decision.
- A published 0.2.2+ artifact is not automatically a governor; promotion requires the separate procedure in `SELF_HOSTING.md`.
