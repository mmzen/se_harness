+++
id = "WO-PLG-025"
type = "work_order"
title = "Complete repository cleanup and align onboarding checks"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[assurance]
commit_bound_verification = "required"
rationale = "The final candidate changes the skill-provider lock, public documentation contract and trusted onboarding checks used by future contributors and assurance decisions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".engineering-harness.delegation.toml",
  ".engineering-harness.lock",
  ".agents/skills/harness-operator-brief/SKILL.md",
  ".agents/skills/harness-operator-brief/scripts/check_brief.py",
  ".agents/skills/harness-operator-brief/skill-contract.json",
  ".agents/skills/harness-orient/SKILL.md",
  ".agents/skills/harness-orient/scripts/orient.py",
  ".agents/skills/harness-orient/skill-contract.json",
  ".claude/skills/harness-orient/SKILL.md",
  "AGENTS.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/README.md",
  "docs/notes/delegation-class.md",
  "docs/notes/agentic-execution-plugin-distribution.md",
  "docs/notes/codebase-kiss-work-orders-2026-09-13.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-024.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-024.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-024/",
  "README.md",
  "tests/test_public_onboarding.py",
  "docs/notes/technical-communication.md",
  "docs/notes/agentic-execution-phase4-skills.md",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-029.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-025.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-025.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-025/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-022.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-022-evaluator.json",
]

