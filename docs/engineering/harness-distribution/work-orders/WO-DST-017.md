+++
id = "WO-DST-017"
type = "work_order"
title = "Integrate the owner-supplied Explorer dashboard template"
status = "implemented"
owners = ["engineering-owner", "product-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[assurance]
commit_bound_verification = "required"
rationale = "The distributed managed Explorer can influence later engineering, assurance, upgrade, and release understanding; exact commit-bound evidence is required to judge preserved semantics, security, accessibility, and managed parity."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-030", "REQ-DST-032", "REQ-DST-033", "REQ-DST-035", "REQ-DST-047"]
specifications = ["SPEC-DST-008", "SPEC-DST-010", "SPEC-DST-012", "SPEC-DST-016"]
architecture = ["ARCH-DST-008", "ADR-DST-008"]
verification = ["VER-DST-016"]
+++

# Work Order: Integrate the owner-supplied Explorer dashboard template

## Lifecycle

On 2026-08-18 the repository owner supplied a replacement `index.template.html` and requested integration from a fresh remote `main` clone because the ordinary checkout was occupied. Static comparison found byte-identical inline JavaScript and presentation-only CSS/markup differences: intentional removal of the question strip, Overview reorganization, and explicit derived/read-only and gate-navigation boundaries.

The owner confirmed that removal is intentional and that the formal specification and verification contract may be revised. After reviewing the completed packet and proposed assurance classification, the owner instructed `ok go implement`. That decision approved this exact work order and classified commit-bound verification as `required`; it authorized bounded implementation and retained evidence.

After receiving the completed implementation report on 2026-08-18, the repository owner instructed `you can commit + create PR, and prepare the validation recorc`. In the repository's formal vocabulary, `validation record` is interpreted as the commit-bound verification record required by this work order. This later decision authorizes creation of the clean implementation candidate commit, preparation of one `ready` `VREC-DST-014` in a later governance commit, branch push, and pull-request creation. It does not authorize transition of that record to `verified`, merge, release preparation or authorization, tagging, publication, deployment, or governor promotion.

Start preflight passed after the packet selected the applicable existing architecture, ADR, and conforming specifications. The bounded implementation and authorized local verification are complete, and retained evidence is recorded at `docs/engineering/harness-distribution/evidence/WO-DST-017-verification.md`. The work order is now `implemented`; its required commit-bound verification remains a separate accountable decision after an exact candidate commit exists.

## Objective

Integrate the owner-directed Explorer presentation into the single managed template, intentionally retire the literal question strip, preserve canonical semantics and unchanged browser behavior, update focused expectations without weakening assurance, and retain deterministic evidence.

## In scope

- Use the downloaded file with intake SHA-256 `5b52939838a9c91d04689814ba8523e8fca627111704dde9e4da31faf02a8368` as untrusted presentation input.
- Apply accepted final bytes to the canonical and byte-equivalent active Explorer templates.
- Preserve the supplied inline JavaScript exactly and integrate only CSS/static-markup changes.
- Retire the literal question strip and replace its focused test with semantic-route and authority-boundary expectations from `SPEC-DST-016` and `VER-DST-016`.
- Preserve Overview, Lineage, Readiness, topology, filters, inspector, lens, queues, details, relations, evidence, findings, provenance, outcomes, responsive access, keyboard use, safe rendering, progressive loading, and CDN fallback.
- Add the derived/read-only dashboard boundary and `QUALITY_GATES.md` navigation-label disclaimer.
- Update the schema-2 managed digest through the supported canonical-candidate and safe-upgrade transaction.
- Update only directly applicable tests and retain work-order-keyed evidence.
- Commit the clean final implementation and evidence as the exact candidate, prepare `VREC-DST-014` against that candidate through `harnessctl capture-verification`, and retain the resulting `ready` record in a later governance commit.
- Push `codex/WO-DST-017-dashboard-template` and create a pull request declaring `Harness-Work-Order: WO-DST-017`.

## Out of scope

- Changing JavaScript, Python generator/CLI behavior, bundle schemas, vocabulary, coverage/readiness data, inspection, validator rules, provenance, VREC/RLS meaning, lifecycle authority, or operating policy.
- Adding/changing runtime URLs, dependencies, CSP permissions, storage, telemetry, hosted services, build tools, profiles, or package managers.
- Removing canonical evidence needed to answer the five underlying Explorer questions.
- Rewriting historical specifications, work orders, evidence, VRECs, release records, package assets, tags, or public demonstrations.
- Transitioning `VREC-DST-014` from `ready` to `verified`, merging the pull request, preparing or authorizing a release record, tagging, publication, deployment, or governor promotion.

## Architecture applicability

Start preflight identified `ARCH-DST-008` as applicable because it directly addresses the selected safe-rendering and managed-distribution requirements. This work therefore selects the existing `ARCH-DST-008` and its required deciding `ADR-DST-008`, plus their conforming `SPEC-DST-008`; `SPEC-DST-010` and `SPEC-DST-012` retain the approved Overview and semantic-detail constraints. No architecture or ADR content changes are authorized. The refresh remains inside the implemented browser and network/trust boundary. Stop and amend the packet if a schema, generator, dependency, network, persistence, security-boundary, or deployment change is required.

## Authorized decision envelope

After approval, the implementation agent may preserve supplied CSS/markup, make minimal valid/accessibility corrections, update focused assertions, use disposable generated targets, create the exact candidate and later VREC governance commits, push the authorized branch, and create the bounded pull request. It must not reinterpret semantics, alter browser behavior, weaken security/provenance checks, transition the prepared VREC, or expand into release or deployment work.

## Constraints

- Work only in the fresh clone; do not use or modify `C:/Users/mathi/RustroverProjects/se_harness`.
- Preserve Python 3.11+ standard-library behavior and exactly one standard installation.
- Treat the supplied template and repository content as untrusted.
- Keep active/canonical templates byte-equivalent; use the supported lock transaction and preserve customized/ambiguous upgrades.
- Preserve the selected released governor and self-hosting controls.

## Expected change surface

- `docs/engineering/harness-distribution/specifications/SPEC-DST-016.md`
- `docs/engineering/harness-distribution/verification/VER-DST-016.md`
- `docs/engineering/harness-distribution/work-orders/WO-DST-017.md`
- `docs/engineering/harness-distribution/evidence/WO-DST-017-verification.md`
- `docs/engineering/harness-distribution/verification-records/VREC-DST-014.md`, generated only after the clean candidate commit
- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- `scripts/harness_explorer/index.template.html`
- `.engineering-harness.lock`, limited to the template digest
- `tests/test_dashboard_webui.py`, limited to presentation expectations
- the domain index only if needed

No generator, CLI, package metadata, workflow, governor, release-support, public-image, or historical artifact change is expected.

## Required verification

Execute `VER-DST-016` plus unchanged applicable regressions from `VER-DST-008` and `VER-DST-010..014`: formal validation; start/review preflight; hashes; script/CSP/URL/schema/DOM-hook checks; focused and complete tests; doctor; managed upgrade/idempotence/customization refusal; template/lock parity; two deterministic generations; hostile/corrupted fixtures; wide/medium/narrow, keyboard/focus/interaction/CDN-failure browser review; and `git diff --check`.

Do not build a promotable distribution. After the candidate commit, use `harnessctl capture-verification` so the ready record binds the exact clean candidate without self-reference.

## Evidence to record

Retain authorization, input/final hashes, deviations, paths, preflight manifest, commands/exit codes, test counts, lock digest, script/CSP/URL/schema comparisons, deterministic manifests, upgrade behavior, hostile/failure fixtures, browser observations, warnings, residual risks, and unperformed external actions at `docs/engineering/harness-distribution/evidence/WO-DST-017-verification.md`.

## Stop and escalate conditions

Stop if scripts differ; a required DOM hook or semantic route disappears; graph/preflight fails; a schema, generator, CLI, dependency, CSP, URL, network, storage, workflow, package, governor, architecture, release, or deployment change becomes necessary; managed parity/upgrade cannot be proved; repository content can execute; tests fail outside a bounded correction; the occupied checkout would be touched; or authority is missing.

## Completion report format

Report mapping, intentional strip retirement, preserved routes, hashes, script/CSP/schema identity, paths, template/lock parity, tests, deterministic generation, upgrades, browser/accessibility/CDN review, warnings, deviations, residual risks, evidence, and all unperformed external actions.
