+++
id = "ADR-DST-001"
type = "adr"
title = "Adopt one standard template with hash-based ownership"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-DST-001"]
+++

# ADR

## Status

Accepted.

## Decision

Maintain exactly one canonical repository template. Track tool-owned content with hashes, use bounded managed blocks for shared root files, and preserve customized files during upgrade.

## Consequences

Installations are predictable and testable, while repositories can customize workflow documents without silent replacement. Customized files require explicit human reconciliation when the distribution evolves. Separate minimal or offline modes are deliberately unsupported.

