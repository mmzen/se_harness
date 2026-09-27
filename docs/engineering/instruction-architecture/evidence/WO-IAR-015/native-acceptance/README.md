# Native instruction-delivery acceptance — 2026-09-27

Selected work: WO-IAR-015. Contract: VER-IAR-014 and REQ-IAR-026.
Source candidate: `2b45556ee23aff46e2cb131ac08992dc59131709`.
The source repository remains governed by released evaluator 0.18.0. These
disposable installations exercise the non-promotable 0.19.0 candidate wheel,
SHA-256 `3b45680ee7f76509e09a933a4d061ff522d29c25b236201985861376221f5b3f`.
The wheel's source commit is `2f339039fe4f6189334fcd10632e20360cfa389f`;
its package inputs were checked unchanged through the source candidate.

## Native startup and compaction

| Host and surface | Observed evidence |
| --- | --- |
| Codex CLI `0.155.0-alpha.16.4`, Windows | The original CLI session receives the complete matching root at startup and again after manual compaction. It actually reads COMMUNICATION.md and DEFINE_CHANGE.md for the new-change explanation. See [CLI observation](codex-cli/REPORT.md). |
| Codex native app-server, same installed version | A disposable replay captures compaction completion, then matching plugin `sessionStart` start/completion notifications and the subsequent correct probe response. See [callback observation](codex-callback/REPORT.md). The notification calls the event `sessionStart`; it does not expose a `source=compact` field. The explicit compaction and event sequence establish the trigger. |
| Claude Code `2.1.273`, Windows | The original session records successful `SessionStart:startup` and `SessionStart:compact` callbacks, complete matching root delivery, actual COMMUNICATION.md and DEFINE_CHANGE.md reads, and the correct post-compaction probe. See [Claude observation](claude-cli/REPORT.md). |

The Codex root digest is
`b55a88ab900a7466b372ec32a4bc80ca47fa26a79ec0f8bc703aba58174bfaab`.
The Claude root digest is
`be7c525c4cc2e4ec91186453353d3c2889c25e1cfa5f47ab52902acce57c6fae`.
The project-name difference accounts for their different contents. Both have
the final heading `After compaction` and select 0.19.0.

## Repository switching and unavailable inputs

| Case | Expected outcome | Native observations |
| --- | --- | --- |
| Current 0.19.0 installation | Deliver its complete root and matching path/digest. | Both hosts pass. |
| Switch to an installation made by the actual released 0.18.0 evaluator | Deliver the other repository's 0.18.0 root; no cached 0.19.0 root. | Both hosts pass. |
| Return to 0.19.0 | Deliver the current repository's 0.19.0 root again. | Both hosts pass. |
| Missing ENGINEERING_HARNESS.md | Explicit missing-regular-file delivery gap; no usable root; stop the affected governed action. | Both native hooks deliver that gap. Codex also reports the gap and withholds work authority. |
| Altered root bytes | Explicit installed-digest mismatch; no altered policy delivered as valid. | Both native hooks report the mismatch. Codex also reports the gap and withholds work authority. |
| Configuration selects 0.18.0 while lock selects 0.19.0 | Explicit release-selection mismatch; no silent upgrade or cached root. | Both native hooks report the mismatch. Codex also reports the gap and withholds work authority. |

See [Codex boundary observations](codex-boundaries/observation.json)
and [Claude boundary observations](claude-boundaries/observation.json).
All fixture files remain unchanged by these native runs. Codex switches working
directories in one ephemeral conversation, with explicit compaction between
cases. Claude uses consecutive native `--init-only` startup invocations against
the same isolated profile and different working directories. This establishes
native hook selection, not a same-conversation Claude switch or model response.

The initial Claude metadata-echo attempt was rejected by its API with
`reasoning_extraction`. Its successful hook payload and API refusal are both
retained in [the original attempt](claude-probe-refusal/current.events.json).
No model was changed and no safety setting was disabled. The subsequent
`--init-only` checks assess host callbacks without requesting a model answer.
Earlier successful human-run startup/compaction probes remain separate evidence.

## Uncertain-write recovery

The fault is a withheld acknowledgement, not a simulated process crash.
The collector performs one real `raise-risk` in each disposable repository,
retains its successful result, and does not disclose that result to the native
session. The session receives the intended title, description, next action,
owner and selected WO. Exact source definitions are copied as fixture inputs;
they do not grant authority over the real source repository.

