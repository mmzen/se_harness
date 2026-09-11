# Change skill acceptance

The product is Markdown instructions. A script that hard-codes the desired
authority decisions cannot test whether an agent follows those instructions.
The independent agent pass therefore fixed its oracle before reading the skill,
then executed the supplied requests in disposable repositories with a separate
call recorder. Its raw results and corrected repeats are retained under
`docs/engineering/plugin-integration/evidence/WO-PLG-010/acceptance/independent-windows/`.

The oracle, fixed input bytes, original and corrected skill copies, command
arguments, stdout/stderr, state readbacks and hashes remain reviewable. A fresh
behavioral repeat needs an agent, the skill, those raw inputs and isolated tool
access. It must record actual calls and effects, including absent actions.

## Live delegation supplement

Run `run_live_delegation.py` with an independently verified external 0.16.0 or
0.17.0 evaluator's absolute Python and `-I -B`, from outside the checkout. Pass
`--source ABSOLUTE_CHECKOUT --sandbox NEW_DIRECTORY --evidence NEW_DIRECTORY`.
The source must contain the fixed historical commits named in the script.

This runner clones locally, changes refs only in disposable clones, and reads
real public GitHub check results. It never pushes a fixture or changes lifecycle
state. It probes the existing released guard's three delegated rights, four
non-delegated rights, branch-only class and unpublished-head refusals. It is
explicitly separate from observing an agent's choices and from actually applying
start, completion or VREC preparation.

The frozen published commit is historical evidence. If its remote check is no
longer available, the run fails; it must not substitute a fabricated passing
check or another commit. Requires Git, local checkout access and GitHub read
access. The temporary child-process Git config trusts only the exact source
checkout/Git-directory paths; it does not change the user's Git configuration.

Retain failed setup attempts and successful repeats separately. Neither this
runner nor command replay registers native host hooks or qualifies live plugin
activation.

## Portable command replay

Run `run_workflow_replay.py` with the verified external 0.16.0 Python and
`-I -B`. Supply `--source ABSOLUTE_CHECKOUT --sandbox NEW_DIRECTORY
--wheel ABSOLUTE_RELEASED_WHEEL`. The default `fixtures/observed/` contains
hashed raw artifacts, helper inputs and the observer's actual command sequence.
Input corruption is rejected before target creation. The replay initializes
fresh platform-managed repositories; it never copies a Windows lock or venv
to Linux. Each subprocess retains arguments, status, output, before/after hashes
and observed mutations. The runner compares effects against the fixed traces.

The retained Linux repeat made 75 calls. Its readiness step runs the existing
Bash setup and shared handler; it does not register a native plugin. Empty
mutation sequences remain replayed snapshots, not independent proof of an
agent's refusal. Keep the separate Windows behavioral report for those choices.
