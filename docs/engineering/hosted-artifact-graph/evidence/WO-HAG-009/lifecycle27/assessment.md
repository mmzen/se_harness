# Native lifecycle round 27

**Combined qualification remains incomplete.** Codex completed the synthetic
lifecycle and its accepted operations replay correctly. Claude reached the
30-minute limit before handoff apply, verification, release or native exports.
No actual implementation verification or release decision is requested.

Tested implementation candidate: `1b4ca16833b3908882e4a961c150156aca417f3c`.
The later evidence commit does not change that candidate's implementation.
This is the full VER-HAG-007 qualification, not the one-artifact efficiency test.

| Trial | Observed outcome | Wall time | Calls/items | Peak input context |
| --- | --- | ---: | ---: | ---: |
| Codex 221 | Test lifecycle completed; 13 accepted operations and four native exports independently replayed | 1,639.322 s | 242 observed items; lower bound | Unavailable |
| Claude 221 | Timed out; five accepted operations replayed, no native exports | 1,800.122 s | 130 calls | 165,599 tokens |
| Codex 221 reads | Separate fixed-view repeat: nine valid MCP results match HTTP across all seven tools | 286.159 s | 32 observed items; lower bound | Unavailable |

## What the correction resolved

The [candidate27 correction](../../WO-HAG-011/lifecycle-correction27/review.md)
names the setup entry, preserves the approved shell spelling, exposes failed
sub-commands, identifies the retained test Git base and captures observed reads.
Both full trials used the new package. Both reached a passing handoff preview
with a valid test Git base. The previous missing-base failure did not recur.
No service behavior, evaluator policy, permission or acceptance criterion changed.

This is progress in correctness, not evidence of an overall efficiency gain.
Codex took longer than round 26 and produced more visible output. Claude again
reached the limit. Its 43 retained command records total about 64 seconds of
subprocess execution; that measurement does not explain or assign the remaining
wall time to model reasoning. Visible tool-result volume was 1,817,151 characters
for Codex and 430,213 for Claude. Characters are not tokens.

## Codex: completed behavior and limits

Codex authored and used a corrected work order after discovering that the
original scope omitted the paired decision file. It preserved the original
approved record and comparison base. WO-P3-902 reached `implemented`,
VREC-P3-902 reached `verified`, and RLS-P3-902 reached test `released` for 0.0.1.
WO-P3-901 remains `in_progress`; RISK-P3-901 remains `mitigating`. Completion of
the corrected work must not be described as completion of that original work.

The independent assessor replayed all 13 accepted lifecycle operations through
released evaluator 0.22.1. It reconstructed four native exports, checked exact
Git bytes and retained candidate objects, and ran released validation. The
synthetic candidate is `4e714835fc74f166e8463ce0df6988522cdc2772`; the later
governance head is `9a406d9638934789fade80dc8fd005935c589462`. Neither verifies
the actual implementation candidate.

The native run retained the deliberate out-of-scope handoff refusal, unknown
accepted reply, original-key lookup, identical retry and changed-key conflict.
The identical retry returned the same receipt with project 17→18 and context
15→16. The changed-draft attempt failed with `HAG_REMOTE_STALE_PROJECT`, not a
digest-only stale-preview error. Preserve that exact distinction. The released
evaluator, rather than agent text, supplied subsequent lifecycle results.

### Read comparison correction

The proctor repeated the first nine MCP requests too late, after the context had
changed. All nine comparisons mismatched. Those results remain retained and do
not establish a service parity defect or a passing read case.

A separate native read-only session then used the completed project's fixed
state: project version 34, context version 32, and exact retained baselines.
Its nine valid responses matched independent HTTP results exactly across
`check`, `work-context`, `revision`, `impact`, `lineage`, `compare` and `cypher`.
One deliberately bounded impact result was incomplete. The agent preserved its
continuation and explained why it could not supply a complete governing context.

