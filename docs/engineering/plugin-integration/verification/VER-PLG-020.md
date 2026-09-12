+++
id = "VER-PLG-020"
type = "verification"
title = "Verify safe evaluator skill ownership migration and restoration"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[relations]
verifies = ["REQ-PLG-028", "REQ-PLG-029", "REQ-PLG-030", "REQ-PLG-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "assurance-owner"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only VER-PLG-020 approval as assurance-owner. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Verification Contract: Verify safe evaluator skill ownership migration and restoration

## Independence

Expected file sets, bytes, identities, digests, and refusals come from SPEC-PLG-020 and fixed fixture inputs.
The assurance owner approves this contract before implementation. Candidate output never defines its expected result.
This contract states acceptance criteria; it claims no observed implementation success.

## Requirement-to-evidence matrix

| Requirement | Cases | Pass condition |
| --- | --- | --- |
| REQ-PLG-028 | OWN01, OWN02, OWN03, OWN04, OWN14 | Exact selected retirement; ownership changes only with a valid reviewed plan; other content unchanged. |
| REQ-PLG-029 | OWN05, OWN06, OWN07, OWN08, OWN12 | Valid ownership survives all inventory consumers, replay, ordinary upgrades, and a credential-free clone. |
| REQ-PLG-030 | OWN04, OWN09, OWN10, OWN11, OWN13 | Stale plans refuse; failures recover; explicit restoration is safe; concurrency never partially applies. |
| REQ-PLG-031 | OWN01, OWN03, OWN12, OWN14 | Independently pinned provider data is validated without executing it or claiming native host support. |

## Platform and evaluator identities

The governing evaluator for development is the root-pinned released 0.17.0 in an isolated environment outside candidate source.
Candidate source and an explicitly non-promotable isolated candidate wheel exercise the new operation on disposable repositories only.
Use Python 3.11 and 3.13 on Ubuntu and Windows; record exact runner image, OS, Python, candidate commit, package hash, and evaluator identity.
The full fault and ownership matrix runs on Python 3.13 on both operating systems; Python 3.11 runs the interface and compatibility smoke cases.
No Linux or Windows CI result is a claim about native Codex or Claude qualification. macOS remains untested unless separately selected.

## Acceptance scenarios

Each case retains invocation arguments, structured result, exit status, input hashes, recursive ordinary-file snapshots, lock snapshots, and observed write destinations.
External plugin fixtures include inert scripts that create a sentinel if executed; the sentinel must remain absent.

| Case | Fixture and action | Required observation |
| --- | --- | --- |
| OWN01 | Plan and apply each selected host binding against a valid current standard fixture. | Planning writes nothing; application retires exactly seven catalog files, binds the expected retained skills, and leaves external packages unchanged. |
| OWN02 | Add unrelated skills and owner content beside selected files. | All unrelated bytes, empty/nonempty owner directories, and owner fragments remain unchanged; no recursive directory deletion occurs. |
| OWN03 | Independently vary customization, missing owned file, unowned shadow, symlink, junction/reparse point, hard link, path escape, case collision, duplicate key, unknown schema, or size limit. | Each applicable case refuses before the first write; retain platform-specific unsupported fixture mechanisms explicitly. |
| OWN04 | Change each reviewed input after planning, including equal-size file content and external inventory. | Application refuses a stale digest; lock, files, and external content remain unchanged. |
| OWN05 | Replay successful migration twice; run doctor and every supported installer entry point. | No lock-byte drift, extra evidence overwrite, or recreation of retained repository skills; direct APIs cannot bypass ownership handling. |
| OWN06 | Ordinary version-compatible upgrade and a deliberately unsupported ownership-format upgrade. | Compatible upgrade preserves the exact binding; incompatible upgrade refuses atomically and does not reconstruct the default catalog. |
| OWN07 | Run released 0.17.0 against plugin-owned schema 4; also run candidate against an unsupported old lock. | Every writing path refuses before mutation; read-only commands report unsupported identity/format without claiming readiness. |
| OWN08 | Reintroduce a selected retained file or tamper with the binding and expected inventory. | Doctor and applicable mutation guards fail; deleting an offending record cannot turn it into an accepted repository-owned installation. Current-lock evaluator-evidence matching accepts a valid schema-4 binding and refuses a mismatched evaluator identity. |
| OWN09 | Inject an exception at each deletion, lock replacement, recovery-record update, and postcondition boundary. | Complete prior snapshots are restored or an explicit recovery-required failure is retained; no partial success. |
| OWN10 | Terminate an independent application process at each durable transaction boundary; restart and recover. | Pending recovery is detected before another mutation. Untouched targets recover consistently; intervening owner edits or new files remain untouched, with explicit recovery-required status. Tampered, truncated, or path-escaping recovery metadata never causes an overwrite or escaped write. |
| OWN11 | Restore repository ownership, including variants with owner-created path conflicts. | Exact selected-distribution retained files return only when safe; conflicts preserve all original bytes and the old binding. |
| OWN12 | Clone a plugin-owned fixture into a different path without external packages or host credentials. | Repository integrity and governed CLI checks remain meaningful; availability is explicitly unobserved, never reported as proven. |
| OWN13 | Race two independent migration/restoration processes with different plans. | One exclusive transaction or explicit contention refusal; neither commits stale inputs or a mixed ownership state. |
| OWN14 | Wrong expected package hash, changed root, changed version, missing payload, missing retained core, incompatible evaluator identity, and inactive-host observations. | Data mismatch refuses migration; syntactically valid inventory does not claim host activation or enforcement. |

For OWN03, test the full applicable path matrix on each platform, with at least one real linked-path refusal on each.
A filesystem mechanism unavailable to a runner remains explicitly unavailable and is never counted as a passed refusal.

## Regression and package checks

Run the repository's canonical source test runner, release-distribution validation, candidate help, and required released-evaluator graph, integrity, and scope checks.
Prove ordinary init/upgrade behavior remains unchanged without plugin ownership.
Package inventory tests verify the new evaluator module and ownership contract ship in wheel and source distributions.
Candidate packaging is non-promotable test evidence outside the checkout; it authorizes no release build, tag, publication, or adoption.
The installed candidate may test disposable fixtures only; it never governs this implementation checkout.

## Evidence retention

Retain case JSON, subprocess logs, raw file hashes, fault schedules, recovery records, and exact CI links under `evidence/WO-PLG-020/`.
Bind a later VREC to the exact committed implementation candidate after completion is separately recorded.
Retain the approved plan and all failures, missing observations, recovery failures, and supported-version limits.
Native activation, C10/C11 enforcement, live repository rollout, and public qualification are outside this contract.

## Review clarification: recovery preservation

The existing preservation rules also apply after interruption. Test changed tracked files, newly created destinations, corrupted snapshots, and tampered/truncated/path-escaping recovery records before attempting recovery.
Recovery must retain usable diagnostic inputs and preserve unexpected current content; it must not overwrite that content merely to reconstruct the old snapshot.
These are concrete negative cases for REQ-PLG-030 and PLG-OWN-005 through PLG-OWN-010, not permission to weaken rollback or delete owner changes.


## Approved legacy-reader reconciliation — 2026-09-12

The operator approved this exact appendix as `assurance-owner` with the instruction "i approve the 4 amendements". The approval was recorded at `2026-09-12T18:28:18Z` under WO-PLG-020. Its reviewed proposal and decision receipt are retained in that work order's governance evidence. The original definition text, approvals and historical observations remain preserved. This approval does not establish passing acceptance, completion or verification.

### Approved applicability: OWN07 interface census and report boundary

This appendix supersedes only OWN07's unqualified “Every writing path” and universal read-only-refusal wording. Test the real isolated released 0.17 executable against a valid schema-4 fixture and retain a version check, syntactically valid argv, actual process status, diagnostics and complete before/after snapshots. Enumerate every public interface and writing mode that can modify installed files/the lock or create/change formal governance artifacts, including the applicable installer, scaffolding, artifact creation, transition/decision/risk, verification capture and release preparation interfaces. Trace shared direct/delegated entry points separately and identify any coverage inference. Every applicable protected interface MUST refuse before its mutation with an unsupported-lock or evaluator-incompatibility diagnostic. Use a valid fixture for that interface or otherwise prove that the compatibility check caused the refusal. An unrelated lifecycle/input refusal, parser usage error or candidate-only mocked guard is insufficient evidence.

Separately exercise artifact-graph validation, evidence generation, retained check-result generation and derived reporting. Record their actual refusal or successful output generation. Successful generation of the specifically observed evidence/report output may satisfy this boundary observation only when snapshots prove that pre-existing installation/configuration/lock bytes, formal artifact metadata and external provider bytes remain unchanged. It is not a passing unsupported-format refusal and MUST NOT be reported as installation compatibility, governing readiness or matching evaluator-bound assurance. Unexpected additional writes or changes remain failures.

Run the expanded OWN07 selection in the already required Python 3.11 smoke and Python 3.13 full source/package observations on Ubuntu and Windows. Preserve the original four-probe results and the newly observed contrary results; do not rewrite them. All other OWN cases, regression/package requirements, source/package authority distinctions, unavailable-mechanism rules and exact-candidate evidence obligations remain unchanged. Completion and VREC preparation remain pending until the amended observations and existing gates pass.
