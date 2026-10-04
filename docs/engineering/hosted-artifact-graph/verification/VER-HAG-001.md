+++
id = "VER-HAG-001"
type = "verification"
title = "Independent hosted context and draft-authoring qualification"
status = "approved"
owners = ["quality-owner"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-HAG-001", "REQ-HAG-002", "REQ-HAG-003", "REQ-HAG-004", "REQ-HAG-005", "REQ-HAG-006", "REQ-HAG-007", "REQ-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Independent hosted context and draft-authoring qualification

## Independence

Expected values come from REQ-HAG-001 through REQ-HAG-008 and SPEC-HAG-001 through SPEC-HAG-003. The positive context fixture is pinned to source commit 82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1 and WO-RLS-038. Its governing IDs and path membership are fixed in SPEC-HAG-001 before implementation. Compare evaluator results with the independently installed 0.22.0 release and its recorded archive/payload digests; do not generate expected answers from the candidate server. A second reviewer can replay retained requests against the recorded component tuple.

Primary platform: Linux x86_64 Docker, Python 3.11 or later, one service and one transactional Memgraph instance with the exact version/image/configuration recorded. Any Windows-host Docker execution is additional observed coverage. Unsupported or unavailable prerequisites produce an unperformed result, never a pass. The checkout remains governed by released 0.22.0, even when the separately installed candidate wheel supplies new remote commands.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-HAG-001 | Inspection + integration | SC-01, SC-02 | Full original bytes/provenance survive import; deterministic repeat and explicit duplicate/unresolved refusal |
| REQ-HAG-002 | Integration + invariant | SC-02, SC-05, SC-10 | Revision content is append-only and baseline B remains byte/digest identical |
| REQ-HAG-003 | Comparison + demonstration | SC-03, SC-04 | Known governing set/scope equals the independent fixture; view and completeness are explicit |
| REQ-HAG-004 | Integration | SC-05, SC-06 | Incomplete draft accepted; malformed and prohibited relation/state edits refused without effects |
| REQ-HAG-005 | Concurrent/fault integration | SC-07, SC-08 | One competing write succeeds; dependency staleness refuses; retry returns original accepted result; faults roll back |
| REQ-HAG-006 | Protocol/security tests | SC-04, SC-09 | Domain/MCP/Cypher reads obey view, admission and bounds; deferred DB authorization remains explicit |
| REQ-HAG-007 | Differential tests + inspection | SC-03, SC-06, SC-11 | Pinned server evaluation and original path/code hashes preserved; unavailable bindings never pass |
| REQ-HAG-008 | Packaged demonstration + resilience | SC-10, SC-12 | Actual component tuple completes the twelve steps; restart/restore and incompatibility outcomes recorded |

## Acceptance scenarios

1. **SC-01 — Import fidelity.** Read complete formal Git blobs through the canonical importer. Compare every original byte digest, identity, relation, source path and commit. Include approved/implemented/verified/released historical records; confirm no fresh approval event is created. In disposable copies inject duplicate artifact IDs and unresolved targets; both fail baseline completion with actionable deterministic reports. An unrelated Explorer export is refused as an unsupported import source.
2. **SC-02 — Repetition and immutability.** Import the same snapshot twice. Expect one equivalent baseline and no duplicate revisions/receipts. A changed byte under the same declared provenance identity is refused. Fix serialization byte vectors manually from the SPEC-HAG-001 rules, including ordering, Unicode, body changes and edge changes; independently compute SHA-256. This must happen before implementing the serializer.
3. **SC-03 — Work context.** Ask through the packaged CLI for WO-RLS-038 at B. Match all twelve governing IDs, the eleven declared paths and the separately classified dependencies in SPEC-HAG-001. Compare significant findings with the released evaluator against the same pinned source view. In a synthetic branch of the reference fixture add one valid open blocking decision and one absent evidence blob; retain distinct pending-decision and unavailable-evidence outcomes. Do not change the historical source fixture.
4. **SC-04 — Read consistency.** Compare exact revision, work context, dependency/impact, baseline comparison, verification lineage and evaluator blockers across HTTP and MCP. Verify baseline and draft views differ only as declared. Unknown baseline/project, truncated rows/bytes/depth and missing references must not appear as empty complete success. Cross-project access is denied even though deployment contains only one project.
5. **SC-05 — Valid drafts.** Open a context at B; create an evaluator-template requirement with legitimate incompleteness, revise its body and a valid derives_from capability target, and check it. Expect new immutable revisions and exactly their declared edges. The unfilled draft produces authoring findings without becoming an approved definition. Its new context identity accompanies every result.
6. **SC-06 — Actual invalidity and protected input.** Submit malformed TOML, a type/ID mismatch, duplicate metadata and a requirement derives_from release-record edge. Separately attempt imported lifecycle, human decision, actor and evidence-record changes. Each refuses with a stable classification and no revision/head/version/receipt partial state. A locally validated request with different server rights or evaluator identity still refuses at the server.
7. **SC-07 — Concurrent/stale governing context.** Use two independent clients and database connections starting at project version N. Race different writes; exactly one accepts. Repeat after changing only a governing capability or another project artifact; the previously prepared request refuses even if its target draft revision is unchanged. No automatic retry may silently update its expected version or baseline.
8. **SC-08 — Receipt and transaction recovery.** Inject a connection loss after commit but before client receipt. Retry the same key/full request: return the original result, including its accepted version, exactly once. The same key with altered content, context or baseline refuses. Operation lookup is principal/project-scoped. Inject failure between graph writes before commit and at commit; subsequent reads show all effects or none, including receipt and version. Concurrent identical keys yield one accepted operation.
9. **SC-09 — Cypher and resource boundary.** Execute allowed parameterized read forms at B and a named draft view. Reject write clauses, CALL, subqueries, administration, multiple statements, schema operations, file loading and grammar ambiguities before database execution. Test comments, literals, case and parameter substitution without relying on keyword matching. Confirm view binding, row/byte/depth/time limits and rollback behavior. Report that this proves the application contract only; Memgraph-enforced read-only authorization remains unresolved. No public exposure or authoritative-pilot claim is permitted.
10. **SC-10 — Twelve-step user walkthrough.** Execute SPEC-HAG-003's complete sequence through the actual packaged CLI/plugin-guided agent path: import, freeze B, retrieve context, read with domain/MCP/Cypher, open a draft, submit valid body and relation revision, check, refuse an actually invalid revision, refuse stale context, recover an accepted retry, retrieve unchanged B, and retain the report. Mocks and direct database calls cannot replace this evidence.
11. **SC-11 — Historical bindings and evaluator selection.** Independently reproduce legacy path/content hashes using canonical text handling and all original scoped code inputs. Moving a file, changing scoped code or removing evidence must affect assessment as the released contract specifies. A new remote baseline digest cannot satisfy a legacy digest field. Reject a substituted same-version wheel, wrong payload/policy identity, candidate-as-governor fallback and unsupported evaluator. Inspect that no parallel lifecycle policy or client-supplied identity grants mutation rights.
12. **SC-12 — Package and recovery.** Build and separately install the actual client and candidate plugin guidance; build the service image and record all component digests. Start from explicit initialization, then restart with the same volume and recover B and an accepted operation receipt. Restore a consistent backup into a fresh volume and compare identities at the recorded cutoff. An unsupported client/API/evaluator/schema tuple and an uninitialized/incompatible schema fail before mutation, without automatic migration. Record the configured limits, measured import/context/command latency, restart/restore time and storage size; no unmeasured production SLA claim.

## Static checks and existing regressions

Inspect one admission path, one transaction acceptance path and shared domain/MCP read handlers. Verify secret redaction and bounded regular-file handling. Run the repository's applicable canonical test runner and distribution checks after implementation, together with the new remote-client and container integration tests. Reuse existing evaluator tests rather than copying their implementation. Record exact commands and exits; a skipped Memgraph integration scenario is unperformed coverage.

## Evidence retention

Retain bounded request/response transcripts, component tuple, source identities, fixture expectations, actual command exits, failure observations, read comparisons and the verification report under `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/`. Do not retain secrets, entire database dumps or unnecessary source duplicates. Large immutable images/source archives/backups receive durable locations and content digests in the report. These observations are not a hand-authored VREC. Use the existing released capture procedure later, on the actual clean candidate; it allocates the record and evaluator evidence destinations.

## Residual uncertainty

Database-side read-only authorization is unresolved by user direction and must remain visible in the report. Phase 2 does not prove authenticated human approvals, whole-workflow hosted write coverage, authority cutover, multi-tenant isolation, adversarial public-service readiness, power-loss guarantees, production RPO/RTO or rolling upgrades. Failure to express draft validation or historical bindings with the selected release requires a scoped decision before implementation proceeds past that boundary.
