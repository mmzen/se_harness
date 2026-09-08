# Implementation and integration scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Part of the [scenario guide](README.md), using the [scenario template](../plugin-scenario-template.md). See the [operation overview](../plugin-operation-workflows-2026-09-06.md) for the shared component model.

**Review date:** 2026-09-08. **Source baseline:** [`aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0; the repository's governing evaluator is 0.15.0. Existing interfaces were inspected, not exercised against that released evaluator. The proposed plugin workflows have not been integration-tested.

These scenarios grant no work or decision authority. **New** means a component must be built; **Reuse** retains an existing implementation or responsibility; **Adapt** changes its packaging; **Not used** means it is unnecessary here. A *work order* (WO) defines authorized work. A *verification record* (VREC) binds evidence to an exact candidate commit.

The plugin supplies `scripts/harnessctl` **[New packaging]** (`scripts/harnessctl.exe` on Windows), with portable Python, a published evaluator, its templates, and package metadata outside the target repository. Skills and hooks call this entry point directly. The commands below use `harnessctl` as shorthand for that plugin path; `REPO` is the absolute target repository path. The installed evaluator must match the repository's required version before these scenarios run.

These scenarios use the new before-tool hook script `scripts/check-tool-action`, registered in `hooks/hooks.json`. It translates supported host events into existing `harnessctl` checks. See the [shared calling convention](README.md#shared-component-names-and-calling-convention) for host paths and optional subagent invocation.

**Known boundary:** `--decision ID=ACTOR` records an actor assertion; it does not authenticate a human decision. Skills must use actual authority, but instructions and local hooks cannot guarantee that an agent obeys. Deterministic enforcement remains an open requirement in [issue #347](https://github.com/mmzen/se_harness/issues/347).

The agent follows an applicable evaluator next step automatically while the user's request and actual authority cover it. Named skill invocations below are optional entry points, not a prompt required at each stage. Reuse a decision that still covers the exact action, content, candidate, and destination; ask only for missing authority or a material change. A next step identifies what to do, but does not itself grant permission.

## Scenario 9: Start a work order

### 1. Purpose and starting point

**Purpose:** Establish that the agent may begin one approved work order.

- **Starts when:** The evaluator reaches WO start within the requested work, or the user requests it through `change` **[New]**.
- **Requires:** An approved WO, the checks from [scenario 3](setup-and-sessions.md#scenario-3-start-a-session), and its governing documents.
- **Successful result:** An authorized transition changes only that WO to `in_progress`.

### 2. Workflow

```text
change start [New] → read the selected WO and required context
        ↓
Existing check → start preflight
        ↓
Engineering owner authorizes start, or existing delegation applies
        ↓
Existing transition → preview → apply → check actual state
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `change` skill **[New]** | Continue from the applicable next step within the existing request. Optional direct entry: ask Codex to use `verity-plane change` to start WO-DEMO-009, or invoke `/verity-plane:change start WO-DEMO-009` in Claude Code. Read `skills/change/SKILL.md`; no repeated invocation is needed. |
| 2 | Main agent → file tools | Read the selected WO, `docs/engineering/OPERATING_CARD.md`, and the phase reading manifest's governing artifacts. |
| 3 | Agent → shell tool → bundled `harnessctl` | Run `check REPO --artifact WO-DEMO-009 --json`, then `preflight REPO --work-order WO-DEMO-009 --phase start --json`. The first projects state; the second checks start readiness. Neither starts work. |
| 4 | Engineering owner, or eligible delegate | Establish the exact start authority. Reuse an existing decision if it covers this start. Otherwise obtain the engineering owner's decision. Use DR-015 delegation only when its required facts are proven. |
| 5 | Agent → bundled `harnessctl` | Run `transition` for `WO-DEMO-009=in_progress` with the actual permitted actor, first without `--apply`. Inspect the preview, then repeat with `--apply` while the selected content and authority still match. |
| 6 | Agent → bundled `harnessctl` | Run `check` for the WO again and report its actual state and next step. A preview or failed apply is not a start. |

For DR-015, `[delegation] class = "execution"` must exist at the PR base, and the required live CI check must pass for the exact candidate head. A class added only on the working branch cannot authorize itself. Eligible delegation does not require another human start decision.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides start mode. | **New:** follows existing `PROC-WO-START`. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action` before covered actions. | **Reuse:** host event. **New:** required applicable checks; the hook does not grant start authority. |
| **Script** | `scripts/harnessctl` runs the external published evaluator. | **Adapt:** package the existing CLI with its runtime. |
| **Tool/interface** | Codex `exec_command`, or Claude Code `Bash` / native `PowerShell`, calls `harnessctl`. | **Reuse:** existing shell tools and CLI arguments. |
| **Evaluator** | `check`, start `preflight`, and `transition` determine readiness and update the WO. | **Reuse:** existing gates, workflow engine, and delegation checks. |
| **Subagent** | Not used. | **Not used:** the main agent handles the start sequence. |
| **Human** | The engineering owner supplies `DR-WO-START` when required. | **Reuse:** existing right and any decision that already covers the action. |
| **External control** | CI provider supplies current check results for delegation. | **Reuse:** live CI facts; they confer no Git, merge, or release authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Integrity, context, or start preflight fails. | Stop before applying the transition. | Resolve the returned blocker within authorized scope, then repeat the checks. |
| Required start authority is missing. | The agent presents the exact WO and start decision; the WO stays approved. | The engineering owner decides, or an eligible existing delegation is established. |
| Delegation or its CI evidence fails. | The delegated route is unavailable. | Follow the evaluator's corrective or human-decision route. |
| The apply response is interrupted. | The actual state is uncertain. | Read the WO and decision event before retrying. |

### 5. Example result

> Illustrative: WO-DEMO-009 is now `in_progress` following its authorized start. Related artifacts are unchanged. Next: implement its approved scope.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py), [preflight](../../../se_harness/preflight.py), and [workflow engine](../../../se_harness/workflow.py) already provide these commands:

```sh
harnessctl check REPO --artifact WO-DEMO-009 --json
harnessctl preflight REPO --work-order WO-DEMO-009 --phase start --json
harnessctl transition REPO --set WO-DEMO-009=in_progress --decision WO-DEMO-009=ACTOR --json
harnessctl transition REPO --set WO-DEMO-009=in_progress --decision WO-DEMO-009=ACTOR --apply --json
harnessctl check REPO --artifact WO-DEMO-009 --json
```

`ACTOR` is the actual permitted actor. The CLI argument alone proves no authority. [DR-015](../../engineering/DECISION_RIGHTS.md#governed-delegated-execution) covers only WO start, completion, and VREC preparation. A `check` without a checkpoint projects state and does not evaluate execution gates.

**Proposed additions**

`change` start mode calls the packaged CLI directly. `scripts/check-tool-action` runs existing checks for supported tool events; it does not implement lifecycle rules or authenticate the actor.

**Inputs, outputs, and writes**

- **Inputs:** Repository, WO, governing context, and actual start decision or delegation facts.
- **Outputs:** Preview, blockers or apply result, actual state, and next step.
- **Writes:** Successful apply changes the selected WO's status and decision event. Projection, preflight, and preview are read-only.

**Host differences**

Codex uses `exec_command`; Claude Code uses `Bash` / native `PowerShell`. Both call the installed plugin path. Hook coverage is host-specific and must be demonstrated; see the [hook limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

Proposed acceptance checks: authorized start changes only the selected WO; branch-only delegation or stale CI cannot qualify delegated execution; an interrupted apply is inspected before retry. These are requirements for future testing, not results from this note.

**Open questions**

How will authenticated human authority be enforced at the effect boundary? The current actor argument and this packaging proposal do not close issue #347.

</details>

## Scenario 10: Implement the change and collect evidence

### 1. Purpose and starting point

**Purpose:** Produce the authorized change and retain what its checks actually found.

- **Starts when:** A selected WO is `in_progress` and implementation is the applicable next step within the existing request, or the user requests it directly.
- **Requires:** Approved scope, acceptance criteria, verification contracts, and the repository's required check commands.
- **Successful result:** Implementation and evidence are ready for the completion decision; the WO remains `in_progress`.

### 2. Workflow

```text
change implement [New] → main agent prepares an in-scope edit
        ↓
Supported PreToolUse → scripts/check-tool-action [New] → harnessctl check
        ↓
Agent edits and runs the repository's actual checks
        ↓
evidence prepare [New] → retain results → harnessctl handoff check
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `change` skill **[New]** | Continue after the authorized start without waiting for another implementation prompt. Optional direct entry: ask Codex to use `verity-plane change`, or invoke `/verity-plane:change implement WO-DEMO-010` in Claude Code. Read `skills/change/SKILL.md` and the WO's required context. |
| 2 | Agent → edit tools | Prepare an edit through Codex `apply_patch`, or Claude Code `Edit` / `Write`. The main agent implements the change. |
| 3 | Host `PreToolUse` → `scripts/check-tool-action` **[New]**, for covered edits | Run the applicable existing `check` pre-action gates for the selected WO, `PROC-WO-IMPLEMENT`, and actual declared paths before the effect. Translate the result into the host's hook response. Do not skip required gates to reduce latency; report actions the adapter cannot cover. |
| 4 | Agent → shell tool | Run the commands required by the repository's owner instructions and verification contract. Retain their actual command, exit result, and evidence location, including failures. |
| 5 | Agent following `evidence` prepare mode **[New]** | Read `skills/evidence/SKILL.md`. Run `harnessctl evidence REPO --artifact WO-DEMO-010 --checkpoint handoff --json`, then fill its packet with the actual results and references. An empty packet proves nothing. |
| 6 | Main agent → optional `evidence-reviewer` **[New]** | Supply only the selected criteria, diff, and retained results. The read-only helper reports omissions; it cannot decide completion or independent assurance. |
| 7 | Agent → bundled `harnessctl` | Run review `preflight`, then `check --checkpoint handoff --from-git BASE`. Report the actual handoff result and completion decision. The Git-based handoff may update evidence and `handoff.json`, so invoke it deliberately. |

Evidence preparation is also directly available: ask Codex to use the `verity-plane evidence` skill, or invoke `/verity-plane:evidence prepare WO-DEMO-010` in Claude Code. Skills provide instructions; tools execute the named commands.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides implementation; `skills/evidence/SKILL.md` guides evidence preparation. | **New:** modes call existing commands. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action` for supported intended edits. | **Reuse:** host event. **New:** action mapping, registrations, and recursion protection. |
| **Script** | `scripts/harnessctl` runs harness checks; repository scripts run the project's checks. | **Adapt:** package the existing CLI. **Reuse:** actual project scripts. |
| **Tool/interface** | `apply_patch`, `Edit`, or `Write` edits; `exec_command`, `Bash`, or `PowerShell` runs commands. | **Reuse:** existing host tools. |
| **Evaluator** | Pre-action and handoff `check`, `evidence`, and review `preflight` evaluate scope and evidence. | **Reuse:** workflow compliance and evidence operations. |
| **Subagent** | `evidence-reviewer` optionally reports evidence gaps. | **New:** read-only helper with no artifact write or decision right. |
| **Human** | The affected owner decides changes outside approved scope. | **Reuse:** existing scope and remediation rights. |
| **External control** | Repository and credential protections restrict later external actions. | **Reuse:** protections actually configured. **New:** missing deterministic controls remain separate work in issue #347. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| An edit exceeds approved scope. | The agent stops that edit; a supported hook may also block it. | Follow [scenario 8](definition-and-approval.md#scenario-8-revise-approved-definitions-or-work-scope), then refresh the governing context. |
| Required checks fail. | Retain the failure and report the blocker. | Fix within scope and rerun the affected checks. |
| A shell operation has no reliable effect mapping. | Hook coverage is absent; declared paths do not prove arbitrary shell effects. | Keep the action within actual authority and inspect observed Git changes at handoff. |
| Evidence is missing or stale. | No successful handoff is claimed. | Retain actual results, refresh the packet, and repeat the affected checks. |

### 5. Example result

> Illustrative: The change for WO-DEMO-010 and its actual test results are retained. The handoff check passes; the WO remains `in_progress`. Next: resolve the implementation-completion decision through the permitted owner or delegated route.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py) and [workflow compliance](../../../se_harness/workflow_compliance.py) provide:

```sh
harnessctl check REPO --artifact WO-DEMO-010 --checkpoint pre-action --procedure PROC-WO-IMPLEMENT --changed-path src/example.py --changed-path tests/test_example.py --changes-complete --json
harnessctl evidence REPO --artifact WO-DEMO-010 --checkpoint handoff --json
harnessctl preflight REPO --work-order WO-DEMO-010 --phase review --json
harnessctl check REPO --artifact WO-DEMO-010 --checkpoint handoff --from-git BASE --json
```

Use the actual selected action's paths and comparison base. `--changes-complete` is a caller assertion. Review `preflight` is read-only; Git-based handoff can rebind evidence and write `handoff.json`.

**Proposed additions**

The two skill modes and `scripts/check-tool-action` call this same CLI. The hook adapter needs explicit supported-action mappings and must avoid recursion. The optional `evidence-reviewer` follows the [shared host registration](README.md#shared-component-names-and-calling-convention).

**Inputs, outputs, and writes**

- **Inputs:** Selected WO, approved criteria, intended paths, actual Git changes, comparison base, commands, and results.
- **Outputs:** Command results, evidence references, optional review findings, and handoff result.
- **Writes:** Code, tests, retained results, evidence packet, and possibly `handoff.json`. The helper writes none of these.

**Host differences**

Codex uses `apply_patch` and `exec_command`; an existing `write_stdin` session does not create a new `PreToolUse` event. Claude Code uses `Edit` / `Write` and `Bash` / native `PowerShell`. Neither host's hooks cover every possible effect; see [coverage limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement).

**Checks that demonstrate the behavior**

Proposed acceptance checks: retain real results before a completion handoff; reject an empty evidence packet or failed required check; inspect outputs after interruption before rerunning. Test the supported hook mappings separately from uncovered operations. Measure typical and slow check times over representative covered edits against the agreed performance budget. Optimize execution and invalidate any reusable computation when its inputs change; never skip a required gate or use a stale result for speed.

**Open questions**

Which host operations provide reliable intended paths for the first hook mappings? An arbitrary shell command cannot be declared covered merely because it ran through a shell tool.

</details>

## Scenario 11: Complete implementation and prepare verification

### 1. Purpose and starting point

**Purpose:** Record implementation completion, then prepare the exact candidate for assurance when required.

- **Starts when:** The handoff is ready and completion is the applicable next step within the existing request, or the user requests it directly.
- **Requires:** Passing completion gates and completion authority; an eligible candidate and preparation authority when a VREC is required.
- **Successful result:** The WO is `implemented`; when required, a VREC is `ready` for assurance.

### 2. Workflow

```text
change complete [New] → completion decision or eligible delegation
        ↓
Existing transition → preview → apply → WO is implemented
        ↓
When required: evidence prepare [New] → eligible candidate and authority
        ↓
Existing capture-verification → ready VREC → assurance handoff
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `change` skill **[New]** | Follow the applicable completion step without requiring a new invocation. Optional direct entry: ask Codex to use `verity-plane change`, or invoke `/verity-plane:change complete WO-DEMO-011` in Claude Code. Read the skill and refresh the handoff if its inputs changed. |
| 2 | Engineering owner, or eligible delegate | Establish the completion decision. Reuse existing authority when it covers this action. DR-015 delegation requires the PR-base class and current successful CI for the exact head. |
| 3 | Agent → bundled `harnessctl` | Preview `transition` to `WO-DEMO-011=implemented` with the actual actor, then apply while the reviewed content and authority still match. Run `check` for the WO and follow its next step. |
| 4 | Agent following `evidence` prepare mode **[New]** | If commit-bound verification is required, read `skills/evidence/SKILL.md`, identify the verification contracts and retained evidence, and establish an eligible clean candidate. Any Git commit needs its own actual authorization. |
| 5 | Agent and preparation actor | Present the proposed VREC ID, WOs, verification contracts, evidence paths, and current candidate. Reuse actual preparation authority or eligible DR-015 delegation that covers those inputs. Ask only if that authority is missing or no longer applies; completion authority alone does not imply it. |
| 6 | Agent → bundled `harnessctl` | Call `capture-verification` with those inputs. This existing command writes the ready VREC and evaluator evidence immediately; it has no preview flag. |
| 7 | Agent → bundled `harnessctl` | Run `check` for the new VREC. Report its actual state, bound commit, evidence, and assurance decision. Preparation is not verification. |

For `commit_bound_verification = "not_required"`, follow the evaluator's next step without creating an unnecessary VREC. [TRC-012](../../engineering/TRACEABILITY.md) allows this only for work that solely records or transports an already authorized governance decision. Applicable evidence and decisions still apply; mixed scope must be split or classified `required`.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides completion; `skills/evidence/SKILL.md` guides preparation. | **New:** distinct modes follow existing procedures. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action` before covered calls. | **Reuse:** host event. **New:** required applicable checks; no inferred completion or preparation authority. |
| **Script** | `scripts/harnessctl` runs the existing evaluator and provenance functions. | **Adapt:** bundle the runtime and CLI; no new preparation API. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` invokes `harnessctl` and separately authorized Git commands. | **Reuse:** existing tools. |
| **Evaluator** | `transition`, `capture-verification`, and `check` record completion and prepare evidence. | **Reuse:** workflow and provenance engine. |
| **Subagent** | `evidence-reviewer` may inspect selected evidence before preparation. | **New:** optional read-only helper; no preparation or assurance authority. |
| **Human** | The engineering owner decides completion; the permitted preparation actor authorizes preparation when required. | **Reuse:** distinct existing rights. |
| **External control** | The CI provider supplies live facts for eligible delegation. | **Reuse:** CI evidence; delegation does not grant Git or external-action authority. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Completion gates or required authority fail. | Do not apply completion; report the blocker. | Resolve it and refresh the affected handoff and preview. |
| Candidate worktree is dirty or evidence selection is invalid. | `capture-verification` refuses preparation. | Settle authorized changes and correct the inputs. |
| A Git commit needs authorization that has not been given. | Wait before that Git action. | Obtain the missing authorization, then recheck the resulting candidate. |
| Preparation is interrupted. | A VREC or evidence file may already exist. | Inspect its actual ID and writes before retrying; preserve history. |

### 5. Example result

> Illustrative: WO-DEMO-011 is `implemented`. VREC-DEMO-011 is `ready` and binds its retained evidence to the candidate. No verification or merge occurred. Next: the assurance owner reviews VREC-DEMO-011.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py), [workflow](../../../se_harness/workflow.py), and [provenance](../../../se_harness/provenance.py) provide:

```sh
harnessctl transition REPO --set WO-DEMO-011=implemented --decision WO-DEMO-011=ACTOR --json
harnessctl transition REPO --set WO-DEMO-011=implemented --decision WO-DEMO-011=ACTOR --apply --json
harnessctl check REPO --artifact WO-DEMO-011 --json
harnessctl capture-verification REPO --id VREC-DEMO-011 --work-order WO-DEMO-011 --verification VER-DEMO-011 --evidence EVIDENCE_PATH --owner PREPARATION_ACTOR --json
harnessctl check REPO --artifact VREC-DEMO-011 --json
```

`capture-verification` has no preview flag. It binds the eligible current checkout commit, not an agent-supplied candidate hash. The VREC belongs in a later governance commit than the candidate it names; it cannot contain its own future commit hash. Neither `ACTOR` nor `PREPARATION_ACTOR` authenticates a decision.

**Proposed additions**

The skill modes call the existing commands through `scripts/harnessctl`. Completion, preparation, and Git actions each need applicable authority, but authority already covering them is retained. Continue automatically through covered steps and present only a missing or changed decision. No extra transaction protocol is introduced.

**Inputs, outputs, and writes**

- **Inputs:** WO, handoff, completion decision, verification contracts, evidence, eligible candidate, and preparation authority.
- **Outputs:** Completion result and, when required, a ready VREC, candidate identity, and next assurance decision.
- **Writes:** WO completion event; VREC and evaluator evidence when required. Committing later governance records is a separate authorized Git action.

**Host differences**

Codex uses `exec_command`; Claude Code uses `Bash` / native `PowerShell`. Both use the bundled CLI. The optional reviewer and [hook limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement) are the same as scenario 10.

**Checks that demonstrate the behavior**

Proposed acceptance checks: capture a ready VREC for an eligible clean candidate; reject dirty or invalid preparation inputs; preserve historical records when the candidate changes. Confirm that a `not_required` WO follows its own next step while retaining applicable evidence and decisions.

**Open questions**

How will the host reliably bind actual completion and preparation decisions to the action being executed? The existing role arguments alone cannot enforce this.

</details>

## Scenario 12: Independently verify the candidate

### 1. Purpose and starting point

**Purpose:** Let the assurance owner judge whether retained evidence verifies the exact candidate.

- **Starts when:** A ready VREC reaches the assurance step within the existing request, or the user submits it through `evidence` **[New]**.
- **Requires:** The VREC's candidate, verification contracts, evidence, and accountable assurance owner.
- **Successful result:** The assurance owner's explicit decision is recorded on that VREC only.

### 2. Workflow

```text
evidence review [New] → read VREC, candidate, criteria, and evidence
        ↓
Existing check → transition checkpoint for verified
        ↓
Independent assurance owner decides
        ↓
Existing transition → preview → apply → report actual VREC state
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `evidence` skill **[New]** | Continue from VREC preparation when the request covers review preparation. Optional direct entry: ask Codex to use `verity-plane evidence`, or invoke `/verity-plane:evidence review VREC-DEMO-012` in Claude Code. Read `skills/evidence/SKILL.md`. |
| 2 | Agent → file and shell tools | Read the VREC, exact candidate, verification criteria, and retained evidence. Run `harnessctl check REPO --artifact VREC-DEMO-012 --checkpoint transition --target verified --json`. Present its gate results and unresolved findings. |
| 3 | Main agent → optional `evidence-reviewer` **[New]** | Ask the read-only helper to inspect the selected evidence and report gaps. Its observations support the human reviewer; they do not authorize verification. |
| 4 | Agent and assurance owner | Reuse the owner's actual independent assurance decision if it still covers this VREC, candidate, and evidence. Otherwise present only the missing or changed decision for the owner's review. DR-015 execution delegation does not cover assurance. |
| 5 | Agent → bundled `harnessctl` | Preview `transition` for the selected VREC and chosen outcome with the actual actor. Apply only while the reviewed VREC, candidate, evidence, and decision remain applicable. |
| 6 | Agent → bundled `harnessctl` | Run `check` for the VREC again. Report its actual outcome and next decision. Related WOs and release records do not change by inference; no merge occurs. |

The owner may choose a valid rejection or supersession instead. Rejection needs its reason; supersession needs an eligible successor. A separate model or a reviewer label does not establish independent human assurance: the review must satisfy the repository's role-separation policy.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/evidence/SKILL.md` guides review mode. | **New:** follows `PROC-VREC-DECIDE` and valid alternatives. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action` for a supported transition call. | **Reuse:** host event. **New:** mapping; it cannot authenticate the assurance owner. |
| **Script** | `scripts/harnessctl` runs the existing assurance checks and transition. | **Adapt:** package the current evaluator. |
| **Tool/interface** | `exec_command`, `Bash`, or `PowerShell` runs the CLI; the agent presents evidence to the owner. | **Reuse:** existing tools and human conversation. |
| **Evaluator** | Assurance checkpoint `check` and `transition` validate and record the selected outcome. | **Reuse:** gates and transition engine. |
| **Subagent** | `evidence-reviewer` optionally reports gaps for this candidate. | **New:** read-only helper; observations only. |
| **Human** | The assurance owner exercises `DR-VREC-DECIDE` after independent review. | **Reuse:** existing accountability and separation rules. |
| **External control** | Authenticated enforcement must prevent an agent from impersonating the assurance owner. | **New:** unresolved control requirement in issue #347; the CLI actor string is insufficient. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Evidence or candidate binding fails. | The evaluator refuses verification. | Repair through authorized work and prepare eligible evidence for the actual candidate. |
| The assurance owner has not decided. | The agent stops before apply; passing checks do not decide. | The actual assurance owner reviews and decides. |
| Reviewed inputs change. | Stop using a decision that no longer covers those inputs. | Present the changed candidate or evidence for the required review. |
| Owner rejects or supersedes the VREC. | Apply only that valid outcome and retain history. | Record the reason or eligible successor and follow the next step. |

### 5. Example result

> Illustrative: The assurance owner's decision changed VREC-DEMO-012 to `verified`. Its referenced WO is unchanged; no merge occurred. Next: the repository or release owner selects the delivery path.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

The [CLI](../../../se_harness/cli.py), [workflow engine](../../../se_harness/workflow.py), and [decision-rights policy](../../engineering/DECISION_RIGHTS.md) define the current path:

```sh
harnessctl check REPO --artifact VREC-DEMO-012 --checkpoint transition --target verified --json
harnessctl transition REPO --set VREC-DEMO-012=verified --decision VREC-DEMO-012=assurance-owner --json
harnessctl transition REPO --set VREC-DEMO-012=verified --decision VREC-DEMO-012=assurance-owner --apply --json
harnessctl check REPO --artifact VREC-DEMO-012 --json
```

`assurance-owner` is a role assertion, not authentication. Existing `transition --reason ID=TEXT` supplies a rejection reason; for supersession, the reason identifies the eligible successor VREC. Preserve the original candidate and evidence facts.

**Proposed additions**

The `evidence` review mode and optional reviewer make the existing sequence easier to use. Packaging the evaluator and adding a hook do not create authenticated decision enforcement; that gap remains explicit.

**Inputs, outputs, and writes**

- **Inputs:** VREC, evidence, candidate, actual assurance decision, and any required reason or successor.
- **Outputs:** Gate results, resulting VREC state, and next decision.
- **Writes:** The selected VREC's decision fields and lifecycle event. No inferred changes to related artifacts.

**Host differences**

Codex calls the CLI through `exec_command`; Claude Code uses `Bash` / native `PowerShell`. Optional subagents use the [shared host registrations](README.md#shared-component-names-and-calling-convention). Host tool permission is not an assurance decision.

**Checks that demonstrate the behavior**

Proposed acceptance checks: an authorized eligible transition changes only the selected VREC; invalid candidate or evidence binding blocks verification; changed implementation preserves historical records. A separate boundary test must prove that an agent cannot apply a forged human role. This proposal does not claim that control exists.

**Open questions**

Which authenticated control will enforce the human decision at the transition boundary? This must be resolved before claiming that the plugin guarantees independent assurance.

</details>

## Scenario 13: Authorize and perform integration

### 1. Purpose and starting point

**Purpose:** Integrate eligible work under the repository owner's exact decision.

- **Starts when:** Integration is the selected next step within the existing request, or the repository owner requests it directly.
- **Requires:** Applicable verified coverage, exact PR/head/target and merge method, action-specific authority, and all required controls at the external effect.
- **Successful result:** An authorized agent or human executes the permitted merge through existing project tools, and its observed result is reported.

### 2. Workflow

```text
change integrate [New] → harnessctl check → inspect the exact PR
        ↓
Reuse exact owner authority → check current coverage and external controls
        ↓
Authorized agent or human executes through the protected project route
        ↓
Agent reads remote state and reports the actual result
```

| Step | Who acts | Action and result |
| --- | --- | --- |
| 1 | Main agent → `change` skill **[New]** | Continue when integration is the applicable selected step and the request covers it. Optional direct entry: ask Codex to use `verity-plane change`, or invoke `/verity-plane:change integrate PR_URL` in Claude Code. Read `skills/change/SKILL.md`. |
| 2 | Agent → bundled `harnessctl` | Run `check` for the selected WO or VREC and follow the returned delivery procedure. Present applicable coverage and the repository owner's integration decision. The existing integration procedure performs no merge. |
| 3 | Agent → shell tool → existing `gh` | Read the exact PR, current head, target branch and commit, reviews, and checks through the existing GitHub interfaces. Reuse the actual owner decision only while it covers that action, head, target, and method. Ask only for missing or materially changed authority. Green CI alone does not authorize merging. |
| 4 | Authorized agent or human → protected GitHub route | Check all current gates and independently enforced external controls. When they are demonstrated, the authorized agent may execute with existing `gh pr merge` and the permitted method; a human may use the same permitted project route. A covered tool call also runs `scripts/check-tool-action` before the effect. Missing or unproven external enforcement disables agent automation and produces a specific enforcement blocker. |
| 5 | Agent → existing `gh` | Read the PR state and resulting merge commit after execution. Report merged, still open, or unknown from observed remote facts. Do not infer WO, VREC, or release-state changes. |

There is no `harnessctl merge`. The human retains the decision right; an authorized agent may execute it. Verification or release approval does not imply merge authority. Agent execution requires demonstrated independent enforcement under [issue #347](https://github.com/mmzen/se_harness/issues/347); this note does not claim those controls already exist. When they are missing, report that exact blocker. A human may use an existing permitted protected route, but an extra human execution step is not a permanent plugin requirement.

### 3. Components and implementation mapping

| Component | Role in this scenario | Current implementation → proposed change |
| --- | --- | --- |
| **Skill** | `skills/change/SKILL.md` guides integrate mode, reusing applicable authority. | **New:** follows existing `PROC-REPOSITORY-INTEGRATION`. |
| **Hook** | `PreToolUse` calls `scripts/check-tool-action` before covered external-action requests. | **Reuse:** host event. **New:** required applicable checks; these do not replace independent merge controls. |
| **Script** | `scripts/harnessctl` runs the selected harness check. | **Adapt:** package the existing CLI; no merge script. |
| **Tool/interface** | Shell tools run harness and GitHub reads, then authorized `gh pr merge`; a human can use GitHub. | **Reuse:** existing CLI and protected project interfaces. |
| **Evaluator** | `check` reports applicable coverage and the delivery decision. | **Reuse:** existing procedure; no integration command is added. |
| **Subagent** | Not used. | **Not used:** another agent cannot authorize integration. |
| **Human** | The repository owner retains the exact decision right; execution may be delegated to an authorized agent. | **Reuse:** existing delivery and external-action rights; no new delegation waiver. |
| **External control** | GitHub rules, required checks, reviewers, and credential restrictions protect the actual merge route. | **Reuse:** controls actually configured. **New:** missing deterministic enforcement remains issue #347. |

### 4. Stops, decisions, and recovery

| Situation | What happens | How it resumes |
| --- | --- | --- |
| Applicable verification or exact merge authority is missing. | The agent reports only the missing requirement. | Complete the required coverage or obtain the missing owner decision; keep decisions that still apply. |
| Required deterministic controls are absent or unproven. | Disable agent execution and name the enforcement blocker. | Establish the required controls, or let a human use an existing permitted protected route. Human execution is not a substitute for a control that the route itself requires. |
| PR head, target, or action changes. | Earlier review may no longer cover the action. | Revalidate coverage and refresh authority where needed. |
| A local hook is disabled or bypassed. | Instructions alone cannot prevent an external effect. | Enforce required checks and credential restrictions outside the agent's editable workspace. |
| A merge response is lost. | The outcome is unknown, not automatically failed. | Read actual PR and target state before any retry. |

### 5. Example result

> Illustrative: The existing owner decision still covers this PR, head, target, and merge method. Agent execution is blocked because independent authority enforcement has not been demonstrated; no new approval is requested and no merge occurred. Next: resolve the identified enforcement gap through the repository's permitted process.

### 6. Implementation details

<details>
<summary>Commands, sources, host differences, and checks</summary>

**Current implementation**

[WORKFLOW.json](../../engineering/WORKFLOW.json) defines `PROC-REPOSITORY-INTEGRATION` as a delivery decision. The [merge-boundary analysis](../plugin-installation-proposal-2026-09-06.md#the-merge-boundary-must-stand-on-its-own) explains the independent control requirement.

```sh
harnessctl check REPO --artifact VREC-DEMO-012 --json
```

This projects state and the next decision; it grants no merge authority. Existing GitHub CLI reads can establish the remote facts:

```sh
gh pr view PR_URL --json number,url,state,headRefOid,baseRefName,reviewDecision,statusCheckRollup,mergeCommit
gh pr checks PR_URL
```

Use the actual PR URL. These commands do not prove that live repository protection and credential settings cover every route.

For a merge commit explicitly covered by the owner's decision, the existing execution command is:

```sh
gh pr merge PR_URL --merge --match-head-commit HEAD_SHA
```

`HEAD_SHA` is the authorized exact PR head. Use only the permitted merge method. This safeguard checks the head, not the owner's identity or target-state authority; those require independent controls at the effect. Do not add `--admin` or other bypasses. If the project uses a merge queue, its queued execution and later target state must also remain within authority and pass its enforced checks.

**Proposed additions**

`change` integrate mode follows existing tools through preparation and authorized execution. It reuses matching decisions and asks only for missing or changed authority. No new merge API is added. Agent execution is enabled only when independent controls authenticate authority and prevent unauthorized effects through GitHub APIs, direct Git access, and alternative credentials.

VRECs live in later governance commits than their verified candidate. A future enforcement design must check the implementation and permitted later governance changes; requiring a VREC to name its own commit is impossible. Agent-editable branch content must not waive the trusted rules.

**Inputs, outputs, and writes**

- **Inputs:** Exact PR, head, target, merge method, applicable coverage, repository controls, and owner authority.
- **Outputs:** A missing-decision or enforcement blocker, or the observed remote result and merge commit.
- **Writes:** The authorized agent's or human's merge changes the remote repository. Preparation and status reads do not.

**Host differences**

Codex uses `exec_command`; Claude Code uses `Bash` / native `PowerShell` for the same GitHub CLI. Covered execution requests run the applicable `scripts/check-tool-action` checks. Both hosts have [coverage limits](../plugin-installation-proposal-2026-09-06.md#hooks-useful-intervention-incomplete-enforcement), so neither substitutes for independent protections.

**Checks that demonstrate the behavior**

Proposed acceptance checks: matching existing authority permits execution without another prompt; missing or changed authority stops only the affected action; absent external enforcement disables agent execution. Verify current gates, exact head and target checks, alternate API/Git routes, the observed merge commit, and a status read before retry after an ambiguous response. A reused decision never skips a required gate.

**Open questions**

Which GitHub rules and credential restrictions will close issue #347 for every supported integration route? This is separate enforcement work, not an extra plugin skill or command.

</details>
