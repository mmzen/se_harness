# Implementation Evidence for WO-DST-013

## Scope and authority

The repository owner approved `REQ-DST-042..047`, `SPEC-DST-012`, `ARCH-DST-009`, `ADR-DST-009`, `VER-DST-012`, and `WO-DST-013`, then explicitly authorized implementation with `go implementation` on 2026-08-16. This record retains implementation and test evidence only. It does not approve or verify the candidate, transition a VREC, authorize a release, commit, push, open or merge a pull request, publish a package, publish the public demonstrator, or deploy content.

`WO-DST-012` remains separate implemented work in the same uncommitted candidate. Its retained evidence is `WO-DST-012-verification.md`.

## Implemented behavior

| Requirement | Retained implementation result |
| --- | --- |
| `REQ-DST-042` | The Lineage detail heading is exact `ID - title`. Overview shows common dates and metadata plus requirement, architecture, work-order assurance, VREC, and RLS fields only where applicable. |
| `REQ-DST-043` | Every validator-parsed artifact body has an additive LF-normalized Markdown projection with byte count, SHA-256, and explicit included/omitted state. A bounded local Markdown subset is parsed from escaped input and passed through a DOM allowlist sanitizer; raw HTML, media, arbitrary attributes, and unsafe URLs are not emitted. |
| `REQ-DST-044` | Requirement statements retain one exact accessible string and receive local presentation-only EARS clause tokens. Ambiguous statements remain exact and unclassified; no validation result is created. |
| `REQ-DST-045` | Every resolved source, target, and derived `via` ID in Relations is a keyboard-operable artifact reference using the existing `visitLineage` path and 20-visit history semantics. Missing targets remain noninteractive text. |
| `REQ-DST-046` | Governed work-order and VREC evidence paths are deduplicated, safely resolved below evidence roots, bounded, hashed, rendered, and emitted as passive `content/<sha256>.txt`. The repository-specific Pages packager accepts only snapshot-declared raw files whose name, bytes, length, and digest match. |
| `REQ-DST-047` | The ambiguous coverage badge is removed. Type, State, and derived Assurance have separate named labels, accessible exact values, stable visual tokens, and non-color shapes/prefixes. Requirement definition coverage remains two explicit Overview fields. |

`ARCH-DST-009` is implemented by one-way parser-owned artifact bodies and governed evidence references flowing through a bounded deterministic projector, additive snapshot fields, transactional raw output, local rendering/sanitization, and read-only Lineage presentation. `ADR-DST-009` remains the accepted decision. Formal validation, lifecycle, relation authority, assurance, and publication authority are unchanged.

## Content, output, and dependency review

- Snapshot schema remains `harness-dashboard-snapshot-v1`; existing top-level `evidence` indexes are unchanged and optional `artifact.content` plus top-level `evidence_documents` are additive.
- Limits are 262,144 UTF-8 bytes per document and 16,777,216 projected UTF-8 bytes in deterministic artifact-ID then evidence-path order. Oversized and over-budget documents are omitted whole with explicit reasons.
- The first complete current-repository generation projected 491 documents: 416 artifact bodies plus 75 unique evidence documents, with zero omissions and 1,763,023 projected UTF-8 bytes.
- The same generation emitted 75 unique passive raw evidence files. Example: `WO-AGR-001-verification.md` projected 6,185 bytes with SHA-256 `716d5a9bde45134b0b40234a8f6740d1a366c6df3fdb7c98fe4fa46a3389c986`, served as `content/716d5a9bde45134b0b40234a8f6740d1a366c6df3fdb7c98fe4fa46a3389c986.txt`.
- Transactional writing now validates nested POSIX-relative names, containment, case-fold collisions, exact recursive output completeness, rollback, and safe cleanup.
- No package or browser dependency was added. The implementation uses a deliberately bounded local Markdown subset plus an explicit post-parse allowlist sanitizer, so there is no third-party dependency or license addition. The exact accepted `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` remains the sole runtime URL exception.
- Local dashboard generation performs no publication. Snapshot information and publication documentation state that sharing or publishing the bundle exposes all included artifact bodies, evidence bodies, and raw evidence; no secret scanning or redaction is claimed.

## Automated verification

