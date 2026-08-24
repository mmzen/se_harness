+++
id = "ADR-IPK-001"
type = "adr"
title = "Use expiring Actions artifacts with disposable local-version overlays"
status = "approved"
owners = ["technical-owner", "repository-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "technical-owner"
+++

# ADR: Use expiring Actions artifacts with disposable local-version overlays

## Status

Proposed. The authoritative lifecycle state is the front-matter `status`; this
document records no accepted decision while it remains `draft`.

## Context

The candidate workflow already builds and installs a wheel from an exact commit,
but discards it. Retaining that wheel unchanged would make unreleased bytes and
the public `0.6.0` distribution report the same version. Installing from Git
avoids retained storage but makes every tester rebuild and does not solve that
identity ambiguity. A package index or GitHub Release would make discovery
easier at the cost of creating a release-like publication surface.

The repository needs an installable current-commit package for bounded testing,
not another promotion channel.

## Decision drivers

- Bind installed behavior to one exact commit and workflow run.
- Ensure a public release and an unreleased integration build never share a
  version identity.
- Retain only bytes installed successfully on Linux and Windows.
- Let artifacts expire without changing release history.
- Use no publication credential, release environment, tag, or lifecycle record.
- Keep the committed base version unchanged for ordinary release preparation.
- Provide a route that operators can use with standard GitHub and Python tools.

## Considered options

### Option A: document direct installation from Git

Operators could use `pip install` against a commit URL. This has little CI
surface, but each operator performs an independent build, cannot download the
exact wheel verified by CI, and receives the unchanged base version.

### Option B: retain the current same-version candidate wheel

This reuses existing build output and is operationally simple. It is rejected
because different candidate commits and the public release would all claim the
same installed version.

### Option C: publish pre-releases to TestPyPI or PyPI

An index provides familiar installation and retention. It also requires
credentials, globally managed version identities, publication cleanup and a
release-like operating model. TestPyPI is not a dependable private integration
channel and PyPI uploads are immutable external publication actions.

### Option D: create GitHub pre-releases or draft releases

Release assets are discoverable and durable, but tags and GitHub Release state
would deliberately blur the boundary this design must preserve.

### Option E: retain expiring GitHub Actions artifacts with a disposable PEP 440 local version

CI exports the exact commit, overlays only the two version declarations in
disposable directories, builds deterministically, verifies the same staged
bytes on Linux and Windows, then retains a short-lived artifact. The manifest
marks the distribution non-promotable and binds its provenance.

### Option F: operate a private integration package index

A private index could later provide stronger discovery and retention controls,
but introduces service ownership, authentication, credentials, cleanup policy,
availability and cost. It is deferred until artifact-based usage demonstrates
that those costs are justified.

## Decision

Choose Option E.

- A `main` package version is `<base>+main.g<sha12>`.
- A pull-request package version is `<base>+pr<number>.g<sha12>`.
- The overlay exists only in two independent disposable exact-commit exports;
  candidate checkout and committed version files remain unchanged.
- The final artifact is named `se-harness-integration-<full-commit>` and contains
  exactly one wheel, `integration-manifest.json`, and `SHA256SUMS`.
- One-day staging transfers exact bytes to Linux and Windows verification. Final
  retention is 14 days for `main` and 3 days for pull requests.
- The artifact is installable for testing but is non-promotable. It cannot be
  fed into PyPI publication, GitHub Release creation, RLS/REL preparation, or
  automatic governing-evaluator selection.
- Option F may be reconsidered only through a separate approved architecture
  decision and work order.

## Consequences

### Positive

- A tester installs the exact wheel verified by CI.
- Version and commit are visible through normal package interfaces.
- Expiration limits stale candidate accumulation and does not rewrite history.
- Release credentials and release state remain outside the workflow.

### Negative

- GitHub authentication may be required to download an Actions artifact.
- Artifact discovery is less convenient than `pip install` from an index.
- An expired package must be reproduced from the same reachable commit.
- Local-version ordering is not a substitute for release ordering and the
  package must be installed by explicit file path.

### Operational

- Operators select a workflow run, download the exact artifact, verify its
  checksums, and install it into an isolated environment.
- CI maintains pinned build tools and must test Linux and Windows before final
  retention.
- Documentation must state that normal index upgrades do not select this lane.

### Security

- Commit archives, manifests, checksums, wheels and workflow metadata remain
  untrusted until checked at each boundary.
- Workflow permissions stay at `contents: read`; no release environment or
  publishing secret is available.

## Validation

Execute `VER-IPK-001`: deterministic independent builds, hostile archive and
payload cases, exact manifest and checksum checks, same-byte Linux/Windows
installation, retention dependency checks, release-authority static scans, and
operator-command rehearsal.
