# Lifecycle state contract

The workflow contract is the source of truth for lifecycle state meaning. In
workflow schema v3, `lifecycles` contains one row for every state admitted by
each artifact family. Both transition planning and validation read those rows;
they no longer maintain separate lists of legal states.

Each row answers six questions:

- `transitions_to`: which state may follow this one;
- `grants_authority`: whether the artifact may serve as current governance
  authority or coverage;
- `reserves_version`: whether a release record blocks another active proposal
  for the same version;
- `transitionable`: whether the state has an outgoing transition;
- `must_remain_visible`: whether the artifact remains part of governance
  history;
- `predecessor_adapter`: whether an older evaluator needs an explicit bounded
  compatibility adapter to assess that state.

For example, a ready release record reserves its version but grants no release
authority. A released record reserves the version and grants authority. A
rejected record does neither: it is terminal history, so a new record may reuse
the version after the rejected attempt while the failed decision remains
visible.

Some definition and work-order state names are retained as terminal
compatibility vocabulary even though the current planner cannot create them.
Recording these rows explicitly is important: an old `superseded` requirement
or a validation fixture using `ready` remains readable because the registry says
so, not because a global fallback list happens to accept it.

There are two byte-identical delivery copies of the contract for two isolated
runtime roles. Package commands read `se_harness/workflow_contract.json`. The
standalone validator installed in a repository reads
`docs/engineering/WORKFLOW.json`. The validator does not import candidate
package code into a locked predecessor process; tests prove that both roles
interpret the same contract bytes and lifecycle matrix.

An invalid or partially upgraded v3 contract is a hard failure. Consumers do
not fall back to old constants, guess missing properties, or accept a v2
transition table as v3 lifecycle semantics. Upgrading a repository's root
evaluator and managed contract remains a separate governed operation.
