+++
id = "VER-HUP-022"
type = "verification"
title = "Verify repository adoption of public 0.20.0"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-29"
updated = "2026-09-29"

[relations]
verifies = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-027", "REQ-IAR-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T20:27:15Z"
decided_by = "assurance-owner"
reason = "Human mmzen: i approve WO-HUP-024 and VER-HUP-022. Applies the reviewed verification contract; legacy assurance-owner records the human decision. Reviewed SHA-256 94c8284793f5815c8811abc80759866e8097ab428b403e0db9c8bb50c43d1194"
+++

# Verify repository adoption of public 0.20.0

## Independence

Use the public wheel released under RLS-SEH-029, not a build from this checkout:
`se_harness-0.20.0-py3-none-any.whl`, SHA-256
`7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0`.
The installed-payload digest is
`88c26138f759af78b2d7eeed3d15f92b573ff264ea6a531b2c22dbbf1905130e`.
Derive expected instruction bytes from that wheel and expected preservation
from the pre-upgrade repository. Use SPEC-IAR-014 and SPEC-IAR-015 for the
ownership and discovery rules. Product qualification remains recorded in the
release evidence; these checks assess adoption in this repository.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-022, REQ-IAR-023 | inspection, test | A020-01 | The installed root and conditional guides match the released payload, with the actual project name and version. Root reading triggers and returned procedure headings resolve. Current routes do not require the six old guide pointers. |
| REQ-IAR-024 | test, demonstration | A020-02 | Isolated public 0.20.0 identity, doctor, artifact validation, released-root qualification and applicable preflight pass. The CI evaluator pin agrees with the lock. The predecessor assessment accepts the single retained upgrade transaction from the integration base. |
| REQ-IAR-025, REQ-IAR-028 | inspection, test | A020-03 | AGENTS.md, the six existing owner pointers and unrelated owner files retain their exact bytes. Absent CLAUDE.md remains absent. The installer reconciles its lock without hand edits or pointer deletion. A repeated upgrade has no pending content changes. |
| REQ-IAR-023, REQ-IAR-027 | inspection, test | A020-04 | The explicitly selected WORK_ORDER.template.md matches the released template. Its authority link resolves and its assurance wording identifies the actual human. Current adoption notes distinguish root 0.20.0, source 0.21.0, actual local plugin state and later pointer cleanup. Historical records remain unchanged. |
| REQ-IAR-024 | test | A020-05 | The two development version declarations agree at 0.21.0; evaluator-facts derives root 0.20.0 and candidate 0.21.0. Full-scale source tests, distribution checks, CLI smoke checks and applicable complete-scope/handoff checks pass. |

## Execution

Use governing 0.19.0 for draft preparation, approval and execution start.
Use the exact released 0.20.0 evaluator for preview and upgrade. After a
successful apply, use the resulting 0.20.0 evaluator for repository governance.
Retain the before/after identities and the actual apply output.

Run `python scripts/run_tests.py --scale full` with command-local Git
line-ending conversion disabled and retain actual failures and platform skips.
Run `python scripts/validate_release_distributions.py --root .` and the
source CLI help check. At the exact candidate commit, run the repository's
released-root and predecessor assessment procedures with the public evaluator.
Retain commands, exit codes and candidate identities. Linux and Windows hosted
checks remain required before integration; local Windows results do not prove
both platforms. Do not weaken a check to accommodate adoption.

## Owner and lifecycle preservation

Compare the complete change set with WO-HUP-024. Before and after upgrade,
compare owner-file hashes and formal-artifact bytes. Only separately applied
decisions for the selected work may change lifecycle state. Preserve accepted
definitions, previous verification and release records, public receipts and
immutable tags. The target preview reports no legacy entry retirement, so no
new AGENTS/CLAUDE retirement receipt is required.

## Evidence retention

Retain one transaction at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-024-evaluator-upgrade.json`.
Keep concise command results, file comparisons, selected preview, template diff,
failed attempts and exact candidate identity under the sibling `WO-HUP-024/`
directory. Bind the completed checks to the exact candidate in VREC-HUP-022,
including its generated `evidence/VREC-HUP-022-evaluator.json` companion.
Human verification acceptance is a later decision.

## Residual uncertainty

This adoption does not install or update the user's host plugin and does not
claim fresh native startup or compaction qualification. The chat's parent
working directory has no selected installation; this session explicitly selects
`work/se_harness` and reads its installed root. This manual recovery is not proof
of automatic delivery. Active-consumer checks and native delivery are required
before separately authorizing removal of the six owner pointers.
