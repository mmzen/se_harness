# WO-HUP-020 draft review

Prepared on 2026-09-16 by Codex. This is a draft-package review; implementation,
approval and assurance have not been performed. All three artifacts remain draft.

## Reviewable approval inputs

| Artifact | SHA-256 of complete draft bytes | Proposed approving role |
| --- | --- | --- |
| SPEC-HUP-020 | `27e0357c5775bf78f1b3386ac9db52a02802be7dd9a79c36735bda870079b64d` | technical-owner |
| VER-HUP-020 | `edb0c5c5eaf1617f689da8f0ff15138cccb4a7f5e3818210caa057b90345b15f` | assurance-owner |
| WO-HUP-020 | `c245f873e89869a6f4464c1ef15d4070ecc0b1f1b41f3b0c6e9b76e8e1861661` | engineering-owner |

The proposed target is approved for each named artifact. The released
transition preview passed without applying a transition. Its projected states
are not the artifacts' actual states.

## Observations

- Released evaluator 0.18.0: graph valid, 1661 artifacts,
  zero errors and 48 warnings. The selected approval gates pass.
- Released doctor: 64 passing checks. The initial sandbox
  run failed Git's filesystem-owner check; the ordinary host run passed without
  changing Git configuration. Both outputs are retained outside the checkout.
- 106 fetched local/remote/tag refs were inspected before allocating
  SPEC-HUP-020, VER-HUP-020, WO-HUP-020 and the proposed later VREC-HUP-019.
- Existing source, tests, root identity, workflow and VREC-PLG-022 are unchanged.
  No implementation tests were run for this drafting-only stage.

## Design and scope review

The real failure is the two-part schema and same-version lock restriction.
The addendum addresses both, retaining unrelated drift and evaluator checks.
One existing assessor and test module are sufficient; the existing catalogue
is read from the trusted base as data. This avoids a second path list, candidate
imports, a new dependency or a migration framework.

The selected HUP requirements, architecture and ADR already cover this reader.
The addendum explicitly replaces HUP-LSF-007's schema-3-only restriction and
its preserved exclusion in the plugin specification. Their earlier approvals
and observations remain untouched. The verification plan tests public outcomes
and the actual PR boundary, with hosted CI reported only after it runs.

Review found that VER-PLG-025 originally selected VREC-PLG-022 only. VER-HUP-020
now expressly scopes the later aggregate to VREC-HUP-019 and assesses the
assessor changes separately from the unchanged cleanup acceptance. This
resolves the preparation mismatch before approval; the old VREC is preserved.

## Baseline and retained outputs

- Remediation base: `0dadc352b3a5e6c64c721e1c688cc215438ddd7f`.
- PR base: `f05c478a29c39f94968fdc842a34c861d30a42ac`.
- [Original failed CI job](https://github.com/mmzen/se_harness/actions/runs/35101599351/job/104812126088).
- [Read-only local reproduction](original-planner-failure.json).
- [Reviewed inputs and local output references](draft-review.json).

## Next decision

Approve SPEC-HUP-020 as technical-owner, VER-HUP-020 as assurance-owner and
WO-HUP-020 as engineering-owner. The approval grants the work order's routine
execution and verification preparation through DR-015. It does not verify the
future candidate or perform delivery.
