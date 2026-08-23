+++
id = "WO-HUP-003"
type = "work_order"
title = "Reconcile self-hosting checks after 0.6.0 root adoption"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[assurance]
commit_bound_verification = "required"
rationale = "Repository owner guidance and the complete source suite are trusted inputs to later engineering and assurance decisions."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "AGENTS.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003-verification.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-007.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-003.md",
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_dashboard_webui.py",
  "tests/test_instruction_architecture.py",
  "tests/test_predecessor_assessment_contract.py",
  "tests/test_revision_provenance.py",
  "tests/test_validation_taxonomy.py",
]

[relations]
implements = ["REQ-HUP-007"]
specifications = ["SPEC-HUP-003"]
verification = ["VER-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T08:06:31Z"
decided_by = "repository-owner"
reason = "Approved REQ-HUP-007, SPEC-HUP-003, VER-HUP-003, WO-HUP-003, and its exact eight-path post-adoption compatibility plan for implementation."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T08:07:32Z"
decided_by = "engineering-owner"
reason = "Approved exact eight-path plan and passing released-0.6.0 start preflight authorize bounded implementation."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-23T08:23:58Z"
decided_by = "engineering-owner"
reason = "Exact eight-path compatibility implementation, keyed evidence, focused tests, affected modules, two complete-suite runs, released-governor gates, and 43-path scope audit all pass."
+++

# Work Order: Reconcile self-hosting checks after 0.6.0 root adoption

## Lifecycle

At `2026-08-23T08:06:31Z`, the accountable repository owner approved
`REQ-HUP-007`, `SPEC-HUP-003`, `VER-HUP-003`, this work order, and its exact
eight-path compatibility plan for implementation. The approval authorizes
start preflight, transition to `in_progress`, the eight listed implementation
edits, local verification, evidence retention, and transition to `implemented`
when every required check passes. It authorizes no additional path, commit,
VREC, push, pull request, merge, tag, release, publication, deployment,
credential use, issue mutation, or history rewrite.

## Objective

Resolve only the ten required-suite failures caused by legitimate adoption of
the released 0.6.0 root, while preserving the exact HUP-002 transaction and all
role, evidence, integrity, negative-test, release, and external-action controls.

## Exact reviewed implementation plan

1. Update the `AGENTS.md` owner region for released 0.6.0, schema-3 JSON paths,
   and post-adoption equality; do not change its managed marker block.
2. Update artifact-catalog tests to validate exact adopted-policy equality and
   source-path independence.
3. Reconcile the retired-context permitted-mention inventory with the exact
   HUP-002 records and withdrawn managed-router mention.
4. Update the dashboard installed-target assertion from 524,288 to 2,097,152
   bytes and require equality with the packaged target.
5. Update owner-region expectations from 0.5.0 to 0.6.0 while preserving all
   owner facts, fragment integrity, path coverage, and the 6,000-byte limit.
6. Compare the installed engineering workflow to the packaged 0.6.0 workflow,
   leaving the historical predecessor-assessment workflow unchanged.
7. Add canonical evaluator evidence and a matching schema-3 lock only to
   revision-provenance temporary fixtures.
8. Replace the validation-taxonomy byte-inequality assertion with exact current
   equality while retaining every vocabulary and diagnostic-plane assertion.

No other implementation path or test assertion may change without an amended
and reapproved work order.

## In scope

- The exact eight implementation paths above.
- This HUP-003 definition packet, domain-index entry, keyed evidence, and
  lifecycle updates.
- Focused, module, complete-suite, released-governor, scope, security, and diff
  verification.

## Out of scope

Any `se_harness/` or `templates/repository/standard/` change, managed root or
lock change, package/version/build change, release or verification record,
repository release tool, publisher or Pages change, credential use, external
action, candidate commit, VREC, push, pull request, merge, tag, release,
publication, deployment, issue mutation, force push, or history rewrite.

## Authorized decision envelope

After explicit approval, implementation may choose helper constant names and
assertion presentation within the exact behaviors in `SPEC-HUP-003`. It may not
weaken a negative assertion, add a legacy production exemption, change product
runtime or package templates, change managed bytes, or expand the path list.

## Required verification

- `VER-HUP-003` exact focused, module, and complete-suite checks.
- Released 0.6.0 identity, no-op replay, doctor, graph validation, review
  preflight, inspection, dashboard, and release-distribution validation.
- Owner-region size and fragment-digest checks, retired-context byte and lock
  checks, exact path audit, evidence scan, and `git diff --check`.

## Stop and escalate conditions

Stop on any non-HUP-003 changed path, managed-root drift, new test failure,
negative-test relaxation, governor origin mismatch, fragment-integrity change,
fixture leakage into production, graph error, credential signal, external
action, or need for a commit/VREC/push/PR/merge/release/publication/deployment
without separate authority.

## Completion report

Report exact changed paths, focused/module/full test counts, owner and managed
hashes, governor and graph results, warnings, deviations, residual risks, and
all unperformed external and lifecycle actions.
