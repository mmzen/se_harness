+++
id = "WO-RLS-048"
type = "work_order"
title = "Correct 0.23.0 client admission and release instruction packaging"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-16"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification for client admission, instruction packaging and release membership."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-23-0/", "server/hosted_artifact_graph/service.py", "tests/hosted_artifact_graph/qualify_boundaries.py", "tests/hosted_artifact_graph/test_release_combination.py", "release/plugin-assembly.json", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[relations]
implements = ["REQ-HAG-008", "REQ-PLG-002", "REQ-IAR-030"]
specifications = ["SPEC-HAG-003", "SPEC-PLG-001", "SPEC-IAR-016"]
verification = ["VER-RLS-039", "VER-RLS-040"]
architecture = ["ARCH-HAG-001", "ADR-HAG-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T16:16:57Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the revised WO-RLS-048 review published at 321fe678d982505d55d8531c6ca63fee6b606275. This approves exact 0.23.0 client admission, the ten existing instruction mappings, five named implementation/test paths and release-domain evidence, with required commit-bound verification under VER-RLS-039/040. It explicitly authorizes the linked manual REL-SEH-036 membership amendment, preserving accepted bytes and lifecycle history, and inclusion in the existing review-publication grant for codex/release-0-23-0 to mmzen/se_harness:main, PR #544, including a later separately given verification-decision push. This supersedes the earlier narrow unapproved proposal. Human verification, merge, complete-release approval, adoption and host updates remain separate. Reviewed work-order SHA-256 26304636c8dc58a6d2cbb513107540e66324c8fd57c531d184a2b6aedf2c7b0d; release amendment before 87dba9065a6c855b660e395060e04373378155695bfe6f421374d44e5758cf0f and after fdb373581bd98b334536b9212f72f9d15739d5b20d1834641f48c94ad832f464."
scope_paths = ["docs/engineering/release-0-23-0/", "server/hosted_artifact_graph/service.py", "tests/hosted_artifact_graph/qualify_boundaries.py", "tests/hosted_artifact_graph/test_release_combination.py", "release/plugin-assembly.json", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-12T16:19:50Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-16T11:33:44Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Codex records completion of approved local preparation at source bb0890045f462343ecae66ca30b20b06cf6e8ae6. Exact source/package/host/service observations are retained. mmzen directed continuation with R23-NATIVE-010/011 open and desktop deferred/unverified, recorded through DEC-RLS-010/011. No failed or unrun result is a pass. Final committed-candidate build/staging identity, aggregate capture, human verification and release decision remain separate."
+++

# Correct 0.23.0 client admission and release instruction packaging

## Objective and cause

The approved release uses client 0.23.0, but Service.compatibility still accepts
only 0.22.2. WO-RLS-045 covers the preparation helper and excludes runtime
changes. Its scope inspection missed this second constant. The retained
predicate observation demonstrates the mismatch; it is not a service-test pass.

The fixed release assembly map also omits ten tracked routing/reference files.
Development assembly includes them automatically, but release archives would
contain broken instruction links. The retained inventory and failing composed
link checks show this second scope omission. This expanded draft supersedes
the earlier narrow, unapproved WO-RLS-048 proposal; that proposal is preserved.

## In scope

1. Add exact client 0.23.0 to the service's closed supported-client set. Preserve
   0.22.2 for the existing development combination. Keep the configuration/client
   identity match, wheel digests, plugin 0.2.7, pinned evaluator 0.22.1, image,
   runtime, database, schema, protocol and authority checks unchanged.
2. Test both permitted versions, unsupported versions, configuration/version
   mismatch and wrong component identities. Run actual in-container compatibility
   checks through the existing boundary suite and the new tuple's walkthrough.
3. Add only the ten existing files listed in missing-instruction-files.json to
   release/plugin-assembly.json, using their existing destination paths. Preserve
   all previous mappings. Check that the packaged skill entry points and required
   reference routes resolve in both host packages. Keep exact-source/inventory
   validation; do not replace the fixed map with automatic discovery.
4. Include this work in the final aggregate commit-bound verification using
   existing VER-RLS-039/040. Preserve all previous candidate and evidence bindings.
5. If separately and explicitly approved with this work, apply only the linked
   REL-SEH-036 amendment that adds WO-RLS-048 to release membership. Preserve the
   complete accepted bytes and lifecycle history and retain the amendment's human
   reason and before/after digests. The installed evaluator has no generic
   accepted-definition amendment command; this is a bounded manual activation,
   not a general bypass or a new lifecycle rule.

## Expected change surface

| Path | Purpose |
| --- | --- |
| server/hosted_artifact_graph/service.py | Admit the exact new client version while preserving other tuple checks. |
| tests/hosted_artifact_graph/qualify_boundaries.py | Actual service compatibility success and refusal checks in the existing qualified container. |
| tests/hosted_artifact_graph/test_release_combination.py | Deterministic helper/client boundary coverage alongside WO-RLS-045. |
| release/plugin-assembly.json | Add the ten reviewed existing instruction assets to both host release packages. |
| tests/plugin_integration/package_assembly/test_refresh_guidance.py | Check required route inclusion and composed instruction links. |
| docs/engineering/release-0-23-0/ | The exact linked release-membership amendment, proposal, checks, aggregate verification and generated evidence sidecars. |

No new instruction content or package-builder/publisher behavior is proposed.
No API, schema, protocol, dependency, source-import, storage, authentication or
database ACL change is included. Keep Git authoritative and the service private.
No new verification contract is needed: the accepted release contracts already
require this exact combination and its compatibility refusals. Do not weaken them.

## Verification and authority

Required commit-bound verification is proposed because the release and service
readiness depend on the runtime admission checks. The human must confirm it
before approval. Work approval permits the bounded local implementation, tests,
evidence, completion and aggregate verification preparation.

Request inclusion of this correction in the existing review-publication grant
for codex/release-0-23-0 to mmzen/se_harness:main, including the later separately
given verification decision. Human verification, merge, complete-release approval,
adoption and host updates remain separate. The linked manual amendment requires
its explicit matching authorization; this draft does not apply it.

## Completion and stop

Both declared clients pass their actual matching tuple. An unsupported version,
mismatched configuration or changed required identity remains refused. The final
0.23.0 packaged walkthrough and applicable native cases pass under VER-RLS-040.
Record actual commands, results, failures and component digests under this
release domain. Stop affected work if a wider runtime or contract change is needed.
