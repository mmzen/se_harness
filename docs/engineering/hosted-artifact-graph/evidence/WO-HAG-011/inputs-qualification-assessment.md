# Authoring and Codex qualification — 10 October 2026

The approved Codex environment works for native CLI tests. Qualification remains
incomplete: Claude's missing-input case still fails content review, and positive
Claude authoring still misses the efficiency goals. WO-HAG-011 stays **in progress**.
No verification request or completion is made.

Candidate: `a2499d21f154e7682ff160cc122a72dd597936a3`.

## Applied changes and authority

mmzen approved the bounded Windows test amendment. Its [activation record](codex-permissions-20261010/activation.json)
links the exact preserved accepted VER-HAG-008 and WO-HAG-011 to their replacements.
Earlier approval/start events and failed trials remain unchanged. The previous
assessment's unapplied proposal is historical; this assessment records its application.

The native driver now exposes an explicit session-only Codex profile. The selected
local service is reachable, workspace writes work, outside writes are denied, and
the tested external proxy and direct connections are denied. The managed proxy
allows no external destinations. MXC can expose other loopback services: this is
not port-level isolation. The helper fixes the selected endpoint/project. Each
Codex test has its own retained boundary probe. No global settings, app restart,
desktop-app termination or host-plugin installation was used in this amendment.

The hosted guide now puts input sufficiency before mutation and removes conflicting
single-file read wording. It is 900 words, down from 906: a small edit, not a major
size reduction. Candidate14's validation label and bounded batch reader remain.
The label distinguishes shape/link admission from unassessed content quality.

## Native results on this candidate

| Trial | Case | Independent content result | Seconds | Calls | Peak input tokens |
| --- | --- | --- | ---: | --- | ---: |
| [claude-91](claude-91-assessment.json) | Missing inputs | fail | 304.362 | 19 | 59,565 |
| [codex-91](codex-91-assessment.json) | Missing inputs | pass | 120.868 | 12 visible items; exact count unavailable | Unavailable |
| [claude-92](claude-92-assessment.json) | Positive contract | pass | 286.940 | 21 | 57,952 |
| [claude-93](claude-93-assessment.json) | Positive contract | pass | 247.157 | 20 | 57,592 |
| [claude-94](claude-94-assessment.json) | Positive contract | pass | 249.398 | 21 | 58,929 |
| [codex-92](codex-92-assessment.json) | Positive contract | pass | 193.065 | 17 visible items; exact count unavailable | Unavailable |

Claude91 correctly reports incomplete input but saves the false claim that no
recorded intent or governing artifact exists. Its own report acknowledges the
existing definitions. That contradiction fails EFF-04A. One create call used a
project ID as a context ID and failed; the agent recovered through import and
draft-open. Both the failure and saved document remain in the evidence.

Codex91 reads the existing definitions and stops with the missing distinct
operational benefit and agreed measure. No mutation occurred; the independent
final project version is zero. This is a correct negative result, not successful
positive authoring or a speed comparison with completed drafts.

Claude92's contract passes independent review, but its report omits a recovered
failed create call. The independent assessment preserves that failure. Claude93,
Claude94 and Codex92 have no observed failed call. Codex92 also passes content
review: its alternative draft defines the exact comparison, input identities,
failure outcomes and evidence filename without claiming execution. Each saved positive draft is read independently and
compared with submitted bytes. All seven imported records remain unchanged.
The per-trial assessments record further findings, including the final repetition
and Codex positive result; native self-assessments are not the independent verdict.

## Cost and simplicity findings

Comparable positive Claude runs use the same candidate, task, fresh-project work,
permissions and `claude-opus-4-6`. Their full ranges and medians are:

- wall_seconds: 247.157–286.94; median 249.398.
- native_calls: 20–21; median 21.
- peak_input_context: 57592–58929; median 57952.

