---
name: harness-orient
description: Orient an operator to an installed SE Harness repository or one selected formal artifact using its exact released evaluator. Use for read-only repository understanding and next-decision guidance; do not use for implementation, approval, release, Git, credential, or external-action requests.
---

# Harness Orient

Return one decision-ready, read-only orientation to the installed repository.
The harness remains the authority for integrity, lifecycle state, scope, gates,
and accountable roles.

## Explicit hosted sandbox

For an explicitly selected hosted sandbox, first follow setup's hosted selection.
Use its separate candidate client, exact project and baseline or context/version.
Do not run the repository-orientation helper against an endpoint.

Create a transient request outside the checkout. Use the selected service's v1
read schema or its MCP tool schema, including `operation`, `project_id`, `view`
and a budget within 500 rows, 2 MiB and depth eight. Domain reads are `revision`,
`work-context`, `compare`, `impact`, `lineage` and `check`; `cypher` is constrained
exploration with parameters. MCP exposes these same reads, not mutations.

```text
CLIENT_PYTHON -I -m se_harness remote read --endpoint ENDPOINT --project PROJECT --token-env TOKEN_VARIABLE --request ABSOLUTE_REQUEST_JSON --json
```

Read `complete`, unresolved references and any continuation before reporting a
governing context. A partial response cannot support that claim.
If the host saves or truncates a response, inspect the returned file through an
available, permitted read tool. A saved-file notice or successful tool call does
not establish completeness. For large JSON, extract the result metadata without
loading the whole graph into the conversation. If the response cannot be read,
report its completeness as unassessed; do not report unseen content or use it to
support a governing claim.

Retain the view,
revision and evaluator identities and report the embedded released result unchanged.
An accepted read is not an approval. Database-side read-only enforcement remains
unverified under RISK-HAG-001; use only the private public-data sandbox.
The rest of this skill applies to a local repository selection.

## Required inputs

Obtain an unambiguous repository target, a structured launcher for the target's
exact external released evaluator, its expected version and installation root,
and an optional selected artifact. Do not discover an executable in the target
checkout or silently use one from `PATH`.

Use the selected entry returned by activation in the current context. If no
checkout is active, follow the setup skill's activation procedure with the actual
checkout path and host/session values delivered by the hook. After switching or
compaction, validate the selected checkout again. Read applicable owner instructions.
AGENTS.md is not a plugin installation or instruction-delivery requirement.

For a `released-resources-v1` selection, use the exact evaluator's
`resources ABSOLUTE_REPOSITORY --resource RESOURCE_ID --content --json` to read one
required instruction or checklist. Resolve returned resource locations outside
the checkout; formal artifact paths stay relative to the checkout. Do not require
repository copies of ENGINEERING_HARNESS.md or docs/engineering/harness/.
For a legacy selection, use its validated repository entry and task router.

When a result includes `instruction_discovery`, require `status = "available"`.
Read its current step's exact file and heading and each prerequisite whose
condition applies. Read the selected formal records separately. The
`evaluator_only_inputs` are not normal agent reading. An incompatible result
stops the affected action; report the version/discovery gap.

For a released result without this field, use that installed root's procedure
router and reading manifest. Do not apply candidate instructions to an older
selected release. A manual root read does not prove automatic host delivery.

Use the repository-selected released evaluator in its private environment,
through the absolute Python path with `-I -m se_harness`. The helper reports the selected artifact when one was requested. Preserve its actual result,
including failures. If the evaluator needs repair, report setup as the next
step; orientation itself stays read-only.

For this read-only orientation, use the helper below with the selected
evaluator version and environment root. It performs the required identity and
repository checks; do not repeat them before calling it.

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
