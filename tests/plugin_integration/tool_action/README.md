# Before-tool handler: invocation and acceptance

`check-tool-action.py` checks a proposed file edit with the existing released
evaluator. It returns a host decision before the edit. It adds no approval
store, lifecycle policy, installer or readiness cache.

WO-PLG-008 implements the shared handler. WO-PLG-005/006 own host registration;
WO-PLG-015 qualifies live interception. This directory tests captured protocols
on Windows. It does not establish that a running Codex or Claude installation
intercepts every tool.

## Supported actions

| Host | Tool input | Paths checked |
| --- | --- | --- |
| Codex `apply_patch` | `tool_input.command`: a native patch | Every added, updated or deleted path; both paths of a move |
| Claude `Write` | `file_path`, `content` | The named file |
| Claude `Edit` | `file_path`, `old_string`, `new_string`; optional boolean `replace_all` | The named file |

The event must be `PreToolUse`, with `cwd` equal to the configured repository.
Unknown input fields, patch syntax, path traversal, linked targets and paths
outside the repository are refused. A recursion marker grants no exemption.
Shell commands, continuing shell sessions, MCP and other tools are unmapped.
They receive a coverage refusal if delivered to this handler; a tool which
never emits an event is outside its control.

The canonical Codex field is `command`, even where a hook matcher uses the
`Edit` or `Write` alias. The supported denial is `hookSpecificOutput` with
`hookEventName: PreToolUse`, `permissionDecision: deny`, and a nonempty
`permissionDecisionReason`. See the [Codex hook reference](https://learn.chatgpt.com/docs/hooks)
and [Claude hook reference](https://code.claude.com/docs/en/hooks).

## What happens for one edit

1. Read the host event from stdin and derive the actual edit paths.
2. Check the prepared environment and repository through released `identity`
   and `doctor`, using WO-PLG-007's shared runtime verifier.
3. Run the same released evaluator with the selected work order:

   ```text
   <absolute-environment-python> -I -B -m se_harness check <repository>
     --artifact <selected-WO> --checkpoint pre-action
     --procedure PROC-WO-IMPLEMENT --changes-complete
     --changed-path <actual-path> [--changed-path <another-path>] --json
   ```

4. Require a current schema-2 passing result for that work order, then recheck
   the installation snapshot and mapped paths.
5. Return a denial on failure. On success, return context stating that checks
   passed, without an `allow` decision that could override host permissions.

`pre-action` preserves the evaluator's required implementation gates. A
scope-only check cannot replace it: scope alone does not establish an eligible
work-order state. If current evidence or another prerequisite is missing, the
evaluator's correction remains required. The handler does not manufacture that
evidence, approve work, mark it implemented, prepare a VREC or merge a PR.
The evaluator may write its existing derived check evidence; failures require
inspection of partial writes before retry.

## Binding inputs and time budget

Bindings invoke the prepared environment's absolute Python with `-I -B`,
followed by the absolute script path and these arguments:

| Arguments | Source |
| --- | --- |
| `--repo`, `--environment` | Explicit repository and prepared environment, outside the checkout |
| `--version`, `--payload-sha256`, `--archive-sha256` | Expected released runtime identity |
| `--host codex\|claude`, `--artifact WO-...` | Qualified binding and selected work order |
| `--inner-timeout`, `--host-timeout` | Measured evaluator and host budgets, in seconds |
| `--startup-margin`, `--cleanup-margin`, `--output-margin` | Measured reserves, in seconds |
| `--refusal-mode deny` | A synchronous binding that supports the documented refusal |

These are binding inputs, not fields the tool event can override. Selecting an
artifact does not authenticate its owner. There is one monotonic inner deadline
across identity, doctor and the checkpoint; each call consumes the remaining
time. The inner budget plus all three margins must be strictly below the host
timeout. Required checks are not omitted to fit a budget.

The current process controller supports Windows only. It creates the evaluator
suspended, assigns it to an owned Job Object, then resumes it. Cleanup stops the
tree and records its process counts and exits. See Microsoft's [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
and [process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags).
Other platforms return unavailable coverage; this work makes no Linux or macOS
process-control support claim.

Stdout carries the small host response first. Stderr carries evaluator results,
argv, timing, cleanup and coverage observations. `--refusal-mode report-only`
reports **UNENFORCED** and never claims a successful check. If the handler cannot
start, the host times out or required denial is missing, inspect actual effects
before retry. The handler cannot prove protection after its own output is lost.

## Run the tests

Use a provided Python 3.11+ on Windows:

```text
python -B -S -m unittest discover -s tests/plugin_integration/tool_action -p "test_*.py" -v
```

Run real-evaluator acceptance from this checkout, with new disposable output
directories and an isolated, verified installation of released 0.17.0:

```text
<environment-python> -I -B tests/plugin_integration/tool_action/run_acceptance.py
  --evaluator <absolute-environment-python>
  --sandbox <new-fixture-directory-outside-checkout>
  --evidence <new-evidence-directory>
```

The runner fixes runtime digests and budgets before testing. It initializes a
disposable repository with the released evaluator, uses explicitly synthetic
work-order data, and prepares the existing pre-action evidence. Positive and
scope-refusal cases run the real evaluator. `fault_invoke.py` replaces only the
final check process for C03; `fault_worker.py` supplies failed, stalled and
interrupted children with a retained partial write. Those fault controls exist
only in tests.

An independent, deliberately fail-open host fixture records target hashes and
effect counts. It performs a sentinel write if the required denial is absent.
Those effects demonstrate the fixture's behavior, not a native host's behavior.
C08/C09 inject host timeout, launch failure and missing output outside the handler.
C06 refuses a caller-supplied checkpoint override as unmapped; supported edits
always use the fixed implementation checkpoint.

The [implementation evidence](../../../docs/engineering/plugin-integration/evidence/WO-PLG-008/README.md)
maps C01–C10 to observed results and retained failures.
