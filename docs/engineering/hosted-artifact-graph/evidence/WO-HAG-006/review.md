# Review the hosted evaluator reconciliation and CI correction

WO-HAG-005 reconciles the existing hosted branch with public evaluator 0.22.1.
WO-HAG-006 fixes the CI assessor for a stacked branch whose comparison base
predates that already integrated adoption. Both use the approved bounded scope.
This assessment covers VER-HAG-004 and VER-HAG-005; it does not verify the service.

## Delivered behavior

The hosted definitions now select public 0.22.1, with their accepted predecessors
preserved. DEC-HAG-001 records mmzen's existing extend-evaluator choice using the
supported authority-owner field. The prior HAG owner and in-progress state stay
unchanged. The branch incorporates approved main and retains its original PR target.

When the original comparison base has no target release, the CI assessor requires
one common ancestor with fetched default-branch history. It compares exact release
and transaction bytes, complete evaluator identity, configuration and lock. It still
binds the original base lock and executes the independent released evaluator.
Missing, malformed, ambiguous or changed authority refuses. No new dependency,
service or evaluator policy copy was added.

## Criteria and evidence

| Criterion | Observed result | Evidence |
| --- | --- | --- |
| RC-01, CI-05 preservation | Pass: 133 unchanged original HAG files, 18 checked VREC/bound paths, original live packet archived exactly before the supported rebind, historical packet body unchanged | preservation.json; WO-HAG-001-handoff-before.txt; VER-HAG-004-accepted-before.txt; amendment.json |
| RC-02 exact public governor and decision | Pass: isolated public 0.22.1 identity, doctor, validation and decision recording; development source remains 0.22.2 | checks.zip actual-assess.json and evaluator-facts.json; ../WO-HAG-005/reconciliation-checks.zip and amendment.json |
| RC-03 released draft admission | Pass: seven real released-evaluator probes; incomplete drafts distinguished from invalid records; reference formal bytes preserved | ../WO-HAG-005/reconciliation-checks.zip draft-probe-results.json and reference-projection.json |
| RC-04 integration | Pass: 180 reviewed main transport paths checked; the current developer note is the sole subsequent explicitly authorized correction among those paths | preservation.json; ../WO-HAG-005/integration-manifest.json |
| CI-01/02 trust and refusal cases | Pass: 40 focused tests on Windows (2 POSIX skips), 40 on Linux (no skips), synthetic 7.4.0/7.5.0 history and altered/missing/ambiguous input cases | checks.zip focused-windows-2.json and focused-linux-2.json |
| CI-03 actual original-base assessment | Pass at implementation commit: original base retained; exact main anchor, release/transaction equality and installed public governor proved; checkout unchanged | assessment-proof.json; checks.zip actual-plan.json, actual-assess.json and assess-result.json |
| RC-05, CI-04 local regression | Pass: 1,316 tests, 23 reported skips; distribution and CLI checks pass; 1,968 artifacts, zero errors, 63 existing warnings | checks.zip source-full.json, distribution-check.json, cli-smoke.json and correction-validation.json |
| CI-06 handoff and capture | Recorded by the later released lifecycle and verification preparation outputs; original-base combined scope includes WO-HAG-001/003/004/005/006 | lifecycle.zip and the subsequent VREC |
| CI-04/RC-05 actual PR CI | Pending publication at this assessment; must pass before merge | Current PR #535 checks, reported separately |

## Failures and review

Both first focused runs refused missing history correctly but returned a generic Git
message that broke the established diagnostic assertion. The correction explains
that the trusted base has no target release and adopted history is unavailable.
Both complete focused reruns pass. The original failure logs remain in checks.zip.
Read-only command recovery mistakes (an extra positional repository, an old evaluator
used for context reads, and transient helper parsing errors) are retained separately
from qualification results; no lifecycle write used those failed commands.

The implementation adds one bounded history lookup to the existing assessor. The
existing transition selector, origin checks and clean-worktree requirements remain.
This is the smallest change that preserves the approved PR base and independent
adoption proof. Retargeting would change the approved boundary; trusting a candidate
release alone would lose independent evidence. Regression tests check distinct
history and tampering failures, rather than only mirroring successful output.

## Limits and next decision

WO-HAG-001 remains in progress. Zero hosted service scenarios have run; all twelve
VER-HAG-001 cases, the packaged walkthrough and restart/restore remain required.
RISK-HAG-001 stays raised, with Cypher and the private sandbox controls preserved.
VREC-HAG-001/002 keep their historical candidates and complete evidence bytes.

The aggregate ready record asks the human to accept only this prerequisite
reconciliation and CI correction. Merge, release, deployment and hosted-service
verification are excluded. PR #535 remains an unfinished-work draft targeting
codex/hosted-artifact-graph-inputs. Existing review-publication authority covers
this package and a later separately supplied verification decision.
