# CLI work-to-delivery qualification — WO-IAR-029

The Codex CLI walkthrough passed on the 0.21.0 successor fixture and the 0.20.0
legacy fixture. **Codex Windows desktop delivery remains unverified**, as requested
by human mmzen. This report makes no desktop pass claim.

The product code candidate remains `e79368c677541d7092129a853e8b39157865ace9`. The product repository
continues to use released evaluator 0.20.0. These disposable repositories test
the development wheel and the legacy release without adopting either in the product.

## Observed workflow

| Check | Successor 0.21.0 | Legacy 0.20.0 |
| --- | --- | --- |
| Same native session selects the correct checkout and release | Passed | Passed after explicit switch |
| New work-order template preview, creation and completion | Passed | Passed |
| New draft validation | Zero errors and warnings | Zero errors and warnings |
| New draft remains unapproved; its note is not implemented | Passed | Passed |
| Previously authorized execution | Started once through evaluator | Resumed existing start; no duplicate |
| Exact note bytes, scope, review and Git-derived handoff | Passed | Passed |
| Local completion and clean committed candidate | Passed | Passed |
| Exact candidate/destination and human push/PR authority identified | Passed | Passed |
| Local remote unchanged; no publication | Passed | Passed |

The successor resolves guides and templates from external resources. It has no
repository entry or harness-guide directory. The legacy checkout retains its
0.20.0 repository instructions. Native resume callbacks delivered the corresponding
release in both execution phases while the host stayed in the parent directory.

The fixture work order permits an exact plain-text change and transport of the
separately prepared draft. Its approvals are explicit synthetic test inputs.
The native agent used the evaluator for lifecycle changes, retained actual tests
and handoff evidence, and left the separate draft and accepted definitions unchanged.
Independent readback confirmed one start event per work order, correct note bytes,
clean candidates, matching scope and empty fixture-remote refs.

## Exact fixture candidates

| Fixture | Candidate | Proposed destination |
| --- | --- | --- |
| Successor | `018cd804759cbee9b20e93eae5e93ddca6e95468` | `C:\Users\mathi\AppData\Local\Temp\iar29-flow5\successor-remote.git` |
| Legacy | `5260937be249c49cf9cd19ef491f6670d42cd9dc` | `C:\Users\mathi\AppData\Local\Temp\iar29-flow5\legacy-remote.git` |

Both handoffs named proposed head `refs/heads/workflow-demo`, base `refs/heads/main`
and separate human `DR-EXTERNAL-ACTION` authority. No external action was authorized
or performed by this test.

## Failures retained

An initial native attempt refused an invalid fixture work-order ID and left the
work approved but unstarted. Corrected fixtures passed preflight before their
positive runs. The trace also retains fixture setup corrections, the first capture
timeout, the missing pre-start evidence path and the recovered Windows argument
quoting failure. These failures are preserved alongside successful reruns.

## Evidence and remaining scope

[cli-workflow.json](cli-workflow.json) records the assessed results.
[cli-workflow-traces.json](cli-workflow-traces.json) retains native events, commands,
outputs, fixture artifacts, independent checks and final runner sources. Long text
is stored once under its SHA-256 and referenced by `retained_text_sha256`.

This continuation qualifies the work-to-delivery workflow through Codex CLI.
Earlier Claude delivery/recovery results remain in [native-review.md](native-review.md).
Desktop delivery is unverified; the accepted VER-IAR-021 wording is preserved.
WO-IAR-029 has not received a completion transition or a verification record.
The original plugin was restored in the disposable Codex profile after testing.

The product repository's released 0.20.0 evaluator passed complete change scope,
validation (zero errors; 54 existing warnings) and review preflight. Its current
step remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, the Git-derived
handoff check for WO-IAR-029. No product completion transition was applied.
