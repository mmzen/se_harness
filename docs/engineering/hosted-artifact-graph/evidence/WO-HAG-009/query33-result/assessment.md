# Claude correction and full hosted lifecycle assessment

The instruction correction is implemented. The focused graph-read diagnostic
passed, but **Claude is not yet qualified for the complete workflow**. The full
run exercised the service successfully and produced reproducible exports. It
also exposed procedure and reporting failures that prevent a full pass.

The PR remains draft. WO-HAG-009/010/011 remain in progress. No actual verification
decision, merge, release or switch from Git authority is recorded here.

## What changed

- Direct task links now lead from hosted setup to drafting, lifecycle, reads and
  evidence guidance. The read guide links directly to reporting guidance.
- The public Cypher reference explains named relationship variables and optional
  return aliases. A refused anonymous relationship does not mean relationships
  are unsupported.
- Reporting guidance distinguishes exact operation outcomes, receipt lookup from
  retry, supported behavior from observed behavior, and tool errors from service
  refusals.
- The completed full run exposed a separate reader defect: export directories
  ending in `.json` were opened as files. The summary and replay readers now skip
  ordinary directories while retaining nested records and existing file checks.
  See the [reader correction and validation](reader-fix.md).

These are instruction and qualification-reader corrections. No service runtime,
wire schema, evaluator rule, permission, dependency or acceptance criterion changed.
Performance improvements remain outside this continuation.

## Exact versions and evidence

