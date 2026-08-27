+++
id = "SPEC-RSK-002"
type = "specification"
title = "Guard operation, doctor check, skill integration, and amendments for the risk artifact"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-RSK-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "technical-owner"
+++

# Specification: Guard operation, doctor check, skill integration, and amendments for the risk artifact

## Scope

Refines `SPEC-RSK-001`. Rules `RSK2-AMD-*` replace the named rules of that
specification; every other rule stands.

## Behavioral rules

**RSK2-GRD-001:** `PUBLIC_MUTATION_OPERATIONS` gains `"raise-risk"`;
`create_risk` calls `require_mutation_authority(root, operation="raise-risk")`.
The guard's identity checks are unchanged.

**RSK2-DOC-001:** `inspect_installation` adds one check `C-RSK-001` that
passes when `load_risk_policy` returns a level and fails with the reason
otherwise. `doctor` prints it like every other check; preflight surfaces it as
an `I001` installation diagnostic through the existing path.

**RSK2-SKL-001:** `harness-draft-change` and `harness-execute-work-order` gain
one procedure sentence each: a risk noticed during the procedure is one more
canonical destination in the same change plan, admitted while `identified` or
`raised`, named in the receipt, and written by the evaluator through the change
bundle; the skill never disposes a risk. Neither skill gains an evaluator
operation, an effect class, or a risk-specific admission rule of its own. The
risk path is admitted by the standing scope exception of `REQ-RSK-006` under the
existing `draft-create` and `implementation-write` effect classes, and
`guard.py` / `check_scope.py` keep their closed `ALLOWED_EFFECTS` sets, in which
a `risk-raise` effect class is refused before the evaluator is called.

**RSK2-SKL-002:** `harness-prepare-assurance` runs `harnessctl risks` for
each selected work order and includes the register in the assurance decision
packet. It does not dispose.

**RSK2-SKL-003:** The `harness-prepare-assurance` contract `version` advances
by a minor step, because a required evaluator operation is added; the other two
contracts stay byte-identical and their `version` fields do not move. The
portable-core digests in
`tests/fixtures/agentic_execution/phase4/skills/portable-vectors.json` are
regenerated, and
`tests/fixtures/agentic_execution/host_activation/expected_surfaces.json`
follows the version. The frozen Phase 3 record in
`tests/fixtures/agentic_execution/phase3/portable_vectors.json` is not
regenerated. The Claude adapters are unchanged.

**RSK2-AMD-001 (replaces RSK-ART-001 residual clause):** `residual_likelihood`
and `residual_impact` are top-level metadata fields, integers 1-5 in integer
or string form, required once `mitigated`.

**RSK2-AMD-002 (replaces RSK-LCY-002):** `identified -> raised` is set by
`raise-risk` at creation from the score and the level in force. A stored
`identified` risk whose score reaches its recorded level is `E-RSK-003`. The
transition command does not special-case the edge.

**RSK2-AMD-003 (replaces RSK-SRF-002):** The `RISKS` reading step is present
in `PROC-WO-START` and `PROC-WO-IMPLEMENT`. Decision-only procedures surface
the register through their `*-RISK` predicate message.

## Failure behaviour

Every rule fails closed through the guard, `doctor`, a skill stop condition,
or validation.

## Amendment record

**Rules RSK2-SKL-001 and RSK2-SKL-003, amended 2026-08-27 by the engineering
owner under `WO-RSK-003`.** Both rules were written against the schema-v2 skill
surface, in which a portable skill wrote governed targets itself. `WO-AEX-006`,
`WO-AEX-007` and `WO-AEX-008` replaced that surface with the schema-v3 closed
contracts of the delegated execution model, in which the evaluator owns every
governed-target write.

`RSK2-SKL-001` required an operation and an admission rule that cannot exist
under that model. Measured in `se_harness/skill_contract.py`, `_parse_v3_contract`
refuses any deviation: `SKC036` requires `client.direct_target_writes` false and
`client.target_writer` `"evaluator"`; `SKC038` requires `effects.permitted` to
equal the closed profile exactly and requires `"direct-target-write"` among the
prohibitions; `SKC035` requires the operation lists to equal the profile. The
helpers say the same thing in code: `check_scope.ALLOWED_EFFECTS` is
`{implementation-write, test-execution, evidence-write}` and
`guard.ALLOWED_EFFECTS` is `{draft-create, draft-revise, planning-note-write}`,
both closed. A `raise-risk` operation invoked from a skill's own effect plan and
a `risk-raise` permitted effect written directly by the skill are therefore
unrepresentable, not merely unfashionable. The rule now states the route the
risk write actually takes.

`RSK2-SKL-003` was wrong on three counts against what the model allows. Only
`harness-prepare-assurance` changes, because only it gains a required evaluator
operation, `risks`; the other two contracts must stay byte-identical, since a
`version` move with no contract change would be a false digest. The move is a
minor step, not a patch, because a required operation is added. And
`tests/fixtures/agentic_execution/canonical_vectors.json` no longer exists: the
live fixture is `phase4/skills/portable-vectors.json`, while
`phase3/portable_vectors.json` became a frozen historical record that
`tests/test_agentic_execution.py` pins against phase 4's own `previous` values,
so regenerating it would falsify history rather than update a fixture.

The amendment changes the mechanism and no obligation. Both skills still cause a
risk to be raised without a scope decision, by the standing exception of
`REQ-RSK-006` shipped under `WO-RSK-001`. Neither disposes, and the amendment
adds the stronger statement that neither holds a risk-raising effect class at
all. `RSK2-SKL-002` stands verbatim and is delivered exactly as approved, as do
`RSK2-GRD-001`, `RSK2-DOC-001`, `RSK2-AMD-001`, `RSK2-AMD-002`, `RSK2-AMD-003`,
the scope statement, and the failure-behaviour statement that every rule fails
closed. No rule is added, removed, renumbered, or reordered, no refusal becomes
a warning, and no waiver is introduced.

`REQ-RSK-007` and `VER-RSK-002` restate the same mechanism and were amended in
the same act, each with its own amendment record. `VER-RSK-002`'s
`RSK2-SKL-003` matrix row is unchanged: it verifies that the regenerated digests
equal `build_skill_manifest`, which is true of whichever fixture holds them.
