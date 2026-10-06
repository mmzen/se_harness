# Codex qualification and analysis — 2026-10-06

**Codex completed the real hosted walkthrough and all seven native MCP reads on the existing candidate.** Every native MCP response matches the same HTTP request. Codex correctly identified the large impact response as partial. This improves the native evidence; WO-HAG-001 and WO-HAG-007 remain `in_progress`.

## Observed results

| Check | Actual result | Evidence inside observations.zip |
| --- | --- | --- |
| Exact packaged instruction read | Setup and change files read successfully with normal host configuration and a read-only sandbox | `observations/native-read-normal-profile.json` |
| First walkthrough | Readiness passed; import was `not_sent` because the sandbox could not open the client wheel | `observations/native-walkthrough.json`, `observations/walkthrough/` |
| File diagnosis | `PermissionError: [Errno 13]` opening the exact wheel; ACL differs from readable test files | `observations/native-diagnose.json`, `observations/file-acl-observation.json` |
| Retry prerequisites | Readback confirmed readiness and project version zero before another import attempt | `observations/readiness-before-retry.json` |
| Reviewed walkthrough retry | Exit 0; all 18 installed-client observations passed, including expected refusals | `observations/native-walkthrough-retry.json`, `observations/walkthrough-retry/` |
| First MCP session | All seven tools discovered; each refused because approval policy was `never`; no service response | `observations/native-mcp.json` |
| Reviewed MCP session | All seven reads returned; no review denial or MCP error | `observations/native-mcp-reviewed.json` |
| HTTP/MCP comparison | All seven exact requests and responses match | `observations/http-mcp-comparison.json` |
| Agent interpretation | Six complete reads; impact correctly reported partial at 500 rows; checkpoint-free check correctly reported `not_assessable` with no evaluated gates | `observations/native-mcp-reviewed.json` |

The 18 operations cover readiness, import, original baseline, identical import retry, work context, draft open/create/read/revise, prohibited-relation refusal, stale-version refusal, accepted retry, changed-content key refusal, unchanged baseline, comparison, Cypher, checkpoint-free check and freeze. Expected refusal exits are successful test assertions. The sum of recorded command durations is 90.743 seconds, excluding model reasoning and approval review.

The original baseline stays `se-harness-artifact-baseline/v1:sha256:42873b9a551cede806281cdb1afcc413cf626f46051b1644880759b68cb9bf57`. The resulting draft context is `cc35dfd9-0cda-4613-b939-acb9b829d46d`, version 2; final project version is 5. Freeze produces `se-harness-artifact-baseline/v1:sha256:2ae23cb3a92de98b7ea6c75f07cbdf8e146aede9f6a3eccba1895d7459ece15f`. These are sandbox data identities, not lifecycle approvals.

## What caused the Codex problems

Three observations must remain separate:

1. **Earlier temporary-profile refusal.** The earlier run could not start a shell read. Its temporary profile omitted the normal host's Windows sandbox setting. The normal-profile read now succeeds. This supports a test-configuration explanation, but the exact old rejection rule was not isolated; do not claim a controlled causal comparison.
2. **Current wheel access failure.** The first new walkthrough reached the service, then failed locally before sending the import. The exception chain identifies the exact wheel. Its ACL grants the owner, Administrators and SYSTEM access; the readable comparison file also has sandbox access entries. The retry used the normal automatic approval reviewer for the same test launcher and original wheel. Only its output directory changed, preserving the failure. No ACL was changed, protected wheel copied, persistent setting weakened or bypass flag used.
3. **Current MCP approval setting.** The read-only `exec` session used approval policy `never`. The tools required approval, so all calls were refused by Codex before receiving service responses. A new session submitted the unchanged requests through `--approve-for-me`, the normal automatic reviewer. It did not install an always-allow tool rule. All seven then succeeded.

These failures do not establish an authentication or service defect. Actual model sessions succeeded with the normal host credential store. No OAuth credentials were copied into test profiles. This observation does not guarantee future authentication lifetime.

The raw diagnostic records also retain command-interface mistakes while inspecting `codex sandbox` help and its required permission-profile option. Those are diagnostic invocation errors, not hosted-service failures.

