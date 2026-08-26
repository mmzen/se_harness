+++
id = "CAP-CIP-001"
type = "capability"
title = "Produce candidate evidence and a release from one execution of each check"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
derives_from = ["INT-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "product-owner"
+++

# Capability: Produce candidate evidence and a release from one execution of each check

## Description

The repository's pipeline runs every check that protects a user exactly once
per commit and per lane, hands the results downstream as artifacts rather
than recomputing them, expresses the release qualification once for both
its rehearsal and its authorized execution, and identifies a release unit by
a commit whose census is measured rather than declared.

## Users

Engineers pushing to pull requests; the release owner approving a release
unit; the assurance owner reading candidate evidence; agents following the
release sequences.

## Boundaries

Does not change what a check asserts. Does not move authority: publication
still needs the `pypi` environment decision, and the release still needs a
`released` record. Does not touch the managed router, lifecycle families, or
decision rights. The managed `engineering-harness.yml` changes in the
standard template only; the root copy follows at the next governor upgrade.

## Derived requirements

`REQ-CIP-001` through `REQ-CIP-006`.
