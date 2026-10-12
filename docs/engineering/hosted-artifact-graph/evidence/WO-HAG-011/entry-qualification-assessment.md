# Focused drafting entry: qualification remains incomplete

The instruction and test-driver correction is implemented. Two of the three
positive Claude drafts passed independent content review. The third failed the
required concrete evidence-retention plan. All three missed every efficiency
goal. Codex qualification remains pending because its ordinary shell cannot start.
No verification record was prepared. WO-HAG-011 remains `in_progress`.

Tested candidate: `de65c510021b229519dfce04667704808f0f4fe5`. Governor: separately installed released 0.22.1.
Disposable client: 0.22.2. Candidate plugin: 0.2.7. Claude Code: 2.1.273,
model `claude-opus-4-6`. The installed host plugin and all permissions are unchanged.
Git remains authoritative. This report records tests, not human verification.

## What changed

- The native driver can supply operator-selected canonical sections and exact
  source-manifest pointers in its opening context. It reuses the existing section
  reader and checks source identities. It supplies no finished artifact or
  operation sequence. The selected text and its digests are retained.
- The plugin routes verification drafting to its applicable procedure and tells
  the agent to reuse already-delivered sections. Known artifact pointers replace
  broad inventory discovery; their presence is not a content read.
- The command reference separates draft mutations from revision reads. Read
  syntax explicitly excludes mutation-only arguments. Fixture execution has a
  separate reference, with its own task trigger.
- Native prompts use stdin to avoid Windows command-line size limits. A focused
  regression preserves exact UTF-8 and mixed line endings on that route.

The opening entry is **explicit qualification support**, not evidence of
automatic startup delivery, desktop behavior or compaction. No released resource,
service, schema, evaluator policy, dependency, approved definition or lifecycle
history changed in this correction.

## Native observations

| Trial | Case | Seconds | Native calls | Peak input tokens | Content review |
| --- | --- | ---: | ---: | ---: | --- |
| [claude-21](claude-21-visible.md) | Missing-input diagnostic | 276.799 | 20 | 66,183 | fail |
| [claude-22](claude-22-visible.md) | Positive 1 | 318.857 | 25 | 70,333 | pass |
| [claude-23](claude-23-visible.md) | Positive 2 | 289.164 | 23 | 65,496 | pass |
| [claude-24](claude-24-visible.md) | Positive 3 | 343.415 | 23 | 68,999 | fail |
| Codex | Both required cases | unavailable | unavailable | unavailable | pending host recovery |

For the three comparable positive attempts, the median was
**318.857 seconds, 23 calls and
68,999 peak tokens**. The ranges were
289.164–343.415 seconds,
23–25 calls and
65,496–70,333 tokens.
These include every completed attempt, including the failed third draft.
The goals remain below 180 seconds, at most 15 calls and below 40,000 peak tokens.
Three observations on one host are not a general benchmark.

The earlier positive trial, [claude-12](claude-12-visible.md), took 328.952 seconds,
31 calls and 63,615 peak tokens, and failed its plan-only boundary. This correction
removes that observed execution error and reduces calls in these trials, but
does not establish a useful speed improvement; context grew. Opus10 remains a
different intent task and is not a same-task positive-performance comparison.

## Content findings

`claude-22` and `claude-23` produce usable verification drafts: the correct
requirement link, independently derived expected string, a complete matrix,
specified check/pass condition and a concrete retained-evidence file. Neither
executes the fixture or changes lifecycle state. `claude-24` preserves those
boundaries but leaves the destination as `docs/engineering/lifecycle-pilot/evidence/`
“under the governing work order directory.” It identifies neither the work order
nor the evidence file. That fails the approved concrete-retention criterion even
though draft admission reports zero incomplete fields.

Missing-input diagnostic: **fail**.
The saved INT-P3-001 acknowledges imported INT-P3-900, but its success measure repeats the greeting acceptance check and says that inspecting or testing the fixture measures the operational outcome. It does not report the missing agreed operational success measure. The native report explicitly calls this complete and denies that the measure is an acceptance test. This fails EFF-04A even though the service admits the draft.

All actual failures and refusals remain in the trial evidence. Each accepted
draft was separately read from the service and compared with the submitted bytes.
Where a baseline was imported, all seven imported records were also read
independently and compared with their original Git-blob bytes. Native in-progress
observation snapshots are preserved; the completed independent captures supply
the final numbers above. Minor report-path/snapshot limitations remain in each
independent assessment; native reports were not rewritten to conceal them.

## Why the cost remains high

