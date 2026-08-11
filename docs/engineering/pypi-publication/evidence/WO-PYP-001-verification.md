# WO-PYP-001 implementation verification

Date: 2026-08-11
Work order: `WO-PYP-001`
Verification contract: `VER-PYP-001`
Platform: Windows, repository workspace clone of `8eb4aa4363baa72274196a1fe91a622a91d96b37`

## Scope and authority

The accountable repository owner authorized the workflow, artifact packet, tests, implementation evidence, and GitHub `pypi` environment with the instruction recorded in `WO-PYP-001`. No instruction authorized a workflow dispatch or PyPI upload. This evidence therefore verifies configured capability only and records no package-index publication.

The implementation does not edit the historical GitHub-only `RLS-SEH-001`, rebuild version `0.2.0`, move tag `v0.2.0`, create a commit, push a branch, open a pull request, transition a verification/release record, or upload a distribution.

## Implemented controls

- Manual `workflow_dispatch` only, requiring tag, wheel SHA-256, and sdist SHA-256.
- Final `vMAJOR.MINOR.PATCH` releases only; draft and prerelease metadata stop the job.
- Job and GitHub environment restricted to `main`.
- Serial production concurrency group with in-progress cancellation disabled.
- Exact universal-wheel and normalized-sdist names derived from the selected tag.
- Independent lowercase SHA-256 comparison plus byte-exact two-line `SHA256SUMS` comparison.
- Only the verified wheel and sdist copied into the publisher directory.
- Job-scoped `contents: read` and `id-token: write` permissions.
- No checkout, repository-code execution, package build, dependency installation, PyPI secret, password, `.pypirc`, or fallback credential.
- Official `pypa/gh-action-pypi-publish` pinned to full commit `a892a5a61159132606e93a2fa6f4358831b04d26`, the current `v1.14.2` tag observed through the GitHub API on 2026-08-11.
- Metadata verification, attestations, and hash reporting explicit; duplicate skipping absent.

## Artifact-graph validation

Before implementation, from the owner working tree:

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 108 | Errors: 0 | Warnings: 0
```

After adding the approved packet and after implementation:

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 122 | Errors: 0 | Warnings: 0
```

## Focused deterministic verification

```text
python -m unittest tests.test_pypi_publishing -v
Ran 6 tests in 0.002s
OK
```

The tests cover manual trigger and required inputs, main-only serial deployment, protected environment name, shell-safe input transport, tag and hash validation, final-release state inspection, exact filenames, independent digests, exact manifest equality, publisher-directory isolation, least privilege, no checkout/build/secret path, immutable action SHA, metadata verification, attestations, hash reporting, duplicate failure, and the retained `0.2.0` checksum vector.

Workflow YAML parsed successfully with PyYAML 6.0.3 using `BaseLoader`. The extracted Bash preflight script passed `C:\Program Files\Git\bin\bash.exe -n` syntax validation.

## Complete repository verification

Python 3.14.6:

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 60 tests in 24.505s
OK (skipped=2)
```

Python 3.11.9:

```text
C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 60 tests in 24.552s
OK (skipped=2)
```

Both skips are the existing expected Windows symlink-privilege cases. No PyPI-specific test was skipped.

Additional gates:

```text
python -m se_harness --help
PASS: command help rendered with every existing command.

python -m se_harness doctor .
PASS: Python, configuration, lock, required files, Claude import, and every managed/seed entry.

python scripts/generate_harness_dashboard.py --root .
Harness Explorer generation: PASS
Artifacts: 122 | Relations: 429 | Errors: 0 | Warnings: 6
Snapshot: 06c6cef85a9ca0c52f787baa0de36a0fd33107803c02d1603ab722f688f1b16a

git diff --check
PASS
```

The six dashboard warnings predate this packet: five governance-only `WO-REV-002` through `WO-REV-006` items have no verified commit-bound VREC, and `VREC-AGR-001` remains a possible supersession review. The new PyPI packet adds no error or warning.

## GitHub environment evidence

The GitHub REST API created and read back environment `pypi`:

- Environment ID: `19679968294`.
- Required reviewer: `mmzen` (GitHub user ID `8011340`).
- Prevent self-review: `false`, explicitly authorized by the accountable repository owner after implementation.
- Custom deployment-branch policy: `true`.
- Allowed branch: `main` (policy ID `57065399`, type `branch`).
- Administrators may bypass: GitHub returned `can_admins_bypass: true`.
- Environment contains no PyPI secret.

The environment was initially created with self-review prevented. The accountable repository owner later explicitly authorized self-review with the instruction `i authorized self review and created the publisher`; the GitHub API was updated and read back with `prevent_self_review: false` while preserving the required reviewer and `main` allowlist. GitHub's documented environment REST update parameters do not expose `can_admins_bypass`; that external administrative bypass remains a residual control for owner review.

## PyPI publisher boundary

The user reported creating the PyPI account and `se-harness` project. The available browser session was not authenticated to PyPI, so automation did not request, receive, or handle credentials and did not change PyPI settings.

The accountable repository owner subsequently confirmed creating this exact Trusted Publisher configuration with the instruction `i authorized self review and created the publisher`:

```text
Owner: mmzen
Repository: se_harness
Workflow: publish-pypi.yml
Environment: pypi
```

PyPI publisher settings are authenticated administrative state and are not exposed through a public read API before publication. This evidence therefore retains the accountable owner's explicit confirmation rather than claiming an independent automated inspection. The workflow must first exist on GitHub `main`; registering or exercising another workflow identity is outside this evidence.

## Known `0.2.0` publication inputs

These values are retained for a later separately authorized publication record and workflow dispatch:

```text
Tag: v0.2.0
Wheel SHA-256: 56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d
Sdist SHA-256: 7c94cc0f4998b045b2766c60bc03a887bfdc53ae87f3494bb702e1d947bf873d
```

No dispatch occurred and these values do not grant publication authority.

## Deviations and residual risk

- The irreversible end-to-end PyPI upload is intentionally unexecuted under this work order. It requires a separate release-owner authorization and post-publication evidence.
- PyPI publisher configuration is owner-confirmed authenticated state but cannot be independently inspected through the public PyPI API before publication.
- Self-review is intentionally enabled for the required reviewer `mmzen`. This reduces separation of duties for a solo publication and is an explicitly accepted owner decision; exact hash inputs, `main` restriction, manual environment approval, and separate publication authorization remain required.
- GitHub reports that administrators can bypass environment protection. The main-only job condition still fails alternate-ref runs, but an administrator can change repository workflow/configuration and remains a privileged actor.
- GitHub, PyPI, hosted-runner tools, and upstream action availability are external dependencies.
- The publisher action pin must be reviewed and deliberately updated for security fixes; a mutable reference is prohibited.
- The current contract supports final universal-wheel releases only.

## Verification conclusion

`WO-PYP-001` is implemented and its locally testable controls pass on Python 3.11 and 3.14. The GitHub environment is configured with required `mmzen` review, explicitly authorized self-review, and a `main`-only deployment policy. The owner confirms the exact PyPI publisher exists. The workflow is not active until merged to `main`, and no production publication is authorized or attempted.
