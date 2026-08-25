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

**RSK2-SKL-001:** `harness-draft-change` and `harness-execute-work-order`
gain `raise-risk` in their `required_operations` and one procedure sentence
each: a risk noticed during the procedure is raised with `raise-risk` and
reported in the receipt; the skill never disposes. Their `guard.py` /
`check_scope.py` admit `docs/engineering/*/risks/RISK-*.md` as an effect path
for a new `identified` or `raised` risk only.

**RSK2-SKL-002:** `harness-prepare-assurance` runs `harnessctl risks` for
each selected work order and includes the register in the assurance decision
packet. It does not dispose.

**RSK2-SKL-003:** Contract `version` fields advance (patch); the portable-core
manifests in `tests/fixtures/agentic_execution/canonical_vectors.json` are
regenerated; the Claude adapters are unchanged.

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
