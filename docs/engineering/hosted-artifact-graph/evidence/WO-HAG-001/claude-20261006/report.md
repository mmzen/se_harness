# Claude qualification — 2026-10-06

Claude authentication now works. The native tests found a real MCP discovery defect, which is corrected in candidate `5fa50787dba1fdd010f625335d844416dd3bf002`. The corrected service passes the native tool calls and the repeated service checks. **Native-agent qualification remains incomplete because Claude misreported a large partial response.** WO-HAG-001 and WO-HAG-007 remain `in_progress`.

## Observed results

| Check | Actual result | Evidence inside observations.zip |
| --- | --- | --- |
| Native Claude on preceding candidate04 | 18 installed-client steps passed; native MCP exposed no tools | `observations/native-session.json`, `observations/walkthrough/`, `observations/mcp-session.json`, `observations/mcp-session-v2.json` |
| MCP defect diagnosis | All seven tool schemas lacked the root `type: "object"` required by Claude's MCP validator | `observations/mcp-diagnostic-excerpt.txt` |
| Regression on preceding image | New regression fails in seven tool subtests | `observations/mcp-regression-old-image.json` |
| Installed corrected runtime | Five test methods pass | `observations/runtime-installed-05.json` |
| Native Claude on candidate05 | 18 installed-client steps passed on a fresh sandbox graph | `observations/native05/native-session.json`, `observations/native05/walkthrough/` |
| Native MCP on candidate05 | All seven tools discovered and called; every response equals the same HTTP request | `observations/native05/mcp-session.json`, `observations/native05/http-mcp-comparison.json` |
| Large impact response | Service reports `complete: false` and `row_limit`; Claude incorrectly calls it complete without reading the output file | `observations/native05/impact-native-tool-output.json`, `observations/native05/mcp-session.json` |
| Separate bounded impact probe | With one row, Claude correctly reports `complete: false`, `row_limit`, and no full governing-context claim | `observations/native05/mcp-bounded-session.json` |
| Live service boundary suite | Exit 0; 52 check observations plus completion record (53 files) | `observations/boundaries-05/`, `observations/boundaries-05.json` |
| Full source suite | 1,319 tests, 23 reported skips, exit 0 | `observations/source-suite-05.json` |
| Distribution and CLI smoke | Passed | `observations/distribution-checks-05.json`, `observations/cli-smoke-05.json` |
| Released validation | 1,970 artifacts, zero errors, 63 existing warnings | `observations/released-validation-05.json` |
| Pinned builds | Two independent builds passed; exact tuple rebuilt and separately installed | `observations/client-replay-05.json`, `package-05/`, `observations/client-install-05.json` |

Expected refusal outcomes are successful test assertions, not admitted invalid changes. Skips are not passes. The source-suite total includes the reported skips.

## Exact candidate and environment

