# Evaluator 0.22.0 / plugin 0.2.5 delivery complete

The delivery checker returns **complete** with exit code 0. All five declared
surfaces are satisfied under REL-SEH-034 and WO-RLS-034/035/036, including the
README correction verified in VREC-PLG-034. This report records public readbacks;
it does not change an assurance decision or adopt the release.

| Surface | Observed result |
| --- | --- |
| Evaluator | GitHub and PyPI archives match the RLS-SEH-032 digests; existing public install evidence remains valid. |
| Marketplace | Plugin 0.2.5 remains at `7d30907f15bd7e06fb632e1ebf4e88e01b68726c`; both distributed package inventories match; required Codex CLI fresh/update routes passed. |
| Documentation | PR #530 merged at `80df326d5dcd78f4a51ea29f7502cced7fc83e2c`. All 14 public documents match the verified and CI-tested head. |
| Demonstration | Public Pages provenance retains governance `01ec43c86c9d30949295c07ac91c742be91e713a` and the exact released candidate. |
| Release markers | GitHub latest is `v0.22.0`; remote `last` is `abbec12ac5524c8adfb28693f846dd59de88f759`. |

The maintenance branch `release/0.22` also names the exact released candidate.
The `last` update used an exact expected-old-ref lease. Git and API readbacks
confirmed the result. Version-tag and archive bytes were preserved.

## Evidence

- [Final result](delivery-result-v6.json), [bound plan](delivery-plan-v4.json),
  [observations](delivery-observations-v6.json) and [checker invocation](closeout-check.json).
- [Merged documentation and public identities](merged-readback.json), with
  raw responses in [the readback archive](merged-readback-raw.zip).
- [Marker operations and readbacks](marker-closeout.json), with exact commands
  and responses in [the marker archive](marker-closeout-raw.zip).
- [Pre-marker result](delivery-result-v5.json) preserves the last incomplete
  state. Earlier plan versions and frozen VREC evidence are unchanged.

## Accepted limits and follow-up

Claude Code installation/update and native session tests, and Codex Windows
desktop tests, were **not run and remain unverified** under DEC-RLS-005/006.
Both distributed packages were byte-checked. No omitted host test is reported
as passed. Revisit the omissions before the next plugin release or before
claiming those routes verified.

RISK-RLS-006 remains an unfixed evaluator limitation with its recorded workaround.
Repository/host adoption of 0.22.0 and activation of the complete-release route
remain separate follow-up work. The repository still selects evaluator 0.21.0.
