+++
id = "WO-IAR-022"
type = "work_order"
title = "Stop shipping obsolete guide pointers safely"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Later discovery, adoption and assurance decisions rely on changed trusted content or retained host evidence. The human approved verification bound to the exact candidate commit."
decided_by = "mmzen"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md",
  "pyproject.toml",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "tests/test_installer.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_progressive_instruction_discovery.py",
  "tests/test_instruction_discovery.py",
  "tests/test_release_build.py",
  "tests/test_upgrade_rehearsal.py",
  "tests/plugin_integration/progressive_discovery/",
  "templates/repository/standard/docs/engineering/harness/UPGRADE.md",
  "templates/repository/standard/docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md",
  "docs/engineering/instruction-architecture/acceptance/guide-retirement/",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-022.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-022/",
]

[relations]
implements = ["REQ-IAR-028", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014", "SPEC-IAR-015"]
verification = ["VER-IAR-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T07:52:17Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve, you can start the work orders\". Approval covers the reviewed instruction-cleanup package and required commit-bound assurance. Legacy evaluator role engineering-owner records that human decision; Codex applies it. Reviewed SHA-256 cb0d5f0455ae20e2c46c2cc19997b4775d5c2390a54d2339c9a287965ff722bc."
scope_paths = ["templates/repository/standard/docs/engineering/OPERATING_CARD.md", "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md", "templates/repository/standard/docs/engineering/QUALITY_GATES.md", "templates/repository/standard/docs/engineering/WORKFLOW.md", "templates/repository/standard/docs/engineering/TRACEABILITY.md", "templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md", "pyproject.toml", "se_harness/installer.py", "se_harness/preflight.py", "tests/test_installer.py", "tests/test_hash_bound_integrity.py", "tests/test_instruction_architecture.py", "tests/test_workflow_documentation_contract.py", "tests/test_progressive_instruction_discovery.py", "tests/test_instruction_discovery.py", "tests/test_release_build.py", "tests/test_upgrade_rehearsal.py", "tests/plugin_integration/progressive_discovery/", "templates/repository/standard/docs/engineering/harness/UPGRADE.md", "templates/repository/standard/docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md", "docs/engineering/instruction-architecture/acceptance/guide-retirement/", "docs/engineering/instruction-architecture/work-orders/WO-IAR-022.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/"]
+++

# Stop shipping obsolete guide pointers safely

## Objective

Implement the product-wide retirement option if selected in DEC-IAR-002.
New installations use the current collection; existing owner files survive
upgrades. This work does not delete the six installed files in this repository.

## Dependencies and entry conditions

DEC-IAR-002 must select the product-wide option. REQ-IAR-028, SPEC-IAR-015 and
VER-IAR-017 must be accepted, and this WO must be approved with required
assurance. Use the verified active-reference correction from WO-IAR-021 as the
implementation base. Record its exact source commit and evidence in the handoff.
These are contractual stop conditions; no unsupported depends_on relation or
invented automatic lifecycle dependency is added.

## In scope and planned sequence

1. Inventory current consumers of all six paths. Classify necessary historical
   references and old-release adapters. Confirm replacement routes independently.
2. Remove the six current source templates and their pyproject distribution
   entries together. Do not remove files from installed repository policy.
3. Exercise existing leaving-seed behavior first. Change installer/preflight
   only if a demonstrated gap prevents the specified preservation, supported
   predecessor migration, clear preview or consistent resulting readiness.
   Keep this correction inside the existing ownership and transaction model.
4. Describe the preserved-owner upgrade and separate cleanup procedure in the
   product's upgrade/migration guidance. Use supported commands; do not introduce
   a speculative delete flag or promise an unavailable command.
5. Run fresh-install, upgrade, negative-control, packaging and replay tests.
   Record exact bytes, paths, lock effects and remaining references.

## Out of scope

No automatic owner-seed deletion, machine-policy change, new lifecycle/schema,
new CLI command, removal of old-version adapters/fingerprints, accepted-history
rewrite or deletion of this repository's installed pointers. No root or
ARTIFACT_AUTHORING removal. Unused renderer cleanup is deferred until its callers
and compatibility obligations are separately established. Release and adoption
are later actions; no version or tag is authorized here.

## Authorized decision envelope

After approval, choose the smallest change satisfying SPEC-IAR-015. Prefer the
existing installer behavior; it already lets seeds leave the tracked set while
preserving owner files. Test helpers may be adjusted where their old expectation
conflicts with the accepted new contract, while preserving real coverage.
Do not lower upgrade guarantees to make the new package pass.

## Expected change surface and stops

Six templates, packaging entries, bounded installer/readiness corrections only
if needed, migration guidance and focused tests are the complete product scope.
Stop on an active consumer not covered by WO-IAR-021, customized owner ambiguity,
unsafe destination, a required new public command or an unsupported predecessor.
An architectural boundary change requires a new reviewed definition package.
Real repository cleanup additionally waits for WO-IAR-020 native qualification,
a published release and a separately approved adoption work order.

## Required verification and evidence

Apply VER-IAR-017 on Windows and Linux, including the real installed-wheel
rehearsal. Retain the complete consumer disposition and owner-preservation proof
under evidence/WO-IAR-022/. A clean source search alone is insufficient.

## Assurance and completion

The human repository owner, mmzen, confirmed commit-bound assurance as
`required`: later discovery, adoption and assurance decisions rely on changed
trusted content or retained host evidence. Verification must bind the exact
candidate commit. The recorded approval is: "I approve, you can start the work orders".

The evaluator records work authority through the explicit lifecycle transition.
This approval does not grant verification acceptance, release or real host
configuration authority beyond the decision envelope above.

After approval, use the repository-selected released evaluator for the exact
WO's start, scope and handoff checks. Retain actual findings and the complete
declared change set. Prepare a VREC through the supported command for the exact
clean candidate commit; only a human may accept it.

The completion report gives the WO ID, candidate commit, changed files, contract
criteria and observed evidence, unresolved limitations, retained evidence paths,
actual evaluator result and its next typed step. A passing preview is not an
applied transition. No accepted definition or history is rewritten by this WO.
