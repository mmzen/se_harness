+++
id = "REQ-IPK-002"
type = "requirement"
title = "Retain only integration packages installed successfully on Linux and Windows"
status = "approved"
owners = ["requirements-steward", "quality-owner", "service-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an integration wheel has been built deterministically, THE SYSTEM SHALL verify the exact staged bytes on Linux and Windows in fresh isolated environments, SHALL retain one final artifact only after both platforms pass, and SHALL make artifact expiration and exact installation inputs explicit."
verification_method = "hosted-cross-platform-installation-test"

[relations]
derives_from = ["CAP-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "requirements-steward"
+++

# Requirement: Retain only integration packages installed successfully on Linux and Windows

## Rationale

A wheel that existed only inside one successful Linux job is evidence, not a
usable integration channel. The consumer must receive the same bytes that were
actually installed on both supported operating-system families.

## Required response

- Stage the payload for at most one day after deterministic build.
- On Linux and Windows, download the staged payload, independently verify the
  manifest and every checksum, install the wheel into a new virtual environment
  with `--no-index --no-deps`, and run outside the checkout with isolated Python.
- Require installed version and wheel metadata to equal the manifest version.
- Exercise `harnessctl --version`, `init`, `doctor`, `validate`, and managed
  upgrade on a disposable standard repository.
- Prove the checkout remains unchanged.
- Only after both platform jobs pass, copy the same staged bytes into the final
  artifact named `se-harness-integration-<full-commit>`.
- Retain `main` artifacts for 14 days and pull-request artifacts for 3 days.

## Failure and boundary behavior

A missing file, extra file, checksum failure, metadata mismatch, platform test
failure, checkout change, or staging/final byte difference prevents final
retention. A failed or cancelled workflow may leave a clearly named one-day
staging artifact for diagnostics, but never the final artifact name.

Expiration is normal. Operators reproduce an expired artifact by running the
same governed workflow for the same reachable commit; they do not silently use
a newer commit.

## Acceptance examples

- One `main` run finishes with a final artifact containing exactly the verified
  wheel, manifest, and checksum file; both platforms installed the wheel hash in
  that manifest.
- Windows reports a version mismatch: the final retention job is skipped and no
  artifact beginning `se-harness-integration-` is created for that run.
