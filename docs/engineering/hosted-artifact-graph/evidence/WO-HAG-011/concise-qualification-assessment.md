# Single task delivery: qualification assessment

WO-HAG-011 remains **in progress**. Candidate `fbf29c98e02895e6c980c81a48f697f7cded0e94` removes duplicate
task delivery and the separate model-written observations file. 2 of three
positive Claude drafts pass independent content review. The missing-input
diagnostic still fails. Both Codex cases remain pending because the host cannot
start an ordinary shell command. No verification record or acceptance is claimed.

## Results

| Trial | Case | Seconds | Calls | Peak input tokens | Content review |
| --- | --- | ---: | ---: | ---: | --- |
| claude-31 | Missing input | 224.905 | 17 | 52,823 | fail |
| claude-32 | Positive | 194.375 | 19 | 53,476 | pass |
| claude-33 | Positive | 209.797 | 23 | 57,672 | pass |
| claude-34 | Positive | 216.707 | 22 | 56,820 | fail |

Positive goals remain **under 180 seconds**, **at most 15 calls**, and **under
40,000 peak input tokens**. See each exact goal result in
`concise-native-metrics.json` inside [candidate checks](candidate09-checks.zip).
Costs and content correctness are separate; a faster incorrect draft is a failure.

Compared with the three positive attempts on candidate `de65c510`:

| Measurement | Previous median | Current median | Observed change |
| --- | ---: | ---: | --- |
| Duration (seconds) | 318.857 | 209.797 | 34.2% lower |
| Tool calls | 23 | 22 | 4.3% lower |
| Peak input tokens | 68,999 | 56,820 | 17.7% lower |

The requested outcome, fixture, model and permission boundary are unchanged.
Delivery and report instructions changed deliberately. These are three attempts,
not a general latency benchmark or a controlled attribution of every saving.
The negative case is not a successful-authoring performance comparison.

## What changed

- Startup now sends a short file pointer. The task file holds the complete
  canonical sections and requested outcome. Previously that content arrived
  on stdin and was then read again from the file. Compaction keeps the same pointer.
- One durable focused-task template replaces the old request for both a written
  report and a model-written observations JSON. One content report also serves
  as the transient progress note; machine capture supplies metrics and failures.
- Hosted drafting guidance asks for a source for claimed outcomes and measures,
  and a usable evidence destination. It supplies no finished draft or expected
  diagnostic answer. The negative result shows the limits of that guidance.

No service, evaluator policy, dependency, installed host plugin or permission
configuration changed. The candidate plugin is 0.2.7 and client is 0.22.2;
the governing released evaluator remains 0.22.1 outside the checkout.

## Delivery and remaining cost

| Trial | Initial pointer bytes | Task file bytes | Task reads | Duplicate task bytes | Initial host context tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-31 | 440 | 31,103 | 1 | 0 | 15,669 |
| claude-32 | 440 | 30,245 | 1 | 0 | 15,678 |
| claude-33 | 440 | 30,245 | 1 | 0 | 15,669 |
| claude-34 | 440 | 30,245 | 1 | 0 | 15,669 |

The selected nine canonical sections remain exact, with source identity and
seven artifact pointers. Pointers do not establish reading or comprehension.
This tests explicit delivery, not automatic startup, desktop or compaction.
Source byte counts are not provider token counts.

The capture still shows separate selection, skill/reference, tool-index,
component-identity and fixture reads before the chosen service operations.
Full captures identify their purpose and count. Some report prose still repeats
operation information, although the separate observations JSON is gone.
Removing duplicate delivery helps; it does not solve content judgement or make
the current route meet every efficiency goal. Adding another layer of repetitive
instructions is not supported by these observations.

## Independent content review

### claude-31

- The saved Problem claims no current definition establishes the greeting value or verification path, despite the imported REQ-P3-900 and VER-P3-900. The native run did not read those records before this absence claim.
- The success measure substitutes existence of an accepted definition, which the request did not specify as the operational outcome. The final response calls the intent complete instead of reporting the missing agreed operational success measure.

Document SHA-256: `fa4f2f7e9c2aba54e75a63ca95df725f50491c2d85d55f421a0b42fa6945009a`.

[Visible calls and replies](claude-31-visible.md), [retained evidence](claude-31-evidence.zip), [inventory](claude-31-inventory.json).

### claude-32

- Draft VER-P3-901 verifies REQ-P3-900. Its matrix identifies a test, independent expected string, operation and exact pass condition.
- The plan names the concrete future destination docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-result.json and the retained pass/fail plus returned value.
- The document has no empty optional headings. The report explicitly says no test ran and no lifecycle decision occurred.

