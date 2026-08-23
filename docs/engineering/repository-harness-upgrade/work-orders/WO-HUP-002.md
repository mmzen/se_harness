+++
id = "WO-HUP-002"
type = "work_order"
title = "Upgrade the standard root governor to released 0.6.0"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[assurance]
commit_bound_verification = "required"
rationale = "Every later engineering, assurance, mutation, and release decision will rely on the exact schema-3 governor, managed policy, evaluator identity, and role separation established by this root transition."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".github/workflows/engineering-harness.yml",
  "AGENTS.md",
  "CLAUDE.md",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/QUALITY_GATES.json",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/TRACEABILITY.md",
  "docs/engineering/WORKFLOW.json",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/capabilities/CAP-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-verification.md",
  "docs/engineering/repository-harness-upgrade/intent/INT-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-004.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-005.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-006.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-002.md",
  "docs/engineering/templates/RELEASE_RECORD.template.md",
  "docs/engineering/templates/VERIFICATION_RECORD.template.md",
  "docs/engineering/templates/WORK_ORDER.template.md",
  "scripts/generate_harness_dashboard.py",
  "scripts/harness_explorer/index.template.html",
  "scripts/inspect_engineering_artifacts.py",
  "scripts/validate_engineering_artifacts.py",
]

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af"
target_version = "0.6.0"
target_payload_sha256 = "c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42"
target_archive_name = "se_harness-0.6.0-py3-none-any.whl"
target_archive_sha256 = "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"
publication = "immutable"
authorized_by = "repository-owner"

