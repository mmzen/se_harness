+++
id = "ARCH-HAG-003"
type = "architecture"
title = "Released lifecycle adapter with disposable Git projections"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "concurrency-consistency-reliability-or-failure-strategy", "material-alternatives"]
rationale = "Closed lifecycle operations produce multiple artifacts and evidence files, and ordinary Git provenance must survive atomic storage and export. ADR-HAG-003 records the proposed bounded design."
assessed_by = "Codex"

[relations]
addresses = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]
conforms_to = ["SPEC-HAG-007"]
+++

# Released lifecycle adapter with disposable Git projections

## Context and scope

Extend the existing Phase 2 service for the test-copy contract in SPEC-HAG-007.
Git continues to govern real work. This draft introduces no real authority
cutover, identity provider, database ACL or public service.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Installed remote client | Explicit endpoint and test selection; typed commands; receipt recovery; export into a new destination |
| Existing HTTP service | Validate the closed protocol and sandbox principal; reject unsupported or real-authority operations |
| Lifecycle adapter | Materialize a guarded disposable projection, invoke the released command, enumerate and validate all generated outputs |
| Released evaluator 0.22.1 | Sole lifecycle/gate authority and producer of formal record bytes |
| Existing Memgraph store | Immutable artifact and evidence revisions, baseline/context references and atomic complete-result receipts |
| Test Git projection | Ordinary clean Git history used for capture and release provenance; retained objects remain bound to their hosted input baseline |
| Export/replay tool | Export exact selected bytes and required Git objects; inspect independently with the released evaluator |

## Dependency direction and flow

Client → typed service boundary → lifecycle adapter → released evaluator.
The adapter submits its complete result to the store. The store does not decide
lifecycle legality. Reads and the seven MCP read tools continue through existing
bounded read paths; no new writable MCP tool is required.

For one mutation: bind immutable inputs, materialize, run, inspect file effects,
then compare versions and commit the whole result. Any stale input or invalid
output rejects the transaction. The graph receipt is the accepted outcome;
unreferenced projection files are recoverable staging only. Preserve the Git
objects associated with a committed result through restart and export.

## Trust boundaries

Treat remote requests, source content, artifact metadata and generated paths as
untrusted. Retain existing input sizes, containment checks, evaluator isolation,
private network boundary, service key and constrained Cypher. Do not pass shell
text or arbitrary executables from clients. Test actor labels supply fixture
inputs; they establish no real human authentication or authorization.

Imported real records are immutable. New rehearsal records are segregated and
labeled in project metadata, responses and export manifests. The service cannot
write the real repository or perform an external release action.

## Simplicity and cost

Keep one process, one store and synchronous requests. Reuse the existing adapter,
immutable revisions and transaction receipt mechanism. The necessary added cost
is complete multi-file write handling plus retention/export of ordinary test Git
history. A single-record patch loses generated evidence; a new hosted provenance
format would require a wider evaluator release and adoption. ADR-HAG-003 compares
these choices. No generic workflow engine, replication or background queue.

## Conformance

VER-HAG-006 checks real transactions, evaluator parity, provenance, export and
restart behavior. Existing Phase 2 wire and read tests remain regression inputs.
Approval of this architecture is pending with the rest of the package.
