+++
id = "WO-IAR-019"
type = "work_order"
title = "Exercise guarded instruction retirement in the upgrade rehearsal"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed for human approval: CI and subsequent integration decisions rely on the rehearsal distinguishing a tested installer transaction from native host qualification. The changed executable test behavior requires assurance bound to the candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/upgrade_rehearsal.py",
  "tests/test_upgrade_rehearsal.py",
  "docs/notes/evaluator-migration-rehearsal.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-019.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-019/",
]

[relations]
implements = ["REQ-IAR-025", "REQ-ECP-012"]
specifications = ["SPEC-IAR-014", "SPEC-ECP-007", "SPEC-ECP-025"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-IAR-014", "VER-ECP-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T10:01:30Z"
decided_by = "engineering-owner"
reason = "The human replied I approve to the presented WO-IAR-019 scope and required assurance classification. Reviewed SHA-256 c8829fdc143a4d6ffaab70f7943b76597b6aeec88314d252a83d55d84ce65dc6. Codex applies that recorded decision; no native qualification, merge or release is approved."
scope_paths = ["repository_tools/upgrade_rehearsal.py", "tests/test_upgrade_rehearsal.py", "docs/notes/evaluator-migration-rehearsal.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-019.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-019/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T10:02:28Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts execution under the recorded human scope approval and DR-WO-START."
+++

# Exercise guarded instruction retirement in the upgrade rehearsal

## Objective

Make the existing Windows and Linux rehearsal test the candidate's guarded
instruction migration without claiming that a synthetic host trace proves
native delivery. This work order is a proposal and grants no execution authority.

At PR #489 head 253310ad21b967b35311c4f5d1af8ad341e92c1b, both platforms fail
at successor-upgrade-apply. The candidate requires delivery evidence to remove
recognized AGENTS/CLAUDE fragments; the rehearsal supplies none. The exact
hosted wheel reproduces that refusal locally and preserves every prior byte.
The separate CLI diagnostic correction belongs to existing WO-IAR-014.

## In scope

1. Read the real successor's JSON upgrade preview. If it reports that retiring
   the old instruction entries requires delivery evidence, first run the real
   upgrade without that evidence as a negative control. Require its refusal and
   prove that it changed no file in the disposable repository.
2. Prepare a clearly labelled synthetic delivery receipt and trace only inside
   that disposable test workspace. Bind them to that export, its predecessor
   lock, candidate version and planned entry. Reuse the installed candidate's
   planning API in its isolated interpreter to obtain planned bytes; do not
   duplicate template rendering or patch the installer, guard or CLI.
3. Pass the fixture to the real successor upgrade using the existing
   --instruction-delivery-evidence argument. Continue every existing handover
   assertion, including the real transaction, successor doctor/validation,
   predecessor rejection, ownership preservation, payload binding, cleanup,
   two-run determinism and cross-platform agreement.
4. Identify the receipt and trace as synthetic installer-test inputs in the
   retained result and explanatory documentation. Report native host delivery
   as not assessed by this rehearsal. No artifact or summary may describe the
   fixture as an observed native event or complete product qualification.
5. Extend the existing rehearsal tests for both required and unneeded delivery
   evidence, refusal-control failures, failed positive upgrades, and the
   explicit qualification boundary. Keep existing failure assertions intact.

Use the preview's declared requirement, not hard-coded release pairs. Older
or already migrated installations that do not request delivery evidence retain
their existing rehearsal path. Test fixtures are not copied into the operational
checkout, shipped product, integration package, or real adoption instructions.

## Design rationale

SPEC-ECP-025 requires a network-free rehearsal with credentials filtered out.
Running authenticated agent sessions inside it would require a separate design
and change that boundary. The installer already has synthetic receipt fixtures
for testing its transaction and refusal behavior. Extending that testing
boundary to the real installed-wheel rehearsal is the smaller correction.

This supplies an explicit test input; it does not simulate a successful
installer call or treat the missing-evidence refusal as successful migration.
The accepted VER-IAR-014 native startup/compaction demonstrations remain
separate required evidence under WO-IAR-015. They are still incomplete.

## Out of scope

No production bypass, relaxed receipt validation, altered lifecycle gate,
accepted artifact/history rewrite, or replacement of native qualification with
fixtures. No workflow permissions, credentials, network access, host settings,
new release-specific scenario framework, root self-upgrade, merge or publication.
No changes to VREC-IAR-009 or the work it already verifies.

## Authorized decision envelope

After human approval, the executor may start, implement, test, retain evidence,
record actual completion and prepare the required verification under the
installed execution procedure. Approval must cover the required assurance
classification above. No new or changed definition is approved by implication.

The existing user authorization to push and update PR #489 supplies delivery
context for the correction on work/progressive-instruction-discovery in
mmzen/se_harness. It grants no merge, release or native-support acceptance.

## Required verification

- Focused rehearsal tests exercise the real argument boundaries and retain
  existing failure behavior. Fixture metadata must explicitly deny native
  qualification; failed real upgrades must still fail the rehearsal.
- The absent-receipt control refuses without writes. The positive fixture
  drives the actual installed candidate's upgrade and all handover checks.
- Two real runs on each hosted platform pass and produce the same canonical
  lock digest across both runs and platforms. Missing runs remain missing.
- Run the repository-required regression and distribution checks, released
  doctor/validate, phase preflight, complete scope/handoff and combined PR checks.
- Review retained result metadata and the integration packaging path to ensure
  synthetic inputs cannot be mistaken for native qualification or shipped as
  adoption evidence. Keep WO-IAR-015's unverified claims visible.

## Evidence and completion

Retain candidate commit and wheel identity, command arguments, outputs, fixture
classification, before/after byte comparison, actual platform results, semantic
digests, diff review and released-evaluator checks under evidence/WO-IAR-019/.
Do not claim that this CI correction completes the broader instruction evolution.

## Stop conditions

Stop for missing authority, paths beyond this scope, changed product semantics,
failed integrity/required checks, a refusal control that writes files, or any
result that claims synthetic input is native evidence. Report the exact issue
and required scope or definition decision before the affected action continues.
