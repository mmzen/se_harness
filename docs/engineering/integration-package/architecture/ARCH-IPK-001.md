+++
id = "ARCH-IPK-001"
type = "architecture"
title = "Qualified Actions-artifact lane outside the release pipeline"
status = "approved"
owners = ["technical-owner", "security-owner", "service-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-IPK-001", "REQ-IPK-002", "REQ-IPK-003"]
conforms_to = ["SPEC-IPK-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["deployment-or-operating-model", "security-privacy-or-trust-boundary", "technology-framework-vendor-or-external-service", "concurrency-consistency-reliability-or-failure-strategy", "material-alternatives"]
rationale = "The design creates a new hosted package-distribution lane, uses GitHub Actions artifact storage, defines which staged bytes become available after concurrent platform checks, and must preserve a strict trust boundary from release and evaluator authority. Direct Git installation, retained same-version wheels, package-index publication, and Actions artifacts are materially different alternatives."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "technical-owner"
+++

# Architecture: Qualified Actions-artifact lane outside the release pipeline

## Context and scope

Candidate CI already proves that an exported commit can build and install. The
missing boundary begins after that proof: preserving exact tested bytes for a
human tester without entering release orchestration.

## Components and responsibilities

- **Candidate gates:** existing source, package, and migration jobs remain the
  prerequisites and do not retain a user-facing wheel.
- **Exact-export builder:** repository-owned standard-library script that
  validates the event identity, extracts a bounded archive, applies the declared
  identity overlay, builds twice, and emits the staged payload.
- **Staging artifact:** one-day internal handoff of exact bytes from build to
  independent platform jobs. Its name cannot be confused with the final channel.
- **Platform verifiers:** Linux and Windows independently validate and install
  the same staging payload. They do not trust builder-reported hashes.
- **Retention coordinator:** waits for all verifiers, rechecks payload identity,
  and makes the final expiring artifact visible.
- **Operator documentation:** turns a run and commit into a safe, explicit
  download and isolated-install procedure.

## Dependency direction

Commit and event metadata flow into the exact-export builder. Immutable staged
bytes flow to platform verifiers. Successful platform results permit the
retention coordinator to copy the same bytes. Nothing flows from the integration
lane into release preparation, publication, managed-root selection, or lifecycle
authority.

The repository script depends only on the Python standard library and invokes
the separately installed, exact-pinned build frontend through structured
arguments. Product runtime code does not depend on the integration script.

## Trust boundaries

GitHub supplies event metadata and artifact storage, but neither supplies
release authority. Archives, downloaded artifacts, wheel metadata, and manifests
are untrusted until independently checked. Workflow credentials are read-only;
no publishing secret or release environment is available.

The version overlay is trusted only because its two paths and exact transformations
are declared, hashed, repeated independently, and excluded from the checkout.

## Reliability and failure strategy

- Build twice and require byte equality.
- Stage once, verify the same bytes on both platforms, and retain only after the
  matrix converges.
- Use exact file inventories and hashes at every boundary.
- Treat cancelled, skipped, timed-out, missing-output, or partial matrix results
  as failure to retain.
- Keep staging briefly for diagnosis and final artifacts long enough for testing;
  rely on the commit for reproduction after expiry.

## Required patterns

- Plan and validate before writing a final payload.
- Canonical manifest and portable filenames.
- No-index clean-environment install.
- Least-privilege `contents: read` workflow permissions.
- Explicit non-promotable identity at every output boundary.

## Prohibited patterns

- Retaining the existing same-version candidate wheel as the final artifact.
- Patching committed version files.
- Uploading to a package index or GitHub Release.
- Reusing release bundles, credentials, tags, RLS records, or publication jobs.
- Making a platform verifier rebuild the wheel it claims to verify.
- Automatically installing into or upgrading a non-disposable repository.

## Conformance checks

Execute `VER-IPK-001`, including deterministic double build, hostile archive and
manifest cases, exact file inventory, Linux/Windows same-byte installation,
workflow/static authority checks, and documentation command rehearsal.

## Related ADRs

`ADR-IPK-001` selects GitHub Actions artifacts with a disposable PEP 440 local
version overlay and rejects the release-like alternatives.