- Product candidate: `5fa50787dba1fdd010f625335d844416dd3bf002`. Later evidence commits are review heads, not this tested product commit.
- Combination: `sha256:435c059909edcc93b029508058546cd20a5e005bc5b818e6707281df4953a633`; [complete component identities](combination.json).
- Candidate client: 0.22.2; candidate plugin: 0.2.7; service: 0.1.0.dev1. These remain unpublished.
- Governor and service evaluator: public 0.22.1, archive `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
- Claude Code: 2.1.273; model explicitly selected for these tests: `claude-haiku-4-5-20251001`. The configured default model was unavailable; no persistent model setting was changed.
- Native host: Windows. Service: Linux/amd64 Docker, Python 3.13.16, Memgraph 3.13.1. Exact image identities are in the combination.
- Service image: `sha256:8fed660c2b13e80022dfff3a4dbd5c4f38de5b5f03f5ee05a5c5b394ddc4af83`.
- Fresh private Compose project: `hagmcp20261006`, loopback HTTP port 18088. Existing candidate04 volumes were preserved. The original public Git-blob source volume is mounted read-only.
- Normal Claude credential store used. OAuth credentials were not copied into test profiles. The exact candidate plugin was loaded only for these sessions and checked byte-for-byte against its archive.

The client and plugin archive hashes differ from candidate04 because they were rebuilt for the new candidate. Every unpacked member is byte-identical; no member was added or removed. `observations/component-content-comparison.json` retains that comparison. The service code changed as described below; earlier service results are not relabelled as candidate05 runs.

## Correction and review

`server/hosted_artifact_graph/app.py` now places `type: "object"` at the root of each advertised MCP input schema. The existing operation constraints remain. `tests/hosted_artifact_graph/test_runtime.py` checks real advertised schemas and their rejection of invalid shapes. `tests/hosted_artifact_graph/qualify_boundaries.py` checks advertised object schemas and validates actual requests before HTTP/MCP comparisons.

This corrects native client discovery within WO-HAG-001's approved service and test paths. It does not change accepted definitions, decision rights or the selected evaluator. Review checked all seven operations, schema constraints and exact HTTP parity. The old-image regression failure is retained alongside the corrected-image pass.

## What the native runs establish

Claude read the exact packaged setup/change guidance and an inspected test launcher, then invoked the actual installed CLI sequence. The sequence exercises import, unchanged baseline reads, work context, draft creation/revision, invalid and stale refusals, retry/key reuse, comparison, Cypher, checkpoint-free evaluation and freeze. This is a guided native run with a prepared launcher; it is not an unscripted end-to-end workflow or a desktop test.

The original baseline remains `se-harness-artifact-baseline/v1:sha256:42873b9a551cede806281cdb1afcc413cf626f46051b1644880759b68cb9bf57`. The candidate05 walkthrough created context `e6e47c2e-72af-4547-aa74-e838a3571d88` at version 2 and froze `se-harness-artifact-baseline/v1:sha256:80a56173a239b40f0a97189958fce44c01b75bd65a7d45f8ed2b54f2e55210c2`. The later boundary suite advanced the disposable context to version 4; the native responses remain bound to their earlier observed version.

The seven native MCP operations are revision, work-context, compare, impact, lineage, check and cypher. Six responses are complete. The broad impact response is partial. Exact HTTP/MCP equality includes that partial result; equality does not turn it into a complete governing context.

Claude Code saved the large impact response to a file. Claude did not inspect that file and incorrectly marked the response complete. The exact saved bytes are retained. A separate, smaller probe shows that Claude can interpret a visible partial result correctly. **That follow-up does not erase the original reporting failure or establish reliable handling of saved large responses.**

Generated narratives also contain unsupported timings and imprecise step descriptions. The sum of recorded command durations is 93.358 seconds on candidate04 and 90.949 seconds on candidate05; use the command records rather than Claude's totals. Cypher is a graph query. Freeze creates an immutable baseline, not lifecycle approval. The checkpoint-free result is `not_assessable` with no checkpoint gates evaluated; it does not report that all gates passed.

## Remaining qualification and decisions

The current result improves SC-04 and SC-10 coverage and fixes native schema compatibility. It is not a blanket pass for all twelve VER-HAG-001 scenarios. The large-response reporting issue remains. Codex's earlier native run could not read the candidate guidance under its tool policy; no new Codex run is claimed here. Desktop remains unperformed.

Independent evaluator and restart/restore results for candidate04 remain available in [the historical report](../phase2-20261005/protocol04-assessment.md). They were not rerun on candidate05 in this report. Final exact-tuple qualification must account for that distinction. No historical VREC candidate or evidence was rebound to this service correction.

RISK-HAG-001 remains raised. The private sandbox tests prove application query controls, not Memgraph-enforced read-only authorization. There is no public deployment or authority cutover.

No completion transition, hosted VREC, human verification, merge, release or deployment was performed. The existing unfinished-work publication grant covers retaining this evidence in draft PR #535 with the original target and blockers disclosed.

## Retention and continuation

[observations.zip](observations.zip) preserves actual arguments, outputs, failures, component build records, native transcripts and qualification scripts. [inventory.json](inventory.json) lists every member's byte count and SHA-256. The earlier WO-HAG-001 handoff packet is retained byte-for-byte as `historical/WO-HAG-001-handoff-before.md` before any supported rebinding.

Images, wheels, complete sources, database backups and credential files are excluded from the evidence archive. The combination and command records identify local build locations and digests. These local large artifacts are not claimed to be published release assets.

[continuation.json](continuation.json) gives the selected candidate, local sandbox inputs and remaining coverage. Obtain fresh context with released 0.22.1 before continuing. The observed context returned `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`: `harnessctl check REPO --artifact WO-HAG-001 --checkpoint handoff`. A passing structural handoff cannot replace missing qualification.

The complete original-base PR check initially refused the old handoff binding. Released `evidence` rebound the live packet after its previous bytes were archived, and the same complete PR check passed. The original refusal, supported rebind and pass are retained under `review-checks/` in the archive. This structural pass does not close the qualification gaps above.