| Check | Result |
| --- | --- |
| `harnessctl upgrade .` plan | PASS; only the active generator and Explorer template required reconciliation; protected governor files remained protected. |
| `harnessctl upgrade . --apply` | PASS; active managed copies and schema-2 lock digests updated transactionally. |
| post-apply `harnessctl upgrade .` | PASS; 32 unchanged managed files and no pending update. |
| focused `python -m unittest tests.test_dashboard_webui tests.test_dashboard_publication` | PASS; 34 tests. |
| complete `python -m unittest discover -s tests -p "test_*.py"` | PASS; 226 tests, 3 conditional skips. |
| `harnessctl validate .` | PASS; 416 artifacts, 0 errors, 42 pre-existing classified maintenance warnings. |
| `harnessctl doctor .` | PASS; canonical/active generator and template parity, managed lock integrity, protected self-hosting controls, and required files. Existing canonical-location advisories remain warnings. |
| JavaScript syntax compilation with bundled Node.js 24.19.0 | PASS. |
| `git diff --check` | PASS; no whitespace error. Git reported only the repository's configured future LF-to-CRLF checkout notices. |

Focused tests compare every projected artifact with validator-parsed `Artifact.body`; cover 0, 1, 262143, 262144, and 262145-byte boundaries; fill and cross the 16 MiB budget; exercise traversal, unsafe extension, missing, non-UTF-8, and available-symlink evidence; verify LF, length, hashes, associations, raw paths, nested output, case-fold collision, prior-output rollback, optional old-v1 content, and deterministic serialization. Publication tests prove declared raw copying and reject tampered content or undeclared files.

## Browser and accessibility review

The generated site was served from `http://127.0.0.1:8765/` and reviewed in the Codex in-app browser at the normal viewport and at 600 by 800 pixels.

- Explorer loaded 416 artifacts and 1,503 relations with the observed full revision retained and a 12-character presentation prefix.
- Requirement `REQ-AGR-001` displayed the exact heading, three named labels, dates, requirement metadata, two named definition-coverage fields, body, and exact EARS statement. Observed clauses were `trigger`, `subject`, `obligation`, and `response`; their concatenated text remained exact.
- Five incident relations exposed ten operable source/target references. Activating `OPS-AGR-001` changed the detail and appended exactly one history visit. Back/history navigation to `REQ-AGR-001` and then `WO-AGR-001` remained consistent.
- `WO-AGR-001` evidence displayed path, state, format, bytes, digest, four explicit artifact associations, passive raw link, collapsible rendered Markdown, and the non-authority notice. The raw URL returned HTTP 200 from the standalone local server.
- The evidence rendering contained no `script` or `img` elements. The browser console contained no warnings or errors.
- At 600 pixels, document width remained below viewport width, the detail panel and labels wrapped without horizontal page overflow, the evidence path remained readable, and mobile navigation remained usable.
- Type, State, and Assurance are independently announced. EARS has one exact screen-reader string, clause names, and a textual presentation-only explanation. Color remains supplementary.

Observed local HTTP requests were the generated root and one digest-named raw evidence file. The optional pinned 3D renderer retained its existing accepted CDN behavior; all Lineage details, Markdown, EARS, relations, evidence, readiness, and provenance remained local.

## Changed implementation surface

- canonical and active `scripts/generate_harness_dashboard.py`
- canonical and active `scripts/harness_explorer/index.template.html`
- `.engineering-harness.lock`
- repository-specific `.github/scripts/publish_dashboard.py`
- Explorer and publication focused tests
- `docs/notes/harnessctl-reference.md`
- `docs/notes/harness-dashboard-publication.md`
- DST-013 definitions, domain index, and this evidence

No validator, inspector, preflight, VREC/RLS command, release workflow trigger, Python package dependency, version, public site, external repository setting, or deployed artifact was changed.

## Deviations and residual risks

- The local renderer intentionally supports the allowlisted Markdown subset, not every CommonMark or repository extension. Unsupported syntax remains inert readable text.
- Natural-language EARS interpretation is deliberately bounded. Repeated or incomplete obligation structure falls back to unclassified exact text rather than guessing.
- Evidence content may contain sensitive material. The generator cannot prove absence of secrets; accountable owners must review the bundle before any separately authorized publication.
- The public Pages packager had to be updated because its prior flat three-file allowlist would reject the newly required raw evidence directory. The correction preserves the existing trigger and authority boundary and fails closed unless every raw file is declared and hash-consistent.
- The final deterministic snapshot hash is intentionally not embedded in this evidence body because this file itself is projected into that snapshot; the twice-generated final digest and output-tree comparison belong in the completion report and later commit-bound verification evidence.
- The 42 validation maintenance warnings and doctor canonical-location advisories predate this work and are not silently remediated here.
