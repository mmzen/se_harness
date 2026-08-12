+++
id = "ADR-IAR-003"
type = "adr"
title = "Assign review commands to the workflow module"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-IAR-003"]
+++

# ADR: Assign review commands to the workflow module

## Status

Accepted on 2026-08-12 through the repository owner's instruction `ok, make the change accordingly then`.

## Context

The router repeats review preflight from the workflow and separately owns the dashboard invocation. That allocation is functional but inconsistent with the responsibility boundary adopted for other lifecycle procedure.

## Decision drivers

- Give ordered lifecycle activity one focused owner.
- Keep the central contract concise without hiding authority constraints.
- Keep mandatory review instructions in fully managed content.
- Preserve safe two-file upgrade and integrity behavior.

## Decision

Keep only review routing and the evidence-versus-authority invariant in `ENGINEERING_HARNESS.md`. Assign exact review-preflight, dashboard generation, and candidate-inspection procedure to `WORKFLOW.md`, with quality conditions remaining in `QUALITY_GATES.md`.

## Consequences

The router becomes more consistent and the workflow becomes the single ordered-procedure owner. Two managed files and two lock digests change together. Reviewers must continue to evaluate router, workflow, and quality gates as a routed policy set.

## Validation

Execute `VER-IAR-003` and confirm exact command ownership, semantic preservation, safe prior-content migration, managed parity, deterministic evidence, and no behavior or authority changes.
