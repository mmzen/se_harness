# Continuation Addendum: Hosted Qualification Checks

Qualification: WO-HAG-009/011, VER-HAG-007
Session: claude-253 (continuation of claude-251)
Date: 2026-10-11
Agent: Claude Opus 4.6 (claude-opus-4-6)
Evaluator: 0.22.1 (released)
Client: 0.22.2 (candidate)

## Scope

This addendum records checks performed in session claude-253 against the test project established in claude-251. The prior report (`inputs/prior-work/native-report.md`) remains unchanged. This addendum distinguishes earlier observations from newly executed checks and states remaining limits.

No new definitions, lifecycle decisions, imports, resets, releases, or publication were performed. The only mutation-endpoint operations were an identical cached retry and a conflicting request under the same accepted key.

## Selected context

| Field | Value |
| --- | --- |
| project_id | `dcfd9c45-0a2a-450a-9cd5-66c566d60af7` |
| context_id | `1262e8c0-289f-41b6-917c-9b0574a05890` |
| context_version | 25 |
| project_version (start) | 27 |
| project_version (end) | 27 |
| authority_mode | `sandbox-projection` |
| test_copy | `true` |

## 1. MCP tool exercise

All seven read-only MCP graph tools were called against context version 25. Each tool used schema `se-harness-graph-read/v1`; responses arrived as `se-harness-graph-read/v2`.

| Tool | Target | Outcome |
| --- | --- | --- |
| `mcp__hag__check` | `WO-P3-900` | Completed. Returned artifact status and compliance predicates. |
| `mcp__hag__lineage` | `REQ-P3-900` | Completed. Returned lineage graph with root `REQ-P3-900`. |
| `mcp__hag__revision` | `sha256:7b40dc95ba3e63e69b10ec0cbf3042b637a799ed0bb824c7f6bfb234d23de55c` | Completed. Returned revision envelope with base64-encoded document. |
| `mcp__hag__work-context` | `WO-P3-900` | Completed. Returned work order scope, governing artifacts, and dependencies. |
| `mcp__hag__impact` | `INT-P3-001` | Completed. Returned downstream impact with affected artifacts and relations. |
| `mcp__hag__compare` | context v25 vs v25 | Completed. Self-compare returned empty diff (no changes between identical versions). |
| `mcp__hag__cypher` | `MATCH (a:Artifact) RETURN a.artifact_id AS id LIMIT 10` | Completed. Returned artifact identifiers from the graph. |

### Cypher dialect observations

The server accepts a constrained Cypher read dialect. The successful query required:

- A node label (`:Artifact` accepted; `:Binding`, `:ArtifactRevision` refused with "Unknown public label or relationship").
- The property `artifact_id` (not `id` or `status`).
- An `AS` alias on the `RETURN` clause.
- A `LIMIT` clause.

Relationship traversal queries (e.g., `MATCH (a:Artifact)-[r:derives_from]->(b:Artifact)`) were refused with `HAG_REMOTE_QUERY_SYNTAX`. The constrained dialect does not accept relationship patterns or unlabelled node matches.

### Compare limitation

Comparing different context versions (v1 vs v25 or v24 vs v25) returned `HAG_REMOTE_STALE_CONTEXT`. Only the self-compare (v25 vs v25) succeeded.

## 2. Identical-retry check

### Method

The original native-authored request file `inputs/prior-work/lifecycle-transition-defs-apply.json` was resubmitted via `remote rehearse --request`. This file contains key `lc-transition-defs-002`, mode `apply`, `expected_project_version: 16`, `expected_context_version: 14`, and the original `preview_digest`.

### Result

The server returned the cached receipt with no additional version increment.

| Field | Value |
| --- | --- |
| outcome | `accepted` |
| receipt_id | `sha256:78b226ab7b97a1214d2fdc3cb63df7cb3785266f1aa7ccc416e9f9a3adc07893` |
| request_digest | `sha256:08e28cf44227dc4fe64ae34e6699c226e56897bfe36c2017047fe9bba18bd4bc` |
| versions.project | before: 16, after: 17 |
| versions.context | before: 14, after: 15 |
| http_status | 200 |
| record | `work/identical-retry-001.json` |

The returned versions (project 16 to 17, context 14 to 15) match the original execution point, not the current state (project 27, context 25). A post-retry status check (`work/status-002.json`) confirmed project_version remained at 27. The server returned the existing committed result without creating a duplicate effect.

### Changed-content refusal

A modified request file (`work/lifecycle-transition-defs-conflict.json`) reused the same key `lc-transition-defs-002` with one changed reason field on `INT-P3-001`.

