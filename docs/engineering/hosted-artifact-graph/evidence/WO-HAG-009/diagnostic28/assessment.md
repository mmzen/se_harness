# Focused Claude hosted lifecycle diagnostic — 11 October 2026

The corrected test reached its targeted outcome: Claude authored a work order,
recorded a risk and its paired decision, obtained a passing handoff and completed
the synthetic work. Six accepted lifecycle operations passed independent replay
with the released 0.22.1 evaluator. The session still reached its 15-minute limit.
This is useful functional evidence, not a clean native-session or full
qualification pass. Efficiency remains inadequate.

WO-HAG-009 and WO-HAG-011 remain in progress. No real work order was completed,
no VREC was prepared or accepted, and no merge or release is requested here.

## What changed

Candidate `dfcf1e976123836f00354a228c8e72a833f2e3cf` changes two plugin references
and the test tool index. The guidance names 15 exact released instruction
sections and nine request-schema locations. It also clarifies the helper's
test-copy handling, paired decision target and accountable actor field.

The [correction review](../../WO-HAG-011/lifecycle-correction28/review.md) retains
the exact scope and checks. No service runtime, evaluator policy, permission or
acceptance criterion changed. This correction makes routes more precise; its
instruction text is not claimed to be shorter.

## Test design and preserved setup error

The first diagnostic, `claude-231`, was invalid. I supplied imported draft
records and asked Claude to perform lifecycle actions on the imported work
order. The service correctly protects imported records from those writes. I
stopped that run after 412.963 seconds and 48 tool calls. The project stayed at
version 2 with no accepted lifecycle apply operation. The refusal and failed
attempt to replay an empty accepted-operation set remain in the evidence.
This was my test-design error, not evidence of a service defect.

The corrected diagnostic, `claude-232`, uses a new project and a separate small
fixture. The proctor approved six synthetic governing definitions through the
released evaluator before import. The fixture commit is
`29837fc72d3301e7b59b7c628262f3ad2931517b`; it does not approve repository work.
Claude then had to author its own editable WO-P3-001 and all its requests. It
received synthetic test-owner/test-executor authority and the requested risk
choice, but no completed request or help during execution. The imported
WO-P3-900 stayed unchanged. The fixture greeting was already implemented.

This narrower task excludes fresh authorship of the six governing definitions,
VREC/RLS preparation, planned failures/retries, MCP parity and native exports.
It is not comparable to the prior full NQ/EFF workload and cannot establish a
speed improvement over that workload. The 900-second limit belongs to this
diagnostic; no approved full-qualification limit was changed.

## Observed result

| Operation | Observed result |
| --- | --- |
| Import and draft authoring | Imported approved definitions; created and completed a new work-order draft. |
| Synthetic approval and start | WO-P3-001 reached approved, then in_progress. |
| Greeting assertion | Passed: the existing function returns exactly `Hello rehearsal`. |
| Risk creation | RISK-P3-001 and paired DEC-P3-001 created. |
| Risk decision | `mitigate` accepted for DEC-P3-001; risk became mitigating. |
| Handoff | Evidence and complete declared change set accepted. |
| Work completion | WO-P3-001 reached implemented. |
| Final service state | Project version 10; context version 8. |
| Session | Timed out after 900.063 seconds; exit 1. Both report files were retained before timeout, but no normal terminal response completed. |

The independent assessor replayed approval, start, risk creation, decision,
handoff and completion. All six matched released-evaluator semantic results
and exact file effects. Receipt lookups bound each request to the observed
service operation. This partial replay does not independently qualify every
draft-authoring operation or the omitted NQ cases. Proctor exports used for
replay do not count as native exports.

Two refused requests were recovered without assistance:

- A draft-context request named nonexistent WO-P3-901. Claude selected the
  existing baseline work order to open the context and created a new work
  order inside it.
- Start preflight used `preview` instead of the required read mode `inspect`.
  The corrected request succeeded.

The native report records both errors, but its later “Refusals: None” statement
is inconsistent with them. Its “Unresolved limits: None” does not establish
completion of the host session or full qualification. Those original statements
remain unchanged in the evidence; this assessment supplies the actual limits.

## Cost and remaining problem

The run made **70 tool calls**: 21 reads, 32 Bash calls and 17 writes. Its peak
input context was **144,984 tokens**. These are neither the size of one artifact
nor total billed tokens.

Matched provider timestamps cover all 70 tool calls. Their nonoverlapping
intervals total **48.458 seconds**. The other **851.605 seconds** occurred outside
those intervals. That time is not separately attributable to model generation,
provider waiting, compaction or host work. It must not be called measured
reasoning time. See [the exact timing metadata](timing.json).

The service ran through localhost Docker, not a WAN deployment. The evidence
does not show a graph-database bottleneck and supplies no matched local-artifact
benchmark. Exact pointers helped the selected operations succeed, but manual
request construction and long model-mediated sequences remain. The earlier
[slowness RCA](../slowness-rca-20261011/RCA.md) remains applicable.

## Checks, identities and boundaries

Candidate checks passed: 15 instruction selectors and nine schema pointers,
40 focused tests, the 1,337-test source suite with 24 reported skips, distribution
checks, CLI smoke and reproducible package preparation. Earlier Windows temp
and observer-command failures remain retained alongside the successful checks.
No skipped test is counted as a pass.

The selected client is 0.22.2; the plugin is session-loaded candidate 0.2.7; the
service is 0.1.0.dev1; the governor remains separately installed public 0.22.1.
The [provenance inventory](provenance-inventory.json) binds their exact packages
and image. Compared with candidate27, runtime source paths were unchanged and
all 127 extracted client-wheel members match. Archive and server image identities
are still recorded separately; this comparison grants no new qualification pass.

Staged input digests remained unchanged. Before/after observations match for the
selected noncredential host settings and repository HEAD/tracked state. Both
disposable trial container sets are stopped, with volumes preserved. The active
Codex application and host plugin were not changed.

## Evidence and next step

- Invalid setup: [visible transcript](claude-231-visible.md), [exact records](claude-231-evidence.zip), [inventory](claude-231-inventory.json).
- Corrected diagnostic: [visible transcript](claude-232-visible.md), [exact records and replay](claude-232-evidence.zip), [inventory](claude-232-inventory.json).
- Package/fixture provenance: [archive](provenance.zip), [inventory](provenance-inventory.json).
- [Review-check archive](report-checks.zip) and [inventory](report-checks-inventory.json) retain selected scope, preflight and released validation.

Private provider reasoning, account stores, tokens and raw provider streams are
excluded. Original local records are preserved; archive entries retain their
exact bytes and hashes.

The released evaluator still selects **STEP-WO-IMPLEMENT-CHECK** for real
WO-HAG-009 and WO-HAG-011: retain and assess implementation evidence. Full native
qualification for both hosts and the efficiency criteria remain pending. This
diagnostic does not justify work completion or a verification request. The next
correction should reduce the remaining manual lifecycle-request and result
handling before another expensive full run. New typed lifecycle commands would
need a bounded artifact proposal; this update does not authorize them.

PR #543 stays draft with the original main comparison base and its missing
WO-HAG-009 handoff evidence disclosed. Its existing unfinished-work publication
grant is reused; no gate or criterion is waived.
