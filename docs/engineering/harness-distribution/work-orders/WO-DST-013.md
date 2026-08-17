+++
id = "WO-DST-013"
type = "work_order"
title = "Enrich Explorer artifact details safely"
status = "implemented"
owners = ["engineering-owner", "product-owner", "security-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the canonical dashboard payload, untrusted Markdown and evidence handling, generated output contents, public disclosure boundary, security-critical path containment and sanitization, managed distribution, and human interpretation of relations and assurance signals; future review and publication decisions require exact-commit evidence."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-042", "REQ-DST-043", "REQ-DST-044", "REQ-DST-045", "REQ-DST-046", "REQ-DST-047"]
specifications = ["SPEC-DST-012"]
verification = ["VER-DST-012"]
architecture = ["ARCH-DST-009", "ADR-DST-009"]
+++

# Work Order: Enrich Explorer artifact details safely

## Lifecycle

On 2026-08-16 the repository owner reviewed and accepted the challenged proposal for a richer Lineage detail panel, including curated dates and metadata, safe artifact/evidence Markdown, non-authoritative EARS highlighting, relation-driven history navigation, exact ID-title headings, and separate type/state/assurance labels. The owner then explicitly authorized creation of this separate artifact packet with `ok go, you can create the artifact packet`.

Packet creation did not itself approve the definitions or authorize implementation. The repository owner subsequently directed `go implementation` on 2026-08-16, accepting `REQ-DST-042..047`, `SPEC-DST-012`, `ARCH-DST-009`, `ADR-DST-009`, `VER-DST-012`, and this bounded work order. `WO-DST-012` remains a separate implemented candidate transaction. This work order is now `in_progress`; commit, assurance, release, publication, and deployment remain separate decisions.

During implementation, the existing repository-specific Pages packager was found to enforce a three-file flat allowlist. Because the approved specification requires the existing explicit publication action to expose only snapshot-declared digest-named raw evidence, leaving that boundary unchanged would make every future publication fail closed after successful generation. The bounded correction extends the same packager to verify and copy only exact `content/<sha256>.txt` files declared by the snapshot; it creates no new trigger, action, authority, or deployment. The canonical and active implementation, publication compatibility, focused and complete tests, deterministic generation, managed integrity, and desktop/narrow browser review are complete. `ARCH-DST-009` and this work order are therefore `implemented`; commit-bound verification remains required and no assurance or publication transition is inferred.

## Objective

Make the focused Lineage detail panel a safe, portable place to understand a formal artifact and its retained evidence while preserving canonical semantics, reversible navigation, deterministic generation, and explicit assurance/publication boundaries.

## In scope

- Add deterministic optional artifact-body and evidence-document content to the existing canonical snapshot contract.
- Present exact ID-title headings, dates, curated common and type-specific metadata, and separately named type/state/assurance labels.
- Move requirement definition coverage into explicitly named Overview fields and remove the ambiguous header coverage badge.
- Render artifact and evidence Markdown through a local allowlisted parser/sanitizer boundary with escaped fallback, explicit omissions, and no new runtime URL.
- Add deterministic, non-authoritative, accessible EARS clause highlighting for requirement statements.
- Make every resolved relation artifact reference navigate through the existing 20-visit Lineage history semantics.
- Generate digest-named portable raw evidence files with bounded, contained, transactionally verified output.
- Add content/publication disclosure and update directly applicable Explorer/distribution documentation.
- Reconcile canonical and active managed copies and retain verification evidence keyed to `WO-DST-013`.

## Out of scope

- Changing artifact schemas, formal Markdown files, relation direction/authority, lifecycle transitions, validation rules, inspection recommendations, quality gates, VREC/RLS eligibility, release policy, or aggregate scoring.
- Treating EARS highlighting as validation or autocorrecting a requirement statement.
- Rich editing, comments, artifact mutation, repository writes, browser-history persistence, server-side search, hosted content services, authentication, telemetry, analytics, secret scanning, or automatic redaction.
- Inferring vendor-specific GitHub/GitLab source URLs or publishing a dashboard automatically.
- Changing the accepted Overview `3d-force-graph@1.79.0` URL, its risk, or the Overview/Lineage/Readiness information architecture beyond the detail panel.
- Committing, preparing or transitioning a VREC, opening a pull request, releasing, publishing a package, or deploying the public demonstrator without later explicit authority.

## Authorized decision envelope after approval

The implementation agent may choose the concrete locally packaged Markdown parser/sanitizer after dependency, license, security, package, deterministic-output, and consumer-install checks; safe CSS and clause colors; metadata layout; evidence expansion default; exact omission/fallback wording; and internal helper structure. It must preserve the specified content fields, limits, associations, allowlist, no-network rule, EARS non-authority, assurance vocabulary, history path, raw naming, deterministic behavior, and explicit publication boundary.

If an acceptable renderer requires a new Python or local browser dependency, update package metadata and record the dependency review. Do not invent a full unsafe Markdown parser merely to avoid a reviewed dependency. Stop if no candidate can satisfy both rendering and distribution constraints.

## Constraints

- Preserve Python 3.11+ compatibility, deterministic LF serialization, transactional generation, and target-local `harnessctl dashboard` ownership.
- Treat every repository string, Markdown document, URL, path, and evidence byte as untrusted.
- Preserve additive v1 compatibility and existing field meanings.
- Keep current canonical generator/template and active managed copies byte-equivalent through supported reconciliation.
- Preserve protected self-hosting governor controls, unrelated work, historical generated dashboards, and current public release payloads.
- No publication or external transmission is authorized by implementation.

## Expected change surface

- canonical and active `scripts/generate_harness_dashboard.py`
- canonical and active `scripts/harness_explorer/index.template.html`
- repository-specific `.github/scripts/publish_dashboard.py` compatibility for snapshot-declared raw evidence only
- locally distributed renderer/sanitizer assets and package metadata only if the approved implementation requires them
- `.engineering-harness.lock` entries produced by the supported managed transaction
- focused generator, security, distribution, package, and WebUI tests
- DST-013 definitions, domain index, retained evidence, and directly applicable Explorer/publication documentation

No validator, inspector, preflight, workflow, VREC/RLS command, release automation, or public deployment mutation is expected. Stop if implementation demonstrates otherwise.

## Required verification

Execute every applicable case in `VER-DST-012` plus relevant regressions from `VER-DST-008`, `VER-DST-010`, and `VER-DST-011`. At minimum verify formal graph validity; phase-appropriate preflight; additive snapshot compatibility; exact bodies/dates/type-specific fields; Markdown allowlist and hostile fallback; all EARS families and ambiguity; source/target/via relation navigation with 20-entry history; evidence association, path/symlink containment, hashes, raw links, budgets, recursive transactions and rollback; four assurance signals and named requirement coverage; no new runtime URL; CSP/network behavior; deterministic double generation; managed upgrade plan/apply/idempotence; canonical/active/lock parity; dependency/package/wheel/sdist/fresh-install behavior when applicable; browser desktop/narrow/accessibility/focus review; full tests; doctor; inspect; and `git diff --check`.

## Evidence to record

Retain the exact accepted dependency and license review; commands and exit codes; test counts; artifact/evidence fixture paths, bytes, hashes and associations; snapshot and raw tree manifests; budget selection/omissions; hostile Markdown/URL/path/symlink results; EARS tokens/fallback; relation-history transitions; label/coverage state table; observed network requests; transactional rollback; deterministic digests; active/canonical/lock hashes; package/consumer parity; browser and accessibility observations; disclosure text; changed paths; deviations; residual risks; and deployment status in `docs/engineering/harness-distribution/evidence/WO-DST-013-verification.md`.

## Stop and escalate conditions

Stop if implementation requires a breaking snapshot change; another runtime URL; unsanitized HTML; arbitrary repository reads; silent truncation; nondeterministic selection; unsafe or incomplete raw output; vendor-only source links; assurance inference; validation/lifecycle change; a new publication action; an unreviewed dependency or incompatible license; protected-control changes; loss of managed parity; failing tests; or any commit, VREC, PR, release, publication, or deployment action without explicit authority.

## Completion report format

Report requirement and architecture mapping; content projection and limits; renderer/sanitizer/dependency decision; metadata/body/EARS/label behavior; relation-history behavior; evidence associations/raw output/security; deterministic snapshot/output hashes; managed/package/consumer parity; tests and browser review; disclosure boundary; changed paths; deviations; residual risks; and all external actions not performed.
