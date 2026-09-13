+++
id = "SPEC-KIS-001"
type = "specification"
title = "Simpler checks for ordinary engineering work"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

contract = "An implementation must remove the accepted ordinary-work restrictions while retaining safe file operations, package integrity and explicit owner decisions."

[relations]
specifies = ["REQ-KIS-001", "REQ-KIS-002", "REQ-KIS-003", "REQ-KIS-004", "REQ-KIS-005", "REQ-KIS-006", "REQ-KIS-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "technical-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the technical-owner approval of SPEC-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Simpler checks for ordinary engineering work

## In plain words

Make ordinary work easy to run and easy to retry. Check real boundaries without preserving restrictions that have no useful job.

## Scope

All 38 accepted codebase candidates, delivered through seven work orders, with seven useful protections retained.

## Terms

- **Ordinary command:** local inspection or governed editing, without publication or a new installation.
- **Relevant inputs:** the tested code and the selected governing chain and declared dependencies.
- **Final candidate:** the exact integrated commit proposed for release.

## Rules

**KIS-CUT-001.** The PR selector MUST normalize LF and CRLF before parsing work-order declarations.

**KIS-CUT-002.** Owner-instruction length MUST be advisory, with managed-fragment preservation checked independently.

**KIS-CUT-003.** Scope checks MUST accept literal Git filenames and normalize native CLI separators while rejecting traversal and outside-root destinations.

**KIS-CUT-004.** The PR selector MUST accept one work order or an explicit list, checking changed paths against the union of approved scopes.

**KIS-CUT-005.** Local execution delegation MUST use the recorded owner approval of the selected scope without requiring that approval in the PR base.

**KIS-CUT-006.** Authorized local transitions MUST use relevant retained checks without requiring live GitHub access.

**KIS-CUT-007.** Handoff evidence MUST accept a simple work-order evidence reference without an exact four-field header at byte zero.

**KIS-CUT-008.** Evidence freshness MUST cover the tested candidate and relevant governing inputs, excluding unrelated artifact edits.

**KIS-CUT-009.** Verification preparation MUST consume selected structured data without generating the dashboard.

**KIS-CUT-010.** Verification capture MUST support an explicit committed candidate in a temporary worktree when the caller checkout contains unrelated files.

**KIS-CUT-011.** A selected-artifact check MUST return the next valid action without requiring the caller to supply an internal procedure name.

**KIS-CUT-012.** Preflight MUST separate selected-scope blockers from unrelated diagnostics while rejecting repository-wide identity ambiguity.

**KIS-CUT-013.** Each consuming format MUST validate its own checksum fields without a global suffix-based field census.

**KIS-CUT-014.** Integrity checks MUST assess effective attributes or consumed bytes without requiring attributes inside a designated text region.

**KIS-CUT-015.** Interpreter selection MUST allow ordinary linked environment directories while checking the effective interpreter and imported checker origin.

**KIS-CUT-016.** Ordinary runtime identity MUST report the Python version without hashing the Python executable.

**KIS-CUT-017.** Runtime identity MUST assess the effective import path without rejecting an ignored PYTHONPATH variable.

**KIS-CUT-018.** Identity checking MUST validate the invoked module or console route without requiring the unused route.

**KIS-CUT-019.** Ordinary commands MUST check checker origin and version, reserving full payload checks for installation, upgrade, release, doctor or explicit inspection.

**KIS-CUT-020.** Release preparation MUST accept a verified installed checker payload without requiring the original checker wheel archive receipt.

**KIS-CUT-021.** Internal evaluator evidence MUST hash validated canonical values, tolerate equivalent JSON whitespace, and reject duplicate keys or altered identity.

**KIS-CUT-022.** Installation MUST lock only machine policy and router fragments, leaving guidance, templates and owner settings editable through explicit keep-or-replace handling.

**KIS-CUT-023.** Release preparation MUST use one final-candidate verification covering the release scope, with earlier work records retained as historical inputs.

**KIS-CUT-024.** An explicit ready-record refresh MUST reuse evidence only when relevant candidate contents and governing inputs are unchanged.

**KIS-CUT-025.** Package acceptance MUST use a small disposable target and inspect the paths its operation can touch.

**KIS-CUT-026.** Deterministic build replay MUST run for build or publication input changes and actual release preparation, rather than every ordinary PR.

**KIS-CUT-027.** Requalification of an older release MUST run for publication-path changes or explicit release preparation, rather than every ordinary PR.

**KIS-CUT-028.** Unpublished draft publication MUST verify existing required assets and upload only missing assets while refusing conflicting required bytes.

**KIS-CUT-029.** Publication MUST validate the required asset subset while ignoring unrelated release attachments.

**KIS-CUT-030.** Release census MUST assist review without requiring commit-trailer exemptions to approve the final release scope.

**KIS-CUT-031.** New evidence MUST retain concise summaries and retrievable raw-result references; existing large bundles MUST receive an archival assessment without silent deletion.

**KIS-CUT-032.** Tests MUST verify public outcomes instead of internal call shapes or variable-name inventories, except a necessary packaging import boundary.

**KIS-CUT-033.** Text-integrity tests MUST use small LF/CRLF checks and supported-platform checkouts without aggressive Git garbage collection.

**KIS-CUT-034.** Runtime tests MUST cover supported installations, one unavailable-capability failure and actual escape paths instead of retired synthetic capability matrices.

**KIS-CUT-035.** Requirement approval MUST require a meaningful obligation and acceptance condition without requiring the literal keyword SHALL.

**KIS-CUT-036.** Authoring guidance MUST use a short clarity checklist and high-signal hints without exact sentence, word or identifier budgets.

**KIS-CUT-037.** Risk recording MUST accept a description, owner and action with optional scoring; blocking requires an explicitly requested accountable decision.

**KIS-CUT-038.** Response integrity MUST bind stable machine evidence only where consumed, excluding human-facing wording from the checksum contract.

**KIS-KEEP-039.** File operations MUST reject writes or deletes outside the selected target, including supported link and junction escapes.

**KIS-KEEP-040.** Updates MUST preserve owner content outside managed fragments and obtain an explicit choice before replacing customized repository files.

**KIS-KEEP-041.** Writes MUST use atomic file replacement with bounded rollback for ordinary multi-file failures.

**KIS-KEEP-042.** Package download and publication MUST verify required artifact hashes and refuse replacement of conflicting published bytes.

**KIS-KEEP-043.** Candidate test jobs MUST have no publication credentials or permission to obtain them.

**KIS-KEEP-044.** Meaningful scope, assurance and release decisions MUST retain explicit accountable owner approval.

**KIS-KEEP-045.** Evidence MUST identify the actual checker origin and version and the exact tested candidate.


## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Harmless formatting, ignored environment setting or unrelated file | Continue with the simpler rule | Optional useful hint |
| Actual scope escape, wrong imported checker or corrupt package | Refuse before the affected write or publication | Name the input and corrective action |
| Unavailable remote check during authorized local work | Keep local result and show remote status separately | CI unavailable; no false success claim |
| Changed relevant candidate or governing input | Require fresh affected evidence | Identify what changed |
| Conflicting required release asset | Stop that publication attempt | Name the conflicting asset |

## Examples

**Given** a PR body with Windows line endings. **When** its work order is selected. **Then** it selects the same ID as LF text (KIS-CUT-001).

**Given** an approved local task and an unavailable GitHub service. **When** its required local checks pass. **Then** the permitted local action proceeds (KIS-CUT-006).

**Given** an unpublished draft with one correct required asset. **When** publication resumes. **Then** only missing required assets are uploaded (KIS-CUT-028).

**Given** a changed required published package. **When** publication checks its digest. **Then** it refuses the mismatch (KIS-KEEP-042).

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-001 | KIS-CUT-001, KIS-CUT-002, KIS-CUT-003, KIS-CUT-007, KIS-CUT-011, KIS-CUT-035, KIS-CUT-036, KIS-CUT-037; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-002 | KIS-CUT-004, KIS-CUT-005, KIS-CUT-006, KIS-CUT-008, KIS-CUT-009, KIS-CUT-010, KIS-CUT-012; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-003 | KIS-CUT-013, KIS-CUT-014, KIS-CUT-015, KIS-CUT-016, KIS-CUT-017, KIS-CUT-018, KIS-CUT-019, KIS-CUT-020, KIS-CUT-021, KIS-CUT-022; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-004 | KIS-CUT-023, KIS-CUT-024, KIS-CUT-030, KIS-CUT-038; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-005 | KIS-CUT-025, KIS-CUT-026, KIS-CUT-027, KIS-CUT-028, KIS-CUT-029; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-006 | KIS-CUT-031; KIS-KEEP-039 through KIS-KEEP-045 where applicable |
| REQ-KIS-007 | KIS-CUT-032, KIS-CUT-033, KIS-CUT-034; KIS-KEEP-039 through KIS-KEEP-045 where applicable |

## Not decided here

- Small internal helper names and decomposition within the approved scope.
- A later release version, publication decision or live root upgrade.
- A later historical archive move after its destination and preserved references are reviewable.

## Compatibility and migration

This specification explicitly replaces the following earlier behavior for the selected KIS work orders and future candidate implementation.
It does not rewrite an old decision, verification result, release or its evidence. Earlier completed work retains its original contract.
Do not keep contradictory restrictions as a second compatibility mode for new operations. Retain readers for historical records where stated above.

| Candidate rules | Earlier contracts | Replacement and retained boundary |
| --- | --- | --- |
| 001–003, 007, 011 | SPEC-IAR-012; SPEC-ECP-001/002/003/009/011/014/016/017; SPEC-WEX-002; SPEC-AUT-004 | Replace raw-byte budgets, header positioning, procedure knowledge and harmless path spelling restrictions; preserve actual scope and machine status. |
| 004–006, 008–012 | SPEC-ECP-001/003/006/010/015/017; SPEC-AEX-001/006/008; SPEC-IAR-001; SPEC-REV-001 | Replace sole-base-branch delegation, local live-CI dependency, global freshness and dashboard/dirty-caller prerequisites; preserve explicit approval and exact tested input. |
| 013–022 | SPEC-HBI-001; SPEC-REB-001/004/011/015; SPEC-PMI-001; SPEC-HUP-012; SPEC-DST-001/002 | Retire field census, region policing, interpreter layout restrictions and repeated receipts; reduce the future managed inventory while preserving published bytes and fragment safety. |
| 023–024, 030 | SPEC-REV-001; SPEC-AGR-001; SPEC-VSP-001/002; SPEC-CIP-001 | Use one final integration verification with historical input links; add explicit safe ready refresh; make trailer census advisory. |
| 025–029, 031 | SPEC-CIP-001/002/003/004; SPEC-RLO-001/002/004/005; SPEC-PLG-021 | Narrow rehearsal triggers and target snapshots, resume unpublished drafts, validate required asset subsets and retain smaller new evidence; preserve final release qualification. |
| 032–034 | SPEC-HBI-001; SPEC-REB-011/015; test-suite contracts | Remove tests of retired restrictions and internal syntax; preserve supported-installation, packaging and escape tests. |
| 035–038 | SPEC-AUT-001/002/004; SPEC-TCM-001/003/004/005/006/007; SPEC-RSK-010; SPEC-WEX-001/002/003; SPEC-ECP-003/017 | Replace mandatory keyword, grammar budgets, compulsory risk scoring/pairing and prose digests; preserve meaningful descriptions, explicit decisions and stable machine data. |

Matching earlier requirements, architecture and verification expectations apply only outside these stated replacements.
Implementers update current explanatory notes and candidate templates in the same slice as behavior. Historical artifacts remain factual records.
The installed root remains released 0.17.0 until separately authorized adoption. All work in this packet is governed by that released evaluator.

## Data and interface contracts

- **PR selection (004):** keep the singular `Harness-Work-Order: WO-...` line; add one `Harness-Work-Orders: WO-..., WO-...` line. Reject both forms together, duplicate IDs and malformed IDs. Check every selected approved scope; accept only the union. No release aggregation protocol is added.
- **Local authority (005–006):** reuse the explicit engineering-owner approval event on the work order and its execution delegation. Start, completion and evidence preparation use the released checker and relevant local checks. A scope change requires new explicit owner approval. A class label or successful test alone grants nothing. CI remains required at repository integration and publication; an unavailable provider is reported separately during local work. Do not add signatures, a second approval receipt or a new authentication service.
- **Freshness and capture (008–010, 012):** use the selected chain and its declared dependencies. Record the exact code commit. For explicit committed capture, create and test a temporary worktree of that commit; never relabel dirty-tree results as committed evidence. Duplicate IDs and an unreadable selected chain remain blockers. Unrelated diagnostics are background findings.
- **Checker identity (015–021):** retain the environment entry point when a virtual environment needs it; inspect the actual imported package origin after resolving links. Ordinary writes use origin/version. Doctor or explicit integrity inspection still checks the full installed payload. Release preparation still checks the checker payload and exact release artifacts, but does not demand a receipt for the checker's original archive. Accept legacy identity evidence with its legacy hash rule; use canonical parsed values for new internal evidence. External published archive hashes remain byte hashes.
- **Smaller managed surface (022):** the new target inventory locks the core router, machine `WORKFLOW.json` and `QUALITY_GATES.json`, and the existing managed instruction/ignore fragments. The installed evaluator owns executable policy. Human policy explanations, authoring guidance, artifact templates, CI workflow and owner configuration are editable seeded files. The selected evaluator version remains a validated setting matching the installation record; an edit is not an implicit upgrade. Initialize absent seeded files; on later update keep customized files by default and replace only on an explicit operator choice. Read previous locks and migrate only through an explicit installation/upgrade operation. Do not rewrite this repository's current 0.17.0 root during these work orders.
- **Final verification (023):** create one final-candidate VREC covering every released work order and required verification contract. Its evidence may cite earlier work records at other commits, but it must demonstrate the final integration was tested. The RLS binds this final VREC at its exact candidate. Earlier VRECs remain unchanged historical sources and do not independently substitute for final assurance. This retains a simple final-candidate relationship rather than adding automatic evidence equivalence.
- **Ready refresh (024):** add an explicit refresh operation that compares the relevant Git tree entries and governing inputs, then creates a new ready record with the new candidate and the checked reuse explanation. Retain the original record and its evidence. Do not silently retarget a record or mark either one verified. Changed relevant contents require new tests. No automatic rebase watcher or heuristic patch-equivalence service.
- **CI triggers (026–027):** ordinary PRs retain the source suite, installed-package smoke checks and managed validation. Candidate build replay runs on changes to packaging inputs (`pyproject.toml`, `MANIFEST.in`, `release/`, build scripts and `repository_tools/release_build.py`) or publication implementation/workflows/tests. The older-release leg runs on publication implementation/workflow changes. Explicit release preparation runs both. Use one small shared change decision based on changed paths; a required workflow reports an explicit successful skip when irrelevant, so branch protection does not wait forever. Keep supported Windows and Ubuntu package coverage. No scheduled job is added.
- **Publication retries (028–029):** resume only an unpublished draft. Compare each expected filename and digest before upload; upload missing files, leave matching files and unrelated attachments alone. Published release/package bytes stay immutable. Keep the protected publication environment and its credentials away from candidate jobs.
- **Evidence retention (031):** new tracked evidence contains the command, candidate, checker version/origin, result, useful failure excerpt and raw-artifact location with retention/expiry information. Upload full logs through existing CI artifacts; permanently required publication evidence remains in the existing durable release bundle. Missing raw output is unavailable evidence, never a pass. Inventory existing bundles by size and bound-record references; recommend an archive destination and a reference-preserving move plan. This work order implements the accepted review-and-assess recommendation; it does not delete bound history, rewrite Git history or introduce a storage service.
- **Writing and risk (035–037):** retain a nonempty requirement obligation and at least one concrete acceptance condition through the selected verification contract or requirement examples. Writing keywords and sentence length are advice. A new risk needs a nonempty description, owner and next action; scoring and taxonomy are optional. A risk alone does not block. Use the existing decision mechanism only when the owner explicitly asks for a stop. Existing scored risks, paired decisions and recorded dispositions remain readable with their original meaning.
- **Human output (038):** machine status, candidate identity, artifact IDs and command argument arrays remain structured. Existing versioned response readers retain compatibility; new evidence digests exclude explanatory prose. Remove renderer-byte tests that only lock wording.

These choices are part of the accepted simplification implementation envelope. They are not permission to use new candidate behavior to waive the currently installed governor's rules.
