+++
id = "REQ-IPK-003"
type = "requirement"
title = "Keep integration packages outside release and evaluator authority"
status = "approved"
owners = ["requirements-steward", "release-owner", "security-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an integration package is built, retained, downloaded, or installed, THE SYSTEM SHALL identify it as non-promotable candidate material, SHALL create no release or external publication state, and SHALL require operators to select and verify it explicitly without replacing the target repository's governing evaluator."
verification_method = "automated-authority-boundary-and-documentation-test"

[relations]
derives_from = ["CAP-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "requirements-steward"
+++

# Requirement: Keep integration packages outside release and evaluator authority

## Rationale

Installability is deliberately similar to a release. Without a hard vocabulary
and workflow boundary, a convenient testing wheel can be mistaken for released
authority or promoted through an unrelated publication path.

## Required response

- Call the output an `integration package`, never a release candidate or
  intermediate release in machine contracts.
- Record `promotable: false`, channel, expiration, exact commit, and workflow run
  in the manifest and documentation.
- Use no tag, GitHub Release, PyPI/TestPyPI upload, release environment,
  publication credential, RLS, REL, VREC transition, or release workflow input.
- Do not add the final artifact to `publish-pypi.yml` or any release bundle.
- Do not update `.engineering-harness.toml`, `.engineering-harness.lock`, a
  managed target, or the exact released evaluator automatically.
- Document isolated installation, checksum verification, identity inspection,
  disposable-target smoke testing, uninstallation, expiration, and the warning
  that `pip install --upgrade se-harness` selects the public index rather than
  this channel.

## Failure and boundary behavior

Any attempt to give the artifact a release tag, omit its non-promotable marker,
publish it to an index, use release credentials, or feed it into the release
workflow is outside this requirement and must fail review or static verification.

Installation grants technical capability only. It does not authorize the
installed package to govern an existing repository; that remains a separate
owner decision and managed evaluator transition.

## Acceptance examples

- A tester downloads the Actions artifact, verifies the checksums, installs it
  in `C:\temp\se-harness-integration`, and initializes a disposable repository.
  The existing production repository and its released evaluator do not change.
- A workflow change adds the integration wheel to a PyPI upload glob. Static
  verification fails before merge.
