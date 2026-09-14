# One execution route

Proposal for discussion · 14 September 2026 · No implementation or lifecycle decision in this report.

PR #474 is merged. This review uses main at `001612615191`; its file tree matches the reviewed checkout.

**Recommendation: approving a work order should authorize its routine execution. Make this the single execution procedure, without a separate delegation option.** Keep owner approval of scope, acceptance of the result and delivery decisions explicit.

## What needs challenging

| Interpretation | Recommendation | Why |
| --- | --- | --- |
| Make delegated execution the default but keep the other route | Go further: remove the route choice | A default setting would leave two procedures, fallback logic and two sets of instructions to maintain. |
| Require a separate AI agent for every work order | Do not require this | Delegation is permission to execute. A person or agent can be the executor; a second process, task or model is unnecessary. |
| Let the executor approve its own result | Keep the accountable acceptance decision | Completing the work and accepting its correctness are different responsibilities. Project policy can require different people without creating another execution route. |
| Approve a packet and immediately start every work order | Execute only the selected, eligible work | Approval grants scope. It does not choose priorities, ignore dependencies or start parallel work. |
| Require a VREC for every task | Follow the existing assurance classification | Routine execution should prepare a VREC when required, not invent one for work that does not need it. |
| Add switches for manual mode, strict mode or alternate delegation classes | Omit them | No present need for these variants has been established. |

## The proposed experience

**Owner approves scope → executor starts, implements, checks and records completion → executor prepares required verification evidence → owner accepts or rejects → authorized delivery.**

The executor continues the selected approved work without asking again to start it, mark it implemented or prepare its VREC. Each state change is still applied and recorded when it actually happens. Approval itself leaves the work order approved until execution starts.

Example: you approve a work order to simplify a hook. The executor performs the change, runs the agreed checks, records completion and prepares the verification record. The next request to you is to accept the result. If the solution needs a new behavior outside the approved scope, you decide that change. A failed test is repaired within scope; it is not converted into a fresh permission request.

Routine local edits, tests, evidence and commits should be covered by execution approval. Push and PR creation can also be authorized upfront when their action and destination are specified. Do not ask twice for an unchanged authorization. Verification alone does not authorize merge, release or publication.

## What the code says today

| Finding | Evidence | Consequence |
| --- | --- | --- |
| Candidate delegation is already local | [Local approval check](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/se_harness/gate_source.py#L77) and [DR-015](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/templates/repository/standard/docs/engineering/DECISION_RIGHTS.md#L79) | The earlier KISS work removed the preliminary merge and live CI requirement from candidate execution. Retain that improvement. |
| Delegation still requires an optional work-order class | [Work-order template](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md#L21) | An approved task can still fall onto the owner-operated route simply because the table is absent. |
| The executor command is applied as an overlay to an owner-oriented result | [Delegation overlay](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/se_harness/gate_source.py#L94) | Removing the route split should remove the fallback and overlay, while retaining the common approval and scope checks. |
| Candidate policy and instructions disagree | [Current candidate policy](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/templates/repository/standard/docs/engineering/DECISION_RIGHTS.md#L79), [Old template wording](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md#L49), [Change skill](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/plugins/verity-plane/common/skills/change/references/work-orders.md#L60), [Evidence skill](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/plugins/verity-plane/common/skills/evidence/references/records.md#L53) | The template and skills still describe the old PR-base and live-CI requirements. They can reintroduce unnecessary interruptions even after the code is simplified. |
| Delegated VREC preparation is restricted to one WO | [Preparation split](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/se_harness/provenance.py#L453) | Remove this actor-specific restriction. Preserve the existing selected-WO list and check approval and evidence for every selected WO. Do not add a new batching feature. |
| This repository still uses released 0.17.0 | [Installed version](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/.engineering-harness.toml#L1) versus [Candidate version](https://github.com/mmzen/se_harness/blob/001612615191da499775cebb1a59f65480e9ce4a/pyproject.toml#L7) | Merging candidate changes does not activate them in this repository. Release and adoption remain necessary before the new procedure governs its own development. |

## Proposed shared wording

> Approving a work order authorizes execution of its approved scope, including start, implementation, required checks, evidence capture, completion recording and required verification-record preparation. The executor continues that work without further permission for these steps while the approved scope and applicable conditions remain satisfied. The executor records the work actually performed under its own identity. Scope changes, acceptance of the result and external delivery remain with the accountable owners unless the specific delivery action is already authorized.

Keep this rule in `DECISION_RIGHTS.md`. Put the ordered procedure and executor next actions in `WORKFLOW.json`, with its human explanation in `WORKFLOW.md`. The work-order template makes the effect of approval clear. The change and evidence skills refer to these installed rules rather than reproducing version-specific authorization logic.

This does require an explicit amendment to today's rule that earlier actions grant no later authority: work-order approval will expressly grant the named execution operations. It must not remain an inference made only by a skill.

## One bounded implementation work order

1. Amend the applicable requirements, specification, decision-right policy and workflow contract together. Make execution approval a clear part of WO approval. Keep owner acceptance and delivery rights separate.
2. Replace optional delegation with one executor procedure. Remove the new-work-order delegation table, route selection and owner-route fallback. Reuse the current local approval, scope and evidence checks for every executor; do not simply delete their enforcement.
3. Reuse the existing transition and capture commands. Keep actual actor attribution. A human running those commands follows the same procedure as an agent; there is no human-only override or requirement to launch a subagent.
4. Remove the delegated-only one-WO capture limit and use the common checks for each explicitly selected WO. Preserve the verification behavior already supported for that set.
5. Update templates, both skills' references and current operator notes together. Remove stale PR-base and live-CI instructions. Skills ask for the actual missing decision only; they do not invent a second permission system.
6. Replace tests of the two execution routes with tests of the agreed outcomes. Reuse the existing test suite and CI; add no workflow, receipt, signature or execution-mode setting.

The implementation should reduce maintained branches and instructions. Renaming delegation, setting it to true by default or keeping an owner fallback would not meet this proposal.

## Check the behavior, not every branch

| Situation | Expected result |
| --- | --- |
| Selected WO is approved; applicable local checks pass; GitHub is unavailable | Execution can start, complete and prepare required verification without another owner prompt or network authorization. |
| Approval is missing, approved scope has changed, or a required local check fails | The affected operation does not proceed; it reports the actual missing approval or failed condition, without offering a second route around it. |
| A person runs the supported execution commands | The same approval, scope and evidence rules apply, with truthful attribution. |
| Preparation explicitly covers several eligible WOs | Check every selected WO under the same rule; no actor-specific one-WO restriction. |
| Work is complete but owner acceptance is absent | Completion and preparation do not claim verification, merge, release or publication. |
| Old decisions and evidence are inspected | Their recorded meaning remains unchanged. |

Skill review should also demonstrate the ordinary sequence without redundant start, completion or preparation questions. This is a focused behavior check using the existing skill test approach, not a new conversation-testing system.

## Adoption without a second permanent route

Apply the new approval meaning prospectively. Keep historical delegation fields readable, but omit them from new templates. Do not rewrite old approvals or silently expand what they granted. Any unfinished work approved under the old contract can have its remaining scope expressly approved under the new one through the existing amendment process.

Use the currently installed evaluator while implementing this proposal. Ship the coherent code, policy, template and skill change, then adopt that release through the normal authorized process. The candidate should contain one execution route; old released versions are not a reason to retain a parallel legacy engine inside it.

**Suggested next step:** approve this scope, then prepare one implementation work order. This proposal does not yet allocate an artifact ID, change product files or authorize release/adoption.
