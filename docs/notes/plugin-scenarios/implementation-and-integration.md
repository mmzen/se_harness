# Implementation and integration scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Part of the [scenario guide](README.md), using the [scenario template](../plugin-scenario-template.md). See the [operation overview](../plugin-operation-workflows-2026-09-06.md) for the shared component model.

**Review date:** 2026-09-06. **Source baseline:** [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; the repository's governing evaluator is 0.15.0. Existing interfaces were inspected, not exercised against that released evaluator. The proposed plugin workflows have not been integration-tested.

These scenarios grant no work or decision authority. **New** marks a proposed component or operation that must be built. **Reuse** retains an existing implementation or responsibility; **Adapt** changes its packaging or invocation; **Not used** means it is unnecessary here. A *work order* (WO) defines authorized work. A *verification record* (VREC) binds evidence to an exact candidate commit.

Every bridge call below means the new `bin/launcher bridge --request REQUEST_FILE --json` interface. `REQUEST_FILE` contains structured JSON with `operation`, absolute `repo`, and that operation's inputs. The launcher runs the installed `scripts/bridge` **[New]** with the trusted external evaluator. An `evaluator` request contains an `argv` array, never a shell command string. The `harnessctl` examples show the existing evaluator arguments that the bridge would pass; `REPO` is the absolute repository path.

Use the [shared calling convention](README.md#shared-component-names-and-calling-convention) for launcher calls and optional subagent delegation.

The new `review-preview` operation returns the selected contents, intended effects, and `plan_id`. The new `decision-review` human interface records an authenticated decision for that exact plan and returns `decision_ref`. The new `review-apply` operation rechecks both before applying it. For the narrow delegated route in scenarios 9 and 11, it instead checks the existing delegation rule and fresh CI facts. Neither an actor-name argument nor a local JSON file proves authority. The protected decision store and its host interface remain to be designed.

## Scenario 9: Start a work order

### 1. Purpose and starting point

**Purpose:** Establish that the agent may begin one approved work order.

- **Starts when:** The user asks to start a named WO with the `change` skill **[New]**.
- **Requires:** An approved WO, the session checks from [scenario 3](setup-and-sessions.md#scenario-3-start-a-session), and its governing documents.
- **Successful result:** An authorized transition changes only that WO to `in_progress`.

### 2. Workflow

```text
User invokes change start [New] for one WO
        ↓
Agent reads context → bridge [New] checks readiness and previews start
        ↓
Engineering owner decides, or evaluator confirms delegated authority
        ↓
Bridge applies the reviewed transition → WO is in_progress
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to start WO-DEMO-009.” **Claude Code:** invoke `/verity-plane:change start WO-DEMO-009`. The main agent reads `skills/change/SKILL.md`. |
| 2 | Agent → existing file and shell tools | Read the selected WO, `docs/engineering/OPERATING_CARD.md`, and the phase reading manifest's governing artifacts. Call the bridge using Codex `exec_command`, or Claude Code `Bash` / native `PowerShell`. |
| 3 | `scripts/bridge` **[New]** → existing evaluator | Run `check` for the selected WO, then `preflight --phase start`. The first call projects state without evaluating execution gates; preflight returns readiness blockers or the start decision. |
| 4 | Agent → `review-preview` **[New]** | Submit the selected WO, target `in_progress`, and proposed accountable actor. The bridge runs the existing transition preview and returns an exact-content plan. No lifecycle state changes. |
| 5 | Engineering owner → `decision-review` **[New]** | Review the WO and intended start, then authorize that exact action. If the evaluator returns an eligible delegated route, use its existing DR-015 checks instead of inventing a new human decision. |
| 6 | Agent → `review-apply` **[New]** | Send the `plan_id` and human `decision_ref`, or the selected delegated route. The bridge refreshes inputs and authority, then invokes the existing transition with `--apply`. |
| 7 | Bridge → agent following `change` | Run `check` again. Report the actual WO state and the evaluator's next step. A failed apply or missing decision must not be reported as a start. |

For delegated execution, `[delegation] class = "execution"` must exist at the PR base and the required live CI check must pass for the exact candidate head. A delegation added only on the working branch cannot authorize itself. Passing preflight or granting shell permission does not start work.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `change`, at `skills/change/SKILL.md`, guides start mode. | **New:** follows the existing `PROC-WO-START` sequence. |
| **Hook** | `PreToolUse` invokes `hooks/handler` for explicitly supported calls. | **Reuse:** host event. **New:** `hooks/hooks.json` registrations and handler; it does not start the WO automatically. |
| **Script** | `bin/launcher` selects the runtime; `scripts/bridge` invokes checks and the reviewed transaction. | **New:** shared execution path; no second lifecycle engine. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes the bridge; `decision-review` captures the start decision. | **Reuse:** shell tools. **New:** structured bridge and authenticated decision interface. |
| **Evaluator** | `check`, start `preflight`, and `transition` determine readiness and apply the legal change. | **Reuse:** CLI, workflow engine, and DR-015 delegation checks. |
| **Subagent** | Not used. | **Not used:** the main agent can prepare the start handoff. |
| **Human** | The engineering owner exercises `DR-WO-START` when that route is required. | **Reuse:** existing right. **New:** binding its authenticated decision to the reviewed plan. |
| **External control** | The CI provider supplies fresh check results for delegated execution. | **Reuse:** live CI facts. They grant no Git, merge, or release authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Integrity, required context, or start preflight fails. | The evaluator refuses start; `review-apply` must not change the WO. | Resolve the returned blocker within authorized scope, then repeat checks and preview. |
| A human start decision is missing. | `decision-review` shows the exact WO and action; apply waits. | The engineering owner supplies the decision, then the bridge rechecks the plan. |
| Delegation or its CI evidence fails. | The bridge refuses the delegated route. | Follow the evaluator's corrective or human-decision route. |
| The apply response is interrupted. | The agent cannot assume the WO stayed approved. | Read the actual WO state and decision event before deciding whether a retry is needed. |

### 5. Example result

> Illustrative: WO-DEMO-009 is now `in_progress` following its authorized start. Related artifacts are unchanged. Next: implement the approved scope.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [CLI](../../../se_harness/cli.py), [preflight](../../../se_harness/preflight.py), and [workflow](../../../se_harness/workflow.py) at the page baseline. Existing evaluator arguments:

```sh
harnessctl check REPO --artifact WO-DEMO-009 --json
harnessctl preflight REPO --work-order WO-DEMO-009 --phase start --json
harnessctl transition REPO --set WO-DEMO-009=in_progress --decision WO-DEMO-009=ACTOR --json
harnessctl transition REPO --set WO-DEMO-009=in_progress --decision WO-DEMO-009=ACTOR --apply --json
harnessctl check REPO --artifact WO-DEMO-009 --json
```

- `ACTOR` is the actual permitted actor after authority checks; the CLI argument itself is only an assertion. [DR-015](../../engineering/DECISION_RIGHTS.md#governed-delegated-execution) permits delegated WO start, completion, and VREC preparation only.

**Proposed additions**

- `change` start mode; `evaluator`, `review-preview`, and `review-apply` bridge operations. For example, an evaluator request has `operation: "evaluator"` and `argv: ["check", "REPO", "--artifact", "WO-DEMO-009", "--json"]`, with the actual absolute path replacing `REPO`.
- `decision-review` binds selected content and intended state to an authenticated owner. For delegation, the bridge rechecks PR-base policy and live exact-head CI; it does not trust a caller's `delegated-executor` string.

**Inputs, outputs, and writes**

- **Inputs:** Repository, WO, governing context, intended start, reviewed plan, human decision or eligible delegation facts.
- **Outputs:** Preview, blockers or apply result, actual state, and one next step.
- **Writes:** On successful apply, selected WO status and decision event. Decision capture also writes its protected audit record; projection and preview do not change artifacts.

**Host differences**

- **Codex:** Use `exec_command`; its hook matcher is `Bash`. `hooks/handler` needs an enabled and trusted registration.
- **Claude Code:** Use `Bash` or native `PowerShell`; a supported `PreToolUse` denial can intervene. Both hosts retain the documented [hook coverage limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement); the bridge must check its own calls even when no hook ran.

**Checks that demonstrate the behavior**

- **Success:** Approved WO, passing gates, and exact start authority → only that WO becomes `in_progress`.
- **Refusal:** Branch-only delegation or stale exact-head CI → no delegated transition.
- **Recovery:** Interrupted apply → actual state is inspected before any retry.

**Open questions**

- Which authenticated human interface and protected decision store will implement `decision-review`?

</details>

## Scenario 10: Implement the change and collect evidence

### 1. Purpose and starting point

**Purpose:** Produce the authorized change and retain what the checks actually found.

- **Starts when:** A selected WO is `in_progress` and the user requests implementation.
- **Requires:** Approved scope, acceptance criteria, verification contracts, and the repository's required check commands.
- **Successful result:** The implementation and retained evidence are ready for the completion decision; the WO remains `in_progress`.

### 2. Workflow

```text
User invokes change implement [New] for the started WO
        ↓
Supported PreToolUse → hooks/handler [New] → evaluator check
        ↓
Agent edits and runs the repository's checks
        ↓
Evidence skill [New] retains results → review preflight and handoff
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to implement WO-DEMO-010.” **Claude Code:** invoke `/verity-plane:change implement WO-DEMO-010`. The main agent reads `skills/change/SKILL.md` and the WO's required implementation context. |
| 2 | Agent → existing edit tools | Prepare a bounded edit request for Codex `apply_patch`, or Claude Code `Edit` / `Write`. A supported `PreToolUse` event runs before the requested tool executes in step 3. The main agent remains the implementer. |
| 3 | Existing `PreToolUse` → `hooks/handler` **[New]**, when supported | For a mapped action, call the shared bridge with the selected WO, `PROC-WO-IMPLEMENT`, and declared paths. The existing `check --checkpoint pre-action` returns the gate result; the handler translates a refusal into the host's supported response. If permitted, the host runs the edit tool. Unsupported actions are reported as uncovered. |
| 4 | Agent → `exec_command`, `Bash`, or `PowerShell` | Run the required commands from the repository's owner instructions and verification contract. Retain the real command, exit result, and evidence location, including failed checks. The plugin supplies no invented universal test command. |
| 5 | Agent → `evidence` skill **[New]** | Read `skills/evidence/SKILL.md` in prepare mode. Through the bridge, call existing `evidence --checkpoint handoff`, then fill the returned packet with substantive results and references using the edit tools. Creating the packet does not create test evidence. |
| 6 | Main agent → optional `evidence-reviewer` **[New]** | Delegate review of the selected criteria, diff, and retained results using the [host-specific invocation](README.md#shared-component-names-and-calling-convention). The helper returns omissions or concerns; it does not edit records, approve completion, or claim independent assurance. |
| 7 | Agent → bridge → existing evaluator | Run read-only review `preflight`, then `check --checkpoint handoff --from-git BASE`. Return the actual scope and evidence result and the completion decision. The Git-based handoff can rebind evidence and write `handoff.json`; invoke it explicitly, not as an automatic read-only hook check. |

The `evidence` mode can also be requested directly: “Use the verity-plane evidence skill to prepare the evidence for WO-DEMO-010” in Codex, or `/verity-plane:evidence prepare WO-DEMO-010` in Claude Code. The skill instructs the agent; only tools and executable code perform the calls.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides implement mode; `skills/evidence/SKILL.md` guides prepare mode. | **New:** instructions name the existing checks and preserve their returned next step. |
| **Hook** | `PreToolUse` → `hooks/handler`, registered in `hooks/hooks.json`, checks supported intended actions. | **Reuse:** host event. **New:** action mapping and recursion guard; no general shell-effect parser. |
| **Script** | `bin/launcher` and `scripts/bridge` invoke the evaluator; repository scripts execute the required project checks. | **New:** shared plugin scripts. **Reuse:** the repository's actual check scripts and commands. |
| **Tool/interface** | `apply_patch`, `Edit`, and `Write` edit; `exec_command`, `Bash`, and `PowerShell` run checks and the bridge. | **Reuse:** host tools. **New:** structured evaluator request mapping. |
| **Evaluator** | `check` pre-action and handoff, `evidence`, and review `preflight` evaluate scope and retained evidence. | **Reuse:** workflow compliance and evidence operations. |
| **Subagent** | `evidence-reviewer` optionally inspects coverage and reports gaps. | **New:** read-only helper, with no artifact write or decision right. |
| **Human** | The affected definition or engineering owner resolves work outside approved scope. | **Reuse:** existing remediation and scope decisions; test success supplies none. |
| **External control** | `integration-gate` keeps merge credentials and authority separate from implementation tools. | **New:** proposed protected service in scenario 13; a local hook cannot provide this boundary. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| An edit exceeds approved scope. | The agent stops that edit; a supported mapped hook call also returns refusal. | Obtain the affected owner's revised-scope decision through [scenario 8](definition-and-approval.md#scenario-8-revise-approved-definitions-or-work-scope), then refresh context. |
| Required checks fail. | Record the failure; the agent cannot claim implementation completion. | Fix within scope and rerun affected checks. |
| A shell operation has no reliable effect mapping. | The plugin reports that hook coverage is absent; declared paths are not proof of arbitrary shell effects. | Keep the action within explicit authority and use observed Git changes at handoff; protected external effects still need their separate gate. |
| Evidence is missing or stale. | The evaluator reports the blocker and no successful handoff is claimed. | Retain actual results, refresh the packet, and repeat the affected checks. |

### 5. Example result

> Illustrative: The change for WO-DEMO-010 and its actual test results are retained. The handoff check passes; the WO remains `in_progress`. Next: the engineering owner decides whether implementation is complete.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [CLI](../../../se_harness/cli.py) and [workflow compliance](../../../se_harness/workflow_compliance.py) at the page baseline. The following are evaluator arguments, not new plugin commands:

```sh
harnessctl check REPO --artifact WO-DEMO-010 --checkpoint pre-action --procedure PROC-WO-IMPLEMENT --changed-path src/example.py --changed-path tests/test_example.py --changes-complete --json
harnessctl evidence REPO --artifact WO-DEMO-010 --checkpoint handoff --json
harnessctl preflight REPO --work-order WO-DEMO-010 --phase review --json
harnessctl check REPO --artifact WO-DEMO-010 --checkpoint handoff --from-git BASE --json
```

- Paths are illustrative; the caller supplies the actual selected action's paths. `--changes-complete` remains a caller assertion. `BASE` is the actual Git comparison base.

**Proposed additions**

- `change` implement mode and `evidence` prepare mode use `operation: "evaluator"` with the existing command's argument array. `hooks/handler` invokes that same bridge for its supported pre-action calls; it must not recursively re-enter itself or run the full handoff automatically.
- Optional `agents/evidence-reviewer`: Claude Code registers `agents/evidence-reviewer.md`; Codex needs separate `.codex/agents/evidence-reviewer.toml` project registration. This is one proposed helper role with host-specific definitions, not a mandatory second implementer.

**Inputs, outputs, and writes**

- **Inputs:** Selected WO, approved criteria, intended paths, actual Git changes, comparison base, check commands, and retained results.
- **Outputs:** Command results, evidence references, optional review findings, and the evaluator's handoff result.
- **Writes:** Code, tests, actual result files, evidence packet, and retained `handoff.json`. Git-based handoff can rebind evidence. The review helper writes none of these.

**Host differences**

- **Codex:** `exec_command` uses the `Bash` hook matcher. `write_stdin` does not start a new `PreToolUse` event; hosted tools are not assumed covered. Use `apply_patch` only under the adapter's demonstrated coverage or report the gap.
- **Claude Code:** Use `Edit` / `Write` and `Bash` / native `PowerShell`. A hook timeout does not reliably stop execution. Both adapters must report their [coverage limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

- **Success:** In-scope changes and retained real passing results → completion handoff, with the WO still `in_progress`.
- **Refusal:** Empty evidence packet or failed required check → blocker, no completion claim.
- **Recovery:** Interrupted check or handoff → inspect actual outputs and writes before rerunning it.

**Open questions**

- Which host operations provide enough reliable effect information for the first supported hook mappings?

</details>

## Scenario 11: Complete implementation and prepare verification

### 1. Purpose and starting point

**Purpose:** Record implementation completion, then prepare the exact candidate for assurance when required.

- **Starts when:** The implementation handoff is ready and the user requests completion.
- **Requires:** Passing completion gates and completion authority; an eligible candidate and preparation authority when a VREC is required.
- **Successful result:** The WO is `implemented`; when required, a new VREC is `ready`, awaiting assurance.

### 2. Workflow

```text
change complete [New] → refresh handoff and preview completion
        ↓
Owner decision or eligible delegation → WO is implemented
        ↓
evidence prepare [New] → settle exact candidate and preparation authority
        ↓
capture-verification creates a ready VREC, when required
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to complete WO-DEMO-011.” **Claude Code:** invoke `/verity-plane:change complete WO-DEMO-011`. Read `skills/change/SKILL.md` and refresh the selected handoff result if its inputs changed. |
| 2 | Agent → `review-preview` **[New]** | Through `exec_command`, `Bash`, or `PowerShell`, request the WO transition to `implemented`. The bridge runs the existing transition preview and returns its plan and completion gates. |
| 3 | Engineering owner → `decision-review` **[New]**, or eligible delegate | Supply the actual completion decision. For DR-015 delegation, the bridge instead checks the class at the PR base and required live CI for the exact head; the actor's name does not prove delegation. |
| 4 | Agent → `review-apply` **[New]** | Recheck the plan and completion authority, then call existing `transition --apply`. Only the selected WO becomes `implemented`. Read the returned next step before preparing anything else. |
| 5 | Agent following `evidence` prepare mode **[New]** | Read `skills/evidence/SKILL.md`. If commit-bound verification is required, identify the verification contracts and retained evidence. Settle the candidate using existing Git commands through the shell tool; any commit needs its own actual authorization. |
| 6 | Agent → `review-preview`, then preparation actor → `decision-review` **[New]** | Present the proposed VREC ID, WOs, verification contracts, evidence paths, preparation actor, and eligible current candidate. Bind that exact preparation request to its authority, or prove the eligible delegated preparation route. |
| 7 | Agent → `review-apply` → existing `capture-verification` | Recheck current candidate and inputs, then create the ready VREC and evaluator evidence. `capture-verification` writes immediately; the preview in step 6 is a new bridge operation, not an existing CLI dry run. |
| 8 | Agent → bridge → existing `check` | Select the new VREC and report its actual state, bound commit, retained evidence, and assurance decision. The agent has prepared verification, not performed it. |

For `commit_bound_verification = "not_required"`, follow the evaluator's actual next step without creating an unnecessary VREC. [TRC-012](../../engineering/TRACEABILITY.md) limits this classification to recording or transporting an already authorized governance decision. Applicable evidence and accountable decisions still apply; mixed scope must be split or classified `required`.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides completion; `skills/evidence/SKILL.md` guides VREC preparation. | **New:** distinct modes follow the evaluator's returned procedures. |
| **Hook** | `PreToolUse` → `hooks/handler` checks covered transition and preparation calls. | **Reuse:** host event. **New:** explicit registrations and mappings, with no automatic completion. |
| **Script** | `bin/launcher` and `scripts/bridge` preserve exact inputs and resolve the evaluator. | **New:** reviewed operations; they must not invent a candidate hash or a preparation dry-run command. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` runs the bridge and authorized Git operations; `decision-review` captures each distinct decision. | **Reuse:** shell and Git tools. **New:** reviewed request and decision interfaces. |
| **Evaluator** | `transition`, `capture-verification`, and `check` apply completion and prepare candidate evidence. | **Reuse:** workflow engine and `capture_verification()`. |
| **Subagent** | `evidence-reviewer` can inspect selected evidence inputs before preparation. | **New:** optional read-only helper; it supplies no preparation or assurance authority. |
| **Human** | Engineering owner decides completion; the named preparation actor authorizes preparation when due. | **Reuse:** distinct existing rights. **New:** authenticated capture of their exact decisions. |
| **External control** | CI provider supplies live facts for eligible delegated rights. | **Reuse:** existing CI evidence. Delegation supplies no Git or external-action authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Completion gates or authority fail. | The WO remains `in_progress`; the bridge refuses completion. | Resolve the returned blocker and refresh handoff and preview. |
| Candidate worktree is dirty or evidence selection is invalid. | `capture-verification` refuses preparation. | Settle authorized changes and correct the exact inputs before a new preview. |
| A candidate commit needs authorization. | The agent waits before that Git action; completion authority does not supply it. | Obtain the exact missing Git authorization, then recheck the resulting candidate. |
| A response is interrupted after preparation. | A VREC or evidence file may already exist. | Inspect its actual ID and writes before retrying; do not create a duplicate record or rewrite history. |

### 5. Example result

> Illustrative: WO-DEMO-011 is `implemented`. VREC-DEMO-011 is `ready` and binds its retained evidence to the selected candidate. No verification or merge occurred. Next: the assurance owner reviews VREC-DEMO-011.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [CLI](../../../se_harness/cli.py), [workflow](../../../se_harness/workflow.py), and [provenance](../../../se_harness/provenance.py) at the page baseline. Existing evaluator arguments:

```sh
harnessctl transition REPO --set WO-DEMO-011=implemented --decision WO-DEMO-011=ACTOR --json
harnessctl transition REPO --set WO-DEMO-011=implemented --decision WO-DEMO-011=ACTOR --apply --json
harnessctl capture-verification REPO --id VREC-DEMO-011 --work-order WO-DEMO-011 --verification VER-DEMO-011 --evidence EVIDENCE_PATH --owner PREPARATION_ACTOR --json
harnessctl check REPO --artifact VREC-DEMO-011 --json
```

- `capture-verification` has no preview flag. It binds the eligible current candidate; it does not accept an agent-invented commit value. A VREC belongs in a later governance commit than the candidate it names, because it cannot contain the hash of its own future commit.

**Proposed additions**

- `change` complete mode and `evidence` prepare mode use the shared `review-preview` / `review-apply` operations. A preparation plan binds the VREC ID, selected WOs and contracts, evidence identities, candidate, and actor before the existing writing command runs.
- The new bridge must distinguish completion, preparation, and Git authority. A completion decision cannot stand in for the other two.

**Inputs, outputs, and writes**

- **Inputs:** WO, handoff, completion decision, verification contracts, evidence paths, eligible current candidate, and preparation authority.
- **Outputs:** Completion result and, when required, ready VREC path, exact candidate identity, and next assurance decision.
- **Writes:** WO completion event; VREC and evaluator evidence when required; protected decision records. Committing the later governance records remains a separate authorized action.

**Host differences**

- **Codex:** Use `exec_command` for bridge and Git calls. The optional helper needs `.codex/agents/evidence-reviewer.toml` registration.
- **Claude Code:** Use `Bash` / native `PowerShell`; the optional helper is `agents/evidence-reviewer.md`. Both use the same bridge semantics and retain the [hook limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

- **Success:** Required verification plus an eligible clean candidate and preparation authority → ready VREC with the actual commit.
- **Refusal:** Completion authority alone, dirty worktree, or changed plan inputs → no claimed preparation success.
- **Recovery:** Changed candidate → repeat eligibility and evidence checks for that candidate, preserving historical records.

**Open questions**

- How should `decision-review` show separate completion, preparation, and Git decisions without concealing any of them?

</details>

## Scenario 12: Independently verify the candidate

### 1. Purpose and starting point

**Purpose:** Let the assurance owner judge whether retained evidence verifies the exact candidate.

- **Starts when:** The user submits a ready VREC for review with the `evidence` skill **[New]**.
- **Requires:** The VREC's candidate, verification contracts, retained evidence, and the accountable assurance owner.
- **Successful result:** The assurance owner's explicit decision is recorded on the selected VREC only.

### 2. Workflow

```text
evidence review [New] → inspect the VREC, candidate, and evidence
        ↓
Existing assurance checkpoint → eligible decision or blockers
        ↓
decision-review [New] → assurance owner decides
        ↓
review-apply [New] → existing transition changes only the VREC
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `evidence` skill **[New]** | **Codex:** ask “Use the verity-plane evidence skill to review VREC-DEMO-012.” **Claude Code:** invoke `/verity-plane:evidence review VREC-DEMO-012`. The main agent reads `skills/evidence/SKILL.md` in review mode. |
| 2 | Agent → existing file and shell tools | Read the selected VREC, exact candidate, verification criteria, and retained evidence. Through the bridge, run existing `check --checkpoint transition --target verified` for that VREC. Return assurance gate results and unresolved findings. |
| 3 | Main agent → optional `evidence-reviewer` **[New]** | Delegate the bounded material using the [host-specific invocation](README.md#shared-component-names-and-calling-convention). The helper returns evidence gaps to the main agent. Its findings assist the assurance owner; no subagent result authorizes verification. |
| 4 | Agent → `review-preview` **[New]** | Request only the selected VREC's intended outcome. The bridge runs existing transition planning and returns a plan containing that candidate, reviewed evidence, target state, and actual accountable actor. |
| 5 | Assurance owner → `decision-review` **[New]** | Inspect the evidence and make the assurance decision for the exact plan. Verification is a human assurance decision; DR-015 execution delegation does not cover it. |
| 6 | Agent → `review-apply` **[New]** | Send `plan_id` and authenticated `decision_ref` through the shell tool. The bridge rechecks the binding and evaluator gates, then invokes `transition --apply` for the selected VREC. |
| 7 | Bridge → agent following `evidence` | Run `check` for the VREC again. Report its actual outcome and the evaluator's delivery-path decision. No WO or RLS is changed by inference, and no merge is performed. |

The owner may instead choose a valid rejection or supersession outcome. Rejection needs the recorded reason; supersession needs an eligible successor. A separate model or a “reviewer” label does not establish independent assurance: the actual review and decision must satisfy repository role-separation policy.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `evidence`, at `skills/evidence/SKILL.md`, guides review mode. | **New:** follows `PROC-VREC-DECIDE` and its valid alternatives. |
| **Hook** | `PreToolUse` → `hooks/handler` checks a supported assurance transition call. | **Reuse:** host event. **New:** registered operation mapping; no inferred approval. |
| **Script** | `bin/launcher` and `scripts/bridge` preserve the candidate and reviewed decision inputs. | **New:** reviewed transaction binding around the existing evaluator. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes the bridge; `decision-review` presents the human decision. | **Reuse:** shell tools. **New:** exact-content decision interface. |
| **Evaluator** | Assurance checkpoint `check` and `transition` validate and apply the selected VREC outcome. | **Reuse:** assurance gates and transition engine. |
| **Subagent** | `evidence-reviewer` reports gaps for this candidate. | **New:** optional read-only helper; observations only. |
| **Human** | The assurance owner reviews evidence and exercises `DR-VREC-DECIDE`. | **Reuse:** existing accountability and separation rules. **New:** authenticated decision capture. |
| **External control** | The protected decision store retains provenance that `integration-gate` can check later. | **New:** decision provenance and independent integration enforcement; a local role string supplies neither. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Evidence or candidate binding fails. | The evaluator refuses verification; the bridge must not apply it. | Repair through authorized work and prepare eligible evidence for the actual candidate. |
| No assurance decision exists. | The VREC stays `ready`; passing checks and helper findings do not decide. | The accountable assurance owner reviews and decides in `decision-review`. |
| Reviewed inputs change. | The bridge rejects the stale plan or decision binding. | Present the changed candidate or evidence for the required fresh review. |
| Owner rejects or supersedes the VREC. | Apply only the valid selected outcome and preserve its history. | Retain the reason or eligible successor; follow the evaluator's next step. |

### 5. Example result

> Illustrative: The assurance owner's decision changed VREC-DEMO-012 to `verified`. Its referenced WO is unchanged; no merge occurred. Next: the repository or release owner selects the delivery path.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [CLI](../../../se_harness/cli.py), VREC transitions in [workflow](../../../se_harness/workflow.py), and [decision rights](../../engineering/DECISION_RIGHTS.md) at the page baseline. Existing evaluator arguments for verification:

```sh
harnessctl check REPO --artifact VREC-DEMO-012 --checkpoint transition --target verified --json
harnessctl transition REPO --set VREC-DEMO-012=verified --decision VREC-DEMO-012=assurance-owner --json
harnessctl transition REPO --set VREC-DEMO-012=verified --decision VREC-DEMO-012=assurance-owner --apply --json
harnessctl check REPO --artifact VREC-DEMO-012 --json
```

- `assurance-owner` is a CLI actor assertion, not authentication. Existing `transition --reason ID=TEXT` supplies a rejection reason; for supersession the reason identifies the eligible successor VREC.

**Proposed additions**

- `evidence` review mode, the optional `agents/evidence-reviewer` helper, and shared `review-preview` / `review-apply` operations. `decision-review` binds the actual assurance owner to the exact VREC, candidate, evidence, and selected outcome.
- Lifecycle legality stays in the evaluator. The human interface supplies authentic decision provenance; it does not replace gate checks.

**Inputs, outputs, and writes**

- **Inputs:** Selected VREC, retained evidence, candidate identity, intended outcome, actual assurance decision, and any required reason or successor.
- **Outputs:** Gate results, exact review plan, resulting VREC state, and next required decision.
- **Writes:** Selected VREC decision fields and lifecycle event, plus the protected decision record. Referenced artifacts and historical candidate facts remain unchanged.

**Host differences**

- **Codex:** Use `exec_command`; optional review helper registration is `.codex/agents/evidence-reviewer.toml`.
- **Claude Code:** Use `Bash` / native `PowerShell`; optional helper definition is `agents/evidence-reviewer.md`. Neither host's tool permission authenticates an assurance decision; their [hooks](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) only assist supported checks.

**Checks that demonstrate the behavior**

- **Success:** Eligible evidence and actual assurance decision → selected VREC changes only.
- **Refusal:** Reviewer-agent approval, fabricated actor argument, or stale decision binding → no applied human decision.
- **Recovery:** Changed implementation → reassess candidate coverage while preserving historical VREC facts.

**Open questions**

- Which identity provider and protected store will make `decision-review` decisions verifiable at later external actions?

</details>

## Scenario 13: Authorize and perform integration

### 1. Purpose and starting point

**Purpose:** Merge eligible work only after the repository owner authorizes the exact action.

- **Starts when:** The repository owner selects integration for the candidate.
- **Requires:** Applicable verified coverage, trusted policy, an exact PR/head/target, and action-specific authority.
- **Successful result:** The proposed `integration-gate` performs only the authorized merge and reports the actual result.

### 2. Workflow

```text
change integrate [New] → present coverage and exact PR/head/target
        ↓
decision-review [New] → repository owner authorizes the merge
        ↓
integration-gate [New] rechecks authority and current remote inputs
        ↓
Protected merge → observed result and resulting commit
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | User → `change` skill **[New]** | **Codex:** ask “Use the verity-plane change skill to prepare integration of this PR.” **Claude Code:** invoke `/verity-plane:change integrate PR_URL`. The main agent reads `skills/change/SKILL.md` and resolves the exact PR and selected artifact. |
| 2 | Agent → bridge → existing evaluator | Run `check` for that WO or VREC and follow `PROC-REPOSITORY-INTEGRATION` when the evaluator returns it. Present verified coverage and the repository owner's integration decision. This existing procedure performs no merge. |
| 3 | Agent → `integration-preview` → `integration-gate` **[New]** | Send a structured bridge request naming the repository, PR, current head, target branch and commit, merge method, and selected coverage. The protected service reads remote facts and returns eligibility, intended effects, and `plan_id`. |
| 4 | Repository owner → `decision-review` **[New]** | Authorize the exact merge action shown in that plan. An earlier VREC decision, a request to implement, or green CI does not supply this external-action authorization. |
| 5 | Agent → `integration-submit` → `integration-gate` **[New]** | Send `plan_id` and authenticated `decision_ref`. Return `operation_id`; at the effect boundary, the service rereads remote identities, trusted policy, required checks, and coverage, refusing stale or unauthorized inputs. |
| 6 | `integration-gate` **[New]** → protected GitHub API | Use credentials unavailable to the coding agent to perform the permitted merge. Record the actual PR outcome and resulting commit; do not infer any WO, VREC, or RLS transition. |
| 7 | Agent → `integration-status` **[New]** | Send `operation_id` through the bridge and report its observed result: pending, denied, merged with commit, or unknown. If the response is ambiguous, inspect remote state through the service before proposing a retry. |

`integration-gate` is new work linked to [issue #347](https://github.com/mmzen/se_harness/issues/347), not an existing SE Harness command. Until independent enforcement is demonstrated, the plugin stops at the owner handoff and offers no unattended merge. The proposed service, credentials, and repository protections must cover every merge route, including direct API and Git access.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `change`, at `skills/change/SKILL.md`, guides integrate mode. | **New:** explains the existing `PROC-REPOSITORY-INTEGRATION` handoff and proposed protected execution. |
| **Hook** | `PreToolUse` → `hooks/handler` can intervene before a covered integration request. | **Reuse:** host event. **New:** local mapping only; alternate routes remain outside its authority. |
| **Script** | `bin/launcher` and `scripts/bridge` send structured previews and reviewed requests. | **New:** client of `integration-gate`; no agent-held merge credential. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes the bridge; `decision-review` captures the exact merge decision. | **Reuse:** shell tools. **New:** protected service request and decision interface. |
| **Evaluator** | `check` reports applicable coverage and the integration decision. | **Reuse:** coverage gates and existing procedure; there is no `harnessctl merge` implementation. |
| **Subagent** | Not used. | **Not used:** another agent cannot authorize integration. |
| **Human** | The repository owner selects integration and authorizes the specific external action. | **Reuse:** path-specific and external-action rights. **New:** authenticated binding to exact remote inputs. |
| **External control** | `integration-gate` validates and performs the merge using protected credentials and repository rules. | **New:** deterministic action-time enforcement across every route. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| The protected service is absent or its enforcement is unproven. | The plugin presents the owner handoff; it does not offer unattended integration. | The owner uses the repository's established reviewed delivery process until the service is demonstrated. |
| Applicable verification or exact merge authority is missing. | `integration-gate` denies the action. | Obtain the eligible coverage or actual repository-owner decision, then preview again. |
| PR head, target, or merge action changes. | The service rejects a plan whose bound inputs no longer match. | Revalidate coverage and refresh authority when the change requires it. |
| Hook is disabled or another API is used. | External protections must still deny unauthorized integration. | Use the protected authorized route; a local warning is not enforcement. |
| The merge response is lost. | The outcome is unknown, not automatically failed. | Read actual remote PR and target state before any retry. |

### 5. Example result

> Illustrative: Verification is eligible, but integration is waiting. No merge occurred. Next: the repository owner authorizes the exact PR, head, target, and merge action shown in `decision-review`.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

- Inspected [WORKFLOW.json](../../engineering/WORKFLOW.json), `PROC-REPOSITORY-INTEGRATION`, and the [merge-boundary proposal](../plugin-installation-proposal-2026-09-06.md#the-merge-boundary-must-stand-on-its-own) at the page baseline. The existing selection can be requested as:

```sh
harnessctl check REPO --artifact VREC-DEMO-012 --json
```

- This projects state and the next decision; it does not perform a merge or grant its authority. No existing `harnessctl` subcommand submits integration.

**Proposed additions**

- `change` integrate mode invokes the new bridge operations `integration-preview`, `integration-submit`, and `integration-status`. Preview inputs are the repository identity, PR URL/number, exact head, target branch/commit, merge method, and selected artifact/coverage; it returns `plan_id`. Submit binds that plan to `decision_ref` and returns `operation_id`. Status reads that operation's observed remote outcome. `scripts/bridge` sends these structured fields to `integration-gate`; the network transport and service implementation are undecided.
- The service combines trusted evaluator results with authentic owner authorization at the moment of the external effect. Agent-editable branch content must not waive trusted requirements or create credentials that bypass it.
- VRECs live in later governance commits than their verified candidate. The service must validate the implementation plus permitted later changes; requiring a VREC to contain its own commit hash would be impossible.

**Inputs, outputs, and writes**

- **Inputs:** Exact PR, head, target branch and commit, merge method, verified coverage, trusted policy, and owner authorization.
- **Outputs:** Preview, denial, or observed merge result and resulting commit identity.
- **Writes:** Protected decision and execution audit records, and only the authorized remote merge. No inferred lifecycle changes.

**Host differences**

- **Codex:** `exec_command` can invoke the client, but hosted tools and existing interactive sessions can bypass local hook coverage.
- **Claude Code:** `Bash` / native `PowerShell` can invoke the same client, but hooks may be disabled or fail to stop execution. Both hosts need the same [external boundary](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement), including protection against alternate credentials and APIs.

**Checks that demonstrate the behavior**

- **Success:** Valid coverage and exact owner authority → one intended merge with an observed resulting commit.
- **Refusal:** Green CI alone, fabricated role, stale plan, missing required coverage, or direct API bypass → deny the unauthorized effect.
- **Recovery:** Ambiguous network response → inspect remote state before retrying; do not merge twice or claim success without evidence.

**Open questions**

- Which protected service, credential model, and atomic remote checks implement `integration-gate` and close issue #347?

</details>
