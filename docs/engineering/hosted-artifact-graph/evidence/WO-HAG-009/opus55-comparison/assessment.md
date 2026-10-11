# Same diagnostic with Claude Opus 5.5

**Opus 5.5 made more progress and reported its limits clearly, but the diagnostic
still did not pass.** It stopped on a real handoff refusal after 13 minutes
56 seconds. Its peak input context was almost twice that of the prior run.

Candidate: `c526fcbe7ac59de9fd45cb8ae461cfb558aaf2b7`. Both runs used the same task,
candidate client, plugin, service, fixture, permissions and 20-minute limit.
PR #543 remains draft. This is a model comparison, not full qualification.

## Comparison

| Observation | Opus 4.6 (Claude311) | Opus 5.5 (Claude321) |
| --- | --- | --- |
| Claude Code | 2.1.273 | Isolated, pinned 2.1.280 |
| Elapsed native session | 20:00, timed out | 13:56, stopped with a blocker |
| Tool calls | 101 | 112 |
| Failed tool items, including negative probes | 14 | 8 |
| Peak input context | 166,173 tokens | 315,053 tokens |
| Accepted lifecycle operations | 1: combined approval | 3: definitions approved, WO approved, WO started |
| Independent replay | 1 passed | All 3 passed |
| Greeting assertion | Not run | Passed, but differs from authored VER |
| Cypher / independent HTTP | 1 exact match | 2 exact matches |
| Valid handoff | Not reached | Reached and refused |
| Changed-draft stale-preview test | Stale-context guard reached | Not performed |
| Final report files | Absent at timeout | Both written, with incomplete outcome disclosed |

These are two incomplete runs with different stopping points. The shorter
session is not a measured completion-time speedup. Peak context is the maximum
provider-reported input, cache-creation and cache-read token sum for a message;
it is not billed token total. The same summarizer was used for both runs.
The 8 errors comprise 5 lookup/argument/selection failures and 3 handoff refusals.
The native report's 109-call figure is explicitly an earlier snapshot; the final
independent count includes 3 subsequent calls.

## What improved

Opus 5.5 read all six artifact-type checklists, the approval-package assessment,
decision rights, work-approval authority, execution steps and RESULTS. Those
reads were absent or incomplete in Claude311. It used `approved` correctly on
the first transition previews. The three accepted operations replayed with the
same states, gates and file effects through the separately installed released
evaluator 0.22.1.

The requirement and verification plan both call for a test. The agent executed
the permitted greeting assertion and kept its actual result. It did not claim
a successful handoff, invent a stale-preview result, change the comparison base
to omit scope findings or expand the approved scope. It wrote both required
reports and retained the failed attempts.

## What still failed

1. **Work-order scope.** The authored WO allows only the assertion evidence
   file. Handoff compares the complete change from the retained pre-approval
   base, which also includes definition approval writes. Released evaluation
   refused `QGP-G4I-PATHS` with `WEX201`, first naming
   `docs/engineering/lifecycle-pilot/capabilities/CAP-P3-001.md`. The native
   agent correctly stopped and identified the omitted scope.
2. **Verification plan versus available execution.** The VER specifies Linux,
   Python 3.13.16, a type assertion and candidate-bound evidence. The permitted
   helper runs the equality assertion on the staged source in local Windows
   Python. The agent disclosed these differences, but disclosure does not
   satisfy its accepted test contract. Content review remains unsuccessful.
3. **Negative-test selection and order.** Both proposed out-of-scope files
   triggered `HAG_REMOTE_PROTECTED_FIELD` before the intended evaluator gate.
   The ordinary handoff separately exposed the real scope omission. No
   changed-draft stale-preview demonstration was performed. This omission
   does not prove that the service cannot support that demonstration.
4. **Lookup and argument recovery.** A nonexistent help path, nonexistent WO,
   invalid JSON pointer and two instruction-reader path attempts caused
   retries. A newer model did not eliminate the discovery/interface problems.
5. **Report identity precision.** The report records the exact qualification
   candidate, then labels implementation candidate C unknown elsewhere. The
   independent assessment retains the actual C above. No test VREC candidate
   P was captured.

After all three refusals, independent receipt lookups returned 404 for their
original keys. Final project version remained 17, the version after start;
WO-P3-001 remained `in_progress`. Both actual Cypher reads returned complete
results with no unresolved references and matched independent HTTP exactly.

## Environment and comparison limits

The user requested Opus 5.5. A no-tools request from CLI 2.1.273 was refused
before inference because the model requires CLI 2.1.280 or newer. The isolated
2.1.280 executable came from Anthropic's official download, matched its published
SHA-256 and had a valid Anthropic Authenticode signature. Its live request and
native session both reported `claude-opus-5-5`; no model fallback occurred.

The user separately authorized `claude update`. That updated the host CLI from
2.1.273 to 2.1.296 before the test. The comparison deliberately used the already
verified isolated 2.1.280 executable. No host app restart or global permission
change was needed. Thus model and required CLI version differ from Claude311;
a single run cannot isolate their effects. Neither run supplies an effort
override, and provider/model defaults need not be identical.

Task and permissions match after normalizing the disposable directory. All
118 content files match byte-for-byte; only configuration.json and combination.json
differ for the new project/deployment identity. The wheel, plugin 0.2.7, service
image and source remain candidate C above. The later Git head 82fc1ca contains
only evidence changes. Existing candidate build/source qualification is reused
from [the prior assessment](../procedure36-result/assessment.md), not rerun.

All 120 staged files were unchanged after execution. All 26 observed native
Write/Edit requests and 30 command captures stayed under work/. The monitored
repository and host settings were unchanged across the run. This is an observed
boundary check, not a claim of OS-enforced isolation for every possible write.
No native hints, answers, corrective commands or operator service mutations
were supplied after setup. The exact test containers were stopped after replay;
their volumes remain preserved.

## Assessment and next step

The model comparison supports using Opus 5.5 for further diagnostics, but does
not justify treating the workflow as qualified or the context problem as fixed.
The next corrections still need to align authored scope with the complete
change, align the verification plan with available execution, and select/order
the negative tests correctly. Keep instruction and service findings separate;
this report introduces no policy, permission or runtime change.

WO-HAG-009/010/011 remain in progress. The released next step is
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. Formal qualification criteria
remain unchanged; this diagnostic replaces no required Opus 4.6 or paired-host
case. No actual VREC, verification, merge or release decision is made.

Before this evidence update, all applicable technical checks on 82fc1ca passed;
three conditional rehearsals were skipped. The harness validate check remained
failed for unfinished qualification (`QGP-G4I-EVIDENCE`). The draft PR keeps
that blocker disclosed and preserves its complete comparison base.

## Evidence

- [Visible native transcript](claude-321-visible.md).
- [Native evidence inventory](claude-321-inventory.json) and
  [archive](claude-321-evidence.zip): exact requests, results, inputs, reports,
  independent replay, instruction trace, refusal and boundary checks.
- [Provenance inventory](provenance-inventory.json) and
  [archive](provenance.zip): comparison proof, exact drivers, CLI identity and
  prior-package equality records.
- Report scope, preflight and validation results are retained in
  report-checks.zip and report-checks-inventory.json after the checks run.

Private reasoning, raw provider/account logs, credentials and executable
binaries are excluded. Earlier evidence and failures remain unchanged.
