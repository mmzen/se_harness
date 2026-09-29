# Public marketplace confirmation — WO-PLG-028

The authorized 2026-09-29 publication advanced `plugin-marketplace` to
`86d75e56e28c0c34819c0079b41dc67075f58490`. All 63 public Git blobs match the
distribution verified by VREC-PLG-023. See [publication.json](publication.json).

## Observed checks

- Public fresh installation and update from retained public 0.1.0 passed on
  Codex 0.158.0-alpha.2.1 and Claude Code 2.1.273, on Windows. All installed
  package digests match. [Public routes](public-routes.json) distinguish the
  seeded prior-public fixture from the subsequent actual public Git update.
- Codex native startup and manual compaction passed after selecting the public
  plugin. Claude native initialization delivered the complete root in both
  route profiles. Its signed-in model probe stopped because the disposable
  OAuth session expired; Claude manual compaction remains unrun.
  See [native delivery](native-delivery.json) and [traces](native-traces.json).
- [Commands](commands.json) and [failures/recovery](failures-and-recovery.json)
  preserve the Windows path/line-ending fixture issues and the expired login.
- The [unchanged evaluator and marker readback](unchanged-public-readback.json)
  still matches released 0.19.0. [Demonstration readback](demonstration-readback.json)
  retains the deployed release manifest; the [assessment](demonstration-assessment.json)
  confirms the previously authorized release provenance and all three top-level
  file digests. This was a readback, not a new deployment.
- [Local checks](checks.json) retain 61 passing tests and one explicit Windows
  symlink-privilege skip, passing graph validation and a clean whitespace check.
  [Availability review](availability-review.json) bounds the source claims to
  observed results. These checks assessed the dirty working copy, not a final
  exact-commit candidate.
- The [version 3 delivery result](delivery-pending-result.json) has valid inputs
  and remains incomplete: marketplace native acceptance and public documentation
  integration are pending. The evaluator, demonstration and release markers
  are satisfied by the retained observations. [Evidence mapping](delivery-evidence-mapping-v3.json)
  explains the reuse of immutable earlier evidence.

## Remaining work

Renew the disposable Claude Code login, complete its native session checks,
run final handoff checks, and prepare the required exact-commit verification.
WO-PLG-029 covers the separately approved and locally checked test correction.
No verification acceptance or documentation push/PR/merge is inferred.
Overall delivery is incomplete; final public documentation readback follows
separately authorized integration. Historical evidence remains unchanged.

Claims exclude desktop UI, automatic-threshold compaction and other operating
systems. Real user profiles and release markers were not changed.
