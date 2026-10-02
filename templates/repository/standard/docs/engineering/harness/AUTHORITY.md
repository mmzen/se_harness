# Actors and decision rights

An actor is either a human or an agent. A human is a person. An agent is an
automated system that performs work under granted authority.

## Roles and accountabilities

| Profile | Accountable for                                                                                                                                                                      |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Human   | Making decisions on product intent, requirements, design, work scope, verification, release and external actions; authorizing work and changes to its scope.                         |
| Agent   | Preparing artifacts and decision proposals; starting, carrying out and checking authorized work; retaining evidence; preparing verification records; reporting results and blockers. |

Agents have no independent authority to approve scope, accept assurance,
release software, or perform external actions.

Both humans and agents MUST follow the applicable checks, evidence requirements,
and decision rules.

## Decision rights

A profile describes who performs an action. A decision right describes which
action that person or agent is authorized to perform. Being a Human does not
grant every right in this table. Being an Agent grants none by itself.

Use the artifact's recorded ownership and any existing explicit delegation to
identify the accountable human. Resolve a team name or ownership label to the
human making this decision. A proposed `owners` value, an example actor name,
or authorship of a draft MUST NOT assign decision authority.

Approval, verification acceptance, and release decisions MUST be made by an
authorized human. An agent MAY prepare the material and apply that human's
recorded decision when authorized to do so. Applying the decision does not
make the agent its author. The selected IDs, reviewed content, target states,
and reason MUST still match the decision at apply time.

The following stable IDs name rights and operations, not additional profiles.
All applicable gates remain required.

These DR-* identifiers come from the selected evaluator's decision-right
catalogue. Use the right and exact action returned by that evaluator. Legacy
owner labels identify recorded accountabilities; they do not create additional
Human/Agent profiles or assign a decision to a person by themselves.

| Right ID                   | Accountable profile and authority                                                                                                  | Required input                                                                                                    | Result                                                                                               |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| `DR-DEFINITION-DECIDE`     | Human authorized to decide the selected definition.                                                                                | Complete definition, exact proposed state, and required checks.                                                   | Decision on that definition only.                                                                    |
| `DR-WO-SELECT`             | Human authorized to approve the work scope.                                                                                        | Complete governing chain, bounded work order, and assurance classification.                                       | Approval or rejection of the selected work order.                                                    |
| `DR-WO-START`              | Human or Agent executing the selected work under its recorded approval.                                                            | Unchanged approved scope and passing start checks.                                                                | The selected work order becomes `in_progress`.                                                       |
| `DR-WO-COMPLETE`           | Human or Agent executing the selected work under its recorded approval.                                                            | Completed scope, passing handoff checks, and retained evidence.                                                   | The selected work order becomes `implemented`.                                                       |
| `DR-VREC-PREPARE`          | Human or Agent under the approval of every selected work order.                                                                    | Exact candidate, selected work and verification contracts, retained evidence, and passing preparation checks.     | One `ready` verification record; no acceptance decision.                                             |
| `DR-VREC-DECIDE`           | Human authorized to accept verification for the selected candidate.                                                                | Ready record, assessed evidence, and the exact verify, reject, or supersede decision.                             | Decision on that verification record only.                                                           |
| `DR-DELIVERY-SELECT`       | Human authorized for the chosen integration or release-preparation path.                                                           | Exact candidate, destination, and coverage required by that path.                                                 | One path-specific instruction.                                                                       |
| `DR-RLS-PREPARE`           | Human authorizes the release inputs; a Human or Agent may carry out the preparation.                                               | Exact release contract, candidate, included work, verification coverage, version, and passing preparation checks. | One `ready` release record; no release decision.                                                     |
| `DR-RLS-DECIDE`            | Human authorized to make the release decision.                                                                                     | Ready release record, assessed contract obligations, and the exact release or reject decision.                    | Decision on that release record only.                                                                |
| `DR-EXTERNAL-ACTION`       | Human authorized for the exact external action. A Human or Agent may execute the authorized operation.                             | Action, immutable target, destination, prerequisites, and recovery conditions.                                    | Authorization limited to that operation; the subsequent tool result records its actual effects.      |
| `DR-RELATED-RECORD-SELECT` | Human or Agent; no decision authority is needed for inspection.                                                                    | Exact existing artifact ID.                                                                                       | Read-only selection.                                                                                 |
| `DR-REMEDIATION-SCOPE`     | Human authorized to change the affected definition or work scope.                                                                  | Failed criterion and proposed bounded correction.                                                                 | Explicit authority for the revised scope.                                                            |
| `DR-DECISION-DISPOSE`      | Human accountable for the artifact blocked by the decision; for a deviation, the human accountable for the affected specification. | Open or deferred decision, selected option or disposition, exact reason, and any required revisit trigger.        | Recorded disposition and any declared paired-risk effect. Other blocked artifacts keep their states. |

For a lifecycle decision, the `--decision` value identifies its actual
decision-maker. When an agent applies a human decision, that value is the
human who made it. For start and completion under approved execution, it is
the actual Human or Agent executor. Supplying either identity does not grant
authority. Preparation `--owner` values identify the preparation actor, not
a future assurance or release decision-maker.

