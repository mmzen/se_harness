+++
id = "WO-WLC-001"
type = "work_order"
title = "Normalize and enforce work-order lifecycle semantics"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
specifications = ["SPEC-WLC-001"]
architecture = ["ARCH-WLC-001", "ADR-WLC-001"]
verification = ["VER-WLC-001"]
+++

# Work Order: Normalize and enforce work-order lifecycle semantics

## Objective

Make work-order completion and assurance unambiguous, remove the recursive governance-status anomaly, enforce configured verified-work provenance, and distribute the same behavior through the standard harness.

## Authorization

The accountable repository owner explicitly approved the recommended normalization and enforcement on 2026-08-11 with the instruction `yes, ok go` after reviewing the current approved, implemented, and verified work-order inventory and its Explorer findings.

## In scope

- Add policy-aware verified-work coverage validation and deterministic tests.
- Remove duplicate derived `W-REV-001` generation.
- Update canonical and self-installed lifecycle documentation and the work-order template.
- Normalize exactly the eleven legacy work orders named by `SPEC-WLC-001` to `implemented`.
- Update managed integrity through the supported self-upgrade path.
- Retain complete implementation evidence keyed to this work order.

## Out of scope

Changing VREC or RLS status, relations, commits, hashes, timestamps, or authority; changing release payload; superseding records; adding lifecycle values; inferring completion automatically; committing; pushing; opening or merging a pull request; creating or moving a tag; dispatching or approving the PyPI workflow; package upload; and deployment.

## Authorized decision envelope

The implementation may choose concise helper and test names, reuse existing `E010` revision-consistency classification, and update documentation wording without broadening lifecycle semantics. It may not normalize additional work orders, change historical evidence, or weaken configured provenance requirements.

## Expected change surface

Formal packet and evidence; eleven legacy work-order front matters; root and canonical validator, Explorer, workflow, traceability, and work-order template; focused revision-provenance tests; self-repository lock metadata.

## Required verification

Perform every check in `VER-WLC-001`, validate the graph before and after implementation, run the full suite on Python 3.11 and the local runtime, verify managed integrity and installed-repository behavior, review the final diff, and retain exact results and residual risks.

## Stop and escalate conditions

Stop if normalization would change a VREC or RLS, a completed action lacks evidence, configuration-disabled compatibility breaks, canonical/root parity cannot be achieved safely, a required test fails, or completion would require commit, remote, release, or publication authority.

## Completion evidence

Retain commands, results, normalized IDs, provenance-preservation inspection, deviations, and authority boundaries in `docs/engineering/work-order-lifecycle/evidence/WO-WLC-001-verification.md`.
