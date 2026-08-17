+++
id = "SPEC-DST-012"
type = "specification"
title = "Safe content-rich Explorer artifact details"
status = "approved"
owners = ["technical-owner", "product-owner", "security-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-DST-042", "REQ-DST-043", "REQ-DST-044", "REQ-DST-045", "REQ-DST-046", "REQ-DST-047"]
+++

# Specification: Safe content-rich Explorer artifact details

## Scope and authority

Extend focused Lineage details with complete curated metadata, artifact Markdown bodies, non-authoritative EARS highlighting, fully navigable relation references, and retained evidence content. Preserve the canonical snapshot as the only persisted Explorer data boundary and preserve every formal artifact, relation, lifecycle, assurance, verification, and release authority.

The change is additive to `harness-dashboard-snapshot-v1`: existing fields keep their meaning and older consumers may ignore the optional content fields. Historical generated dashboards remain self-contained and unchanged.

## Content inputs and projection

1. Use the validator-parsed `Artifact.body` as the artifact-body source. Never reread front matter into the body or parse a second formal artifact model.
2. Preserve `created` and `updated` values already normalized in each artifact. Add no generation time to canonical snapshot data.
3. Add an optional `content` object to each normalized artifact with `format = "markdown"`, exact normalized body text, UTF-8 byte count, SHA-256, and an explicit included or omitted state.
4. Normalize body line endings to LF in the same deterministic parsing boundary used by the artifact model. Do not otherwise rewrite Markdown.
5. Preserve the existing top-level `evidence` entries and their `work_order` and `paths` fields unchanged. Add an optional top-level `evidence_documents` collection so document content is projected once without changing the meaning of existing path indexes.
6. Each unique evidence-document entry contains all explicit work-order and verification-record associations, the exact repository-relative path, format, UTF-8 byte count, SHA-256 when readable, included or omitted state, omission reason when applicable, LF-normalized projected Markdown when included, and generator-owned raw output path when included.
7. Work-order evidence is discovered only through the existing governed filename convention. Verification-record evidence is selected only from its explicit `evidence_paths`; duplicate paths are projected once and may have multiple artifact associations.
8. Resolve candidate evidence paths against the repository root and allowed `docs/engineering/**/evidence/` roots. Require a regular nonsymlink UTF-8 file whose final resolved location remains inside the allowed root.
9. Order artifact and evidence content records by canonical artifact ID and repository-relative path. Identical repository state produces byte-identical snapshot and raw content files.

## Deterministic capacity limits

10. Set the per-document UTF-8 projection limit to 262,144 bytes and the combined artifact-body plus evidence-content projection limit to 16,777,216 bytes.
11. Measure limits before embedding or writing raw copies. A document that exceeds its per-document limit is omitted as a whole.
12. Apply the total budget in deterministic artifact-ID/path order. Once the next document would exceed the total, omit that document and all later over-budget candidates individually with reason `total_content_budget_exceeded`.
13. Never truncate a document silently. Preserve path, observed size where available, digest where safely computed, and omission reason.
14. Add projected-document count, omitted-document count, and projected UTF-8 bytes to noncanonical generation summary data. Do not turn those counts into assurance or health scores.

## Safe Markdown contract

15. Render only from projected Markdown. The browser never fetches repository documents after generation.
16. Use locally distributed, pinned rendering and sanitization code. Do not use another CDN, hosted API, remote module, remote stylesheet, remote font, or runtime package fetch.
17. Disable raw HTML. Permit headings, paragraphs, emphasis, strong text, ordered and unordered lists, block quotes, horizontal rules, inline code, fenced code, tables, and links whose final scheme is explicitly allowed.
18. Allow only `http`, `https`, and generator-owned relative raw-content links. Add `rel="noopener noreferrer"` to external links and do not grant opener access.
19. Do not render remote or data-backed images, SVG, audio, video, iframe, object, embed, form controls, style, script, event handlers, custom elements, MathML, or artifact-provided IDs/classes.
20. Sanitize rendered output through an allowlist after Markdown parsing. Rendering failure falls back to escaped plain text and a visible notice.
21. Keep heading levels inside the detail panel's document outline. Do not allow body headings to replace page or selected-artifact headings.
22. Render code and all repository-derived strings inertly. Highlighting libraries, if any, must be locally distributed and may not execute a language payload.

## Overview detail behavior

23. Render the detail heading as `${id} - ${title}` using exact canonical values.
24. Show a curated metadata definition list with ID, type, lifecycle state, assurance signal, owners, created, updated, source path, and applicable type-specific projected fields.
25. Type-specific fields include requirement verification method; architecture decision-assessment summary; verification-record commit, object format, worktree state, verification time, snapshot hash, and supersession fields; and release-record commit, object format, version, tag, release time, and authority fields when present.
26. Do not repeat the complete relation set in Overview or show arbitrary raw TOML. Missing applicable values use `Unavailable`; irrelevant type-specific fields are omitted.
27. Render the artifact body after metadata. Empty bodies use a concise `No artifact body retained` state.
28. For requirements, render specification coverage and verification-contract coverage as separate named metadata fields. For nonrequirements, omit definition coverage.

## EARS statement highlighting

