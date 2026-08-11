# WO-PYP-002 publication preflight evidence

Date: 2026-08-11
Work order: `WO-PYP-002`
Base commit: `8eb4aa4363baa72274196a1fe91a622a91d96b37`

## Authority and boundary

The accountable repository owner authorized the exact sequence `commit, capture, commit and push + PR`. The authorization includes two normal commits, one ready commit-bound verification capture, one new-branch push, and one pull request targeting `main`. It excludes verification transition, merge, release transition, workflow dispatch, environment approval, PyPI upload, tag movement, release-asset replacement, force push, and history rewriting.

## Base and branch preflight

The working branch is `feature/pypi-trusted-publishing`. A fresh `git fetch origin --prune` on 2026-08-11 confirmed local `HEAD` and `origin/main` both resolved to `8eb4aa4363baa72274196a1fe91a622a91d96b37` before the candidate commit.

The configured origin is `https://github.com/mmzen/se_harness.git`. The intended remote branch does not replace `main`; the PR base is `main`.

## Candidate scope

The candidate contains only:

- the governed `pypi-publication` artifact packet and implementation evidence;
- `.github/workflows/publish-pypi.yml`;
- deterministic workflow invariant tests;
- the engineering-artifact overview update;
- this separately authorized commit/capture/push/PR work order and preflight evidence.

The GitHub `pypi` environment is external state already read back as required reviewer `mmzen`, explicitly authorized self-review, custom branch policy `main`, and no PyPI secret. The accountable owner confirms the exact PyPI Trusted Publisher exists. Neither external configuration grants package-publication authority.

## Verification inherited from the candidate

`WO-PYP-001-verification.md` retains the exact commands and results for:

- 122 formal artifacts, zero validation errors, and zero warnings;
- six focused PyPI workflow tests;
- 60 complete tests on Python 3.14.6 and Python 3.11.9 with two expected Windows symlink skips on each runtime;
- CLI help and source doctor;
- parsed workflow YAML and Bash syntax;
- main-only environment and workflow controls;
- Harness Explorer generation with no errors and six pre-existing governance review warnings;
- clean diff hygiene.

These checks must be rerun immediately before the candidate commit. Capture must then run from a clean tree and bind only `WO-PYP-001`, `VER-PYP-001`, and `docs/engineering/pypi-publication/evidence/WO-PYP-001-verification.md`.

## Immediate pre-commit verification

The complete gate was rerun after adding this authorization and evidence:

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 123 | Errors: 0 | Warnings: 0

python -m unittest discover -s tests -p "test_*.py"
Ran 60 tests in 24.888s
OK (skipped=2)

C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 60 tests in 26.531s
OK (skipped=2)

python -m se_harness --help
PASS

python -m se_harness doctor .
PASS

Workflow YAML parse
PASS

Extracted workflow Bash syntax
PASS

git diff --check
PASS
```

Harness Explorer generation passed with 123 artifacts, 434 relations, zero errors, the same six pre-existing governance review warnings, and snapshot `37347135542a19306039045bd471699916941bcef7055696f0b6c9fc121508f3`.

## Derived results

The first commit SHA, `VREC-PYP-001` snapshot and candidate fields, second governance commit SHA, remote branch, pull request URL, and CI results are necessarily derived after this evidence is committed. They remain inspectable through Git, the ready verification record, and GitHub and must not be guessed here.

## Residual risk

GitHub and its hosted checks are external dependencies. Administrators can bypass the environment protection rule and remain privileged actors. `VREC-PYP-001` will initially be `ready`, not verified. The workflow cannot run until merged to `main`, and no PyPI publication is authorized by this work order.
