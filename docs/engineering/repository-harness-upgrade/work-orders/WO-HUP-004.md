+++
id = "WO-HUP-004"
type = "work_order"
title = "Replace version-specific predecessor CI with portable governor succession"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[assurance]
commit_bound_verification = "required"
rationale = "Future CI, assurance, integration, and governor upgrades will trust the base/target resolver, evaluator identity boundary, workflow routing, and cross-platform role assertions changed by this work."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".github/workflows/predecessor-evaluator-assessment.yml",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/architecture/adr/ADR-HUP-001.md",
  "docs/engineering/repository-harness-upgrade/capabilities/CAP-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-004-verification.md",
  "docs/engineering/repository-harness-upgrade/intent/INT-HUP-003.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-008.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-009.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-004.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-004.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-004.md",
  "scripts/validate_governor_transition.py",
  "tests/test_governor_transition.py",
  "tests/test_inspection.py",
  "tests/test_predecessor_assessment_contract.py",
]

[relations]
implements = ["REQ-HUP-008", "REQ-HUP-009"]
specifications = ["SPEC-HUP-004"]
architecture = ["ARCH-HUP-003", "ADR-HUP-001"]
verification = ["VER-HUP-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "repository-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T20:23:09Z"
decided_by = "engineering-owner"
+++

# Work Order: Replace version-specific predecessor CI with portable governor succession

## Lifecycle

The corrective packet is approved and this work order is `in_progress`.
Implementation and local qualification are authorized; completion,
commit-bound verification, commit, push, and hosted execution remain separate
governed actions.

## Objective

Correct the two hosted failures on PR 122 through one future-proof transition
assessment and one portable evaluator-role assertion, without changing the
0.6.0 root transaction or restoring a permanent compatibility view.

## In scope

- Add one repository-owned, read-only transition resolver implementing
  `SPEC-HUP-004`.
- Convert the existing predecessor-assessment workflow in place to generic
  governor-transition routing with no concrete version constants.
- Replace the remaining raw-byte inequality assertion in
  `tests/test_inspection.py`.
- Update the workflow contract test and add exhaustive resolver tests.
- Retain exact local and hosted evidence under the keyed HUP path.

## Out of scope

`se_harness/`, candidate templates, managed root files, root configuration or
lock, product/package version, release/VREC/RLS/REL mutation, publication and
Pages workflows, branch protection, external policy, credentials, tag,
publication, deployment, maintenance, merge, or history rewrite. Disposition
of `VREC-HUP-003` is separate assurance-owner work.

## Authorized decision envelope

After explicit approval and start, implementation may choose private helper
names, bounded JSON field presentation, and fixture organization inside the
exact paths above. It may not weaken identity/evidence predicates, add a
version constant, alter managed/current-governor CI, construct a compatibility
view, change a lifecycle record other than this work order, or add a path.

## Constraints

- Preserve current root lock and every managed digest.
- Use only full commit identities and canonical hash modes.
- Treat event metadata, target repository content, paths, archives, environment,
  and subprocess output as untrusted.
- Never expose persistent Git credentials to the workflow.
- Keep the existing workflow file until branch/check policy has been separately
  reviewed; no external-policy change is authorized.

## Expected change surface

Exactly the 16 paths in `[execution_scope]`. The evidence path and two new
resolver paths may be created; all others already exist. No prefix or inferred
adjacent file is admitted.

## Required verification

Execute every `VER-HUP-004` positive and negative case, both complete local
runtime suites, exact public 0.6.0 gates, release-distribution validation,
exact-scope and protected-surface comparisons, and hosted push/PR lanes.

## Evidence to record

- Base/target and work-order/evidence fixture matrix.
- Exact evaluator archive, payload, and origin output.
- LF/CRLF assertion results.
- Python 3.11 and default-runtime complete-suite summaries.
- Exact public doctor/validate/inspect/dashboard results.
- Changed-path, checkout-clean, secret/path, and diff checks.
- Hosted run IDs and exact candidate SHA.

## Stop and escalate conditions

Stop on ambiguous base, any hard-coded governor, unavailable or mismatched
identity, candidate-source evaluator execution, compatibility-view need,
checkout mutation, credential signal, unexpected path, root/managed/product/
release change, failed negative case, or any lifecycle/external action not
separately authorized.

## Completion report format

Report exact changed paths, resolved routing for each event case, all identity
and evidence bindings, focused/full/hosted results, warnings and deviations,
candidate identity, and every intentionally unperformed lifecycle or external
action.
