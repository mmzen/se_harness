# Claude automatic compaction: fresh-session recovery

The required Claude automatic-compaction observation passed on the unchanged
0.21.0 candidate. Native Claude Code emitted an automatic compaction boundary,
its compact hook delivered the complete expected harness entry, and the next
resumed turn completed successfully. No criterion was waived.

## Observed results

| Case | Result |
| --- | --- |
| Fresh startup above the checkout | Passed; the native hook delivered the unselected bootstrap. |
| Clone and activate the actual checkout | Passed; the helper used the session and data path delivered by the native hook. |
| Resume with the selected repository | Passed; the exact entry and selected checkout were restored. |
| Automatic compaction | Passed in the third generated inventory batch. The native compact boundary reported trigger `auto`, 73,768 tokens before and 16,712 after compaction. |
| Delivery at automatic compaction | Passed; `SessionStart:compact` delivered the complete expected entry with the same session and selected checkout. |
| Continuation after compaction | Passed; a resumed turn answered an ordinary arithmetic question successfully. |
| Repository preservation | Passed; the complete fixture file inventory and its byte digests are unchanged. |
| Shipped package input preservation | Passed for all 28 shipped files. Two generated Python bytecode files appeared in the disposable package. The initial assertion of whole-directory equality failed and is retained as an inspection finding. |

## Exact inputs and procedure

- Governing evaluator for the real repository: released 0.20.1, identity and doctor passed.
- Repository HEAD at test: `8e8b43ad28184fa2744071d1626d354661c5929e`.
- Candidate wheel source: `c1bcbfb8e053ee8099e98b1dc34fcf547adc46eb`.
- Candidate wheel SHA-256: `66467146b32853ce87d7a782a9452aca8e20ead4ba4cb07837ec16c518aa784d`.
- Delivered entry SHA-256: `9c581e0e80d3e1851eb5ce46bffd06945264aa366b64b7360232c5bee4319990`.
- Host: Claude Code 2.1.273; native reported model `claude-opus-5` throughout.
- Session: `ed90626b-c244-4473-aeac-5712953f70eb`.
- The prepared package was unpacked into a new disposable directory. An actual
  native startup supplied the session identity before the fixture was cloned.
- Subsequent turns used the documented per-process
  `CLAUDE_CODE_AUTO_COMPACT_WINDOW=100000`. No percentage override or manual
  compact command was used. Saved user settings and safeguards were not changed.
- Ordinary code questions and three distinct generated stationery-inventory CSV
  batches grew the conversation. Model tools were disabled. Native events and
  hook output established delivery; the model was not asked to disclose internal
  reasoning or reproduce instructions.
- The independent assessment read the expected entry directly from the exact
  wheel and matched all six selected-repository resume/compact deliveries.

The companion JSON retains the exact driver, arguments, input text, cwd, runtime
identity, stdout, stderr, exit statuses, native events, byte digests and independent
assessment. The recorded whole-directory comparison failure is explained by
`scripts/__pycache__/harness_runtime.cpython-314.pyc` and
`scripts/__pycache__/inject_instructions.cpython-314.pyc`; no shipped file changed.

## Meaning and limits

This closes the missing Claude automatic-compaction observation in VER-IAR-021
for this candidate, as required by VER-IAR-022. Earlier manual-compaction and
resume observations remain retained. Earlier `reasoning_extraction` refusals
also remain retained; their cause has not been established. Session history,
task content and compaction timing changed together, so this result does not
isolate which difference enabled recovery or prove that the refusal cannot recur.

This is native Claude Code evidence. Codex Windows desktop remains explicitly
unverified. With model tools disabled, this run does not establish the separate
formal work-to-delivery walkthrough or every integrated migration criterion.
The fixture and candidate are not this repository's governing installation.

WO-IAR-030 remains `in_progress`. VREC-IAR-020 is not prepared or accepted.
The next stage is the remaining integrated evidence assessment and the evaluator's
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK` handoff step. No completion,
assurance, publication or release is inferred from this native pass.

The refusal did not recur in this bounded recovery, so no support report was
needed or submitted. No product implementation or accepted artifact changed.