[relations]
implements = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-KIS-009", "REQ-DST-069"]
specifications = ["SPEC-PLG-021", "SPEC-KIS-003", "SPEC-DST-024", "SPEC-DST-029"]
architecture = ["ARCH-PLG-004", "ADR-PLG-004", "ARCH-KIS-002", "ADR-KIS-002"]
verification = ["VER-PLG-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T12:40:39Z"
decided_by = "engineering-owner"
reason = "The owner approved the reviewed replacement package with \"i approve\" on 2026-09-16, exercising the named engineering-owner decision for WO-PLG-025. Reviewed SHA-256 c1729a68823febb66a11162761f32eac83087d35b871a3780d624a9d400f66c5. This records the definition or execution-scope approval; it makes no assurance or external-delivery decision."
scope_paths = [".engineering-harness.delegation.toml", ".engineering-harness.lock", ".agents/skills/harness-operator-brief/SKILL.md", ".agents/skills/harness-operator-brief/scripts/check_brief.py", ".agents/skills/harness-operator-brief/skill-contract.json", ".agents/skills/harness-orient/SKILL.md", ".agents/skills/harness-orient/scripts/orient.py", ".agents/skills/harness-orient/skill-contract.json", ".claude/skills/harness-orient/SKILL.md", "AGENTS.md", "docs/notes/developing-se-harness.md", "docs/notes/README.md", "docs/notes/delegation-class.md", "docs/notes/agentic-execution-plugin-distribution.md", "docs/notes/codebase-kiss-work-orders-2026-09-13.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-024.md", "docs/engineering/plugin-integration/verification/VER-PLG-024.md", "docs/engineering/plugin-integration/evidence/WO-PLG-024/", "README.md", "tests/test_public_onboarding.py", "docs/notes/technical-communication.md", "docs/notes/agentic-execution-phase4-skills.md", "docs/engineering/harness-distribution/README.md", "docs/engineering/harness-distribution/specifications/SPEC-DST-029.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-025.md", "docs/engineering/plugin-integration/verification/VER-PLG-025.md", "docs/engineering/plugin-integration/evidence/WO-PLG-025/", "docs/engineering/plugin-integration/verification-records/VREC-PLG-022.md", "docs/engineering/plugin-integration/evidence/VREC-PLG-022-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-16T12:44:12Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start routine execution of the owner-approved replacement cleanup work order after passing start preflight."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-16T13:03:27Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed the approved cleanup and onboarding corrections. The full 1068-test suite passes with 15 skips; required integrity, graph, distribution, review and Git-derived handoff checks pass. Earlier failures and reuse comparisons are retained under the approved evidence scope."
+++

# Complete repository cleanup and align onboarding checks

## Objective and existing work

Finish the cleanup begun under WO-PLG-024 and resolve the onboarding failures
that prevented its completion. The comparison baseline remains
`f05c478a29c39f94968fdc842a34c861d30a42ac`. The complete diff from that baseline,
including the first work order and its evidence, belongs to this replacement
scope. No source or evaluator upgrade is part of this recovery.

Already applied locally: eight file removals, released plugin-ownership
migration, selected guidance edits, and the owner's exact two-link README
repair. The README SHA-256 is
`240bf535c917234225d19e0efe1b48521322eb6f6504c5b7a5619a9e866546dc`.
The full source run reported 1,068 tests, 12 failures and 15 skips. Ten failures
reproduce the earlier README/manual-setup mismatch; two depend on root skill
copies removed by the cleanup. Failed scope and preparation checks are retained
under the original evidence directory. None is a passing acceptance result.

## Replacement decision

The approval package proposes SPEC-DST-029 and VER-PLG-025 approval, approval
of this WO, and the engineering owner's explicit transition of WO-PLG-024
from `in_progress` to `rejected` with this reason:

> Remaining execution is replaced by WO-PLG-025 because the original scope
> omitted required README, test and documentation corrections. Preserve the
> already applied cleanup and all observations. This disposition closes the
> original work authorization; it neither marks that work complete nor rejects
> the released plugin-ownership behavior.

Use the released transition command to record that disposition. Do not edit
the original scope, approval event, start event or body. VER-PLG-024 remains
approved historical input, with no assertion that it passed. Draft creation
makes none of these decisions. Only WO-PLG-025 is selected for remaining
execution and the future VREC; do not manufacture completion of WO-PLG-024.

## In scope

1. Carry forward the eight authorized removals and schema-4 plugin provider.
   Compare against the baseline and retained before/after lock observations;
   preserve evaluator 0.18.0 and all unrelated lock entries. Do not replay
   migration or restore root skills just to make the old tests pass.
2. Preserve the exact repaired README identified above and the owner's deleted
   value-proposition documents. Activate SPEC-DST-029 prospectively through its
   reviewed definition approval, preserving SPEC-DST-024's recorded history.
3. Correct `tests/test_public_onboarding.py`: test the native installation and
   explicit setup path, check the linked manual examples where they now live,
   and resolve the retained skills from their shipped source locations instead
   of requiring disposable root copies. Use existing CLI and guide inputs;
   no new framework, product behavior or host installation is needed.
4. Correct the current provider/source explanation in
   `docs/notes/technical-communication.md`. Update only the historical banner
   or current pointer in `agentic-execution-phase4-skills.md`, keeping its dated
   body intact. Carry forward the other selected guidance corrections and
   change the AGENTS owner-region reference to this replacement work order.
5. Update the two domain indexes to identify this package and actual states.
   Preserve the original artifact package and all its retained observations
   as inputs carried by the final diff. Write new evidence under WO-PLG-025.
6. Run required checks, retain the bound handoff, record actual completion,
   commit the candidate, and prepare VREC-PLG-022 through released commands.

## Out of scope

Runtime/product source, installer behavior, other tests, templates, package and
marketplace inputs, CI, selected evaluator, managed policy and instruction
fragments, persistent user profiles, archive purges, other projects, release
builds, publication, push, PR and merge. The permission to carry earlier evidence
in the complete diff does not permit rewriting it. Preserve both publication
branches. README changes beyond the exact approved two links are excluded.

## Authorized decision envelope

Once the reviewed definitions and work-order decisions above are applied,
Codex may start, perform these local edits and commits, run checks, retain
evidence, record completion and prepare VREC-PLG-022 under DR-015 without
renewed permission for those operations. Record execution under Codex's own
identity. Engineering, technical and assurance decisions remain explicit.
This grant does not verify a future VREC or authorize external delivery.

Reserve VREC-PLG-022 for the replacement; check all refs again before capture.
VREC-PLG-021 remains uncreated and is not repurposed from the original package.

## Verification and evidence

VER-PLG-025 governs the final candidate. Reuse the earlier migration,
restoration and native-discovery observations only after comparing their
relevant inputs; record the reuse and its limits. Do not rerun successful
unchanged migrations for ceremony. Retain failed runs alongside the successful
remediation results. Run the full source suite after the corrections, plus the
repository's required distribution, CLI, doctor and phase checks.

Use released 0.18.0 from its absolute external Python path with `-I -m se_harness`.
Candidate source is 0.19.0; retain the documented candidate-doctor skew and
require the released doctor to pass. Check the complete diff from the stated
baseline, not only changes made after creating this WO.

The scoped WO-PLG-025 evidence directory includes the normal generated
WO-PLG-025-handoff.md and handoff.json outputs. Inspect other generated capture
destinations before writing. Keep disposable fixtures and bulky raw diagnostics
outside the checkout. Retain actual results, commands, runtime identities,
file digests, review findings and limitations. The candidate and ready VREC
belong in separate commits; no earlier record is rewritten.

## Constraints and stops

Apply ARTIFACT_AUTHORING.md's simplicity and review questions. Reuse the
existing ownership operation and test mechanisms. A new evaluator amendment
feature would require product development, release and adoption; this bounded
replacement uses the currently supported workflow instead.

Stop the affected action for a failed required check, changed approved content
or scope, managed-integrity failure, ID collision, unexpected path, changed
replacement inputs, or a required correction outside this exact scope. Do not
waive test failures, rewrite historical facts or infer approval from a check.

## Completion report

Report the final file inventory, provider choice, onboarding corrections,
actual test and scope results, evidence reuse and limits, candidate commit,
WO-PLG-024 disposition, WO-PLG-025 state and VREC-PLG-022 readiness. Preserve
the released schema-2 result's next accountable action. Preparation makes no
assurance, integration or release decision.
