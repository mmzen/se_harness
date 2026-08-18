+++
id = "OPS-PYP-001"
type = "operating_contract"
title = "Operate the PyPI publication channel"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-18"

[relations]
assures = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
+++

# Operating Contract: Operate the PyPI publication channel

## Service level objectives

Every authorized production publication either uploads the exact released wheel and sdist with attestations or fails visibly before/at PyPI without rebuilding, fallback credentials, or duplicate suppression. No unauthorized workflow run is approved through the environment.

## Observability

Observe the selected RLS, derived release plan, environment deployment approval, logs, action SHA, release asset URLs and hashes, PyPI project/version/file pages, PyPI hashes and attestations, and an exact-version installation smoke test.

## Alerts and escalation

Treat publisher mismatch, missing environment protection, changed action pin, hash/manifest divergence, draft/prerelease selection, existing filename, metadata or attestation failure, partial upload, unexpected PyPI owner, or install failure as blocking. Escalate to repository, release, quality, and security owners.

## Capacity and cost boundaries

One protected job downloads and, when absent, uploads one small wheel and sdist per released-record orchestration. No cache, persistent runner, background service, API-token rotation, or automatic retry is required.

## Backup and recovery

GitHub retains immutable tag history, release assets, checksums, workflow runs, and governance evidence. PyPI files cannot be replaced. Recover from an unpublished failure by correcting configuration and obtaining a new dispatch authorization; recover from a defective published artifact through a new verified version.

## Security and compliance controls

Maintain required environment review, exact PyPI publisher identity, job-scoped read/OIDC permissions, immutable action pinning, no checkout/build, independent hashes, exact manifest equality, metadata verification, attestations, and no duplicate skipping or stored credential.

## Automated remediation envelope

Automation may resolve the operator-selected released RLS, validate derived identities, download public release assets, compare bytes, request short-lived OIDC credentials through the pinned publisher, and upload only after environment approval. It may not select the latest release, change hashes, approve deployment, retry a partial publication automatically, delete external state, or create a corrective version.

## Runbooks

Before dispatch, inspect the governing released record, its structured distribution block, environment protection, PyPI publisher, and action pin. Dispatch `publish-pypi.yml` from `main` with only that RLS ID. After success, compare PyPI hashes to the derived release plan, inspect attestations, install `se-harness==VERSION` in a fresh environment, run `harnessctl --version`, and retain results. For any anomaly, stop and preserve external state.

## Evidence retention

Retain the publication authorization, workflow/deployment URLs, approver, tag and candidate, GitHub and PyPI asset URLs, hashes, attestations, timestamps, install command/output, deviations, partial states, and corrective decision.
