+++
id = "WO-PLG-024"
type = "work_order"
title = "Remove obsolete root integration files and adopt plugin skills"
status = "rejected"
owners = ["engineering-owner"]
created = "2026-09-16"
updated = "2026-09-16"

rejected_at = "2026-09-16T12:40:39Z"
rejected_by = "engineering-owner"
rejection_reason = "Remaining execution is replaced by WO-PLG-025 because the original scope omitted required README, test and documentation corrections. Preserve the already applied cleanup and all observations. This disposition closes the original work authorization; it neither marks that work complete nor rejects the released plugin-ownership behavior. The owner approved this exact replacement disposition with \"i approve\" on 2026-09-16."
[assurance]
commit_bound_verification = "required"
rationale = "Later checks and contributors will rely on the changed skill-provider lock, root skill inventory and operational guidance."
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
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-021.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-021-evaluator.json",
]

[relations]
implements = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-KIS-009"]
specifications = ["SPEC-PLG-021", "SPEC-KIS-003"]
architecture = ["ARCH-PLG-004", "ADR-PLG-004", "ARCH-KIS-002", "ADR-KIS-002"]
verification = ["VER-PLG-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T09:05:14Z"
decided_by = "engineering-owner"
reason = "On 2026-09-16 the owner approved VER-PLG-024 and WO-PLG-024 in response to the exact reviewed draft package and named roles. Record engineering-owner approval of this bounded cleanup, reviewed SHA-256 5f4c0a2441443f2a712451cb5173400474c247b389e95100c69700e568190eb0. DR-015 authorizes routine execution and required verification preparation; assurance and external delivery remain separate."
scope_paths = [".engineering-harness.delegation.toml", ".engineering-harness.lock", ".agents/skills/harness-operator-brief/SKILL.md", ".agents/skills/harness-operator-brief/scripts/check_brief.py", ".agents/skills/harness-operator-brief/skill-contract.json", ".agents/skills/harness-orient/SKILL.md", ".agents/skills/harness-orient/scripts/orient.py", ".agents/skills/harness-orient/skill-contract.json", ".claude/skills/harness-orient/SKILL.md", "AGENTS.md", "docs/notes/developing-se-harness.md", "docs/notes/README.md", "docs/notes/delegation-class.md", "docs/notes/agentic-execution-plugin-distribution.md", "docs/notes/codebase-kiss-work-orders-2026-09-13.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-024.md", "docs/engineering/plugin-integration/verification/VER-PLG-024.md", "docs/engineering/plugin-integration/evidence/WO-PLG-024/", "docs/engineering/plugin-integration/verification-records/VREC-PLG-021.md", "docs/engineering/plugin-integration/evidence/VREC-PLG-021-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-16T09:08:42Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the owner-approved cleanup under DR-015 after the released start preflight passed. The approved behavior and path scope are unchanged."

[[lifecycle_events]]
from = "in_progress"
to = "rejected"
decided_at = "2026-09-16T12:40:39Z"
decided_by = "engineering-owner"
reason = "Remaining execution is replaced by WO-PLG-025 because the original scope omitted required README, test and documentation corrections. Preserve the already applied cleanup and all observations. This disposition closes the original work authorization; it neither marks that work complete nor rejects the released plugin-ownership behavior. The owner approved this exact replacement disposition with \"i approve\" on 2026-09-16."
+++

# Remove obsolete root integration files and adopt plugin skills

## Objective

Make this checkout use the released plugin ownership option and remove root
integration remnants that no longer serve its 0.18.0 evaluator. This applies
existing behavior to this repository; it does not change that behavior or
reopen the approved requirements, specifications or architecture decisions.

The planning baseline is `f05c478a29c39f94968fdc842a34c861d30a42ac` on
2026-09-16. It includes the owner's latest README edits and deletion of
`VALUE_PROPOSAL_EXEC.md` and `VALUE_PROPOSAL_LONG.md`. Preserve those changes.
The selected governor is released 0.18.0; candidate source reports 0.19.0.

## In scope

1. Delete the unused `.engineering-harness.delegation.toml`. Its separate
   live-PR delegation prerequisite was retired by SPEC-KIS-003 and the root
   evaluator upgrade. Preserve historical explanations and evidence as history.
2. Apply the released `skill-ownership --provider plugin` operation to this
   checkout, selecting the installed Verity Plane replacement. Remove the seven
   catalogued root skill files and let the command write the schema-4 lock with
   `skill_ownership.provider = "plugin"`. Preserve all unrelated lock entries
   and the selected evaluator identity. Do not hand-edit the lock or replace
   product templates.
3. Update the owner region of AGENTS.md and the selected contributor guide to
   explain this checkout's provider choice, per-host plugin installation, the
   existing installation guide, and repository-skill restoration. A clone can
   run the evaluator without a locally installed plugin; invoking plugin skills
   requires that host's plugin installation. Correct the schema-3 description
   for this root without changing general default-installation guidance.
4. Correct the current execution explanation and its notes-index entry. Mark
   the old plugin proposal and dated KISS work-order plan as historical, linking
   current guidance and recorded completion without rewriting their dated
   analysis. Add a concise cleanup entry to the plugin domain index.
5. Retain the required checks and review, record completion, and prepare the
   commit-bound verification record for this work through the released tools.

## Out of scope

Product source, tests, templates, package inputs, plugin source and marketplace
catalogs, CI, evaluator version, root managed policy and instruction fragments,
CLAUDE.md, README.md, release branches, older formal artifacts and retained
evidence are unchanged. No archive purge, backlog disposition, cache cleanup,
release build, provider-catalog submission, or migration of other repositories
is included. The historical proposals keep their paths and dated contents;
only a current-status banner or pointer is added.

At baseline there is no root `.agent/` or `.codex/`. The selected seven files
are in `.agents/` and `.claude/`; this work grants no general deletion of host
configuration directories or unrelated skills.

## Authorized decision envelope

Draft preparation grants no lifecycle approval. Once the engineering owner
approves this WO and the assurance owner approves VER-PLG-024, Codex may select
and execute it under DR-015: start, edit, make local commits, run checks, retain
evidence, record completion and prepare verification without further permission
for those covered operations. Use the executor's own identity.

The executor may choose concise wording, evidence filenames within the named
directory and disposable fixture locations outside the checkout. It may use
the already installed plugin and disposable host profiles to check discovery.
It may not change persistent user plugin installations or profiles. Approval
does not verify a future VREC or authorize push, PR, merge, publication or a
different delivery target. Preserve `plugin-marketplace` and
`work/plugin-marketplace-publication`.

VREC-PLG-021 is reserved for this package, not authored or decided here. Check
its continued availability before capture; a collision requires an explicit
bounded scope amendment rather than overwriting another record.

## Constraints

Use the absolute Python path of the external released 0.18.0 environment with
`-I -m se_harness`, from outside the checkout, for governance. Follow the
selected check's phase manifest and procedures. Apply the shared design and
review questions in ARTIFACT_AUTHORING.md; the existing ownership command is
the smallest complete solution and needs no migration framework or new tests
that merely repeat its implementation.

Before applying the ownership command, inspect a fresh preview, the required
replacement files and every existing deletion destination. Resolve each
destination inside this checkout, reject redirects, and confirm there are no
extra files outside the seven authorized paths. The unused fourth disposable
directory must still be absent. If the actual deletion surface has changed,
stop that operation and amend scope. Do not infer native discovery or package
authenticity from the command's file-presence check.

## Expected change surface

Exactly eight tracked removals are expected: the delegation TOML and seven
root skill files. The lock changes only ownership schema/provider and those
seven catalog entries. The other changes are the explicitly selected guidance,
this new artifact package and its evidence. The current root copies total
61,153 Git-blob bytes; this cleanup reduces confusion, not repository size.
Large historical evidence remains subject to its existing retention decisions.

## Required verification

Meet VER-PLG-024 C01-C04 using the existing checks. Run the repository-required
source suite, distribution validation, CLI smoke and applicable doctor and
preflight checks; distinguish candidate-source output from the released
governor's result. Use released graph validation, scope and handoff checkpoints,
and review preflight at the stages required by the selected procedure. Inspect the complete diff
against the approved scope. Do not add a build or host-version matrix.

## Evidence to record

Keep one concise summary under `evidence/WO-PLG-024/` with the baseline and final
candidate, actual command outcomes, coverage, material review findings and
limits. Retain relevant command results there or reference immutable earlier
evidence after comparing its inputs. Generated scratch environments and bulky
diagnostics stay outside the checkout. Do not copy historical evidence trees
or invent successful checks. Candidate and VREC belong in separate commits.

## Stop and escalate conditions

Stop the affected action for missing authority, failed managed integrity or a
required check, invalid governing relations, missing replacement skills,
unexpected deletion targets, changed approved scope, or an out-of-scope fix.
Resolve in-scope failures and continue unchanged authority. Preserve actual
failure results and unchanged lifecycle states. A missing native host is a
reported observation limit, subject to C03's explicit evidence-reuse rule.

## Completion report format

Report removed files, provider/lock outcome, guidance corrections, actual
checks and limitations, candidate identity, retained evidence, selected artifact
states and exactly one next accountable action from the released schema-2
result. Completion records work performed; assurance and delivery remain
separate decisions.