| Field | Value |
| --- | --- |
| outcome | `refused` |
| http_status | 409 |
| error.code | `HAG_REMOTE_KEY_REUSE` |
| error.message | `Operation key has different content.` |
| record | `work/conflict-retry-001.json` |

The server detected the content difference and refused the request. No version increment occurred.

## 3. Audit of prior report claims

The prior report (`inputs/prior-work/native-report.md`) was checked against the prior call index (`inputs/prior-native-call-index.json`, 181 native calls from claude-251).

### Section 3.1: Uncertain-reply recovery

**Prior claim**: The server returned HTTP uncertain transport for the `lc-transition-defs-002` apply. Recovery used `remote operation --key lc-transition-defs-002`. The operation had committed.

**Call index evidence**: Event 296 wrote `lifecycle-transition-defs-apply.json` with key `lc-transition-defs-002`. Event 298 submitted this request via `remote rehearse`. Event 305 performed `remote operation --key lc-transition-defs-002` and confirmed the operation had committed.

**Assessment**: The call index supports the uncertain-recovery sequence. The apply was submitted, and the key lookup confirmed commitment.

### Section 3.2: Identical retry without duplicate

**Prior claim**: "After confirming the uncertain reply committed, a second identical request with the same key was submitted. Result: the server returned the existing committed result."

**Call index evidence**: After event 305 (the key lookup), no second `remote rehearse --request` call with `lifecycle-transition-defs-apply.json` appears in the call index. The only follow-up was the lookup at event 305.

**Assessment**: The prior report described a lookup as an identical retry. A lookup (`remote operation --key`) queries the status of an accepted key. It does not resubmit the original request to the rehearse endpoint. The task states: "Lookup alone is not execution of a retry." This session executed the actual identical retry (see Section 2 above) and confirmed the cached receipt return.

### Section 3.3: Changed request under accepted key refused

**Prior claim**: After the raise-risk operation committed under key `lc-raise-risk-001`, a modified request reusing the same key was refused with `HAG_REMOTE_KEY_REUSE`.

**Call index evidence**: Event 386 wrote `lifecycle-changed-key-refused.json` with key `lc-raise-risk-001` and changed content. Event 388 submitted this request and received `HAG_REMOTE_KEY_REUSE` (HTTP 409).

**Assessment**: The call index supports this claim. The changed request was submitted via `remote rehearse` and was refused.

### Section: MCP tool usage

**Prior claim**: All seven MCP tools were called. Cypher was exercised with 6 query patterns; all returned `HAG_REMOTE_QUERY_SYNTAX`.

**Assessment**: The prior report accurately recorded the Cypher refusals. This session discovered the constrained dialect requirements (mandatory `:Artifact` label, `artifact_id` property, `AS` alias, `LIMIT`) and achieved a successful Cypher read.

## 4. Retained work files

| File | Purpose |
| --- | --- |
| `work/status-001.json` | Initial service status (project_version 27) |
| `work/status-002.json` | Post-retry service status (project_version 27, unchanged) |
| `work/identical-retry-001.json` | Identical retry result (cached receipt returned) |
| `work/lifecycle-transition-defs-conflict.json` | Modified request for conflict test |
| `work/conflict-retry-001.json` | Conflict test result (HAG_REMOTE_KEY_REUSE) |
| `work/observations-001.json` | Mid-session observations snapshot |
| `work/native-observations.json` | Final observations |
| `work/native-report.md` | This addendum |

## 5. Remaining limits

1. **Cypher relationship traversal**: The constrained dialect refused all relationship-pattern queries. Only label-property queries on `:Artifact` succeeded.
2. **Compare across versions**: Only self-compare (same version vs same version) succeeded. Cross-version compare returned `HAG_REMOTE_STALE_CONTEXT`.
3. **Database read-only enforcement**: Deferred under `RISK-HAG-001`. The `database_read_only_enforcement` field reports `deferred: RISK-HAG-001`.
4. **No verification, release, deployment, or authority switch**: This session performed read-only graph queries and two authorized mutation-endpoint tests. It grants no real verification or release authority.
5. **Instruction read timing**: This session cannot retroactively prove that a procedure was read before an earlier action in claude-251.
6. **Prior report unchanged**: The prior report at `inputs/prior-work/native-report.md` was not modified. This addendum records the correction to Section 3.2 separately.

## Observations summary

| Metric | Value |
| --- | --- |
| Native calls (this session, final) | 60+ |
| Model turns (this session) | 30+ |
| Peak input context | 177,246 tokens |
| Prior session native calls | 181 |
| MCP tools exercised | 7/7 completed |
| Cypher queries attempted | 12+ (1 succeeded) |
| Mutation-endpoint tests | 2 (1 cached receipt, 1 refused) |
| Project version change | None (remained 27) |
