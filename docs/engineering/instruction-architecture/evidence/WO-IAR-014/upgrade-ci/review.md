# Upgrade rehearsal failure in PR #489

## Current result

Hosted CI remains failed. No new commit or push has been made in this correction.
The diagnostic fix is tested locally under approved WO-IAR-014. The rehearsal
adaptation is proposed in draft WO-IAR-019 and has not been implemented.

## Observed failure

Both [Linux](https://github.com/mmzen/se_harness/actions/runs/36309978980/job/108594145000)
and [Windows](https://github.com/mmzen/se_harness/actions/runs/36309978980/job/108594144990)
fail at successor-upgrade-apply. The exact downloaded candidate wheel reproduced:

```text
DiscoveryError: legacy entry retirement requires --instruction-delivery-evidence; no files were written
```

PR head: 253310ad21b967b35311c4f5d1af8ad341e92c1b.
Hosted candidate merge: fed7587bbe4ee994a1988fc232e187b9f2bb0561.
Wheel SHA-256: 1f4bd1a08424783b4ef96cf76a1153dd6b2714d26362f77ed85354fa0f0371c8.
The downloaded checksum matched. Every predecessor file was unchanged after
the refusal. See hosted-reproduction.json and the complete stderr alongside it.

The previous Linux source-identity and governed PR-scope failures are resolved
in the hosted run. This failure occurs later in the pipeline. The integration
package jobs did not run because they depend on the failed rehearsal.

## Local correction

The CLI now handles DiscoveryError as a normal refusal: exit 2, an actionable
diagnostic, no traceback and no writes. Receipt requirements are unchanged.
The regression exercises absent and stale receipts through the actual CLI
handler. Before the fix both cases raised uncaught exceptions; afterward they
return the expected refusal and preserve all target bytes. This diagnostic fix
alone does not make the positive upgrade rehearsal pass.

- Focused installer/discovery tests: 18 passed.
- Full-scale Windows regression: 1,119 tests, no failures/errors, 16 skips.
- Distribution validation and CLI help: passed.
- Released 0.18.0 doctor, validation and WO-IAR-014 review preflight: passed.
- Draft graph validation and WO-IAR-019 approval preview: passed. The preview
  did not approve or start the work order.
- Original regression failure, hosted traceback and invalid argument attempts
  remain retained; no failed observation is relabelled as a pass.

## Proposed correction to the rehearsal

Review ../../../work-orders/WO-IAR-019.md. Its proposed assurance classification is required.

1. Prove that the actual installed candidate refuses retirement without delivery
   evidence and leaves the disposable export unchanged.
2. Supply an explicitly synthetic, export-bound fixture to the real upgrade.
   Report it as an installer test input, with native delivery not assessed.
3. Keep every existing real handover assertion and both runs on each platform.
   Failed applies, bad locks, changed ownership or inconsistent digests still fail.

The production guard stays unchanged. Native startup/compaction demonstrations
remain required under VER-IAR-014 and WO-IAR-015; these fixture runs cannot
satisfy them or justify claiming the broader evolution complete.

The proposed code paths are repository_tools/upgrade_rehearsal.py and
tests/test_upgrade_rehearsal.py, plus its explanatory note, own record and evidence.
These paths are outside the active implementation work orders. The completed
WO-IAR-017 cannot be reused as authority for a new test change. The draft proposes
no workflow or credential change, no network access and no release/adoption.

Draft WO-IAR-019 SHA-256: c8829fdc143a4d6ffaab70f7943b76597b6aeec88314d252a83d55d84ce65dc6.
Existing WO-IAR-014 remains in_progress. WO-IAR-019 remains draft.

## Decision needed

Approve WO-IAR-019's bounded scope and required assurance classification to
implement this correction and update PR #489 under the existing push authority.
The installed Change skill's Work orders reference says: "Ask the accountable
owner for a scope change when necessary"; its SKILL.md requires following the
approved scope and existing installed procedure. The proposed paths are the
specific reason this decision is needed; the already approved diagnostic work
did not need renewed permission.
