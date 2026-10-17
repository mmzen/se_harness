+++
id = "WO-RLS-052"
type = "work_order"
title = "Ground hosted drafting in confirmed source inputs"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-13"
updated = "2026-10-16"

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
decided_at = "2026-10-13T13:12:42Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" on 2026-10-13 to WO-RLS-052, required commit-bound verification and its linked release-membership amendment, reviewed in PR #544 at 6672142f0901da97942782519d305d028d783222. This authorizes the exact one-file source-grounded drafting correction, bounded local checks and new-candidate qualification under unchanged VER-HAG-008 and VER-RLS-040. It explicitly authorizes the reviewed manual REL-SEH-036 gates amendment, preserving accepted bytes and lifecycle history, and includes this work in the existing review-publication grant for codex/release-0-23-0 to mmzen/se_harness:main, including later separately given verification-decision pushes. Human verification, merge, complete-release approval, desktop omission, adoption and host updates remain separate. Reviewed work-order SHA-256 67473adf749a6754d7e80ad8f47e3a95393675630b52b375e89d8563abba9aeb; instruction before 57a6fb26a8710381620ca0d579c53f442c397db66e2d7be1004db686604b6b64 and after 09912f982b0dbcaadcd3d79f895d91aa83fb3de0f1a32d45f666de8400879be6; release amendment before 141e1708e5a3c6293641f8d09865459444fedd189e984adc0580989ed1fc54e9 and after 3cdd7f1616e9450e9649bccd27d777113bf39d9799297cc6ee34178be41b1f1b."
scope_paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-13T13:15:46Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-16T11:33:44Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Codex records completion of approved local preparation at source bb0890045f462343ecae66ca30b20b06cf6e8ae6. Exact source/package/host/service observations are retained. mmzen directed continuation with R23-NATIVE-010/011 open and desktop deferred/unverified, recorded through DEC-RLS-010/011. No failed or unrun result is a pass. Final committed-candidate build/staging identity, aggregate capture, human verification and release decision remain separate."
+++

# Ground hosted drafting in confirmed source inputs

## Objective

Prevent unsupported interpretations from being reported as supplied inputs or
complete draft content. Address R23-NATIVE-007/008 from candidate
32f2834e82b92e773536808c16b00256ffaae896. The previous table was visible but its
judgments were wrong. This is a new instruction hypothesis, not a proven fix.

## In scope and expected change surface

- `plugins/verity-plane/common/skills/change/references/hosted-drafts.md`:
  replace duplicated routing/readiness text with the existing requester
  confirmation step, followed by direct source support for each required input.
  Distinguish observed behavior, confirmed needs, deductions and proposed limits.
  Separate a baseline from a success condition. Count accepted writes from
  receipts, without treating reads as mutations. Apply only the reviewed bytes
  in evidence/WO-RLS-052/hosted-drafts-proposed.txt.
- `docs/engineering/release-0-23-0/`: draft, review, preserved accepted bytes,
  linked release-membership amendment and required evidence. Fixed generated
  handoff/pre-action packets belong to evidence/WO-RLS-052. Candidate package
  and native evidence remain in evidence/WO-RLS-045 and WO-RLS-046. The later
  aggregate VREC and evaluator sidecar remain in this release domain; inspect
  the actual generated paths before writing.
- Only with explicit approval, amend REL-SEH-036 to add WO-RLS-052 to its gates.
  Preserve the previous accepted file and complete lifecycle history. The exact
  one-line proposed revision is retained; preparation does not apply it.

Inspected consumers are release/plugin-assembly.json,
repository_tools/plugin_distribution.py,
tests/plugin_integration/package_assembly/test_refresh_guidance.py,
tests/test_resources.py, tests/hosted_artifact_graph/test_native_support.py and
tests/hosted_artifact_graph/qualify_agents.py. Both packages deliver the same
shared file. Existing packaging and native-input checks cover delivery; their
code needs no change. No service, schema, evaluator or architecture change is
proposed. SPEC-HAG-008 governs the instruction presentation unchanged.

## Constraints and out of scope

Keep the task, fixture, model, permissions and accepted REQ-HAG-014,
SPEC-HAG-008, VER-HAG-008 and VER-RLS-040 unchanged. Do not provide test answers,
prefill the assessment or turn semantic review into a quote/keyword test.
Direct support still requires semantic judgment. No new approval checkpoint,
tool, runtime, dependency or mandatory repository file is introduced. The
requester-confirmation step already exists; reuse a matching confirmation.
Do not treat every task as incomplete. The positive case must still succeed
when the required inputs and confirmation are present.

The assessment remains transient in conversation or an existing temporary
report. Reuse unchanged sources. Git remains authoritative; the service stays
private. Authentication/ACL changes and broad performance work stay deferred.

## Required verification and evidence

Propose required commit-bound verification because release decisions rely on
the exact delivered instructions and their observed native behavior. Human
confirmation of that classification is pending. Use the existing aggregate
final VREC rather than another assurance layer.

After approval, run applicable existing resource/package and native-input
checks. Build and check the exact candidate packages required by VER-HAG-008.
Run one fresh Claude EFF-04A2 diagnostic with unchanged inputs and criteria.
Inspect its direct source support, requester confirmation, operations, report,
final reply and any saved artifact independently. Quotation or table presence
is not a pass. Read actual service state separately and preserve imported bytes.

A failure stops further native attempts on that candidate. A pass permits the
existing Codex diagnostic and positive EFF-04B sequence. A clarification stop
is a negative-case result, not positive authoring or proven speed improvement.
Required source, installed-package, lifecycle/delivery and separate desktop
checks remain required. Reuse evidence only under the accepted contract's exact
identity comparisons and stated limits.

Retain commands, outcomes, failures, elapsed time, calls, context measurements
and exact candidate/component identities at the existing evidence paths.
Preserve all preceding failed candidates and verdicts.

## Authorized decision envelope

The user's "Ok continue" on 2026-10-13 authorizes preparing the next correction.
It does not approve these new exact bytes. WO-RLS-051 remains in progress and
bound to its failed candidate; do not amend its approved scope or replay start.

Request approval for this exact instruction replacement, local qualification,
evidence, completion and verification preparation. Include bounded review
publication to mmzen/se_harness, branch codex/release-0-23-0, target main, draft
PR #544, including a later separately supplied verification-decision push.

The installed evaluator has no generic accepted-definition amendment command.
Request explicit manual activation of the linked REL-SEH-036 revision adding
only WO-RLS-052. Preserve and link the preceding accepted bytes and history.
Human verification, merge, complete-release approval, desktop omission,
adoption and host updates remain separate. No public delivery or provider
configuration change is authorized by this draft.

## Stop and completion

Stop on another diagnostic failure, unavailable required evidence, changed
accepted behavior or uncovered paths. Complete only after the required checks
pass with retained evidence. Report actual effects, failures, limits, lifecycle
state and the evaluator's typed next step. A further correction needs its own
review; do not respond to failure with another unreviewed wording change.
