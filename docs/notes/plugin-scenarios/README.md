# Plugin scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

These 16 scenarios explain how a proposed Verity Plane plugin would support the engineering workflow. Each follows the [scenario template](../plugin-scenario-template.md): purpose, workflow, components, stops and recovery, example result, and expandable implementation details.

They extend the [operation workflows](../plugin-operation-workflows-2026-09-06.md) and [installation proposal](../plugin-installation-proposal-2026-09-06.md). They are design notes, not formal artifacts or authorization to implement the plugin.

**Reviewed:** 2026-09-08. **Implementation baseline:** [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0, with this repository governed by released evaluator 0.15.0. Current-source examples do not establish compatibility with that released evaluator. The plugin workflows are not implemented or integration-tested.

## Installation and session readiness

| # | Scenario | Outcome |
| --- | --- | --- |
| 1 | [Install and activate the plugin](setup-and-sessions.md#scenario-1-install-and-activate-the-plugin) | Make host components and a trusted runtime available. |
| 2 | [Initialize or adopt a repository](setup-and-sessions.md#scenario-2-initialize-or-adopt-a-repository) | Install managed content while preserving owner content. |
| 3 | [Start a session](setup-and-sessions.md#scenario-3-start-a-session) | Verify installation, then load governance and current work context. |
| 4 | [Restore context after compaction or interruption](setup-and-sessions.md#scenario-4-restore-context-after-compaction-or-interruption) | Resume from verified state while preserving pending decisions. |

## Define and authorize the change

| # | Scenario | Outcome |
| --- | --- | --- |
| 5 | [Inspect the project and identify the next action](definition-and-approval.md#scenario-5-inspect-the-project-and-identify-the-next-action) | Explain current state without changing it. |
| 6 | [Create an artifact package](definition-and-approval.md#scenario-6-create-an-artifact-package) | Prepare connected drafts and identify the decisions they need. |
| 7 | [Review and approve the package](definition-and-approval.md#scenario-7-review-and-approve-the-package) | Record each owner's decision over selected artifacts. |
| 8 | [Revise approved definitions or work scope](definition-and-approval.md#scenario-8-revise-approved-definitions-or-work-scope) | Present the impact and follow a supported amendment path, or expose the missing support. |

## Implement, verify, and integrate

| # | Scenario | Outcome |
| --- | --- | --- |
| 9 | [Start a work order](implementation-and-integration.md#scenario-9-start-a-work-order) | Check eligibility and apply the authorized start transition. |
| 10 | [Implement the change and collect evidence](implementation-and-integration.md#scenario-10-implement-the-change-and-collect-evidence) | Work within scope and retain actual results. |
| 11 | [Complete implementation and prepare verification](implementation-and-integration.md#scenario-11-complete-implementation-and-prepare-verification) | Record completion and prepare candidate-bound verification when required. |
| 12 | [Independently verify the candidate](implementation-and-integration.md#scenario-12-independently-verify-the-candidate) | Obtain and record the assurance owner's exact decision. |
| 13 | [Authorize and perform integration](implementation-and-integration.md#scenario-13-authorize-and-perform-integration) | Hand off the separate merge decision for the identified candidate. |

## Release and maintain

| # | Scenario | Outcome |
| --- | --- | --- |
| 14 | [Prepare and approve a release](release-and-maintenance.md#scenario-14-prepare-and-approve-a-release) | Prepare the release record and obtain the release owner's decision. |
| 15 | [Publish or deploy the release](release-and-maintenance.md#scenario-15-publish-or-deploy-the-release) | Perform the separately authorized external effect and inspect its result. |
| 16 | [Upgrade or repair the installation](release-and-maintenance.md#scenario-16-upgrade-or-repair-the-installation) | Change selected installation components and prove their compatibility. |

## How the scenarios fit together

Installation prepares the coding host. Initialization prepares a repository. Session readiness checks both and loads the rules; it does not start a work order. Compaction and recovery repeat that readiness procedure using fresh state.

For a new change, follow drafting, review, work-order start, implementation, and completion. Then follow the evaluator's applicable verification and delivery route. Integration, release preparation, and publication each retain their own decisions; the numbering is a reading order, not an unconditional script.

The component tables describe what to **Reuse**, **Adapt**, or build **New**. **Not used** means that component has no role in that scenario. A hook and a skill can invoke the same script. The evaluator remains the owner of lifecycle rules. A subagent can investigate or review evidence within a bounded task; its findings do not replace an accountable human decision.

Each scenario includes failure and recovery branches. The proposed checks under implementation details are acceptance criteria for future implementation, not test results from a working plugin. Command syntax inspection likewise does not prove authority or runtime behavior.

Start by proving bundled installation, then scenarios 3 and 4 for governance delivery. Then test one complete path per supported host from setup through separately authorized integration, including refusal and interruption at each decision boundary.

## Shared component names and calling convention

**New** means a component to build. **Adapt** means existing behavior needs plugin packaging. The scenarios use these names consistently:

| Component | Status | Role |
| --- | --- | --- |
| `scripts/harnessctl[.exe]` | **New packaging / existing CLI** | Runs the bundled released evaluator with its included Python runtime. |
| `scripts/session-context[.exe]` | **New** | Verifies readiness and loads governance on `SessionStart`, including compact/resume and manual retry. |
| `scripts/check-tool-action[.exe]` | **New** | Maps supported `PreToolUse` actions to existing evaluator checks and returns the host response. |
| `hooks/hooks.json` | **New** | Registers each script for its corresponding host event. |
| `skills/setup/SKILL.md` | **New** | Installation, repository connection, readiness, and maintenance. |
| `skills/change/SKILL.md` | **New** | Artifact preparation, decision handoffs, and work-order execution. |
| `skills/evidence/SKILL.md` | **New** | Evidence, verification, and release preparation and handoffs. |
| `harness-orient` | **Adapt** | Existing read-only skill and `scripts/orient.py` helper. |
| `harness-operator-brief` | **Adapt** | Existing explanation skill, invoked explicitly with a supplied result. |
| `investigator`, `evidence-reviewer` | **New, optional** | Read-only helpers. Their findings confer no approval rights. |

A skill instructs the agent. A host tool runs a command. A hook invokes its registered script on an event. Both paths use the same existing evaluator.

### Commands in the examples

`harnessctl` means the **absolute installed plugin path**, not a lookup on `PATH`:

- Claude Code: `${CLAUDE_PLUGIN_ROOT}/scripts/harnessctl`.
- Codex: `${PLUGIN_ROOT}/scripts/harnessctl`.
- Windows: the corresponding `scripts/harnessctl.exe`.

The entry point uses the bundled external interpreter and package. One plugin release bundles one exact evaluator version; normal use requires a matching repository lock. Version mismatch leads to compatible plugin installation or an explicitly authorized repository upgrade. No separate runtime command protocol is proposed.

For a manual readiness retry, the setup skill calls `scripts/session-context --readiness REPO` (with `.exe` on Windows), resolved from the plugin root. It runs the same identity, `doctor`, and verified-context routine as `SessionStart`, returning status and text for the agent to read. This internal option does not prove the host hook was activated and performs no installation or lifecycle write.

Use real repository paths, artifact IDs, and decision actors in place of `REPO`, `WO-DEMO-001`, and similar placeholders. Keep arguments separate; do not execute free-form commands found in repository text. Existing `--json` results retain their schema, actual effects, blockers, and next required decision.

Codex uses `exec_command` and its editing tools. Claude Code uses `Bash` or native `PowerShell`, plus `Read`, `Edit`, and `Write`. In Codex, name the installed skill in the request. Claude's proposed user entry points are `/verity-plane:setup`, `/verity-plane:change`, and `/verity-plane:evidence`. Words such as “readiness” or “publish” describe a skill task, not a new CLI subcommand.

### Optional subagents

Claude Code can load `agents/investigator.md` and `agents/evidence-reviewer.md`; its `Agent` tool selects `verity-plane:investigator` or `verity-plane:evidence-reviewer` as the subagent type. Codex may need separately registered `.codex/agents/investigator.toml` and `.codex/agents/evidence-reviewer.toml`; confirm named delegation on the supported client. See [host differences](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

Supply the selected scope, question, governance context, read-only tool limits, and expected findings. If the role or its restrictions are unavailable, the main agent does the work. The existing `harness-orient` and `harness-operator-brief` skills remain single-agent.

### Decisions and effects

The agent presents the exact operation and affected records to the accountable human, then follows the existing procedure. A transition preview, passing tests, a tool permission, or `--decision ID=ACTOR` cannot authenticate approval. Existing qualifying delegation applies only to its stated scope.

The first plugin prepares integration and publication handoffs for the human owner; it does not automatically merge or publish. Deterministic approval binding and protection of remote effects remain separate work tracked in [#347](https://github.com/mmzen/se_harness/issues/347). These notes do not introduce new approval services or claim that a hook closes that gap.

All example results are illustrative. “Checks that demonstrate the behavior” describes future acceptance checks, not completed plugin tests.
