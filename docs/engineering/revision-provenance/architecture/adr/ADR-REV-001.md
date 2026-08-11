+++
id = "ADR-REV-001"
type = "adr"
title = "Use formal instance records rather than mutating reusable contracts"
status = "approved"
owners = ["technical-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-REV-001"]
+++

# ADR

## Status

Accepted.

## Decision

Add `verification_record` and `release_record` artifact types. Contracts retain reusable policy, while records bind one clean candidate commit to evidence and an accountable decision. Records are committed after the candidate they name.

## Consequences

Intent-to-commit lineage is explicit and queryable. Release policy no longer accumulates mutable release instances. Governance commits follow candidate commits, and repositories must reconcile records with tags through their release process.

