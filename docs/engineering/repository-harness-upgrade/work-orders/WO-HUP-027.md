+++
id = "WO-HUP-027"
type = "work_order"
title = "Complete CI compatibility with schema-5 adoption"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved WO-HUP-027 and required commit-bound verification in VREC-HUP-026; integration relies on the corrected CI evaluator identity and schema-5 rehearsal checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".github/workflows/engineering-harness.yml",
  "tests/test_ci_pipeline.py",
  "repository_tools/upgrade_rehearsal.py",
  "tests/test_upgrade_rehearsal.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-027.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027-evaluator.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-026.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-026-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T09:24:09Z"
decided_by = "mmzen"
reason = "Human mmzen: Approve WO-HUP-027 and required verification. Approves the reviewed four-file CI correction and required commit-bound verification in VREC-HUP-026. Reviewed work-order SHA256 a2b5ef5207baf04e5f2997206852d4bdcc81c2037d202699d2c67ad7e4a1a26f; patch SHA256 44c92fb2d3f4845e9c8de2dbeac05f964d4e98d089787c74c872906c08555751. Human verification remains separate; existing push/PR authority applies only after verification."
scope_paths = [".github/workflows/engineering-harness.yml", "tests/test_ci_pipeline.py", "repository_tools/upgrade_rehearsal.py", "tests/test_upgrade_rehearsal.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-027.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027-evaluator.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-026.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-026-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T09:24:58Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Complete CI compatibility with schema-5 adoption

## Objective

The Engineering Harness job on PR #520 can resolve the adopted released 0.21.0
resources with the exact archive identity recorded in the repository lock.
The Linux and Windows upgrade rehearsals also accept a valid schema-5
external-resource predecessor and preserve its layout across the handover.
Reuse SPEC-IAR-016 IAR-EXT-002, IAR-EXT-004 and IAR-EXT-009, and the usable-repository
criterion A0210-04 in VER-HUP-003. No new product contract is needed.

## Observed failure

The validate job in run 36988047041 fails at check-pr with:
"WO-HUP-003: selected evaluator archive_name does not match installed resources".
CI installs by index package name. That installation has no direct archive name;
the schema-5 selection records an exact wheel and archive digest. A fresh isolated
index installation reproduces the failure. Installing the digest-verified public
wheel restores the PR check. Earlier local checks used a wheel installation and
therefore missed this CI installation difference.

The later Linux and Windows jobs in run 36988046990 fail because
repository_tools.upgrade_rehearsal recognizes only schema-3 repository ownership
and schema-4 plugin ownership. Both report "the exported lock has unsupported
ownership for schema 5". The source and package evidence jobs, predecessor
assessment, publication rehearsal and CodeQL checks pass.

WO-HUP-003, WO-HUP-005 and WO-HUP-026 are implemented, and VREC-HUP-025 is verified.
Preserve those states, decisions and evidence. Do not reopen completed work or
rewrite its approved scope. This correction needs its own verification record.
The unchanged comparison base remains 695d6773dc86f25691a9799e969bcca014207837.

## In scope

- In the repository-owned Engineering Harness workflow, download only the pinned
  evaluator wheel to runner temporary storage. Before installation, check that
  exactly one wheel exists and its version, filename and SHA-256 match the lock.
- Install that local wheel into the existing isolated evaluator environment with
  no dependency or index lookup during installation. Keep the existing public
  download source, exact version pin, trigger, permissions and required checks.
- Add deterministic tests in tests/test_ci_pipeline.py that execute the proposed
  validation block. Cover a matching wheel and corrupt, missing, multiple,
  misnamed, path-escaping, wrong-version and incomplete-identity inputs.
- Extend the existing rehearsal lock classifier for schema 5 with
  released-resources-v1 and no skill_ownership field. Reject external-resource
  declarations on older schemas and preserve version, payload, doctor, validation,
  unchanged-source, deterministic replay and ownership/layout preservation checks.
- Extend its existing fixture and tests for external-to-external handover, invalid
  layouts or ownership, unknown schemas, forbidden layout switches and successor
  version/payload mismatches. Preserve the legacy retirement refusal control.
- Retain the real CI failures, isolated reproductions, reviewed patch, actual checks
  and correction assessment; prepare VREC-HUP-026 at an exact clean candidate.

## Out of scope

Released evaluator code, resource resolver semantics, lock edits, product workflow
templates, other workflows, new versions, credentials, native host tests, further
resource retirement, publication and merge. Existing required gates are preserved.
The public release and prior verification record remain unchanged.

## Proposed assurance and decision envelope

Required commit-bound verification is proposed because the changed CI bootstrap
establishes the evaluator identity used for later checks. Human confirmation is
pending; no assurance decision-maker is invented in draft metadata.

Approval permits the exact implementation, local checks and commits, evidence
retention, completion and VREC-HUP-026 preparation. VREC-HUP-026 covers this
correction under VER-HUP-003; retained VREC-HUP-025 continues to cover the original
adoption. Reuse its migration and native evidence without claiming new observations.
Human verification remains separate. The human's existing push/PR direction applies
to updating PR #520 after the correction is verified; it does not authorize merge.

## Constraints and expected change surface

One workflow, the existing upgrade-rehearsal helper and their two existing
test modules change. Reuse pip download, a short
stdlib digest check and local-wheel installation; do not add another installer,
resolver or dependency. Run governance with the repository-selected released
0.21.0 evaluator outside the checkout. Treat lock fields as data, not paths to
execute; compare against the single downloaded filename before installation.
The workflow remains a repository-owned editable seed. Product-template adoption
for other repositories is separate work and is not silently included here.

## Required verification

1. Preserve the hosted failure and reproduce it in a separate index-installed
   public 0.21.0 environment. Confirm the wheel name/digest against the lock and
   public package before local-file installation. The unchanged selected PR
   passes check-pr and released-root qualification with that installation.
2. Execute the validation block and upgrade-rehearsal tests for normal and refusal
   inputs. Rehearse the actual 0.21.0-to-CI-built-0.21.1 handover twice in disposable
   exports and compare semantic digests, preserving the original checkout. Run the
   existing CI-pipeline suite, full-scale source suite, distribution checks and
   released evaluator validation. No required check is weakened or skipped.
3. Review the exact diff, complete scope/handoff and capture VREC-HUP-026 at the
   clean correction candidate. Check the actual four-work-order PR body against
   the original base after adding WO-HUP-027.
4. Obtain the separate human verification decision before updating the PR. The
   failed hosted job and applicable Linux/Windows jobs must pass before integration.
   Claude and Codex desktop remain unverified; no new host evidence is claimed.

## Evidence to record

Retain CI log and current run state, original reproduction and any failed probe,
corrected probe results, patch digest, review, regression/full-suite results and
completion receipts under evidence/WO-HUP-027/. Raw logs may remain outside the
repository with their retrieval paths and digests. Use the declared evaluator and
VREC paths for generated evidence. A proposal or prototype is not implementation.

## Stop and escalate conditions

Stop the affected action for missing public identity, a required failing check,
a necessary path outside this scope, or a change to accepted behavior. Do not edit
the lock, modify an installed released evaluator, bypass resource identity checks
or relabel a prototype as proof of the final candidate.

## Completion report format

Report the installation correction, actual checks, exact candidate, verification
state and hosted CI result. Keep remaining human acceptance and merge decisions
explicit. Preserve failed evidence alongside successful corrected runs.
