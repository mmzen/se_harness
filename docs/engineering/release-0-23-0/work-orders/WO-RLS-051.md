+++
id = "WO-RLS-051"
type = "work_order"
title = "Assess supplied inputs before hosted drafting"
status = "draft"
owners = ["mmzen"]
created = "2026-10-13"
updated = "2026-10-13"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-RLS-040"]
+++

# Assess supplied inputs before hosted drafting

## Objective

Make the agent expose missing required inputs before authoring, and use the
same assessment when reporting content readiness. Address R23-NATIVE-005/006
from candidate 74feac0767f33658b31fb9e9ad2b6a13a188c13c. A saved draft must not
be called complete while required inputs are missing or claims lack support.
This is an instruction hypothesis to qualify, not an established fix.

## In scope and expected change surface

- `plugins/verity-plane/common/skills/change/references/hosted-drafts.md`:
  replace the passive readiness table with a visible input assessment before
  drafting. Each required item names its supplied fact/source or missing input
  and question. Reuse that assessment after saving and in the final report.
  Mark proposed scope limits consistently in the draft and report. Exact
  proposed bytes are in evidence/WO-RLS-051/hosted-drafts-proposed.txt.
- `docs/engineering/release-0-23-0/`: the proposal, preserved versions, review,
  exact candidate checks, native observations and aggregate verification.
  Fixed handoff/pre-action packets belong to the selected work order's evidence
  directory. Qualification stays in evidence/WO-RLS-045 and WO-RLS-046. The
  aggregate VREC and evaluator sidecar are allocated later in this release
  domain; check their returned paths before writing.
- With explicit human authorization, add only WO-RLS-051 to the gates of
  REL-SEH-036, linking and preserving its complete preceding accepted bytes
  and lifecycle history. This proposal leaves that record unchanged.

Inspected consumers: release/plugin-assembly.json includes this exact shared
file in both packages; repository_tools/plugin_distribution.py verifies them.
tests/plugin_integration/package_assembly/test_refresh_guidance.py,
tests/test_resources.py and tests/hosted_artifact_graph/test_native_support.py
cover resource, packaging and native-input delivery. qualify_agents.py delivers
the same selected file. No consumer, service, runtime or schema change is needed.
SPEC-HAG-008 already governs this instruction presentation; its architecture
boundary and accepted content criteria stay unchanged.

## Constraints and out of scope

Do not change the test request, fixture, model, permissions, accepted
SPEC-HAG-008/VER-HAG-008, evaluator policy, content requirements or thresholds.
Do not prefill the assessment, supply the diagnostic's missing answers, add a
second evaluator or convert semantic review into a keyword check. No extra
tool, mandatory repository file, lifecycle checkpoint or approval is introduced
for the native agent. The assessment lives in conversation or an existing
temporary report. Do not invent an audience, problem, benefit, measure or limit.
Broad performance work remains deferred; any speed benefit must be measured.
Git remains authoritative and the service stays private.

## Required verification and evidence

Propose required commit-bound verification: release decisions depend on the
correctness of these instructions and their observed native behavior. Human
confirmation of that classification is pending. Include this work in the existing
aggregate final VREC, without a separate assurance layer.

After the exact approved edit, run applicable existing resource/package and
native-input checks. Build and test the exact candidate packages required by
VER-HAG-008 before native execution. Run one fresh Claude EFF-04A2 diagnostic
with the same request, fixture, model and permissions. Independently inspect the
input assessment, actual calls, report, final reply and any saved artifact.
Assess correctness under the existing contract, not by table presence alone.
Retain original imported bytes and read saved state separately.

A failure stops further native repetitions on that candidate. A pass permits
the existing Codex diagnostic and positive-case sequence. Defer broader native
qualification until that first diagnostic passes. Reuse earlier service evidence
only with the exact comparisons and limits permitted by its contract. Required
source, package, lifecycle/delivery and separate desktop checks remain required.

Retain commands, results, failures, durations, calls, context measurements and
candidate/component identities at this release's existing evidence locations.
All earlier failed candidates retain their verdicts. An incomplete draft or
clarification stop is not successful positive authoring or a general speed claim.

## Authorized decision envelope

The user confirmed the proposed approach with "Ok go" on 2026-10-13. This permits
preparation; approval of this exact work order and required verification remains
pending. WO-RLS-050 binds a different edit and is not reinterpreted here.

Requested approval covers the exact instruction replacement, local checks,
qualification, evidence, completion and verification preparation. It includes
review publication to mmzen/se_harness, source codex/release-0-23-0, target main,
PR #544, including a later separately given verification-decision push.

The installed evaluator has no generic accepted-definition amendment operation.
Request explicit manual activation of the exact linked REL-SEH-036 revision
adding only WO-RLS-051. Preserve the preceding complete file and lifecycle history.
Human verification, merge, complete-release approval, desktop omission, adoption
and host updates remain separate. No public delivery or provider-setting change.

## Completion and stop

Complete only after the approved correction and required independent checks pass
with evidence. Stop on another diagnostic failure, changed required behavior,
uncovered paths or unavailable required evidence. Report actual effects, checks,
limits and the released evaluator's typed next step. Do not ask for an extra
completion decision within unchanged approved execution.
