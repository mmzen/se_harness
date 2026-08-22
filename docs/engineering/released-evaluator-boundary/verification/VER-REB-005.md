+++
id = "VER-REB-005"
type = "verification"
title = "Hosted predecessor-assessment and portable fault-injection assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
verifies = ["REQ-REB-013", "REQ-REB-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "quality-owner"
+++

# Verification Contract: Hosted predecessor-assessment and portable fault-injection assurance

## Independence

Assurance independently acquires the hosted logs and public 0.5.0 wheel, computes candidate/tree/blob/raw hashes, selects diagnostic mutations and extra omissions, and runs Linux/Windows failure injection without trusting adapter-reported identities. The candidate implementation may produce evidence but cannot decide whether an expected-red observation is acceptable.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-013` | C4 failure replay | runs `32558379907` and `32558379908`, exact SHA and jobs | Exact original failures and skipped package job are retained without reinterpretation |
| `REQ-REB-013` | Full-checkout legacy matrix | exact `E009`; changed path/status/code; added error; earlier identity/integrity failure | Only exact `E009` after successful identity/integrity matches the transitional expectation; every variation blocks |
| `REQ-REB-013` | Assessment-view integration | exact C5, closed rejected pair, external 0.5.0 | `doctor`, `validate`, and dashboard pass in a view whose artifact count equals the complete candidate count minus exactly two (643 for the reviewed 645-artifact C5 scope), while full candidate validation passes separately |
| `REQ-REB-013` | Preparation/assessment equivalence | paths, sparse bytes, commit/tree/blob/raw identities | Both operations derive byte-identical view specifications and omissions |
| `REQ-REB-013` | Hosted evidence replay | workflow/job/run URLs, logs, artifact JSON, hashes, return codes | Independent replay reproduces every bounded identity and output digest |
| `REQ-REB-013` | Path/runtime negatives | extra/missing/linked path, dirty SHA, Git config/object change, evaluator/wheel/lock substitution | Every case fails before external or source mutation |
| `REQ-REB-014` | Fault-seam inspection | production exclusive-create wrapper and mock targets | Production flags/mode are unchanged and no test patches process-global `os.open` |
| `REQ-REB-014` | Platform failure matrix | Python 3.11/Linux, Windows/current runtime, first/second write and between-write mutation | Intended adapter error/rollback is stable; temporary cleanup succeeds; zero output remains |
| Both | Complete qualification | full suites, candidate package, graph, distribution, diff, protected paths | All required candidate/view lanes pass and root/history remain unchanged |

## Acceptance scenarios

1. C4 candidate `b099a2728d945ee705c1f956ec012f9730df15ac` reproduces the exact old-workflow `E009` and Linux `dir_fd` errors.
2. The local prototype at exact C4 omits only `REL-SEH-008` and `RLS-SEH-009`; released 0.5.0 `doctor` and `validate` pass with 635 artifacts, zero errors, and 47 legacy warnings.
3. C5 full candidate validation sees every artifact and passes; the old full-checkout result remains exactly one expected predecessor limitation.
4. C5 hosted predecessor assessment passes with exact 0.5.0 and uploads canonical evidence; candidate source and package jobs pass.
5. Adding a second legacy error, altering its code/path, or omitting a third file fails the release gate.
6. The two rollback tests pass on Linux Python 3.11 and Windows without intercepting cleanup calls.

## Property and invariant tests

- Assessment and preparation choose the same pair independent of discovery order.
- The assessment schema is canonical, deterministic, host-neutral, and closed.
- Candidate/source/view HEAD, tree, object format, blobs, and raw hashes remain exact across replay.
- The complete checkout has identical tracked/untracked/protected-state maps before and after assessment.
- Exact expected-red matching cannot accept a different job, SHA, evaluator, command, diagnostic, or count.
- Exclusive-create call count reflects only adapter writes, never temporary-directory internals.

## Static and architecture checks

- Trace through `SPEC-REB-006`, `ARCH-REB-005`, `ADR-REB-005`, and `WO-REB-007`.
- Confirm zero diff to `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, all other root-managed paths, released evaluator material, maintenance state, and rejected history.
- Confirm the new workflow has read-only contents permission, pinned actions, fixed commands, exact evaluator hash checks, checkout no-change proof, and bounded artifacts.
- Confirm no generic `continue-on-error`, failure suppression, arbitrary omit flag, root upgrade, history rewrite, or automatic lifecycle action.

## Security and privacy checks

Exercise symlinks/junctions, path case/aliases, unsafe output roots, alternate Git objects/config, malicious logs, duplicate JSON keys, injected ANSI/control bytes, environment contamination, executable replacement, and artifact collision. Confirm evidence excludes secrets and host identifiers.

## Performance and resilience checks

Run focused assessment/failure tests and full suites on Python 3.11/Linux and the current Windows runtime. Rehearse interruption before view creation, between commands, during evidence creation, during cleanup, and during final candidate replay. No source mutation or partial evidence may remain.

## Manual assessments

- Technical/security owners accept the transitional dual-plane trust statement.
- Assurance owner explicitly reviews the exact expected-red diagnostic and green replacement evidence.
- Release owner confirms root-managed state and external policy remain unchanged and accepts that GitHub still displays the legacy workflow as failed.

## Evidence retention

`WO-REB-007` evidence retains both failed C4 runs/jobs/logs, prototype results, packet approval, exact C5 paths and identities, local Linux/Windows matrices, view/evaluator evidence, hosted run/job/artifact identities, root/history hashes, and actions not performed.

## Residual uncertainty

GitHub runner/runtime changes and future predecessor schemas remain external uncertainties. This transitional lane is retired only after separately governed publication and root-evaluator adoption.
