+++
id = "WO-RLS-053"
type = "work_order"
title = "Fit complete native inputs with a smaller tool guide"
status = "draft"
owners = ["mmzen"]
created = "2026-10-13"
updated = "2026-10-13"

[execution_scope]
paths = ["tests/hosted_artifact_graph/native-tools.md", "tests/hosted_artifact_graph/native-execution-tools.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-RLS-040"]
+++

# Fit complete native inputs with a smaller tool guide

## Objective

Allow the complete positive authoring input to fit the existing 64 KiB limit
for both native hosts at the ordinary qualification paths. Preserve the whole
fixture, applicable instructions, native operation choice and independent review.
Candidate 05c629ddfc0f40924823160d8aaf0fa4e77940a2 passed both missing-input
diagnostics, but its positive test stopped before provider invocation. This work
addresses entry size, not an established positive content or performance result.

## In scope and expected change surface

- `tests/hosted_artifact_graph/native-tools.md`: apply only the reviewed shorter
  guide. Preserve transport restrictions, typed fields, revision reads, discovery
  and observation semantics. Remove duplicate authoring/report policy in favor
  of the already supplied hosted-drafts reference. Route raw requests, lifecycle
  rehearsal and handoff encoding to the existing execution guide before use.
- `tests/hosted_artifact_graph/native-execution-tools.md`: preserve its complete
  existing bytes; append the original raw/lifecycle/encoding paragraphs unchanged,
  with a heading and reading condition. No new file or ordinary drafting read.
- `docs/engineering/release-0-23-0/`: proposal, release index, retained accepted
  bytes, explicit linked release-membership amendment and qualification evidence.
  Fixed handoff/pre-action destinations belong to evidence/WO-RLS-053. Candidate
  package/native evidence stays in evidence/WO-RLS-045 and WO-RLS-046. The final
  aggregate VREC and evaluator sidecar remain in this domain; inspect actual
  generated paths before writing.
- Only after explicit approval, activate the exact one-line REL-SEH-036 revision
  adding WO-RLS-053 to its gates. Preserve its accepted bytes and lifecycle history.

Inspected consumers: `tests/hosted_artifact_graph/qualify_agents.py`,
`native_call.py`, `test_native_support.py`, existing native staging, and the
selected plugin's setup/hosted-context and change/hosted-drafts references.
The existing execution guide is already staged and inventoried. Initial complete
input delivery selects native-tools; its linked execution guide remains available.
No client, service, evaluator, schema, template, plugin package or CI implementation
needs changing. Existing source/package checks and offline full-input assembly
verify this presentation change; no new framework or text-matching test is proposed.
SPEC-HAG-008's existing instruction-routing rules apply; no architecture change.

## Constraints and out of scope

Keep REQ-HAG-014, SPEC-HAG-008, VER-HAG-008 and VER-RLS-040 unchanged. Preserve
the original task, every fixture file, all nine selected positive-case sections,
the selected plugin references, model, permissions and 64 KiB refusal. No expected
answer, shortened source, silent pointer fallback, larger limit or specially short
path. Exact native launch inputs must be measured again; path/selection growth
can consume remaining headroom. Do not claim this works at every possible path.

Keep the WO-RLS-052 content correction and its candidate-bound evidence. The new
guide is another instruction hypothesis until native qualification passes. Do not
silently reuse old diagnostic passes for this new candidate. Git remains authoritative;
the service remains private. Authentication/ACL changes and broad performance work
remain deferred. No host upgrade, restart, global setting or permission expansion.

## Required verification and evidence

Propose required commit-bound verification because release assurance will rely on
the instructions delivered to the native tests. Human confirmation is pending;
use the existing final aggregate VREC, without another assurance layer.

1. Compare each retained guide duty with the review's coverage table. Confirm the
   original raw/lifecycle paragraphs and prior execution guide are preserved.
2. Assemble the actual complete positive entries for both hosts before provider
   launch. Retain source/section/reference identities, byte counts and the unchanged
   overflow refusal. Measure ordinary qualification paths; stop if either exceeds
   65,536 bytes. The offline proposal result does not certify a future candidate.
3. Run existing native input/capture tests, including oversized, missing, tampered,
   duplicate, linked/outside and credential refusal cases. Run required source,
   distribution, installed-package and CLI checks on the exact candidate.
4. Under VER-HAG-008, run a fresh Claude EFF-04A2 diagnostic first. Stop native
   repetitions if it fails. A pass permits the Codex diagnostic with boundary
   probes, one Claude EFF-04B, two more independent correct Claude attempts, then
   Codex EFF-04B. Assess actual content/effects independently; a small input is not
   correctness. Preserve failures and required observation limits.
5. Complete remaining VER-RLS-040 native lifecycle/delivery, walkthrough/restore
   and separate desktop evidence. Reuse evidence only where exact identity and
   the accepted contract permit it. Unperformed checks remain pending.

Retain commands, outputs, failures, timings, call/context observations and exact
Git/package/component identities in the existing release evidence locations.
Do not feed the size review, prior verdicts or expected outputs to native tests.

## Authorized decision envelope

The user's "Ok go" permits preparing and publishing this proposal under the
existing bounded release review grant. WO-RLS-052 permits different exact bytes;
it does not authorize these two test-guide edits. No approval/start is repeated.

Request implementation approval, required verification, and explicit manual
activation of the linked REL-SEH-036 membership amendment. The installed evaluator
has no generic accepted-definition amendment command. Preserve and link previous
accepted bytes/history; do not invent a lifecycle event for the manual amendment.

Approval includes local qualification, evidence, completion/verification preparation
and ordinary review pushes to mmzen/se_harness, codex/release-0-23-0, target main,
draft PR #544, including later separately supplied verification decisions.
Human verification, merge, complete-release approval, desktop omission, adoption
and host updates remain separate. No public delivery/provider change is included.

## Stop and completion

Stop on uncovered paths, input overflow, lost instructions, changed criteria,
diagnostic failure or unavailable required evidence. A further correction requires
its own review. Complete only after required checks pass with retained evidence.
Report actual behavior, failures/limits, lifecycle state and the evaluator's one
typed next step. A proposal, passing size check or green CI is not native acceptance.
