+++
id = "WO-IAR-024"
type = "work_order"
title = "Complete the consumer corrections for guide retirement"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Human-approved commit-bound assurance for the consumer corrections and retirement checks used by subsequent adoption and release decisions."
decided_by = "mmzen"

[execution_scope]
paths = [
  "plugins/verity-plane/common/skills/evidence/references/records.md",
  "tests/test_workflow_execution.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_retired_surface.py",
  "tests/test_progressive_instruction_discovery.py",
  "tests/fixtures/progressive-discovery/released-0.19.0/",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-024.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-024/",
]

[relations]
implements = ["REQ-IAR-027", "REQ-IAR-028"]
specifications = ["SPEC-IAR-014", "SPEC-IAR-015"]
verification = ["VER-IAR-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T08:45:48Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", in response to the request to approve WO-IAR-024 and required commit-bound verification, with existing 0.19.0 engineering-owner encoding. Reviewed draft SHA-256 dc3524d84f1fc3894800b5838a0511e25afce57a7a70e02a7ebfa4dec1891d5e. The only pre-transition edits record the supplied assurance decision. Approval input SHA-256 50926b20a944c367aedc6a0bdccfc6b4e013782b824e0ccc70a95a2af8036d21. Codex applies that human decision."
scope_paths = ["plugins/verity-plane/common/skills/evidence/references/records.md", "tests/test_workflow_execution.py", "tests/test_standard_repository_lifecycle.py", "tests/test_retired_surface.py", "tests/test_progressive_instruction_discovery.py", "tests/fixtures/progressive-discovery/released-0.19.0/", "docs/engineering/instruction-architecture/work-orders/WO-IAR-024.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-024/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T08:46:22Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the unchanged approved scope under mmzen's recorded approval after passing start checks."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-28T09:18:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex completed the unchanged approved scope. VER-IAR-017 evidence, full Windows/Linux suites, installed-package checks and combined complete-change handoff pass. Human commit-bound verification remains pending."
+++

# Complete the consumer corrections for guide retirement

## Objective

Remove the remaining current plugin dependency on DECISION_RIGHTS.md and
update the additional tests that require retired source templates. This is a
bounded companion to WO-IAR-022 under the existing product-wide decision.
It does not change the accepted retirement behavior.

## Observed need

At source commit d0e94b1cc50be9972aec85d5f64064b3361aeb06, the evidence skill's
references/records.md, line 51, unconditionally requests DECISION_RIGHTS.md.
The operating-card and workflow tests in test_workflow_execution.py read
current source templates that WO-IAR-022 will delete. The policy-customization
test in test_standard_repository_lifecycle.py expects a fresh installation to
create TECHNICAL_COMMUNICATION.md. The obsolete-command guard in
test_retired_surface.py reads the WORKFLOW.md source template.

These four files are outside WO-IAR-022's approved paths. The plugin reference
is also outside completed WO-IAR-021. Its omission was found during the
retirement consumer inventory after VREC-IAR-013 was verified. That verified
record and its candidate remain unchanged; it does not verify this correction.
These findings come from source inspection, not a claimed failed test run.

WO-IAR-022 explicitly stops on an uncovered active consumer. Keep its six
templates until this reference is corrected under an approved work order.
Historical references and version-conditioned fallbacks do not require removal.

## In scope and exact change surface

| File or bounded directory | Required correction |
| --- | --- |
| plugins/verity-plane/common/skills/evidence/references/records.md | Route the current collection to docs/engineering/harness/AUTHORITY.md#authority-from-work-approval. Retain DECISION_RIGHTS.md only for older releases whose installed root selects it. Preserve preparation checks, human decision rights and external-action limits. |
| tests/test_progressive_instruction_discovery.py | Check the evidence reference's current authority route against an installed collection without the six pointers. Include a broken current-route negative control. Keep the legacy fallback explicit rather than banning historical filenames. |
| tests/test_workflow_execution.py | Keep the legacy operating-card renderer's content, size and malformed-contract checks. Remove equality with a deleted current template. Assert a fresh install does not create or track the card. Check current workflow command wording in CONTINUE.md; retain machine procedure and removed-command checks. |
| tests/test_standard_repository_lifecycle.py | Replace the fresh obsolete-guide assumption with an upgrade fixture containing a released 0.19.0 pointer plus owner customization. Assert exact byte preservation, leaving-seed lock reconciliation, passing readiness and consistent retry under SPEC-IAR-015. Preserve the separate supported 0.18.0 customization-refusal coverage. |
| tests/test_retired_surface.py | Move the obsolete workflow-command and verbatim-report guards to their current instruction owners, CONTINUE.md and RESULTS.md. Preserve all prohibited phrases and the checks on the current CLI reference. |
| tests/fixtures/progressive-discovery/released-0.19.0/ | Retain only the six released pointer files and their provenance. Extract them from the independently retained public 0.19.0 wheel, record its SHA-256 and exact member digests, and account explicitly for Git newline conversion. Do not derive expected bytes from the candidate renderer. |

Proposed replacement for the unconditional opening of the preparation paragraph:

> For the current instruction collection, read
> `docs/engineering/harness/AUTHORITY.md#authority-from-work-approval` and use
> the actual workflow result for preparation. For an older release, follow
> the authority guide selected by its installed root; that guide may be
> `docs/engineering/DECISION_RIGHTS.md`.

Keep the following checks on every selected WO, reuse of existing preparation
authority and separation from verification, release and external authority.
No reference to an old guide becomes an unconditional fallback when the current
guide is missing: a missing current instruction remains a discovery failure.

The released wheel is se_harness-0.19.0-py3-none-any.whl, SHA-256
43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8.
The six fixture names are OPERATING_CARD.md, DECISION_RIGHTS.md, QUALITY_GATES.md,
WORKFLOW.md, TRACEABILITY.md and TECHNICAL_COMMUNICATION.md. Preserve the
existing released-0.18.0 fixtures and fingerprints.

## Dependencies and authorized decision envelope

Use the verified correction at a0435434bcfa9ce385931e2d0e64bf98cab300e1 and its
verified VREC-IAR-013. The verification decision was retained in governance
commit d0e94b1cc50be9972aec85d5f64064b3361aeb06.

After approval, implement the reference correction first. Confirm its current
route resolves without the six pointers in a disposable fixture. Then continue
WO-IAR-022 under its existing approval, and test both changes together at one
candidate. Test expectations that require retirement are assessed against that
combined candidate; they are not evidence that retirement already occurred.
Record separate actual states for both work orders.

The implementer may choose test helpers within these paths. No new package,
runtime service, CLI command, lifecycle gate or architecture is needed.
The existing requirements and verification contract apply unchanged.

## Out of scope and stops

No installed repository pointer deletion, machine-policy or decision-right
change, historical evidence rewrite, weakened preservation assertion, test skip,
real host adoption, release, push, PR mutation or merge. This work order does
not authorize product-source changes assigned to WO-IAR-022.

Stop the affected work if another active consumer needs a change outside the
combined approved path set, if expected predecessor bytes cannot be established,
or if passing a test requires weakening SPEC-IAR-015. Do not reopen completed
WO-IAR-021 or broaden WO-IAR-022's recorded approval.

## Required verification and retained evidence

Apply VER-IAR-017 to the combined WO-IAR-022/WO-IAR-024 candidate. Run the
affected test modules and the full repository suite on Windows and Linux,
distribution validation and CLI smoke checks. Retain real installed-wheel
and sdist results, supported predecessor upgrades, refusal and retry cases,
and the complete consumer disposition required by that contract.

Under evidence/WO-IAR-024/, retain the before/after reference and test changes,
fixture provenance, actual commands and runtimes, failures and final results,
review findings and complete changed paths. Shared retirement results may be
retained once under WO-IAR-022 and explicitly included in the same verification
record. Do not treat an evidence index as recursive capture.

Run the selected released evaluator's scope, start, handoff and completion
checks. Prepare one VREC for the exact clean combined candidate and explicitly
select both work orders and VER-IAR-017. Only the human may verify it.

## Assurance proposal and completion

The human repository owner mmzen confirmed **required** commit-bound assurance
with "I approve", in direct response to the request to approve WO-IAR-024 and
required verification, using the existing 0.19.0 engineering-owner encoding.
The correction changes instructions and tests on which later retirement and
release decisions depend.

If approved, local execution follows AUTHORITY.md#authority-from-work-approval.
The selected 0.19.0 evaluator still uses engineering-owner for WO approval;
retain the actual human identity and exact decision in its reason.

Report corrected consumers, preserved compatibility checks, actual test
results, remaining gaps, the exact candidate and the evaluator's next typed
step. Preparation of this draft does not start either work order.
