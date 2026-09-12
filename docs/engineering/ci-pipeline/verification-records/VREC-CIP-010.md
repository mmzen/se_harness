+++
id = "VREC-CIP-010"
type = "verification_record"
title = "Verification candidate for WO-CIP-010"
status = "verified"
owners = ["codex-preparation-actor"]
created = "2026-09-12"
updated = "2026-09-12"
commit = "07fb188b24f73187671439f34d6c39c611f83fa1"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-12T11:27:50Z"
prepared_by = "codex-preparation-actor"
artifact_snapshot_sha256 = "322cc252364769519252c87c46f2ddadf6a5c38e4a1ffbbc9830c96eb1b9e99c"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-010/WO-CIP-010-handoff.md", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/completion-ci.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/completion-decision.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/handoff.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted-checks.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Linux/rehearsal-result-1/upgrade-rehearsal-result.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Linux/rehearsal-result-1/upgrade-rehearsal-timing.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Linux/rehearsal-result-2/upgrade-rehearsal-result.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Linux/rehearsal-result-2/upgrade-rehearsal-timing.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Linux/upgrade-rehearsal-runtime.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Windows/rehearsal-result-1/upgrade-rehearsal-result.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Windows/rehearsal-result-1/upgrade-rehearsal-timing.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Windows/rehearsal-result-2/upgrade-rehearsal-result.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Windows/rehearsal-result-2/upgrade-rehearsal-timing.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/hosted/Windows/upgrade-rehearsal-runtime.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/local-checks.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-010/process-observations.json"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-010-evaluator.json"
evaluator_evidence_sha256 = "44d4b74d9febe03a0828dfeee8cd8322fd02db74ff866d7191440e17164e7abb"