## Component and execution identity

- Product candidate: `5fa50787dba1fdd010f625335d844416dd3bf002`. No product source changed during this continuation. Later evidence commits are separate review heads.
- Combination: `sha256:435c059909edcc93b029508058546cd20a5e005bc5b818e6707281df4953a633`; [full component identities](combination.json).
- Codex CLI: 0.159.2; normal configured model: `gpt-6-astra`. No model override or persistent host configuration edit.
- Exact candidate client: 0.22.2; packaged guidance: 0.2.7; service: 0.1.0.dev1. These are unpublished development components.
- Checkout governor and service evaluator remain the separate public 0.22.1 wheel with archive SHA-256 `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
- Service image: `sha256:8fed660c2b13e80022dfff3a4dbd5c4f38de5b5f03f5ee05a5c5b394ddc4af83`. Linux/amd64 Docker, Python 3.13.16 and Memgraph 3.13.1; exact pins are in the combination.
- Fresh private Compose project `hagcodex20261006`, loopback port 18089. Existing graphs and the read-only original Git-blob source were preserved.

The candidate plugin archive was extracted and its 28 file identities were checked. Native Codex explicitly read those exact guidance files. The normal published Verity Plane plugin was disabled only for these test invocations to avoid mixing instruction versions. **This does not prove automatic candidate-plugin installation/loading, startup/compaction delivery or desktop behavior.** The walkthrough is a guided run of an inspected launcher, not an unscripted authoring exercise. The successful walkthrough needed reviewed execution escalation, so it does not establish operation entirely within the unextended sandbox.

## Analysis and remaining work

The client/service protocol works through native Codex in this tested configuration. Codex followed the selected guidance, preserved the explicit views and budgets, reported actual failures, and correctly distinguished a partial impact response from a complete context. The broad impact response contains 123 artifacts and 377 relations, with `complete: false` and `row_limit`. Exact transport equality preserves that limitation; it does not make the traversal complete. One successful native session is evidence for this run, not a guarantee across models or repeated runs.

The [earlier Claude report](../claude-20261006/report.md) remains unchanged. Claude's large-response reporting failure is still open. Its smaller successful probe and this Codex success do not erase that observation. The next useful correction to investigate is a concise, readily visible completeness summary for large results, with a native retest of the affected behavior. This is an analysis recommendation, not a changed accepted contract or an implementation in this report.

Complete final qualification against the exact tuple before work completion: assess the remaining independent evaluator and restart/restore coverage, which currently belongs to candidate04. The existing candidate05 source suite (1,319 tests with 23 reported skips), live boundary checks, distribution checks and pinned builds remain linked through the earlier report; they were not rerun for this evidence-only continuation. Skips remain unperformed coverage.

RISK-HAG-001 stays raised. The private sandbox's application controls do not establish Memgraph-enforced read-only access. No hosted VREC, completion, verification acceptance, merge, release, public exposure or authority cutover is claimed. Desktop and automatic candidate-plugin loading were not tested; previous public-release omissions are not transferred to this candidate.

## Retention and review

[observations.zip](observations.zip) retains actual prompts, arguments, outputs, requests, responses, failures and qualification helpers. [inventory.json](inventory.json) lists exact member hashes; [continuation.json](continuation.json) records the live sandbox selection and remaining work. Images, wheels, complete package/source trees, credential files, host profiles and database dumps are excluded. The previous handoff packet is preserved byte-for-byte before any supported rebind.

Review checked that the report distinguishes protocol results from model prose, keeps the product candidate fixed, preserves all earlier failures and does not infer authority from successful tests. No additional implementation or test infrastructure is introduced into product code. The existing unfinished-work publication grant covers this evidence update to draft PR #535, keeping its original target and comparison base. The selected released continuation remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`; structural handoff checks cannot replace missing qualification.

Released validation reports 1,970 artifacts, zero errors and 63 existing warnings. Both selected review preflights pass. The complete original-base PR check first refused the stale handoff binding. The released evidence command rebound the live packet after its previous bytes were preserved; the same complete PR check then passed. These results are retained under `review-checks/`. This structural pass does not complete qualification.
