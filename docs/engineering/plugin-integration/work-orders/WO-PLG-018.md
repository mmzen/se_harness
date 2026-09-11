+++
id = "WO-PLG-018"
type = "work_order"
title = "Integrate the verified plugin workflow stack"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[assurance]
commit_bound_verification = "required"
rationale = "Integration creates a combined trusted tree and adds a preservation checker; later delivery relies on the exact assembled candidate. Existing component verification does not prove this combination."
decided_by = "engineering-owner"

[delegation]
class = "execution"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-007-evaluator.json",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-008-evaluator.json",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-009-evaluator.json",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-010-evaluator.json",
  "docs/engineering/plugin-integration/evidence/WO-PLG-010/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-012/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-017/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-007.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-008.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-009.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-010.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-010.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-011.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-012.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-017.md",
  "plugins/verity-plane/common/skills/change/",
  "plugins/verity-plane/common/skills/evidence/",
  "plugins/verity-plane/common/skills/harness-operator-brief/",
  "plugins/verity-plane/common/skills/harness-orient/",
  "tests/plugin_integration/change_skill/",
  "tests/plugin_integration/evidence-skill/",
  "tests/plugin_integration/retained-skills/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-018.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-018.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-018/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-011.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-011-evaluator.json",
  "tests/plugin_integration/stack-integration/",
  "docs/notes/plugin-stack-integration-2026-09-11.md",
]

[relations]
implements = ["REQ-PLG-017", "REQ-PLG-018", "REQ-PLG-019", "REQ-PLG-020", "REQ-PLG-021"]
specifications = ["SPEC-PLG-010", "SPEC-PLG-011", "SPEC-PLG-012"]
verification = ["VER-PLG-018"]
+++

# Work Order: Integrate the verified plugin workflow stack

## Lifecycle

Draft proposal only. The operator authorized preparation of this proposal on
2026-09-11, not work-order approval or start. VER-PLG-018 requires its own
assurance-owner approval. Approving this WO would delegate only start, completion
and single-WO VREC preparation through the existing execution class and gates.
Verification and external merge remain separate operator decisions.

## Objective

Deliver WO-PLG-010, WO-PLG-011, WO-PLG-012 and WO-PLG-017 together through one
bounded PR to main, preserving their verified implementation and decision history.

## In scope

Import the exact 3,177 paths in [plan.json](../evidence/WO-PLG-018/plan.json),
SHA-256 `68b59c5837e890396701e46f5e37cc391a3ebf91d9f71c736d27e50345155aaa`.
The plan pins base main, all five PR heads, expected modes/blobs and source owners.

Keep this packet's approved files on a branch from the pinned main baseline.
After authorized start, merge the pinned #446 head, then the pinned #444 head.
The former already contains #445, #448 and #449 history. Add only the integration
checker and its tests, new evidence, this WO's authorized lifecycle receipts and
the later VREC-PLG-011/sidecar. Carry existing records exactly as imported.

## Out of scope

Plugin behavior changes, rewriting source tests/evidence, managed policy or CI
changes, archive-limit increases, rebase/squash, version changes, release, native
host qualification, VREC008 supersession, original WO scope/state changes and
merging or closing GitHub PRs. Those external actions require separate authority.

## Authorized decision envelope

Choose the checker implementation and compact new evidence layout within the
declared integration-only paths. Existing component-prefix entries permit import
of the frozen manifest, not additional edits. Do not resolve conflicts by choosing
new content; a conflict or different source/base requires a reviewed amendment.

## Constraints

- Preserve the approved manifest digest, original commits and VREC candidate ancestry.
- Original WOs remain implemented; VREC007/009/010 remain verified; VREC008 remains ready.
- Old record bodies, lifecycle events, sidecars and evidence are unchanged. Inspect
  evidence at its bound commit, preserving documented later receipt refreshes.
- No broad domain, plugins or tests directory permission is granted.
- Keep the final Git archive at or below 10,000 entries. The source preview has
  9,955 before this packet and new evidence; count the final governance tree too.
- A CI result must name its tested head/merge commit and actual base. Never relabel
  old component success or a local fork-point comparison as final hosted success.
- Record VREC011 only after a clean committed candidate exists. Check ID availability
  again before capture; a collision requires an amended planned path.

## Expected change surface

The frozen imports contain 3,171 additions and six modifications relative to
main c0451b7694b02f140f95661b07907d4722b336cd. Only this packet, the integration
checker, its tests and new integration evidence may add content beyond that import.
Proposal delivery itself contains no imported implementation changes.

## Required verification

Execute VER-PLG-018. Reuse unchanged component evidence under VER-PLG-010/011/012,
then prove the combined candidate through independent byte/ancestry checks and
the existing repository and hosted Windows/Linux lanes. Required assurance binds
this integration candidate; it does not rebind or replace existing VRECs.

## Evidence to record

Retain the approved plan, a compact report and raw-results archive/index, source
and candidate identities, exact checks, failures, archive counts and lifecycle
receipts under evidence/WO-PLG-018/. Preserve enough entry budget for the later
VREC, sidecar and final operator decision. Do not repack prior evidence.

## Stop and escalate conditions

Stop affected integration on changed inputs, conflict, undeclared effect, payload
or record mismatch, missing ancestor, invalid graph/integrity, missing authority,
failed required check, stale CI/base identity, evidence loss or archive overflow.
Approval of this plan cannot waive those conditions.

## Completion report format

Report imported work, the exact candidate and plan, preservation results,
Windows/Linux and hosted outcomes, final archive count, remaining limitations,
unchanged records and exactly one next accountable decision from harnessctl.
