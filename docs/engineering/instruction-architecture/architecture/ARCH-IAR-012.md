+++
id = "ARCH-IAR-012"
type = "architecture"
title = "Released resources with thin host adapters"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[decision_assessment]
outcome = "adr_required"
triggers = ["data-ownership-or-persistence", "deployment-or-operating-model", "security-privacy-or-trust-boundary", "material-alternatives"]
rationale = "Moving selected policy out of repositories changes resource ownership, CI delivery and version isolation. Cloning after startup also requires a small host-session checkout record. Review both boundaries in the existing ADR."
assessed_by = "Codex drafting agent; proposed for human technical review"

[relations]
addresses = ["REQ-IAR-029", "REQ-IAR-030", "REQ-IAR-031"]
conforms_to = ["SPEC-IAR-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 5f12e9bde409331d8a1bfee358c979eee1e97a19b32ee4be35771d8281c933eb."
+++

# Released resources with thin host adapters

## Components and responsibilities

- Repository: portable release selection, formal authority and owner content.
- Released wheel: one resource set, integrity identity and lifecycle evaluator.
- Private environment: immutable selected installation outside the checkout.
- Resource resolver: validates selection and exposes the selected files/headings.
- Plugin bootstrap: brief selection/setup guidance before a checkout is active.
- Activation helper: validates the exact checkout, records it for the host session,
  and immediately returns its selected entry through the resource resolver.
- Session record: local checkout path outside repositories, scoped to one host
  and session; contains no lifecycle authority or copied policy.
- Plugin: setup, startup/compaction delivery and skills that follow resolver results.
- CI/CLI: resolve the same package directly, without installing a host plugin.
- Installer: previews and applies the minimal repository writes and safe migration.

## Dependency direction and trust

The plugin and CI depend on the selected released evaluator. The evaluator reads
repository artifacts as inputs. Repository content cannot choose executable code
from a checkout or supply replacement lifecycle rules through a copied JSON file.
Plugin caches and machine paths are not portable authority; release identity is.
The session record is an input locator. Treat it as untrusted input and validate
the referenced repository and released identity before use. Host/session identity
comes from the host event, not transcript parsing or a shared parent directory.

## Flow

With no repository selected, deliver the bootstrap. The agent clones or identifies
the requested checkout and calls activation. Activation validates it, records the
session selection and returns the compact entry before governed work.

On startup, compaction or resume, resolve the saved session selection first, or
discover from the host cwd when there is no saved selection. Read the repository's
release pin, locate the installed environment, validate identity, resolve resources
and deliver the entry. An invalid saved selection reports its gap without fallback.
The hook performs no installation or lifecycle mutation. Distinct release
environments coexist; coordinated setup fills a missing one without changing an
environment another session uses. New work and delivery use existing procedures.

## Significant decision and cost

Use the existing wheel as the resource carrier. A plugin-only copy would require
another CI delivery mechanism and could drift when the plugin updates. A separate
resource archive would add a manifest, publisher and compatibility relation without
an agreed need. The added costs here are one external resource lookup, explicit
discovery locations and a supported legacy-layout branch. One small local record
per host session is also needed: cwd-only discovery cannot find a checkout cloned
below the session directory. This record avoids repeated human path entry and
keeps parallel sessions independent. It requires no repository file or background
service. The existing ADR records this bounded adapter choice with the carrier.

## Conformance

The three verification contracts cover resource identity, native delivery and
minimal installation/migration. This architecture changes resource persistence
and trust boundaries, so its selected ADR is required before work approval.
It supplies no acceptance or release decision by itself.
