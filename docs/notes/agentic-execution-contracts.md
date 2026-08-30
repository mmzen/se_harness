# Runtime-neutral Agentic Execution contracts

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

The Phase 2 contract layer gives SE Harness one provider-neutral way to check
the data exchanged by future skills, agents, and mutation controls. It is a
pure Python API: callers supply already-observed values, and the module returns
validated canonical data or a stable diagnostic. The module does not inspect
Git, read repository state, execute commands, call a model, or write anything.

## What was added

- `se_harness/agent_contract.json` is the canonical
  `se-harness-agent-contract-catalog-v1` catalog. It declares the eight public
  schemas, nested field sets, compatibility variants, collection ordering,
  resource bounds, and `AEXCON001` through `AEXCON018` diagnostic classes.
- `se_harness.agent_contract` strictly parses and validates the catalog and
  semantic documents using only the Python standard library.
- `tests/fixtures/agentic_execution/contracts/` contains independent canonical
  byte and digest vectors, including representative index, deleted, executable,
  symlink, gitlink, and untracked worktree states.

The existing `se-harness-skill-contract-v1` and `harness-orient` portable-core
digest are unchanged.

## Authority boundary

Three similar terms have intentionally different meanings:

| Result | Meaning | What it does not mean |
| --- | --- | --- |
| `constructed` | Supplied values form a valid envelope candidate within the supplied managed maximum | The envelope was derived from current repository authority |
| `admissible` | One supplied operation is inside the candidate's operation, path, profile, writer, retry, evidence, and stop bounds | The operation is admitted or authorized to run |
| valid receipt or packet | The evidence or projection is complete and internally consistent | An accountable decision was made |

Only a later, separately approved exact-evaluator integration may observe live
state and use the words `derived` or `admitted`. A runtime permission, agent
name, skill, model response, receipt, or valid JSON document cannot cross that
boundary.

## Main API

The most common functions are:

- `parse_contract_bytes(...)` and `validate_contract(...)` for the eight public
  schemas;
- `canonical_json_bytes(...)` and `canonical_sha256(...)` for
  `se-harness-canonical-json-v1` identity;
- `construct_repository_state_binding(...)` for a binding candidate made from
  complete supplied worktree and governance observations;
- `construct_envelope_candidate(...)` and `narrow_autonomy_envelope(...)` for
  intersection and monotonic child-scope checks;
- `assess_admission(...)` for a pure one-operation assessment;
- `project_decision_packet(...)` and `render_decision_packet(...)` for an exact
  workflow-result-v2 plus packet-context projection;
- `validate_execution_receipt(...)` with `ReceiptExpectations` for comparison
  against an independent execution plan; and
- `validate_logical_execution_profile(...)` for non-authoritative,
  provider-neutral profiles with a mandatory single-agent fallback.

Every failure raises `AgentContractError`. Its `code`, `path`, and bounded
`message` can be returned as structured diagnostics without exposing the input
value.

## Typical pure flow

```python
from se_harness.agent_contract import (
    assess_admission,
    construct_envelope_candidate,
    construct_repository_state_binding,
)

binding = construct_repository_state_binding(worktree_observation, governance_observation)
construction = construct_envelope_candidate(
    state_binding=binding.value,
    evaluator_payload_sha256=expected_evaluator_payload,
    procedure_id="PROC-WO-IMPLEMENT",
    request=requested_scope,
    managed_scope=maximum_managed_scope,
)
assessment = assess_admission(
    construction.envelope.value,
    envelope_sha256=construction.envelope.sha256,
    expected_current_repository_state=binding.sha256,
    operation="write-evidence",
    target_paths=["docs/evidence/result.json"],
    execution_profile="implementer",
    requested_writers=1,
    retry_ordinal=0,
    evidence_paths=["docs/evidence/result.json"],
    stop_boundary="accountable-decision-required",
)
```

Even when `assessment.outcome == "admissible"`, the caller must stop. Phase 2
has no effect callback and cannot make the live-state comparison needed before
a governed write.

## Fail-closed behavior

The parser rejects duplicate and unknown keys, unknown schema versions, floats,
non-finite numbers, invalid Unicode, oversized or deeply nested documents,
invalid identifiers, non-lowercase digests, and unsafe paths. Collections are
normalized only when the catalog declares set semantics; source-ordered
sequences retain their order and duplicate identities fail.

Envelope children may remove capability but cannot add it. They cannot change
the work order, repository binding, evaluator payload, or actor assertion;
increase writers or retries; add operations, paths, or profiles; remove a stop
boundary; or weaken evidence obligations.

Receipt validation uses a separately supplied `ReceiptExpectations` value. It
does not trust the receipt to define its own planned operations, workers,
changed paths, evidence, or state chain. Decision-packet projection likewise
requires one complete workflow result and one exact context; it cannot invent a
missing decision or hide a failed or not-assessable gate.

## Compatibility and packaging

- Decision-packet v1 remains validation-only compatible. Phase 2 projections
  produce v2 because v1 has no selected-scope or lifecycle-state location.
- The Phase 1 three-field operation and legacy `AEXORI` deviation variants
  remain valid only for the `single-agent-orientation` receipt profile without
  an envelope digest.
- The catalog is package data in source and wheel distributions. Its canonical
  SHA-256 is expected to match across the checkout and installed package.
- No new runtime dependency, CLI command, skill, subagent, adapter, or mutation
  integration was added.
