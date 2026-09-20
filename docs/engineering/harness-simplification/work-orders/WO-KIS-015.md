+++
id = "WO-KIS-015"
type = "work_order"
title = "Resolve recovery PR scope and onboarding integration"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-20"
updated = "2026-09-20"

[assurance]
commit_bound_verification = "required"
rationale = "The correction changes a documentation acceptance check and integration scope; retain a new candidate record without rebinding the two previously verified repairs."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/decisions/DEC-KIS-001.md",
  "docs/engineering/harness-simplification/evidence/VREC-KIS-015-evaluator.json",
  "docs/engineering/harness-simplification/evidence/WO-KIS-015/",
  "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/README.md",
  "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment-evidence.zip",
  "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment.html",
  "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment.md",
  "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-recovery-plan.html",
  "docs/engineering/harness-simplification/recovery-2026-09-19.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-011.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-013.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-005.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-007.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-015.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-005.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-006.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-007.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-008.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-011.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-013.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-015.md",
  "tests/test_public_onboarding.py"
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024", "SPEC-DST-029"]
verification = ["VER-KIS-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T15:28:22Z"
decided_by = "engineering-owner"
reason = "On 2026-09-20 the owner instructed \"you can resolve this\" after the PR #488 scope blocker was reported, continuing the authorized push and PR. Record the bounded corrective scope and applicable check plan for carrying the already reviewed recovery package, preserving accepted README bytes, and reconciling the upstream onboarding test. This uses the supplied correction authority; it does not claim the owner separately reviewed these newly authored record bytes, accept the future corrected candidate, or authorize merge/release. Draft bytes recorded for reproducibility: a1e9d48614f93e92c3c11b671b0f1e243cbc26a47fdf3ac913657a862de4a357"
scope_paths = ["docs/engineering/harness-simplification/README.md", "docs/engineering/harness-simplification/decisions/DEC-KIS-001.md", "docs/engineering/harness-simplification/evidence/VREC-KIS-015-evaluator.json", "docs/engineering/harness-simplification/evidence/WO-KIS-015/", "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/README.md", "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment-evidence.zip", "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment.html", "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-assessment.md", "docs/engineering/harness-simplification/evidence/recovery-2026-09-19/se-harness-recovery-plan.html", "docs/engineering/harness-simplification/recovery-2026-09-19.md", "docs/engineering/harness-simplification/requirements/REQ-KIS-011.md", "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md", "docs/engineering/harness-simplification/requirements/REQ-KIS-013.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-005.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-007.md", "docs/engineering/harness-simplification/verification-records/VREC-KIS-015.md", "docs/engineering/harness-simplification/verification/VER-KIS-005.md", "docs/engineering/harness-simplification/verification/VER-KIS-006.md", "docs/engineering/harness-simplification/verification/VER-KIS-007.md", "docs/engineering/harness-simplification/verification/VER-KIS-008.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-011.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-013.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-015.md", "tests/test_public_onboarding.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-20T15:28:46Z"
decided_by = "delegated-executor"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the bounded PR #488 integration correction under the owner instruction to resolve it and the recorded scope approval."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-20T15:40:01Z"
decided_by = "delegated-executor"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex completed the bounded PR #488 correction. All applicable hosted checks pass on f55db0962a812a9b4a79bc543feca4d74f652d7f; the full Windows 1094-test suite and focused/rejection checks pass. Full PR scope is checked against actual main with the three declared work orders. Accepted README, existing definitions, decisions and verified-record evidence are preserved. No new assurance acceptance or merge is inferred."
+++

# Resolve recovery PR scope and onboarding integration

## Objective and authority

Resolve the scope failure on PR #488 under the owner's instruction "you can
resolve this", following the already authorized push and PR. Carry the exact
previously approved recovery planning package through the existing combined-PR
scope check. Reconcile its README acceptance with the newer test on main.
This is a prospective integration correction, not retroactive approval of
historical implementation or a new product behavior.

## In scope

- Admit the twenty enumerated planning paths already included in the reviewed,
  owner-approved recovery package. Their definitions, decisions and retained
  source evidence keep their current bytes and lifecycle histories.
- Update only the two untyped package indexes to state the current implemented
  and verified repair status and the three approved, unstarted work orders.
- In tests/test_public_onboarding.py, compare the four published native plugin
  commands only with the README plugin subsection. Keep the exact argument
  checks and all linked manual-installation checks. The accepted inline CLI
  section is a separate route; it is neither a plugin command nor prohibited
  by SPEC-DST-029, which makes inline manual guidance optional.
- Retain current main by ordinary merge, keep the accepted README byte-for-byte,
  and retain the new checks and completion/verification records under this scope.
- Add this work order to PR #488's existing two-order declaration. Push ordinary
  commits to mmzen/se_harness, recovery/wo-kis-010, under the existing request.

## Out of scope

No product runtime, installed policy, CI configuration, settings, dependency,
version, approved requirement or specification changes. No implementation of
WO-KIS-011/012/013, reapproval of their scope, historical VREC/RLS rewrite,
force push, merge to main, release, publication or independent-review claim.

## Decision envelope and simplicity

Use the existing subsection helper and command comparison. A narrow additional
work order admits the original package without widening or rewriting completed
orders. No new requirement, specification, artifact type or checker exception
is needed. Local verification and ordinary commits follow recorded execution
approval; later acceptance of a new VREC remains the owner's decision.

## Checks and completion

Use VER-KIS-008. Inspect the actual full PR diff from current main, not a later
base that excludes the planning package. Retain failed CI output, focused tests,
Windows full-suite output, required repository checks and hosted CI results.
Complete only when applicable checks pass and preserved inputs still match.
Prepare the required ready record for the actual committed correction; previous
verified records retain their earlier candidate and unchanged evidence.

## Stop conditions and report

Stop for a changed approved README or historical formal record, failed required
check, additional outside-scope path, or further product behavior needed to fix
the PR. Report the exact issue and affected action. The completion report names
actual states, checks, candidate, retained limitations and one next decision.
