# Source-grounded drafting: qualification result

**Both missing-input diagnostics pass. Positive drafting remains blocked by the
64 KiB complete-input limit. Release verification is not ready.**

Candidate `05c629ddfc0f40924823160d8aaf0fa4e77940a2` contains the exact approved WO-RLS-052 guide change and the
approved REL-SEH-036 membership amendment. The guide decreased from 1,607 to
1,588 words. It requires requester confirmation and direct source support for
required inputs, separates baselines from success conditions, and distinguishes
accepted writes from reads. No content criterion, model, fixture or permission
was weakened. Work remains in progress; previous failed candidates keep their verdicts.

## What the native tests established

| Case | Independent result | Observed cost |
| --- | --- | --- |
| Claude EFF-04A2 | Pass. Identifies the missing audience/problem, wanted benefit and success condition. Asks clarification, says Incomplete and attempts no hosted mutation. Its complete two-call capture supports use of the retained final reply as the report. | 154.206 seconds; 2 calls; 2 model turns; 30,097 initial and 34,602 peak input-context tokens. |
| Codex EFF-04A2 | Pass. Distinguishes the existing definitions from the new request, asks for the missing outcome and scope, and saves the required report because capture is incomplete. Failure claims remain limited to observed calls. | 134.790 seconds; 6 visible calls as a lower bound. Exact total calls, model turns and input-context values are unavailable. |
| Claude EFF-04B | Not run. Both preparation attempts refused oversized inputs before provider invocation. | Preparation only; no native authoring duration or content result. |

Separate HTTP reads confirm that both diagnostic projects remain at version 0.
Their staged fixture bytes and inspected host settings are unchanged. No new
artifact, import baseline or saved hosted revision exists in these diagnostic
projects. Correct clarification is not evidence of faster successful authoring.
Claude used claude-opus-4-6. Codex used its unmodified configured default
(gpt-6-astra/high); no equivalent-model historical speed comparison is claimed.

The Codex boundary probes passed: selected loopback service reachable, external
proxy and direct connections denied, workspace writable, outside sentinel
protected. This is not port isolation. Host warnings about icon paths, unsupported
PowerShell snapshots and the legacy_notify after-agent hook (Windows error 206)
remain in the capture. They are separate from the successful visible native tools.
This does not qualify desktop or automatic instruction delivery.

## Positive-case blocker

The positive case uses the same nine instruction sections, complete original
fixture and accepted task as the previous qualified trial. Its prior prompt was
64,750 bytes. Current reference content is 29,026 bytes, versus 26,935 in that
prior trial. Reference growth and longer absolute paths push the new prompt over
the fixed 65,536-byte boundary.

| Prepared location | Complete prompt | Result |
| --- | --- | --- |
| Normal qualification directory | 67,571 bytes | Refused; 2,035 bytes over limit. |
| Short ordinary temporary directory | 66,163 bytes | Refused; 627 bytes over limit. |

The refusals occur before the provider starts and before native capture is
created. Neither is a failed Claude content attempt or a native retry-to-pass.
No input was truncated, expected answer supplied, or pointer fallback used.
Both fresh setups and the error records are preserved.

Two assessor setup errors are also retained: a provenance helper was first run
from the wrong working directory, and the sandbox redirected a temporary folder
to a location whose child creation was denied. Corrected provenance passed;
ordinary host temporary storage was then used. A live Codex-log reader also
initially treated warning lines as JSON and was corrected. These did not change
the candidate or affect the native agents. No automatic approval rejection occurred.

## Checks and exact identities

