+++
id = "WO-RLS-054"
type = "work_order"
title = "Discover communication instructions before hosted explanations"
status = "draft"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/setup/references/hosted-context.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-HAG-007", "VER-RLS-040"]
+++

# Discover communication instructions before hosted explanations

## Objective

Make the existing communication prerequisite discoverable before the first
English explanation on the explicit hosted route. At candidate a98a1571,
both full native runs read it late: Claude events 25 then 182; Codex 23 then 54.
Their functional lifecycle, seven graph reads and exported records pass independent
assessment. This proposal does not convert those timing observations to passes.

## In scope and expected change surface

- `plugins/verity-plane/common/skills/setup/references/hosted-context.md`: apply
  only the proposed short early pointer in evidence/WO-RLS-054/hosted-context.patch.
  Keep the policy in its released resource and reuse complete content already
  supplied. Both hosts read this route before their observed first explanation.
- `docs/engineering/release-0-23-0/`: review, retained accepted bytes, exact linked
  membership amendment, qualification, and the existing final aggregate VREC.
  Keep fixed handoff/pre-action outputs under evidence/WO-RLS-054; actual package
  and native evidence remain under evidence/WO-RLS-045 and WO-RLS-046.
- After explicit approval only, apply the exact REL-SEH-036 gates amendment
  adding WO-RLS-054. Preserve accepted bytes and lifecycle history. The released
  evaluator has no generic amendment command; manual activation needs approval.

Inspected consumers are setup/SKILL.md, hosted-context.md, the released
COMMUNICATION/root routing, native task entry, both actual event streams and
the package assembly path. No new tool, lifecycle, policy edition or ordinary
artifact is needed. Existing package and native checks cover the changed route;
no text-matching regression test or new framework is proposed. No architecture
or behavior change beyond instruction reading order applies.

## Constraints and out of scope

Keep accepted REQ/SPEC/VER meaning, task, fixture, model, permissions, native
choice, 64 KiB limit and evidence criteria. No retry-to-pass, expected answer,
policy waiver, larger budget, source summary or silent input fallback.
Preserve all prior failed candidates. No host-global update, current app restart,
public service, authentication/ACL change or broad performance work.
Desktop remains required separately; no previous-release omission applies.

## Authorized decision envelope

This is an unapplied proposal. Request exact implementation and required
commit-bound verification, plus manual activation of the linked membership
revision. Proposed assurance is required because release decisions depend on
the instruction discovery and its evidence. Do not fill decided_by before the
human confirms it. Reuse the final aggregate VREC, not a new assurance layer.

Approval may include bounded local checks and qualification and ordinary review
pushes to mmzen/se_harness, codex/release-0-23-0, target main, draft PR #544,
including the ready record and a later separately supplied verification decision.
Verification acceptance, merge, complete release, desktop omission, adoption and
host updates remain separate. No approved file is amended by drafting this WO.

## Required verification and evidence

Compare exact before/proposed bytes and confirm the existing policy is referenced,
not duplicated. Run applicable package, source and complete-input checks. The
extra pointer changes packaged input size; remeasure both focused entries before
provider launch. Stop on overflow, without truncating or changing the limit.

Run affected native qualification with final packaged guidance under unchanged
VER-HAG-007/008 and VER-RLS-040. Establish the first communication read before the
first eligible explanation from actual events. Retain full functional and export
results; do not claim current qualification from changed instruction bytes alone.
Apply the existing diagnostic-first/positive sequence and remaining delivery
criteria; skipped or unperformed tests remain pending. Reuse only results whose
exact inputs and governing contracts permit reuse, with an explicit comparison.

Retain exact commands, exits, failures, actual package/component/model identities,
input hashes, content assessments and elapsed/call/context observations. Keep
private reasoning, credentials, profiles and temporary working notes out of Git.
Assess future generated verification destinations before writing them.

## Stop and completion

Stop affected work on uncovered paths, instruction gaps, input overflow, failed
diagnostic, missing required evidence or changed authority. Complete only after
the required checks and retained evidence satisfy the contracts. Report actual
effects, remaining limitations, unchanged/updated state and the evaluator's one
typed next step. Green CI and draft admission do not accept the native result.
