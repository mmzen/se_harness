# Release decision review: RLS-SEH-029

RLS-SEH-029 is ready for mmzen's release decision for SE Harness 0.20.0.
The release gates and exact bound-record replay pass. Nothing has been published.

## Exact decision inputs

| Input | Value |
| --- | --- |
| Release contract | REL-SEH-031 |
| Release record | RLS-SEH-029, ready |
| Candidate commit | `7253d13b212ad6f7df670021290fea32e81d66de` |
| Version and intended tag | `0.20.0`, `v0.20.0` |
| Verified coverage | VREC-SEH-029; exactly 16 work orders and 10 verification contracts |
| Human verification | mmzen: “I verify VREC-SEH-029 as assurance owner.” |
| Ready RLS SHA-256 | `0dc2f82b6e756a2b91cf1650180143d5d2d4576a6250fbc73eb155eb853a3157` |
| Verified VREC SHA-256 | `8d247d3b1ab196e44b54c39a5539ae1636f5d071e147fcc1a2d47f464a982856` |
| Wheel SHA-256 | `7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0` |
| Source archive SHA-256 | `5b6784aeabdf72e0e6b43a7a2bc81244c7a9da6415cf39fbc39f440ec57d426c` |

The record and its generated sidecar are under `../../releases/RLS-SEH-029.md`
and `../RLS-SEH-029-evaluator.json`. The distribution table binds the retained
`bundle-0.20.0.json` schema-2 manifest. Governance commits retain records and
observations after C; they do not replace C.

## Required checks

- Windows full source suite at C: 1,162 tests, 17 reported skips, pass.
- Linux full source suite: 1,162 tests, two reported skips, pass.
- Installed-package, Windows/Linux predecessor upgrade and integration checks pass.
- Both manual publication-rehearsal legs pass. The earlier record leg assessed
  RLS-SEH-028; it was not used as proof of this new record.
- [RLS-SEH-029 replay](https://github.com/mmzen/se_harness/actions/runs/36612357797)
  passed on review commit `be1755679f592acd40051816359856d4019d8ee9`.
  Two fresh pinned Linux builds reproduced both hashes above at C.
- Released evaluator 0.19.0 passes the release-decision gates. Repository
  distribution validation passes for all 17 distribution-bearing records.

`bound-record-replay.json` retains the complete technical replay result.
`bound-record-replay-ci.json` retains the workflow, artifact hash, download
command and raw artifact expiry. `release-readiness.json` retains the final
gate result. Earlier exact-candidate checks remain in `FINAL_REVIEW.md` and
their named evidence files; that review is preserved as a historical snapshot.

## Marketplace and complete delivery

`delivery-plan-bound-v1.json` retains the approved five-surface scope with the
allocated record and observed build hashes. It preserves the original
VREC-bound preparation plan unchanged. Unknown future public identities remain
null. Its release observation is ready, and no public surface is marked passed.
`delivery-ready-result-v1.json` reports valid inputs and incomplete delivery.
Exit 1 is expected for that honest pending state.

After exact evaluator publication, approved WO-PLG-030 obtains the public wheel,
assembles and qualifies plugin 0.2.2 for both hosts, then prepares the reviewed
history-preserving marketplace commit. Human verification and exact publication
authority precede that push. Approved WO-PLG-031 checks public fresh/update
routes and reconciles current documentation. Both remain approved and unstarted.

The evaluator publisher does not update plugin-marketplace. The explicit
downstream procedure is documented in REL-SEH-031, the two work orders,
`docs/notes/plugin-marketplace-publication.md` and
`docs/notes/release-delivery-completion.md`. Successful future branch delivery
must be observed; a rehearsal cannot guarantee it. Latest/last, demonstration,
documentation and marketplace observations remain part of final closeout.

## Constraints and recovery

The current installed evaluator remains 0.19.0. Existing owner guide pointers
remain untouched until separate adoption and cleanup. Public plugin claims stay
on observed 0.2.1 / 0.19.0 while 0.2.2 / 0.20.0 is pending.

Do not publish before the exact released record is merged and publication is
authorized. Stop on a failed check, changed binding or conflicting remote ref.
Preserve immutable archives and tags after publication; product repairs require
a separately reviewed version. Do not force over concurrent marketplace work.
Binding setup refusals and their successful correction are retained in
`release-binding.json`; neither refusal changed lifecycle state.

## Next human decision

The evaluator returns `PROC-RLS-DECIDE / STEP-RLS-DECIDE` and the response:

> I authorize release record RLS-SEH-029.

This decides only this ready record. It does not authorize merge, publication,
latest/last promotion, adoption or deletion of owner files. Those exact decisions
remain separate. The existing 0.19.0 role encoding retains mmzen's actual human
decision in the reason when Codex applies it.
