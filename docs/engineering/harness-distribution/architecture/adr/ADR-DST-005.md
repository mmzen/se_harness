+++
id = "ADR-DST-005"
type = "adr"
title = "Use advisory canonical paths with safe domain-aware authoring"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-DST-005"]
+++

# ADR: Use advisory canonical paths with safe domain-aware authoring

## Status

Accepted.

## Context

SE Harness recursively discovers artifacts by metadata, which allows existing repositories to organize domains flexibly. A consumer trial placed artifacts directly below its business-goal directory, while the distribution repository uses type-specific subdirectories. Both layouts validate, but the difference weakens predictability, Explorer navigation, agent instructions, and user expectations.

The harness must guide new authoring more strongly without invalidating or silently rewriting repositories that adopted the earlier behavior. It must also keep typed relations and lifecycle state—not paths—as the authority model.

## Decision drivers

- Make new and existing repositories predictable for humans and coding agents.
- Keep artifact creation safe, deterministic, and visibly non-authorizing.
- Co-locate single-domain provenance with the domain it substantiates.
- Preserve all valid legacy layouts and historical provenance.
- Avoid disruptive automatic moves and concurrent-editor conflicts.
- Keep one standard installation and one artifact model.

## Considered options

1. **Leave layout implicit and document examples only**: preserves compatibility but does not systematically prevent divergent authoring.
2. **Make canonical paths validation errors**: produces immediate consistency but confuses organization with authority and breaks valid installed repositories.
3. **Precreate one repository-wide type tree during installation**: standardizes paths but separates business domains and does not solve domain-local provenance or migration.
4. **Automatically reorganize owner artifacts during upgrade**: yields a uniform tree but creates unsafe, noisy, and potentially conflicting repository changes outside managed-file ownership.
5. **Define advisory canonical paths, provide safe authoring commands, and route single-domain provenance locally**: proposed because it improves future consistency while preserving graph semantics and legacy content.

## Decision

Adopt option 5. Define one canonical type-specific layout below each engineering domain. Centralize the mapping and use it for fresh-install guidance, `scaffold-domain`, `create-artifact`, provenance defaults, diagnostics, and tests.

Paths remain advisory organization. Artifact IDs, declared types, typed relations, lifecycle states, exact commit provenance, and accountable transitions remain authoritative. A noncanonical but otherwise valid artifact produces an actionable warning, not a validation error.

Add explicit and inferred single-domain routing for new verification and release records, while preserving explicit output precedence and repository-wide aggregate locations. Never move or rewrite repository-owned artifacts during installation or upgrade. Any legacy migration requires a separately authorized, reviewable repository change.

## Consequences

New authoring becomes consistent and less dependent on agent interpretation. Domain views contain their intent-to-release chain when the work is domain-local. Existing repositories remain operational and receive migration guidance without forced changes.

The CLI and validator gain a shared mapping and additional safety tests. Users may temporarily see advisory warnings until they choose to migrate. Aggregate records continue to live outside a domain by design, so the documentation must explain both locations.

## Validation

Apply `VER-DST-005`. Verify all type mappings, malicious and conflicting path cases, failure atomicity, incomplete draft output, provenance precedence and inference, legacy graph validity, advisory exit behavior, aggregate exceptions, upgrade byte preservation, installed guidance, packaged-template parity, full regression checks, and manual review of the authority boundary.

## Revisit conditions

Revisit if a future artifact schema makes domain identity explicit in metadata, if warning volume reduces diagnostic usefulness, if cross-domain aggregation needs a first-class domain model, or if the ownership contract gains a safe separately authorized migration facility.