Claude reads the recovery instructions and the actual `RISK-IAR-001.md`, matches
the persisted fields and single lifecycle event, and declines to repeat the
write. Its subsequent evaluator identity command is denied by the host's tool
permissions. It preserves that blocker and explicitly declines to invent a
fresh lifecycle verdict. The fixture remains byte-identical. See
[Claude recovery observation](claude-recovery/observation.json).
The collector's original `risk_files` list is empty because it searched for
`RSK-*`; the retained native read and original-write result identify the actual
`RISK-IAR-001.md`. This collection defect does not change the observed record.

The first Codex attempt stopped at a native tool-approval request and made no
fixture changes. That incomplete attempt is retained. The follow-up collector
requires an individual review of each requested command; it grants no blanket
or persistent execution permission. Only inspected read-only commands within
the user's authorized acceptance test may be accepted. The final observation
and its command-review records establish the results of that follow-up.

In the [completed Codex recovery](codex-recovery/observation.json),
manual compaction precedes fresh instruction delivery. Codex rereads the recovery
instructions, finds the exact persisted risk, runs the selected fixture evaluator's
checkpoint-free `check`, and reads its returned implementation-evidence step.
The actual result reports WO-IAR-015 `in_progress`, no blockers, no writes, and
`STEP-WO-IMPLEMENT-CHECK`. Codex reports those fields and does not rerun risk
creation or execute the handoff command. The single risk and every measured
fixture file remain unchanged. The native trace retains the evaluator output.

## Review findings and resolutions

- The first callback collector lacked the app-server's required `excludeTurns`
  option for its ephemeral fork. Its failed attempt is retained; the corrected
  native replay supplies the callback evidence.
- The initial metadata probe used ambiguous `root_path` terminology. The
  human-run corrected probe names the instruction file explicitly. Both the
  callback payload and complete root digest were checked independently of that
  answer.
- Claude's later API refusal leaves that additional model-response probe
  unassessed. Native startup callback checks still have actual logs; the report
  does not count them as model answers.
- The recovery collector initially had no command-approval handler. The Codex
  run stopped. The corrected collector records each exact request and separate
  executor review; it accepts only the reviewed read commands, not persistent
  policies or any decision on a formal artifact.
- Claude interpreted the prompt's contrast between the real source repository
  and the disposable installation as a possible version discrepancy. It did
  identify the fixture's actual 0.19.0 selection and stop at the denied identity
  command. Its source-versus-fixture comment is a probe-communication limitation,
  not evidence of a mismatch in the real source repository. Fresh successful
  lifecycle-context recovery is established by the separate Codex run.

No product behavior change was needed for this acceptance batch. Native host
tool permissions remain distinct from lifecycle authority. Failed attempts are
not erased and passing delivery is not presented as an execution grant.

## Reading cost and supporting checks

The measurement script was rerun against the current instruction files. All
six results exactly match the retained [reading-cost data](../../../acceptance/progressive-discovery/reading-cost.json).
The complete reviewed source has 21,888 whitespace words; the injected root
has 1,191 words. Each scenario includes the root, COMMUNICATION.md, the selected
procedure's entry conditions and applicable reference sections. Repeated line
ranges in the same file count once.

| Scenario | Unique instruction words |
| --- | ---: |
| New requirement draft | 5,049 |
| Resumed implementation | 3,385 |
| Verification decision | 3,952 |
| Pull-request preparation | 4,692 |
| Blocker recovery | 3,680 |
| Evaluator setup | 2,406 |

These are reproducible reading walks, not measured model tokens or a claim that
every native session chose the minimum set. Selected formal artifacts and
evidence are separate inputs. Native reads are retained in their actual traces.
The recomputation is recorded in [reading-recheck.json](provenance/reading-recheck.json).

Current-source checks: 9 focused delivery tests passed with one platform skip;
the full suite passed 1,122 tests with 16 skips. Release-distribution validation,
CLI help, released doctor, graph validation and WO-IAR-015 review preflight pass.
The exact invocations and output are in this work order's evidence directory.

## Coverage and limits

The full suite supplies deterministic route, authority, installation-boundary,
failure and recovery checks. The native observations add real host callback and
agent-behavior evidence; they do not turn deterministic fixtures into native
events. Other work orders retain the instruction map, evaluator comparison and
Windows/Linux migration evidence. This report does not complete those work orders.

Qualification is for the recorded Windows CLI/native backend versions and
explicit manual compaction. Desktop-specific behavior, automatic compaction
thresholds, and every future host version are not established here. A ready
VREC, human verification, merge, release, publication and source-repository
adoption each remain separate from these observations.

`file-index.json` records source and retained byte digests. Raw transport/debug
logs and private reasoning are not retained. The original failed attempts stay
visible. Collector sources in `provenance/` are inspection copies of transient
tools originally run outside the repository; they are not product components.
The collector acquired a per-command review bridge between the initial and
final Codex recovery attempts. The installed product hook was unchanged.
