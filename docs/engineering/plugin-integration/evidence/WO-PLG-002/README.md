# WO-PLG-002 implementation evidence

The setup skill and its environment procedure are delivered at candidate
`ad9cb2cba0f9168a3f2b63f62d2d63a19a548578`. On 2026-09-10, the operator explicitly
authorized completion and verification-record preparation. The released
evaluator recorded WO-PLG-002 as **implemented**. This report is retained before
capture of the ready record; its assurance decision remains separate.

## Delivered behavior

- Discover an actual provided Python, then check Python 3.11+, venv and ensurepip.
- Check the accepted package's fixed wheel hash and the target repository lock.
- Create the private environment outside the repository and install the wheel
  offline, without activation or global changes.
- Reuse only an environment that passes a fresh released-identity check,
  including the observed archive hash. Refuse incomplete or mismatched setup.

The plugin adds two instruction files: `SKILL.md` and `references/environment.md`.
The reference contains the shared Python checks and native PowerShell/Bash
commands. The acceptance runner executes those exact blocks; it is test tooling
under `tests/`, not shipped plugin code. No bootstrap executable or interpreter
is added. Existing evaluator, host adapters and repository controls are unchanged.

## Acceptance observations

Each row exercised ENV01–ENV12 from VER-PLG-002. The retained executed reference
and runner match the candidate bytes. Expected archive and payload digests were
fixed from the published release evidence before running candidate instructions.

| Host | Python | Evaluator | Cases | First setup | Reuse |
| --- | --- | --- | --- | --- | --- |
| Windows | 3.11.9 | 0.16.0 | [12/12](acceptance/win311-016-attempt3/summary.json) | 15.55 s | 1.14 s |
| Windows | 3.14.6 | 0.17.0 | [12/12](acceptance/win314-017-attempt2/summary.json) | 11.71 s | 1.14 s |
| Linux | 3.12.3 | 0.16.0 | [12/12](acceptance/linux312-016-attempt3/summary.json) | 38.06 s | 1.81 s |

Linux used Ubuntu 24.04 under WSL2 and `unshare -Urn`. Retained `/proc` observations
show only loopback and no routes. Windows commands ran under the Codex sandbox's
network restriction. Both sequences use explicit offline pip flags. These are
local observations, not general performance or native plugin support claims.

| Requirement | Evidence |
| --- | --- |
| REQ-PLG-003: provided Python | ENV01, ENV02 and ENV12: usable Python proceeds; missing prerequisites stop before environment creation. |
| REQ-PLG-004: private offline setup | ENV01, ENV03, ENV04, ENV09 and ENV12: external installation, interrupted-state refusal, reuse, wheel checks and no repository/global PATH changes. |
| REQ-PLG-005: released identity | ENV04–ENV11, plus lock checks in ENV12: fixed release/payload/archive expectations, safe entry points and isolated imports. |

ENV08 demonstrates the plugin-specific boundary: generic `identity` passes
when archive metadata is absent, but the documented readiness check refuses it
even when the expected wheel flag was supplied. ENV11 separately refuses a
missing launcher before identity, a wrong launcher, a wrong expected root and
released package code imported outside the selected environment.

## Required checks and limitations

- [Four focused tests](checks/focused-tests/stderr.txt) passed. They exercise
  malformed or incomplete identity, missing archive observation, absent entry
  points and an environment placed inside the target repository.
- [Skill validation](checks/skill-validation/stdout.txt),
  [release-distribution validation](checks/release-distributions/stdout.txt)
  and [candidate CLI help](checks/candidate-help/stdout.txt) passed.
- Released evaluator 0.17.0 reported passing
  [managed integrity](governance/env-final-doctor.json) and
  [graph validation](governance/env-final-validate.json).
- All 17 [hosted checks](governance/completion-20260910/pr-checks.json) passed
  at `81405ca2cd9bc314905b9238f39f1d11f42210b6`, which retains evidence without
  changing the tested implementation. The [hosted Linux suite](governance/completion-20260910/hosted-suite.json)
  ran 1,126 tests and passed with four skips.
- The [full Windows repository suite](checks/full-suite.txt) ran 1,126 tests:
  one error, 23 skips. The error is `WinError 5` while an existing artifact
  allocation test deletes a read-only Git object. The exact test also
  [fails on unchanged main](checks/baseline-failure.txt) at `3143613e`.
  No test was disabled and no exception is claimed. The local full suite is
  not reported as passing. Original log digests and commands are retained in
  [the regression record](checks/regression-runs.json).

Python 3.11 was exercised on Windows. Linux Python 3.11 and macOS were not
available in the selected environments and remain unqualified. The older-Python
and missing-module classes use explicit isolated failure injection; the missing
executable is a real absent path. The version mismatch changes the disposable
installed runtime version. Interruption stops after venv creation and before
package installation. These fixture limits are recorded in each case.

The implementation stage did not perform native plugin installation/activation,
repository initialization, upgrade, release or merge. Work-order completion was
recorded later under the operator's separate instruction, which also authorizes
preparation of one ready verification record.

## Earlier attempts retained

- `win311-016-attempt1`: the runner passed relative fixture paths to a child
  shell in a different working directory. The command failed; absolute runner
  inputs corrected it. No passing result is inferred from that run.
- `linux312-016-attempt1`: the runner expected a route-table header, but the
  isolated namespace returned an empty table. No acceptance case ran. The runner
  now accepts an empty table while still refusing actual routes.
- `linux312-016-attempt2`: the prerequisite probe assumed a Windows-style
  ensurepip wheel location. Ubuntu refused that assumption. The documented
  probe now uses the public `ensurepip.version()` API, and actual offline
  bootstrapping is exercised by venv. The corrected sequences passed on both OSs.
- `win311-016-attempt2` and `win314-017-attempt1` passed before the Ubuntu
  correction. The final runs above supersede them as evidence for the final code.

All available per-case records are retained under `acceptance/`. The first
Windows failed runner was not copied; its source hash and failing command/output
remain in that attempt's records. The Linux constructor failure is documented
here and its executed runner/reference are retained.

## Authority and next step

The [operator authorization](governance/operator-authorization.json) and the
released evaluator's [approval](governance/env-approved-applied.json) and
[start](governance/env-in_progress-applied.json) transitions concern only
WO-PLG-002. The later [operator decision](governance/completion-20260910/operator-decision.json)
authorizes completion and preparation of one ready record. The released
evaluator [applied completion](governance/completion-20260910/env-completion-applied-20260910.json).
The record will bind the clean candidate containing this report and retained
evidence. Its assurance decision remains with the assurance owner; none of the
reported limits is waived.
