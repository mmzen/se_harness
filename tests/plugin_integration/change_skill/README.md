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

## Execution checks

Current candidate execution is covered by the public workflow and capture tests
in `tests/test_delegation_class.py` and `tests/test_revision_provenance.py`.
They exercise local approval, unchanged scope, normal execution and preparation
without requiring GitHub. Skill review follows the installed policy and returned
commands; a scripted command replay is not independent evidence of model behavior.

The previous live-CI guard supplement tested the retired 0.16/0.17 execution
restriction. Its runner was removed by WO-KIS-009; the original source remains
in Git history before this work order, and its recorded observations remain
historical evidence under WO-PLG-010. Do not rerun that old oracle as a current
execution qualification.

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
