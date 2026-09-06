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
