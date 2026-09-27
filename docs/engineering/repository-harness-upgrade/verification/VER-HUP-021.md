+++
id = "VER-HUP-021"
type = "verification"
title = "Verify this repository's 0.19.0 instruction adoption"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[relations]
verifies = ["REQ-IAR-022", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T20:07:47Z"
decided_by = "assurance-owner"
reason = "User: I approve both wo-hup-021 and ver-hup-021"
+++

# Verify this repository's 0.19.0 adoption

## Independence

Use RLS-SEH-028's published wheel, not a build from this checkout. Its SHA-256
is `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.
Expected instruction content comes from that wheel. Expected owner edits come
from the reviewed owner-edit map retained with WO-HUP-021. Preserve the old
lock and source bytes as comparison inputs.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-022 | inspection, demonstration | ADOPT01 | The installed root and 25 conditional guides match the released 0.19.0 payload and its rendered project name. The root's triggers reach real destinations. |
| REQ-IAR-024 | test, demonstration | ADOPT02 | Public 0.19.0 identity, doctor, graph validation, released-root qualification and selected-work preflight pass. Returned procedure locations exist; lifecycle states are preserved except for separately applied decisions. |
| REQ-IAR-025 | inspection, test | ADOPT03 | The installer retires only the recognized AGENTS/CLAUDE fragments. Separately reviewed owner edits remove harness instructions from AGENTS.md and preserve repository facts and commands. The empty harness-created CLAUDE.md is removed. A second upgrade has no pending writes. |
| REQ-IAR-026, REQ-IAR-022 | demonstration | ADOPT04 | Before real retirement, retain distinct native startup and post-compaction traces of the exact planned root in an isolated rehearsal. Bind their digests to this repository, its prior lock and the planned entry. The replacement plugin is installed, enabled and trusted for the actual target on each host claimed ready. Synthetic receipts and a manual read do not pass. |
| REQ-IAR-024, REQ-IAR-025 | inspection, test | ADOPT05 | One transaction JSON binds the base lock to the new released evaluator. Historical VRECs, RLS records, package inputs and immutable tags are unchanged. The predecessor-assessment lane accepts that transaction. |
| REQ-IAR-024 | test | ADOPT06 | The repository derives evaluator 0.19.0 and development candidate 0.20.0. Applicable source, package, distribution, CLI, scope and handoff checks pass; root/version test corrections address only demonstrated adoption assumptions. |

## Execution

Use the governing 0.18.0 evaluator for approval/start until the upgrade applies.
Use the exact public 0.19.0 evaluator for the preview, upgrade and resulting
checks. Run the full source suite at full scale using committed fixture bytes
and command-local Git line-ending conversion disabled, as in the release
evidence. Retain platform skips. Linux and Windows hosted checks remain required
before integration; local Windows evidence does not claim both platforms.

Use the already accepted delivery mechanism and public-wheel plugin assembly.
Record actual host versions and package hashes. Earlier demonstration traces
remain history: reuse requires a byte comparison and a justified applicability
assessment. They do not prove a newly configured target by themselves. Do not
claim Codex desktop support from Codex CLI/app-server evidence.

## Review and evidence

Retain concise results, failed attempts, exact commands, candidate identities,
transaction evidence and trace references under WO-HUP-021's evidence scope.
Test the required behavior, not a copy of the implementation. No new product
behavior, test exemptions or weakened gates are allowed by this contract.

Prepare one clean, commit-bound VREC after completion. Human verification and
repository integration remain separate decisions. A missing delivery prerequisite
leaves the actual root, old entry and lock on 0.18.0.
