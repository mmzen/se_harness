+++
id = "REQ-RLO-007"
type = "requirement"
title = "Resume only from exact external state"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN release orchestration is replayed or observes prior external state, THE SYSTEM SHALL continue only across complete exact matches and shall fail closed on partial, ambiguous, or mismatched state without rewriting immutable history."
verification_method = "automated-state-machine-and-failure-injection-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Resume only from exact external state

## Rationale

GitHub, PyPI, and Pages mutations are not one atomic transaction. Safe automation needs explicit reconciliation semantics rather than blind retry or generic `skip existing` behavior.

## Preconditions and trigger

A run starts after no prior attempt, after a failed stage, or after a fully successful release.

## Required response

Classify each external boundary as absent, complete exact, partial, or mismatched. Create only absent eligible state; treat complete exact state as already completed; stop on partial or mismatched immutable state. Permit a Pages-only replay from the same release and governance identities because Pages is replaceable derived output.

## Failure and boundary behavior

Never move a tag, replace a final GitHub asset, suppress a PyPI duplicate inside the publisher, delete a partial package version, select a new candidate, or alter expected hashes. Preserve diagnostics sufficient for an accountable corrective decision.

## Constraints

Concurrency is serialized per version and for production publication. Cancellation must not interrupt an active immutable publication step.

## Acceptance examples

A rerun after full success performs verification and no duplicate upload. A rerun after tag creation continues to draft release staging. A version with only its wheel on PyPI stops as partial and requires human disposition.

## Open decisions

None.
