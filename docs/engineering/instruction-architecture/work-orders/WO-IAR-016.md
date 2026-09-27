+++
id = "WO-IAR-016"
type = "work_order"
title = "Package the approved startup and compaction instruction delivery"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Future host-delivery and release decisions rely on the archive builder validating the reviewed event configuration and packaged script."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/plugin_distribution.py",
  "tests/plugin_integration/package_assembly/",
  "tests/plugin_integration/test_simple_plugin.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-016.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-016/",
]

[relations]
implements = ["REQ-IAR-026", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:54:07Z"
decided_by = "engineering-owner"
reason = "Human decision: Approve the packaging scope correction. Apply the reviewed bounded builder proposal as a separate work order; no external delivery authority."
scope_paths = ["repository_tools/plugin_distribution.py", "tests/plugin_integration/package_assembly/", "tests/plugin_integration/test_simple_plugin.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-016.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-016/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T07:54:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Execute the human-approved bounded packaging correction under the recorded work-order approval."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-27T17:07:04Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex records completion under the existing approved scope after the retained closeout review, current required checks and passing handoff. Source identity, full regressions, exact lifecycle comparison, platform installer evidence and separate native qualification are retained with explicit limitations. No verification, merge, release or adoption is inferred."
+++

# Package the approved startup and compaction instruction delivery

## Objective

Correct the existing development builder's blanket refusal of hook assets so
it can package the instruction delivery approved under WO-IAR-015. Keep direct
callers and the wrapper consistent instead of duplicating the builder.

## In scope

Validate the reviewed startup/compaction event configuration and referenced
packaged script before writing archives. Accept the approved assets. Refuse
malformed, missing or unsupported hook assets before output replacement.

## Authorization basis

On 2026-09-27 the human answered: “Approve the packaging scope correction”.
The exact bounded proposal is retained in
`../evidence/WO-IAR-015/packaging-scope-proposal.md`. This separate work order
preserves WO-IAR-015's approved scope and history. Approval and start are
applied through released evaluator transitions, not inferred from this prose.

## Dependencies and constraints

Consume the reviewed host delivery assets from WO-IAR-015 and the instruction
collection/discovery from WO-IAR-013 and WO-IAR-014 for integrated acceptance.
Retain wheel identity checks, release/development separation, output ownership
and refusal before writes. A package alone does not establish host qualification.

## Out of scope

No lifecycle/decision-right changes, real user settings, installed root edits,
automatic upgrade, promotable release build, push, PR, publication, deployment
or self-adoption. No additional implementation paths are implied.

## Authorized decision envelope

After approval, choose the minimal implementation and failure tests within
these paths. Routine implementation, checks, local commits, completion and
required verification preparation need no duplicate permission. New scope or
changed accepted semantics require a bounded proposal. Human verification
acceptance and external delivery remain separate.

## Required verification

Apply VER-IAR-014's package and host boundaries. Test direct and wrapper
assembly, both approved host configurations, missing/malformed assets and
unchanged outputs after refusal. Preserve identity and output-ownership failure
tests. Run applicable repository checks and released preflight/handoff checks.
Report missing native host/platform evidence as unverified, never as passed.

## Evidence and completion

Retain actual commands, exit codes, candidate/evaluator identities, complete
changed paths, checks and limitations in `../evidence/WO-IAR-016/`. Complete
only after this bounded implementation and its required evidence are ready.
Prepare commit-bound verification through the supported evaluator command;
a human makes the verification acceptance decision.

## Stop conditions

Stop the affected action on failed integrity, invalid selected inputs, missing
authority, scope mismatch or a required check failure. Preserve prior evidence
and inspect uncertain writes before retrying.
