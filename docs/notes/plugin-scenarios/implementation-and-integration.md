# Implementation and integration scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Part of the [scenario guide](README.md), using the [scenario template](../plugin-scenario-template.md). See the [operation overview](../plugin-operation-workflows-2026-09-06.md) for the shared component model.

**Review date:** 2026-09-06. **Source baseline:** [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; the repository's governing evaluator is 0.15.0. The mappings below come from source and policy inspection. Native plugin workflows and compatibility with the released evaluator have not been integration-tested.

These scenarios propose plugin behavior; they grant no work or decision authority. **Reuse** means an existing responsibility or implementation is retained; **Adapt** means it needs changes; **New** means it is missing; **Not used** means the scenario does not need it. Commands mentioned below describe inspected interfaces. The proposed launcher would select a trusted external evaluator, and the bridge would invoke it with structured arguments.

A *work order* (WO) defines authorized work. A *verification record* (VREC) connects evidence to an exact candidate commit. All example results are illustrative, not reports of executed work.

## Scenario 9: Start a work order

### 1. Purpose and starting point

**Purpose:** Establish that an agent may begin one approved work order.

- **Starts when:** The user requests the start of a selected WO.
- **Requires:** An approved WO, its governing documents, and a working evaluator.
- **Successful result:** The authorized transition changes that WO to `in_progress`.

### 2. Workflow

```text
Select the approved WO
        ↓
Read required context and check readiness
        ↓
Human start decision or proven delegated route
        ↓
Apply the start transition and report its result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Agent using the change skill | Select the WO and read the operating card and phase reading manifest. |
| 2 | Bridge and evaluator | Project the selected work and run start preflight. Return blockers or the permitted next step. |
| 3 | Engineering owner or eligible delegate | Authorize the start through the route returned by the evaluator. |
| 4 | Bridge | Preview and apply the explicit transition, then read the resulting state. |

Passing preflight alone does not start work. Execution delegation must exist at the PR base, with the required CI check passing for the exact candidate head. A delegation added only on the working branch cannot authorize itself.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide selection and explain the start decision. | **New:** change skill follows `PROC-WO-START`. |
| **Hook** | Check a supported start invocation. | **New:** before-tool registration calls the shared bridge. |
| **Script** | Select runtime and pass bounded arguments. | **New:** launcher and bridge wrap existing commands. |
| **Tool/interface** | Expose start checks and explicit transitions. | **Adapt:** CLI becomes a structured plugin operation. |
| **Evaluator** | Check readiness and apply the legal transition. | **Reuse:** `preflight`, `transition`, and delegation checks. |
| **Subagent** | Not used. | **Not used:** start needs no separate worker. |
| **Human** | Make the engineering start decision when due. | **Reuse:** `DR-WO-START`; trusted decision capture is new. |
| **External control** | Supply live CI facts for delegation. | **Reuse:** CI-provider checks; these grant no Git authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Integrity or prerequisites fail. | Evaluator refuses the transition; WO stays approved. | Correct within authorized scope, then repeat preflight. |
| Delegation is absent or its CI gate fails. | Delegated start is refused. | Follow the evaluator's corrective or human-decision route. |
| A start decision is pending. | Bridge presents the selected WO and waits before apply. | Capture the engineering owner's exact decision and refresh checks. |

An actor-name argument records an assertion; it does not authenticate the owner.

### 5. Example result

> Illustrative: WO-DEMO-009 is now `in_progress` following the authorized start transition. Related artifacts are unchanged. Next: implement the approved scope.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected `check`, start `preflight`, and `transition` in [CLI](../../../se_harness/cli.py), [preflight](../../../se_harness/preflight.py), and [workflow](../../../se_harness/workflow.py) at the page baseline.
- [DR-015](../../engineering/DECISION_RIGHTS.md#governed-delegated-execution) limits execution delegation to WO start, completion, and VREC preparation.

**Proposed additions**

- A decision view and structured bridge; the evaluator continues to compute legality.

**Inputs, outputs, and writes**

- **Inputs:** Repository, selected WO, governing context, start decision or proven delegation.
- **Outputs:** Actual state, blockers, and one next step.
- **Writes:** Selected WO status and decision event when apply succeeds.

**Host differences**

- **Codex:** Covered before-tool checks need explicit host support and trust.
- **Claude Code:** Before-tool denial needs the supported host response. See [hook limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) for both hosts; hooks do not replace evaluator checks.

**Checks that demonstrate the behavior**

- **Success:** Approved WO plus valid start authority → `in_progress`.
- **Refusal:** Branch-only delegation → no delegated transition.
- **Recovery:** Interrupted response → read actual state before retrying apply.

**Open questions**

- How will the plugin authenticate and bind a human start decision to the exact transition?

</details>

## Scenario 10: Implement the change and collect evidence

### 1. Purpose and starting point

**Purpose:** Produce the authorized change and retain evidence of what was checked.

- **Starts when:** A started WO permits implementation.
- **Requires:** Approved scope, acceptance criteria, verification contracts, and required project checks.
- **Successful result:** The change and its evidence are ready for the completion decision.

### 2. Workflow

```text
Read scope and acceptance criteria
        ↓
Implement within scope and run required checks
        ↓
Retain results and check the actual changed paths
        ↓
Present implementation evidence for completion
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent using the change skill | Investigate and edit only the selected implementation scope. |
| 2 | Covered hook and evaluator | Check explicitly mapped actions before execution; return supported refusal responses when needed. |
| 3 | Agent and project tools | Run required checks and retain their actual results, including failures. |
| 4 | Agent using the evidence skill | Fill the evidence packet with substantive results and references. |
| 5 | Bridge and evaluator | Run review preflight and the Git-based handoff check; present the completion decision. |

The main agent remains the implementer. An optional reviewer can inspect evidence coverage, but cannot approve work. A check of declared paths does not prove the effects of an arbitrary shell command.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Guide implementation and evidence preparation. | **New:** change and evidence instructions route existing checks. |
| **Hook** | Check explicitly supported mutations. | **New:** action mapping and recursion guard; no universal shell parser. |
| **Script** | Invoke project checks and collect returned results. | **Adapt:** retain project scripts; add the shared bridge. |
| **Tool/interface** | Edit files, run checks, and submit evidence operations. | **Reuse:** normal host tools and existing CLI interfaces. |
| **Evaluator** | Evaluate scope, evidence, and handoff. | **Reuse:** workflow compliance and review preflight. |
| **Subagent** | Inspect coverage against the selected criteria. | **New:** optional read-only evidence reviewer; no record writes. |
| **Human** | Resolve changes beyond approved scope. | **Reuse:** affected definition or engineering owner decides. |
| **External control** | Protect integration while implementation continues. | **New:** independent merge enforcement from issue #347. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Required tests fail. | Handoff cannot claim completion. | Fix within scope and rerun the affected checks. |
| An edit needs wider scope. | Agent stops that edit; scope is not expanded automatically. | Obtain the applicable revised-scope decision. |
| Evidence is missing or stale. | Evaluator reports the evidence blocker. | Retain actual results, refresh the packet, and repeat handoff. |

### 5. Example result

> Illustrative: The change for WO-DEMO-010 and its test results are retained. The handoff check passes; the WO remains `in_progress`. Next: the engineering owner decides whether implementation is complete.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected `evidence`, review `preflight`, and checkpoint `check` in [CLI](../../../se_harness/cli.py) and [workflow compliance](../../../se_harness/workflow_compliance.py) at the page baseline.
- `--changed-path` with `--changes-complete` declares a change set; completeness remains a caller assertion.

**Proposed additions**

- Map known host actions to supported evaluator inputs. Use one shared bridge for hook and skill calls.

**Inputs, outputs, and writes**

- **Inputs:** Selected WO, actual changes, Git comparison base, retained test results.
- **Outputs:** Evidence references and the evaluator's handoff result.
- **Writes:** Code, tests, evidence packet, and retained `handoff.json`. Git-based handoff can rebind evidence; it is not a read-only status operation. Generating a packet does not generate test evidence.

**Host differences**

- **Codex:** Some tools and interactive-session input lack before-tool coverage.
- **Claude Code:** Hook timeout does not reliably stop execution. Both adapters must report their [coverage limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

- **Success:** In-scope changes and retained passing results → completion handoff.
- **Refusal:** Empty evidence packet → evidence blocker, no success claim.
- **Recovery:** After interruption, inspect changes and retained results before repeating writes.

**Open questions**

- Which host operations can provide a reliable description of their intended effects?

</details>

## Scenario 11: Complete implementation and prepare verification

### 1. Purpose and starting point

**Purpose:** Record completed implementation and prepare evidence for assurance review.

- **Starts when:** The implementation handoff is ready.
- **Requires:** Passing completion gates and completion authority; an eligible candidate and preparation authority when a VREC is required.
- **Successful result:** The WO is `implemented`; when required, a new VREC is `ready`.

### 2. Workflow

```text
Review the implementation handoff
        ↓
Authorized completion → WO becomes implemented
        ↓
Settle the exact candidate and check preparation authority
        ↓
Prepare a ready VREC when required
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Evidence skill | Present the completion decision with the actual handoff result. |
| 2 | Owner or eligible delegate, then bridge | Authorize and apply the selected WO's completion transition. |
| 3 | Agent and repository owner as required | Settle the candidate; any Git commit needs its own authorization. |
| 4 | Bridge and evaluator | Check preparation inputs and authority, then create the ready VREC and evaluator evidence. |

Completion and preparation each follow their own human or eligible delegated route. Neither verifies the work. The VREC is created after the clean candidate commit it names; it cannot contain the hash of its own future commit.

For `commit_bound_verification = "not_required"`, follow the evaluator's actual next step instead of creating an unnecessary VREC. [TRC-012](../../engineering/TRACEABILITY.md) limits this classification to recording or transporting an already authorized governance decision. Applicable evidence and accountable decisions still apply; mixed scope must be split or classified `required`.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain completion and preparation as separate steps. | **New:** evidence skill follows returned procedures. |
| **Hook** | Check a covered transition or preparation call. | **New:** explicit operation mapping to the bridge. |
| **Script** | Pass selected inputs to the evaluator. | **New:** bridge; no candidate hash invented by the agent. |
| **Tool/interface** | Expose completion and VREC preparation. | **Adapt:** existing CLI becomes structured operations. |
| **Evaluator** | Apply completion and bind verification inputs. | **Reuse:** transition engine and `capture_verification()`. |
| **Subagent** | Inspect the proposed evidence inputs. | **New:** optional read-only reviewer, with no decision right. |
| **Human** | Make completion and preparation decisions when due. | **Reuse:** existing rights; exact decision capture is new. |
| **External control** | Report CI status for delegated rights. | **Reuse:** live CI facts; Git authority stays separate. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Completion gate or authority fails. | WO remains `in_progress`. | Resolve the returned blocker and refresh handoff. |
| Worktree is dirty or evidence selection is invalid. | VREC preparation refuses. | Settle authorized changes and correct the exact inputs. |
| The preparation response is interrupted. | Do not assume the record is absent. | Inspect the selected ID and actual writes before retrying. |

### 5. Example result

> Illustrative: WO-DEMO-011 is `implemented`. VREC-DEMO-011 is `ready` and binds its retained evidence to the selected candidate. No verification or merge occurred. Next: the assurance owner reviews VREC-DEMO-011.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected `transition` and `capture-verification` in [workflow](../../../se_harness/workflow.py) and [provenance](../../../se_harness/provenance.py) at the page baseline.
- `capture-verification` creates records immediately; it has no preview flag.

**Proposed additions**

- Present exact preparation inputs and record distinct decisions without adding policy outside the evaluator.

**Inputs, outputs, and writes**

- **Inputs:** WO, verification contracts, evidence paths, preparation actor, eligible current candidate.
- **Outputs:** Completion result and, when required, ready VREC path.
- **Writes:** WO completion event, VREC, and evaluator evidence. Committing these later governance records is a separate authorized action.

**Host differences**

- **Codex:** Native adapter uses the shared structured operation.
- **Claude Code:** Native adapter uses the same semantics. [Hook limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) prevent either host from supplying human authority through tool permission.

**Checks that demonstrate the behavior**

- **Success:** Eligible clean candidate → ready VREC with its actual commit.
- **Refusal:** Dirty worktree → no claimed preparation success.
- **Recovery:** Candidate changes → repeat eligibility and evidence checks for that candidate.

**Open questions**

- How should the decision view show separate completion, preparation, and Git permissions without hiding any of them?

</details>

## Scenario 12: Independently verify the candidate

### 1. Purpose and starting point

**Purpose:** Let the assurance owner judge whether retained evidence verifies the exact candidate.

- **Starts when:** A ready VREC is submitted for assurance review.
- **Requires:** Its candidate, verification contracts, retained evidence, and the accountable assurance owner.
- **Successful result:** An explicit assurance decision is recorded on the selected VREC only.

### 2. Workflow

```text
Select the ready VREC and its exact candidate
        ↓
Inspect evidence and evaluate assurance gates
        ↓
Assurance owner decides
        ↓
Apply that decision and present the next handoff
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Agent using the evidence skill | Present the candidate, criteria, evidence, and unresolved findings. |
| 2 | Bridge and evaluator | Evaluate the selected assurance checkpoint and return eligibility or blockers. |
| 3 | Assurance owner | Decide whether the evidence verifies the candidate, or select rejection or supersession as applicable. |
| 4 | Bridge | Preview and apply the exact decision, then report the resulting VREC state. |

An optional second agent can find gaps. A separate model or a “reviewer” label does not establish independent assurance. The actual review and decision must satisfy repository role-separation policy.

Only the selected VREC changes. Referenced WOs and release records retain their states, and verification does not authorize integration.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Present evidence and the exact assurance decision. | **New:** evidence skill follows `PROC-VREC-DECIDE`. |
| **Hook** | Check a covered assurance transition invocation. | **New:** shared bridge invocation; no inferred approval. |
| **Script** | Preserve inputs and return the evaluator result. | **New:** decision-aware bridge and renderer. |
| **Tool/interface** | Present review material and selected transition. | **Adapt:** checkpoint and transition CLI interfaces. |
| **Evaluator** | Validate and apply the selected VREC transition. | **Reuse:** assurance gates and transition engine. |
| **Subagent** | Report evidence gaps for this candidate. | **New:** optional read-only reviewer; observations only. |
| **Human** | Assess evidence and exercise assurance authority. | **Reuse:** assurance owner; authenticated capture is new. |
| **External control** | Check decision provenance at protected integration. | **New:** independent enforcement under issue #347. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Evidence or candidate binding fails. | Evaluator refuses verification. | Repair through authorized work and prepare eligible evidence. |
| No assurance decision exists. | VREC stays `ready`; successful checks do not decide. | The accountable assurance owner reviews and decides. |
| Owner rejects or supersedes the record. | Apply only the valid selected outcome. | Retain the reason; for supersession, identify an eligible successor without rewriting historical candidate facts. |

An `assurance-owner` argument is not authentication. Trustworthy decision capture remains a design gap, not a capability supplied by the current CLI.

### 5. Example result

> Illustrative: The assurance owner's decision changed VREC-DEMO-012 to `verified`. Its referenced WO is unchanged; no merge occurred. Next: the repository or release owner selects the delivery path.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected transition checkpoint `check` with target `verified` and VREC transitions in [workflow](../../../se_harness/workflow.py) at the page baseline.
- [Decision rights](../../engineering/DECISION_RIGHTS.md) define assurance accountability and related-record boundaries.

**Proposed additions**

- A review view bound to candidate identity and authenticated decision provenance; legality stays in the evaluator.

**Inputs, outputs, and writes**

- **Inputs:** VREC, retained evidence, candidate identity, and actual assurance decision.
- **Outputs:** Selected record's resulting state and next required decision.
- **Writes:** Selected VREC decision fields and lifecycle event; referenced artifacts remain unchanged.

**Host differences**

- **Codex:** Tool permission does not authenticate an assurance decision.
- **Claude Code:** The same boundary applies; [host hooks](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) can assist presentation and checks, not replace assurance.

**Checks that demonstrate the behavior**

- **Success:** Eligible evidence plus actual assurance decision → selected VREC changes only.
- **Refusal:** Reviewer-agent approval alone → no applied human decision.
- **Recovery:** Changed implementation → reassess candidate coverage; preserve historical VREC facts.

**Open questions**

- Which trusted identity and decision store should the plugin use, and how is the reviewed candidate bound to it?

</details>

## Scenario 13: Authorize and perform integration

### 1. Purpose and starting point

**Purpose:** Integrate eligible work only after the repository owner authorizes the exact action.

- **Starts when:** The repository owner selects an integration path for the candidate.
- **Requires:** Applicable verification coverage, trusted policy, and action-specific authority.
- **Successful result:** The protected integration service performs only the authorized merge.

### 2. Workflow

```text
Present candidate, verification, and integration target
        ↓
Repository owner authorizes the exact action
        ↓
External control rechecks authority and current inputs
        ↓
Protected service integrates and reports the actual result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Evidence skill and evaluator | Present eligible coverage and the returned integration decision. |
| 2 | Repository owner | Authorize the named PR, target branch, candidate, and merge action. |
| 3 | External integration control | Validate current eligibility and authenticated authority against trusted policy. |
| 4 | Protected integration service | Perform the permitted action and return the resulting repository identity. |

This external control is proposed work linked to [issue #347](https://github.com/mmzen/se_harness/issues/347). The existing harness has no `merge` command. Until independent enforcement is demonstrated, the plugin should present the handoff without offering unattended integration.

Verification evidence lives in later governance commits. The control must validate the verified implementation plus permitted later changes; demanding a VREC that contains its own commit hash would be impossible. Candidate-authored exemptions cannot waive trusted requirements.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | Explain the exact integration decision. | **New:** evidence skill follows `PROC-REPOSITORY-INTEGRATION`. |
| **Hook** | Intervene before a covered integration request. | **New:** local assistance only; alternate routes still exist. |
| **Script** | Build a structured request and render its result. | **New:** bridge to a protected service, without embedding policy. |
| **Tool/interface** | Request the named repository action. | **Adapt:** GitHub operation exposed through the protected boundary. |
| **Evaluator** | Evaluate applicable coverage and next decision. | **Reuse:** coverage gates and integration procedure; no merge implementation. |
| **Subagent** | Not used. | **Not used:** another agent cannot approve integration. |
| **Human** | Authorize the specific repository action. | **Reuse:** repository owner; authenticated action binding is new. |
| **External control** | Prevent unauthorized merge through every route. | **New:** trusted gate and credentials the agent cannot use to bypass it. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Verification or authority is absent. | Proposed external control denies integration. | Obtain the missing eligible coverage or exact owner decision. |
| PR head or target changes. | Old authorization cannot silently cover different inputs. | Revalidate candidate coverage and refresh authority when required. |
| Hook is disabled or another API is used. | External control must still deny an unauthorized merge. | Proceed only through the protected, authorized route. |

### 5. Example result

> Illustrative: Verification is eligible, but integration is waiting. No merge occurred. Next: the repository owner authorizes the exact PR and target shown in the decision view.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [WORKFLOW.json](../../engineering/WORKFLOW.json), `PROC-REPOSITORY-INTEGRATION`, and the [merge-boundary proposal](../plugin-installation-proposal-2026-09-06.md#the-merge-boundary-must-stand-on-its-own) at the page baseline. This procedure presents a decision; it performs no merge.

**Proposed additions**

- A protected service must combine trusted evaluator results with authenticated action authority. Its gate must run at the external effect boundary.

**Inputs, outputs, and writes**

- **Inputs:** Exact PR, head, target, coverage, trusted policy, owner authorization.
- **Outputs:** Denial or observed merge result and resulting commit identity.
- **Writes:** Authorized remote merge and audit record; no inferred lifecycle changes.

**Host differences**

- **Codex:** Hosted tools and existing interactive sessions can bypass local hook coverage.
- **Claude Code:** Hooks can be disabled or fail to stop execution. Both need the same [external boundary](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

- **Success:** Valid coverage and exact owner authority → one intended merge.
- **Refusal:** Green CI, fabricated role, missing VREC, or direct API bypass → deny as applicable under trusted policy.
- **Recovery:** Ambiguous network response → inspect remote state before retrying.

**Open questions**

- Which protected service, credential model, and action-time checks close issue #347 without race conditions?

</details>
