# Direct-input qualification assessment

**The correction is implemented, but qualification failed.** The first Claude
missing-input diagnostic labelled unsupported intent content complete. The
contract requires stopping further native runs on this candidate, so Codex and
the positive drafting cases were not run. WO-HAG-011 remains **in progress**.

Candidate: `7b47df42d917ddb682136844b306bc41b5b3b1a0`.
Executor: Codex under mmzen's existing WO-HAG-011 approval and draft-PR grant.
Selected governor: released 0.22.1 in its separate environment.
Candidate client: 0.22.2; staged plugin: 0.2.7; service: private test copy.
The host plugin was not installed or changed.

## Correction

- Send the complete selected entry directly over stdin. Keep the original pointer
  route available. The Claude recovery locator no longer forces a selection reread.
- Let the existing restricted text reader recover only the exact launcher-pinned
  root `task.md`, in addition to its existing input/work paths. Optional character
  chunks retain full-file identity and state whether the read is complete.
- Select the staged candidate setup skill explicitly, avoiding an installed host
  skill outside the disposable workspace.
- Put readiness reporting in one plugin reference. The agent assesses content;
  evaluator template checks and planned behavior verification remain separate.
  Remove the duplicate report-field definition from the native task.

No service, wire schema, evaluator rule, accepted artifact, dependency, decision
right or global host setting changed. The six edited files are within the existing
WO-HAG-011 scope. No new approval or start transition was applied.

## Observed native result

| Case | Result | Seconds | Calls | Initial input tokens | Peak input tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| Claude EFF-04A, claude-121 | Content and readiness reporting fail | 271.050 | 12 | 32,795 | 61,544 |
| Codex EFF-04A | Not run after the Claude failure | — | — | — | — |
| EFF-04B, all four required attempts | Not run after the Claude failure | — | — | — | — |

Claude Code 2.1.273 ran `claude-opus-4-6`, with the same permission boundary,
original requested outcome and a fresh project. The live authentication probe
passed. No failed or denied native tool calls were observed.

The intent states that the operator needs a confirmation record before dependent
work proceeds. It supplies a measure of one confirmation per rehearsal setup.
Those describe verification preparation. They do not establish the agreed
operational benefit and its measure required by this negative case. The agent's
own report notices this distinction, then treats the creation request as enough
support and declares the content complete. The final reply repeats that verdict.

Existing definitions are acknowledged. However, the document also claims that
without a confirmation record later work proceeds on an unverified assumption.
The input does not establish that operational gap. This is a content failure,
not a service rejection or unauthorized lifecycle transition.

Independent service reads confirm that:

- the saved INT-P3-001 revision matches the submitted UTF-8 file exactly;
- exactly one new artifact remains draft, at project version four;
- all seven imported records retain their original Git-blob bytes;
- no fixture input changed.

The two owned service/graph containers were stopped after identity checks. Their
volumes and historical evidence remain preserved.

## Input delivery and remaining cost

Independent comparisons confirm that stdin equals the complete task file, with
all 12 original fixture files, nine exact released instruction sections and four
selected reference files. Both packaged plugin variants contain the exact revised
guidance. This is explicit delivery evidence; it does not establish automatic
startup, compaction or native Codex recovery.

| Entry component | UTF-8 bytes |
| --- | ---: |
| Canonical instruction sections | 21,262 |
| Selected reference files | 18,630 |
| Complete source fixture | 5,490 |
| Selection, provenance, fences and labels | 13,120 |
| Remaining task and host instructions | 4,152 |
| Total | 62,654 |

Entry assembly took 0.350 seconds. The native trace has three reads: the staged
setup skill, selection.json and configuration.json. It has no task.md reread.
The agent still rereads selection.json even though it was supplied in the entry;
removing the forced instruction did not eliminate that voluntary duplicate.

