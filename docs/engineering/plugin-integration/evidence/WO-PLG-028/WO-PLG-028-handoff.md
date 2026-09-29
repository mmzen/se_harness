```toml
artifact = "WO-PLG-028"
checkpoint = "handoff"
formal_snapshot_sha256 = "b567177e46368e9480e58aa731a8bccb91f936e38f19f04f2ba6d06f22ff1cc9"
rebound_at = "2026-09-29T16:25:30Z"
```

# WO-PLG-028 handoff evidence

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

See [the current evidence summary](README.md), [local checks](checks.json),
[public routes](public-routes.json) and [native delivery](native-delivery.json).
The public package matches the accepted distribution. All four public package
routes and the Codex session probes passed. Claude model startup stopped on an
expired login; Claude manual compaction is unrun. The work is not complete.

The draft PR is explicitly authorized by mmzen's request "Push and open PR
then ?" on 2026-09-29. This packet binds the partial observations for review.
Its presence and a passing structural PR check do not establish PUB-02
acceptance, authorize an implementation-completion transition, or supply a
verification decision. Final acceptance, exact-commit verification and
separately authorized integration remain pending.
