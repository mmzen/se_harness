```toml
artifact = "WO-PLG-029"
checkpoint = "handoff"
formal_snapshot_sha256 = "0b9445b23d40afe39dabefc72c789862a070e59434fda6008294975ee5006c22"
rebound_at = "2026-09-29T16:25:39Z"
```

# WO-PLG-029 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Completed candidate checks — 2026-09-29

Claude startup, manual compaction and the resumed-session check passed after
renewing the disposable login. All four public package routes and native root
delivery on both hosts now pass. The initial failures below remain historical
observations; they no longer describe the current acceptance result.

See [the candidate assessment](../WO-PLG-028/requirement-assessment.json),
[native retry](../WO-PLG-028/native-delivery-v2.json),
[focused tests](../WO-PLG-028/checks-v2.json), and
[delivery result](../WO-PLG-028/delivery-result-v4.json).
The tests have 61 passes and one explicit Windows symlink-privilege skip.
The delivery result leaves only public documentation integration pending,
as VER-PLG-027 permits for this candidate phase.

Completion and exact-commit verification use these observations and the final
handoff results. A human verification decision and later integration remain
separate. No new marketplace publication or user-profile adoption occurred.

## Earlier partial evidence for draft review

See [the test correction review](review.json) and [local checks](checks.json).
The approved correction matches the reviewed proposal. The combined focused
run has 61 passing tests and one explicit Windows symlink-privilege skip.

The draft PR is explicitly authorized by mmzen's request "Push and open PR
then ?" on 2026-09-29. WO-PLG-029 remains in progress: combined VER-PLG-027
acceptance still needs Claude's model startup and manual compaction checks,
then final handoff and exact-commit verification. This partial packet and a
structural PR check do not supply those results or a verification decision.