| Trial | Initial input tokens | Initial canonical instruction bytes | Reads of already-supplied task.md | Repeated prompt-file bytes | Entry preparation seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-21 | 23,415 | 21,262 | 1 | 30,628 | 0.264 |
| claude-22 | 23,105 | 20,069 | 1 | 29,769 | 0.234 |
| claude-23 | 23,110 | 20,069 | 1 | 29,769 | 0.253 |
| claude-24 | 23,112 | 20,069 | 1 | 29,769 | 0.250 |

The complete prompt was already sent on stdin, yet every positive trial read
`task.md` again. That repeats the opening entry and task with native line
rendering. File sizes above describe source bytes, not provider token counts.
The task also asks the agent to write both a narrative report and structured
observations even though commands and observations are already captured. These
outputs add work and repeat evidence. Exact paths, calls and measured command
times are retained in `entry-native-metrics.json` inside the checks archive.
Provider/model time is unclassified; the evidence does not justify attributing
all elapsed time to a particular read or instruction.

## Checks and component identity

- Source suite: 1,335 tests, 24 skips, exit 0. Distribution validation and CLI
  smoke passed. The final stdin-only correction reran the affected native-driver
  suite: 22 tests passed. It changes no production/runtime source, so the broader
  unchanged-source checks were retained rather than repeated.
- Both candidate package builds were reproduced twice with matching bytes.
  The earlier `474bb8a7465664987e33de05390f6c57be662f00` build is preserved as
  pre-qualification preparation; it ran no native trial. The final candidate
  above includes the line-ending correction and supplies all trials here.
- Nine opening instruction sections matched their exact released source. Seven
  artifact pointers matched the source manifest. The ambiguous selector was
  refused. Both packaged plugin variants match their candidate Git-blob guidance.
  Unit boundaries retain changed/mismatched/escaping input refusals.
- Runtime and dependency paths `se_harness/`, `server/`, `release/` and
  `pyproject.toml` match candidate `456c84a7dcb3a11cd564899da01848f39dc53575`.
  Earlier EFF-02/03 installed-client and service checks are reused only for those
  unchanged bytes. New guidance and driver behavior use the new observations.
- Released validation: 1,991 artifacts, zero errors, 63 existing warnings. Scope
  and review preflight passed before the trials. Final publication checks have
  their own retained archive.

Preparation is outside each native wall clock. Entry-assembly time is listed
above; reproducible-build/package/environment timestamp spans are retained in
the metrics file, separately from native time. Their recorded span excludes the
subsequent pip install and is not presented as a monotonic build duration.
All trial containers were stopped by exact owned names; volumes remain available.
Two transient closeout-script errors happened before any stop. Their inspections,
rechecks and correction are disclosed in the checks archive; they are not native
failures and did not change the candidate.

## Codex blocker

An authenticated Codex CLI 0.162.0-alpha.2 session attempted one ordinary shell
read. It failed before executing the command: `helper_unknown_error: setup refresh
had errors`. The host sandbox log identifies OS error 32 while opening the ACL
target for `node_repl.exe`: another process holds the file. Resetting this chat's
computer-use kernel did not clear the lock. Other live helpers were not stopped,
and permissions were not changed. A host repair is required before a normal
Codex qualification run; no failed or omitted check is accepted here.

## Simplicity review and next correction

The correction reuses existing readers, manifests, command capture and ordinary
files. It introduces no workflow engine, policy copy, dependency, retry layer or
new approval. The extra driver code is limited to preparing an exact opening
view and its provenance. However, duplicating that view through the task file
defeats its context benefit, and verbose output requirements remain costly.

The next in-scope correction should remove that duplicate delivery path and
stop asking the agent to rewrite machine observations. Keep one short authored
content assessment with links to captured evidence. Make the existing content
review check whether an executor can locate the planned evidence without choosing
an unnamed work order or file. Do not supply a completed contract, lower the
retention criterion or silently edit this candidate's results. Shortening canonical
released instructions themselves is a separate scope decision.

WO-HAG-011 remains `in_progress`; required assurance is unchanged. The released
continuation remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, with bound
`check REPO --artifact WO-HAG-011 --checkpoint handoff`, using the selected
0.22.1 evaluator and absolute checkout. Remaining test findings and unavailable
host access must be resolved before completion/verification preparation.
WO-HAG-009/010 full NQ qualification is also incomplete. PR #543 remains draft
with its existing complete comparison base and declared work-order set.

## Evidence

- [Checks and component review](candidate08-checks.zip), [exact inventory](candidate08-checks-inventory.json).
- [Final publication checks](candidate08-publication-checks.zip).
- Each trial above links its visible transcript. Its matching `claude-NN-evidence.zip`
  and `claude-NN-inventory.json` retain inputs, commands, results, independent
  readback and assessments. Private reasoning, credentials and raw provider streams
  are excluded; their retained private-event digests identify the originals.
