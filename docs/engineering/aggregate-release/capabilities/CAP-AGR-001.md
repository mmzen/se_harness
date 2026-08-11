+++
id = "CAP-AGR-001"
type = "capability"
title = "Prepare and inspect an aggregate software release"
status = "approved"
owners = ["product-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-AGR-001"]
+++

# Capability: Prepare and inspect an aggregate software release

## Actor and need

An assurance or release owner needs to qualify a version containing multiple release-bearing work orders without losing intent-to-requirement-to-commit lineage.

## Capability statement

An accountable owner can explicitly select multiple work orders, their verification contracts, and retained evidence; bind the combined scope to one clean final candidate commit; prepare a release record for the same scope and commit; and inspect every resulting lineage in the Harness Explorer.

## Boundaries

The capability prepares `ready` records only. It does not infer scope, grant approval, transition lifecycle state, mutate Git, create a tag, build a package, or publish a release.

## Outcomes

One version has one unambiguous candidate commit and an explicit set of released work. Every listed work order has evidence at that candidate, and single-item use remains a supported special case.

## Candidate requirements

Aggregate verification capture, aggregate release preparation, exact scope and commit consistency, deterministic validation, backward-compatible CLI behavior, complete Explorer lineage, preserved authority boundaries, and safe template upgrades.
