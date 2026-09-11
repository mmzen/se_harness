---
name: evidence
description: Retain observed checks and prepare SE Harness verification or release records through existing released procedures. Use for evidence handoff, candidate capture, preparation recovery, and identifying the next accountable decision.
---

# Evidence

Make the selected candidate and its observed results reviewable. Preparation
leaves the assurance or release decision with its accountable owner.

## Establish context and select the procedure

Before a governed write, require the current repository's freshly verified
released evaluator, passing managed integrity, and complete governance context
read in this session. Read the managed `AGENTS.md` gate, `ENGINEERING_HARNESS.md`,
operating card and selected phase reading manifest. A summary, lifecycle
projection or stale handler receipt does not establish readiness.

If that context is absent, stale or incomplete, stop governed writes and recover
through `setup`. Setup prepares the evaluator environment; it does not itself
deliver complete context. Where supported, read `session-context.py` delivery
through its matching `END VERIFIED GOVERNANCE` marker, including the exact
full-read argument array if requested. Report unavailable verified delivery as
a readiness blocker. Do not bypass it with a directly runnable mutation.

Use setup's verified absolute environment Python with `-I -m se_harness`, from
outside the checkout, with cleared `PYTHONPATH` and that environment's `Scripts`
or `bin` first in the process PATH. Expand returned `harnessctl` argument arrays
to that invocation; preserve every argument and the absolute repository path.
Confirm operations against the selected release's help and `WORKFLOW.json`.

Select one WO, VREC or RLS with checkpoint-free `check --artifact ID`. Follow
its actual procedure and gates. For an already supplied decision, compare the
inputs in [Continuing authority](../change/references/authority.md); continue
without another approval while that decision still applies. If the reference
is unavailable, read the installed decision-rights contract and report the
missing adapter dependency before an affected write. An actor argument or
suggested response is not an approval.

## Retain observations

Record the full candidate commit, actual argument arrays, working directory,
runtime identity, exit status, output, relevant file paths and byte digests.
Keep failed and missing checks visible. Separate a fixture or intercepted tool
from a real host or external action. Do not invent a result, erase an original
failure after a successful retry, or turn an unrun check into a pass.

Choose the relevant reference:

- [Prepare evidence and records](references/records.md) for handoff, VREC or RLS.
- [External actions](references/external-actions.md) if the selected procedure
  reaches integration, tagging, publication or deployment.

If acknowledgement is lost, inspect the existing record, evidence, lifecycle
history, Git state and checkpoint-free projection before retrying. Compare
them with the requested operation and retained inputs. Continue only effects
known not to have occurred. If effects cannot be inspected, stop the affected
write and report the uncertainty; do not create a replacement ID or overwrite
the existing record to conceal it.

At handoff, obtain the selected schema-2 result and report observed effects,
material non-effects, final lifecycle state, the blocker or accountable
decision, and its one typed next step. Preparing a ready record never supplies
the later verification or release decision.
