# Complete release: evaluator 0.23.0 and plugin 0.2.7

## Decision requested

Approve the complete release under **RLS-SEH-034 / REL-SEH-036**, including the
listed protected integrations and public delivery actions. This review is a
proposal; the release record remains `ready` until mmzen supplies that decision.

Exact [delivery plan](complete-release-plan.json) SHA-256:
`420b4b82891b2fe77244cc3c4a995ddab8153a11f649324f01b1f37e83e51b34`.
The immutable review commit presented with the request binds this plan, the
ready record and all preparation material. Only the recorded RLS decision may
be added before its protected integration. Later receipt integrations are limited
to the exact paths listed in the plan. No unrelated change or check bypass is covered.

## Inputs already verified

- Candidate: `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15`; VREC-SEH-034 verified by mmzen.
- Release coverage: 20 implemented work orders and 11 verification contracts.
- Wheel SHA-256: `ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c`.
- Source archive SHA-256: `777c9c1f518f6db1d3beb013f9bbb908544c482598ee399767fd789414f2ccfa`.
- Two ready-record builds reproduced those archives: [run 39007950424](https://github.com/mmzen/se_harness/actions/runs/39007950424).
- Read the [verified assessment](verification-assessment-48e851bb.md),
  [replay receipt](ready-record-replay-034-receipt.json), and
  [plan checks](complete-release-plan-check.json).

The replay used preparation commit `c7be3ce0e3f28dc19b13691e00bdf2ab93474dde`.
The subsequent README correction changes no RLS bytes, binary candidate, recipe,
archive, qualified plugin file or candidate-bound evidence. All captured hashes
remain equal. All 47 focused documentation/onboarding checks pass. The earlier
README CI failure and intermediate local errors are preserved in the
[correction evidence](../WO-RLS-047/source-guide-bound-correction.md).
Final review-head CI must pass before the approval request.

## Actions covered by this one decision

| Action | Exact destination and condition |
| --- | --- |
| Release decision and integration | Record mmzen's decision on RLS-SEH-034. Merge PR #545 into `mmzen/se_harness:main` through its required checks, using a merge commit and exact checked head. The diff from the immutable review head may add only the RLS decision/binding. |
| Evaluator | Publish the bound wheel and source archive as PyPI `se-harness==0.23.0` and GitHub `v0.23.0`. Tag the exact candidate and establish `release/0.23` at that candidate. Re-download and test the public wheel. |
| Marketplace | Promote commit `d04776866046b60b14ffef14ced1453c4aafa7d9` from parent `85ae003769f53908addbdcf46c820a8af530ac24` to `plugin-marketplace`. Exact tree: `0e0ff666693ad7f00564435e2f35ce8e31a2fb4e`; identity SHA-256: `f3d3f808d06d09f15628fbbe7958a8bf6e72807f0536a8c9905d947d78376a5e`. Verify both public CLI fresh and 0.2.6-to-0.2.7 update routes in disposable profiles. |
| Documentation | Integrate the exact source guidance at `92f948ad9faea69e00485d59c0680694e21bc30e` and compare its ten hashes below. Preserve the qualified package snapshots; retain later availability observations as JSON receipts. |
| Demonstration | Run the existing Pages workflow with the first main commit containing the exact released binding. Check `https://mmzen.github.io/se_harness/` and its existing domain `https://www.verityplane.ai/`; no provider-setting change. |
| Markers | After required non-marker observations pass, set GitHub latest to `v0.23.0` and move `last` from `4f640284ec496b88cd7aa4ba88ca537d9374a2f8` to `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15` using the exact lease. |
| Receipts | Commit and integrate only the plan's named receipt paths through protected PRs. Check the five delivery surfaces against the frozen plan; keep observed effects separate from authority. |

The plugin bundles evaluator/client 0.23.0. The private hosted service continues
to use evaluator 0.22.1. Its tested combination is
`sha256:70890d365551c04d38eb74afb8f815cf30c5eb61d09e9ac7d1e322b9b657de0a`.
All 89 marketplace files match the qualified identity. This plan publishes no
hosted service or container image.

## Readiness and limitations

Provider protections remain enabled: main requires PR/checks and merge commits;
PyPI permits only main with the approved reviewer removal retained; marketplace
and maintenance refs deny deletion and non-fast-forward updates. The version
and maintenance refs were absent; PyPI 0.23.0 returned 404. These observations are
rechecked before each action. The human's prior PyPI publisher-settings
confirmation is historical evidence, not a new authenticated settings read.

Both live CLI probes passed. Claude requires explicit `claude-opus-5-5` because
the configured default returned model-not-found (404). No global setting was
changed. Authentication is point-in-time evidence; failed later checks stop
the affected delivery observation.

- R23-NATIVE-010/011 remain open under DEC-RLS-010 / RISK-RLS-008.
- Codex Windows desktop remains not run/unverified under DEC-RLS-011 / RISK-RLS-009.
- Git remains authoritative. The service stays a private source build.
  RISK-HAG-001/002 and the existing application controls remain applicable.
- WO-RLS-047 remains in progress. Public observations and final VER-RLS-041
  assurance follow publication and are excluded from release membership to avoid
  circularity. This request does not fabricate those future results or decisions.
- Repository adoption, user-host updates, authentication/DB ACL work, production
  deployment, provider-setting changes and performance work are excluded.

## Recovery

Inspect remote effects before any retry. Resume only missing actions whose
identities and conditions still match this plan. Never replace an immutable
published version or archive. A conflicting ref, changed payload, failed required
check or missing control stops the affected action. Keep partial delivery visible.
Do not move latest/last until the required preceding observations pass. A changed
plan needs a new decision; an unchanged plan does not need repeated authorization.

## Frozen documentation

The canonical plan schema permits seven README/docs paths. Its bound readiness
companion also fixes the three package-source README paths, so all ten are checked.
The initial unsupported draft was corrected before any human review; its failure
and prior drafts are retained in [preparation evidence](complete-release-preparation.zip).

| Source path at `92f948ad9faea69e00485d59c0680694e21bc30e` | Git-blob SHA-256 |
| --- | --- |
| `README.md` | `5a43ded264071388de30e800bc937772fa2cd485797cc27ed8e41ebbbb42c940` |
| `release/plugin-marketplace/README.md` | `c332eec96d9dc844c1f63265d0fd7c245c581974d4aca3eb3e22214bcd1cdb4c` |
| `plugins/verity-plane/codex/README.md` | `1e5ddb4d7399eb0d8535ba6758e49a0e9cdddae25fa06b86bb757cfbbd91e57d` |
| `plugins/verity-plane/claude-code/README.md` | `585d8e150f7523612dc34d4818a31c26f8c67331cf48eefb8e37b65e8079adba` |
| `docs/notes/plugin-installation-guide.md` | `22474d27a9d81931e96d930152cbe12876aceb9dec93a0f0edf2ed50c4cb38b7` |
| `docs/notes/plugin-marketplace-publication.md` | `8f41926cb06525046f264f283fb3fe0bd39383db94d20362e9556e7e5cf1ce58` |
| `docs/notes/developing-se-harness.md` | `998993410965121f0817ae6c63256d2fd1af7da33c5ad63c3914a15b79abb412` |
| `docs/notes/harness-installation-and-upgrades.md` | `0f99f65b22e737116ae599a2e0a75fdfdf83bbd31cf61c6d07a070617fd27203` |
| `docs/notes/hosted-artifact-graph.md` | `04d11a302f3bdb892be2d49e57191fa446b35081b661d01f8ddef9ca9b0c7dbc` |
| `docs/engineering/release-0-23-0/evidence/WO-RLS-047/README.md` | `9c755ca77710a2e5bc09b83f2d413323d1ec57920e5f3f289bdb12a6a2784218` |
