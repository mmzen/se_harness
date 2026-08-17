# Verification evidence for WO-DST-016

## Authority and boundary

This local evidence records implementation checks performed under the repository owner's 2026-08-17 authorization for `WO-DST-016`. It supports an `implemented` work-order state only. It does not provide commit-bound assurance, approve a verification record, authorize a release, or mutate GitHub policy.

## Delivered consumer model

- The standard distribution renders one additive `.github/workflows/engineering-harness.yml` with one `validate` job and read-only repository permission.
- The job creates one runner-temporary virtual environment, installs exact `se-harness==$SE_HARNESS_VERSION` as a binary distribution, proves its module and template origins are inside that environment and outside the checkout, then uses the same `python -I -m se_harness` boundary for selection, preflight, doctor, validation, and Explorer generation.
- Consumer CI contains no governor/bootstrap job, candidate-source fallback, direct checkout-script execution, generic YAML merge, application-test implication, or external GitHub-policy mutation.
- `harnessctl select-work-order` rejects missing, duplicated, malformed, non-text, duplicate-key, and oversized event input. Its output is selection data, never authority.
- The implementation repository's `.github/workflows/engineering-harness.yml`, `.engineering-harness.toml`, and `.engineering-harness.lock` remained unchanged at Git object IDs `65f491b0929e4c3e2626e35bf74819383c4b7ce2`, `8ef1736825fd917456e6582e5440a23f4bc7ad63`, and `434e2cd0a9e9d5f6c1428f4d2af37dbec25e789b` respectively.

## Installation, conflict, and migration evidence

- Init/adopt fixtures added the dedicated workflow beside zero, one, or several unrelated workflows while preserving unrelated bytes.
- An unknown exact destination produced a conflict, an actionable separate-filename instruction, no lock, and no partial write.
- A lock-tracked prior workflow upgraded transactionally; a second plan reported all 34 managed files unchanged. A customized workflow blocked the complete apply while another missing managed file remained missing.
- A disposable repository initialized with the actually published PyPI `se-harness==0.4.0` then upgraded with the fresh candidate wheel. Its rendered workflow SHA-256 changed from `0B850207FB04C054F3C936BCBF2E2A18C1D9F79DE14232B25FA328A0159C5ED4` to `CE364ACD155AA67A6024DA5642B97F6AA7E61FCDCEAED9DC45A8D6869CE343A3`; the second plan was unchanged and candidate `doctor` passed.
- The former and candidate canonical workflow Git blob IDs were `c280c617e4a8f147b239a517ca74d363a973101f` and `016e2cdf40d21c390cf6772f5e3f1527b25f46a6` during verification.

## Package and test evidence

- A non-promotable `se_harness-0.4.0-py3-none-any.whl` was built into a disposable directory and installed without dependencies or an index into a fresh environment. Init, doctor, graph validation, and workflow topology checks passed.
- Isolated identity reported version `0.4.0`; both `se_harness.__file__` and `template_root()` resolved below the fresh environment, outside the source checkout.
- `python -B -m unittest discover -s tests -p "test_*.py"`: 232 tests passed in 75.301 seconds; 3 environment-dependent tests skipped.
- Final affected regression: 67 tests passed in 26.373 seconds; 1 environment-dependent test skipped.
- Formal validation passed for 443 artifacts with structure, governance, and policy at E0/W0. Its 42 maintenance warnings pre-date and are outside this work order.
- Root `harnessctl doctor`, start preflight for `WO-DST-016`, exact CLI help, and `git diff --check` passed. The rendered workflow was manually reviewed and structurally asserted by source/package tests; no YAML parser dependency was added.

## Documentation and residual risk

README and focused notes now explain automatic GitHub workflow discovery, additive installation, safe standard upgrades, exact-path conflict handling, external required-check configuration, package-owned commands, and the self-hosting-only three-plane exception.

PyPI availability and GitHub runner behavior remain external dependencies. Exact version pinning does not claim repository-pinned checksums or artifact attestation, which remain explicitly out of scope. Application tests and workflow ordering remain repository policy. The build also exposed the existing setuptools warning that the table-form project license becomes unsupported after 2027-02-18; it is unrelated to this packet.

Hosted GitHub CI, candidate commit creation, VREC preparation or transition, commit, push, pull request, branch protection/ruleset changes, release, package publication, and demonstrator deployment were not performed.
