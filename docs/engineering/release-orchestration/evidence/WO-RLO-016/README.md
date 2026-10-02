# Complete-release activation review

Status: reviewed configuration proposal prepared by Codex; no provider mutation.
Human verification of this implementation and the later one-time configuration
decision remain pending. This review does not authorize a release.

## Observed controls

Read-only GitHub API snapshots in this directory retain commands, UTC observation
times, exit codes and public control data. No token, cookie or credential is stored.

| Control | Observed result | Effect |
| --- | --- | --- |
| `pypi` environment | Required reviewer `mmzen`; self-review prevention false | A separate human provider decision is currently required. |
| `pypi` allowed refs | One custom policy: branch `main` | Preserve exactly. |
| GitHub Pages | Branch protection rule; no required reviewer observed | No reviewer removal proposed. |
| Main ruleset 20693381 | Pull request, required `validate` check, deletion and non-fast-forward protections | Preserve; never use an administrator bypass for release integration. |
| Publisher workflow | One main-only RLS input, isolated qualification, credential jobs using inert inputs, PyPI OIDC | Implementation retains these boundaries. |
| PyPI Trusted Publisher | Current account-side binding not accessible through the GitHub API | Unverified; confirm before activation. Historical publication is not a readback of current settings. |

The live environment already permits administrator bypass. This proposal neither
adds nor uses that permission. It leaves unrelated controls unchanged.

## Exact proposal and recovery

`configuration-proposal.json` retains the supported request fields before and
after, plus the recovery request. The sole intended change is `reviewers: []`
on `PUT /repos/mmzen/se_harness/environments/pypi`. Keep the main-only custom
branch policy, wait timer and self-review setting unchanged. Do not send the
read-only response's IDs or URL fields back as configuration.

Before apply, read the environment and branch policies again. Compare normalized
settings with the retained `before` value. If any control differs, refresh this
review rather than overwriting it. Obtain the owner's decision on the concrete
diff after implementation verification, integration and product release/adoption.
No apply is authorized by the present work order.

After the later authorized update, read back the environment, main-only branch
policy, main protections and PyPI binding. Confirm only the redundant reviewer
rule disappeared. If readback or readiness fails, restore `recovery` under that
configuration decision and read back again. Do not dispatch a complete release
while a required control remains unverified or a reviewer is still required.

## Rollout order

1. Verify WO-RLO-014/015/016 at their exact candidate and integrate the reviewed PR.
2. Release the supporting evaluator/plugin under the currently selected release
   rules and actual authority. Candidate instructions do not govern their rollout.
3. Separately adopt that release in this repository.
4. Confirm Trusted Publishing still binds `mmzen/se_harness`, `publish-pypi.yml`
   and the `pypi` environment. Confirm required host credentials and checks.
5. Review and apply the exact one-time environment change; retain all readbacks.
6. Prepare the first expressly selected complete-release package. Complete its
   candidate assurance before the one final release approval.

The implementation fixture tests exercise reviewer-present refusal, main-only
controls, exact matching grants, unknown responses and safe retry. They do not
claim that the live change has been applied or that future credentials are ready.
