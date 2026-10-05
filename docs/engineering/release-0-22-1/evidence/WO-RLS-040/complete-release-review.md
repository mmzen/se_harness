# Approve the complete release: evaluator 0.22.1 and plugin 0.2.6

**Decision requested from mmzen:** approve RLS-SEH-033 and the complete delivery
below. One response authorizes every listed release action while the frozen
inputs, gates and destination controls continue to match. No release decision
has been applied and nothing has been published for these versions.

The release delivers standalone draft validation, actual human attribution for
legacy owner labels, the 4 MiB dashboard limit and the draft-evidence transition
correction. It makes the evaluator fixes available for later Hosted Artifact
Graph adoption. The unfinished hosted service is excluded.

## Exact review and verification

- [Ready RLS-SEH-033](../../releases/RLS-SEH-033.md), under [REL-SEH-035](../../release/REL-SEH-035.md).
- Binary candidate: `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`.
- [VREC-SEH-033](../../verification-records/VREC-SEH-033.md) is verified by mmzen.
- Documentation candidate: `dc3b6d39b3980299b5443e6036d3fe8aa34c4fa3`.
- [VREC-RLS-003](../../verification-records/VREC-RLS-003.md) is verified by mmzen;
  its decision is `febda5a5be9d484231a932f19111bec8ebf72f8d`.
- [Frozen delivery plan](complete-release-plan.json), SHA-256
  `50c97db22f33cdcf0eb44b229b5e1ab7d5afca887cca6ffb4a9e380bc8c3641b`.
- [Readiness](complete-release-readiness.json), with [current raw observations](complete-release-readiness.zip)
  and [plan checks](complete-release-preparation.zip).

The request names the exact committed review head in PR #536. That commit is the
integration base for the release decision; it cannot be placed inside its own
files. Its bytes bind this review and the plan together. Subsequent decision or
receipt integration must pass the existing publisher's content comparison.

## Actions covered by this one decision

| Action | Exact destination and bounds |
| --- | --- |
| Record and integrate release | Apply RLS-SEH-033 through released evaluator 0.22.0 as mmzen. Bind the exact plan digest and this review commit. Push that decision to existing PR #536 (`codex/release-0-22-1` to `mmzen/se_harness:main`), mark it ready, and merge its exact checked head only after required CI/protections pass. Use a merge commit, the only method allowed by current main protection. No administrator bypass. |
| Evaluator publication | Run existing `publish-pypi.yml` from main with `release_record=RLS-SEH-033`. Publish immutable tag `v0.22.1`, GitHub release/assets and PyPI `se-harness==0.22.1`, with the exact archives below. |
| Maintenance branch | After protected release integration, advance `release/0.22` by ordinary fast-forward from `abbec12ac5524c8adfb28693f846dd59de88f759` to the binary candidate before the publisher's maintenance reconciliation. Check the observed old tip and ancestry immediately before writing and read back the result. Never force. The current reconciler checks an existing line but does not advance an older one. |
| Plugin publication | After independent public-wheel digest comparison, fast-forward `plugin-marketplace` from `7d30907f15bd7e06fb632e1ebf4e88e01b68726c` to reviewed child `85ae003769f53908addbdcf46c820a8af530ac24`. Publish both already-qualified plugin 0.2.6 payloads unchanged. |
| Documentation | Integrate the verified source documents with PR #536. Compare the plan's exact hashes at the documentation commit, release-governance commit and current main. Preserve immutable package README snapshots. |
| Demonstration | Deploy through the existing GitHub Pages workflow to `https://mmzen.github.io/se_harness/` and its configured `https://www.verityplane.ai/` destination. Use the first main commit containing the exact released record/binding as `release-governance`; retain provenance/readback. No domain/settings change. |
| Public observations | Observe the public evaluator install and both plugin hosts' fresh/update-from-0.2.5 routes. Retain actual content identities, failures, outputs and times under WO-RLS-042 / VER-RLS-038. Missing tests remain pending; no advance acceptance of their results is supplied. |
| Latest and last | Only after every required non-marker observation passes, promote GitHub latest from `v0.22.0` to `v0.22.1` and `last` from `abbec12ac5524c8adfb28693f846dd59de88f759` to binary candidate `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`. Use the existing serialized publisher and exact lease for `last`. |
| Receipts and closeout | Make ordinary release-only branches, pushes and protected PR merges to main containing only the fourteen named JSON receipt paths in the plan. Each receipt must retain `release_record`, `candidate_commit` and `plan_sha256`. Check the diff with `check-integration --receipts`; retain marker readback and the five-surface completion report. No unrelated edits, evidence rewrite or permission bypass. |

