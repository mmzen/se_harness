# Hosted Artifact Graph: Phase 2 qualification

The private sandbox completes the agreed read, draft-authoring and recovery outcome on product candidate `21d268664ffeb111b8b9e9e94921073c7bc99ec1`. The assessment covers WO-HAG-001 and the supporting WO-HAG-007 correction under VER-HAG-001. These are observed test results, not human verification or merge approval.

## Result and component identity

An agent retrieves the fixed work context, creates and revises an incomplete draft through the installed client, receives specific refusals, recovers an accepted operation after a lost reply, and retrieves the original baseline unchanged. Claude runs the packaged walkthrough with the candidate plugin loaded. Both native CLIs exercise all seven MCP reads, which match the corresponding HTTP responses. Large partial impact results remain partial.

| Component | Tested identity |
| --- | --- |
| Product source | `21d268664ffeb111b8b9e9e94921073c7bc99ec1` |
| Combination | `sha256:febab9cfb9a72fe2e78b5ef64c3da9319aa2e95305ae1840e9c981584ebe0b96` |
| Client | Unpublished 0.22.2; wheel `9c3e37dfd82dce4541ae06b2c50dcdd7cc10bc3b3d4b7a167b7f0e4a098512b2` |
| Plugin | Unpublished 0.2.7; both host ZIP and inventory digests in [combination.json](combination.json) |
| Service | 0.1.0.dev1; image `sha256:6b782fb0aa48bddc655801a4c1b709d90b0cb02d17c4f9b52905574165ccbb35` |
| Runtime/store | Linux/amd64, CPython 3.13.16, Memgraph 3.13.1; immutable pins in the combination |
| Evaluator | Separate public 0.22.1, archive `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |

The client and plugin archives and service image derive from the same clean source commit. The generated combination file retains its original build-time statement, `built; qualification pending`; this report records the later qualification observations. A later evidence or governance commit does not change the product identity above. The checkout governor remains the isolated public evaluator.

## Requirement and scenario assessment

Paths below refer to members of [observations.zip](observations.zip), under `bounded/`, unless another prefix is stated. [inventory.json](inventory.json) gives every retained member's byte count and SHA-256.

| VER-HAG-001 case | Observed evidence and result | Assessment |
| --- | --- | --- |
| SC-01 — Import fidelity | `imported-bytes.json` compares all 1,909 original Git documents, byte hashes, IDs, paths, relations and provenance. `imports/` refuses duplicate IDs, unresolved targets, changed declared bytes and Explorer input. Imported lifecycle claims remain original bytes. | Pass for the public reference snapshot. |
| SC-02 — Repetition and immutability | `walkthrough/` returns the same import receipt on identical retry and retains B after draft edits. Fixed pre-implementation canonical vectors remain in the source fixtures; `wire-shape-checks.json` and the source suite exercise them. | Pass. |
| SC-03 — Work context | `history/released-oracle.json` and `history/historical-bindings.json` compare the independently installed release with the hosted result. The fixed context has twelve governing IDs, eleven paths and two dependencies. `context-variants/` retains an open blocking decision and a separate missing-evidence result while preserving the reference source. | Pass. |
| SC-04 — Read consistency | `native-claude/mcp-http-comparison.json`, `native-codex/http-mcp-comparison.json` and `boundaries/` establish seven exact HTTP/MCP comparisons, explicit views, unknown-identity refusals and row/byte/depth bounds. Impact reports `complete=false`, `row_limit`. | Pass for the tested views and limits. |
| SC-05 — Valid drafts | `walkthrough/` uses the released authoring template through the installed remote client, accepts legitimate incompleteness and appends a body/relationship revision. B stays unchanged. | Pass. |
| SC-06 — Invalidity and protected inputs | `boundaries/` refuses malformed TOML, duplicate metadata, type/ID mismatch, prohibited relations, imported decisions/evidence/state, forged actor fields and incompatible rights/identities. Before/after store fingerprints match on refusals. `live-cli-refusal-assessment.json` confirms specific malformed/duplicate refusals reach the real installed CLI. | Pass. |
| SC-07 — Concurrent and stale inputs | `boundaries/` races independent connections: one different request accepts and identical keys recover one receipt. `receipt-inputs/` creates another real artifact, keeps the pending request's selected revision unchanged, and receives `STALE_PROJECT`. | Pass on this run. Earlier unexplained race failure remains recorded below. |
| SC-08 — Retry and transaction recovery | `lost-reply/` suppresses an actual committed response, then recovers the same result with no extra increment. `lost-reply-cli-assessment.json` confirms that installed-CLI lookup and retry after restart also return the exact original result without another increment. `receipt-inputs/` refuses changed context/baseline under an accepted key. `boundaries/` checks principal-scoped lookup and rollback after graph writes, before commit and at failed commit. | Pass. |
| SC-09 — Cypher boundaries | `boundaries/` exercises parsed allowed reads, unsupported forms, selected-view restriction, budgets and rollback. `read-time-bound.json` records the real five-second database transaction limit. | Pass for the application contract. Direct time stress is not a public-grammar/HTTP exhaustion or database-authorization test. |
| SC-10 — Packaged agent walkthrough | `native-claude/walkthrough-session.json` records the session-loaded candidate plugin and guided execution of eighteen real installed-client operations covering the twelve required steps. The two native MCP sessions exercise the read surface. | Pass for this guided CLI path. |
| SC-11 — Historical bindings/evaluator | `history/` independently recomputes the original legacy digest, including original paths, scoped code and line-ending rules. `integrity/` refuses substituted archive/payload, candidate-as-governor and damaged stored links/contracts. The missing-evidence variant stays incomplete. | Pass. |
| SC-12 — Packages and recovery | Pinned two-build replay matches; installed runtime checks and exact package readback pass. Explicit initialization and stored schema/index refusals pass. `recovery/recovery.json` records real restart, quiesced backup and restore into a new volume with matching store, baseline and receipt identities. | Pass for the declared private Docker sandbox. |

REQ-HAG-001 is covered by SC-01/02; REQ-HAG-002 by SC-02/05/10; REQ-HAG-003 by SC-03/04; REQ-HAG-004 by SC-05/06; REQ-HAG-005 by SC-07/08; REQ-HAG-006 by SC-04/09; REQ-HAG-007 by SC-03/06/11; REQ-HAG-008 by SC-10/12. WO-HAG-007's three supporting files are covered by the full suite and preserved [correction assessment](../../WO-HAG-007/correction-assessment.json).

The synthetic pending-decision fixture does not invent a human decision. It introduces separate synthetic active work, retains the exact decision predicate and compares the installed service handler to the independent evaluator. The missing-evidence variant reports `binding_unavailable`; it does not reinterpret missing input as a pass. The original imported fixture stays unchanged.

## Checks and measurements

- Source runner: 1,319 tests, 23 reported skips, exit 0. Skips remain unperformed coverage.
- Installed service runtime: seven tests, exit 0, including the saved-response and oversized-refusal regressions.
- Wire schemas and canonical fixtures: 60 checks pass.
- Distribution checks: 23 records pass. CLI smoke passes.
- Released validation before evidence retention: 1,970 artifacts, zero errors, 63 existing warnings. Warnings are not risk acceptance.
- Walkthrough command durations are retained individually in `walkthrough/*-result.json`; their sum is 89.795 seconds. Model reasoning and approval-review time are excluded.
- Restart: 4.746 seconds. Restore: 6.117 seconds. The acknowledged cutoff is project version 11; exact baseline/receipt identities and logical-store digest are in `recovery/recovery.json`.

The backup is 123832320 bytes, SHA-256 `3e3dbedb913d3e4492e5a9247251633544d10531144fc385298aa60f51de57bb`, retained at `C:\Users\mathi\Documents\Codex\2026-09-20\verity-plane-plugin-verity-plane-se\work\hag-bounded-20261006\recovery\graph-data.tar`. It is excluded from Git. The exact packages, build records and configuration remain at `C:\Users\mathi\Documents\Codex\2026-09-20\verity-plane-plugin-verity-plane-se\work\hag-bounded-20261006`. Images remain in the local Docker store under their immutable identities. The report includes no production RPO, RTO or power-loss guarantee.

## Corrections and preserved failures

1. Candidate `9e0199480a40e7cd207c9f682bb17d66bf977513` added explicit saved-response guidance. Claude still misreported an unread large response after shell helper commands were refused. Its second restricted probe made no MCP call. `guidance-only/` retains both outcomes; neither is a pass. That helper was not executed. Its original saved-file shape assumption and an analysis decoding error are retained as analysis failures.
2. Candidate `b55d096a510a5517addd69f504922438bf03b1e0` changed commas in MCP text from spaces to line breaks. JSON values and byte count stay the same. The regression fails on the prior image and passes with the correction. Claude reads the saved result with its ordinary bounded file tool and correctly reports partial coverage; Codex does likewise. `readable/` retains those actual sessions and the 52 boundary observations. No helper shell permission was needed to read that result.
3. Review of those observations found a separate client defect. A malformed draft returned a 3,384,949-byte refusal containing 1,909 unrelated valid records. Replaying that actual response through the unchanged installed client produced `outcome=unknown`. The final candidate keeps all released parser errors and omits the unusable catalog only when parsing fails. Its regression proves large successful catalogs still retain their content. Final live CLI probes now show the specific `HAG_REMOTE_INVALID_DRAFT` refusal for both malformed TOML and duplicate metadata. The original failed replay and regression remain under `readable/`.
4. The final schema test first could not start because Docker's address pools were exhausted. Two completed task-owned environments were taken down without deleting named volumes, images or evidence. The exact volume readbacks match. The unstarted probe was then run successfully; the failed command and scoped recovery remain in this archive.

Earlier [Claude](../claude-20261006/report.md), [Codex](../codex-20261006/report.md) and [Phase 2](../phase2-20261005/protocol04-assessment.md) reports retain their identities and failures. The early equal-key race once returned unknown results with no effects; its exact cause was not isolated. Later actual races, including this final run, pass. No causal fix or general reliability guarantee is inferred from those passes. Historical VREC-HAG-001/002/003 and their bound evidence are unchanged.

## Review and limits

Review traced admission through `Service.command`, isolated released parsing/evaluation, guarded `Store.commit`, and one shared `read` handler for HTTP/MCP. Revision content, declared edges, draft head, version and receipt commit together. Read transactions roll back. Source/evidence resolution checks contained regular files and original byte identities; imported prose is never executed. Default logs exclude document bodies and credentials. The latest corrections reuse these paths and add no second lifecycle policy or general response framework.

The project-wide guard and complete materialization are deliberate simple choices. They produce conservative conflicts and measurable per-command cost. The retained command timings expose that cost; this result makes no production performance claim.

Claude's candidate plugin was loaded for the test session. Codex explicitly read the exact candidate guidance under its normal profile and automatic approval reviewer. **Automatic Codex candidate-plugin installation/loading, startup/compaction and desktop behavior were not exercised.** The walkthrough is guided execution of an inspected launcher, not unscripted authoring. Controlled response-loss and changed-dependency variants use the retained test drivers on the same tuple; the final installed CLI separately confirms lookup and retry after recovery. These boundaries do not borrow any earlier release waiver. Native model prose is not the test oracle; actual commands, assertions and exact responses govern this assessment. Claude's walkthrough summary still mislabels a context read as creation, a simple Cypher read as cryptographic verification, and an identical accepted retry as retrying with current state. Those claims are unsupported by the actual commands and are not adopted here. Its MCP summary also miscounts the impact and lineage artifacts. The exact responses contain 123 impact artifacts and 377 relations, and five lineage artifacts and eight relations. Both native comparisons use these actual responses; the report does not adopt the incorrect prose counts. The exact duration is computed from retained results above, not its approximate total. Successful sessions do not guarantee future model behavior or authentication lifetime.

RISK-HAG-001 remains **raised**, not accepted or closed. Application restrictions and a private loopback sandbox do not establish Memgraph-enforced read-only authorization. Authenticated human lifecycle decisions, hosted authority cutover, untrusted-network exposure, production deployment, multi-tenancy, power-loss recovery, HA, migrations and public release remain outside Phase 2.

## Review handoff

Use the released evaluator to record eligible implementation completion and prepare one commit-bound verification record for WO-HAG-001 and WO-HAG-007 under VER-HAG-001. Publish that ready record and this assessment in existing draft PR #535, preserving target `codex/hosted-artifact-graph-inputs` and original comparison base `be1812e7042081014cc7682da8b9cd3822d9071f`. Only the accountable human can accept verification. This report supplies no merge, release, risk-acceptance or deployment decision.

[continuation.json](continuation.json) retains exact local selections. Obtain fresh evaluator context before continuing; do not replay completed transitions from this report. All earlier packet bytes were saved in the archive before any supported handoff rebind.
