+++
id = "WO-DST-018"
type = "work_order"
title = "Integrate the revised Explorer dashboard and authorized routing"
status = "implemented"
owners = ["engineering-owner", "product-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[assurance]
commit_bound_verification = "required"
rationale = "The managed Explorer, browser routing, formal requirements, verification contracts, and enforced payload budget influence later engineering, assurance, upgrade, and release understanding; exact commit-bound evidence is required before any verified claim."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-030", "REQ-DST-032", "REQ-DST-033", "REQ-DST-035", "REQ-DST-040", "REQ-DST-041", "REQ-DST-042", "REQ-DST-045", "REQ-DST-047", "REQ-DST-050", "REQ-DST-055"]
specifications = ["SPEC-DST-008", "SPEC-DST-010", "SPEC-DST-011", "SPEC-DST-012", "SPEC-DST-013", "SPEC-DST-014", "SPEC-DST-017"]
architecture = ["ARCH-DST-008", "ADR-DST-008", "ARCH-DST-010", "ADR-DST-010"]
verification = ["VER-DST-008", "VER-DST-010", "VER-DST-011", "VER-DST-012", "VER-DST-013", "VER-DST-014", "VER-DST-017"]
+++

# Work Order: Integrate the revised Explorer dashboard and authorized routing

## Lifecycle

On 2026-08-19 the repository owner supplied a slightly revised `index.template.html` and instructed `please integrate this one`. The owner explicitly authorized raising the Explorer shell limit to 256 KB and authorized URL fragments and browser history state. In the repository's binary size convention, this work records 256 KiB as 262,144 UTF-8 bytes. Browser verification then found that a fresh Lineage fragment was replaced before topology initialization and malformed percent encoding stopped initialization; after the agent described the two minimal corrections, the owner explicitly authorized them with `yes OK`. Those instructions approve this bounded work order and its prospective specification/verification revisions; they do not verify a candidate or authorize commit, push, pull request, merge, release, publication, deployment, or governor promotion.

Implementation completed on 2026-08-19 with retained evidence at `docs/engineering/harness-distribution/evidence/WO-DST-018-verification.md`. The `implemented` status records completion of the authorized work only; commit-bound verification remains required and no VREC, release, or external action is implied.

After implementation evidence and review preflight passed, the repository owner explicitly instructed `OK: commit the clean candidate under WO-DST-018.` This authorizes one local candidate commit containing the bounded work-order change set. It does not authorize push, pull-request mutation, VREC preparation or transition, tag, release, publication, or deployment.

## Objective

Integrate the exact revised dashboard into the single canonical managed Explorer, adopt the authorized 262,144-byte shell cap and controlled fragment/History API routing, preserve existing trust and authority boundaries, update focused assertions, and retain deterministic evidence.

## In scope

- Treat the supplied file with SHA-256 `6b6881a095fac417c358548342eb31737c58b9bf6345cf632b066f8aa53f470a` as untrusted exact-byte input.
- Begin from its unchanged bytes in the canonical template, then reconcile the final authorized revision and schema-2 lock through supported upgrade.
- Apply the separately authorized non-throwing route decoder and topology-before-Lineage-route rendering correction, then reconcile that final canonical revision through supported upgrade.
- Raise both canonical and active generator `MAX_INDEX_BYTES` values to 262,144.
- Revise `REQ-DST-041`, `REQ-DST-055`, `SPEC-DST-011`, `SPEC-DST-013`, `VER-DST-011`, and `VER-DST-013` only as needed to record the owner's routing and size decisions.
- Add `SPEC-DST-017`, `VER-DST-017`, this work order, and work-order-keyed evidence.
- Update focused WebUI tests for the new controls, authorized History API behavior, route safety, `data-integrity` selector, and size cap without weakening CSP, URL, schema, provenance, accessibility, or managed-distribution checks.
- Execute formal, unit, integrity, upgrade, deterministic-generation, route, responsive, keyboard, and CDN-failure verification available locally.

## Out of scope

- Editing the supplied template bytes beyond the two explicitly authorized routing corrections, changing bundle schemas, adding a runtime dependency or URL, changing resource descriptors, adding persistent browser storage, sending telemetry, or deriving repository paths from routes.
- Changing validator, inspection, readiness, evidence, VREC/RLS, publication, workflow, governor, release, or deployment semantics.
- Building a promotable distribution, committing, pushing, opening a pull request, transitioning verification/release state, publishing, or deploying.

## Authorized decision envelope

The implementation agent may update formal wording and focused test expectations, choose deterministic route-safety fixtures, run disposable local servers and browsers, use the supported managed upgrade transaction, and apply the explicitly authorized safe-decoding and Lineage-initialization corrections. It may not otherwise alter the supplied template, increase another limit, weaken a security assertion, or expand external actions without further owner permission.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and exactly one standard installation.
- Keep canonical/active templates byte-equivalent and generator copies equivalent under the schema-2 `utf8-text-lf-v1` managed representation.
- Preserve customized/ambiguous upgrade refusal and owner content outside managed markers.
- Preserve the exact released governor and all self-hosting controls.
- Treat repository content, fragments, manifests, resources, lock data, and the attachment as untrusted.

## Expected change surface

- Formal requirement/specification/verification/work-order/evidence artifacts for routing and shell capacity.
- Canonical and active Explorer templates and dashboard generators.
- The schema-2 managed lock entries produced by safe upgrade.
- Focused Explorer contract tests and the distribution-domain index.

## Required verification

Run start/review preflight; formal validation; focused and complete standard-library tests; doctor; release-distribution validation; exact attachment/template hashes; generator/template parity; deterministic double generation; 262,144-byte shell budget; bootstrap/schema/CSP/URL/storage scans; safe route and Back/Forward/reload checks; hostile route fixtures; managed upgrade plan/apply/idempotence/customization refusal; desktop/medium/mobile, keyboard/focus, progressive request, and CDN-failure review; and `git diff --check`.

## Evidence to record

Retain the authorization and 256 KiB interpretation, intake/final hashes and bytes, preflight manifest, formal graph result, changed files, lock digests, focused/full test counts, deterministic manifests, resource sizes, route/security scans, upgrade behavior, browser observations, deviations, residual risks, and unperformed external actions at `docs/engineering/harness-distribution/evidence/WO-DST-018-verification.md`.

## Stop and escalate conditions

Stop if another template edit is needed; another limit or schema must change; a new URL, dependency, storage mechanism, network request, workflow, architecture, governor, release, publication, or deployment change is needed; repository-derived values can execute or escape controlled routes; managed parity fails; tests require weakened assurance; or requested action exceeds this authority.

## Completion report format

Report authorization mapping, hashes, sizes, exact template preservation, route behavior, formal changes, generator/lock parity, tests, deterministic generation, upgrades, browser/accessibility/CDN review, warnings, deviations, residual risks, retained evidence, and every unperformed external action.
