+++
id = "VER-PLG-021"
type = "verification"
title = "Verify useful plugin behavior with a small acceptance set"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[relations]
verifies = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-PLG-035", "REQ-PLG-036", "REQ-PLG-037"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "assurance-owner"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the assurance-owner approval of VER-PLG-021 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Verification Contract: Verify useful plugin behavior with a small acceptance set

## Independence

Expected results come from REQ-PLG-032 through REQ-PLG-037 and SPEC-PLG-021.
Tests create explicit disposable inputs and assert the specified final state. Candidate output never supplies the expected result.
The earlier local prototype is a starting point, not evidence that this whole work order has passed.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-032 | Test | K01, K02 | Edited, extra and missing old copies are handled; incomplete replacements fail before deletion. |
| REQ-PLG-033 | Test | K03, K04, K05 | Deletion remains inside the selected destinations; interruptions can be retried; restoration overwrites disposable copies. |
| REQ-PLG-034 | Test | K06 | Schema-4 compatibility, doctor, upgrade and plugin-free clone checks preserve the provider choice. |
| REQ-PLG-035 | Test and inspection | K07 | Setup creates, reuses and repairs its own environment; actual failures are reported. |
| REQ-PLG-036 | Test and inspection | K08, K09 | No blocking hooks or exact-version allowlists remain; instructions invoke the selected checker; required failures remain visible. |
| REQ-PLG-037 | Test and inspection | K10, K11, K12, K13 | Development rebuilds are bounded; release checks remain; CI duplication and obsolete contracts are removed. |

## Acceptance scenarios

| Case | Inputs and action | Expected result |
| --- | --- | --- |
| K01 Replacement | Old skills contain an edit and an extra file; another selected old directory and a catalog entry are absent; an unrelated managed file differs. Apply migration twice. | Selected copies and entries disappear; unrelated skills and files survive; the second application succeeds. |
| K02 Invalid inputs | Try a missing lock, malformed lock, wrong plugin name and missing replacement file. | Each fails before deleting any old skill. |
| K03 Destination boundary | Use a redirected old directory and a plugin inside a directory selected for deletion; run existing report-output protection tests. | Reject both before deletion, preserve the external destination, and preserve ordinary report destination protection. |
| K04 Ordinary interruption | Inject one deletion error and one atomic-lock-save error; remove the error and rerun each operation. | Each error is reported; each rerun finishes. No journal or recovery command is required. |
| K05 Restoration | Restore repository skills over locally changed disposable copies. | Current templates and ordinary managed entries return; unrelated content stays unchanged. |
| K06 Portable ownership | Read a previous schema-4 binding, reapply migration, run doctor and upgrade, and check a clone with no plugin. | A portable provider-only record works; ordinary upgrade does not recreate old skills; unknown providers produce an error. |
| K07 Setup | Use a valid wheel, rerun setup, retry after an interrupted installation, and try an unavailable prerequisite. | One private path is reused or repaired; success follows an actual checker invocation; missing prerequisites produce clear guidance. |
| K08 Explicit operation | Inspect both packages; exercise their skill entry instructions with a working checker and a failing checker. | No automatic blocking hooks ship; current host patch versions are not denied by a profile; actual checker results govern the response. |
| K09 Instruction and log behavior | Inspect start, compaction and repository-switch instructions; make optional logging unwritable. | Files are read normally; no delivery-marker ceremony is required; logging failure does not change the operation result. |
| K10 Development build | Build from local source and a local wheel, rebuild its output, and target an unrelated nonempty directory. | Both host archives contain required skills and development labeling; rebuilding works; the unrelated directory survives. |
| K11 Publication boundary | Run existing publication validation against development inputs and valid existing release fixtures. | Local output does not qualify itself as a release; existing valid release inputs remain accepted. |
| K12 Removal review | Review the diff against all 50 proposal scenarios, current docs and CI steps. | Every accepted removal is delivered or identified as a failing criterion; seven retained protections remain covered. |
| K13 Minimal checkout | Reproduce the configured sparse checkout from the real candidate commit; run the package job and its downstream checks. | Only the required script is materialized; the checkout stays unchanged; package acceptance passes without the snapshot-size refusal. |

These are behavior groups, not a required count of separate test functions.
Use small fixtures and direct assertions; do not add per-case filesystem archives or a new evidence framework.

## Platforms and evaluator

Use the repository-pinned released evaluator 0.17.0 outside the checkout for graph, integrity, scope and workflow checks.
Run the normal candidate-source suite once in its existing CI job.
Run the installed migration acceptance on Windows and Ubuntu using each existing Python 3.11 package environment and the same candidate wheel.
Run focused setup, assembly and explicit-command tests on those operating systems within existing jobs.
Run one current native skill-discovery smoke for each host on the owner's Windows development environment when implementation is assessed.
Native smoke needs no before-tool denial or historical host-version replay because the new design provides no automatic interception.
Record an unavailable host as missing acceptance, not successful qualification. macOS and simultaneous migration writers are outside the claim.
On a Windows runner without symlink privileges, record the skip and use Ubuntu for the required redirection case.

## Evidence retention

Retain commands, exit codes, concise logs, the tested commit, the candidate wheel identity and CI links in WO-PLG-021's evidence directory.
Keep one result per distinct check. Reference previous historical records rather than copying their archives.
Record before/after code size, test counts and comparable CI durations if observed; do not claim a measured speedup without measurements.
The seven kept protections and all 43 accepted changes are traced in the proposal coverage map.

## Pass criteria

All matrix criteria pass, required checks pass, and no changed path leaves the approved work-order scope.
The diff removes the abandoned machinery and its obsolete tests instead of retaining a second supported route.
Historical VREC, RLS, decided DEC and evidence bytes remain unchanged.
Implementation completion and a later commit-bound verification record follow the existing workflow.

## CI prerequisite amendment — 2026-09-13

The owner accepted the minimal-checkout fix with "ok go", including rerunning package acceptance and downstream checks.
This records the assurance-contract decision for K13, not a verification result for the whole work order.
