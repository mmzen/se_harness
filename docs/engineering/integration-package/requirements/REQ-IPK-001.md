+++
id = "REQ-IPK-001"
type = "requirement"
title = "Bind every integration wheel to a unique version and exact commit"
status = "approved"
owners = ["requirements-steward", "repository-owner", "technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an eligible candidate commit enters the integration-package lane, THE SYSTEM SHALL derive a unique PEP 440 local version from the unchanged base version, event channel, and commit, SHALL apply that overlay only to a disposable exact-commit export, and SHALL bind the resulting wheel, overlay, build environment, and workflow run in a canonical manifest and checksum set."
verification_method = "automated-package-provenance-test"

[relations]
derives_from = ["CAP-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "requirements-steward"
+++

# Requirement: Bind every integration wheel to a unique version and exact commit

## Rationale

The current candidate wheel contains different bytes from public `0.6.0` while
reporting the same version. A retained copy would make that ambiguity durable.
The integration identity must therefore differ without changing the source
version that governs ordinary release preparation.

## Required response

- Require the versions in `pyproject.toml` and `se_harness/__init__.py` to match.
- Reject a base version that already contains a local-version segment.
- Derive `<base>+main.g<sha12>` for a `main` push and
  `<base>+pr<number>.g<sha12>` for a pull-request candidate.
- Export the exact candidate commit with Git, reject unsafe archive members, and
  modify only the two declared version fields in disposable export directories.
- Build twice from independent exports with pinned build-tool versions and a
  commit-derived `SOURCE_DATE_EPOCH`; require byte-identical wheels.
- Emit canonical UTF-8/LF `se-harness-integration-package-v1` JSON recording the
  full commit, channel, base and integration versions, workflow run and attempt,
  Python and build-tool versions, overlay path and before/after hashes, wheel
  filename, size, and SHA-256, plus `promotable: false`.
- Emit `SHA256SUMS` for the wheel and manifest using lowercase SHA-256 values and
  deterministic path ordering.

## Failure and boundary behavior

Mismatch between source version fields, malformed event identity, unsafe
archive paths, symlinks, unexpected overlay changes, nondeterministic wheels,
invalid wheel metadata, manifest mismatch, or checksum mismatch fails before a
final artifact is retained. No fallback removes the commit from the version or
reuses the base version unchanged.

The overlay never changes the checkout, commit, tag, release record, source
archive, or public version declaration.

## Acceptance examples

### Main candidate

Given base `0.6.0` and commit
`1cdc75259da8156e93ad8c32110ee196296b8cea`, the integration version is
`0.6.0+main.g1cdc75259da8`; both independent builds produce one identically named
and byte-identical wheel, and the manifest binds the full commit.

### Failure

If `pyproject.toml` reports `0.6.0` while `se_harness/__init__.py` reports
`0.6.1`, the lane fails and retains no final integration artifact.
