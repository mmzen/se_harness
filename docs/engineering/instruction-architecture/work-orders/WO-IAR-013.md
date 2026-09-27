+++
id = "WO-IAR-013"
type = "work_order"
title = "Split the agent instructions and preserve their meaning"
status = "approved"
owners = ["engineering-owner", "repository-owner", "quality-owner"]
created = "2026-09-20"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Later engineering and governance decisions rely on the instruction, discovery and ownership behavior; verification must bind the exact candidate commit. The reviewed required classification is adopted by the user's instruction to start these work orders."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/",
  "tests/test_instruction_architecture.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_progressive_instruction_discovery.py",
  "docs/engineering/instruction-architecture/acceptance/progressive-discovery/",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-013.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-013/",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "engineering-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
scope_paths = ["templates/repository/standard/ENGINEERING_HARNESS.md.tpl", "templates/repository/standard/docs/engineering/", "tests/test_instruction_architecture.py", "tests/test_workflow_documentation_contract.py", "tests/test_progressive_instruction_discovery.py", "docs/engineering/instruction-architecture/acceptance/progressive-discovery/", "docs/engineering/instruction-architecture/README.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-013.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-013/"]
+++

# Split the agent instructions and preserve their meaning

## Objective

Split the agent instructions and preserve their meaning. This work order is a draft and grants no execution authority.

## In scope

Create the compact root and 25 supporting files in the candidate template
tree. Assign all source sections and rules, convert the 31 main steps to headings,
repair stale links, and make reading triggers and outputs explicit. Resolve
the decision-right annotation through existing recorded rights, retaining any
semantic question for human review. Make COMMUNICATION.md canonical. State
unsupported exception/revision behavior. Update retained authoring references
and prepare the owner-region adoption map without editing installed AGENTS.md.

## Dependencies and sequencing

Content work may begin after its own approval and gates. It supplies destinations to the evaluator and host work orders; combined acceptance waits for all three.

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

Content allocation, link/step coverage, exact-command inspection and representative reading measurements from VER-IAR-014.
Run applicable repository checks and required phase/handoff checks from that
contract. Classify existing unrelated warnings separately. Do not mark missing
host/platform evidence as passed.

## Evidence and completion

Retain actual outputs, source identities, complete changed paths, selected
contract coverage and limitations under evidence/WO-IAR-013/. Report completed
behavior, failed/unassessed cases, final evaluator state and its exact next
action. Prepare required VREC evidence through released commands when eligible.

## Stop conditions

Stop the affected action for failed integrity, scope, authority or required
checks; a policy conflict; unsafe owner-content migration; or a required input
that cannot be obtained. Preserve unrelated changes and prior evidence.
