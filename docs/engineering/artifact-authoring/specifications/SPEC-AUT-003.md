+++
id = "SPEC-AUT-003"
type = "specification"
title = "Corpus migration: typed architecture relations, decision assessments, the vocabulary verification method"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Every legacy architecture gains typed relations and a decision assessment, every requirement a vocabulary verification method, and the one-shot migration script leaves the repository."

[relations]
specifies = ["REQ-AUT-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:58:19Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. Rules AUT-MIG-001 to AUT-MIG-012."
+++

# Specification: Corpus migration: typed architecture relations, decision assessments, the vocabulary verification method

## In plain words

One work order rewrites the front matter of fifteen architectures and two
hundred and seventy-one requirements. Three validator windows then have
nothing left to tolerate, and the script that did one of the rewrites is
deleted.

## Scope

The formal artifacts under `docs/engineering/` that the three windows
tolerate, measured on `main` at `a68caf70`; the migration script and its test;
`SPEC-AUT-001` rule `AUT-VOC-003`. Closing the windows in the validator is a
later work order under issue #381, not this one.

## Terms

- **Legacy architecture.** An `implemented` architecture whose relations
  carry `constrains`, the relation the typed pair `addresses` and
  `conforms_to` replaced under `WO-IAR-005`.
- **Deciding ADR.** The active ADR whose `decides` names the architecture.
- **Steward decision.** The mapping of a verification-method string the
  script cannot map, recorded in the evidence with its reason.

## Rules

**AUT-MIG-001.** For each legacy architecture, requirement targets of
`constrains` MUST move to `addresses`, specification targets to
`conforms_to`, and `constrains` MUST be removed.

**AUT-MIG-002.** `conforms_to` MUST also name every active specification that
specifies an addressed requirement, so that no addressed requirement lacks a
conforming specification.

**AUT-MIG-003.** Each completed architecture without `[decision_assessment]`
MUST gain one with `outcome = "adr_required"`, triggers from the controlled
vocabulary matching its deciding ADR, a rationale naming that ADR, and
`assessed_by = "technical-owner"`.

**AUT-MIG-004.** Every migrated architecture MUST carry an amendment record
naming this work order and a bumped `updated`; its title, status, statement
and ADR relations MUST NOT change.

**AUT-MIG-005.** `scripts/migrate_verification_methods.py --apply` MUST be run
once on the checkout; each rewritten requirement carries the array and
`verification_notes` with the original string.

**AUT-MIG-006.** The four values the script cannot map MUST be set to
`["test"]` with the original in `verification_notes`, as steward decisions
recorded in the evidence: `REQ-REB-004`, `REQ-REB-011`, `REQ-REB-014`,
`REQ-REB-018`.

**AUT-MIG-007.** After the run, no requirement MAY hold a string
`verification_method`; the script, its test in
`tests/test_artifact_authoring_policy.py` and the note paragraph in
`docs/notes/artifact-authoring.md` MUST be deleted.

**AUT-MIG-008.** `SPEC-AUT-001` MUST be amended by record: `AUT-VOC-003`'s
migration ran under this work order, with the mapping table and the steward
decisions retained in its evidence.

**AUT-MIG-009.** A test MUST assert that no architecture carries
`constrains`, that every completed architecture carries a valid
`[decision_assessment]`, and that no requirement holds a string
`verification_method`.

**AUT-MIG-010.** The released 0.16.0 evaluator's `validate` on the candidate
MUST report 0 errors and no `W014` or `W015`; every other diagnostic count
MUST equal the baseline.

**AUT-MIG-011.** The change set MUST hold only the migrated artifacts, the
deleted script and its test, the note, `SPEC-AUT-001`, this packet, the
domain index and the evidence.

**AUT-MIG-012.** Closing the `W014` and `W015` branches, the `W-ECP-002`
grace and the `WEX-ECP-030` hint, and documenting the `prepared_at` and
`execution_scope` branches as permanent, is a following work order and MUST
NOT be done here.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| an addressed requirement has no conforming specification | the validator refuses the architecture; the work stops and escalates | `E016` |
| an assessment names a trigger outside the vocabulary or no trigger | the validator refuses | `E014` |
| a requirement's front matter cannot be parsed | the script refuses the file and writes nothing | exit 2 |
| a string value survives the run | the corpus test names the file | test failure |
| the script or its test survives | the retired-surface reading names the path | test failure |

## Examples

**Given** `ARCH-DST-001` with `constrains = ["REQ-DST-001", …,
"REQ-DST-006"]`, **when** migrated, **then** it carries `addresses` with the
six requirements, `conforms_to = ["SPEC-DST-001"]`, an assessment naming
`ADR-DST-001`, and no `constrains` (AUT-MIG-001 to AUT-MIG-004).

**Given** `REQ-REB-004` with `verification_method =
"automated-active-surface-invariant"`, **when** migrated, **then** it carries
`["test"]` and the original string in `verification_notes` (AUT-MIG-006).

**Given** the candidate, **when** the released evaluator validates it,
**then** the maintenance plane holds no `W014` or `W015` (AUT-MIG-010).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-AUT-008` | AUT-MIG-001, AUT-MIG-002, AUT-MIG-003, AUT-MIG-004, AUT-MIG-005, AUT-MIG-006, AUT-MIG-007, AUT-MIG-008, AUT-MIG-009, AUT-MIG-010, AUT-MIG-011, AUT-MIG-012 |

## Not decided here

- The exact triggers chosen per architecture from the controlled
  vocabulary, read from each deciding ADR's context and drivers.
- The wording of the fifteen amendment records and of the rationale
  sentences.
- Whether the corpus test lives in `test_architecture_traceability.py`,
  `test_artifact_authoring_policy.py` or a new module.
- The order in which the two rewrites are committed.
