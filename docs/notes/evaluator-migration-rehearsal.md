# Rehearsing an evaluator migration

> This is an operator guide. A rehearsal produces evidence only. It does not approve a candidate, change a lifecycle record, release or publish anything, or replace the repository's current released evaluator.

## Why this exists

When SE Harness version N introduces governance rules that version N-1 does not understand, neither version can simply take over the whole release process:

- N-1 is still the released evaluator and must remain selected for the repository.
- N must prove that the future repository is valid under its new rules.
- N cannot make itself authoritative merely because its tests pass.

The 0.6.0 release found the missing handover steps one at a time. `harnessctl rehearse-migration` now runs the complete handover in a disposable directory before a release. It uses two separately installed Python environments: one for the released predecessor and one for the successor candidate.

## What the rehearsal does

The command always runs the same nine stages, in this order:

| Stage | Purpose |
| --- | --- |
| `prepare` | Let the predecessor role prepare the first proposal, directly or through its exact declared compatibility adapter. |
| `validate-complete` | Let the successor inspect the complete graph without changing it. An expected incompatibility is recorded as structured data, not ignored text. |
| `reject` | Replay an already attributed rejection fixture. The runner does not make the rejection decision. |
| `replace` | Create a distinct corrected proposal while preserving the rejected proposal as immutable history. |
| `assess` | Record the successor's complete-graph result separately from the predecessor-compatible view result. |
| `release-plan` | Resolve the corrected release inputs without changing lifecycle state or Git. |
| `publish-plan` | Resolve publication inputs without a credential, tag, upload, or external call. |
| `render` | Render a disposable governance snapshot that points to the corrected proposal. |
| `adopt` | After a simulated immutable publication and a separate attributed fixture, exercise root adoption only in the disposable root, including rollback and no-op replay. |

The predecessor remains selected through the first eight stages. Only `adopt` may select the successor, and it does so only inside the disposable test root.

## Running it

Prepare two non-editable environments outside the operational checkout. The predecessor must be the exact released version. The successor must be the exact candidate package or other exact candidate runtime being qualified.

```powershell
harnessctl rehearse-migration <operational-root> `
  --scenario tests/fixtures/governance_migration/historical-0.5.0-to-0.6.0.json `
  --predecessor-python <external-0.5.0-env>/Scripts/python.exe `
  --successor-python <external-candidate-env>/Scripts/python.exe `
  --output <external-absent-directory> `
  --json
```

On Linux, use each environment's lexical `bin/python` path. Do not resolve that final virtual-environment link to the shared system interpreter.

The scenario may live in the checkout because it is read only. The output must be outside the checkout, must not contain the checkout, and must be absent or empty. The two interpreters and their installed packages must also be outside the checkout and isolated from one another.

## Reading the result

The retained file is `governance-migration-result.json`. Important fields are:

- `overall_result`: `pass` only when all nine stages passed.
- `first_failed_stage`: the first failed stage; every later stage is `not-run`.
- `classification`: whether the successor needs a migration and which operations are affected.
- `runtimes`: exact version, interpreter, and installed-package digests for both roles, without host paths.
- `stages`: actor role, view, decision fixture, permitted and observed disposable changes, bounded report, and report digest for every stage.
- `operational_state.unchanged`: proof that repository bytes, HEAD, and refs did not change.
- `external_actions`: explicit `false` values for credentials, network, lifecycle transition, tag, release, publication, deployment, maintenance, policy, and real root upgrade.
- `semantic_sha256`: a replay digest that omits timing, host/interpreter facts, the raw checkout digest, and the independently built successor distribution identities so Windows and Linux results can be compared. The full result still retains those exact platform facts; the digest keeps the candidate Git identity, scenario, contract/runner identity, stage reports, decisions, and unchanged-state claim.

A pass is qualification evidence. Accountable owners still decide whether to approve requirements, verify a VREC, release an RLS, publish, or later adopt the released evaluator.

## Relationship to release qualification roles

The migration rehearsal proves the whole simulated predecessor-to-successor sequence in disposable state. It does not replace the narrower operational claims made by `harnessctl qualify`. A real workflow records complete successor validation as `complete-candidate` and later root ownership as `released-root`; the former `predecessor-view` operation was retired under `WO-REB-028`, and this rehearsal is now the one mechanism that exercises a predecessor evaluator against a successor. The rehearsal result and those typed results remain separate evidence because they answer different questions.

## Failure behavior

The runner fails before or at the affected stage when it sees an unknown field, noncanonical JSON, missing or reordered stage, role substitution, forged decision fixture, undeclared adapter or view, shared runtime, checkout import, credential-bearing environment, unexpected write, timeout, malformed child report, source/ref change, failed rollback, or result disagreement.

It does not try another evaluator, remove extra repository files, accept an error string, continue after failure, or repair the operational checkout. It removes only its own disposable workspace and retains the bounded result.

## Adding a future scenario

Use `synthetic-n-minus-1-to-n.json` as the version-neutral example. A new scenario may select only capabilities, roles, views, adapters, decisions, and stages already allowed by `se-harness-governance-migration-v1`. It must remain canonical UTF-8/LF JSON and must bind its fixture and decision bytes with SHA-256.

If a future migration needs a new stage, decision meaning, authority effect, or view type, create a new contract version and obtain accountable review. Do not silently modify a completed historical scenario.

The exact 0.5.0-to-0.6.0 scenario is permanent regression history. The candidate workflow runs it twice on Windows and Linux with the digest-pinned public 0.5.0 wheel and a non-promotable wheel exported from the exact candidate commit. Public-wheel acquisition and candidate building happen before the core runner; the runner itself has no network or credential path.