Document SHA-256: `c5861c4d65191143c00f1bd1a561ea648c5256dd3e0e5424fea567ad287bc8fc`.

[Visible calls and replies](claude-32-visible.md), [retained evidence](claude-32-evidence.zip), [inventory](claude-32-inventory.json).

### claude-33

- Draft VER-P3-901 links REQ-P3-900 and derives the expected string from its acceptance criterion. Matrix and import/call/equality steps define a usable planned check.
- The plan names docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-assertion.json and specifies actual/expected values, outcome, Python version and timestamp.
- Inapplicable optional headings are removed. The report distinguishes the planned test from execution and makes no verification claim.

Document SHA-256: `7a6d46fc83f5b2f037c32cc6164d168f4b4320f0a2a1180af97d71458ab81579`.

[Visible calls and replies](claude-33-visible.md), [retained evidence](claude-33-evidence.zip), [inventory](claude-33-inventory.json).

### claude-34

- The draft links REQ-P3-900, derives the expected value independently, defines an import/call/equality check, and distinguishes planned from executed tests.
- Evidence retention names only docs/engineering/lifecycle-pilot/evidence/ under the executing work order's directory. Neither the work order nor a filename is selected; a later executor still has to choose them. The concrete-retention criterion fails despite zero admission errors/incomplete fields.
- One create request was refused with HAG_REMOTE_UNKNOWN_IDENTITY (404) because the project UUID was used as the context. The agent recovered and included the failed and successful records in its report; this refusal is retained, not erased or relabeled.

Document SHA-256: `4323f1d8a694536bc2805d4e0635e78d2775f964039bcf6d4ec46c6bbeceec3e`.

[Visible calls and replies](claude-34-visible.md), [retained evidence](claude-34-evidence.zip), [inventory](claude-34-inventory.json).

For every completed trial, a separate service request matched the submitted
draft bytes. Separate reads confirmed all seven imported records were unchanged.
Staged inputs were unchanged. Actual failures and denials, including recoveries,
remain in the retained machine summaries. Source inspection and planned tests
are not recorded as executed tests. No real lifecycle decision occurred.

## Checks and identities

- Driver boundary checks: 23 tests passed, including pointer delivery and exact
  UTF-8/mixed-line-ending transport.
- Source suite: 1,335 tests, 24 skips, exit 0. Distribution and CLI smoke passed.
- Two pinned reproducible builds and disposable package preparation/install passed.
  The build-to-install-start timestamp span was
  375.901 seconds;
  it includes packaging and environment creation, excludes pip installation,
  and is separate from native wall clocks. It is not a monotonic build duration.
- Both plugin variants match candidate guidance. The selected sections preserve
  canonical bytes; the ambiguous selector still refuses. Runtime and dependency
  paths are byte-identical to `456c84a7dcb3a11cd564899da01848f39dc53575`;
  reuse of EFF-02/03 and service evidence is limited to those unchanged components.
- Claude Code 2.1.273, `claude-opus-4-6`: live probe passed. Codex CLI
  0.162.0-alpha.2: the authenticated model answered, but its single ordinary
  file read failed with `helper_unknown_error: setup refresh had errors`.
  No permission change or alternative execution route was used.
- Released validation: 1,991 artifacts, zero errors, 63 existing warnings.
  Scope and review preflight passed. The full PR still has the disclosed
  WO-HAG-009 handoff-evidence blocker; this report does not waive it.

Exact commands, exits, component identities, observations and readback are in
[candidate checks](candidate09-checks.zip) with their
[inventory](candidate09-checks-inventory.json). Native archives omit private
reasoning, raw provider streams, credentials and wheel binaries; their inventories
identify retained bytes and omissions. Earlier evidence remains unchanged.
Only this round's owned service/graph containers were stopped; volumes remain.

The transient report writer initially changed the index's line endings.
`git diff --check` refused before staging. The original bytes were restored
before the bounded index update; the [failed check and recovery](candidate09-publication-recovery.json)
are retained separately from the native results.

## Remaining work

The missing-input behavior remains incorrect. The positive set still lacks
three correct attempts because claude-34 leaves the evidence destination vague.
Both Codex cases need a working ordinary host shell, and WO-HAG-009/010 full
qualification remains incomplete.
Keep PR #543 draft. No completion, VREC, merge, release, adoption or host update
was performed. The released evaluator's next step for WO-HAG-011 remains
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`: `check REPO --artifact WO-HAG-011
--checkpoint handoff`. The current scope-only result is not handoff readiness.
