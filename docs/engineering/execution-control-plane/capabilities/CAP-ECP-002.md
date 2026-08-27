+++
id = "CAP-ECP-002"
type = "capability"
title = "Accountable decisions are authenticated, structured records"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
derives_from = ["INT-ECP-001"]
+++

# Capability: Accountable decisions are authenticated, structured records

## Actor and need

An accountable human holding a decision right under `DECISION_RIGHTS.md`,
and the evaluator that applies the transition they decided. Today the
decision reaches the harness as `--decision ID=ACTOR`, a free-text role
string validated for length and control characters only; no Git-author,
`GITHUB_ACTOR`, `CODEOWNERS`, or signature check exists anywhere in
`se_harness/` or `scripts/` (`se_harness/workflow.py:606`; 2026-08 agentic
execution review, section 5, weakness 1). Any agent can pass
`--decision VREC-X=assurance-owner`. The mutation guard proves which
evaluator wrote, never who decided.

The same human needs the transition they apply to be judged by the gates
the repository declares. `QUALITY_GATES.md` `QG-010` promises that
transitions recheck contract predicates, while `plan_transition` never loads
the gate table (`se_harness/workflow.py:685-750`) and `check_workflow`
refuses the `transition` checkpoint (`se_harness/workflow_compliance.py:395`),
so `check` and `transition` can disagree on the same work order and the
CLI labels every transition failure `WEX201` (`se_harness/cli.py:521`;
complexity audit P0-6). A delegated agent, where a human chose to delegate,
needs the same edge unlocked by the same gate rather than by a
proposed-workspace envelope that guards a token which never leaves its own
process (review section 5, weakness 3).

## Capability statement

`An accountable human can decide a lifecycle transition through a decision
record whose signer identity the evaluator verifies against the configured
identity source and whose role the evaluator checks against the decision
right, and a delegated agent can apply the start, completion, and
record-preparation edges of a work order that declares a delegation class
only while the required pull-request gate for the candidate is passing; in
both cases the edge is judged by the contract's transition gates through the
one evaluator and rendered in one result schema.`

## Boundaries

The capability authenticates and structures decisions and unifies how a
transition is judged. It does not create, move, or remove a decision right;
it does not let a machine decide anything a human decides today (`HRN-005`);
it does not authenticate the agent as a person. The identity source is
configured per repository; where none is configured, transitions that need
a decision fail closed. Delegation is declared by a human on a work order and
is bounded by the gate; it grants no edge that requires a decision right
other than the three named. `capture-verification` and `prepare-release`
change only their result schema.

## Outcomes

- A `--decision` value that the evaluator cannot bind to a verified signer
  holding the right is refused; "accountable humans retain authority" holds
  in the system, not only in documentation.
- `check` and `transition` reach the same verdict on the same repository,
  because one gate evaluator, one rule selector, and one result schema serve
  `focus`, `check`, `transition`, `capture-verification`, and
  `prepare-release`.
- A transition failure names the failing predicate and its corrective, not
  a blanket `WEX201`.
- A delegated agent's authority is a work-order attribute plus a green gate,
  observable in the artifact graph and in CI; no nonce ledger, lifetime, or
  revocation store stands between them.

## Candidate requirements

`REQ-ECP-008`, `REQ-ECP-009`, `REQ-ECP-010`, `REQ-ECP-011`.
