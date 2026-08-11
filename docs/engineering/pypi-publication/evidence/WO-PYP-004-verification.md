# Verification Evidence for WO-PYP-004

Date: 2026-08-11

## Incident result

Protected workflow run `31514559160` failed before OIDC authentication or upload. The exact-asset download and verification step passed. The publisher action then invoked GHCR image tag `a892a5a61159132606e93a2fa6f4358831b04d26`, and Docker returned `manifest unknown`. PyPI version 0.2.1 remained absent.

No artifact changed and no credential fallback, duplicate skip, manual upload, action retry, or environment bypass occurred.

## Root-cause proof

Official `pypa/gh-action-pypi-publish` GitHub metadata reports:

- current release: `v1.14.2`, published 2026-07-29;
- `refs/tags/v1.14.2` object type: annotated `tag`;
- annotated-tag object SHA: `a892a5a61159132606e93a2fa6f4358831b04d26`;
- the tag object's target type: `commit`;
- peeled commit: `dc37677b2e1c63e2034f94d8a5b11f265b73ba33`;
- `release/v1` currently identifies the same commit.

The public GHCR registry returned HTTP `200 OK` for image manifest `ghcr.io/pypa/gh-action-pypi-publish:dc37677b2e1c63e2034f94d8a5b11f265b73ba33`, with digest `sha256:a68d05519f6d7e47372aeaddab80b851b69afa89be179ec41775c72c4e3ab2d5`.

The original test incorrectly treated the annotated-tag object as a commit because both are 40-character Git object IDs. GitHub could resolve the action source, but the action propagated that object ID as the Docker tag, which did not exist.

## Implemented correction

- The publisher action remains upstream release `v1.14.2` but now pins its peeled immutable commit `dc37677...ba33`.
- The static test requires that exact commit and rejects the known tag-object SHA.
- Mutable refs remain forbidden.
- Trigger, `main` restriction, protected `pypi` environment, job-scoped read/OIDC permissions, no checkout/build/credential path, exact release state/names/hashes/manifest, metadata verification, attestations, printed hashes, and strict duplicate failure remain unchanged.
- `ARCH-PYP-001` now directly constrains the five PyPI requirements, matching the preflight coverage model without changing runtime or publication behavior.

## Verification results

Focused PyPI tests passed `6/6`. Python `3.14.6` and Python `3.11.9` each passed all `70` repository tests with `2` expected conditional Windows symlink skips. Formal graph validation passed with `168` artifacts, `0` errors, and `0` warnings. Start preflight passed with the complete PyPI requirement chain. CLI and doctor passed every required and managed-integrity check. Explorer generated `168` artifacts and `599` relations with `0` errors, `1` unrelated historical stale-ready warning, and snapshot `d5c2f8d4295f51c2aba5f368c8a336961af3ee2273e1c0a22c9eace9fc4847bf`. Diff hygiene passed.

Review preflight, candidate capture, and both GitHub CI layers remain required after the clean candidate commit.

## Retry boundary

After the verified correction reaches `main`, confirm PyPI version 0.2.1 is still absent and dispatch the same protected workflow using:

- tag `v0.2.1`;
- wheel `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`;
- sdist `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4`.

The workflow must independently redownload the existing GitHub release. No rebuild or asset mutation is authorized.

## Residual risk

The GHCR manifest exists at verification time but remains an external dependency. PyPI trusted-publisher identity and service availability are not proven until the corrected run completes. The failed run remains immutable evidence and is never hidden or relabeled.
