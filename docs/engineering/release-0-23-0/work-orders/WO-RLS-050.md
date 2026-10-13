+++
id = "WO-RLS-050"
type = "work_order"
title = "Unify hosted draft content-readiness guidance"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-13"
updated = "2026-10-13"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release decisions depend on exact instructions and their independently observed native behavior."
decided_by = "mmzen"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-RLS-040"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-13T06:03:03Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" on 2026-10-13 to WO-RLS-050, required commit-bound verification and its linked release-membership amendment, reviewed in PR #544 at b5a6b1eb3aa6747ce10b7b48024561ad68d2bcf2. This authorizes the exact one-file hosted-drafts instruction correction, bounded local checks and new-candidate qualification under unchanged VER-HAG-008 and VER-RLS-040. It explicitly authorizes the reviewed manual REL-SEH-036 gates amendment, preserving accepted bytes and lifecycle history, and includes this work in the existing review-publication grant for codex/release-0-23-0 to mmzen/se_harness:main, including later separately given verification-decision pushes. Human verification, merge, complete-release approval, desktop omission, adoption and host updates remain separate. Reviewed work-order SHA-256 7002a8faea25d368413206acb50b4b27c94a38549abbb79354fbd5cb9a3e5969; instruction before cdd3d9f13a7998a36ff5f2c293dff8dad6f61c54997f69f41edd48c6b096c23e and after 669c9f141f4d219aab1ad2b90f29c610e1e1a91280be87e6d7f34f9c1f7071cf; release amendment before e56efa4b4b4a2e5045db06e68995423f3ddbb7b2bcebd0a9d6d6ccdc543d2c2c and after 609e424ba14cde14ef45ffb4e432972fe6c36b56a22623edea08611eb1a5010b."
scope_paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-13T06:07:01Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Unify hosted draft content-readiness guidance

## Objective

Make the existing distinction between a saved draft and complete content clear
at the authoring decision and in the final report. Address R23-NATIVE-003/004
from candidate f2ddb5afe42d40cc7c4a426b5c9cb985156a28a3 without changing the
accepted content criteria. The observed failure remains failed.

## In scope and expected change surface

- `plugins/verity-plane/common/skills/change/references/hosted-drafts.md`:
  replace scattered readiness guidance with one decision table and references
  to it. Missing required inputs leave content incomplete. Unsupported problem,
  outcome, measure or scope statements cannot fill that gap. The exact proposed
  bytes and diff are retained in evidence/WO-RLS-050/; this draft does not apply them.
- `docs/engineering/release-0-23-0/`: this proposal, preserved accepted versions,
  exact checks, new candidate qualification, generated handoff/pre-action and
  aggregate verification outputs. This existing release evidence domain covers
  fixed evaluator sidecars and the aggregate VREC whose ID is allocated later.
  With explicit human authorization, add only WO-RLS-050 to REL-SEH-036.gates.

Inspected consumers: the change skill's existing hosted route, the fixed shared
map in release/plugin-assembly.json, repository_tools/plugin_distribution.py,
tests/plugin_integration/package_assembly/test_refresh_guidance.py,
tests/hosted_artifact_graph/qualify_agents.py and test_native_support.py, and
tests/test_resources.py. Both packages already include this file and native
complete-input delivery includes its exact bytes. Those consumers need no edit.
Run their existing applicable checks. No new runtime, parser, dependency,
endpoint, test helper or architecture decision is needed; SPEC-HAG-008 governs
the unchanged design. Existing required verification covers the behavioral outcome.

## Out of scope and constraints

No changes to evaluator policy, task, fixture, model, permissions, accepted
SPEC-HAG-008/VER-HAG-008 content, acceptance criteria or qualification thresholds.
Do not supply the diagnostic's missing answers, weaken a failure, discard prior
trials or retry the failed candidate until a pass. Keep failures visible. Broad
performance work stays deferred; this proposal claims no measured speedup.
Git remains authoritative and the service remains private.

## Required verification and evidence

Required commit-bound verification is proposed; the human must confirm it before
approval. Include this work in the existing aggregate final verification record,
without a duplicate assurance layer. Use VER-HAG-008 and VER-RLS-040 unchanged.

After applying the approved exact edit, check the existing package routes and
instruction/input fidelity. Build and identify the new exact candidate. First
run one fresh Claude EFF-04A2 diagnostic with the same requested outcome, model,
fixture and permissions. Independently assess the report, actual calls and saved
state. A failure stops further native repetitions on that candidate. After a
pass, continue the required Codex boundary/diagnostic and positive-case sequence.
The full lifecycle/delivery checks and separate desktop criterion still apply.

Retain actual commands, outcomes, failures, independent reads, timings and exact
source/package identities at this release's existing evidence locations. Reuse
earlier evidence only where its contract permits and exact applicability is
demonstrated. Complete unaffected release checks under the existing work orders.

## Authorized decision envelope

This draft authorizes nothing. Requested approval permits the exact instruction
edit, bounded local checks, evidence, completion and verification preparation.
It includes the existing review-publication destination: mmzen/se_harness,
codex/release-0-23-0 to main, PR #544, and later separately given verification-
decision pushes. No public release or merge is authorized here.

The evaluator has no generic accepted-definition amendment command. Request
explicit manual activation of the reviewed REL-SEH-036 membership revision,
linked to preserved accepted bytes and retaining lifecycle history. Only its
gates list gains WO-RLS-050. Historical evidence retains its original references.
Human verification, merge, complete-release approval, desktop omission, adoption
and host updates remain separate.

## Completion and stop

Complete after the exact instruction correction and required independent checks
pass with retained evidence. Stop on another diagnostic failure, changed required
behavior, uncovered paths or unavailable required evidence. Report actual effects,
checks, limits and the released evaluator's next step. Do not add a separate
owner completion decision for already approved execution.
