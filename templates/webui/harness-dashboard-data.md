# Harness Explorer data contract

`harness-lineage-prototype.html` is a static, generator-owned presentation of the existing deterministic `harness-dashboard-snapshot-v1` payload. It does not fetch data, define lifecycle authority, or persist a second WebUI model.

## Authoritative boundary

- The formal artifacts and validator remain authoritative for declared engineering state.
- `dashboard-data.json` is the canonical deterministic Explorer snapshot and is hashed by `capture-verification`.
- `generation-summary.json` contains non-canonical run observations such as generation time and elapsed time.
- The browser derives metrics, focused neighborhoods, stage groupings, and visual coordinates in memory only.
- The dashboard never turns derived observations into approval, verification, release, or an aggregate health score.

The generator replaces exactly one `__HARNESS_SNAPSHOT_JSON__` marker inside an inert JSON script element. Embedded JSON escapes `&`, `<`, `>`, U+2028, and U+2029 before the page is written.

## Canonical top-level sections

| Section | Meaning |
| --- | --- |
| `schema` | Must equal `harness-dashboard-snapshot-v1`. |
| `finding_rules_version` | Version of supported derived finding rules. |
| `quality_gates_version` | Version label for the G0-G5 observation model. |
| `repository` | Repository name, observed revision, artifact root, and validator validity. |
| `artifacts` | Normalized formal artifacts. Type and lifecycle remain explicit data. |
| `relations` | Declared and derived edges with direction, authority, target existence, and optional path. |
| `diagnostics` | Validator diagnostics. Errors are blocking observations. |
| `findings` | Rich validator and derived observations with artifacts, paths, evidence, and authority. |
| `coverage` | Active requirement definition coverage by specifications and verification contracts. This is not VREC assurance. |
| `readiness` | Per-work-order G0-G5 observations and exact condition states. |
| `revision_provenance` | Commit-bound VREC and release projections, checkout comparison, and supersession. |
| `revision_policy` | Configured verified-work and release provenance requirements. |
| `experiments` | Optional controlled-trial observations. |
| `evidence` | Work-order-keyed retained evidence paths. |

## UI mapping

The interface retains five explicit questions:

1. **Why does this exist?** uses `artifacts` and `relations` for bounded topology, lineage lanes, exact typed edges, and selected-artifact detail.
2. **Is the definition covered?** uses `coverage` and labels it as specification plus verification-contract coverage.
3. **What needs reassessment?** traverses declared resolvable relations inbound and outbound; a result means reassess, not automatically modify.
4. **What is inconsistent or unassessable?** uses `diagnostics`, `findings`, `readiness`, `revision_provenance`, and `revision_policy` without collapsing `not_assessable` into pass or fail.
5. **Does the harness help?** uses compatible retained `experiments`; absent measurements remain absent.

Overview, Lineage, and Readiness are permitted visual groupings, not alternative data contracts. All canonical fields remain inspectable even when a visual topology is bounded.

## Current artifact vocabulary

The current types are `intent`, `capability`, `requirement`, `specification`, `architecture`, `adr`, `work_order`, `verification`, `verification_record`, `release_contract`, `release_record`, and `operating_contract`. The UI must render unknown future types neutrally instead of dropping them.

## Safety and compatibility

Repository strings are untrusted and are escaped or assigned through text-safe DOM operations. The page sends no repository data to a network service. It loads the original 3D renderer only from the exact versioned unpkg URL recorded in `ADR-DST-008`; no remote font, image, style, hosted API, or telemetry is permitted. If that renderer is unavailable, embedded metrics, filters, focused lineage, definition coverage, readiness, findings, provenance, evidence, and experiments remain usable. Cycles and unusually large components use bounded focused traversal while exact lists remain available.

`harness-dashboard-data.schema.json` documents the canonical snapshot. It intentionally permits additional fields on extensible objects so a presentation can remain forward-tolerant without pretending unknown values have authority.
