# Plugin scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

These 16 scenarios explain how a proposed Verity Plane plugin would support the engineering workflow. Each follows the [scenario template](../plugin-scenario-template.md): purpose, workflow, components, stops and recovery, example result, and expandable implementation details.

They extend the [operation workflows](../plugin-operation-workflows-2026-09-06.md) and [installation proposal](../plugin-installation-proposal-2026-09-06.md). They are design notes, not formal artifacts or authorization to implement the plugin.

**Reviewed:** 2026-09-08. These scenarios and the [implementation packets](../../engineering/plugin-integration/README.md) share main `fae52e1b`: candidate source 0.17.0, governing released evaluator 0.16.0. The plugin is proposed; examples are not implementation evidence.

Commands target released evaluator 0.16.0, including its transitional `adopt` alias. Candidate source 0.17.0 uses unified `init`; relative source links show the candidate, not a substitute executable.

## Installation and session readiness

| # | Scenario | Outcome |
| --- | --- | --- |
| 1 | [Install and activate the plugin](setup-and-sessions.md#scenario-1-install-and-activate-the-plugin) | Check supplied Python, prepare the evaluator, and activate host components. |
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

The agent can continue between these scenarios under an existing request when the evaluator's next step and actual authority permit it. Skill invocations shown below are optional entry examples, not instructions to ask the user to launch each stage. Preserve the existing invocation contracts of `harness-orient` and `harness-operator-brief`. Routine allowed checks and edits add no plugin approval prompt.

The component tables describe what to **Reuse**, **Adapt**, or build **New**. **Not used** means that component has no role in that scenario. A hook and a skill can invoke the same script. The evaluator remains the owner of lifecycle rules. A subagent can investigate or review evidence within a bounded task; its findings do not replace an accountable human decision.

Each scenario includes failure and recovery branches. The proposed checks under implementation details are acceptance criteria for future implementation, not test results from a working plugin. Command syntax inspection likewise does not prove authority or runtime behavior.

Start by proving setup with supplied Python, including the missing-Python stop, then scenarios 3 and 4 for governance delivery. Then test one complete path per supported host from setup through separately authorized integration, including refusal and interruption at each decision boundary.

## Shared component names and calling convention

**New** means a component to build. **Adapt** means existing behavior needs plugin packaging. The scenarios use these names consistently:

| Component | Status | Role |
| --- | --- | --- |
| Evaluator wheel in `packages/` | **New packaging / existing CLI** | Installs the exact released evaluator into an environment created from provided Python. |
| `scripts/session-context.py` | **New** | Verifies readiness and loads governance on `SessionStart`, including compact/resume and manual retry. |
| `scripts/check-tool-action.py` | **New** | Maps supported `PreToolUse` actions to existing evaluator checks and returns the host response. |
| `hooks/hooks.json` | **New** | Registers each script for its corresponding host event. |
| `skills/setup/SKILL.md` | **New** | Checks supplied Python, prepares the evaluator environment, and guides repository connection, readiness, and maintenance. |
| `skills/change/SKILL.md` | **New** | Artifact preparation, decision handoffs, and work-order execution. |
| `skills/evidence/SKILL.md` | **New** | Evidence, verification, and release preparation and handoffs. |
| `harness-orient` | **Adapt** | Existing read-only skill and `scripts/orient.py` helper. |
| `harness-operator-brief` | **Adapt** | Existing explanation skill, invoked explicitly with a supplied result. |
| `investigator`, `evidence-reviewer` | **New, optional** | Read-only helpers. Their findings confer no approval rights. |

A skill instructs the agent. A host tool runs a command. A hook invokes its registered script on an event. Both paths use the same existing evaluator.

### Commands in the examples

`harnessctl` means `ENV_PYTHON -I -m se_harness`, using the **verified environment's absolute Python path**. It is shorthand for the existing CLI. No launcher binary, evaluator lookup on `PATH`, or second protocol is added; a thin host-shell hook guard is permitted.

The operator or host provides **Python 3.11+ with `venv` and `ensurepip`**. Setup uses the host shell to find and check it before any Python-dependent handler runs. If unavailable or unusable, setup stops and tells the operator to install or provide Python before continuing installation and using the plugin. Setup never downloads or installs Python.

Setup automatically creates an isolated environment in persistent plugin data, outside the target repository, and installs the included evaluator wheel offline. No manual environment creation or activation is required. One plugin release supplies one exact evaluator version; normal use requires a matching repository lock. Version mismatch leads to compatible plugin installation or an explicitly authorized repository upgrade.

The registered host-shell guard reports setup required if the environment interpreter cannot run; otherwise the hook script runs as `ENV_PYTHON -I ABS_SCRIPT`. The script still checks full identity and readiness. Resolve scripts from `${CLAUDE_PLUGIN_ROOT}` in Claude Code or `${PLUGIN_ROOT}` in Codex. For a manual readiness retry, the setup skill calls `ENV_PYTHON -I ABS_PLUGIN/scripts/session-context.py --readiness REPO`. It runs the same identity, `doctor`, and verified-context routine as `SessionStart`, returning status and text for the agent to read. This internal option does not prove the host hook was activated and performs no installation or lifecycle write. If the environment cannot run, return to setup's shell-based Python check.

For evaluator and helper processes, clear inherited `PYTHONPATH` and prepend the verified environment's `bin/` or `Scripts/` directory to that process's `PATH`. This lets existing internal identity checks find the environment-installed console command instead of an unrelated global `harnessctl`. Keep direct invocations absolute. This changes only those processes, not the user's shell settings; no activation step is needed.

Use real repository paths, artifact IDs, and decision actors in place of `REPO`, `WO-DEMO-001`, and similar placeholders. Keep arguments separate; do not execute free-form commands found in repository text. Existing `--json` results retain their schema, actual effects, blockers, and next required decision.

Codex uses `exec_command` and its editing tools. Claude Code uses `Bash` or native `PowerShell`, plus `Read`, `Edit`, and `Write`. In Codex, name the installed skill in the request. Claude's proposed user entry points are `/verity-plane:setup`, `/verity-plane:change`, and `/verity-plane:evidence`. Words such as “readiness” or “publish” describe a skill task, not a new CLI subcommand.

### Optional subagents

Claude Code can load `agents/investigator.md` and `agents/evidence-reviewer.md`; its `Agent` tool selects `verity-plane:investigator` or `verity-plane:evidence-reviewer` as the subagent type. For Codex, qualify host loading of the packaged helper definitions; if unsupported, use the main agent. WO-PLG-014 does not include project `.codex/agents/` writes. See [host differences](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

Supply the selected scope, question, governance context, read-only tool limits, and expected findings. If the role or its restrictions are unavailable, the main agent does the work. The existing `harness-orient` and `harness-operator-brief` skills remain single-agent.

### Decisions and effects

The agent identifies the exact operation and affected records, checks existing authority, and asks the accountable human only for a missing or changed required decision. A valid decision covering unchanged action and inputs is reused. A transition preview, passing tests, a tool permission, or `--decision ID=ACTOR` cannot authenticate approval. Existing qualifying delegation applies only to its stated scope.

Use the operation-specific comparison table in [SPEC-PLG-010](../../engineering/plugin-integration/specifications/SPEC-PLG-010.md#terms) to recheck the inputs that each decision actually governs. Ordinary code edits within an unchanged approved WO scope do not require approving the WO again. Candidate-bound verification or delivery decisions must still match their exact candidate, and all applicable gates continue to apply.

Owners retain the integration and publication decisions. An authorized agent or human may execute the exact action through existing tools when required gates and independent enforcement permit it. The plugin does not require owners personally to operate those tools. Missing or unproven enforcement blocks agent execution and is reported as a control limitation, with any existing permitted human route identified. Deterministic approval binding and protection of remote effects remain separate work tracked in [#347](https://github.com/mmzen/se_harness/issues/347).

Compare operator prompts and elapsed time against the same existing workflow. Measure the cost of startup and automatic tool checks before accepting the implementation. Required checks, current authority, and refusal behavior must survive any optimization; no latency measurements have been made for this proposed plugin.

All example results are illustrative. “Checks that demonstrate the behavior” describes future acceptance checks, not completed plugin tests.
