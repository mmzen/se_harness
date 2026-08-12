+++
id = "REQ-DST-019"
type = "requirement"
title = "Declare reader expertise and progressive documentation paths"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a reader enters the public or explanatory SE Harness documentation, THE SYSTEM SHALL state the expected reader expertise for every in-scope document and SHALL provide a coherent path from conceptual understanding through practical use."
verification_method = "automated-inspection-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Declare reader expertise and progressive documentation paths

## Rationale

SE Harness documentation currently mixes onboarding, policy, implementation detail, and examples without consistently identifying the reader it expects. Readers need to know where to start and how to progress without treating a difficulty score as a quality rating.

## Required response

- Every in-scope public or explanatory document states `Target expertise: N/10` near its beginning.
- The score describes expected prior knowledge, not document quality or intrinsic complexity.
- The documentation path progresses from a 4/10 overview to 6/10 models and operational guidance and then to 7/10 practical examples.
- Cross-references route readers to deeper material instead of duplicating authoritative policy.

## Failure and boundary behavior

An expertise label must not imply access control, formal authority, artifact lifecycle state, or compliance. Formal engineering artifacts and historical evidence are not relabeled merely to satisfy this reader-navigation requirement.

## Constraints

The root `README.md` and every document under `docs/notes/` changed or created by this work are in scope. Managed policy files, formal artifacts, historical evidence, and installed consumer templates remain outside the labeling change.

## Acceptance examples

A new reader can begin at the 4/10 overview, follow links to the 6/10 model and phasing guides, and reach the 7/10 worked examples without inspecting source code first.

## Open decisions

None when approved.
