+++
id = "SPEC-HAG-002"
type = "specification"
title = "Hosted command acceptance, context reads and evaluator adapter"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
contract = "Accept bounded sandbox draft commands only after server admission and atomic version checks; expose explicit-view domain, MCP and constrained Cypher reads with recoverable results."

[relations]
specifies = ["REQ-HAG-003", "REQ-HAG-004", "REQ-HAG-005", "REQ-HAG-006", "REQ-HAG-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Hosted command acceptance, context reads and evaluator adapter

## Scope

One Python service supplies the HTTP command/read API and MCP reads over one Memgraph store. Phase 2 accepts sandbox draft commands only. It does not authenticate human approval decisions, issue remote verified/released records or adopt remote authority for this repository. Existing released evaluator behavior is reused through a bounded materialization adapter.

### HAG-API-001 — Explicit identities and proposed routes

Proposed CLI namespace: `harnessctl remote` with explicit `--endpoint`, `--project`, and one `--baseline` or `--context` selector. Credentials come from a named local secret source and are redacted. Ordinary local commands retain current semantics. No implicit fallback from a failed remote write to local files. A saved client configuration names authority mode `sandbox-projection` and cannot claim authoritative remote mode in this POC.

| Domain operation | Proposed HTTP route | Proposed CLI verb |
| --- | --- | --- |
| Import selected source manifest | POST /v1/projects/{project}/imports | remote import |
| Retrieve baseline | GET /v1/projects/{project}/baselines/{baseline} | remote baseline |
| Freeze an explicit draft selection | POST /v1/projects/{project}/baselines | remote freeze |
| Open draft context | POST /v1/projects/{project}/contexts | remote draft-open |
| Create/revise draft | POST /v1/projects/{project}/commands | remote create-artifact / remote revise-artifact |
| Read accepted operation | GET /v1/projects/{project}/operations/{key} | remote operation |
| Exact revision/context/compare/impact/lineage/check | POST /v1/projects/{project}/reads/{operation} | remote read / remote check |
| Cypher sandbox exploration | POST /v1/projects/{project}/reads/cypher | remote query |
| Component/schema readiness | GET /v1/status | remote status |

These are proposed interfaces governed by this draft, not commands already present in 0.22.0. `create-artifact` uses the existing released authoring template, ID validation and supported allocation through a disposable projection. `revise-artifact` submits the full document, avoiding an unnecessary generic patch language. Lifecycle transitions and VREC/RLS preparation return `unsupported_operation` in this sandbox contract.

### HAG-API-002 — Request and result envelopes

Mutation schema `se-harness-remote-command/v1` contains project, context/base baseline, expected project version, expected context version, optional expected revision, operation key, operation name, proposed document or template inputs, and expected evaluator/policy identity. Authentication supplies principal and allowed role from operator configuration, not a request's actor string. Only `sandbox-reader`, `sandbox-author` and import/operator rights exist here; none is a human decision right. Client and server report their actual build identities.

Result schema `se-harness-remote-result/v1` contains operation key/request digest, outcome, selected project/view, before/after versions, affected revision IDs, evaluator/policy identity, meaningful evaluator findings, and an accepted receipt identity when committed. Refusals distinguish malformed input (400), unauthenticated (401), forbidden (403), unknown identity (404), stale context/key mismatch/unsupported identity combination (409), invalid draft contract (422), and bounded resource refusal (429). Include structured stable codes; allocate new remote codes without reusing existing evaluator codes. Embed evaluator JSON and its identity unchanged; do not manufacture a lifecycle next step. Transport uncertainty remains unknown until operation lookup or an idempotent retry resolves it.

### HAG-API-003 — Server evaluation and draft validity

Authenticate and authorize before expensive processing. Check the supported client/API/evaluator tuple. Load a consistent project/context selection. Materialize its canonical documents with original paths in disposable storage outside any development checkout. Supply the selected released configuration/resources and the pinned historical resolver required by checks. Run the exact private evaluator with isolated Python and fixed argument arrays, bounded time/output, no shell, no candidate-import fallback and no artifact-body command execution.

Use the released parser, artifact catalog, relationship type rules, selection and validator findings. Authoring creation deliberately saves an incomplete template, as the existing CLI does; saving a draft does not require every approval predicate. Classify the narrow allowed incompleteness set explicitly from the released draft contract and test it. It may include a missing capability link in a newly generated requirement template. Do not suppress malformed TOML, duplicate keys/IDs, ID/type mismatch or a supplied prohibited relation type. Refuse all changes to identity/type/protected lifecycle/provenance fields on existing imported records; revising an approved baseline definition requires a new draft proposal, not an in-place change to the approved revision.

If the selected evaluator cannot express this classification without inventing policy, stop and return the concrete gap for a contract amendment. Do not add a blanket `ignore_errors` switch. Local prevalidation is advisory; the server runs the same required evaluation against its own selected state before acceptance.

### HAG-API-004 — Concurrency and atomic acceptance

One project-wide integer version protects every accepted command, including import, baseline/context creation and changes to inputs used for acceptance. The caller also supplies context version and expected target revision where applicable. Evaluate against a consistent snapshot at N. In a Memgraph explicit transaction under transactional snapshot isolation, read and conditionally update the same project guard from N to N+1, recheck the selected context/revision/identity, then write all revision content, declared edges, context head and operation receipt. Commit all or none. A changed dependency increments the project guard and invalidates a pending command even when its target is unchanged.

Evaluation may occur outside the short write transaction only when its entire input is bound to N and the commit transaction verifies N and the same immutable selection. A process lock is not sufficient concurrency control. A database conflict maps to a stale/conflict result; do not automatically rebase and accept a stale human-reviewed request. Test concurrent connections, not just sequential mocks.

Before version checks, look up `(project, principal, operation_key)`. An accepted equal request digest returns the stored original result, including the old expected version. A different semantic request under that key is refused. Authenticate the retry again and enforce project access. The request digest binds context, expected versions, operation, content and evaluator/policy selection; it excludes bearer secrets and transport timestamps. A rejected transaction leaves no partial acceptance receipt. A concurrent identical-key loser reads the winner's committed result after conflict. Operation lookup never invents success for an unknown key.

### HAG-API-005 — Reads and completeness

Read operations are exact revision, work context, compare, impact, verification lineage, check/blockers and constrained Cypher. MCP tools expose the same six domain reads plus Cypher, using the service's authenticated read handlers and explicit schemas. Use the maintained MCP SDK pinned in server dependencies; do not implement a second protocol or expose mutation through arbitrary MCP text.

Each result reports project, view kind, baseline or context/version, revision/evaluator identities, provenance, unresolved references and `complete`. A budget stop reports `complete=false`, the reason and a continuation strategy at the same view. Context selection must be complete to support a governing claim. Impact is limited to known declared traceability. No query may infer approval from a successful read. Return exact declared scope separately from relevant decisions and unrelated findings. Public storage labels/edge kinds/properties used by Cypher are versioned as `se-harness-graph-read/v1`; changes to them are distinguished from internal database migrations.

### HAG-API-006 — Cypher retained with a stated enforcement gap

The user explicitly directed on 2026-10-04: retain Cypher, defer read-only enforcement at Memgraph, and record an unresolved item. This modifies the brief's database-boundary requirement for the Phase 2 sandbox only. Do not claim database-enforced read-only access or authoritative pilot readiness.

Accept a deliberately narrow parsed Cypher read grammar: one bounded MATCH/OPTIONAL MATCH, optional WHERE, and RETURN with a bounded LIMIT, parameters and an explicit selected view. Refuse write clauses, multiple statements, CALL/procedures, subqueries, file/network loaders, schema/auth/admin commands and unsupported syntax. Use a parser/AST allowlist, not keyword substring filtering. Bound variable-length traversal depth; bind the selected baseline/context server-side rather than trusting a caller WHERE clause. Run exploratory queries in an explicit transaction that is rolled back, with no commit path. This is defense in depth, not a substitute for database privileges.

Use only non-sensitive disposable data. Keep the database port on the private Compose network; the sandbox API binds loopback. A single service process holds the write credential; it never returns that credential to a client. Read credential separation and Memgraph role enforcement remain a required open item owned by security-owner before any authoritative pilot, shared tenant or untrusted-network exposure. A parser bypass or unsupported semantic construct stops the Cypher route and the affected completion claim; do not weaken the grammar to make a demo pass.

### HAG-API-007 — POC budgets

Initial acceptance envelope: at most 2,500 imported artifacts, 10,000 retained revisions, 1 MiB per document, 64 MiB per source import (excluding separately retained evidence archives), two concurrent authors, 500 rows and 2 MiB per read response, and traversal depth eight. Bound Cypher execution to five seconds and evaluator execution to 120 seconds. Measure representative content/history before claiming this envelope. Report over-limit input honestly; no silent clipping of canonical content. Larger imports or limit changes require review against the contract and measured need.

## Examples and coverage

Two requests at N changing different artifacts conflict conservatively because they share a governing project. Retrying an accepted N request at N+1 still returns its stored result. A draft requirement linked by derives_from to a release record is invalid; a just-created template with missing authoring text remains saved but not approval-ready. An approved document body submitted to the draft edit route cannot replace the baseline revision.

REQ-HAG-003: HAG-API-005. REQ-HAG-004: HAG-API-001/002/003. REQ-HAG-005: HAG-API-004. REQ-HAG-006: HAG-API-005/006/007. REQ-HAG-007: HAG-API-002/003/004.

## Implementation references

Memgraph explicit transactions and snapshot conflicts are documented at https://memgraph.com/docs/fundamentals/transactions. Database RBAC is documented as Enterprise at https://memgraph.com/docs/database-management/authentication-and-authorization/role-based-access-control. These references justify the transaction mechanism and recorded enforcement gap; actual behavior must be tested against the pinned image.
