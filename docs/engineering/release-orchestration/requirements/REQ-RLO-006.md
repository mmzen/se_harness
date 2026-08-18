+++
id = "REQ-RLO-006"
type = "requirement"
title = "Deploy the release demonstration from trusted main context"
status = "approved"
owners = ["release-owner", "service-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN the final GitHub Release is available, THE SYSTEM SHALL generate and deploy the SE Harness demonstration from the immutable main-history governance snapshot while the Pages deployment remains in a main-authorized workflow context."
verification_method = "automated-provenance-pages-policy-and-replay-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Deploy the release demonstration from trusted main context

## Rationale

The tag identifies candidate code, while the demonstration must include the later released governance record. A GitHub `release` event runs under a tag ref and is rejected by the deliberately main-only Pages environment.

## Preconditions and trigger

The orchestrator was dispatched from `main`, resolved a released RLS and immutable governance commit, and verified the final GitHub Release.

## Required response

Reuse the existing released-governor validation, canonical Explorer generation, immutable provenance resolution, bounded Pages packaging, and least-privilege deployment controls from the main-context orchestration. Retain a manual main-only replay using explicit release and governance identities for recovery.

## Failure and boundary behavior

Do not deploy from a tag checkout, moving main head, missing record, or mismatched candidate. A build or deploy failure leaves the last successful site intact and remains replayable without changing lifecycle state or the software release.

## Constraints

The demonstration is repository-specific derived promotional output. It does not become package assurance, release authority, or consumer-template content.

## Acceptance examples

The orchestrator publishes the exact governance snapshot under the main-authorized environment. A release event with `refs/tags/v...` cannot independently enter the deployment job.

## Open decisions

None.