The reviewed base is the whole PR #536 release package, compared with main
`82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`. The release-decision addition is limited
to the named RLS file: one appended human release event and its delivery binding,
with candidate, distributions, relations and body unchanged. Later observation
commits are limited to the exact JSON paths. This grant does not pre-verify future
formal verification records or change WO-RLS-042's assurance obligations.

## Immutable payload identities

| Payload | SHA-256 |
| --- | --- |
| `se_harness-0.22.1-py3-none-any.whl` | `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |
| `se_harness-0.22.1.tar.gz` | `beea95b6431ae35d383789181fc59d1aae80efdab70d517b2dedf8782dfdc240` |
| Staged `PACKAGE-IDENTITY.json` | `4a62e5bb6a3ffb36ca723dca8fe3e71588d050bab70c5b1f11778dabb532249d` |
| Codex plugin ZIP | `26dcd08aa17a0da3ba899ee4096ec7e6c90c99b7d556038519f3128c56f925f8` |
| Claude Code plugin ZIP | `eb503fb3767d8f832b88df06d41a8c18e037b036bee258a6eb7a224f7cb41e40` |

Staged tree: `0069f9012fc6f6270410bfebbb673831d8745550`, accessible through
`codex/plugin-0-2-6-staging`. The publisher's inspection confirms its complete
69-file tree and inventory bindings. The plan also fixes both assembly-inventory
digests. The selected archives are the verified Windows staging bytes; equivalent
expanded Linux staging does not imply identical compressed ZIP bytes.

## Checks, controls and limitations

Windows and Linux qualification, installed archives, upgrade rehearsals, native
Codex CLI/Claude Code tests and reproducible builds passed as assessed in
[the binary review](final-verification-review.md). The [ready-record replay](ready-record-replay-receipt.json)
reproduced both bound archives twice. Independent documentation verification
passed its 44 focused checks and full Windows suite (1,293 tests, 23 skips).
The documentation review head passed 17 CI checks; two unrelated manual-rehearsal
legs were skipped by workflow policy, not counted as passes. Current review-head
CI is reported in the PR; integration waits for required checks at the exact head.

Fresh live Codex and Claude authentication probes pass in the existing disposable
profiles. This is point-in-time readiness, not a guarantee that a future token
cannot expire. GitHub still enforces main PR/validate, main-only PyPI deployment,
and non-fast-forward/deletion protections for marketplace and maintenance.
The separately approved PyPI reviewer-only correction remains applied. mmzen's
four-field Trusted Publisher confirmation is retained as human account-side
evidence. OIDC and workflow permissions are unchanged.

**Codex Windows desktop is not run / unverified**, under accepted DEC-RLS-009 and
RISK-RLS-007. Revisit before the next plugin release or a verified-desktop claim.
Required public CLI routes remain to be observed after publication. Their absence
is not reported as success or silently covered by the desktop omission.

Original package README snapshots keep historical staging wording. The verified
source guidance explains how to use current release records and public identity
readback. These source changes do not rebuild or rebind the qualified payloads.
No hosted service scenario, repository/host adoption, HAG pin amendment, live
DEC-HAG-001 disposition or unrelated provider change is included.

## Recovery and completion

Before each write, compare the frozen plan, candidate, payloads, targets, current
gates and provider controls. Inspect uncertain effects first. Retain exact
completed outputs and resume only missing work under the same grant. Do not
repeat the approval solely because a provider, session or day changes.

Stop on changed expected refs, different immutable content, expired access,
failed gates or unexpected integration changes. Preserve failed observations.
Never overwrite published version bytes, move an immutable version tag, force
marketplace/maintenance, change protections, or broaden a receipt path to clear
a failure. An input/scope change needs a matching decision; an unavailable check
keeps delivery pending. No rollback deletes or hides published evidence.

Formal release authorization, evaluator publication and five-surface completion
are separate facts. Report complete delivery only after all required public
observations and both marker readbacks pass. Continue every permitted action
without another release/publication prompt while this reviewed grant matches.

**Response:** “Approve the complete release” approves RLS-SEH-033 and all actions
above for this frozen plan. “Request changes” leaves the RLS ready and public
state unchanged. Neither this prepared review nor a passing check is a decision.
