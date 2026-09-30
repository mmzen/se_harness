+++
id = "WO-IAR-037"
type = "work_order"
title = "Create missing domain parents after minimal installation"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification in VREC-IAR-020 by approving the reviewed WO-IAR-037 proposal. Formal artifact creation relies on the safe authoring path and its regression checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/artifact_layout.py",
  "tests/test_resources.py",
  "tests/test_managed_template_texts.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-037.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-037/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T19:14:21Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve. This answers the explicit WO-IAR-037 and required verification question. Approval answers the reviewed proposal including required commit-bound verification in VREC-IAR-020. Reviewed draft SHA256 cc5d39fc7371afefaec8b6b27ad29ae4f812a1664a882c8967161ea37639a625; only confirmed assurance metadata was added before preview."
scope_paths = ["se_harness/artifact_layout.py", "tests/test_resources.py", "tests/test_managed_template_texts.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-037.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-037/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T19:14:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Create missing domain parents after minimal installation

## Objective and observed defect

Make the existing scaffold-domain command usable immediately after the approved
two-file installation. The command currently attempts to create the domain
directory before docs/engineering exists. The focused run
install036-focused-02.json retains the failure in DraftedWorkOrderTests.
The implementation file is outside the active work orders' approved paths.

## Bounded correction

In se_harness/artifact_layout.py, include missing ancestor directories in the
scaffold preview and create them in order during apply. Reuse the existing path
validation, mutation authority, atomic index writer and rollback list. Create
only the requested domain and its required parents. Do not create directories
during init, read-only commands or dry-run. Preserve existing owner files.

Add boundary checks in tests/test_resources.py for the two-file starting point,
preview without writes, successful creation, repeat without changes, parent
conflicts or links, and rollback that removes only newly created empty paths.
Keep the existing installed-template guidance assertions in
tests/test_managed_template_texts.py; the observed failing scenario must pass
without pre-creating its missing parents in the test.

## Constraints and exclusions

Use the existing authoring code. No new framework, command or installation
profile is needed. Preserve legacy behavior, invalid-input refusals and resource
identity checks. Do not change lifecycle rules, gates, accepted definitions,
installed repository instructions, CI workflows, releases or credentials.
Return additional scope or a changed requirement for review.

## Proposed assurance

Required commit-bound verification, included in VREC-IAR-020 with VER-IAR-022
and WO-IAR-030/034/035/036. The authoring path creates formal records that later
decisions rely on. Human confirmation is pending; no assurance decider is set.

## Authorized decision envelope

After approval, implement the bounded correction, run its checks, retain evidence,
make local commits, record completion and prepare the combined verification
record. This draft grants no implementation authority. Human verification and
external publication remain separate decisions.

## Verification and evidence

Run the resource and template-drafting regressions, the existing authoring suite,
the full suite on stable inputs, and distribution validation. Exercise fresh
domain creation through the actual installed candidate wheel outside the checkout
on Windows and Linux. Verify preview paths and unchanged owner bytes. Retain
actual failures, subsequent results and candidate identities under the declared
evidence prefix. Native host coverage and the released CI verifier compatibility
dependency remain distinct integrated qualification items; do not claim they
pass from a unit fixture or this correction.

## Stop and completion

Stop affected work for a changed approved contract, out-of-scope path, missing
authority or required check failure. Report the exact changed behavior, checks,
retained evidence, remaining limitations and evaluator's current typed next step.
Prepare VREC-IAR-020 only through released capture after its required inputs pass.
