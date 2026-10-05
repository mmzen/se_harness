+++
id = "WO-HAG-006"
type = "work_order"
title = "Unblock reconciliation checks without changing the PR base"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because later CI, reconciliation and delivery depend on the trust selection and preserved evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  "scripts/validate_governor_transition.py",
  "tests/test_governor_transition.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/hosted-artifact-graph/README.md",
  "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-006.md",
  "docs/engineering/hosted-artifact-graph/verification/VER-HAG-005.md",
  "docs/engineering/hosted-artifact-graph/verification/VER-HAG-004.md",
  "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-006.md",
  "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-003.md",
  "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/WO-HAG-001-handoff.md",
  "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-006/"
]

[relations]
implements = ["REQ-HUP-008", "REQ-HAG-008"]
specifications = ["SPEC-HAG-006", "SPEC-HUP-004", "SPEC-HAG-003"]
architecture = ["ARCH-HUP-003", "ADR-HUP-001", "ARCH-HAG-001", "ADR-HAG-001"]
verification = ["VER-HAG-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T13:25:58Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to SPEC-HAG-006, VER-HAG-005 and WO-HAG-006, required commit-bound verification, DEC-HAG-003 bounded-manual-revision of the exact VER-HAG-004 proposal, and ordinary draft PR #535 updates in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs. Review binding SHA-256 c9d4d84326b0e26d39519a1eadb91e216e4a6f01700213ec3c76a6854e55a649. This covers local implementation, checks, aggregate ready-record publication and later separately given verification-decision push. No verification acceptance, risk acceptance, retargeting, base-branch update, force push, merge, release or deployment. The exact manual amendment grants no general revision mechanism or gate waiver."
scope_paths = ["scripts/validate_governor_transition.py", "tests/test_governor_transition.py", "docs/notes/developing-se-harness.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-006.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-005.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-004.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-006.md", "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-003.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/WO-HAG-001-handoff.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-006/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-05T13:26:47Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Unblock reconciliation checks without changing the PR base

## Objective

Make the approved reconciliation assessable against PR #535's original base,
with independent proof of the adoption already integrated on main and preserved
historical evidence. WO-HAG-005 remains in_progress until these checks pass.

## In scope

- Implement only SPEC-HAG-006's bounded additional history comparison in the
  existing CI assessor, with meaningful tests and the matching operator note.
- Preserve WO-HAG-001's current handoff bytes before the released command
  rebinds the live packet. Keep every earlier VREC and its bound evidence exact.
- Apply only the separately authorized, digest-bound VER-HAG-004 amendment
  reviewed under DEC-HAG-003. Do not invent a lifecycle or revision command.
- Run VER-HAG-005, retain all failures, and prepare aggregate commit-bound
  verification with the completed WO-HAG-005 reconciliation.

## Expected change surface

| Path | Reason |
| --- | --- |
| scripts/validate_governor_transition.py | Reuse adoption proved in independent default-branch history while retaining the original event base. |
| tests/test_governor_transition.py | Synthetic-history positive cases and distinct trust/identity refusals. |
| docs/notes/developing-se-harness.md | Explain this CI route and correct the now-stale hosted 0.22.0 pin sentence. |
| HAG README | Current findings and evidence links only. |
| SPEC-HAG-006, VER-HAG-005, WO-HAG-006, DEC-HAG-003 | This bounded package and its actual decisions. |
| verification/VER-HAG-004.md | Exact separately approved linked amendment allowing one live handoff to be rebound after preserving its predecessor bytes. |
| evidence/WO-HAG-001/WO-HAG-001-handoff.md | Supported current-snapshot rebind; no manual evaluator-header edit or invented test observation. |
| evidence/WO-HAG-006/ | Prior packet and definition bytes, binding, commands, failures, tests, review and lifecycle evidence. |

The workflow already fetches the default branch and passes it to the assessor;
no workflow edit is planned. No dependency, package metadata, portable evaluator,
service code or plugin change is needed. Existing architecture responsibilities
remain; the specification makes the additional immutable history input explicit.
Generated VREC and evaluator-evidence paths are selected by capture and must be
checked under automatic relationship admission; no whole parent directory grant.

## Out of scope

No retargeting or update of codex/hosted-artifact-graph-inputs, no changing the
original scope baseline, no weakened gate, release, adoption version change,
hosted implementation, risk acceptance, deployment, force push or merge.
Historical VREC-HAG-001/002 candidates and evidence remain immutable.

## Proposed authority and assurance

Propose required commit-bound verification because CI will rely on a new
trusted-history selection. Human classification is pending; do not supply an
assurance decided_by identity until the human confirms it.

Approval would permit the named implementation, checks, local commits and
aggregate verification preparation under VER-HAG-004/005. It must explicitly
include SPEC-HAG-006's prospective CI addendum and DEC-HAG-003's exact bounded
manual amendment, not a general accepted-artifact editing capability.

Also propose ordinary review pushes and updates to draft PR #535 in
mmzen/se_harness, source codex/hosted-artifact-phase1, target
codex/hosted-artifact-graph-inputs. Include these reviewed drafts, ready record,
evidence and later separately given verification-decision push. Keep the PR
draft while WO-HAG-001 is unfinished. Existing publication authority is reused
for unchanged WO-HAG-005 scope; this request adds only this correction package.
Human verification, merge, release and deployment remain separate.

## Checks and evidence

Execute VER-HAG-005 and the amended VER-HAG-004. Keep original B, integrated M,
tested/captured commits, complete path lists, released evaluator identity,
actual exits, skips and limits. Full PR coverage uses all five selected WOs
against B, even when CI finds an independent adoption-history anchor.

## Stop conditions and completion

Stop for changed reviewed amendment bytes, ambiguous or candidate-only trust,
uncovered paths, changes to older VREC bindings, another packet requiring
unapproved rewriting, or a required failed check. Report actual scope and next
evaluator step. Completion and ready capture never imply human verification.
