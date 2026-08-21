# Workflow

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in BCP 14
(RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

This document defines the procedure bound to the executable workflow contract.
[`WORKFLOW.json`](WORKFLOW.json) defines the permitted transitions, ordered
next-action rules, required handoff fields, gate IDs, and decision-right IDs.
The installed `WORKFLOW.json` MUST be byte-identical to the contract loaded by
`harnessctl`.

## Workflow authority

`WFL-001` - A lifecycle transition MUST appear in `WORKFLOW.json`, pass every
gate named by the selected workflow rule, and be exercised by the role named by
its decision-right ID. Prose, adjacency, a passed command, or the status of a
related artifact MUST NOT authorize a transition.

`WFL-002` - A transition changes only the artifacts explicitly selected by the
actor. A VREC decision MUST NOT change a referenced work order. An RLS decision
MUST NOT change an included VREC or work order. A work-order decision MUST NOT
change its definitions, VRECs, or RLS records.

`WFL-003` - `harnessctl focus` and `harnessctl transition` MUST select the first
matching recommendation in the ordered `recommendations` array. They MUST NOT
invent, merge, or skip recommendations.

`WFL-004` - A command that prepares, validates, inspects, captures, or renders
information MUST NOT exercise a decision right. Only an explicit actor decision
and an applied permitted transition change lifecycle state.

`WFL-005` - `rejected` is terminal. `superseded` is terminal and applies only
to a ready VREC with one eligible successor. Historical lifecycle events MUST
remain append-only.

## State model

The permitted transitions are:

| Artifact class | From | To |
| --- | --- | --- |
| Definition | `draft` | `approved`, `rejected` |
| Definition | `approved` | `implemented`, `rejected` |
| Work order | `draft` | `approved`, `rejected` |
| Work order | `approved` | `in_progress`, `rejected` |
| Work order | `in_progress` | `implemented`, `rejected` |
| Work order | `implemented` | `verified`, `released` |
| Work order | `verified` | `released` |
| Verification record | `ready` | `verified`, `rejected`, `superseded` |
| Release record | `ready` | `released`, `rejected` |

The JSON contract is authoritative if this summary and the contract differ.
Conformance tests MUST fail on such a difference.

## End-to-end procedure

1. The author MUST use
   `harnessctl scaffold-domain . --domain <lowercase-kebab-domain>` once for a
   new domain, then
   `harnessctl create-artifact . --domain <domain> --type <type> --id <ID>` for
   each new draft. The author MUST complete accountable fields and validate the
   graph before requesting a decision.
2. The product or domain owner MUST approve the intent, capabilities, and
   requirements after `QG-G0-INTENT` and `QG-G1-DEFINITION` pass.
3. The technical owner MUST approve specifications and architecture after
   `QG-G1-DEFINITION` and `QG-G2-ARCHITECTURE` pass. Each architecture MUST
   declare its decision applicability. ADR count follows coherent significant
   decisions; no one-ADR-per-requirement rule exists.
4. The assurance owner MUST approve the verification contracts. The engineering
   owner MAY then approve one bounded work order after
   `QG-G3-WORK-AUTHORIZATION` passes.
5. Before implementation, the implementation actor MUST run
   `harnessctl focus . --artifact WO-...` and
   `harnessctl preflight . --work-order WO-... --phase start`, read every file
   in the manifest, and receive an explicit start decision.
6. The implementation actor MUST change only the authorized scope, retain
   work-order-keyed evidence, and run
   `harnessctl preflight . --work-order WO-... --phase review` plus the
   repository checks named by `REPOSITORY_CONTEXT.md`.
7. The engineering owner MAY mark only that work order `implemented` after
   `QG-G4-IMPLEMENTATION-EVIDENCE` passes.
8. When commit-bound verification is `required`, the authorized actor MUST
   commit the clean candidate before preparing a VREC. `capture-verification`
   MUST bind that exact candidate, work-order set, verification-contract set,
   and retained evidence. The resulting VREC remains `ready`.
9. The assurance owner MUST decide the VREC independently. A verified VREC does
   not change its work orders. Repository integration and release preparation
   are separate paths with separate authority.
10. Release preparation MUST use eligible verified coverage at one exact
   candidate commit. The release owner MUST decide the ready RLS independently.
   A released RLS does not tag, publish, deploy, or operate anything.
11. Each external action MUST receive its own explicit authority after
    `QG-G5-EXTERNAL-ACTION` passes.

## Bound procedures

Each row is bound to the same ID in `WORKFLOW.json`. "Result" states the only
permitted lifecycle effect; the contract's `non_effects` remain mandatory.

| Workflow ID | When | Gate / decision right | Required procedure and result |
| --- | --- | --- | --- |
| `WFL-WO-READY-VREC` | Focused WO is `implemented`; a related VREC is `ready`. | `QG-G4-ASSURANCE-DECISION` / `DR-VREC-DECIDE` | Focus the ready VREC. The assurance owner decides only that VREC; the WO remains `implemented`. Do not capture a duplicate VREC. |
| `WFL-WO-VERIFIED-VREC` | Focused WO is `implemented`; a related VREC is `verified` or `released`. | `QG-G4-VERIFIED-COVERAGE` / `DR-DELIVERY-SELECT` | Focus the VREC, then select repository integration or release preparation. Selection changes neither record. |
| `WFL-WO-PREPARE-VREC` | Focused WO is `implemented`; no ready, verified, or released VREC covers it. | `QG-G4-CANDIDATE-READY` / `DR-VREC-PREPARE` | Run `capture-verification` with exact inputs. Create one ready VREC; do not change or verify the WO. |
| `WFL-WO-START` | Focused WO is `approved`. | `QG-G3-WORK-AUTHORIZATION` / `DR-WO-START` | Run start preflight. Begin only after the engineering owner explicitly instructs implementation; then transition only the WO to `in_progress`. |
| `WFL-WO-IMPLEMENT` | Focused WO is `in_progress`. | `QG-G4-IMPLEMENTATION-EVIDENCE` / `DR-WO-COMPLETE` | Implement the bounded scope, retain evidence, and run review preflight. Completion changes only the WO to `implemented`. |
| `WFL-WO-COMPLETED` | Focused WO is `verified` or `released`. | No gate / `DR-RELATED-RECORD-SELECT` | Inspect its independent VREC and RLS records. Inspection changes nothing. |
| `WFL-VREC-DECIDE` | Focused VREC is `ready`. | `QG-G4-ASSURANCE-DECISION` / `DR-VREC-DECIDE` | The assurance owner verifies, rejects with a reason, or supersedes with one eligible successor. Change only the VREC. |
| `WFL-VREC-DELIVER` | Focused VREC is `verified` or `released`. | `QG-G4-VERIFIED-COVERAGE` / `DR-DELIVERY-SELECT` | Select repository action or authorized release preparation. Selection changes nothing. |
| `WFL-RLS-DECIDE` | Focused RLS is `ready`. | `QG-G5-RELEASE-DECISION` / `DR-RLS-DECIDE` | The release owner releases or rejects with a reason. Change only the RLS. |
| `WFL-RLS-EXTERNAL` | Focused RLS is `released`. | `QG-G5-EXTERNAL-ACTION` / `DR-EXTERNAL-ACTION` | State the exact tag, publication, deployment, or operating action and obtain separate authority. Release status performs no external action. |
| `WFL-REJECTED` | Focused artifact is `rejected`. | No gate / `DR-REMEDIATION-SCOPE` | Preserve the rejected artifact. Create or revise a bounded artifact chain and obtain normal approvals. |
| `WFL-VREC-SUPERSEDED` | Focused VREC is `superseded`. | No gate / `DR-RELATED-RECORD-SELECT` | Focus its declared successor. Preserve the old VREC as release-ineligible history. |
| `WFL-DEFINITION-COMPLETE` | Focused definition is `approved`. | `QG-G1-DEFINITION`, `QG-G2-ARCHITECTURE` / `DR-DEFINITION-DECIDE` | Complete remaining definitions or create and approve one bounded work order. Do not approve related definitions implicitly. |
| `WFL-DEFINITION-WORK` | Focused definition is `implemented`. | `QG-G3-WORK-AUTHORIZATION` / `DR-WO-SELECT` | Select the exact related work order. An implemented definition authorizes no new work. |
| `WFL-DEFAULT-REVIEW` | No earlier rule matches. | No gate / `DR-RELATED-RECORD-SELECT` | Report the current state and select one independently authorized transition. Change nothing. |
| `WFL-FAIL-REMEDIATE` | A workflow command fails. | No gate / `DR-REMEDIATION-SCOPE` | Report the exact blocker and unchanged state. Resolve it and rerun the same command; obtain new authority if remediation changes governed scope. |

## Transition procedure

For an accountable lifecycle decision:

1. Run `harnessctl focus . --artifact <ID>` and read the current state,
   recommendation, required authority, command or response, and alternatives.
2. Identify the matching ordered workflow rule in `WORKFLOW.json`. Verify its
   named gates pass and the actor holds its named decision right.
3. Obtain a statement naming the artifact, target state, and actor. Rejection
   MUST include a reason. VREC supersession MUST name the successor in `--reason`.
4. Preview the exact transition without `--apply`:
   `harnessctl transition . --set <ID>=<state> --decision <ID>=<actor>`.
5. Compare the preview to the explicit decision. Apply the same command with
   `--apply` only when they match.
6. Run `harnessctl focus . --artifact <ID>` again and report the resulting
   handoff. Do not transition a related artifact unless the actor separately
   selected and authorized it.

Use one transition packet when several definitions are mutually dependent and
each transition is explicitly named. A packet MUST NOT infer an omitted target.

## Lifecycle handoff procedure

After a completed stage or a stop condition, the agent MUST emit these fields in
this order:

1. `Completed`
2. `Current lifecycle state`
3. `Recommended next step`
4. `Human decision or approval required`
5. `Command or suggested response`
6. `Alternative next steps` only when the selected JSON rule contains one or
   more alternatives

The values MUST be rendered from the selected JSON rule using actual artifact
IDs. The agent MUST recommend exactly one next step, MUST NOT replace it with an
open-ended question, and MUST NOT report a lifecycle effect that did not occur.
When several stages complete in one response, report only the final state and
its next rule.

## Failure procedure

On a failed command, failed gate, invalid graph, missing authority, or scope
conflict, the agent MUST stop before the transition, report the exact failing
criterion and unchanged state, and recommend one safe retry or one accountable
escalation. Remediation that changes scope, accepts risk, or exercises a
reserved decision right requires a new explicit decision.

A record cannot contain the hash of its own commit. A VREC or RLS therefore
resides in a governance commit after the exact candidate commit it governs.