Goals remain less than 180 seconds, at most 15 calls and less than 40,000 peak
input tokens. They are measured separately from content correctness. Codex's
JSON stream does not supply an exact native-call total, model-turn count or peak
input context; visible completed items are a lower bound. No values are inferred.
Codex92 takes 193.065 seconds and has 17 visible tool items, so it misses the time
and call goals; its context goal is unavailable. Claude91's original assessment
has a null `native_tool_calls` alias; its retained primary summary's `native_calls`
is 19, which is the value used in this comparison.

Claude93 makes ten Read calls, one Skill call, seven Bash calls and two Write
calls. Only 7.015 seconds are captured inside client commands out of 247.157
seconds wall time. The rest is unclassified; it is not measured model time.
No repeated read path is observed in that run, but separate known-path reads
still add turns. The batch reader exists and was not used in that run.

The focused entry retains nine exact canonical sections (27,097 bytes), and the
whole task file is about 30 KiB before the separate tool guide and hosted guide.
Claude begins with 15,661 provider-reported input tokens. Removing six guide words
cannot explain or solve a roughly 58k-token peak. Exact host/task/package identities
and the actual calls are retained in [the comparison](candidate15-comparison.json).
Opus10 remains historical; its intent task is not a comparable positive benchmark.

The evidence supports three next correction targets, without adding a new framework:

1. Fix the contradiction between source facts and authored problem statements.
   A readiness label alone did not prevent invented absence claims. Keep the
   original missing-input task and independent review; do not insert its answer.
2. Use the existing batch reader for already-known independent files, and remove
   duplicated identity/report prose where the exact evidence already holds it.
   Keep dependent mutations explicit and ordered.
3. Inspect the canonical sections selected for this narrow authoring task. Reduce
   unnecessary reading at its source rather than add more warning paragraphs.
   Any changed accepted instruction meaning or new implementation path needs its
   own bounded amendment; this report does not apply one.

## Technical checks and evidence

The source suite passed: 1,336 tests, 24 skips. Native-support tests: 25 passed.
Distribution checks, CLI smoke, exact reproducible Linux producer builds, package
installation, instruction fidelity, released validation (1,991 artifacts, zero
errors, 63 warnings), scope and review preflight passed.

Native durations include the whole agent session and exclude package/service
preparation. The recorded source-suite wall time is 165.672 seconds. Build and
package records retain commands and timestamps; their aggregate elapsed time was
not captured and is unavailable. It is not counted as zero.

Real installed-client EFF-02/03 checks pass for typed/raw request equivalence,
exact bytes, stale versions, reused keys, capture failure after acceptance and
lost-response recovery. The final project version is six with no duplicate
mutation. These transport fixtures do not establish native content quality.
The component comparison bounds reuse to unchanged service, dependency and
governor bytes; changed client presentation has fresh installed-client evidence.

The [check archive](candidate15-checks.zip) and [inventory](candidate15-checks-inventory.json)
retain actual commands, results, source/build/package identities, selected-service
boundary probes, independent reads and preparation failures. Each native trial
has a separate `TRIAL-evidence.zip`, visible transcript and inventory. Credentials,
raw host events and private reasoning are omitted. Known test tokens were checked
absent. Owned test containers were stopped after assessment; their volumes remain.

## Delivery and remaining work

PR #543 remains a draft against main, with complete comparison base
`55caaada508495bea7d97effd27644d1ce8373da` and WO-HAG-009/010/011 declared.
At remote `15530192ba0a230c34384b98d86e4ffeb21055ba`, Engineering Harness CI fails
`WO-HAG-009 / QGP-G4I-EVIDENCE` for missing handoff evidence at the current formal
snapshot. Other completed checks passed; the release-rehearsal legs were skipped.
The same known blocker is disclosed, not hidden by changing the comparison base.
New publication-head CI must be read separately.

Full VER-HAG-007 NQ-01–05 remains incomplete. These explicit CLI trials do not
qualify automatic startup, compaction or Windows desktop delivery. Git remains
authoritative. No VREC, verification acceptance, merge or release is claimed.

The released evaluator's current step is `STEP-WO-IMPLEMENT-CHECK` under
`PROC-WO-IMPLEMENT`. Continue the bounded content correction and retain its actual
results before attempting completion or verification preparation.
