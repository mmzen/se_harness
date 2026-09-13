+++
id = "VER-KIS-001"
type = "verification"
title = "Verify the simpler behavior and retained protections"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[relations]
verifies = ["REQ-KIS-001", "REQ-KIS-002", "REQ-KIS-003", "REQ-KIS-004", "REQ-KIS-005", "REQ-KIS-006", "REQ-KIS-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "assurance-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the assurance-owner approval of VER-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Verify the simpler behavior and retained protections

## Independence

Expected outcomes below come from the accepted review and SPEC-KIS-001, not from candidate output.
Use source and explicitly non-promotable candidate packages for product tests; use the isolated released 0.17.0 evaluator for governing decisions.
This is a verification plan. It claims no implementation or passing acceptance result.

## Requirement-to-evidence matrix

| Requirement | Checks | Pass condition |
| --- | --- | --- |
| REQ-KIS-001 | K01, K02, K03, K07, K11, K35, K36, K37 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-002 | K04, K05, K06, K08, K09, K10, K12 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-003 | K13, K14, K15, K16, K17, K18, K19, K20, K21, K22 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-004 | K23, K24, K30, K38 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-005 | K25, K26, K27, K28, K29 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-006 | K31 | All listed outcomes observed; obsolete behavior and its tests removed. |
| REQ-KIS-007 | K32, K33, K34 | All listed outcomes observed; obsolete behavior and its tests removed. |

## Bounded acceptance checks

| Check and candidate | Work order | Observable pass condition |
| --- | --- | --- |
| K01 / KISS-01 | WO-KIS-001 | Equivalent LF and CRLF PR bodies select the same IDs; conflicting or malformed IDs still fail. |
| K02 / KISS-02 | WO-KIS-001 | The same owner instructions pass with LF and CRLF beyond the former byte cutoff; edited managed markers still fail. |
| K03 / KISS-03 | WO-KIS-001 | A literal bracket filename and a native CLI path are accepted inside scope; traversal, absolute outside paths and Git-reported escapes fail. |
| K04 / KISS-04 | WO-KIS-002 | One and multiple explicit approved IDs produce the expected union; an unapproved ID or path outside every scope fails. |
| K05 / KISS-05 | WO-KIS-002 | A recorded owner-approved local delegation starts without a preliminary merge; absent approval or widened unapproved scope fails. |
| K06 / KISS-06 | WO-KIS-002 | With GitHub unavailable, a locally authorized transition with passing retained checks succeeds; a failed local check still blocks. |
| K07 / KISS-07 | WO-KIS-001 | A referenced evidence note works without the old header; a missing referenced file fails; descriptive metadata does not invalidate it. |
| K08 / KISS-08 | WO-KIS-002 | An unrelated artifact edit preserves freshness; a governing requirement change or changed tested input requires new evidence. |
| K09 / KISS-09 | WO-KIS-002 | Capture succeeds with dashboard generation unavailable; independently requested dashboard generation still works. |
| K10 / KISS-10 | WO-KIS-002 | An explicit candidate is captured despite an unrelated untracked note; committed candidate and temporary-worktree test results match; no dirty bytes enter evidence. |
| K11 / KISS-11 | WO-KIS-001 | The ordinary selected-artifact check returns the valid action for draft, approved and implemented work without procedure knowledge. |
| K12 / KISS-12 | WO-KIS-002 | An unrelated incomplete work order is reported separately; a selected-chain error and duplicate global artifact ID still block. |
| K13 / KISS-13 | WO-KIS-003 | An unrelated new checksum-named metadata field does not fail a census; a bad checksum consumed by its own format fails. |
| K14 / KISS-14 | WO-KIS-003 | Equivalent effective attributes inside or outside a comment region behave equally; genuinely wrong required bytes still fail. |
| K15 / KISS-15 | WO-KIS-003 | A real linked external tool directory works on Windows and Ubuntu; an imported checker from the candidate checkout fails. |
| K16 / KISS-16 | WO-KIS-003 | Ordinary identity returns Python version with no executable digest field or binary-hash read requirement. |
| K17 / KISS-17 | WO-KIS-003 | An ignored PYTHONPATH under isolated Python does not block; a real candidate import still fails. |
| K18 / KISS-18 | WO-KIS-003 | The isolated module route works without the console launcher; a selected broken console launcher reports its own error. |
| K19 / KISS-19 | WO-KIS-003 | Ordinary commands succeed with version and origin checks; an explicit full inspection detects a changed installed payload. |
| K20 / KISS-20 | WO-KIS-003 | A checker installed without an archive receipt prepares a release when its payload and release artifacts are valid; wrong release artifact hashes fail. |
| K21 / KISS-21 | WO-KIS-003 | Whitespace-equivalent JSON produces the same internal identity; changed required values and duplicate keys fail. |
| K22 / KISS-22 | WO-KIS-003 | Editing guidance, templates or owner settings survives doctor and a keep choice; altered machine policy fails; fragment-adjacent owner content survives replacement. |
| K23 / KISS-23 | WO-KIS-004 | Earlier verified work at different commits can support one explicitly verified final candidate; missing final verification or incomplete scope fails. |
| K24 / KISS-24 | WO-KIS-004 | A harmless rebase supports an explicit ready successor with reused evidence; changed relevant content requires rerun and verified history is untouched. |
| K25 / KISS-25 | WO-KIS-005 | A large unrelated input file does not expand acceptance snapshots; an attempted write outside the disposable target is rejected. |
| K26 / KISS-26 | WO-KIS-005 | A normal documentation/runtime PR skips deterministic replay; a build-input change and explicit release preparation select it. |
| K27 / KISS-27 | WO-KIS-005 | An ordinary PR skips the older-release leg; a publication-path change and explicit release preparation select it. |
| K28 / KISS-28 | WO-KIS-005 | Retry of a partial unpublished draft uploads only missing required assets; same-name wrong bytes and replacement of published packages fail. |
| K29 / KISS-29 | WO-KIS-005 | A release with all required assets plus a screenshot passes; a required asset with conflicting bytes fails. |
| K30 / KISS-30 | WO-KIS-004 | An owner-approved final scope tolerates an untrailed integration commit without exemptions; missing final verified work remains a release failure. |
| K31 / KISS-31 | WO-KIS-006 | A new run produces a concise tracked summary plus downloadable raw results, and an inventory identifies existing bundle size, record references and archival options. |
| K32 / KISS-32 | WO-KIS-007 | A behavior-preserving refactor needs no internal-name expectation updates; public failures and the required package import boundary remain tested. |
| K33 / KISS-33 | WO-KIS-007 | No integrity test invokes aggressive GC; LF/CRLF equivalence and one real checkout run on each supported OS pass. |
| K34 / KISS-34 | WO-KIS-007 | Actual supported interpreter installations and one unavailable capability pass/fail as specified; actual origin and path escapes still fail. |
| K35 / KISS-35 | WO-KIS-001 | A clear requirement without SHALL and a concrete acceptance condition can be approved; a blank obligation or missing acceptance condition cannot. |
| K36 / KISS-36 | WO-KIS-001 | Clear prose outside old budgets remains eligible; ordinary missing-field and contradictory-value validation remains active. |
| K37 / KISS-37 | WO-KIS-001 | A short unscored risk can be recorded without blocking work; an explicitly raised blocking decision still stops its named scope; legacy scored risks remain readable. |
| K38 / KISS-38 | WO-KIS-004 | A wording-only change leaves machine evidence identity unchanged; changed candidate, state or command arguments change the relevant structured result. |

These are coverage outcomes, not a requirement for 38 separate test modules or one test per sentence.
Reuse a small shared fixture when outcomes overlap. Remove old failure assertions when the restriction is removed; do not preserve them as a disabled mode.
Each work order runs only its listed acceptance checks plus applicable retained protections and current repository-required validation.

## Retained protections

| Review item | Minimum evidence where the slice touches this boundary |
| --- | --- |
| KISS-39 | One real outside-target refusal for each supported escape mechanism used by the operation. |
| KISS-40 | Owner text beside a managed fragment survives; a customized seeded file follows the explicit keep/replace choice. |
| KISS-41 | One ordinary write failure leaves the file atomic and a multi-file operation recoverable. |
| KISS-42 | One conflicting required package digest is rejected. |
| KISS-43 | Workflow permission review shows candidate jobs cannot obtain publication credentials. |
| KISS-44 | Missing explicit approval does not become approval because a check passed. |
| KISS-45 | Wrong effective checker origin/version fails and reported candidate matches the tested commit. |

## Platforms and evaluation

Use supported Windows and Ubuntu environments for paths, imports, installation and checkout behavior.
Use the already supported interpreter versions in the affected CI lanes; do not invent a new matrix.
Run the appropriate source suite, distribution-surface validation, CLI help, released doctor/graph and selected work-order checks required by the repository.
The present required checks continue until an approved implementation changes them through the candidate route.
No promotable release build, external publication, live root upgrade or new host installation is authorized by this plan.

## Evidence and completion

Record commit, checker identity, commands, results, useful failure excerpts and stable CI/raw-output references in the selected work order's evidence directory.
Update the 38-candidate coverage table with observations and report relevant source/test/CI reductions without claiming unmeasured speedups.
A later VREC is prepared by the released evaluator after the candidate commit; no reserved VREC is created by this packet.
