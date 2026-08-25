+++
id = "SPEC-AUT-001"
type = "specification"
title = "Authoring policy, requirement template, validator signals, attributes, vocabulary, and approval predicates"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-AUT-001", "REQ-AUT-002", "REQ-AUT-003", "REQ-AUT-004", "REQ-AUT-005", "REQ-AUT-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "technical-owner"
+++

# Specification: Authoring policy, requirement template, validator signals, attributes, vocabulary, and approval predicates

## Scope

Six bounded contracts over the managed policy set, the requirement template,
the validator, `create-artifact`, one skill core, and two gates. No
lifecycle state, decision right, or relation changes.

## Policy (AUT-POL)

**AUT-POL-001:** Canonical source
`templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`,
installed as `docs/engineering/ARTIFACT_AUTHORING.md`, mode `managed`,
schema-3 digest. Router row: "Authoring rules for formal artifacts".

**AUT-POL-002:** Structure: purpose and precedence (below machine contracts,
formal semantics, and the workflow, decision-right, gate, and traceability
policies; above templates, skills, and prose); one `## <type>` section per
artifact type carrying a `### Checklist` (bullets a tool can print) and
`### Guidance` (judgement rules); the requirement section carries the five
EARS shapes, the singularity rule, the vocabulary, the attributes, and the
fit-criterion guidance.

**AUT-POL-003:** `create-artifact` prints the `### Checklist` bullets of the
created type after the creation line; `--quiet` suppresses them. The
checklist is read from the installed policy, never from package text.

**AUT-POL-004:** `harness-draft-change` step 6 gains: "Apply the installed
authoring policy for each selected type; its checklist is the review
standard." Contract version advances; vectors regenerate.

**AUT-POL-005:** `REQUIRED_PATHS` and `POLICY_PATHS` include the policy.

## Statement shapes (AUT-STM)

**AUT-STM-001:** Accepted openers, after optional leading whitespace:
`THE SYSTEM SHALL`, `THE <Name> SHALL`, `WHEN `, `WHILE `, `IF `, `WHERE `.
An `IF` statement must contain ` THEN `.

**AUT-STM-002:** `W-AUT-001` opener unrecognised; `W-AUT-002` more than one
`SHALL`; `W-AUT-003` statement over 300 characters. Plane `maintenance`.

**AUT-STM-003:** The template shows the five shapes as commented lines above
`statement` and states "one obligation per requirement; split on 'and SHALL'".

## Vocabulary (AUT-VOC)

**AUT-VOC-001:** `verification_method` is an array of 1-4 distinct values
from `test`, `analysis`, `inspection`, `demonstration`; `verification_notes`
optional string.

**AUT-VOC-002:** Until `WO-AUT-002` lands, a string value is accepted with
`W-AUT-004`; after it, a string or an unknown value is `E-AUT-001` (structure).

**AUT-VOC-003:** The migration is a script under `scripts/` run once under
`WO-AUT-002`, applying the mapping of `REQ-AUT-003`, writing the original
string to `verification_notes`, and retaining the mapping table and the list
of steward decisions as evidence.

## Attributes (AUT-ATT)

**AUT-ATT-001:** Optional `priority` in `must`, `should`, `could`; `source`
non-empty string, resolved when it matches an artifact ID; `measure`
non-empty string. Invalid values are `E-AUT-002` (structure).

## Approval predicates (AUT-GTE)

**AUT-GTE-001:** Evaluator `authoring_ready`; predicates `QGP-G1-AUTHORING`
in `QG-G1-DEFINITION` and `QGP-G2-AUTHORING` in `QG-G2-ARCHITECTURE`.
Fail when the selected artifact's file contains `<[A-Za-z][^>]{2,80}>`
outside fenced or inline code, or when `## Open decisions` exists and its
first non-empty line is not `None` or `None.`.

**AUT-GTE-002:** Corrective form: response naming the first offending
placeholder or the open-decision line.

## Template (AUT-TPL)

**AUT-TPL-001:** `REQUIREMENT.template.md` body: `## Rationale`,
`## Behavior` (bullets trigger, response, on failure),
`## Assumptions and dependencies`, `## Acceptance examples` (normal and
failure, Given/When/Then), `## Open decisions`; front matter shows
`priority`, `source`, `measure` filled, `verification_method = ["test"]`,
and the five shapes commented. Under 2,500 bytes.

**AUT-TPL-002:** One sentence points executable scenarios to
`acceptance/<REQ-ID>.feature` and to the verification contract that names them.

## Failure behaviour

Warnings never block; errors and gate predicates fail closed; the policy
grants no authority.
