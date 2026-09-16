+++
id = "WO-HUP-020"
type = "work_order"
title = "Support plugin ownership in the existing CI assessor"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[assurance]
commit_bound_verification = "required"
rationale = "Future CI and integration decisions rely on the assessor distinguishing a legitimate provider switch from evaluator or lock drift. The corrected PR requires assurance at its new candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "scripts/validate_governor_transition.py",
  "tests/test_governor_transition.py",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-020.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-020.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-020.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-020/",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-019.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-019-evaluator.json",
]

[relations]
implements = ["REQ-HUP-008", "REQ-HUP-024"]
specifications = ["SPEC-HUP-004", "SPEC-HUP-012", "SPEC-HUP-020"]
architecture = ["ARCH-HUP-003", "ADR-HUP-001"]
verification = ["VER-HUP-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T14:03:02Z"
decided_by = "engineering-owner"
reason = "The owner approved this exact reviewed package with \"i approve\" on 2026-09-16, exercising the engineering-owner decision for WO-HUP-020. Reviewed SHA-256 c245f873e89869a6f4464c1ef15d4070ecc0b1f1b41f3b0c6e9b76e8e1861661. This approves the definition or bounded execution scope; it records no assurance or external-delivery decision."
scope_paths = ["scripts/validate_governor_transition.py", "tests/test_governor_transition.py", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-020.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-020.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-020.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-020/", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-019.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-019-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-16T14:05:43Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved bounded assessor correction under DR-015 after passing start preflight; reviewed owner approval is recorded."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-16T14:39:13Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Complete the approved bounded correction under DR-015: review, 1078-test local suite, final comparison regressions, required checks, committed CI replay and combined scope pass. Retained evidence distinguishes the final candidate capture and pending hosted CI."
+++

# Support plugin ownership in the existing CI assessor

## Objective and baseline

Repair the predecessor-assessment failure on PR #487 by accepting supported
skill ownership without weakening evaluator or unrelated lock checks. The
remediation baseline is 0dadc352b3a5e6c64c721e1c688cc215438ddd7f on
work/repository-cleanup. The complete PR remains based on
f05c478a29c39f94968fdc842a34c861d30a42ac and includes implemented WO-PLG-025.

The owner accepted the bounded KISS proposal with "ok go". This authorizes
preparation of these concrete drafts; it does not claim approval of their
previously unseen bytes. Approve SPEC-HUP-020, VER-HUP-020 and this work order
through the released evaluator before implementation. The two earlier
specifications are read unchanged, with the new addendum's explicit scope.

## In scope

1. Apply SPEC-HUP-020 in scripts/validate_governor_transition.py: supported
   schema-4 parsing and a bounded provider-switch comparison using the existing
   catalogue from the trusted base as data. Retain standard-library isolation.
2. Extend tests/test_governor_transition.py with the meaningful acceptance and
   refusal cases in VER-HUP-020, reusing its fixtures and existing upgrade tests.
3. Update this domain index and retain the original failure, local checks,
   complete scope comparison and normal design/implementation review findings.
4. Run required checks, retain the released handoff, record actual completion,
   commit the corrected candidate and prepare VREC-HUP-019 with the released
   capture command. Select WO-HUP-020 and implemented WO-PLG-025 for that one
   aggregate record, with VER-HUP-020 and VER-PLG-025 evidence coverage.

## Out of scope

Changes to product runtime, installer, catalogue contents, templates, root
configuration/lock, evaluator version, workflows, other tests, plugin packages,
marketplace refs, historical artifact bodies or evidence, user installations,
credentials and external policy. VREC-PLG-022 and all earlier verification and
release records remain unchanged. No release build, merge or publication.

## Authorized decision envelope

After recorded approval, Codex may start, implement, test, make ordinary local
commits, record completion and prepare required verification under DR-015.
It may choose private helpers and fixture organization within these paths.
The existing ARCH-HUP-003/ADR-HUP-001 responsibilities and trust boundary remain;
no new architecture or general migration mechanism is needed.

Use baseline 0dadc352b3a5e6c64c721e1c688cc215438ddd7f for this WO's scope/handoff.
Use both WO-PLG-025 and WO-HUP-020 for complete PR scope. Earlier cleanup changes
are inputs, not permission to edit their completed scope or historical records.
The aggregate preparation above is authorized by this WO approval and the
unchanged WO-PLG-025 execution grant, subject to relevant input/evidence checks.
Owner assurance and delivery of the corrected candidate follow their existing
decision procedures. This draft does not extend prior delivery authorization
to an unidentified new candidate.

## Verification and evidence

Execute VER-HUP-020 and the repository-required checks. Keep raw output and
concise summaries in the keyed evidence directory. Preserve the failing CI
observation and distinguish local acceptance from hosted checks pending later
delivery. Recheck that the marketplace publication ref remains unchanged.
Complete exactly the nine paths/prefixes in execution_scope; verify both this
remediation diff and the combined PR scope at their respective bases.

## Stop and escalate conditions

Stop the affected operation for missing approval, failed integrity or required
check, evidence mismatch, an extra implementation path, an exception that
permits unrelated drift, a need to import candidate code, or changed published
plugin inputs. Report the exact failed condition and bounded recovery.

## Completion report

State accepted ownership cases, retained rejection behavior, actual checks,
candidate identity, evidence reuse basis, material limitations and the next
accountable decision. Record implemented only after local work and required
evidence are complete. Prepare the new VREC without claiming owner verification.
