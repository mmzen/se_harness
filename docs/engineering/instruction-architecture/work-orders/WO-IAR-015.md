+++
id = "WO-IAR-015"
type = "work_order"
title = "Deliver current instructions at startup and after compaction"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "quality-owner"]
created = "2026-09-20"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Later engineering and governance decisions rely on the instruction, discovery and ownership behavior; verification must bind the exact candidate commit. The reviewed required classification is adopted by the user's instruction to start these work orders."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/.agents/skills/",
  "templates/repository/standard/.claude/skills/",
  "plugins/verity-plane/common/",
  "plugins/verity-plane/codex/",
  "plugins/verity-plane/claude-code/",
  "scripts/build_plugin_archives.py",
  "scripts/build_plugin_marketplace.py",
  "tests/plugin_integration/progressive_discovery/",
  "tests/plugin_integration/test_simple_plugin.py",
  "tests/plugin_integration/package_assembly/",
  "tests/plugin_integration/change_skill/",
  "tests/plugin_integration/evidence-skill/",
  "tests/plugin_integration/repository_connection/",
  "tests/plugin_integration/onboarding/",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-015.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-015/",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-026", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "engineering-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
scope_paths = ["templates/repository/standard/.agents/skills/", "templates/repository/standard/.claude/skills/", "plugins/verity-plane/common/", "plugins/verity-plane/codex/", "plugins/verity-plane/claude-code/", "scripts/build_plugin_archives.py", "scripts/build_plugin_marketplace.py", "tests/plugin_integration/progressive_discovery/", "tests/plugin_integration/test_simple_plugin.py", "tests/plugin_integration/package_assembly/", "tests/plugin_integration/change_skill/", "tests/plugin_integration/evidence-skill/", "tests/plugin_integration/repository_connection/", "tests/plugin_integration/onboarding/", "docs/engineering/instruction-architecture/README.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-015.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-015/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T07:43:56Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Execute the reviewed approved work orders as requested by the human on 2026-09-27; native host/platform qualification remains required before completion."
+++

# Deliver current instructions at startup and after compaction

## Objective

Deliver current instructions at startup and after compaction. This work order is a draft and grants no execution authority.

## In scope

Add the smallest host-supported mechanism that delivers the repository's
selected root at startup and after compaction. Update shared skills and host
instructions and alternate repository-owned skill templates to use the current
procedure and conditional references. Keep supported provider routes coherent. Preserve
actual evaluator results, identities and command boundaries. Verify switching
repositories, unavailable inputs and uncertain-operation recovery. Retain native
Codex and Claude Code traces for each automatic delivery claim.

## Dependencies and sequencing

Consume the real collection and discovery result from WO-IAR-013 and WO-IAR-014 for integrated acceptance. A host API limitation is an explicit delivery gap, not permission to restore the AGENTS gate.

DEC-IAR-001 records the remaining adoption/legacy-authority question and blocks
work-order approval while open. All three orders use the same specification,
architecture decision and verification contract.

## Out of scope

No accepted definition/history rewrite; new exception engine; generic revision
command; changed lifecycle/gate/decision-right semantics; installed root policy,
AGENTS.md or lock edits; real user host settings; release build, version bump,
publication, deployment or self-adoption. An isolated non-promotable package
build for acceptance is permitted only after approval and outside the checkout.

## Authorized decision envelope

After approval, the executor may choose code organization and precise wording
within the accepted contract and paths. Routine execution uses the existing
approved-work procedure and needs no duplicate permission. Additional paths,
changed semantics or missing native host support require a bounded proposal.
No push, PR creation, merge, release or other external delivery is granted here.

## Assurance classification

Commit-bound verification is required. On 2026-09-27 the human instructed:
“so let's start the work orders”, adopting the previously reviewed package and
its proposed required verification classification. The machine table records
that classification. Approval and start are applied through harnessctl;
this prose does not itself change lifecycle state.

## Required verification

Native event demonstrations, stale/missing input cases, replayed workflow/authority checks and complete reading-set measurements from VER-IAR-014.
Run applicable repository checks and required phase/handoff checks from that
contract. Classify existing unrelated warnings separately. Do not mark missing
host/platform evidence as passed.

## Evidence and completion

Retain actual outputs, source identities, complete changed paths, selected
contract coverage and limitations under evidence/WO-IAR-015/. Report completed
behavior, failed/unassessed cases, final evaluator state and its exact next
action. Prepare required VREC evidence through released commands when eligible.

## Stop conditions

Stop the affected action for failed integrity, scope, authority or required
checks; a policy conflict; unsafe owner-content migration; or a required input
that cannot be obtained. Preserve unrelated changes and prior evidence.
