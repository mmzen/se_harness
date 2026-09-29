# Publication guidance test correction â€” WO-PLG-029

Human mmzen approved the one-file correction and required exact-commit assurance
on 2026-09-29. The released 0.19.0 evaluator recorded approval and start.

The existing check now reads WO-PLG-028's public receipt. It rejects missing
accepted-package comparison, contradictory public identity and stale publication
wording. Existing manifest, wheel and link checks remain.

[Review](review.json) confirms the reviewed proposal was applied exactly.
[Checks](checks.json) retain 61 passing tests and one explicit Windows privilege
skip. These checks ran on a dirty working copy; they are not commit-bound assurance.

The work is implemented after passing final handoff checks. Claude model
startup and manual compaction pass; see [the native retry](../WO-PLG-028/native-delivery-v2.json). Exact-commit verification remains required.

## Current candidate evidence

The [new focused checks](checks-v2.json) retain the completed Claude-run
follow-up. [Final handoff checks](../WO-PLG-028/completion-checks.json) record
the selected evaluator results and complete combined Git change set.
The candidate assessment is in [requirement-assessment.json](../WO-PLG-028/requirement-assessment.json).
