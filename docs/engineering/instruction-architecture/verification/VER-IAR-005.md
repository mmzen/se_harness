+++
id = "VER-IAR-005"
type = "verification"
title = "Verify typed architecture traceability and compatibility"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-IAR-013"]
+++

# Verification Contract: Verify typed architecture traceability and compatibility

## Independence

Verification derives expected graph states from the approved relation semantics rather than implementation helpers. Automated checks validate types, direct declarations, and deterministic projections; manual review separately assesses whether the model preserves meaningful architecture rationale without creating nominal traceability.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-IAR-013` | relation matrix | `addresses`, `conforms_to`, and compatibility `constrains` targets | Correct target types pass; wrong, missing, duplicate, unknown, and mixed targets have stable diagnostics. |
| `REQ-IAR-013` | triangle property tests | one/many requirements and specifications | Every addressed requirement is specified by a conforming specification; extra routine requirements remain permitted. |
| `REQ-IAR-013` | preflight graph tests | routine and architecturally significant work-order requirements | G1 remains complete; applicable architectures are selected; routine requirements do not require fabricated architecture coverage. |
| `REQ-IAR-013` | migration matrix | completed, ongoing, dual-declared, and ambiguous legacy architecture | Compatibility follows the exact status/type rules, warns visibly, fails ambiguity, and never writes owner artifacts. |
| `REQ-IAR-013` | Explorer inspection | direct, transitive, missing, and legacy states | Declared and derived edges remain distinguishable and unresolved states appear as anomalies. |

## Acceptance scenarios

- A requirement driver and its detailed specification form a coherent typed triangle with architecture.
- A conforming specification includes routine requirements that do not appear in `addresses` and the graph remains valid.
- An addressed requirement absent from all conforming specifications fails.
- A work order selecting a requirement addressed by active architecture cannot omit that architecture.
- A selected architecture unrelated to selected specifications fails relevance checks.
- Conditional ADR applicability remains enforced after the relation-model change.
- Historical requirement-target and specification-target `constrains` forms remain readable with distinct advisories; mixed forms fail.

## Property and invariant tests

- Target type is resolved from artifact metadata, not an ID prefix.
- `addresses` is a subset of requirements specified through `conforms_to` for active typed architecture.
- Multiple conforming specifications may jointly cover addressed requirements.
- The transitive set may strictly contain the addressed set.
- Reordering relations or artifacts does not change diagnostics or dashboard snapshots.
- Direct edges retain declared authority; derived edges never do.
- The existing verification-record `conforms_to` behavior remains unchanged.

## Static and architecture checks

- Inspect architecture and work-order templates, `TRACEABILITY.md`, `QUALITY_GATES.md`, and focused workflow wording if needed.
- Test validator, preflight text/JSON, candidate CI behavior, Explorer snapshot/schema/view, CLI help, doctor, and supported self-upgrade.
- Confirm canonical templates and self-hosted copies are byte-identical and schema-2 lock entries match.
- Confirm no unrelated relation type or historical provenance contract changes.

## Security and resilience checks

Exercise non-string arrays, duplicate and oversized values, unknown IDs, deceptive prefixes, Unicode, injection-shaped relation content, malformed TOML, large graphs, cycles, customized managed files, and upgrade interruption/no-partial-write behavior. No artifact value may be executed or shell-interpolated.

## Full regression

Run focused relation, preflight, dashboard, authoring, installation, integrity, ADR-applicability, and provenance tests plus the complete unit suite on Python 3.11 and the local supported runtime.

## Manual assessments

- Confirm direct requirement rationale remains visible.
- Confirm specification conformance is not treated as proof of implementation satisfaction.
- Confirm architecture is not forced onto every routine requirement.
- Confirm compatibility observations do not invent architectural significance or migration authority.
- Confirm the router remains concise and delegates relation procedure to traceability policy.

## Evidence retention

Retain exact commands, runtimes, fixture matrices, diagnostic codes, direct/derived Explorer states, compatibility classifications, CI assurance source, transactional-upgrade outcomes, changed paths, deviations, and residual risks under `WO-IAR-005`.

## Residual uncertainty

Typed relations cannot prove that an author identified every architecturally significant requirement. Accountable technical review must challenge suspicious omissions using the architecture content, specifications, requirements, and candidate diff.