Silence, elapsed time, a commit, a pull request, tool execution, or a passing
check MUST NOT count as a human decision. A rejection MUST include a non-empty
reason. Supersession MUST name exactly one eligible successor. The decision
and its resulting state MUST remain specific to the selected artifact.

## Complete-release authority

When the selected release contract and reviewed delivery plan explicitly select
complete release delivery, one human response MAY supply the release decision
and authorization for every external action listed in that plan. The human MUST
hold each applicable right. Keep the release decision and observed external
effects as separate records; one response does not perform those actions.

Before requesting that response, prepare all deliverables and complete required
checks and human verification. Present the exact release record, candidate,
versions, payload identities, destinations, required integration, recovery rules
and known limitations. Retain the complete reviewed plan's SHA-256 with the
actual human decision. Use the existing release record and evidence locations.

An agent MUST reuse this authority while the exact plan and conditions still
match. A change of provider, a pause or a resumed session does not require another
approval. Check current gates and provider controls before each external action.
Inspect uncertain results before retrying. A changed plan, candidate, destination
or scope needs a new decision; a failed check must be resolved, not approved away.

The plan MAY cover future governance commits only through an explicit bounded
rule: approved base content plus the recorded decision or specified receipts,
allowed paths and a named protected destination. Compare the exact resulting
diff before integration. This does not authorize unrelated work or bypass checks.

A released state alone grants no external authority. Older decisions keep their
original scope; do not add a complete-release grant after the fact. A plan, actor
label or passing evaluator result cannot authenticate a human decision. If the
contract or plan does not select this route, use its existing separate authority.

## Delegation and separation

A human decision right may be delegated only to another human who is permitted
to hold it. The delegation MUST name the right, its scope, the granting human,
and the receiving human. It MUST be recorded before the delegated decision.
The receiving human MUST decide under their own identity.

An instruction for an agent to apply a recorded human decision delegates the
execution of that command. It does not delegate the decision itself. The
agent MUST NOT supply a new answer, broaden the targets, or claim the human
made a decision that was not given.

Repository policy MAY require different people for conflicting decisions on
the same candidate. When it does, the same human MUST NOT hold both decisions
for that candidate. A human MUST NOT approve their own architecture decision
assessment unless they explicitly hold approval authority for that artifact
and the separation rules permit it. Drafting an assessment grants no such
right.

When the accountable human or required authority is absent or ambiguous, stop
the affected decision. State the exact right and artifact needing an owner.
Do not substitute an available human or agent merely to fill the field.

## Authority from work approval

Work-order approval authorizes execution of its approved scope: start,
implementation, local edits and commits, required checks, evidence capture,
completion recording, and required verification-record preparation. A Human
and an Agent MUST use the same local approval, scope, and evidence checks.
Continue these operations without asking for the same permission again while
their scope and conditions still match. Record execution under the actual
executor's identity.

Approval leaves the work order `approved` until its start transition is
applied. Selecting and scheduling work remain explicit. New approvals need
no separate execution delegation table or second start approval. A preliminary
merge and live CI are not local execution requirements; CI still applies at
integration and publication.

The grant does not include changed scope, acceptance of the result, release,
merge, publication, or other external action. Reuse an existing explicit
authorization for such an action only when its exact target and conditions
still match.

Historical approvals keep their original meaning. Earlier explicit execution
grants remain usable under the same scope checks. An older approval without
such a grant needs an authorized amendment for the remaining execution.
Current metadata or an actor label MUST NOT manufacture that historical grant.
If the installed release cannot record the required authorization, stop the
remaining execution and report the missing historical grant and the lack of
a supported amendment operation. Do not insert invented grant fields or
rewrite the old approval.

## Review publication authority

For work delivered through a PR, request the review-publication grant explicitly
with work approval. Name the selected work, destination repository, source
branch and target branch. The grant covers pushing that bounded work and its
evidence, creating or updating its draft PR, pushing the later recorded
verification decision, and marking the PR ready after that decision is remote.
One human reply may approve implementation and these publication actions.
Ordinary work approval alone does not supply the publication grant.

The final commit is not known at work approval. Before each external operation,
resolve its full commit and check that the changed content, selected records,
branch and destination remain within the granted scope. Preserve required
gates and provider controls. Reuse the grant while those conditions match.
Obtain only missing authority; a changed destination or scope is not covered.
Record the actual grant in the existing decision envelope and transition reason,
not a new authority file. Historical approvals keep their original meaning.

Review publication leaves the VREC ready. It grants no verification, merge,
force-push, release, tag or deployment authority. The human decides verification
after the review package is accessible. Publishing that recorded decision uses
the existing grant; it does not turn verification into permission to merge.
Follow [Publish the review package](PULL_REQUEST.md#publish-the-review-package)
and [Publish the verification decision](PULL_REQUEST.md#publish-the-verification-decision).

<!-- Migration requirement: the released machine contract still contains
legacy owner labels. Preserve its decision-right IDs and actual human
identities. Update machine labels and their consumers in the governed release
migration; this two-profile table does not silently rewrite installed JSON. -->
