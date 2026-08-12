+++
id = "WO-IAR-005"
type = "work_order"
title = "Implement typed architecture traceability"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-IAR-013"]
specifications = ["SPEC-IAR-005"]
architecture = ["ARCH-IAR-005", "ADR-IAR-005"]
verification = ["VER-IAR-005"]
+++

# Work Order: Implement typed architecture traceability

## Lifecycle

The repository owner approved the complete packet before execution. Implementation progresses through `in_progress` and stops at `implemented` after retained evidence. Commit, push, pull-request creation, verification capture or transition, release, tag, publication, and deployment require separate authority.

## Authorization

The repository owner approved `REQ-IAR-013`, `SPEC-IAR-005`, `ARCH-IAR-005`, `ADR-IAR-005`, `VER-IAR-005`, and this bounded work order on 2026-08-12 with the instruction `ok for implementation`. This authorizes implementation and retained evidence only; it does not authorize commit, push, pull-request creation, verification capture or transition, release, tag, publication, or deployment.

## Objective

Replace ambiguous new-use architecture traceability with typed requirement-driver and specification-conformance relations, update readiness and visualization consistently, and preserve historical repositories through explicit no-rewrite compatibility.

## In scope

- Add `architecture.addresses -> requirement` and `architecture.conforms_to -> specification` contracts.
- Add target-type and triangle-coherence validation with deterministic diagnostics.
- Replace all-requirement architecture coverage in preflight with typed specification relevance and explicit architecture applicability.
- Preserve the existing decision-assessment and conditional ADR model.
- Add direct and derived relation states and anomalies to Harness Explorer.
- Update canonical architecture/work-order templates and focused traceability/quality policy.
- Implement completed-legacy and consistent dual-declaration compatibility without owner-artifact rewrites.
- Update candidate tests/checks, run the supported transactional self-upgrade, regenerate the lock, and retain evidence.

## Out of scope

Natural-language inference of architectural significance; automatic artifact migration; removal of the compatibility window; changes to product intent, VREC/RLS provenance, release behavior, or publication; a one-architecture-per-requirement quota; closing the entire extensible relation namespace; commits; pushes; PRs; verification transitions; releases; tags; publication; and deployment.

## Authorized decision envelope

If approved, implementation may choose stable diagnostic codes, internal type-registry design, derived-edge naming, and Explorer styling. It may not remove direct requirement traceability, force architecture coverage on every routine requirement, treat transitive edges as authority, infer architectural significance, weaken ADR applicability, accept mixed legacy targets, or rewrite repository-owned artifacts automatically.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior.
- Treat repository content and relation metadata as untrusted.
- Keep canonical distribution files, operational copies, and the schema-2 lock consistent.
- Preserve owner content and fail transactionally on customized or ambiguous managed files.
- Preserve unrelated user changes and historical commit-bound records.

## Expected change surface

Formal validator and relation helpers; preflight coverage/applicability; dashboard generator and Explorer template; canonical architecture and work-order templates; traceability and quality-gate policy; self-hosted managed copies and lock; focused relation, preflight, dashboard, installer, integrity, security, instruction, and regression tests; instruction-architecture index/acceptance; and retained `WO-IAR-005` evidence.

## Implementation plan

1. Obtain accountable approval for `REQ-IAR-013`, `SPEC-IAR-005`, `ARCH-IAR-005`, `ADR-IAR-005`, `VER-IAR-005`, and this work order.
2. Run start preflight and read the complete governing manifest.
3. Add failing type, triangle, routine-requirement, applicability, migration, Explorer, and security tests.
4. Implement one shared typed-relation/compatibility model in validator and preflight.
5. Update Explorer direct/derived projections and focused managed authoring/policy content.
6. Apply the supported transactional self-upgrade, verify canonical/root/lock parity and idempotence, and confirm no owner artifact was migrated.
7. Execute `VER-IAR-005` on Python 3.11 and the local runtime, retain evidence, move implementation artifacts to `implemented`, and stop for separate commit authority.

## Required verification

Execute every case in `VER-IAR-005`, including wrong target types, coherent and incoherent triangles, routine requirements, work-order applicability, ADR regression, direct/derived graph authority, every legacy class, malicious inputs, transaction safety, managed parity, deterministic Explorer, candidate CI distinction, review preflight, dual-runtime full regression, and diff hygiene.

## Evidence to record

Commands and exit codes; runtimes and test counts; relation/triangle fixture matrix; diagnostics; work-order applicability cases; compatibility classifications; security inputs; CI assurance source; managed parity and no-write proof; Explorer states and snapshot hashes; changed paths; deviations; and residual risk.

## Stop and escalate conditions

Stop if the relation model loses the direct architectural driver, treats every requirement as architecturally significant, allows an addressed requirement outside conforming specifications, confuses derived and declared authority, weakens ADR coverage, requires automatic historical rewrites, accepts ambiguous legacy targets, mislabels independent assurance, encounters a required test failure, or needs authority beyond this work order.

## Completion report format

Report delivered relation semantics, applicability and migration behavior, diagnostics, changed components, verification results, evidence path, residual risks, lifecycle state, and explicitly unperformed actions.
