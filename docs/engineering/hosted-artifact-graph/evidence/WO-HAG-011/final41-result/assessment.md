# Focused authoring qualification: trials 371 and prelaunch 372

Both missing-input cases pass independent content review. The first positive
Claude case did not launch: the complete task exceeded the approved 64 KiB limit.
There is no positive-authoring pass or overall qualification claim.

Candidate: `ee86a842550c19fb6a56913841757b42df9ecaec`.
Review head: `dfeb5adf1f640dea48a53b7a446e49e93c31004a`.

| Case | Result | Observed time and capture |
| --- | --- | --- |
| Claude 371, EFF-04A2 | Pass: asks for missing audience, problem, outcome and success measure; no invented definition | 168.686s; 3 calls; peak context 38,472 |
| Codex 371, EFF-04A2 | Pass: asks for missing inputs; saves a report that discloses incomplete capture | 71.230s; 6 observed tool items; complete calls/context unavailable |
| Claude 372, EFF-04B | Pending: refused before model launch | 67,945-byte prompt; limit 65,536; excess 2,409 |

Claude used the contract's Opus 4.6 model with CLI 2.1.280. The full lifecycle
Opus 5.5 trials are separate. Both completed clarification projects remain at
version zero. Independent state reads, staged-input hashes and monitored
repository/settings comparisons pass. These timings overlapped other native runs
and do not measure successful artifact creation.

Claude's clarification-only reply is eligible because its complete capture shows
no attempted mutation. Codex uses the saved-report branch because its capture is
incomplete; an unchanged project alone would not justify the other branch. Its
proposed wording is explicitly a question, not an agreed outcome. Claude's claim
that any partial draft would contain only invented content is too broad, but the
permitted clarification stop and missing inputs are clear.

## Entry refusal and bounded correction

The 372 refusal preserved the entire requested task and canonical source bytes.
No instruction was truncated and no model was launched. The complete entry
contained 20,069 instruction-content bytes, 5,490 fixture bytes, and 26,661
reference bytes, plus identities, framing and the task.

The correction shares repeated release/path metadata and shortens duplicated
task framing. It preserves all selected canonical sections, references, fixture
contents, requested outcomes, reporting rules and permissions. The 64 KiB cap
remains fixed. Presentation prototypes are diagnostic evidence, not native passes.
The source suite and final packaged qualification are assessed separately.

The earlier client comparison finds only resources.py and wheel RECORD changed
from C26 to C38. This supports reuse of unchanged typed-client comparisons, not
whole-wheel equality. Required focused instruction and new native cases remain.

## Evidence and limits

- [Claude visible transcript](claude-371-visible.md), [evidence](claude-371-evidence.zip), [inventory](claude-371-inventory.json).
- [Codex visible transcript](codex-371-visible.md), [evidence](codex-371-evidence.zip), [inventory](codex-371-inventory.json).
- [Entry refusal, prototype checks and package identities](provenance.zip), [inventory](provenance-inventory.json).

The first retention attempt completed the full-run archives, then stopped because
its wrapper reused the previous output-directory variable. The corrected observer
preserved those archives and retained the focused results separately. No native
input or outcome changed. Prototype test failures and successful correction remain
visible. Private reasoning, account stores and credentials are excluded.

All three test projects' containers are stopped, with their volumes preserved.
EFF-04B still needs three correct comparable Claude trials on one final candidate,
then Codex. Native NQ qualification remains separate. No criterion is waived.
