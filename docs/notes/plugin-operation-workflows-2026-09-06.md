# Plugin workflows: who does what

<!-- Target expertise: 3.5/10. This score describes the knowledge expected from the reader. -->

> Revised 2026-09-08. Companion to the [installation proposal](plugin-installation-proposal-2026-09-06.md).
> Maps [source `aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate 0.16.0. The repository's released evaluator is 0.15.0. The proposed plugin is not implemented; examples describe inspected CLI syntax, not a tested plugin.

## First, distinguish the components

| Component | Meaning | Example |
| --- | --- | --- |
| **Skill** | Instructions the agent follows. | New `change` skill explains how to create a package or start a WO. |
| **Tool** | Host capability the agent invokes. | Codex `exec_command` or Claude Code `Bash` runs a command; an editing tool changes a file. |
| **Script** | Code that performs a defined operation. | New `scripts/hook-handler` translates a host event. |
| **Hook** | An event that automatically invokes the handler. | `SessionStart` triggers installation checks and governance injection. |
| **Evaluator** | Existing SE Harness engine, exposed as `harnessctl`. | Checks scope, computes next actions, and applies permitted transitions. |
| **Subagent** | Optional helper with a bounded task. | New read-only `investigator` finds relevant artifacts. |
| **Human** | Accountable decision owner. | Assurance owner decides whether to verify the candidate. |

A hook handler and a skill-guided agent can call the **same** `scripts/harnessctl`. There is one evaluator and no second lifecycle implementation in the plugin.

```text
User requests work
  -> Agent reads the skill
  -> Agent calls a host tool
  -> Host runs PreToolUse handler, where supported
  -> Tool invokes plugin scripts/harnessctl
  -> Evaluator returns result, blockers, and next action
  -> Agent explains the result or hands off the required decision
```

A covered hook may deny a tool call. Hook coverage is incomplete; evaluator checks still apply to its own operations. Protection of remote effects needs [independent controls](plugin-installation-proposal-2026-09-06.md#the-merge-boundary-must-stand-on-its-own).

## Where the pieces would live

The plugin contains the released evaluator and portable Python, `scripts/harnessctl[.exe]`, one `scripts/hook-handler[.exe]`, host manifests, hooks, and skills. See the [package layout](plugin-installation-proposal-2026-09-06.md#architecture-one-engine-two-adapters).

**Three new skills:** `setup`, `change`, `evidence`. **Two adapted skills:** `harness-orient`, `harness-operator-brief`. Optional `investigator` and `evidence-reviewer` roles are new and read-only.

The runtime lives in the installed plugin, outside the target repository. Artifacts, work orders, evidence, and governing policy stay in the repository. A plugin update does not upgrade that policy or its evaluator lock.

## Operation map

Each row links to the full sequence, including current commands, new components, stops, and recovery.

| Operation | Skill / agent action | Hook or script role | Required handoff |
| --- | --- | --- | --- |
| [Install](plugin-scenarios/setup-and-sessions.md#scenario-1-install-and-activate-the-plugin) | User installs the host plugin, which includes `harnessctl` and Python. | Host loads components; handler checks availability. | Resolve missing trust or an incompatible bundle. |
| [Connect repository](plugin-scenarios/setup-and-sessions.md#scenario-2-initialize-or-adopt-a-repository) | `setup` previews existing `init` or `adopt`, then runs the authorized operation. | Handler checks readiness afterward. | User approves the concrete repository changes. |
| [Start / restore session](plugin-scenarios/setup-and-sessions.md#scenario-3-start-a-session) | `harness-orient` reads the selected state when needed. | `SessionStart` checks identity and `doctor`, then injects governance; repeat on compact/resume. | Resolve failed checks or incomplete context before governed work. |
| [Create package](plugin-scenarios/definition-and-approval.md#scenario-6-create-an-artifact-package) | `change` uses `scaffold-domain`, `create-artifact`, and editing tools. | Same bundled CLI; optional investigator locates existing definitions. | Review connected drafts. Creation does not approve them. |
| [Approve / revise](plugin-scenarios/definition-and-approval.md#scenario-7-review-and-approve-the-package) | `change` presents exact content and existing transition previews. | CLI checks legality; editing follows the applicable amendment procedure. | Actual owners decide; apply only their selected changes. |
| [Start WO](plugin-scenarios/implementation-and-integration.md#scenario-9-start-a-work-order) | `change` runs `preflight` and an authorized `transition` to `in_progress`. | Handler checks covered tool actions. | Human or qualifying existing delegation supplies start authority. |
| [Implement](plugin-scenarios/implementation-and-integration.md#scenario-10-implement-the-change-and-collect-evidence) | Main agent edits within scope and runs project checks. `evidence` retains real results. | Mapped `PreToolUse` checks assist scope enforcement. | Stop on a scope change or failed required check. |
| [Prepare verification](plugin-scenarios/implementation-and-integration.md#scenario-11-complete-implementation-and-prepare-verification) | `evidence` guides completion, then uses `capture-verification` when required and authorized. | Existing CLI binds the VREC to the eligible candidate. | Assurance owner reviews the exact record and evidence. |
| [Verify / integrate](plugin-scenarios/implementation-and-integration.md#scenario-12-independently-verify-the-candidate) | Present verification transition and the separate integration decision. | Existing CLI records the authorized VREC state. No plugin auto-merge. | Assurance owner verifies; integration owner uses the project's GitHub process. |
| [Release / publish](plugin-scenarios/release-and-maintenance.md#scenario-14-prepare-and-approve-a-release) | `evidence` uses `prepare-release` and the project's existing release tools. | CLI prepares RLS; project workflows perform external effects. | Release owner decides; publication is separately authorized and handed off. |
| [Upgrade / repair](plugin-scenarios/release-and-maintenance.md#scenario-16-upgrade-or-repair-the-installation) | `setup` guides compatible plugin installation or existing `upgrade`. | Re-run identity and installation checks. | Repository upgrade remains explicit; startup never applies it. |

## What a direct call looks like

In these notes, `harnessctl` is shorthand for the installed plugin's absolute `scripts/harnessctl` path (or `harnessctl.exe` on Windows). `REPO`, `ACTOR`, and example IDs are placeholders, not literal inputs.

For a new or empty directory, the setup skill instructs the agent to run:

```text
harnessctl init REPO --dry-run --json
```

It presents the proposed changes. Once authorized, the agent repeats the command without `--dry-run`. For a nonempty directory, use `adopt`. There is no `--apply` flag for either command.

For a selected work order:

```text
harnessctl preflight REPO --work-order WO-DEMO-001 --phase start --json
harnessctl transition REPO --set WO-DEMO-001=in_progress --decision WO-DEMO-001=ACTOR --json
```

The transition is a preview. Add `--apply` only after the actual start authority is established. `--decision` records an actor assertion; it does not authenticate that person.

The CLI already provides the operation names and results. Skills and the hook handler preserve arguments and supported JSON schemas; they do not turn a returned decision request into a shell command.

## Details that must stay correct

- **Inspecting is not changing state.** `check` without a checkpoint projects the selected state; it does not pass gates. `preflight` is read-only.
- **Some checks write evidence.** A Git-based handoff check can rebind a packet and retain `handoff.json`; do not run it from a generic read-only startup hook.
- **Preparation is not approval.** `capture-verification` and `prepare-release` write records immediately and have no dry-run mode. Each needs its preparation prerequisites and authorization.
- **Evidence is real output.** Generated evidence templates do not prove tests passed. Retain actual results and candidate references.
- **Verification, integration, and publication are separate.** A verified VREC or released RLS does not itself merge, upload, or deploy. The enforcement gap in [#347](https://github.com/mmzen/se_harness/issues/347) remains open implementation work.

## Implementation map and remaining work

| Existing source | Plugin use | Work to add |
| --- | --- | --- |
| [CLI](../../se_harness/cli.py), [runtime identity](../../se_harness/runtime_identity.py) | Same released commands and identity checks. | Bundle runtime; test exact versions and supported platforms. |
| [Installer](../../se_harness/installer.py) | `init`, `adopt`, `upgrade`. | Setup skill and host registration; preserve owner content. |
| [Artifact layout](../../se_harness/artifact_layout.py) | Domain and individual artifact creation. | Change skill coordinates drafts; no atomic package promise. |
| [Preflight](../../se_harness/preflight.py), [compliance](../../se_harness/workflow_compliance.py) | Readiness and explicit checkpoints. | Hook event mapping, bounded execution, recursion protection. |
| [Workflow](../../se_harness/workflow.py), [result schemas](../../se_harness/workflow_result.py) | Transitions and canonical next steps. | Skills explain results and wait at real decision boundaries. |
| [Provenance](../../se_harness/provenance.py) | Candidate-bound verification and release records. | Evidence skill connects existing operations and human review. |

Use the [scenario template](plugin-scenario-template.md) for the [16 scenarios](plugin-scenarios/README.md). Test a full path on each host, including refusal, interruption, compaction, and missing approval; successful plugin loading alone proves none of those behaviors.