| Identity | Value |
| --- | --- |
| Native qualification candidate C | `4ce5bfb56d5fc594380deec56c20f1696961a621` |
| Subsequent reader correction | `88a65a5768f8e3ce1c5b8d594c4d5308b4d8ca5d` |
| Native host | Claude Code `2.1.273`, `claude-opus-4-6`, Windows |
| Candidate components | Installed client `0.22.2`, session-local plugin `0.2.7`, image `harness-hag:native-query33` |
| Governor | Released evaluator `0.22.1` in its separate environment |
| Evaluator archive SHA-256 | `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |
| Source fixture S | `5820415917e87b64d80bad2f7c39c6d18d692829` |
| Full run test candidate P | `55e3e9998bf8eb02c0ee68097aef6138e1030adb` |

Two pinned builds matched exactly. Both packaged plugins contain the corrected
guidance, and the packaged public contract matches its exact Git blob. All 27
service wheel members and the evaluator/runtime/database/schema/protocol/dependency
inputs match the previously qualified service. This supports explicit service
evidence reuse; it does not claim identical image/archive identities or newly run
restart/restore tests. Exact digests and comparisons are in
[provenance.zip](provenance.zip), with [its inventory](provenance-inventory.json).

The reader correction was made after the native runs. Its offline checks do not
rewrite their candidate identity, inputs, reports or verdicts.

## Observed runs

| Run | Duration | Calls | Reported peak input context | Result |
| --- | ---: | ---: | ---: | --- |
| `claude-281`, focused discovery/read/report diagnostic | 308.899 seconds | 32 | 146,267 | Bounded diagnostic passed; no complete lifecycle claim |
| `claude-282`, fresh full lifecycle | 2,714.143 seconds (45m14s) | 196 | 203,475 | Service operations replay; native qualification incomplete |

These are observed measurements, not a performance improvement claim. The full
run contains 32 tool errors, including expected refusals and seven host permission
denials. It completed within the 3,600-second limit and exited zero. Exit zero is
not the qualification verdict.

The focused run read the setup, read, public Cypher and evidence guidance. All
seven MCP responses matched HTTP exactly. A named `DECLARES` relationship query
returned the three real work-order links. Its report no longer claimed that
relationships were unsupported or aliases mandatory. The remaining source-link
omission is retained in its assessment; this bounded pass does not waive NQ-01/05.

## Full-run assessment against VER-HAG-007

| Case | Observed result | Remaining gap |
| --- | --- | --- |
| NQ-01 — Instructions/context | Initial drafting, lifecycle and evidence routes were read; evaluator identity and test selection were correct | Required before-action sections and later decision, verification, release and reporting procedures were not read. The read guide was not read in this full run. Required context was not reliably recovered after compaction |
| NQ-02 — Agent-driven lifecycle | Exact greeting assertion passed. Ten accepted operations reached test work completion, verified VREC and released RLS. All ten match independent released replay | Handoff used a later comparison base, omitting earlier changes to seven formal files. REL was approved before the final candidate was known, contrary to the selected drafting procedure |
| NQ-03 — Refusals/reads | Out-of-scope handoff and stale-preview refusal occurred; corrected handoff succeeded. Six full-run MCP results match HTTP exactly, with complete responses and no unresolved references | No full-run `revision` MCP call exists, despite the report claiming all seven. The separate focused run supplies seven-tool observations, not a correction to this false claim |
| NQ-04 — Unknown reply/retry | Lost approval reply was recovered by original-key lookup. Identical resubmission returned the identical receipt/version. Changed content under that key conflicted | The final report incorrectly says the identical retry was refused with `HAG_REMOTE_KEY_REUSE` |
| NQ-05 — Exports/report | Four export copies represent two distinct earlier/later baselines. Independent reconstruction checked exact bytes, Git objects and original P binding in VREC/RLS | Final reporting has wrong operation references, a false seventh-tool claim, the wrong retry result, a mislabeled baseline, and missing separate S/C identities |

The service mechanics are reproducible. The complete native claim is not. No
real checkout or monitored host-setting change occurred during either session;
the staged input hashes are unchanged. Both projects' containers are stopped and
their volumes preserved. The sessions received no procedural hints, corrective
commands, operator graph mutations or supplied workflow sequence.

## Material findings and exact corrections to the report

1. **Handoff comparison.** The first accepted input head was
   `000d0a187231a2d0ce8238ddc07acd8c2180b6e1`. Claude used
   `aab791b52c36692ea5a30a7a6c562205f49bb884`, the later start-output head.
   An independent Git diff confirms that this omits earlier changes to INT, CAP,
   REQ, SPEC, VER, REL and WO. A replay of the same arguments cannot establish
   complete scope when the selected comparison base is wrong.
2. **Retry outcome.** Records `021-lookup-approve` and `022-retry-approve` are
   identical accepted results, receipt
   `sha256:460adc206cb3a5b4e25d10683a987c4ccb3098d1bbb7441ad4f54465400e5006`.
   The project version remains the receipt's 16→17 transition. Only the changed
   request in `023-changed-key` returns `HAG_REMOTE_KEY_REUSE`.
3. **Tool coverage.** Actual full-run MCP calls are `cypher`, `check`,
   `work-context`, `lineage`, `impact` and `compare`. No `revision` call was made.
4. **Record references.** Handoff apply is `041`, completion `043`, VREC capture
   `045`, verification `047`, release preparation `049`, and release `051`.
   The native report's lifecycle table shifts these references to other actions.
5. **Baseline identity.** Actual import B is
   `se-harness-artifact-baseline/v1:sha256:1f1c92e8b4b03589d4ed632fda03723862179ba6ca2dc5f5678b32aa5210367d`.
   The exported earlier baseline ending `325fafc0...587140` is the result of the
   mitigation decision, not the import. The later baseline is
   `se-harness-artifact-baseline/v1:sha256:a60a6880a33d6017876b92a8174ce8c2523ef57a1a146f94f1a1d3752aa828a0`.
6. **Reader failure.** The original `observations` command cannot enumerate
   JSON-named directories. Claude attempted denied shell cleanup and then
   re-exported into new directories; the original directories stayed intact.
   Its manual observations remain original agent assertions, not independent facts.
   The subsequent reader fix is covered by regression and actual replay checks.

All original native reports remain unchanged. `assessment/claim-audit.json` in
the full-run archive retains exact comparisons and omitted paths. Offline observer
recovery is explicit: a temporary directory guard enabled review of the failed
original reader; the committed correction later reproduced that summary. A long
observer path caused Windows Git to reject one replay, which then passed in a
shorter new directory. These are reviewer actions after the native run.

## Checks and delivery boundary

The final reader correction passes 41 focused tests; 1,337 source-suite tests with
24 reported skips; distribution and CLI smoke checks; and released validation of
1,991 artifacts with zero errors and 63 warnings. Scope and review preflight pass.
The earlier candidate's package checks and exact builds are preserved separately.
See [reader checks](reader-checks.zip) and [report checks](report-checks.zip).

At remote head `99442cdb28b7b7d1804bab7e6b13fe994508cad7`, CI's `validate` job
failed solely on WO-HAG-009 `QGP-G4I-EVIDENCE`: final handoff evidence is not yet
available. Other completed checks passed; three conditional release-rehearsal
jobs were skipped. This is an unfinished-work draft, not a merge-ready result.

The retained released context leaves the work orders `in_progress`, with
`STEP-WO-IMPLEMENT-CHECK` under `PROC-WO-IMPLEMENT`. The next work is to resolve
the remaining native procedure/reporting findings and rerun the affected cases
before recording final handoff evidence. Do not replace the failed native claims
with the passing service replay. Earlier Codex qualification remains bound to its
own candidate; it is not silently extended to these changed instructions.

## Reviewable evidence

- [Focused visible transcript](claude-281-visible.md),
  [archive](claude-281-evidence.zip), [inventory](claude-281-inventory.json).
- [Full visible transcript](claude-282-visible.md),
  [archive](claude-282-evidence.zip), [inventory](claude-282-inventory.json).
- [Build/setup provenance](provenance.zip), [inventory](provenance-inventory.json).
- [Reader correction](reader-fix.md), [checks](reader-checks.zip),
  [inventory](reader-inventory.json).

Archives include actual requests/results, selected inputs, read traces,
independent HTTP comparisons, replay commands, exports and assessments. They omit
credentials, private reasoning, raw host/system events and account stores. Exact
known test tokens were checked absent. Original protected evidence bytes and the
earlier candidate reports remain preserved.
