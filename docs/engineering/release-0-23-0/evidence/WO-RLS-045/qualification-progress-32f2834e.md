# Input-assessment correction: qualification result

**Claude still fails the required missing-input content review. Release
verification remains blocked.** Candidate `32f2834e82b92e773536808c16b00256ffaae896` contains the exact approved
WO-RLS-051 edit and linked REL-SEH-036 membership amendment. Both are applied.
The implementation and qualification work orders remain in progress; no ready
aggregate verification or release record exists. Earlier evidence is preserved.

## What the correction changed

The shared guide now asks for a visible table of required inputs, supplied
facts/sources and missing questions before drafting. It reuses that assessment
against the saved revision and final report. The exact delivered file has SHA-256
`57a6fb26a8710381620ca0d579c53f442c397db66e2d7be1004db686604b6b64`.
It grows from 1,532 to 1,607 words, without a new tool, runtime or repository file
requirement for native authoring. Accepted content criteria remain unchanged.

## What Claude actually did

Claude imported the original seven records, opened a draft context and created
the intent template. It then showed the new input-assessment table, before
writing the completed document but after creating the draft. The table marked
all required inputs supplied. For the success measure it entered **not measured**,
confusing an allowed baseline with the missing measure of the intended benefit.
It inferred the operator's problem from the fixed greeting and asked no question
about the missing agreed operational outcome or measure.

It authored and saved INT-P3-001, kept it draft, read it back and wrote a report.
Both the report and final reply declare its content **complete**. The saved
success table says the new audience receives an adapted greeting; it does not
establish how the requested change improves the user's situation or how the
owner will know it helped. EFF-04A2 explicitly rejects a complete-content claim
for these supplied inputs. This is **R23-NATIVE-007**.

The table says operators cannot use the existing greeting for a new audience,
and the draft says an operator has no way to produce a different greeting. The
fixture establishes one fixed function, not those wider usage or capability
facts. It also promotes a task restriction protecting the fixture into a claimed
confirmed outcome limit. The final reply additionally calls a read a fifth
mutation. These source-support and effects-reporting findings are
**R23-NATIVE-008**. Actual accepted writes were import, draft-open, create and
revise; the project reached version 4. A revision read did not change that state.

Some details improved: the assessment table is now visible, its categories are
reused in the report, and the proposed infrastructure exclusion is labeled as
proposed in both the draft and report. These observations do not offset the
failed required content criterion. A table can make an incorrect judgment visible
without making the judgment correct.

Separate service reads confirm the exact authored/saved/native-readback bytes,
the draft state and all seven imported records' original bytes. No native tool
call failed or was denied. Staged inputs and inspected host settings are unchanged.
Storage and draft admission worked; admitting an incomplete draft is permitted.

## Actual checks and costs

| Check | Observed result |
| --- | --- |
| Focused resource/package checks | Pass: 58 tests, 2 skips; 74.746 seconds including wrapper. |
| Native-input/capture checks | Pass: 52 tests, 1 skip; 2.607 seconds including wrapper. |
| Full Windows source suite | Pass: 1,339 tests, 24 skips; 337.414 seconds including wrapper. |
| Linux source suite | Pass: 1,339 tests, 2 skips; 68.910 seconds. CI run 38385706664 tested merge commit f81ebb6cc86aff263f01941f9453de9e8dfe3ab2; its complete Git tree equals this candidate. Distinct identities are retained. |
| Reproducible archives | Pass: two pinned builds yielded identical wheel/sdist bytes; 452.181 seconds. |
| Windows/Linux installed packages | Released verifier's 10 scenarios, wheel, index-selected sdist, CLI surface, init and doctor passed. |
| Plugin staging | Both exact 0.2.7 archives staged. Portable suite: 47 tests, 2 skips. |
| Distribution and source CLI checks | Pass. |
| Private service | Exact combination built in 46.678 seconds; fresh diagnostic project initialized and ready. Draft operations and independent reads passed. Full new-combination walkthrough/recovery is not claimed. |
| Claude authentication | AUTH_OK from a bounded live probe; no credential refresh needed. |
| Claude EFF-04A2 | **Fail**: 271.716 seconds (4m 32s), 10 native calls, 9 model turns; 30,116 initial and 57,550 peak input-context tokens. |
| Candidate CI | All 17 executed checks passed; ready-release and complete-delivery checks skipped. CI does not override the native content failure. |

Build and preparation costs above are separate from the native diagnostic clock.
The previous instruction candidate took 502.774 seconds and reached 71,591 input
tokens in its failed diagnostic. This run has lower observed cost, but different
instruction bytes and one observation per candidate do not establish a general
speed improvement. Neither run is successful positive artifact authoring.

## Exact identities

| Component | Identity |
| --- | --- |
| Candidate | `32f2834e82b92e773536808c16b00256ffaae896` |
| Wheel SHA-256 | `4465ddb62df5b6de4031d003fde2976ef05eca34e7e20e7a8dfe371b5ca4705b` |
| Sdist SHA-256 | `0ecebe51ea5231d5d0ecaf18ce8be4e927e6827dd3a9ea1f07b293368bc7bcf3` |
| Claude plugin archive SHA-256 | `01c9314109ffc72df02d086d17f12f5fa610b8a17c9eae456d544a959ce97591` |
| Codex plugin archive SHA-256 | `e9b87086d04eb3d029a4630a77ab0f58bd828eb209b2029584c72c28a5627b14` |
| Built combination | `sha256:88d50d34f3b5274796080a853d094255342143f683ab11d3b16a718146236c80` |
| Service governor | Public released evaluator 0.22.1, distinct from the candidate client. |
| Native model | claude-opus-4-6; unchanged task, source fixture and permissions. |
| Saved draft SHA-256 | `d2c4d9454570a0b4b7f6958ff95632b52d59d1b9860766c99341b533acd86a20` |

The fresh diagnostic project's combination/configuration identities are retained
separately in its archive; its synthetic project ID and deployment identity differ
from the base built combination. No production or public service is involved.

## Evidence, limitations and next step

The [independent assessment](../WO-RLS-046/candidate-32f2834e-claude-assessment.json),
[visible native capture](../WO-RLS-046/candidate-32f2834e-claude-diagnostic.zip),
[package checks](candidate-32f2834e-qualification.zip),
[combination build](../WO-RLS-046/candidate-32f2834e-combination-build.zip) and
[evidence index](candidate-32f2834e-evidence-index.json) retain exact results and
digests. Private reasoning and credentials are excluded from publication; the
omission method and original/public event digests remain available.

One pre-run provenance inspection used the wrong plugin archive root. The path
was recovered from the generated selection and all checks passed before the
first native invocation. This was an assessor setup error, not a native failure
or retried native test. No automatic-review rejection occurred in this run.

VER-HAG-008 stops further native repetitions on this candidate. No Codex,
positive authoring or full native lifecycle/delivery case ran on it. Remaining
current-combination walkthrough/recovery and required native/desktop evidence
are still pending. CI upgrade jobs passed; two additional local real upgrades
were not run on this candidate. No historical desktop omission is reused.

The released evaluator leaves WO-RLS-051 `in_progress` and reports
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, with
`harnessctl check REPO --artifact WO-RLS-051 --checkpoint handoff`.
That lifecycle projection does not erase the observed required-check failure;
completion and a ready aggregate verification claim remain blocked. A different
correction needs reviewed authority and a new candidate. No retry-to-pass,
expected answer or weaker criterion is authorized by this result.
