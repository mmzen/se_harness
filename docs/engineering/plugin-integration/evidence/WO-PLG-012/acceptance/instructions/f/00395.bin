---
name: harness-orient
description: Orient an operator to an installed SE Harness repository or one selected formal artifact using its exact released evaluator. Use for read-only repository understanding and next-decision guidance; do not use for implementation, approval, release, Git, credential, or external-action requests.
---

# Harness Orient

Return one decision-ready, read-only orientation to the installed repository.
The harness remains the authority for integrity, lifecycle state, scope, gates,
and accountable roles.

## Required inputs

Obtain an unambiguous repository target, a structured launcher for the target's
exact external released evaluator, its expected version and installation root,
and an optional selected artifact. Do not discover an executable in the target
checkout or silently use one from `PATH`.

Read the applicable repository instructions and this file completely. Validate
the retained `skill-contract.json` before executing the procedure.

## Procedure

Use the absolute environment Python and release identity already verified by
`setup`. Before running a helper, directly repeat `--version`, released-evaluator
`identity` and `doctor` for this target with that launcher. Match the expected
version, environment root, payload and archive against the target's governing
lock. Stop if a check fails; orientation does not perform setup or repair.

Separately verify this installed plugin core against the previously trusted
plugin package identity, including its contract and helper bytes. Repository
`doctor` verifies managed repository content; it does not authenticate these
plugin copies. Use the absolute helper path under that verified plugin root.
Do not trust a path or digest merely because the target repository supplies it,
fall back to its managed helper, or execute an unverified helper to validate
itself. Missing trusted plugin identity blocks the procedure.

Then run the plugin's `scripts/orient.py` with the same structured inputs. Supply the
evaluator launcher as a JSON array, never as a shell command string. The script
repeats the required `version`, `identity`, and `doctor` checks for its receipt,
then runs `validate --json` and `inspect --json`. When an artifact is selected,
it uses `check --artifact ID --json` only if the verified evaluator advertises
that public command with an optional `--checkpoint` (se-harness 0.11.0 and
later); an evaluator whose `check` requires a checkpoint degrades the
selected scope. It runs preflight only for an explicitly selected work order and
requested phase.

Invoke the helper with the verified absolute environment Python and `-I -B`,
from outside the target. Clear `PYTHONPATH` and put the verified environment's
`Scripts` or `bin` first in the subprocess PATH. The evaluator launcher is the
actual argument array `[ABSOLUTE_PYTHON, "-I", "-B", "-m", "se_harness"]`.
Resolve every placeholder before dispatch; preserve arguments as separate values.

```text
ABSOLUTE_PYTHON -I -B ABSOLUTE_PLUGIN_CORE/scripts/orient.py ABSOLUTE_TARGET
  --evaluator-launcher-json JSON_ARRAY
  --expected-evaluator-version EXACT_VERSION
  --expected-evaluator-root ABSOLUTE_ENVIRONMENT
```

Add `--artifact ID` only for the selected artifact and `--preflight-phase start`
or `--preflight-phase review` only when that WO phase was explicitly requested.
The retained helper owns the operation order and receipt schema. `-B` keeps
bytecode files out of the verified plugin core.

Return the script's canonical JSON result inline. Summarize its lifecycle
state, scoped blockers, repository blockers, separately counted background
observations, required accountable role, and exactly one recommended next
step. Keep candidate-source observations separately labeled and never present
them as the governing result.

## Boundaries

- Perform no repository, Git, lifecycle, environment, network, credential, or
  external mutation.
- Do not install or repair a missing evaluator or damaged managed content.
- Missing required evaluator behavior blocks orientation. Missing optional
  projection (`check`) or requested preflight behavior degrades only the named
  output.
- Do not parse human prose to invent selected scope when the projection JSON
  is absent.
- Do not start work, apply a transition, or claim an accountable decision.
- Stop on ambiguous selection, conflicting owner instructions, evaluator
  identity failure, managed-integrity failure, invalid formal state, malformed
  required JSON, or any observed state change during orientation.
- Use the complete single-agent procedure. Do not spawn or coordinate workers.

The receipt is evidence, not authority. Return it inline and write no receipt
or other evidence file into the target repository.
