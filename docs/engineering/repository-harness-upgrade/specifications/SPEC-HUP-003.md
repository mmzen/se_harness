+++
id = "SPEC-HUP-003"
type = "specification"
title = "Post-adoption self-hosting compatibility contract"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
specifies = ["REQ-HUP-007"]
+++

# Specification: Post-adoption self-hosting compatibility contract

## Scope

Reconcile only the owner guidance and seven source-test modules whose
predecessor assumptions became false after the exact released 0.6.0 standard
root was applied. The HUP-002 managed transaction, schema-3 lock, canonical
package templates, product runtime, and release history are immutable inputs.

## Exact implementation surface

1. `AGENTS.md` owner-controlled region.
2. `tests/test_artifact_catalog.py`.
3. `tests/test_context_routing_retirement.py`.
4. `tests/test_dashboard_webui.py`.
5. `tests/test_instruction_architecture.py`.
6. `tests/test_predecessor_assessment_contract.py`.
7. `tests/test_revision_provenance.py`.
8. `tests/test_validation_taxonomy.py`.

## Behavioral rules

1. State that the installed governor is released 0.6.0 and name
   `WORKFLOW.json` and `QUALITY_GATES.json` as managed contracts.
2. Preserve the instruction to run the governing evaluator outside the
   checkout; describe byte equality as valid immediately after released-root
   adoption and future skew as possible only after later product work.
3. Artifact catalog tests must assert current installed/package equality,
   current 0.6.0 semantics, and distinct source paths; they must not infer
   runtime identity from byte inequality.
4. The retired-context inventory must remove the withdrawn router copy and add
   only the exact HUP-002 index, definition, verification, work-order, and
   evidence records that name the preserved owner path.
5. The dashboard topology test must require both installed and packaged 0.6.0
   targets to equal 2,097,152 bytes while keeping the strict boundary test.
6. Owner-instruction tests must expect released 0.6.0 and all schema-3 managed
   paths without weakening the fragment digest or size constraints.
7. The managed-workflow test must compare the installed workflow with the
   packaged released 0.6.0 workflow rather than the predecessor `HEAD` blob;
   the predecessor-assessment workflow itself remains unchanged and pinned to
   its historical 0.5.0 evaluator.
8. Revision-provenance tests must generate one canonical released-evaluator
   evidence document and matching schema-3 lock for temporary released-record
   fixtures. Production validator behavior and evidence requirements remain
   unchanged.
9. Validation taxonomy tests must accept exact installed/package policy
   equality and continue to verify the closed vocabulary and plane semantics.
10. No assertion unrelated to the ten observed failures may be relaxed.

## Error behavior

Any new or remaining unit failure, changed managed-root byte, checkout-origin
governor, expanded path, production legacy exemption, owner-region size breach,
graph error, or external action stops the work order without a completion
transition.

## Verification

Run the ten previously failing tests first, their seven complete modules next,
then the complete suite. Re-run released 0.6.0 identity, doctor, validate,
preflight, inspect, dashboard, release-distribution validation, no-op upgrade,
scope audit, evidence scan, and diff checks.
