+++
id = "REQ-DST-022"
type = "requirement"
title = "Map the harness to one non-authoritative branching example"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN branching guidance illustrates the SE Harness lifecycle, THE SYSTEM SHALL document one coherent practical Git model at expertise level 6.5/10 while clearly preserving SE Harness independence from that repository policy."
verification_method = "manual-review-and-static-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Map the harness to one non-authoritative branching example

## Rationale

Teams need to see how approved artifacts, bounded implementation, pull requests, candidate commits, governance commits, tags, and releases can fit a normal Git workflow. The example must not become a hidden universal branching requirement.

## Required response

- Document exactly one branching model for this work packet.
- Show where work starts, where the declared work-order ID appears, how candidate and governance commits differ, and where the release tag points.
- Label branch names and merge strategy as illustrative repository policy.
- State that repositories may select different policies and that SE Harness enforces only declared repository or hosting controls within their actual scope.
- Keep terms consistent with the operational-phasing and practical-example notes.

## Failure and boundary behavior

The example must not claim that SE Harness requires GitFlow, trunk-based development, a particular default branch, a branch-name prefix, a merge method, or release branches. Repository-specific guidance must not waive formal artifact authority or work-order scope.

## Constraints

This work documents one model only. Adding programmable branch-policy enforcement, changing GitHub protection, renaming branches, or altering CI behavior is outside scope.

## Acceptance examples

A reader can map one approved work order to a feature branch and pull request, distinguish the candidate commit from later governance commits, and understand that another repository may legitimately choose a different branching policy.

## Open decisions

The packet proposes a simple main-plus-short-lived-work-branch model because it maps cleanly to the repository's one-work-order pull-request declaration without requiring release branches.
