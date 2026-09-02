# Read-only agent orientation with `harness-orient`

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. The skill reports installed
> harness state; it does not approve work, make an accountable decision, or
> authorize a later mutation.

## What it does

`harness-orient` gives a supported coding agent one portable procedure for
understanding an installed SE Harness repository. It uses the repository's
exact external released evaluator to check:

- evaluator version and identity;
- installed managed-file integrity;
- formal artifact graph validity;
- repository-wide lifecycle and attention queues;
- one selected WO, VREC, or RLS scope when the `check` projection is supported; and
- an explicitly requested work-order preflight when that capability exists.

The result names current lifecycle state, selected and repository blockers,
the count of unrelated background observations, the required accountable role,
and one recommended next step. It includes a canonical
`se-harness-execution-receipt-v1` object and its SHA-256.

The procedure is single-agent and read-only. It does not spawn workers, edit a
file, apply a lifecycle transition, install software, use the network or
credentials, change Git, retain a receipt in the target, or affect an external
system.

## Invoke it through an agent

Ask the agent to use `harness-orient` for the target repository and, when
useful, name one formal artifact. Supply the external evaluator environment if
the agent cannot identify it unambiguously. For example:

> Use `harness-orient` to orient to this repository and `WO-ABC-001`. The exact
> released evaluator is version `0.14.0` in `C:\tools\se-harness-eval`.

The agent reads `.agents/skills/harness-orient/SKILL.md`, establishes the
managed skill's integrity with direct exact-evaluator identity and doctor
checks, and only then invokes the included runner with structured arguments.
The runner repeats those checks so the receipt is self-contained. Skill
discovery or loading does not grant implementation or lifecycle authority.

## Invoke the runner directly

First use the external evaluator to verify its identity and run `doctor` on the
target. Do not execute a managed helper whose integrity has not passed. The
commands depend on the evaluator environment; they follow this shape:

```text
<external-python> -I -m se_harness --version
<external-python> -I -m se_harness identity --role released-evaluator --expected-version VERSION --expected-root EVALUATOR_ROOT --checkout-root TARGET --require-isolated-python
<external-python> -I -m se_harness doctor TARGET
```

The evaluator launcher is a JSON array, not a shell command string. On Windows
PowerShell, an external virtual environment can be supplied as follows:

```powershell
python .agents/skills/harness-orient/scripts/orient.py . `
  --evaluator-launcher-json '["C:\\tools\\se-harness-eval\\Scripts\\python.exe","-I","-m","se_harness"]' `
  --expected-evaluator-version 0.14.0 `
  --expected-evaluator-root C:\tools\se-harness-eval `
  --artifact WO-ABC-001
```

On Linux or macOS:

```bash
python .agents/skills/harness-orient/scripts/orient.py . \
  --evaluator-launcher-json '["/opt/se-harness-eval/bin/python","-I","-m","se_harness"]' \
  --expected-evaluator-version 0.14.0 \
  --expected-evaluator-root /opt/se-harness-eval \
  --artifact WO-ABC-001
```

Add `--preflight-phase start` or `--preflight-phase review` only with an
explicitly selected work order. Preflight output is evidence about readiness;
it is not approval or start authority.

## Interpret the result

The runner writes one canonical JSON object to standard output and no file to
the target. Important fields are:

| Field | Meaning |
| --- | --- |
| `outcome` | `completed`, `degraded`, `blocked`, or `failed` procedure result |
| `released_evaluator` | Exact observed version and identity outcome |
| `integrity` and `validation` | Installed-content and formal-graph results |
| `selected` | Selected lifecycle state and governing scope, or `not_assessable` |
| `blockers` | Selected blockers kept separate from repository blockers |
| `background_observation_count` | Unrelated observations that must not displace the selected task |
| `decision` | Required accountable role, one recommendation, and command or suggested response |
| `execution_receipt` | Skill identity, attempted operations, state digests, changed paths, deviations, and residual uncertainty |

`changed_paths` must be empty and the before/after repository and Git-reference
digests must match. The receipt is evidence, not lifecycle authority.

## Compatibility and fallback

The minimum released evaluator is 0.5.0. Version, identity, doctor, validation
JSON, and inspection JSON are required. A missing or unsuccessful required
operation blocks orientation.

The `check` projection (`check --artifact ID --json`, the `focus-json`
operation) and explicitly requested preflight are optional. If the verified
evaluator does not advertise `check`—for example, the supported 0.5.0
capability profile—the selected scope is `not_assessable` and the overall
result is `degraded`. Repository validation and inspection remain available.
The skill does not parse prose or run candidate source to guess the missing
scope.

## Troubleshooting

- **Version or identity mismatch:** supply the exact released evaluator named
  by the repository lock. Do not substitute the checkout or install a package
  during orientation.
- **Managed integrity failure:** preserve the reported diagnostic and follow a
  separately authorized repair or upgrade procedure. Do not run the bundled
  orientation helper.
- **Invalid graph:** correct it only under an approved work order. Orientation
  stops before inspection when validation cannot safely continue.
- **Selected scope not assessable:** use the reported reduced-capability result
  or separately upgrade the repository's evaluator through the managed upgrade
  process.
- **State changed during orientation:** treat the result as failed, identify
  the concurrent writer, and retry only after the target is stable.

See [installation and safe upgrades](harness-installation-and-upgrades.md) for
the evaluator environment and managed upgrade boundary.