29. Render a requirement's exact `statement` in a dedicated EARS region before its body.
30. Use a deterministic local tokenizer, not Prism or another network dependency, to identify case-insensitive `WHERE`, `WHILE`, `WHEN`, `IF`, optional `THEN`, subject/system, `SHALL`, and response segments.
31. Keep one exact accessible statement string. Token spans may change visual presentation only and may not alter, normalize, autocorrect, validate, or persist the statement.
32. Associate each recognized segment with a textual clause name and stable visual token. Provide a concise legend or accessible description so meaning does not depend on color.
33. If a complete deterministic segmentation is unavailable, retain recognized prefix tokens only when boundaries are unambiguous and mark the remaining exact text `unclassified`. Do not emit a validator finding.
34. Bound tokenizer work linearly by statement length and render all token text through safe text construction.

## Semantic labels

35. Replace the unnamed header coverage badge with three independently named labels: `Type`, `State`, and `Assurance`.
36. Type and state values remain exact canonical strings with human-readable spacing only in the visible label; accessible text retains the dimension and value.
37. Use the existing assurance derivation with exactly `assured`, `decision_required`, `attention`, and `not_assessed`. A ready artifact remains `decision_required`.
38. State explicitly in accessible context that assurance is a non-authoritative derived Explorer signal.
39. Assign stable distinct visual tokens to the three dimensions and current values, but keep text, border, shape, or prefix cues so color is supplementary.
40. Unknown values retain exact text and a deterministic neutral fallback style.

## Relation navigation

41. In the Relations tab, render every resolved source, target, and `via` artifact reference as a native button or equivalent keyboard-operable control with the exact ID.
42. Render the exact relation name, source-to-target arrow, declared or derived authority, resolution state, and via path without reversal or renaming.
43. Activating a different resolved artifact invokes `visitLineage(id)` or its single equivalent, rerenders the board/detail, restores selected-card focus, and applies the 20-entry history branch/bound/reveal rules.
44. Activating the current artifact changes nothing and creates no history duplicate.
45. An unresolved ID remains visible text marked `Missing target` and has no focus action. Self, parallel, reverse, and repeated relations remain independently readable.

## Evidence detail and raw output

46. Map projected work-order and verification-record evidence documents to the focused node without implying that other artifact types inherit that evidence.
47. Render every evidence record with exact path, byte count, SHA-256 when available, included/omitted state, and explicit artifact association.
48. Render included Markdown under an individually labeled collapsible section. The path and metadata remain visible without expanding content.
49. Write each included raw document to `content/<sha256>.txt` inside the transactional dashboard output so static hosts serve passive text. Identical content may share one raw file.
50. Construct raw output names from the computed lowercase SHA-256 only. Never use an artifact ID or repository path as an output filename.
51. Use safe relative `content/<sha256>.txt` links with no target-origin inference. Serve raw content as passive text; it is never inserted as active HTML.
52. Extend transactional output writing to create only validated relative parents below the temporary output root, reject collisions with different content, verify the complete expected file set recursively, and retain rollback behavior.
53. If raw output cannot be written and verified, fail dashboard generation rather than publishing a detail link to incomplete content.
54. The Evidence tab states that presence is retained material, not sufficiency, approval, verification, or release authority.

## Publication and privacy boundary

55. Local `harnessctl dashboard` generation reads and writes only local repository/output content and performs no publication or transmission.
56. The generated Overview or snapshot information states that the bundle includes repository artifact/evidence content when projected documents are present.
57. Documentation for the Pages demonstrator states that publishing a generated bundle exposes every included body and raw evidence document. The existing explicit publication action remains the authority boundary.
58. Do not implement secret scanning, automatic redaction, remote content checks, or implicit publication under this work order. A repository owner must keep sensitive material out of a bundle selected for publication.

## Compatibility and distribution

59. Retain `schema = "harness-dashboard-snapshot-v1"` and every existing field. New artifact `content`, top-level `evidence_documents`, and generation-summary counts are optional additive fields.
60. A current Explorer renders missing optional content fields as unavailable and remains compatible with older v1 snapshots. Historical HTML remains unchanged.
61. Preserve the exact accepted `3d-force-graph@1.79.0` URL as the only runtime network exception. Markdown, EARS, relations, evidence, Readiness, and provenance remain usable when it fails.
62. The canonical generator/template and active managed copies remain byte-equivalent after the supported upgrade transaction, and applicable schema-2 lock digests are updated without changing protected governor controls.
63. Update package data and tests if locally distributed rendering/sanitization assets are added. Fresh installations, adoption, doctor, upgrade, and `harnessctl dashboard` must receive the same content behavior.
64. Preserve validation, inspection, preflight, VREC, RLS, release, package publication, and Pages authority semantics.

## Architecture applicability

`REQ-DST-043` and `REQ-DST-046` materially change projected data ownership, active-content handling, static output contents, public exposure, capacity limits, and rendering dependency policy. `ARCH-DST-009` addresses those significant drivers and conforms to this specification. `ADR-DST-009` decides the bounded local content-pipeline strategy. The remaining requirements are presentation behavior governed by the same specification but do not require nominal architecture edges.

## Explicitly unspecified decisions

The implementation agent may choose the locally packaged Markdown parser/sanitizer combination, exact safe CSS, label order, metadata column count, collapsible evidence default, clause colors, and plain-text fallback wording within this contract. Stop if the chosen renderer requires a runtime network request, weakens the standard-library packaging baseline without explicit dependency review, cannot enforce the allowlist, changes formal validation, or requires a breaking snapshot field change.
