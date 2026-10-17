# Public delivery verification assessment

Evaluator/client 0.23.0 and Verity Plane 0.2.7 were delivered under the unchanged
complete-release approval for RLS-SEH-034. The five-surface report is complete.
This assessment covers WO-RLS-047 under VER-RLS-041. The human verification of
these post-publication observations remains separate from the earlier binary
verification and release decision.

| Requirement | Observed result | Retained evidence |
| --- | --- | --- |
| REQ-RLO-019 | Pass. Independent public GitHub/PyPI archives match the approved hashes. Clean evaluator install and qualification pass. Both Windows CLIs pass fresh installation and actual 0.2.6-to-0.2.7 update, installed-file comparison, skill discovery and bundled evaluator setup. All ten frozen source documents, composed links, tagged private-sandbox source and public Pages provenance match. | evaluator-public-install.json, the four public-route receipts, documentation-observations.json and pages-observations.json |
| REQ-RLO-020 | Pass. All five surfaces have matching observed identities and content-bound evidence. Failures and recovery remain visible. | observations.json and delivery-result.json |
| REQ-RLO-023 | Pass. The existing publisher reused exact archives and the staged marketplace child. v0.23.0, release/0.23 and last resolve to the approved binary candidate; latest is v0.23.0. Protected receipt integrations preserve the frozen plan. | publisher.json, marketplace-public-ref.json, maintenance-line.json, release-marker-receipt.json and integration-receipts.json |

## Failures and recovery

The version-specific PyPI metadata endpoint returned 404 twice. The official
PyPI package index exposed both exact archives. Independent downloads, archive
hashes, attestations and a clean public install then passed. The original HTTP
failures and diagnostic results remain in evaluator-public-install.json.

Codex CLI 0.162.0-alpha.17.2 timed out twice during native marketplace upgrade.
Re-adding the same source alone reported alreadyAdded and left the old snapshot.
Recovery used native marketplace remove/add with the same public repository and
explicit plugin-marketplace ref in the disposable profile. The installed 0.2.6
plugin and its exact files remained intact before the successful native update
to 0.2.7. This qualifies the observed recovery route; the ordinary upgrade
timeouts remain recorded and are not reported as passing attempts. No global
setting or operator-host plugin changed.

The first documentation helper tried to resolve package-relative README links
inside the source tree. The corrected observation checks source links in the
source tree and package links in the actual composed marketplace. The helper
failure is retained; no approved document or package bytes changed.

The first publisher completion refused absent committed public observations.
After their protected integration, marker promotion passed. The same job's
report still read the previous pending marker observation. Independent marker
readback and the final receipt integration resolved that reporting dependency.
The final publisher result is successful. No check was waived.

## Scope and limits

The binary candidate remains 48e851bbc94d7fb0c06e9b80666c3860cb5f8c15,
already verified in VREC-SEH-034. This later candidate contains delivery evidence
and work completion, not replacement binaries. The full execution comparison
retains b43bef8c213ecabee94447a8fb52c32294c7ab75, the release-review main baseline.
The review PR compares its own new closeout changes with current main.

R23-NATIVE-010/011 remain open under DEC-RLS-010 / RISK-RLS-008. Codex Windows
desktop remains unverified under DEC-RLS-011 / RISK-RLS-009. These public-route
checks do not claim live model or desktop testing. Git remains authoritative;
the hosted service stays private and source-built, with evaluator 0.22.1.
Repository adoption, user-host updates and public service deployment are excluded.

## Verification preparation recovery

The initial capture could not create its Windows temporary worktree. A second
attempt assessed the receipts but refused source qualification because the helper
used an installed-package runtime. The corrected invocation uses candidate source
for this evidence-only check; released 0.22.1 remains the lifecycle governor.
Both failed attempts and helper versions are retained in closeout-capture-recovery.zip.
No release payload, public observation, requirement or human decision changed.

Base Python also resolved installed distribution metadata outside the checkout
and was refused with RID018. The final retry uses the existing disposable
source-test environment after confirming that it has no installed se-harness
distribution. This additional refusal and environment check are preserved in
closeout-capture-runtime-recovery.zip. The same identity checks remain required.