Two earlier requests selected a requirement for `check`, which accepts only
specified lifecycle artifact types. MCP returned schema-validation text; HTTP
returned `HAG_REMOTE_MALFORMED`. Their error envelopes do not match. They remain
failed requests, separately from the nine matching valid reads.

The first attempt to launch this repeat stopped before starting Codex because
the proctor had omitted the required empty `work` directory. Creating that
directory resolved the launch error without changing inputs or permissions.
No procedural help or authored request was supplied during either native run.

## Claude: remaining failure

Claude reached project version 22. Five accepted operations—definition approval,
work approval, work start, risk creation and risk decision—passed independent
released-evaluator replay. Its out-of-scope handoff was refused. After changing
a selected draft, the old handoff request was refused with
`HAG_REMOTE_STALE_PREVIEW`; a fresh handoff preview then passed.

The native time limit expired before handoff apply. Verification, release, the
seven MCP reads, two exports and the final native report were not performed.
The independent assessor therefore exited 1 with five accepted operations and
zero native exports. Its five assessor-created input snapshots do not satisfy
the native-export criterion. The intermediate `running` assessment, terminal
failure and separate incomplete assessment are all preserved.

Repeated overhead remains visible: guessed headings and file locations, an
unsupported helper flag, a guessed lifecycle state, incorrect risk-decision
fields/identity and malformed handoff inputs. The agent recovered several of
these errors, but recovery consumed calls and context. Automatic compaction
occurred; this test makes no startup or compaction-delivery qualification claim.

Claude used extensionless command-record filenames. The original cost summary
scanned only `.json` and missed them. A separate supplemental scan records all
43 commands without renaming evidence or replacing the original summary.

## Boundaries, supporting checks and evidence

Both providers passed live authentication probes before the full trials.
Codex's fresh workspace/network probes passed before both sessions. Selected
noncredential host settings, the real repository HEAD and its tracked diff match
their respective before/after observations. Staged input digests stayed unchanged.
The read-only repeat preserved the entire observed service status. Both disposable
service/graph pairs are now stopped; their volumes are preserved.

Candidate27's retained checks passed: 40 focused tests, the 1,337-test source
suite with 24 reported skips, distribution checks and CLI smoke. Released
validation reported 1,991 artifacts, zero errors and 63 existing warnings.
Those are candidate-bound results, not newly run source checks for this report.
Client wheel entries and all 27 server wheel entries match candidate26 after
decompression; archive/image hashes differ and remain separately recorded.
The retained component comparison supports only the stated reuse of unchanged
runtime evidence. It does not create new hosted-service test results.

Each trial has a `*-evidence.zip`, `*-inventory.json` and `*-visible.md` here.
Archives retain native inputs, command results, visible exchanges, independent
replays, read comparisons, settings hashes and costs. Inventories bind exact
bytes. Raw provider events, private reasoning and credentials are excluded.
The proctor archive retains the selected orchestration and independent checks.
Historical round-26 evidence is unchanged.

At the tested remote head, Engineering Harness `validate` failed because
WO-HAG-009 has no completed handoff evidence. The other completed CI checks
passed; three conditional release rehearsals were skipped. A later evidence
push must receive its own CI result. This PR remains draft and cannot be merged.

## Next bounded work

Do not spend another full-run budget on unchanged guidance. First remove the
remaining need to guess section names and lifecycle request fields. Replace
ambiguous references with exact existing headings and make required decision
inputs discoverable at their point of use. Check those changes on the affected
Claude operations before a full qualification rerun. Existing work-order scope
permits explanatory and test-driver corrections. New typed lifecycle commands
would extend the approved five-operation client scope and require a separate
bounded artifact proposal; they are not silently included here.

WO-HAG-009 and WO-HAG-011 remain `in_progress`. Their current evaluator step is
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`: run the selected work order's
handoff check. The missing qualification evidence must be resolved before
implementation completion or human verification is offered.
