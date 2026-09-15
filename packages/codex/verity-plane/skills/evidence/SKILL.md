---
name: evidence
description: Retain observed checks and prepare SE Harness verification or release records through existing released procedures. Use for evidence handoff, candidate capture, preparation recovery, and identifying the next accountable decision.
---

# Evidence

Make the selected candidate and its observed results reviewable. Preparation
leaves the assurance or release decision with its accountable owner.

## Repository context

Read the selected repository's AGENTS.md and ENGINEERING_HARNESS.md on entry,
after compaction, and after switching repositories. Read the operating card and
the reading manifest for the selected work. Use normal file reads.

Use the repository-selected released evaluator in its private environment,
through the absolute Python path with `-I -m se_harness`. Run
`check ABSOLUTE_REPOSITORY --artifact ID --json` when beginning governed work,
then follow its procedure and required checkpoints. Preserve its actual result,
including failures. Run setup if the evaluator environment needs repair.

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
