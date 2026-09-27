# Report results and blockers

## Read this when

Report a governed result, handle a refusal or recover an uncertain operation.

## Before this action

Read only the actual selected result and evidence needed to establish its effects. Before eligible English reporting, read [COMMUNICATION.md#communication](COMMUNICATION.md#communication) if it is no longer in context.

## Procedure

### Report a lifecycle result

After a lifecycle stage completes or reaches a stop condition, obtain the
selected evaluator's schema-2 result. The result controls the reported scope,
effects, blockers, final state, required decision, alternatives, and next step.
The human or agent MUST NOT recompute those fields.

For a human-readable report, lead with the outcome or required decision. The
wording and headings may vary, and empty fields may be omitted. The report
MUST preserve:

1. The actual artifact IDs and whether the selected operation completed or
   was blocked.
2. The observed effects, separately from expected effects that did not occur.
3. Every exact blocker and every material non-effect. In particular, do not
   imply approval, a transition, verification, release, a Git action,
   publication, deployment, or operation that did not occur.
4. The final lifecycle state and the accountable human or agent. When a
   decision is required, name the exact decision and authority needed.
5. Exactly one current typed procedure step from the evaluator.
6. The command's argument values and boundaries, or the operative meaning of
   the suggested response.

Only complete alternatives declared by the workflow may be shown. Present them
separately from the primary next step. Do not invent an effect, authority,
blocker, decision, or alternative. Do not add unrelated repository findings
to the selected result. Do not replace the returned next step with an
open-ended question about what to do next.

Automation MUST read the structured JSON result. New results declare
`digest_format = "machine-fields-v1"`. This digest binds machine fields such
as candidate identity, scope, state, gates, and command arguments. Explanatory
wording is excluded. Older retained results keep their original digest format.

### If a procedure is blocked

Stop the affected action before changing lifecycle state or extending scope
when any of these conditions applies:

- Managed-file integrity fails.
- The selected governing graph is invalid or artifact IDs are ambiguous.
- The procedure needs a work order, but no selected work order is eligible
  for that phase.
- A required governing artifact or gate is missing.
- A required check fails or cannot be assessed.
- Repository-owner instructions conflict with the harness contract.
- Remediation would exceed the selected work-order scope.
- The action lacks its decision right or explicit authority.

Use the severity and blocking effect reported by `harnessctl`. Do not
reclassify a finding because it is labelled `structure`, `governance`, `policy`,
or `maintenance`.

Report the exact failed rule or predicate, the unchanged affected lifecycle
state, and any effects that already occurred. Preserve the observed evidence.
Use the evaluator's current result to report one corrective step or one
accountable escalation.

For a failed gate, use the corrective form that `harnessctl check` returns for
the first failing predicate. Do not substitute an unchanged replay of the
failed command. Resolve the missing input, scope, evidence, or decision before
retrying the affected action. Remediation that changes scope, accepts risk,
or exercises a reserved decision right requires the corresponding explicit
decision.

When a correction requires implementation, inspect the proposed work order
with `harnessctl check REPO --artifact WO-ID --json`. Reuse it only if its
approved scope covers the correction and its current state permits execution.
Start approved work through the start procedure; resume work already in
progress. If no eligible work order covers the correction, return to Define
the change and Authorize the work to prepare and approve a new work order.
Preserve completed and rejected records. The selected release provides no
transition from `implemented` back to `in_progress`; do not edit a state or
replay an earlier start to reopen it. A correction that changes an accepted
definition must also follow the linked-revision boundary.

After an interrupted write or uncertain external action, inspect the actual
result before retrying. Continue only work that has not already occurred.

## Read next when

After correcting the exact blocker or confirming uncertain effects → [CONTINUE.md#procedure](CONTINUE.md#procedure). Missing evaluator → [SETUP.md#procedure](SETUP.md#procedure).
## Gates

A gate is a named check used to determine whether an action meets its required conditions. It contains one or more predicates. A predicate is one exact condition, such as “the work order is approved” or “all declared changed paths are within the permitted scope.”

`harnessctl` evaluates the applicable predicates when a checkpoint is requested, a transition is previewed or applied, or a preparation command runs its required checks. A gate result is not an accountable decision.
