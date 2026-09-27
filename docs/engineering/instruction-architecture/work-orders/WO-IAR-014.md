+++
id = "WO-IAR-014"
type = "work_order"
title = "Implement evaluator discovery and safe installer migration"
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
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/workflow.py",
  "se_harness/workflow_result.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/instruction_discovery.py",
  "se_harness/instruction_discovery.json",
  "se_harness/codes.py",
  "se_harness/integrity.py",
  "se_harness/cli.py",
  "se_harness/skill_ownership.py",
  "se_harness/skill_ownership_contract.json",
  "templates/repository/standard/AGENTS.md.fragment",
  "templates/repository/standard/CLAUDE.md.fragment",
  "tests/test_instruction_discovery.py",
  "tests/test_instruction_architecture.py",
  "tests/test_repository_context_retirement.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_installer.py",
  "tests/test_preflight.py",
  "tests/test_workflow_restitution.py",
  "tests/test_workflow_procedures.py",
  "tests/test_skill_ownership.py",
  "tests/fixtures/progressive-discovery/",
  "pyproject.toml",
  "MANIFEST.in",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-014.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-014/",
]

[relations]
implements = ["REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "engineering-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
scope_paths = ["se_harness/installer.py", "se_harness/preflight.py", "se_harness/workflow.py", "se_harness/workflow_result.py", "se_harness/workflow_procedures.py", "se_harness/workflow_contract.json", "se_harness/workflow_contract.py", "se_harness/instruction_discovery.py", "se_harness/instruction_discovery.json", "se_harness/codes.py", "se_harness/integrity.py", "se_harness/cli.py", "se_harness/skill_ownership.py", "se_harness/skill_ownership_contract.json", "templates/repository/standard/AGENTS.md.fragment", "templates/repository/standard/CLAUDE.md.fragment", "tests/test_instruction_discovery.py", "tests/test_instruction_architecture.py", "tests/test_repository_context_retirement.py", "tests/test_context_routing_retirement.py", "tests/test_installer.py", "tests/test_preflight.py", "tests/test_workflow_restitution.py", "tests/test_workflow_procedures.py", "tests/test_skill_ownership.py", "tests/fixtures/progressive-discovery/", "pyproject.toml", "MANIFEST.in", "docs/engineering/instruction-architecture/README.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-014.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-014/"]
+++

# Implement evaluator discovery and safe installer migration

## Objective

Implement evaluator discovery and safe installer migration. This work order is a draft and grants no execution authority.

## In scope

Bind returned procedures and typed steps to exact reading destinations and
separate human reading from evaluator-only inputs. Retire AGENTS fragment
generation/tracking/readiness and the legacy CLAUDE harness adapter. Package
the new collection with explicit ownership, preserve custom/owner content, and
refuse unsafe migrations before writes. Update affected regressions and package
inclusion. Add no lifecycle edges, gate waivers or decision authority.

## Dependencies and sequencing

Use the destinations and semantic map from WO-IAR-013. Installer and discovery tests may use bounded fixtures during development; completion needs the actual collection.

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

Full procedure/typed-step mapping, unchanged lifecycle outcomes, result-consumer compatibility, install/upgrade/refusal/retry and Windows/Linux preservation cases from VER-IAR-014.
Run applicable repository checks and required phase/handoff checks from that
contract. Classify existing unrelated warnings separately. Do not mark missing
host/platform evidence as passed.

## Evidence and completion

Retain actual outputs, source identities, complete changed paths, selected
contract coverage and limitations under evidence/WO-IAR-014/. Report completed
behavior, failed/unassessed cases, final evaluator state and its exact next
action. Prepare required VREC evidence through released commands when eligible.

## Stop conditions

Stop the affected action for failed integrity, scope, authority or required
checks; a policy conflict; unsafe owner-content migration; or a required input
that cannot be obtained. Preserve unrelated changes and prior evidence.
