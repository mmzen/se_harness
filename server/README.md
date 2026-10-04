# Hosted artifact graph service

WO-HAG-001 authorizes this component. Phase 1 defines wire shapes, storage
constraints and independent reference fixtures. No service executable, image,
database deployment or remote CLI is implemented yet.

- [Wire shapes](contracts/remote-v1.json): JSON Schema 2020-12 definitions for
  revisions, baselines, source manifests and the five sandbox mutations.
- [Read shapes](contracts/read-v1.json): six domain reads and Cypher, explicit
  views, typed response data and completeness/continuation fields.
- [Result shapes](contracts/result-v1.json): accepted receipts, refusals and
  stable remote error codes. Semantic checks remain the service's responsibility.
- [Storage schema](contracts/graph-v1.cypher): proposed explicit initialization
  statements for the pinned Memgraph image; runtime qualification is pending.
- [Protocol and operating guide](../docs/notes/hosted-artifact-graph.md): identity,
  selector, atomicity and compatibility rules for implementation.
- [Contract fixtures](../tests/hosted_artifact_graph/fixtures/): fixed byte vectors
  and the full manifest of the pinned Git artifact set, plus explicit outcomes
  for every VER-HAG-001 scenario. Hosted execution remains unperformed.

Run the [explicit schema check](../tests/hosted_artifact_graph/validate_wire_contracts.py)
with a disposable `jsonschema==4.26.0` environment; the protocol guide gives the
commands and distinguishes shape checks from Phase 2 qualification.

The released-evaluator feasibility probe found an admission gap recorded in
[DEC-HAG-001](../docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-001.md).
The command adapter depends on its resolution. The checkout continues to use
the released 0.22.0 evaluator. Candidate code does not govern this checkout.
