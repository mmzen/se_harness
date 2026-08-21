+++
id = "REQ-WEX-007"
type = "requirement"
title = "Confine selected workflow execution and restitution"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN an operator executes or reports work for one selected workflow scope, THE SYSTEM SHALL classify surfaced findings, governed artifact mutations, declared implementation-path changes, and restitution items against that scope; reject out-of-scope governed mutations; exclude unrelated findings and actions from primary restitution; and enter repository-wide analysis only through an explicit repository-wide mode."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Confine selected workflow execution and restitution

## Rationale

Selected-scope projection prevents unrelated work from becoming the current
task only when every execution and reporting boundary preserves that
projection. A repository-wide diagnostic command, an undeclared file change,
or provider-specific prose can otherwise reintroduce unrelated findings and
make the workflow unpredictable across agents.

## Preconditions and trigger

The operator selects one formal workflow artifact. Before a governed mutation,
the operation also identifies every formal artifact and implementation path it
intends to change. Repository maintenance instead requires an explicit
repository-wide selection.

## Required response

- Derive the selected artifacts, governing artifacts, direct lifecycle
  dependencies, and repository-integrity boundary deterministically.
- Classify surfaced findings as selected-scope blockers, repository-integrity
  blockers, or unrelated background observations.
- Classify every declared governed artifact mutation and implementation-path
  change against the selected scope before the operation applies it.
- Reject an out-of-scope governed mutation without applying any part of that
  mutation and identify the exact artifact or path that violated scope.
- Exclude unrelated findings, artifact IDs, remediation actions, and next steps
  from primary restitution.
- Include a repository-level finding as a blocker only when the finding makes
  safe evaluation of the selected scope impossible.
- Require an explicit repository-wide mode before returning actionable details
  for unrelated artifacts.

## Failure and boundary behavior

- An absent, ambiguous, stale, or malformed scope declaration fails closed.
- The system MUST NOT expand scope merely because an unrelated finding or
  changed path is discovered.
- Unrelated observations MAY be omitted or summarized by count; they MUST NOT
  become selected-scope blockers, decisions, or actions.
- A repository-wide result MUST identify itself as repository-wide and MUST NOT
  be represented as the result for a previously selected artifact.
- A failed scope check leaves governed lifecycle state unchanged and reports
  one bounded remediation or accountable scope-expansion decision.

## Constraints

- Reading repository context does not authorize changing or reporting
  unrelated work.
- A Skill, prompt, or agent-specific instruction MAY invoke the scope result but
  MUST NOT redefine or enlarge it.
- Path-scope enforcement applies to the declared operation or change set. This
  requirement does not restore rejected `REQ-WEX-006`, select a trusted Git
  base, validate lifecycle history from a diff, or claim to intercept arbitrary
  edits performed outside governed workflow commands.
- Scope classification and restitution filtering must produce the same result
  for every supported agent given the same repository state and inputs.

## Acceptance examples

### Example: normal behavior

**Given** a selected work order whose governing chain is valid, two declared
implementation paths within its authorized scope, and warnings on an unrelated
work order

**When** the selected iteration is checked and closed

**Then** the declared paths are accepted, the unrelated warnings produce no
selected blocker or next action, and the restitution contains only the selected
work, its dependencies, and any applicable repository-integrity blocker.

### Example: failure behavior

**Given** a selected work order and a governed operation that declares a change
to a path owned only by an unrelated work order

**When** the operation performs its pre-mutation scope check

**Then** the operation rejects the path before applying the governed mutation,
leaves lifecycle state unchanged, and recommends either removing the change or
obtaining an explicit scope-expansion decision.

## Open decisions

The specification must define path selectors, caller-supplied change-set
inputs, the exact repository-integrity blocker taxonomy, and the explicit
repository-wide interface before this requirement is approved for
implementation.