verified_at = "2026-09-12T11:38:44Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-010"]
conforms_to = ["VER-CIP-006"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-12T11:38:44Z"
decided_by = "assurance-owner"
reason = "i verify VREC-CIP-010"
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-010` to candidate commit `07fb188b24f73187671439f34d6c39c611f83fa1`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Preparation scope and candidate

The operator requested "prepare the verification record" for implemented
WO-CIP-010. The released 0.17.0 evaluator prepared this record; the preparation
actor has made no assurance decision. VER-CIP-006 is the exact approved contract.

The clean candidate is `07fb188b24f73187671439f34d6c39c611f83fa1`. The four executable files are byte-identical
in Git to implementation commit `73cd1b4a4f62efa1c260863e60901fa9a321f79b`.
Subsequent candidate commits retain evidence and the implementation-completion
decision. This record and its canonical evaluator evidence are a later
governance change, so the record does not name its own commit.

The existing evidence paths retain the implementation controls and failures.
The final candidate's hosted evidence is additionally identified below by its
exact run, tested merge, runtime, observations and downloaded-byte hashes.

## Assessment against VER-CIP-006

These are preparation findings for the assurance owner's review.

| Criterion | Evidence and observed result |
| --- | --- |
| CLN01: sensitive process control | The real-Git test covers both the shared fixture and actual exporter. With automatic maintenance enabled, each positive control launches maintenance and pack-objects and creates a pack. The repaired commands launch neither automatic maintenance nor GC and create no pack. The test passed in the Windows local suite and Linux hosted suites. Process observations and raw trace hashes remain in process-observations.json. |
| CLN02: inherited settings | The regression enables parent maintenance and low thresholds, asserts disposable overrides, unchanged parent bytes and a clean valid repository. Passed on Windows locally and Linux in CI. |
| CLN03: setup and helper failures | Each refused rehearsal safety setting stops before staging or commit, retains the original error and failed timing stage, and cleans its scratch. Binary/UTF-8 output, identity, disabled signing and checked/unchecked Git failures pass. |
| CLN04: strict cleanup | Successful and failing evaluator paths and the existing injected cleanup-error test pass. Cleanup exceptions remain visible; no retry, ignored exception or process kill was introduced. All four final hosted cleanups finished. |
| CLN05: hosted handover | The final candidate's two Linux and two Windows replays pass with one semantic digest. All six evaluator steps retain their expected meanings, including predecessor refusal and observational successor validation as explained below. |
| CLN06: required checks and scope | All 17 checks pass for the final candidate. Its Linux source suite runs 1,163 tests, 4 skips, in 30.237 seconds. Distribution validation, candidate help/validate, released doctor/validate and preflight passed. The retained local failure and six candidate-template differences are explained below. The complete Git diff stays within WO-CIP-010 and its own record paths. |

## Final candidate hosted evidence

[PR #459](https://github.com/mmzen/se_harness/pull/459) passed all 17 checks for
the candidate above. [Candidate Evidence run 34690783387](https://github.com/mmzen/se_harness/actions/runs/34690783387),
attempt 1, tested merge `ed4cb7dce39484f5dadc42dc064b1130f03ad38a`.
The head and tested merge are distinct identities, both recorded by the runner.

- [Source suite](https://github.com/mmzen/se_harness/actions/runs/34690783387/job/103545510113): 1,163 tests, 4 skips, pass.
- [Linux replays](https://github.com/mmzen/se_harness/actions/runs/34690783387/job/103545677756): Ubuntu 24.04.5, Python 3.11.16, Git 2.55.0.
- [Windows replays](https://github.com/mmzen/se_harness/actions/runs/34690783387/job/103545677776): Windows 10.0.26100, Python 3.11.9, Git 2.55.0.windows.5.

| Platform | Replay | Total seconds | Cleanup seconds | Result |
| --- | --- | --- | --- | --- |
| Linux | 1 | 11.220 | 0.462 | pass |
| Linux | 2 | 11.232 | 0.416 | pass |
| Windows | 1 | 31.760 | 2.743 | pass |
| Windows | 2 | 30.055 | 2.706 | pass |

All four final replays share semantic digest
`56ac08cc7ab8738382dfddcd4219c316f8fe7cc32b189c917d7528c48e562477`. Durations are observations, not a benchmark.
Both disposable Git configuration stages finished in every replay.

In each replay, predecessor doctor before upgrade, upgrade plan/apply and
successor doctor succeed. Predecessor doctor after upgrade exits 1 as required.
Successor validation exits 1 with the existing E012 on historical VREC-PLG-008:
its evaluator evidence differs from the successor lock. This step explicitly
expects any exit status; the rehearsal retains that diagnostic as an observation.
Its passing rehearsal outcome does not claim zero successor-validation errors.
Released 0.17.0 validation of the operational candidate passes.

The two uploaded `upgrade-rehearsal-*` artifacts contain the following files.
Original downloads and the source log were retained outside the checkout.
These are SHA-256 hashes of the original downloaded bytes, without newline conversion.

| Artifact-relative path | SHA-256 |
| --- | --- |
| `upgrade-rehearsal-Linux/rehearsal-result-1/upgrade-rehearsal-result.json` | `a18285d87e9bd1e85b6789b8079e621f0a5122a8ece09e118d8a5a8654201fce` |
| `upgrade-rehearsal-Linux/rehearsal-result-1/upgrade-rehearsal-timing.json` | `69ed03eb756713288cef7ddbfbad2e85dd24f8a42e517f5175a0964add1540e3` |
| `upgrade-rehearsal-Linux/rehearsal-result-2/upgrade-rehearsal-result.json` | `a18285d87e9bd1e85b6789b8079e621f0a5122a8ece09e118d8a5a8654201fce` |
| `upgrade-rehearsal-Linux/rehearsal-result-2/upgrade-rehearsal-timing.json` | `ef8d5fc8f7051680cc7155872439e9f54ed2d80f079140a8f20cad02efbd1289` |
| `upgrade-rehearsal-Linux/upgrade-rehearsal-runtime.json` | `d34d528cd38052dd83a67d30d12051d29d869df45c432a147059f7acc4bdf092` |
| `upgrade-rehearsal-Windows/rehearsal-result-1/upgrade-rehearsal-result.json` | `ac8d35fb1bd404ebe61e2981a032c3392e0938102039afb0001e3defaf4866e1` |
| `upgrade-rehearsal-Windows/rehearsal-result-1/upgrade-rehearsal-timing.json` | `f10ff32300652d2c9de2c58607c3a4071a54b48115bbe045536dea187dfe4fad` |
| `upgrade-rehearsal-Windows/rehearsal-result-2/upgrade-rehearsal-result.json` | `ac8d35fb1bd404ebe61e2981a032c3392e0938102039afb0001e3defaf4866e1` |
| `upgrade-rehearsal-Windows/rehearsal-result-2/upgrade-rehearsal-timing.json` | `2bcbde7fd9edaf75c16b68e0bb0917e0f6c225dcf5ce9e193297211d07917467` |
| `upgrade-rehearsal-Windows/upgrade-rehearsal-runtime.json` | `227a6fb095d0a4e540d78c6bac0ee32df7afcfb1f7dbe710f4b6bf4344e56b7f` |

Downloaded source-job log SHA-256:
`ac0c55ca9752a70565c8480df7bfa449dbc3dc974d97a9157cbe78491cf4e21a`.

## Preserved failures and limits

The initial Windows suite had one unchanged AGENTS.md byte-budget failure
caused by CRLF checkout. Restoring exact committed LF bytes changed no Git
content; all 10 affected owner-region tests passed. Its other tests, including
the cleanup regressions, passed. The failed full-run output remains a failure;
the final Linux candidate suite supplies the complete green run.
An earlier misplaced test assertion was corrected and its failed development
log retained; subsequent runs cover the corrected source.

Candidate-source doctor reports six pre-existing 0.18.0-versus-0.17.0 template
differences: .engineering-harness.toml, .github/workflows/engineering-harness.yml,
ENGINEERING_HARNESS.md, ARTIFACT_AUTHORING.md, TRACEABILITY.md and
templates/WORK_ORDER.template.md under docs/engineering where applicable.
Released-evaluator integrity passes; managed files were not overwritten.

The controlled evidence establishes suppression of automatic Git maintenance.
It does not identify the writer in the two historical PR #456 teardown failures
or exclude every possible filesystem writer. Those failures remain retained.
Historical release replays still use their historical fixture code. No plugin
qualification criterion, accepted C10/C11 limitation, or existing VREC/RLS was changed.

## Pending decision

VREC-CIP-010 remains ready; WO-CIP-010 remains implemented and VER-CIP-006
remains approved. The next step is the assurance owner's decision on this
record. No verification, merge or release decision is recorded by preparation.

## Assurance decision

The accountable operator explicitly stated "i verify VREC-CIP-010".
The released 0.17.0 evaluator applied the assurance-owner decision at
2026-09-12T11:38:44Z, changing only VREC-CIP-010 from ready to verified.
The candidate remains `07fb188b24f73187671439f34d6c39c611f83fa1` and all preparation
bindings and retained evidence remain unchanged. The pending-decision
text above describes the earlier preparation state.

WO-CIP-010 remains implemented; VER-CIP-006 remains approved.
Repository integration and release remain separate decisions.
