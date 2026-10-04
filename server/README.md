# Hosted artifact graph service

WO-HAG-001 authorizes this component. Phase 1 defines wire shapes, storage
constraints and independent reference fixtures. No service executable, image,
database deployment or remote CLI is implemented yet.

- [Wire shapes](contracts/remote-v1.json): JSON Schema 2020-12 definitions for
  revisions, baselines, source manifests and the five sandbox mutations.
- [Storage schema](contracts/graph-v1.cypher): proposed explicit initialization
  statements for the pinned Memgraph image; runtime qualification is pending.
- [Protocol and operating guide](../docs/notes/hosted-artifact-graph.md): identity,
  selector, atomicity and compatibility rules for implementation.
- [Contract fixtures](../tests/hosted_artifact_graph/fixtures/): fixed byte vectors
  and the full manifest of the pinned Git artifact set.

The released-evaluator feasibility probe found an admission gap recorded in
[DEC-HAG-001](../docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-001.md).
The command adapter depends on its resolution. The checkout continues to use
the released 0.22.0 evaluator. Candidate code does not govern this checkout.
