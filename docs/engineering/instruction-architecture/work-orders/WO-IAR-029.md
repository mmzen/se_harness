+++
id = "WO-IAR-029"
type = "work_order"
title = "Connect both host plugins to pinned external resources"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification with package approval. Later agent, CI and installation decisions rely on these instructions, selectors and integrity checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "plugins/verity-plane/common/",
  "plugins/verity-plane/codex/",
  "plugins/verity-plane/claude-code/",
  "release/plugin-assembly.json",
  "repository_tools/plugin_distribution.py",
  "tests/plugin_integration/progressive_discovery/",
  "tests/plugin_integration/package_assembly/",
  "tests/plugin_integration/onboarding/",
  "tests/plugin_integration/repository_connection/",
  "tests/plugin_integration/test_simple_plugin.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-029.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-019.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-019-evaluator.json",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-029/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-030"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 3ced2cb314f96500ab5317ba58466d3bbe197fa1f4ab0dc83302aad51beaf6d2. Only the confirmed assurance metadata and its explanatory paragraph were completed before preview."
scope_paths = ["plugins/verity-plane/common/", "plugins/verity-plane/codex/", "plugins/verity-plane/claude-code/", "release/plugin-assembly.json", "repository_tools/plugin_distribution.py", "tests/plugin_integration/progressive_discovery/", "tests/plugin_integration/package_assembly/", "tests/plugin_integration/onboarding/", "tests/plugin_integration/repository_connection/", "tests/plugin_integration/test_simple_plugin.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-029.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-019.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-019-evaluator.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-029/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T12:21:44Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Connect both host plugins to pinned external resources

## Objective

Use the preceding resource contract to update setup, skills and native hooks.
Retain separate private environments for distinct selected releases and support
the existing 0.20.0 root delivery. Build Codex and Claude packages with the existing
assembly tool. Add the short bootstrap, immediate checkout activation and local
session selection described in IAR-EXT-011 through IAR-EXT-013. Demonstrate the
clone-after-startup cycle, native compaction/resume, parallel session isolation,
repository switching and the existing delivery-authority handoff with temporary
repositories. Do not introduce another policy copy or modify saved user settings.

## Execution order

Implement after WO-IAR-028 supplies its tested interface and evidence. This ordering is an execution prerequisite, not an invented graph relation.

## In scope and change surface

The execution_scope paths above are the complete allowed surface. Directory
prefixes cover only the named component. New files are permitted only where
the declared contract requires them. Template source changes affect future
packages; they do not authorize changing this repository's installed copies.
Shared file overlap is intentional and sequential: resource support first,
host adapter next, then default installation and integrated migration.

The existing plugin component prefixes cover the shared bootstrap text, activation
helper, local record handling, safe evaluator preparation, host adapters and skill
instructions. Extend the listed native-delivery and repository-connection runners
for the agreed scenarios. Use isolated temporary session records and environments
for qualification. No separate service, global last-used repository, descendant
scan or new Git/PR implementation is in scope.

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

Execute VER-IAR-021. Starting focused checks: Use the existing tests/plugin_integration/progressive_discovery, package_assembly, onboarding and repository_connection runners; retain their exact invocation and native traces.
Include actual Codex Windows desktop and Claude Code delivery, manual and automatic
compaction, and simultaneous sessions. Bind those claims to observed host versions
and exact candidate resources. A missing native observation remains unassessed.
Use the exact installed released 0.20.0 evaluator for repository identity,
validation, start/review preflight and complete Git-derived scope/handoff checks.
Test candidate behavior only through the separate candidate route. Prepare this work order's record at its exact candidate. Later combined qualification does not erase earlier results.

## Evidence to record

Retain actual commands, runtime/resource identities, check results, failures and
criterion assessment under docs/engineering/instruction-architecture/evidence/WO-IAR-029/. Use VREC-IAR-019 and its declared evaluator
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
