+++
id = "VER-DST-017"
type = "verification"
title = "Verify the owner-authorized Explorer dashboard revision"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
verifies = ["REQ-DST-030", "REQ-DST-032", "REQ-DST-033", "REQ-DST-035", "REQ-DST-040", "REQ-DST-041", "REQ-DST-042", "REQ-DST-045", "REQ-DST-047", "REQ-DST-050", "REQ-DST-055"]
+++

# Verification Contract: Verify the owner-authorized Explorer dashboard revision

## Independence

Verification derives expected semantics from the approved requirements, existing bundle and rendering specifications, trusted generator limits, and the explicit owner decisions recorded in `SPEC-DST-017`. The supplied HTML is untrusted implementation input, not its own acceptance authority.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-030`, `REQ-DST-047` | static and generated-data comparison | every artifact type, relation, gate state, finding, provenance and assurance label | exact canonical semantics remain distinguishable and no derived observation becomes authority |
| `REQ-DST-032`, `REQ-DST-042`, `REQ-DST-045` | adversarial fixtures and browser review | hostile strings, detail/relation navigation, desktop/mobile, keyboard, CDN failure | content remains inert and all evidence routes remain accessible without the optional 3D view |
| `REQ-DST-033` | package/template/lock/upgrade tests | source candidate, init/adopt target, safe upgrade and customized refusal | one byte-equivalent managed template is installed transactionally without overwriting customization |
| `REQ-DST-035`, `REQ-DST-040` | focused DOM and interaction checks | dense Overview, bounded Lineage depth, connector toggle and missing targets | bounded readable presentation retains exact artifact and relation meaning |
| `REQ-DST-041` | route and history-state browser model | fragments, Back/Forward, reload, malformed routes, 20/21 visits | supported route restores the intended current view while the visit trail remains bounded, new on reload, and non-authoritative |
| `REQ-DST-050` | progressive resource observation and failure injection | summary, topology, readiness, detail and evidence requests | only verified manifest-bound resources load on demand and panel failures remain contained |
| `REQ-DST-055` | deterministic UTF-8 size measurement | real repository and bounded fixtures | generated `index.html` is at most 262,144 bytes and all other existing budgets remain unchanged |

## Acceptance scenarios

- Confirm the revised attachment intake hash, record the separately authorized routing delta, and confirm byte-identical final canonical/active hashes.
- Generate the real repository twice and compare every canonical bundle path and byte; separately compare the noncanonical generation summaries after excluding documented timing fields.
- Exercise Overview filters, density cap, clear scope, inspector, Lineage history/connectors/details, Readiness gate rollups, subject listing, evidence filters, and retry controls.
- Navigate supported fragments directly and through browser Back/Forward; reload Lineage and prove the visit trail starts anew at the routed artifact.
- Exercise malformed, unknown, and encoded routes without external navigation or additional resource acquisition.
- Block the graph CDN and confirm non-3D evidence views remain usable.
- Review desktop, medium, and narrow layouts with keyboard-visible focus and accessible names.

## Property and invariant tests

- Exactly one bootstrap marker and two inline script elements remain.
- Bundle schemas, descriptor validation, same-origin checks, digests, and safe bootstrap escaping remain unchanged.
- Canonical and active templates are byte-equivalent; generator copies are equivalent under the schema-2 `utf8-text-lf-v1` managed representation.
- History routes never enter canonical snapshot data, formal artifacts, retained evidence, or generator output resources.
- Generated shell and summary remain at or below 262,144 UTF-8 bytes.

## Static and architecture checks

- `ARCH-DST-008`/`ADR-DST-008` continue to own the direct canonical-snapshot, managed WebUI and accepted CDN boundary through `SPEC-DST-008`.
- `ARCH-DST-010`/`ADR-DST-010` continue to own progressive integrity, static hosting and shell budgets through `SPEC-DST-013..014`.
- No schema, runtime dependency, workflow, publication, VREC/RLS, governor, or deployment change is introduced.

## Security and privacy checks

- Scan fragments, DOM construction, safe Markdown links, resource acquisition, CSP, URLs, storage, cookies, WebSocket/EventSource, telemetry, and repository-write surfaces.
- Distinguish the local `data-integrity` presentation attribute from forbidden unsupported Subresource Integrity claims on the dynamic graph script.
- Confirm only the accepted graph URL exists and receives no repository data.

## Performance and resilience checks

- Measure `index.html <= 262144`, summary `<= 262144`, topology target `<= 524288`, per-document `<= 262144`, and total projected content `<= 16777216` before compression.
- Repeat deterministic generation and transactional failure/rollback tests.
- Confirm the 20-entry Lineage history, 100-node context bounds, density cap, request cache and retry boundaries remain bounded.

## Manual assessments

Review desktop, medium and mobile visual hierarchy, overflow, touch targets, keyboard traversal, focus, non-color interpretation, Overview density, Lineage connectors/history, Readiness gate posture/listing, route reload, Back/Forward, CDN failure, and explicit non-authority language.

## Evidence retention

Retain authorization, attachment/final hashes and sizes, preflight manifest, changed paths, exact commands/exit codes, focused and full test counts, deterministic bundle manifests, size measurements, upgrade plans, customization refusal, doctor/validation results, route/state observations, browser screenshots/notes, deviations, residual risks, and all unperformed external actions under `docs/engineering/harness-distribution/evidence/WO-DST-018-verification.md`.

## Residual uncertainty

Fragments improve deep linking but expose current presentation selection in the URL and browser history. They do not authenticate the host, preserve prior visits, or make a view authoritative. Browser/layout differences and the accepted CDN supply-chain risk remain bounded through explicit fallbacks and retained evidence.
