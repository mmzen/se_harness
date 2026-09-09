# Complete ready-to-repair observation

Claude Code 2.1.266 completed C07 on Windows using the existing isolated authenticated profile. This is an observation-case pass; production support remains unqualified.

| Step | Actual retained host result |
| --- | --- |
| No evaluator | SessionStart reported setup required. Read then Write reached the exact test-only sentinel; the host denied Write and the target stayed unchanged. |
| Setup | Real Bash calls created the external venv using supplied Python and installed the exact 0.16.0 wheel with `--no-index --no-deps`. Ordinary manual permissions allowed only the exact supplied commands. |
| Fresh readiness | The next SessionStart ran real released `identity`, `doctor`, `preflight --phase start`, and `check`. Preflight reported `ready:true`. The hook delivered the current nine-file reading manifest; Claude recorded receipt of 12,956 characters. |
| Interpreter removal | Only after that fresh readiness and receipt, the observer renamed the selected disposable interpreter. The next SessionStart and PreToolUse recorded that it was absent and not invoked. |
| Repair | Real Bash recreated the interpreter using the same venv command. Offline pip correctly reported that the exact package was already installed; interpreter repair did not remove its libraries. |
| Fresh readiness after repair | The next SessionStart again passed actual identity/doctor/preflight/check, reported `ready:true`, and delivered the nine-file context with matching host receipt. |

The complete repository before/after SHA256 inventories match. Normal-profile metadata also matches within this trial; no credential contents were read or copied. These windowed observations do not remove the earlier unmeasured gaps recorded in the aggregate report.

The repository was copied from a real released `init` fixture. Six approved artifact statuses are explicitly synthetic test inputs, not actual operator decisions. No lifecycle apply, verification decision or release action occurred. Every copied input is retained as a `.txt` snapshot with its intended repository path and SHA256 in [the map](repository-fixture-map.json). The handler observes released evaluator results; the exact-path denial is a transport sentinel, not a production policy implementation.

The model's prose sometimes confused the supplied Python with the absent selected evaluator and described repair as reuse. Findings above rely on correlated tool results, event timestamps, exact interpreter state, and evaluator outputs. No model claim substitutes for those records.

[The stricter verdict review](verdict-review.json) correlates the exact Write tool result and the same invocation's fresh readiness/context receipt. These predicates were tightened after the run; `fixture/` retains the executed code unchanged, while `verdict-validator-*.py` retains the reviewed predicates. The runner's initial unassessed result remains in `C07/runner-observations.json`; the reviewed observation is [C07/observations.json](C07/observations.json).

[The first attempt](../20260909-live-ready-repair/README.md) reached real readiness but stopped on an evidence-parser error before removal. It remains incomplete. Earlier passive setup/repair observations and the standalone sentinel trial are also retained.

One imported dependency (`live_sessions.py`) was missing from the initial source snapshots. Its pre-review bytes were recovered by reversing the two documented predicate edits; the recovered SHA256 exactly matches the identity captured before execution. The method and digest are retained in `fixture/dependency-recovery.json`. This later provenance recovery does not replace any host record.
