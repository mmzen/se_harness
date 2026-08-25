+++
id = "SPEC-RSK-001"
type = "specification"
title = "Risk artifact schema, lifecycle, gate predicate, commands, and configuration"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-RSK-001", "REQ-RSK-002", "REQ-RSK-003", "REQ-RSK-004", "REQ-RSK-005", "REQ-RSK-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "technical-owner"
+++

# Specification: Risk artifact schema, lifecycle, gate predicate, commands, and configuration

## Scope

This specification defines the `risk` artifact, its lifecycle family, the
decision right that disposes it, one gate evaluator applied to seven existing
gates, two commands, one scope exception, and one configuration section. It
changes no other artifact's schema and no existing decision right.

## Artifact (RSK-ART)

**RSK-ART-001:** Type `risk`, prefix `RISK-`, directory `risks/`. Front
matter is the common header plus a `[risk]` table with `category`, `stage`,
`raised_by`, `likelihood`, `impact`, `score`, `acceptance_level`, `cause`,
`effect`, and optional `residual_likelihood`, `residual_impact`.

**RSK-ART-002:** `score = likelihood * impact`; both integers in 1..5.
Validation reports `E-RSK-001` on mismatch (structure plane).

**RSK-ART-003:** `stage` must match every `threatens` target type per the
table in `REQ-RSK-001`; mismatch is `E-RSK-002` (governance plane).

**RSK-ART-004:** Body sections: Scenario; Consequence if realised; Options
considered; Disposition rationale; Residual risk. The template carries them.

## Lifecycle (RSK-LCY)

**RSK-LCY-001:** Family `risk` in `WORKFLOW.json` with states
`identified`, `raised`, `accepted`, `avoided`, `mitigating`, `mitigated`,
`withdrawn` and the transitions of `REQ-RSK-003`. `raised` grants no
authority; terminal states are not transitionable.

**RSK-LCY-002:** `identified -> raised` is written by `raise-risk` (or by
`transition` when a score edit crosses the level) with
`decided_by = "harnessctl"` and `reason = "score S >= acceptance_level L"`.

**RSK-LCY-003:** Workflow rule `WFL-RISK-RAISED` (selector: type `risk`,
status `raised`) -> `PROC-RISK-DISPOSE` with one decision step
`STEP-RISK-DISPOSE` under `DR-RISK-DISPOSE`, outcomes `accepted`,
`avoided`, `mitigating`, `withdrawn`. `WFL-RISK-MITIGATING` ->
`PROC-RISK-MITIGATED` with one decision step, outcome `mitigated`, gated by
`QG-G4-VERIFIED-COVERAGE` over the named work orders.

**RSK-LCY-004:** `DR-RISK-DISPOSE` in `DECISION_RIGHTS.md`; the accountable
role is resolved from `[risk].stage` by the stage table. `transition`
refuses an actor whose role does not match.

## Gate predicate (RSK-GTE)

**RSK-GTE-001:** Evaluator key `undisposed_risks_threatening_scope`.
Input: the selected artifact, its governing chain, and the checkpoint. It
collects risks whose `threatens` intersects that set. `raised` fails at every
checkpoint; `mitigating` fails only for `QG-G5-RELEASE-PREPARATION` and
`QG-G5-RELEASE-DECISION`. Message: first risk ID, score, level, disposing role.

**RSK-GTE-002:** Predicates `QGP-G1-RISK`, `QGP-G2-RISK`, `QGP-G3-RISK`,
`QGP-G4I-RISK`, `QGP-G4A-RISK`, `QGP-G5P-RISK`, `QGP-G5D-RISK` appended to
their gates in `QUALITY_GATES.json`.

**RSK-GTE-003:** Corrective forms: escalation to `DR-RISK-DISPOSE` for every
`*-RISK` predicate; for `QGP-G5P-RISK` and `QGP-G5D-RISK` when the first
risk is `mitigating`, the command `harnessctl focus . --artifact <first mitigated_by WO>`.

## Commands (RSK-CMD)

**RSK-CMD-001:** `harnessctl raise-risk TARGET --domain D --id RISK-D-NNN
--title T --stage S --category C --likelihood L --impact I --threatens ID
[--threatens ID ...] [--cause TEXT] [--effect TEXT] [--raised-by TEXT]`.
Mutation guard as `create-artifact`. Output: schema-2 block; `Done` names
risk, score, level, threatened IDs; `Next` is `STEP-RISK-DISPOSE` when
raised, else `STEP-FOCUS-SELECTED`.

**RSK-CMD-002:** `harnessctl risks TARGET --artifact ID [--json]` lists every
risk threatening the artifact or its chain with status, score, stage, and
disposing role. Read-only; exit 0.

**RSK-CMD-003:** `prepare-release` derives `lists_risks` per `REQ-RSK-005`
and renders a risk table in the record body.

**RSK-CMD-004:** Scope exception in `changed_paths_within_scope`: a path
matching `docs/engineering/*/risks/RISK-*.md` whose catalog status is
`identified` or `raised` is admitted.

## Configuration (RSK-CFG)

**RSK-CFG-001:** `[risk]` in `.engineering-harness.toml`:
`acceptance_level` (integer 1..25, default 1), `scale` (`"5x5"` only),
`release_requires_disposition` (boolean, default true; false is refused in
this increment). The template installs the section with defaults; `doctor`
reports `C-RSK-001` on an invalid value.

## Traceability (RSK-TRC)

**RSK-TRC-001:** `TRC-REL-020 threatens`, `TRC-REL-021 mitigated_by`,
`TRC-REL-022 avoided_by`, `TRC-REL-023 lists_risks`, with the source/target
pairs and cardinalities of `REQ-RSK-005`; `risk` row in the applicability
table: optional per domain.

## Surfaces (RSK-SRF)

**RSK-SRF-001:** Explorer gains a risk register view; `inspect` gains a
"Risks raised" queue naming the disposing role.

**RSK-SRF-002:** Each stage procedure in `WORKFLOW.json` gains one reading
command step `STEP-<PROC>-RISKS` (`harnessctl risks . --artifact {artifact_id}`)
immediately before its first decision step.

## Failure behaviour

Every rule fails closed through validation, the mutation guard, or a gate.
No rule creates, changes, or infers a decision.