| Check | Observed result |
| --- | --- |
| Focused resource/package checks | Pass: 58 tests, 2 skips; 73.820 seconds including wrapper. |
| Native-input/capture checks | Pass: 52 tests, 1 skip; 2.636 seconds including wrapper. |
| Windows source suite | Pass: 1,339 tests, 24 skips; 329.183 seconds including wrapper. |
| Linux source suite | Pass: 1,339 tests, 2 skips; 62.774 seconds. CI run 38404995414 tested merge commit c2ab1e14acd23334c20c80d12d4953c215cb68f5; its full tree equals the candidate. |
| Reproducible archives | Two pinned builds produced identical archives; 441.273 seconds. |
| Windows/Linux packages | Exact wheel and index-selected sdist checks, installed CLI surface, init, doctor and released verifier's 10 scenarios passed. |
| Plugin packages | Both exact 0.2.7 archives staged; portable suite passed 47 tests with 2 skips. |
| Distribution and source CLI checks | Pass. |
| Private combination | Built in 44.528 seconds. Fresh diagnostic services initialized and ready. Full walkthrough/restart/restore is not claimed. |
| Candidate CI | All 17 executed checks passed; ready-release and complete-delivery legs skipped. |
| Released validation | 2,008 artifacts, zero errors, 63 existing warnings. |

Build and preparation time is separate from native duration. Current package identities:

- Wheel: `745b2a53d11157e07ec9c80348c80e3c0b0a68214e2c98c59f522aa7119f064a`.
- Sdist: `385a85bb2b86e1736b50819c8271222faec83c59c53031ba80628f676e2dc527`.
- Claude archive: `8288b3812b4f0b01da5e834165096f7d145b022ad5cb1d8574f08135fad62222`.
- Codex archive: `e986f9ff1e554e0864d08d3e0d845fda25e95ff066b82baa992cac64cb11cb44`.
- Base built combination: `sha256:82394285405363315df44de9615bcd5e710437572aebcb8331238e1f0e324554`.
- Guide: `09912f982b0dbcaadcd3d79f895d91aa83fb3de0f1a32d45f666de8400879be6`.

Each fresh project has its own retained deployment/combination identity. Released
0.22.1 governs the real repository and private service; 0.23.0 is the tested client.
Git remains authoritative. Exact source equivalence with the preceding candidate
is recorded as such; it does not automatically carry forward service qualification.

## Smallest proposed follow-up

Keep the successful source-support correction and the 64 KiB refusal. Reduce the
drafting tool guide's initial content by moving non-drafting command detail to
referenced files read when required. The current native-tools.md is 8,684 bytes.
Preserve every original fixture file, applicable rule, command capability and
source identity. Do not replace complete source content with a semantic summary.

Before implementation, prepare a bounded work order for the exact guide/reference,
staging and regression-test paths. Test both hosts' complete positive entries at
ordinary Windows paths without starting a provider, then rerun affected native
cases on the new exact candidate. This should remove unnecessary initial content
instead of depending on extremely short temporary names or increasing the limit.
The proposal is not an applied correction or an authority to change the contract.

## Evidence and remaining work

The [Claude assessment](../WO-RLS-046/candidate-05c629dd-claude-assessment.json),
[Codex assessment](../WO-RLS-046/candidate-05c629dd-codex-assessment.json),
[evidence index](candidate-05c629dd-evidence-index.json),
[Claude capture](../WO-RLS-046/candidate-05c629dd-claude-diagnostic.zip),
[Codex capture](../WO-RLS-046/candidate-05c629dd-codex-diagnostic.zip) and
[prelaunch evidence](../WO-RLS-046/candidate-05c629dd-positive-prelaunch.zip)
retain observed effects and limits. Credentials and private reasoning are omitted
from publication; original/public digests and omission methods are retained.

Positive repetitions, the Codex positive case, full native lifecycle/delivery,
current-combination walkthrough/recovery and separate desktop evidence remain
pending. CI upgrade jobs passed; additional local real-upgrade runs are not claimed.
No work completion, human verification, merge, release, tag, marketplace promotion,
adoption, provider configuration change or host update occurred.

The released evaluator leaves WO-RLS-052 in_progress and selects
PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK. Required verification cannot be
declared complete while the positive case is unavailable. Preserve the successful
diagnostics and resolve the input-assembly blocker before handoff completion.
