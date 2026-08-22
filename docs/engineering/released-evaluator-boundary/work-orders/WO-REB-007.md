+++
id = "WO-REB-007"
type = "work_order"
title = "Implement hosted predecessor assessment and portable failure injection"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Release decisions will rely on a new candidate-owned hosted lane mediating an immutable predecessor evaluator, exact expected-failure matching, Git view provenance, and cross-platform rollback evidence."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-013", "REQ-REB-014"]
specifications = ["SPEC-REB-006"]
architecture = ["ARCH-REB-005", "ADR-REB-005"]
verification = ["VER-REB-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T07:15:03Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement hosted predecessor assessment and portable failure injection

## Lifecycle

The accountable owners approved the seven-artifact corrective packet and started this work order for bounded local implementation and qualification. Candidate commit, branch/credentials, hosted dispatch, lifecycle disposition, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, and root-evaluator upgrade remain separate accountable actions.

## Objective

Close the two C4 hosted failures without rewriting history, upgrading released 0.5.0, changing root-managed state, or misrepresenting the predecessor's full-graph capability.

## In scope

- Retain exact C4 run/job/log identities and classify the `E009` and Linux `dir_fd` failures separately.
- Refactor view derivation so preparation and hosted assessment share the exact closed-pair/Git/path/isolation core.
- Add one read-only candidate-owned hosted workflow for exact released-0.5 assessment against the derived view.
- Require exact matching of the unchanged legacy workflow's sole `E009` result; fail on any other diagnostic or earlier boundary failure.
- Emit and independently replay canonical `se-harness-predecessor-assessment-view-v1` evidence.
- Introduce an adapter-local exclusive-create seam and update fault injection to patch only that seam.
- Add diagnostic, path, Git, runtime, canonical-evidence, cleanup, Linux/Windows, workflow, and no-mutation tests from `VER-REB-005`.
- Retain complete evidence suitable for a later fourteen-work-order C5 aggregate.

## Out of scope

- Editing, deleting, relocating, renumbering, repointing, or reinterpreting any C1-C4 candidate, VREC, RLS, REL, rejected history, or retained evidence.
- Modifying `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, other root-managed paths, released 0.5.0, or maintenance state.
- Marking the legacy workflow green, changing external required checks/policy, disabling a workflow, or accepting generic CI failure.
- Dispositioning `REL-SEH-010`, approving `REL-SEH-011`, transitioning `WO-REB-006`, or preparing/transitioning any VREC/RLS under this work order.
- Creating a candidate commit, pushing, using credentials, dispatching hosted lanes, tagging, publishing, or deploying without separate authority.

## Authorized decision envelope

After explicit approval and work start, implementation may choose internal module/helper names, assessment artifact display names, and temporary-directory names. It may not change the exact rejected pair, required commands, diagnostic closure, root/history preservation, evaluator identity, canonical schema obligations, or dual-plane trust statement.

## Constraints

- Preserve Python 3.11+ standard-library compatibility on Linux and Windows.
- Use only standard-library/product dependencies already in scope.
- Treat Git, paths, logs, artifacts, workflow context, environment, evaluator bytes, and output as untrusted.
- Use runner-temporary output outside the source checkout and prove recursive source no-change.
- Never claim the predecessor validated the complete graph.

## Expected change surface

- Shared repository-owned predecessor view/assessment implementation and one CLI script.
- One new non-managed hosted assessment workflow; existing managed workflow remains byte-identical.
- Focused predecessor preparation/assessment, workflow, Linux cleanup, and complete regression tests.
- Operator/release documentation and one `WO-REB-007` evidence file.
- Draft successor `REL-SEH-011` remains governance-only until separately approved.

## Required verification

- Execute every method in `VER-REB-005` plus unchanged `VER-REB-004` regressions.
- Reproduce both C4 hosted failures before correction.
- Prove local exact released-0.5 view assessment and complete candidate validation.
- Run focused and complete suites on Python 3.11/Linux and the current Windows runtime.
- Prove workflow static security, canonical evidence determinism, no checkout mutation, zero root/history diff, and exact legacy diagnostic matching.
- After separate candidate/branch authority, pass candidate-source, candidate-package, and new predecessor-assessment jobs at exact C5 while retaining the expected legacy refusal.

## Evidence to record

- C4/candidate/governance/branch identities and both failed run/job URLs/logs.
- Exact legacy evaluator identity, commands, successful pre-failure steps, `E009`, and Linux tracebacks.
- Prototype and final view commits/trees/specifications, omitted blob/raw hashes, graph counts, output hashes, and evaluator tuple.
- Fault seam code path, flags/mode, injected-call matrix, cleanup observations, and before/after maps.
- C5 changed paths, exact local/hosted/build/package identities, and root/history hashes.
- Exact list of actions not performed.

## Stop and escalate conditions

- The old workflow cannot be matched without a generic failure waiver.
- Assessment needs any omission beyond the exact pair or any root-managed/external-policy change.
- Candidate orchestration can select commands/paths or alter predecessor outputs.
- Linux/Windows rollback or cleanup differs materially.
- Any protected history, root evaluator, lock, maintenance state, credential, or external system must change outside separately granted authority.

## Completion report format

Report both C4 failures, selected trust model, assessment schema/commands/view, fault-seam correction, changed surfaces, exact local/hosted results, C5 identity when separately authorized, preserved histories/root state, lifecycle states, and one next accountable decision.
