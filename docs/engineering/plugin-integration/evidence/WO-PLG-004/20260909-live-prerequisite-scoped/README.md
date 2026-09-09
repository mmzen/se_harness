# Actual missing provided-Python setup entry

Claude Code 2.1.266 invoked the probe setup skill in the existing isolated authenticated profile. The skill instructed one read-only Bash check of a deliberately absent provided-interpreter path. The host executed the exact `ls -ld` command, returned missing-path exit 2, and told the operator to install Python 3.11+ with `venv` and `ensurepip` before continuing. No Python was downloaded, no runtime was created, and the disposable repository stayed unchanged.

The selected prerequisite directory was created empty within the task sandbox and explicitly included with `--add-dir`. Permission mode remained manual, with only the exact check allowed. This directory grant is retained in the command record. Normal-profile metadata was equal within this trial's before/after window; credential contents were not read.

The full C02 matrix remains incomplete: this tests the missing-provided-Python branch, not an actually older Python or an unusable `venv`/`ensurepip` installation. The identities record checks the genuinely supplied Python 3.14.6 and imports its actual modules. It does not simulate a negative version or module failure.

## Earlier attempts retained

- [Initial check](../20260909-live-prerequisite/C02/observations.json): actual `test -f` ran, but its structured tool result suppressed the exit code. Observer inventory confirmed absence; the model's guidance alone did not prove the check's failure.
- [Explicit diagnostic attempt](../20260909-live-prerequisite-explicit/C02/observations.json): `ls -ld` was refused by the host because the empty prerequisite directory was outside the permitted working scope. No alternate command bypassed that refusal.
- [Current observation](C02/observations.json): the exact empty task-owned prerequisite directory was then included explicitly in a fresh trial. The real diagnostic and guidance are retained.

These are probe-only fixtures and observations. No lifecycle transition, assurance decision, or production plugin qualification is recorded.

The separate [supplied-runtime inventory](../repository-checks/authenticated-continuation/supplied-runtime-inventory.json) executed the actual accessible Python 3.11.9 and 3.14.6 interpreters; both imported `venv` and `ensurepip`. It does not establish a comprehensive inventory of the machine or a negative-version test.
