+++
id = "VER-HUP-023"
type = "verification"
title = "Verify repository and CI adoption of released 0.20.1"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-REB-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T13:47:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: I approve. Approves the reviewed WO-HUP-025 and VER-HUP-023 adoption package, required commit-bound verification, exact public 0.20.1 adoption, private evaluator switch and bounded ordinary branch-push/draft-PR envelope. Reviewed SHA256 0229dc8d8bfa5ffaffc48dd5a4048f6c0d674167fdb5a142feac4d8c4034da66; transition input SHA256 0229dc8d8bfa5ffaffc48dd5a4048f6c0d674167fdb5a142feac4d8c4034da66. Only the confirmed work-order assurance fields were added. Codex applies the human decision using the selected released evaluator engineering-owner encoding. Verification acceptance and merge remain separate."
+++

# Verify repository and CI adoption of released 0.20.1

## Independence

Expected identity comes from released RLS-SEH-030 and its published wheel:
`se_harness-0.20.1-py3-none-any.whl`, SHA-256
`300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764`.
The installed-payload SHA-256 is
`70d70f9912a3f40865e1bd50ffb1b377f2fb4c29f87575444cf3ae175be0896a`.
Use those public bytes; do not build a substitute from development source.

REQ-REB-027 and SPEC-REB-012 define the existing upgrade. This contract tests
its adoption here. It does not repeat product qualification or qualify the
unmerged minimal-layout successor. Baseline preservation comes from main at
`aeebcabf8e3ed958e0166dfe2754a2af2681a59d` and the actual pre-apply snapshot.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-REB-027 | inspection, test | A0201-01: identity and plan | Isolated public 0.20.1 has the expected wheel and payload. Preview changes only the configuration and root version text, with the installer regenerating its lock. No customization, conflict, seed replacement or entry retirement is proposed. |
| REQ-REB-027 | test, inspection | A0201-02: transaction and preservation | Apply retains one canonical transaction. Config, lock and evaluator agree at 0.20.1. A repeat preview has no pending content changes. Owner files, removed legacy pointers, templates, machine policy and prior formal/evidence records retain their prior bytes or absence. Only this work's explicit lifecycle decisions may change its records. |
| REQ-REB-027 | test | A0201-03: repository and CI | Public 0.20.1 identity, doctor, complete validation and released-root qualification pass. CI pins 0.20.1. The existing transition assessor accepts the trusted base, released RLS and exact transaction without checkout changes. No packet or hand-edited lock is used. |
| REQ-REB-027 | inspection, test | A0201-04: current instructions and regression | The four named current guides/indexes describe adopted 0.20.1 and development source 0.21.0. The installation example and its existing test agree. Relevant documentation tests, the full source suite, distribution checks and source CLI smoke check pass. Both development version declarations remain 0.21.0. |
| REQ-REB-027 | inspection, test | A0201-05: exact candidate | Scope and handoff checks cover the complete change set. The VREC binds the exact clean candidate, approved work and this verification contract. Applicable hosted Linux and Windows checks pass before integration. |

## Execution and failure handling

Use selected public 0.20.0 for package preparation, approval and work start.
Use the exact public 0.20.1 evaluator for upgrade preview and apply. Switch
repository governance to 0.20.1 only after the installer succeeds. Retain the
before/after identities and use the existing private evaluator environment.

Before apply, target doctor is expected to report the old root template,
payload and selected-version differences. All other failures require resolution.
After apply, those three differences must be gone. Record failures honestly;
do not suppress them or treat a warning as approval.

Run the existing commands: `doctor`, `validate`, `qualify released-root`, the
repository governor-transition assessment, the relevant documentation tests,
`python scripts/run_tests.py --scale full`,
`python scripts/validate_release_distributions.py --root .`, and the source CLI
help check. Resolve command arguments from each existing tool's help. Preserve
the candidate, evaluator roles, command arrays, working directories and exit
codes. Hosted CI supplies its existing Linux and Windows package and upgrade
checks; local Windows evidence alone does not establish both platforms.

No new product tests or native login sessions are needed for the reviewed
two-file installer change. Existing refusal and isolation tests remain required
through the normal suites. A newly exposed defect or an unexpected edit returns
to bounded correction planning rather than weakening a check.

## Evidence retention

Retain the installer transaction at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-025-evaluator-upgrade.json`.
Keep the preview, public identity, preserved-file comparisons, check summaries,
failed attempts and candidate evidence under the sibling `WO-HUP-025/` directory.
Keep new raw test logs outside the repository and retain concise actual summaries
and their retrieval information. Preserve previous evidence byte for byte.

Prepare VREC-HUP-024 through `capture-verification` after implementation, at
the exact clean candidate. Its generated evaluator companion belongs at
`docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-024-evaluator.json`.
Human verification acceptance is a separate decision. If that ID is no longer
available, resolve the changed destination before preparation; do not overwrite it.

## Residual uncertainty

Adoption does not update the user's plugin, prove desktop instruction delivery
or automatic compaction, change public release markers, or complete VER-IAR-022.
The minimal-layout candidate must be reconciled and independently qualified
after this adoption is integrated. This contract records no verification result.
