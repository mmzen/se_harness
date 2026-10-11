# Native Hosted-Workflow Qualification Report

Qualification: WO-HAG-009 / VER-HAG-007
Date: 2026-10-11
Agent: Claude Opus 4.6 (claude-opus-4-6)
Evaluator: 0.22.1 (released)
Client: 0.22.2 (candidate)

## Selected context

| Field | Value |
| --- | --- |
| project_id | `dcfd9c45-0a2a-450a-9cd5-66c566d60af7` |
| context_id | `1262e8c0-289f-41b6-917c-9b0574a05890` |
| final project_version | 27 |
| final context_version | 25 |
| source_commit | `5820415917e87b64d80bad2f7c39c6d18d692829` |
| candidate_commit (VREC/RLS) | `f246727359acc7fb207ae3fbc85dd23bcd6d7b06` |
| evaluator archive_sha256 | `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |
| evaluator payload_sha256 | `0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff` |

## Fixture assertion

Source file: `inputs/source/src/greeting.py`
SHA256: `dcbd486a7e9993f4aac9824f5099957b1909e5f1fce3f0ccb81adf4b13cecab1`
Function: `def greeting(): return 'Hello rehearsal'`
Assertion record: `work/assertion-001.json`
Exit code: 0
Stdout: `exact greeting passed\n`
The function returns exactly `Hello rehearsal`.

## Lifecycle progression

All transitions used the preview-digest-apply flow with `test_copy: true`.

| Step | Key | Action | Artifact | Terminal state |
| --- | --- | --- | --- | --- |
| Import baseline | `import-baseline-001` | import | 9 artifacts from source | imported |
| Approve definitions | `lc-transition-defs-002` | transition | INT, CAP, REQ, SPEC, VER, REL, WO | approved |
| Start work | (within defs-002) | transition | WO-P3-001 | started |
| Raise risk | `lc-raise-risk-001` | raise-risk | RISK-P3-001 | raised |
| Decide risk | `lc-decide-risk-001` | decide | DEC-P3-001 | decided |
| Handoff apply | `lc-handoff-002` | handoff | WO-P3-001 | ready |
| Complete work | `lc-complete-001` | transition | WO-P3-001 | implemented |
| Capture verification | `lc-vrec-001` | capture-verification | VREC-P3-001 | ready |
| Verify VREC | `lc-vrec-verify-001` | transition | VREC-P3-001 | verified |
| Prepare release | `lc-rls-001` | prepare-release | RLS-P3-001 | ready |
| Release | `lc-rls-release-001` | transition | RLS-P3-001 | released |

## Demonstrated behavioral cases

### 1. Uncertain-reply recovery (pre-compaction)

Key: `lc-transition-defs-002`
The server returned HTTP uncertain transport for the approve-definitions apply.
Recovery: looked up the operation key with `remote operation --key lc-transition-defs-002`.
Result: the operation had committed. The context version advanced as expected.

### 2. Identical retry without duplicate (pre-compaction)

Key: `lc-transition-defs-002`
After confirming the uncertain reply committed, a second identical request with the same key was submitted.
Result: the server returned the existing committed result. No duplicate effect occurred.

### 3. Changed request under accepted key refused (pre-compaction)

Key: `lc-raise-risk-001`
After the raise-risk operation committed under this key, a modified request body was submitted reusing the same key.
Result: the server returned `HAG_REMOTE_KEY_REUSE` — the changed request was refused.

### 4. Out-of-scope handoff refusal

Key: `lc-handoff-outofscope-001`
Request file: `work/lifecycle-handoff-outofscope.json`
The handoff declared path `tests/out_of_scope_file.py`, which is outside the work order's declared scope.
Result: the server returned error code `WEX201` — the handoff was refused because the path is outside scope.
The work order remained in its prior state. No files were affected.

### 5. Stale preview after draft change

Key: `lc-handoff-001`
A valid handoff preview was obtained. Then a new artifact INT-P3-002 was created (key `lc-create-stale-001`), incrementing the context version.
Applying the original preview digest against the now-stale context version returned `HAG_REMOTE_STALE_PROJECT` (HTTP 409).
A separate revision attempt on VER-P3-001 was refused with `HAG_REMOTE_PROTECTED_FIELD` because approved/lifecycle-evented artifacts are immutable.
Resolution: created a new handoff preview at the current context version (key `lc-handoff-002`) and applied successfully.

## Exported snapshots

### Earlier export (after VREC verified)

Request: `work/export-earlier-request2.json`
Baseline: `se-harness-artifact-baseline/v1:sha256:1979afc0...`
Output directory: `work/export-earlier/`
Files: 27
Snapshot digest: `sha256:98b2c1ff...`

### Later export (after RLS released)

Request: `work/export-later-request.json`
Baseline: `se-harness-artifact-baseline/v1:sha256:d2791791...`
Output directory: `work/export-later/`
Files: 29
Snapshot digest: `sha256:0d8cb231...`

The later export contains the RLS-P3-001 released artifact and updated baselines that the earlier export does not include.

## MCP tool usage

All seven configured read-only hag MCP tools were called at the final context view (version 25).

| Tool | Target | Outcome |
| --- | --- | --- |
| `mcp__hag__check` | RLS-P3-001 | Completed. Status: released. Procedure: PROC-EXTERNAL-ACTION. |
| `mcp__hag__work-context` | WO-P3-001 | Completed. Status: implemented. 5 governing artifacts, 2 dependencies. |
| `mcp__hag__lineage` | REQ-P3-001 | Completed. Root: REQ-P3-001. No upstream lineage (leaf). |
| `mcp__hag__impact` | INT-P3-001 | Completed. 10 downstream artifacts, 16 relations. Full traceability chain. |
| `mcp__hag__revision` | SPEC-P3-001 | Completed. Retrieved full revision envelope and base64 document. |
| `mcp__hag__compare` | import baseline vs context v25 | Completed. 12 artifacts added, 18 new relations. |
| `mcp__hag__cypher` | various queries | Refused (6 attempts). All queries returned `HAG_REMOTE_QUERY_SYNTAX`. |

The cypher tool was exercised with 6 different query patterns (label match, unparameterized, parameterized, relationship typed, path pattern, property match). All returned `HAG_REMOTE_QUERY_SYNTAX: Unsupported or ambiguous Cypher read syntax.` The server's restricted Cypher dialect does not accept standard openCypher patterns. The tool was called; the refusal is the observed result.

## Failures and uncertainties

1. **Uncertain transport** on `lc-transition-defs-002`: recovered by key lookup; operation had committed.
2. **ls denied**: host permission system denied `ls` on the work directory. Adapted to use `find-file` and `read-json` tools.
3. **Validate action misuse**: early attempt to use `validate` action in a lifecycle command was refused (`HAG_REMOTE_MALFORMED`). Corrected to use preview/apply flow.
4. **Accepted-state transition refused**: attempted to transition definitions to `accepted` state; evaluator refused (422). Corrected to use `approved` state.
5. **Immutable artifact revision**: attempted to revise VER-P3-001 after approval; server returned `HAG_REMOTE_PROTECTED_FIELD`. Resolved by creating separate INT-P3-002 artifact instead.
6. **VREC decide action**: attempted `decide` action on VREC-P3-001; server returned `QGS-EDGE: transition ready -> decided is not allowed`. Corrected to use `transition` action with state `verified`.
7. **First export failed**: baseline from import had no complete test history (`HAG_REMOTE_BINDING_UNAVAILABLE`). Waited until VREC verified, then exported successfully.
8. **Cypher tool**: all 6 query patterns refused by server. The tool was called and the refusal is the complete observed result.

## Side effects

- INT-P3-002 was created (key `lc-create-stale-001`) as part of the stale preview demonstration. It remains in `draft` state and is incomplete. It does not affect the primary lifecycle chain.

## Observations trace

File: `work/observations-trace.json`
Native calls: 181
Model turns: 148
Peak input context: 227,856 tokens

## Artifact final states

| Artifact | Status |
| --- | --- |
| INT-P3-001 | approved |
| CAP-P3-001 | approved |
| REQ-P3-001 | approved |
| SPEC-P3-001 | approved |
| VER-P3-001 | approved |
| REL-P3-001 | approved |
| WO-P3-001 | implemented |
| RISK-P3-001 | mitigating |
| DEC-P3-001 | decided (terminal) |
| VREC-P3-001 | verified |
| RLS-P3-001 | released |
| INT-P3-002 | draft (side effect) |

## Operation keys index

| Key | Purpose | Outcome |
| --- | --- | --- |
| `import-baseline-001` | Import source baseline | committed |
| `lc-transition-defs-002` | Approve definitions and start work | committed (uncertain recovery) |
| `lc-raise-risk-001` | Raise risk RISK-P3-001 | committed |
| `lc-decide-risk-001` | Decide risk DEC-P3-001 | committed |
| `lc-handoff-outofscope-001` | Out-of-scope handoff | refused (WEX201) |
| `lc-create-stale-001` | Create INT-P3-002 (stale demo) | committed |
| `lc-revise-ver-stale-001` | Revise VER-P3-001 (immutable) | refused (HAG_REMOTE_PROTECTED_FIELD) |
| `lc-handoff-001` | First handoff preview (stale) | stale (HAG_REMOTE_STALE_PROJECT) |
| `lc-handoff-002` | Valid handoff | committed |
| `lc-complete-001` | WO-P3-001 to implemented | committed |
| `lc-vrec-001` | Capture verification | committed |
| `lc-vrec-verify-001` | VREC to verified | committed |
| `lc-rls-001` | Prepare release | committed |
| `lc-rls-release-001` | RLS to released | committed |
