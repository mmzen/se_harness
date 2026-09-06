# Plugin scenarios

<!-- Target expertise: 3.5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

These 16 scenarios explain how a proposed Verity Plane plugin would support the engineering workflow. Each follows the [scenario template](../plugin-scenario-template.md): purpose, workflow, components, stops and recovery, example result, and expandable implementation details.

They extend the [operation workflows](../plugin-operation-workflows-2026-09-06.md) and [installation proposal](../plugin-installation-proposal-2026-09-06.md). They are design notes, not formal artifacts or authorization to implement the plugin.

**Reviewed:** 2026-09-06. **Implementation baseline:** [`aad82a9`](https://github.com/mmzen/se_harness/tree/aad82a9d03e142b27cb3dc3d0a1ecc38d2d7e055), candidate source 0.16.0, with this repository governed by released evaluator 0.15.0. Current-source examples do not establish compatibility with that released evaluator. The plugin workflows are not implemented or integration-tested.

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
| 13 | [Authorize and perform integration](implementation-and-integration.md#scenario-13-authorize-and-perform-integration) | Enforce the separate decision to merge the identified candidate. |

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

Start implementation design with scenarios 3 and 4 to settle governance delivery. Then test one complete path per supported host from setup through separately authorized integration, including refusal and interruption at each decision boundary.

## Shared component names and calling convention

The scenarios use the same names throughout. **Existing** means present in the inspected repository or host. **New** means a proposed component or interface to build. Skill modes such as `setup readiness` are new instructions, not current `harnessctl` subcommands.

| Component | Status | What it does |
| --- | --- | --- |
| `harness-orient` | **Existing** | Inspects an installed project through its existing `scripts/orient.py` helper; it does not change state. |
| `harness-operator-brief` | **Existing** | Explains a supplied evaluator result when explicitly requested. |
| `skills/setup/SKILL.md` | **New** | Guides runtime setup, repository connection, readiness, and maintenance. |
| `skills/change/SKILL.md` | **New** | Guides artifact drafting, review, amendments, and work-order execution and integration. |
| `skills/evidence/SKILL.md` | **New** | Guides verification, release preparation/review, and publication. |
| `hooks/hooks.json` → `hooks/handler` | **New** | Registers existing host events and translates them into shared script calls and host responses. |
| `bin/launcher` | **New** | Resolves and verifies the external runtime; prepares it only through an authorized setup operation. |
| `scripts/bridge` | **New** | Accepts named structured requests, checks their inputs and authority, and invokes existing evaluator operations. |
| `harnessctl` / `se_harness` | **Existing** | Computes lifecycle legality and next actions; performs supported installation, authoring, evidence, and transition operations. |
| `investigator`, `evidence-reviewer` | **New** | Optional read-only subagent roles for bounded investigation or evidence review. |
| `decision-review` | **New** | Presents an exact action to its accountable human and records an authenticated decision bound to the reviewed inputs. |
| `integration-gate`, `publication-gate` | **New** | Protect the remote merge and publication effects, including credentials and alternate access routes. |

A **skill instructs the agent**. A **host tool runs code**. A **hook reacts to an event**. Both a skill-guided agent and a hook handler can call the same bridge; neither contains a second copy of the evaluator's lifecycle rules.

<details>
<summary>Exact proposed calls, host tools, and decision binding</summary>

**One bridge entry point**

The proposed call is `bin/launcher bridge --request REQUEST_FILE --json`. Resolve the launcher's absolute path from the installed plugin; do not use a repository copy or rely on `PATH`. The native launcher uses the trusted runtime to execute the plugin's `scripts/bridge`. `REQUEST_FILE` contains JSON values, never a shell command string. For example, this new read-only request routes to the existing evaluator's `doctor` command:

```json
{
  "operation": "evaluator",
  "repo": "/absolute/path/to/project",
  "argv": ["doctor", "/absolute/path/to/project", "--json"]
}
```

On Windows, both repository values are absolute Windows paths. The bridge checks that they resolve to the same target. It allows only supported argument arrays; choosing `operation: evaluator` does not bypass mutation checks or turn a writing command into a read-only one. Existing `harnessctl` examples in the scenarios show the arguments passed to this external evaluator.

| New bridge operation | Input and result |
| --- | --- |
| `session-ready` | Repository, event/source, optional explicit artifact → verified governance and current selected state, or a readiness failure. |
| `orient` | Repository and inspection inputs → existing `harness-orient` helper result, after runtime and installation checks. |
| `evaluator` | Repository and allowed `argv` array → existing evaluator result, preserving its checks and write behavior. |
| `repository-preview` / `repository-apply` | Install/adopt/upgrade inputs → reviewed `plan_id`; apply rechecks that plan and current authorization, then reports installer and registration phases separately. |
| `review-preview` / `review-apply` | Exact proposed operation and artifacts → reviewed `plan_id`; apply requires bound authority and fresh evaluator checks. |
| `amendment-preview` / `amendment-apply` | Selected approved content and proposed edits → proposed amendment plan and controlled apply. Their additional semantics still need governed design; existing authorized authoring remains available. |
| `integration-preview` / `integration-submit` / `integration-status` | Exact PR/head/target → plan, protected submission, then observed operation result. |
| `publication-preview` / `publication-submit` / `publication-status` | Released record and configured destinations → plan, protected submission, then per-destination results. |

Runtime bootstrap uses `runtime-preview`, `runtime-prepare`, and `runtime-status` directly on `bin/launcher`, as described in scenario 1. All bridge operation names above are proposed; they are not existing evaluator commands.

**Host tools and subagents**

Codex uses `exec_command` to run the launcher and `apply_patch` for authorized file edits. Claude Code uses `Bash` or native `PowerShell` for the launcher and `Read`, `Edit`, or `Write` for files. Explicitly name the installed skill in a Codex request; Claude Code's proposed entry points use `/verity-plane:setup`, `/verity-plane:change`, and `/verity-plane:evidence` followed by the scenario's mode and selection.

For the two proposed subagent roles, Claude Code discovers plugin files `agents/investigator.md` and `agents/evidence-reviewer.md`. The main agent uses the existing `Agent` tool, selecting `subagent_type: "verity-plane:investigator"` or `"verity-plane:evidence-reviewer"` and supplying the bounded task prompt. Those role definitions and their invocation are **New** plugin configuration. Restrict their tools explicitly; plugin-agent `permissionMode` is ignored. [Claude Code subagents](https://code.claude.com/docs/en/sub-agents).

Codex needs separately installed `.codex/agents/investigator.toml` and `.codex/agents/evidence-reviewer.toml` registrations, with matching `name` fields and read-only configuration. The skill gives this concrete instruction: “Delegate this selected task to investigator. Read only the supplied scope and return findings with file references.” For evidence review it names `evidence-reviewer` instead. Codex's documented interface supports named delegation through instructions; the exact native tool/schema that selects the registered role must be demonstrated on each target client. No portable spawn-command syntax is assumed. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Every delegation supplies the selected IDs, input paths, question, applicable governance context, read-only limits, and expected result. The main agent collects the result before the dependent handoff. If the role or its restrictions cannot be confirmed, omit the optional helper and report that fact. See the [host comparison](../plugin-installation-proposal-2026-09-06.md#native-capabilities-and-their-limits).

**Plans and decisions**

The proposed bridge stores reviewed plans in plugin data. A plan names the repository, evaluator, selected inputs and their digests, intended action, and effects. It rejects stale or edited inputs before writing. A plan ID identifies a review; it is not approval.

`decision-review` is the proposed human interface to a protected decision service. Its record binds the authenticated actor to the exact action, selected content, and candidate or destination when applicable. `decision_ref` points to that record; an agent cannot create authority by writing a reference or supplying `--decision ID=ACTOR`. The service implementation remains open. Formal artifacts retain their existing meaning; this service authenticates the decision, not a replacement lifecycle.

`review-apply` uses an applicable human decision, or an existing delegation that the evaluator independently resolves as eligible. DR-015 delegation is limited to its specified start, completion, and verification-preparation operations, with trusted PR-base scope and live checks for the exact head. A request field claiming “delegated” is insufficient. Reuse valid existing authorization; request a new decision only when the action or changed inputs require one.

Remote gates must check this authority where the effect occurs. Local requests, successful hooks, and plugin files alone cannot enforce the merge or publication boundary.

</details>
