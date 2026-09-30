+++
id = "WO-IAR-028"
type = "work_order"
title = "Build the released resource resolver and evaluator route"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification with package approval. Later agent, CI and installation decisions rely on these instructions, selectors and integrity checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/resources.py",
  "se_harness/cli.py",
  "se_harness/artifact_layout.py",
  "se_harness/instruction_discovery.py",
  "se_harness/instruction_discovery.json",
  "se_harness/preflight.py",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "se_harness/runtime_identity.py",
  "se_harness/evaluator_identity.py",
  "se_harness/workflow_contract.py",
  "se_harness/engine/validation_core.py",
  "se_harness/engine/validation_authoring.py",
  "se_harness/engine/inspect_engineering_artifacts.py",
  "se_harness/engine/dashboard_snapshot.py",
  "se_harness/engine/dashboard_bundle.py",
  "se_harness/hash_bound.py",
  "se_harness/hash_bound_classes.json",
  "pyproject.toml",
  "MANIFEST.in",
  "templates/repository/standard/",
  "tests/test_resources.py",
  "tests/test_instruction_discovery.py",
  "tests/test_progressive_instruction_discovery.py",
  "tests/test_instruction_architecture.py",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_artifact_catalog.py",
  "tests/test_evaluator_identity.py",
  "tests/test_hash_bound_integrity.py",
  "tests/artifact_support.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-028.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-018.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-018-evaluator.json",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-028/",
  "tests/test_installer.py",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-029"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 8be03ea7c47f1c767b2193326f341d2b743e3325bae83ad84ecee167109c0e1f. Only the confirmed assurance metadata and its explanatory paragraph were completed before preview."
scope_paths = ["se_harness/resources.py", "se_harness/cli.py", "se_harness/artifact_layout.py", "se_harness/instruction_discovery.py", "se_harness/instruction_discovery.json", "se_harness/preflight.py", "se_harness/installer.py", "se_harness/integrity.py", "se_harness/runtime_identity.py", "se_harness/evaluator_identity.py", "se_harness/workflow_contract.py", "se_harness/engine/validation_core.py", "se_harness/engine/validation_authoring.py", "se_harness/engine/inspect_engineering_artifacts.py", "se_harness/engine/dashboard_snapshot.py", "se_harness/engine/dashboard_bundle.py", "se_harness/hash_bound.py", "se_harness/hash_bound_classes.json", "pyproject.toml", "MANIFEST.in", "templates/repository/standard/", "tests/test_resources.py", "tests/test_instruction_discovery.py", "tests/test_progressive_instruction_discovery.py", "tests/test_instruction_architecture.py", "tests/test_artifact_authoring.py", "tests/test_artifact_authoring_policy.py", "tests/test_artifact_catalog.py", "tests/test_evaluator_identity.py", "tests/test_hash_bound_integrity.py", "tests/artifact_support.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-028.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-018.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-018-evaluator.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-028/", "tests/test_installer.py", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T11:13:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved resource resolver and evaluator work under human mmzen package approval and required commit-bound verification. Implementation baseline 05bd4e76ba73cbce3117c27774181b97c374915b; installed 0.20.0 remains governing."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-30T11:58:41Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed VER-IAR-020 resource and public-workflow qualification at committed implementation 6b6f64ed94ecfc89dcc9c74179a742b134edd87a. Released combined Git-derived handoff passed from base 3ed0fc5e89462011ea115ad4c4191067f815cf95."
+++

# Build the released resource resolver and evaluator route

## Objective

Implement IAR-EXT-001 to IAR-EXT-004 and IAR-EXT-006: the packaged resource lookup,
portable layout selection and discovery locations; direct authoring from the wheel;
updated readiness checks and candidate source assets. Retain the supported legacy
route. Provide a small tested resource-query command; do not build a registry.
This unit establishes the resource contract and candidate fixture support. The
default installer migration and actual host qualification follow in later units.

## Execution order

No preceding work order. Begin only after the package and applicability decision are accepted.

## In scope and change surface

The execution_scope paths above are the complete allowed surface. Directory
prefixes cover only the named component. New files are permitted only where
the declared contract requires them. Template source changes affect future
packages; they do not authorize changing this repository's installed copies.
Shared file overlap is intentional and sequential: resource support first,
host adapter next, then default installation and integrated migration.

## Out of scope

No changed lifecycle decisions, risk waivers, generic accepted-definition revision,
new policy service, plugin-only policy fork, broad refactor or dependency framework.
No edit to accepted formal definitions, installed ENGINEERING_HARNESS.md,
docs/engineering/harness/, installed templates, machine policy, root configuration
or lock. No credentials, real user settings, release/version adoption, push,
PR, merge, marketplace publication or tagging is authorized by this draft.

## Authorized decision envelope

After approval, the executor may implement the selected contract, choose routine
internal details within the declared paths, run its checks, make local commits,
retain evidence, record completion and prepare verification. Scope or contract
changes return for review. Human verification and external actions remain separate.

## Confirmed assurance

Required commit-bound verification. Human mmzen confirmed this classification
with the package approval: "I confirm and approve". Later agent, CI and
installation decisions rely on these instructions, selectors and integrity checks.

## Required verification

Execute VER-IAR-020. Starting focused checks: python -m unittest tests.test_resources tests.test_artifact_authoring tests.test_artifact_authoring_policy tests.test_instruction_discovery tests.test_progressive_instruction_discovery tests.test_instruction_architecture tests.test_evaluator_identity tests.test_hash_bound_integrity
Use the exact installed released 0.20.0 evaluator for repository identity,
validation, start/review preflight and complete Git-derived scope/handoff checks.
Test candidate behavior only through the separate candidate route. Prepare this work order's record at its exact candidate. Later combined qualification does not erase earlier results.

## Evidence to record

Retain actual commands, runtime/resource identities, check results, failures and
criterion assessment under docs/engineering/instruction-architecture/evidence/WO-IAR-028/. Use VREC-IAR-018 and its declared evaluator
companion only if that ID remains unused across local refs at capture time.
Do not create a VREC by editing a template. Approval grants preparation of the
named outputs, not acceptance. A conflicting ID requires a reviewed path correction.

The shared VREC-IAR-020 destinations authorize later aggregate capture of all
three work orders at one final candidate; they grant no human acceptance.

## Stop conditions and completion

Stop the affected action for a changed approved contract, out-of-scope path,
missing human decision, integrity mismatch, failing required check or ambiguous
migration input. Preserve evidence and report the exact correction needed.
Report changed behavior, complete file scope, actual tests, remaining limitations,
candidate and evidence identities, and the evaluator's next typed step.
