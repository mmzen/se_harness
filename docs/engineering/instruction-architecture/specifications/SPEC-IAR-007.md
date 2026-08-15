+++
id = "SPEC-IAR-007"
type = "specification"
title = "Additive validation diagnostic taxonomy"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-IAR-015"]
+++

# Specification: Additive validation diagnostic taxonomy

## Scope

Add one explicit assessment-plane field to the existing repository validator and expose deterministic plane summaries. This is a reporting-model change only. It does not split the validator, add commands or profiles, or alter any validation rule.

## Taxonomy

The allowed plane vocabulary is closed and versioned as `se-harness-validation-taxonomy-v1`:

| Plane | Meaning | Current examples |
| --- | --- | --- |
| `structure` | Files and metadata can form a typed formal graph. | parsing, required fields, ID uniqueness and prefixes, relation shape, target existence and target type |
| `governance` | The graph preserves mandatory SE Harness assurance invariants. | active requirement coverage, architecture traceability, ADR applicability, VREC/RLS consistency, evidence paths, supersession |
| `policy` | Enforcement originates from an explicit repository configuration switch. | configured provenance coverage for work-order lifecycle claims |
| `maintenance` | The graph remains valid but carries a compatibility or organization advisory. | non-canonical location, legacy architecture trace, missing legacy decision assessment |

Classification is rule-specific, not inferred from the first letter or number of a diagnostic code. A code reused by distinct rules may therefore be emitted in different planes when the rule authority differs.

## Diagnostic contract

Each diagnostic retains `path`, `code`, and `message` and adds `plane`. Errors and warnings remain separate collections; plane does not replace severity. Construction must reject an unknown or missing plane during development and tests.

JSON output retains `valid`, artifact and error/warning counts, `errors`, `warnings`, and `artifacts`. It adds:

- `taxonomy = "se-harness-validation-taxonomy-v1"`;
- `plane_counts`, containing deterministic error and warning counts for all four planes;
- `plane` on every error and warning item.

Human output retains the current overall status, artifact/error/warning summary, and complete diagnostic lines. It adds a compact four-plane summary and a visible plane label on each diagnostic without introducing a score.

## Compatibility

- `valid` remains equivalent to `errors` being empty.
- Exit code remains zero only when no validation error exists.
- Diagnostic codes, paths, messages, and error/warning placement remain unchanged.
- Existing JSON consumers that ignore unknown fields continue to work.
- Deterministic ordering remains based on stable diagnostic content and must not depend on hash or filesystem order.

## Distribution boundary

The implementation updates the canonical standard validator and the self-hosted managed copy through the supported transaction. Focused policy documentation may define the plane names concisely, but no second detailed rule catalog is introduced. Package and fresh-install tests prove that distributed repositories receive the same taxonomy behavior.

## Explicit exclusions

Validation profiles; `inspect` or other new commands; pending, orphan, aging, or maintenance heuristics; policy-schema redesign; evaluator identity; self-hosting governor reconciliation; dashboard redesign; rule additions or removals; severity changes; aggregate scores; lifecycle transitions; commits, pushes, releases, tags, publication, or deployment.
