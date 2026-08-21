+++
id = "REQ-WEX-010"
type = "requirement"
title = "Bind every workflow directive to an executable procedure"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN an active workflow rule directs an action, THE SYSTEM SHALL bind that directive to an exact parameterized command, a fixed procedure identifier containing ordered typed steps, or an exact human decision request; expose the same binding to machine and human consumers; and reject unbound or ambiguous natural-language imperatives."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Bind every workflow directive to an executable procedure

## Rationale

A directive such as "run start preflight", "inspect the records", or "resolve
the blocker" states an intention but does not define one repeatable operation.
Agents can select different commands, omit required steps, or treat a human
decision as executable work. Stable procedure bindings are required for the
same workflow rule to produce the same action across providers.

## Preconditions and trigger

The active machine-readable workflow contains a rule that recommends or
requires an action. All values needed to select the rule are known; values
needed to execute a step may either be bound or explicitly reported as missing.

## Required response

- Assign every reusable or multi-step procedure one unique stable procedure
  identifier.
- Bind each workflow rule to one exact command template, one fixed procedure
  identifier, or one exact human decision request.
- Define a referenced procedure as an ordered list of typed steps. Each step is
  one of:
  - `command`: an exact command template with named parameters and required
    inputs;
  - `decision`: the decision-right ID, accountable role, selected artifact,
    permitted outcomes, and exact response fields;
  - `reference`: exactly one resolvable procedure ID.
- Resolve every placeholder from selected workflow data or identify the exact
  missing input before execution.
- Expose the selected procedure ID, resolved step, required authority, expected
  effect, and mandatory non-effects in machine-readable output.
- Render the same binding in human documentation and restitution without
  replacing it with a paraphrased imperative.
- Preserve stable ordering and produce the same resolved procedure for the same
  active contract, repository state, selection, and inputs.

## Failure and boundary behavior

- A missing, unknown, duplicate, recursive, type-incompatible, or ambiguous
  procedure reference invalidates the workflow contract.
- An unresolved required parameter blocks the affected step and identifies the
  parameter; the system MUST NOT guess a value or substitute another command.
- An imperative with no executable command, fixed reference, or exact decision
  request fails conformance and MUST NOT be presented as an actionable next
  step.
- A failed step reports its completed effects and mandatory non-effects, then
  follows the bounded failure procedure without skipping later.
- A decision step stops for the named accountable actor. It MUST NOT be treated
  as command execution merely because the procedure reached it.

## Constraints

- The machine-readable workflow is the normative owner of procedure bindings.
  Human documentation must be generated from it or conformance-tested against
  it.
- Unbound wording such as "run preflight", "inspect", "select", "resolve", or
  "use exact inputs" is forbidden when it denotes an actionable step.
- Repository-specific operations are stated as prose in the owner-controlled
  region of `AGENTS.md`. They are not bound as executable procedure steps, and
  no reference step resolves step content from a file the harness does not
  govern.
- Exact commands and procedure schemas are versioned public interfaces.
- A procedure MAY prepare data or apply an explicitly authorized mechanical
  transition. It MUST NOT grant authority, approve, verify, release, accept
  risk, or perform an external action without the separately required decision.
- Skills and agent adapters may invoke and render a procedure but must not add,
  remove, reorder, or reinterpret its steps.

## Acceptance examples

### Example: normal behavior

**Given** an approved work order selected by `WFL-WO-START`

**When** the workflow resolves its start procedure

**Then** it identifies one stable procedure ID whose ordered steps include the
exact `focus` command, the exact start-preflight command, the
`DR-WO-START` decision request, the transition preview and apply templates, and
the final `focus` command, with implementation blocked until the decision step
is satisfied.

### Example: failure behavior

**Given** a workflow rule whose procedure says only "run
capture-verification with exact inputs"

**When** workflow-contract conformance is checked

**Then** the rule is rejected because it has neither an exact parameterized
command nor a fixed procedure reference, and no agent-specific interpretation
is offered as a substitute.

## Open decisions

The specification must define the procedure-registry schema, step and parameter
types, reference-depth or recursion rules,
documentation rendering, and compatibility treatment for existing free-form
handoff commands before this requirement is approved for implementation.
