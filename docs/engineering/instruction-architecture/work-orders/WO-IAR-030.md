+++
id = "WO-IAR-030"
type = "work_order"
title = "Deliver minimal installation and safe resource migration"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification with package approval. Later agent, CI and installation decisions rely on these instructions, selectors and integrity checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/installer.py",
  "se_harness/cli.py",
  "se_harness/preflight.py",
  "se_harness/skill_ownership.py",
  "se_harness/skill_ownership_contract.json",
  "se_harness/integrity.py",
  "se_harness/hash_bound.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/github_ci.py",
  "templates/repository/standard/",
  "tests/test_installer.py",
  "tests/test_skill_ownership.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_artifact_catalog.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_instruction_architecture.py",
  "tests/test_resources.py",
  "tests/plugin_integration/progressive_discovery/",
  "tests/artifact_support.py",
  "README.md",
  "GLOSSARY.md",
  "docs/notes/getting-started.md",
  "docs/notes/developing-se-harness.md",
  "release/plugin-marketplace/README.md",
  "scripts/validate_release_distributions.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-030.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-030/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/artifact-authoring.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 79a1e2f0169fbf338322dcc1636fe0d9ec6072b54a2b58dd9726acc7cd93cd91. Only the confirmed assurance metadata and its explanatory paragraph were completed before preview."
scope_paths = ["se_harness/installer.py", "se_harness/cli.py", "se_harness/preflight.py", "se_harness/skill_ownership.py", "se_harness/skill_ownership_contract.json", "se_harness/integrity.py", "se_harness/hash_bound.py", "se_harness/candidate_acceptance.py", "se_harness/github_ci.py", "templates/repository/standard/", "tests/test_installer.py", "tests/test_skill_ownership.py", "tests/test_hash_bound_integrity.py", "tests/test_artifact_catalog.py", "tests/test_workflow_documentation_contract.py", "tests/test_instruction_architecture.py", "tests/test_resources.py", "tests/plugin_integration/progressive_discovery/", "tests/artifact_support.py", "README.md", "GLOSSARY.md", "docs/notes/getting-started.md", "docs/notes/developing-se-harness.md", "release/plugin-marketplace/README.md", "scripts/validate_release_distributions.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-030.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-030/", "docs/notes/harnessctl-reference.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/artifact-authoring.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md"]
+++

# Deliver minimal installation and safe resource migration

## Objective

Complete default initialization and legacy upgrade through the existing installer
transaction. Add explicit integration/scaffolding selection only where needed.
Handle Git byte rules, owner seed preservation, pre-write validation, interruption
and repeat execution. Update active product documentation and template references;
retain historical records. Run integrated package/CLI/CI and host qualification.
The installation guide must describe starting before a clone, activating its
actual path, recovering the selection, and using independent parallel sessions.
Distinguish the short plugin bootstrap from the repository-selected instructions.
This is candidate implementation and qualification; do not adopt the new layout
into this repository or delete its installed harness files.

## Execution order

Implement after WO-IAR-028, WO-IAR-029 supplies its tested interface and evidence. This ordering is an execution prerequisite, not an invented graph relation.

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

Execute VER-IAR-022. Starting focused checks: python scripts/run_tests.py; python scripts/validate_release_distributions.py --root .; packaged CLI smoke; focused installer/ownership tests during development and native delivery qualification on the final candidate.
Use the exact installed released 0.20.0 evaluator for repository identity,
validation, start/review preflight and complete Git-derived scope/handoff checks.
Test candidate behavior only through the separate candidate route. For the final integrated record, include all three work orders and verification contracts at one exact candidate. If earlier native or package evidence no longer matches, rerun the affected checks.

## Evidence to record

Retain actual commands, runtime/resource identities, check results, failures and
criterion assessment under docs/engineering/instruction-architecture/evidence/WO-IAR-030/. Use VREC-IAR-020 and its declared evaluator
companion only if that ID remains unused across local refs at capture time.
Do not create a VREC by editing a template. Approval grants preparation of the
named outputs, not acceptance. A conflicting ID requires a reviewed path correction.

## Stop conditions and completion

Stop the affected action for a changed approved contract, out-of-scope path,
missing human decision, integrity mismatch, failing required check or ambiguous
migration input. Preserve evidence and report the exact correction needed.
Report changed behavior, complete file scope, actual tests, remaining limitations,
candidate and evidence identities, and the evaluator's next typed step.
