# Session context handler

`session-context.py` checks the prepared released evaluator, runs `doctor`, and
returns the managed `AGENTS.md` gate and complete `ENGINEERING_HARNESS.md` router.
It does not install anything or record lifecycle or readiness state.

## Invocation

The future host binding invokes the prepared environment's absolute Python with
`-I -B` and the absolute script path. It supplies these trusted arguments:

| Argument | Meaning |
| --- | --- |
| `--repo` | Existing absolute repository directory, without linked ancestors. |
| `--environment` | Prepared private evaluator environment outside the repository. |
| `--version`, `--payload-sha256`, `--archive-sha256` | Fixed identities from the accepted package; never learned from untrusted hook input. |
| `--host` | `codex` or `claude`. Both selected protocols use the envelope below. |
| `--context-limit` | Qualified capacity for a complete context string, in UTF-8 bytes. |
| `--read-limit` | Qualified complete-read tool capacity; zero means unavailable. |

The event arrives on stdin:

```json
{"hook_event_name":"SessionStart","source":"compact","cwd":"ABSOLUTE_REPOSITORY"}
```

Supported sources are `startup`, `resume`, `clear`, and `compact`. The `cwd` must
match the configured repository. Resume and compaction each repeat identity,
integrity, and source reads. A prior session summary supplies no cached result.

The stdout response uses `hookSpecificOutput.hookEventName = "SessionStart"`
and `hookSpecificOutput.additionalContext`. Failures return explicit `UNREADY`
context through that same supported channel. Structured stderr retains the
evaluator findings and timestamps. The handler writes no files.

These envelopes follow the [Codex hook reference](https://learn.chatgpt.com/docs/hooks)
and [Claude Code hook reference](https://code.claude.com/docs/en/hooks), inspected
on 2026-09-10. Context restoration uses `SessionStart` with source `compact`.
The shared handler does not register a `PostCompact` binding.

## Complete read when the hook is too small

If the full context exceeds the hook capacity, the response remains `UNREADY`
and gives an argument array for the same script with `--read-sha256 HASH`.
The host's supported tool runs that array without shell interpolation and reads
the complete stdout. This mode needs no stdin. It repeats verification and
rejects a changed hash before emitting content.

The receiver must read the complete content through its matching
`END VERIFIED GOVERNANCE` marker. The marker is after all source bytes. Missing,
interrupted, or truncated output remains unready. There is no receipt flag to
trust, separate context file to become stale, or approval store.

The handler can prove what it prepared; it cannot prove what a host later
truncated or delivered to the model. Stderr therefore reports
`complete-output-prepared`, not successful receipt. Bindings must qualify both
capacities and the full-read transport. A host's approximate token limit is not
a UTF-8 byte limit. No fallback is enabled by default.

## Tests

Run focused tests with a provided Python 3.11+:

```text
python -B -S -m unittest discover -s tests/plugin_integration/session_context -p "test_*.py" -v
```

For VER-PLG-007 C01–C08, run `run_acceptance.py` with the released evaluator's
Python and `-I -B`. Supply `--evaluator ABSOLUTE_ENV_PYTHON`, `--sandbox NEW_DIR`,
and `--evidence NEW_DIR`. The runner fixes 0.17.0 release identities in source,
initializes disposable repositories through that release, captures expected
bytes independently, and retains raw commands, outputs and inventories.

The focused tests inject evaluator results to exercise malformed data and race
boundaries. The acceptance cases use the real released evaluator. C05 injects
receiver truncation/interruption; C06 changes line endings after a real doctor
call and checks revalidation; C07 observes a real missing-executable error.
These are shared handler and transport fixtures. Native host registration and
live delivery qualification belong to WO-PLG-005/006 and WO-PLG-015.