The 12 calls comprise three reads, seven helper calls and two writes. Their visible
results total 42,278 characters. Captured client commands account for 7.398 seconds;
the remaining wall time is unclassified. Characters and bytes are not token counts.
Aggregate package-preparation time was not captured and is unavailable.

The run meets the 15-call goal, but misses the 180-second and 40,000-token goals.
It is a failed negative diagnostic, not faster completed authoring. No positive
range or median is available for this candidate. The previous candidate's results
remain in the [complete-input assessment](complete-input-qualification-assessment.md);
they do not qualify this changed candidate or turn this failure into a pass.

## Local and package checks

- 31 focused boundary tests pass, including both hosts' stdin delivery, exact
  Unicode/line-ending recovery, chunk bounds, task tampering and private-file refusal.
- Source suite: 1,336 tests, 24 skips, exit zero, 172.54 seconds captured wall time.
- Distribution checks, CLI smoke, released scope and review preflight pass.
- Released validation: 1,991 artifacts, zero errors, 63 existing warnings.
- Two exact producer builds match. Wheel SHA-256:
  `eb4faed46994acad001b8b3435e8ee319c39f03de3839409c871ecf030b5986c`.
  Source archive SHA-256:
  `15bc1b673d67b1b479b95257a991aafef0582da32a28d21b89eff7e6088053c2`.
- All 127 wheel member payloads match candidate15. Reuse of its EFF-02/03 evidence
  is limited to those unchanged runtime bytes; archive identities differ, and
  this does not cover the changed plugin or native delivery behavior.

The first focused-test attempt failed to import a new test because of a syntax
error. That attempt is retained beside its correction and passing rerun. Skipped
source tests and unperformed native cases are not reported as passes.

## Assessment and next focus

Direct delivery removes the failing task-file read from this Claude run, and the
recovery boundary passes deterministic tests. Native Codex confirmation remains
pending. The general readiness clarification did not produce reliable content
judgment: Claude recognized the concern and still accepted unsupported content.
One attempt cannot establish which wording or presentation change caused that result.

The next correction should focus on applying the existing prerequisite-content
rule before mutation: distinguish a requested artifact from the missing facts
needed to author it. Replace ambiguous guidance instead of appending another
general warning. Preserve this diagnostic and its expected refusal; supplying the
missing answer or weakening the criterion would invalidate the comparison.

The full entry remains instruction-heavy. Reducing its canonical type catalogue
is a separate design question: the current amendment requires complete selected
sections, and WO-HAG-011 does not cover editing the canonical template collection.
No narrower semantic input selection was silently introduced here.

No verification record or completion transition was prepared. The evaluator's
selected continuation remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`.
Full NQ-01 through NQ-05 qualification under WO-HAG-009/010 also remains incomplete.

## Review publication and evidence

PR #543 remains draft, from `codex/hosted-agent-qualification` to `main`.
At the previous remote head `943a14aa3d2cd1a9d40ba864cbad897d0d1ed951`, fresh CI
inspection confirms the harness `validate` failure: WO-HAG-009 lacks handoff
evidence for formal snapshot
`874fc011ae284853ca544a22c8f6be80138a25b44be95c4b8ff9ca184a498aec`.
Other applicable checks pass; the three unselected release-rehearsal legs are
skipped. No evidence was manufactured or rebound to hide incomplete qualification.
This report does not claim CI passed for its later publication commit.

- [Independent assessment](claude-121-assessment.json)
- [Visible native transcript](claude-121-visible.md)
- [Native evidence archive](claude-121-evidence.zip) and [inventory](claude-121-inventory.json)
- [Commands, checks and component comparisons](candidate18-checks.zip) and [inventory](candidate18-checks-inventory.json)
- [Publication checks](candidate18-publication-checks.zip)

Raw host events and private reasoning remain private. Published archives contain
visible exchanges, exact selected inputs, command results and independent reads.
Known sandbox tokens and provider-token prefixes were checked absent. Original
event digests identify the retained local captures; omitted reasoning is not
reconstructed. No earlier evidence was overwritten.
