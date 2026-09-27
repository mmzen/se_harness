# Adoption of SE Harness 0.19.0

The adoption is prepared, not applied. The repository and private evaluator
remain on 0.18.0. The selected release is the public wheel from RLS-SEH-028.

## Proposed change

- Install the compact root and 25 conditional guides with the released installer.
- Configure and demonstrate native startup and post-compaction delivery with
  Verity Plane 0.2.0 before retiring the two old instruction blocks.
- Apply the reviewed owner edit so AGENTS.md contains only repository content.
- Advance the development source version to 0.20.0; this does not release it.
- Update current notes and three tests that expect the old instruction layout.
- Retain the upgrade transaction and prepare commit-bound verification.

[WO-HUP-021](../../work-orders/WO-HUP-021.md) defines the exact paths and limits.
[VER-HUP-021](../../verification/VER-HUP-021.md) defines six acceptance cases.
Review the [proposed AGENTS.md](AGENTS.proposed.md), [complete diff](AGENTS.proposed.diff)
and [owner-edit map](owner-edit-map.md).

## Checks completed

| Check | Result |
| --- | --- |
| Published wheel identity | Matches RLS-SEH-028. |
| Actual 0.19.0 installer preview | 25 add, 8 update, 24 unchanged, 2 legacy-fragment removals; no writes. |
| Target pre-upgrade doctor | Expected 0.18/0.19 version and layout differences only. |
| Restored 0.18.0 evaluator doctor | Passed. |
| Public-wheel plugin assembly and independent package check | Both accepted; package-content evidence only. |
| Draft graph validation | 1,698 artifacts, 0 errors, 52 warnings, 0 advisories. |
| Two-artifact approval preview | All required gates passed; no transition applied. |

The 52 validation warnings are outside the selected work according to the
checkpoint-free work-order result. They are not adoption acceptance evidence.

## Remaining work

Both new artifacts remain draft. The installed plugin is still 0.1.0. Native
delivery of this repository's exact planned root has not yet been demonstrated.
Earlier demo traces refer to different roots and are not relabeled as this proof.

Approve WO-HUP-021 and VER-HUP-021 to start the bounded adoption work. Native
traces and owner bytes must be reviewed before removal approval and installer
apply. Verification acceptance and integration remain separate decisions.

The existing transition procedure requires a statement identifying the
artifacts, target state and accountable actor. The proposed approval uses the
engineering-owner right for WO-HUP-021 and the assurance-owner right for
VER-HUP-021. Its read-only preview is retained in approval-preview.json.
