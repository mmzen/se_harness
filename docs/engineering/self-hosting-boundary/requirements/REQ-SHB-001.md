+++
id = "REQ-SHB-001"
type = "requirement"
title = "Pin one released governor for self-hosted development"
status = "implemented"
owners = ["requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN the harness repository is developed, THE SYSTEM SHALL govern the repository through one exact independently published harness distribution whose version, artifact, source, and digest are pinned separately from the candidate version."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Pin one released governor for self-hosted development

## Required behavior

- The governor is the latest separately selected released distribution, normally N-1 while candidate N is developed.
- Its wheel name, immutable release URL, version, and SHA-256 are declared as host-governance inputs, not derived from candidate source.
- Governor installation occurs in an isolated environment outside the checkout and without editable installation.
- Governor operational managed state and its lock live only in the isolated governor target outside the checkout. The checkout root belongs to candidate source and records the selected governor through a narrow repository-specific descriptor.
- The governor performs no upgrade, template rewrite, dashboard write, or other mutation of the candidate checkout.
- Failure to acquire or verify the exact governor stops independent assurance.

## Boundary

Pinning a governor is bootstrap assurance, not proof that it understands every new candidate schema or behavior.
