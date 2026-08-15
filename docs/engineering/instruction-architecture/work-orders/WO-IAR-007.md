+++
id = "WO-IAR-007"
type = "work_order"
title = "Implement the first validation diagnostic taxonomy"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-IAR-015"]
specifications = ["SPEC-IAR-007"]
architecture = ["ARCH-IAR-007", "ADR-IAR-007"]
verification = ["VER-IAR-007"]
+++

# Work Order: Implement the first validation diagnostic taxonomy

## Lifecycle and authorization

The repository owner approved `REQ-IAR-015`, `SPEC-IAR-007`, `ARCH-IAR-007`, `ADR-IAR-007`, `VER-IAR-007`, and this bounded work order on 2026-08-15 with the instruction `ok i approve`. The bounded implementation and retained evidence are complete, so this work order is now `implemented`. Evidence is retained at `docs/engineering/instruction-architecture/evidence/WO-IAR-007-verification.md`. This state records completed work, not independent verification, and does not authorize commit, push, pull-request creation, VREC preparation or transition, release, tag, publication, or deployment.

## Objective

Make existing validation results immediately understandable as structure, governance, configured policy, or maintenance findings while preserving every current gate and avoiding new operational concepts.

## In scope

- Add the closed four-plane vocabulary and taxonomy version.
- Classify every current validator diagnostic explicitly at its rule emission.
- Add plane metadata and deterministic plane counts to JSON.
- Add a compact plane summary and visible labels to human output.
- Preserve codes, messages, paths, errors versus warnings, validity, and exit behavior.
- Add baseline-compatibility and full taxonomy coverage tests.
- Add concise authoritative taxonomy wording to `QUALITY_GATES.md` and update focused command-reference wording without duplicating a rule catalog.
- Update canonical managed copies, package expectations, and the schema-2 lock through the supported transaction.
- Retain work-order-keyed evidence.

## Out of scope

New validation rules; profiles; `inspect` or other commands; pending, orphan, aging, or maintenance heuristics; policy-schema changes; evaluator identity; changes to `preflight`, `doctor`, or dashboard decisions; aggregate health scores; severity or exit-code changes; lifecycle transitions outside this packet; self-hosting governor reconciliation; release, tagging, publication, or deployment.

## Authorized decision envelope

If approved, implementation may choose concise field and rendering layout, test helpers, and internal constants. It may not add a fifth plane, infer planes solely from code ranges, change a diagnostic's meaning or severity, introduce a score, or expand into the excluded follow-on capabilities.

## Expected change surface

- `scripts/validate_engineering_artifacts.py` and its canonical standard-template copy.
- `docs/engineering/QUALITY_GATES.md` and its canonical copy.
- Focused validator, output, documentation, installer, integrity, and package-data tests.
- `docs/notes/harnessctl-reference.md` only for concise operator-facing interpretation.
- `.engineering-harness.lock`, this domain index, acceptance scenarios if needed, and `WO-IAR-007` evidence.

## Implementation plan

1. Obtain accountable approval for the complete packet and transition this work order to `in_progress`.
2. Capture current text, JSON, exit-code, and fixture diagnostics as the compatibility baseline.
3. Add failing tests for the four-value vocabulary, complete rule classification, output fields, and unchanged semantics.
4. Implement explicit plane construction and deterministic report summaries.
5. Update concise authoritative and operator documentation.
6. Apply the supported managed upgrade and prove parity and idempotence.
7. Execute `VER-IAR-007` on Python 3.11 and the local runtime, retain evidence, transition implementation artifacts appropriately, and stop for separate commit authority.

## Stop conditions

Stop if the change requires a new command, new validation rule, policy redesign, evaluator selection, severity change, exit-code change, historical artifact rewrite, aggregate score, managed-customization loss, or authority beyond this work order.