[relations]
implements = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
specifications = ["SPEC-HUP-002"]
architecture = ["ARCH-HUP-002"]
verification = ["VER-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:31:53Z"
decided_by = "repository-owner"
reason = "Approved the complete HUP-002 definition chain, no-significant-decision assessment, exact 18-change managed plan, and bound standard-root-only 0.6.0 implementation."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T07:38:07Z"
decided_by = "engineering-owner"
reason = "The four-owner deadlock declaration is recorded, target validation passes, and the mandatory no-network recovery rehearsal restored every standard control and external-action invariant."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-23T08:24:17Z"
decided_by = "engineering-owner"
reason = "Exact 0.6.0 transaction and evidence pass; separately approved WO-HUP-003 resolves the only suite stop, and the final 452-test suite plus all released-governor and scope gates pass."
+++

# Work Order: Upgrade the standard root governor to released 0.6.0

## Lifecycle

On 2026-08-23 the accountable owner explicitly approved `INT-HUP-002`, `CAP-HUP-002`, `REQ-HUP-004` through `REQ-HUP-006`, `SPEC-HUP-002`, `ARCH-HUP-002` including its `no_significant_decision` assessment, `VER-HUP-002`, this work order, the exact 18-change managed plan, and the bound standard-root-only upgrade to 0.6.0. This approval authorizes start preflight, transition to `in_progress`, exact plan recheck, transactional apply, local verification, evidence retention, and transition to `implemented` when the authorized work passes. It does not authorize a candidate commit, VREC, push, pull request, merge, release, publication, deployment, or other external action.

## Deadlock declaration

On 2026-08-23 the exact external public 0.5.0 evaluator passed isolated runtime identity but its full-root start preflight stopped solely on the already documented predecessor-boundary set: one `A-E009` for rejected `RLS-SEH-009` and two `A-E010` duplicate-0.6.0 findings for `RLS-SEH-009` and `RLS-SEH-012`. The released 0.6.0 evaluator validated the complete 681-artifact graph with zero errors and reproduced the exact approved 18-change plan.

At `2026-08-23T07:36:50Z`, the repository owner, release owner, security owner, and engineering owner declared that normal 0.5.0 full-root preflight path deadlocked at baseline commit `cccbaa70a6c5a33e19decec0d78f26afd87d5f9e`. They authorized, for this HUP-002 implementation only, the mandatory bounded no-network recovery rehearsal followed by the exact immutable 0.6.0 standard-root transaction. Product changes, commits, VRECs, pushes, pull requests, merges, tags, releases, publication, deployment, credentials, issue changes, and history rewriting remain prohibited.

This declaration accepts no additional predecessor diagnostic and waives no target check. Failed rehearsal, changed plan membership, target validation error, credential signal, or any identity/scope mismatch remains a stop condition.

The mandatory no-network rehearsal then passed with candidate contamination and stale identity rejected, conflicting chains stopped for accountable disposition, exact interrupted-transaction rollback, every normal control restored, absence invariants true, and all credential/network/publication/release/tag/deployment flags false. With those prerequisites complete, the engineering owner moved this work order to `in_progress` for the immediate identity/plan recheck and bounded transaction.

## Objective

Use the independently acquired immutable public 0.6.0 evaluator to upgrade the repository's installed standard root from released 0.5.0/schema 2 to released 0.6.0/schema 3, retain complete transition evidence, and produce one minimal reviewable candidate without changing product, release, publication, or external state.

## In scope

- Verify public 0.6.0 archive, installed payload, runtime origins, entry point, isolation, and checkout exclusion.
- Validate this complete draft packet with released 0.6.0 semantics and obtain accountable approval.
- Retain the exact current-0.5.0 preflight deadlock transcript and complete the mandatory no-network recovery rehearsal.
- Recheck the exact external 0.6.0 read-only upgrade plan immediately before apply.
- Apply the reviewed standard-root transition only through the exact target evaluator, this work order, and `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json`.
- Reconcile the managed root and schema-3 lock, preserve owner bytes, and prove no-op replay.
- Run `VER-HUP-002`, retain `WO-HUP-002-verification.md`, and transition only this work order to `implemented` after all authorized work and local checks complete.

## Exact reviewed managed plan

The public 0.6.0 dry run reports 36 managed paths: 18 unchanged and these 18 additions or updates:

1. `.engineering-harness.toml` — update.
2. `.github/workflows/engineering-harness.yml` — update.
3. `AGENTS.md` managed marker block — update; owner content must remain byte-identical.
4. `CLAUDE.md` managed marker block — update; owner content must remain byte-identical.
5. `ENGINEERING_HARNESS.md` — update.
6. `docs/engineering/DECISION_RIGHTS.md` — update.
7. `docs/engineering/QUALITY_GATES.json` — add.
8. `docs/engineering/QUALITY_GATES.md` — update.
9. `docs/engineering/TRACEABILITY.md` — update.
10. `docs/engineering/WORKFLOW.json` — add.
11. `docs/engineering/WORKFLOW.md` — update.
12. `docs/engineering/templates/RELEASE_RECORD.template.md` — update.
13. `docs/engineering/templates/VERIFICATION_RECORD.template.md` — update.
14. `docs/engineering/templates/WORK_ORDER.template.md` — update.
15. `scripts/generate_harness_dashboard.py` — update.
16. `scripts/harness_explorer/index.template.html` — update.
17. `scripts/inspect_engineering_artifacts.py` — update.
18. `scripts/validate_engineering_artifacts.py` — update.

The transaction may additionally replace `.engineering-harness.lock` with the exact schema-3 result and exclusively create `WO-HUP-002-evaluator-upgrade.json`. It must remove the obsolete lock entry for `docs/engineering/REPOSITORY_CONTEXT.md` without writing, moving, or deleting that owner file. Any other installer action or repository change stops for an amendment.

## Out of scope

Any `se_harness/` or canonical `templates/repository/standard/` product change, package/version/build change, formal-history rewrite, release-record change, repository-tool change, publisher or Pages change, issue action, candidate commit, VREC preparation or transition, push, pull request, merge, tag, GitHub Release, PyPI publication, deployment, protected-environment decision, force push, or external-state mutation.

## Authorized decision envelope

After explicit approval, implementation may choose disposable external directory names, normalized evidence presentation, and ordering of independent checks. It may not choose a different evaluator, accept expanded plan membership, hand-edit partial managed state, delete retired owner content, alter product/release scope, waive a gate, or exercise accountable/external authority.

## Constraints

- Current public 0.5.0 and lock SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af` remain authoritative until apply.
- The applying runtime must match version 0.6.0, payload SHA-256 `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`, archive `se_harness-0.6.0-py3-none-any.whl`, and archive SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- The immediate pre-apply plan must match the exact 18 changes above and report 18 unchanged managed paths.
- Existing owner content and every unrelated path must remain unchanged.
- No checkout source, editable install, or candidate wheel may execute as the released evaluator.

## Expected change surface

- The nine new HUP-002 definition artifacts and the repository-harness-upgrade domain index update prepared before approval.
- After approval, exactly the 18 managed additions/updates listed above, installer-owned schema-3 lock replacement, keyed evaluator-upgrade JSON, implementation evidence, and this work order's accountable lifecycle updates.
- No other path without an amended approved work order.

## Required verification

- `VER-HUP-002` exact released-evaluator identity and digest reconciliation.
- Exact current-0.5.0 preflight boundary output, four-owner deadlock declaration, passing no-network recovery rehearsal, and complete released-0.6.0 graph validation.
- Plan/apply equivalence, transaction evidence, lock integrity, owner-byte preservation, no-op replay, and changed-surface proof.
- Released 0.6.0 doctor, validate, inspect, dashboard, release-distribution validation, CLI help, complete unit suite, workflow parsing, and diff checks.
- Candidate-source and candidate-package separation checks; hosted checks remain pending until separately authorized commit/push work.

## Evidence to record

Retain canonical evaluator-upgrade JSON and `WO-HUP-002-verification.md` with baseline/target identities, public wheel and payload hashes, normalized runtime origins, exact plan and apply outcomes, pre/post managed and owner hashes, lock schema/evaluator/files, changed paths, graph planes, tests, workflow checks, rollback observation, deviations, residual risks, and every unperformed lifecycle or external action.

## Stop and escalate conditions

Stop on missing approval; wrong lock, version, payload, archive, origin, isolation, or entry point; any current-governor preflight diagnostic outside the exact declared `A-E009`/`A-E010` set; failed rehearsal; target graph error; plan expansion; customized or ambiguous predecessor; owner-byte change; partial transaction; failing postcondition or required check; product/release/external mutation; unexplained warning; or need for commit, VREC, push, PR, merge, release, publication, deployment, issue action, force push, or history rewrite without separate authority.

## Completion report format

Report work-order state; evaluator identity; exact changed surfaces; owner-content hashes; schema-3 lock and evidence identities; plan/apply/replay results; graph planes; test counts; hosted checks not performed; warnings, deviations, and residual risks; and every unperformed candidate-commit, VREC, PR, merge, release, publication, deployment, and external action.
