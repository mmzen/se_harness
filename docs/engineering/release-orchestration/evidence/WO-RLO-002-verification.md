# WO-RLO-002 implementation evidence

## Scope and authority

The repository owner approved the RLO-002 work order on 2026-08-18 with `ok go implement`. This evidence covers only the bounded implementation of `REQ-RLO-009`, `REQ-RLO-010`, and `REQ-RLO-011`. It records derived implementation checks; it does not verify a commit, approve or transition a VREC or RLS, create or move a tag, publish a GitHub Release or package, deploy Pages, approve an environment, change external configuration, promote the governor, commit, push, or open a pull request.

Implementation began from `4f73d516c8d336ec65f3808a64cd280b2f702b8f` on branch `work/WO-RLO-002`. The worktree intentionally contains the authorized implementation, so it is not a clean commit-bound candidate. One wheel was built only under ignored `target/` for negative package inspection; it is non-promotable and carries no release authority.

## Implemented boundary

- Removed the unreleased `prepare-release --distribution-manifest` CLI/API path and deleted `se_harness.release_distribution` from the portable package.
- Removed Python wheel/sdist, `python-wheel-sdist`, checksum-layout, and SE Harness publication semantics from the core validator and portable release-record template.
- Preserved generic `harnessctl prepare-release` identity, coverage, lifecycle, path-safety, clean-worktree, and all-or-none output behavior.
- Added one non-packaged `repository_tools.release_distribution` implementation shared by deterministic bundle creation, atomic RLS binding, repository policy validation, trusted-main release resolution, and tests.
- Added `scripts/bind_release_distribution.py` for one ready RLS plus one exact repository-relative bundle manifest, and `scripts/validate_release_distributions.py` for explicit repository policy assessment.
- Added `scripts/check_portable_release_surface.py` so candidate-package evidence checks wheel content and installed CLI help without putting the forbidden repository policy literals inside the packaged self-hosting workflow.
- Rewired `.github/scripts/publish_release.py` to trusted repository tooling. The one-input workflow separately requires the selected distribution-bearing RLS before plan derivation.
- Added the repository policy validator to candidate-source CI and mirrored the reusable workflow in `self_hosting/`.
- Reconciled only the two expected managed lock digests for the portable release template and validator.

## Ownership and dependency result

| Surface | Resulting owner | Package/consumer presence |
| --- | --- | --- |
| Core RLS preparation and lifecycle validation | portable `se_harness` | present |
| SE Harness wheel/sdist manifest and schema 1 distribution table | `repository_tools/` | absent |
| Atomic bundle-to-RLS binding | repository script | absent |
| Repository distribution-policy validation | repository script and repository CI | absent |
| One-input GitHub/PyPI/Pages orchestration | repository workflow and trusted-main helper | absent |

Core validation intentionally treats a repository extension as opaque. The repository policy validator independently checks the complete field set, version-derived filenames, lowercase hashes, canonical checksum bytes, candidate epoch, and NUL-delimited Git tree identity. Publication requires that second assessment for the selected RLS.

## Binder and failure matrix

| Case | Result | RLS bytes after failure |
| --- | --- | --- |
| exact ready RLS plus exact manifest | complete distribution table added before relations | only the authorized insertion changes |
| exact replay | accepted as already exact | unchanged |
| wrong version, commit, epoch, tree identity, filename/path, or checksum bytes | rejected | unchanged |
| duplicate JSON key or incomplete field set | rejected | unchanged |
| partial or conflicting existing distribution state | rejected | unchanged |
| non-ready RLS | rejected | unchanged |
| absolute or escaping repository path | rejected | unchanged |
| injected `os.replace` failure | rejected and temporary file removed | unchanged |

The binder independently recomputes candidate commit time and source-tree identity before replacement. It preserves the original newline style and file mode, writes and flushes a same-directory temporary file, and uses atomic replacement. It never changes RLS status, core identity, relations, or accountable authority.

## Workflow security comparison

The normal publication interface remains exactly one required `release_record` input on `main`. Existing job permissions, protected environments, action identities, immutable-state rules, deterministic double build, public observation, and GitHub/PyPI/Pages separation are unchanged.

The new selected-RLS policy command runs in the trusted-main `resolve` job with `contents: read` before plan creation. The trusted resolver imports `repository_tools.release_distribution`, never candidate package code. Candidate wheel/CLI boundary checks run only in credential-free candidate-package evidence. No candidate code was added to GitHub-write, PyPI OIDC, or Pages-write jobs.

## Verification results

| Command/check | Result |
| --- | --- |
| start and review preflight for `WO-RLO-002` | PASS after accountable approval |
| formal graph validation | PASS: 477 artifacts; structure E0/W0, governance E0/W0, policy E0/W0; unchanged maintenance W44 |
| repository distribution policy over current history | PASS: zero distribution-bearing historical records |
| managed doctor and lock integrity | PASS |
| root/canonical validator and release-template copies | PASS: byte-identical |
| focused RLO/provenance/installer/self-hosting suites | PASS: 100 tests, two existing skips before final additions |
| complete suite on Python 3.14.6 | PASS: 252 tests, three existing skips |
| complete suite on Python 3.11.9 | PASS: 252 tests, three existing skips |
| strict PyYAML parse of both changed workflows | PASS |
| Python compilation of product, repository tools, scripts, workflow helpers, and tests | PASS |
| `git diff --check` | PASS; only host CRLF conversion notices |
| non-promotable wheel inspection | PASS: 57 members; no repository module, namespace, option, kind, or checksum-layout leak |
| wheel install plus disposable `init`, `adopt`, `upgrade --apply`, and `doctor` | PASS on Python 3.11.9; consumer template and validator contain none of the repository distribution terms |

The inspected local wheel was `se_harness-0.4.1-py3-none-any.whl`, SHA-256 `9f5cdba80ee18a96e5c1090fb8817d8dedcc36d088dad2e38f8e676fe0689134`. This hash identifies only a dirty-worktree verification build under `target/`; it must not be uploaded, promoted, or used as release evidence.

## Runtime identities and compatibility

Candidate source remains version `0.4.1`. The independent governor remains the released 0.3.0 wheel selected by `.self-hosting/governor.toml`, SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`; it was not promoted. Generic RLS creation remains format-neutral, and current historical RLS records without a distribution table remain valid. No current RLS required migration because none contains `[distribution]`.

## Documentation, warnings, and residual risk

Updated the repository context and contributor self-hosting/release note with the two-step generic-prepare plus repository-bind process, separate local policy command, and component ownership. Updated the release-orchestration domain index and retained the approved RLO-001 artifacts and evidence unchanged.

The local wheel build emitted the pre-existing setuptools warning that `project.license` as a TOML table is deprecated for a future setuptools version; this work did not alter package metadata. Existing 44 maintenance observations remain outside RLO-002. Host checkout CRLF notices remain non-semantic.

Residual uncertainty remains in hosted runner behavior and the first separately authorized real release using the new binder. Hosted PR checks, a clean candidate commit, released-governor/candidate-package evidence, accountable VREC approval, and a separately authorized RLS/publication transaction are still required. No production action was used to claim implementation success.
