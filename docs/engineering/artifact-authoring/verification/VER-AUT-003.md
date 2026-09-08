+++
id = "VER-AUT-003"
type = "verification"
title = "Independent evidence for the corpus migration"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-AUT-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:58:19Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. The relations, assessments, amendments, vocabulary, retirement, windows, scope and regression rows."
+++

# Verification Contract: Independent evidence for the corpus migration

## Independence

Expected values come from `REQ-AUT-008`, the rules of `SPEC-AUT-003` and the
counts measured on `main` at `a68caf70`: 15 architectures with `constrains`,
14 without an assessment, 271 requirements with a string method, 4 of them
unmappable. The released 0.16.0 evaluator's `validate` is the oracle for
the windows; a front-matter scan independent of the script is the oracle for
the vocabulary; the deciding ADRs are read from the catalog, not from the
migrated files.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-AUT-008` relations | test: front-matter scan of every architecture | no `constrains`; every former requirement target in `addresses`, every former specification target in `conforms_to`; every addressed requirement specified by a named conforming specification (AUT-MIG-001, AUT-MIG-002) |
| `REQ-AUT-008` assessments | test: front-matter scan | every completed architecture carries a valid assessment; each `adr_required` one names an active deciding ADR in its rationale (AUT-MIG-003) |
| `REQ-AUT-008` amendments | inspection of the fifteen files | an amendment record naming `WO-AUT-005`, `updated` bumped, title, status, statement and ADR relations unchanged against `main` (AUT-MIG-004) |
| `REQ-AUT-008` vocabulary | test: front-matter scan of every requirement | every `verification_method` is a non-empty array from the four words; every migrated requirement carries `verification_notes`; the four steward decisions read `["test"]` (AUT-MIG-005 to AUT-MIG-007) |
| `REQ-AUT-008` retirement | test | the script, its test and the note paragraph are absent; `SPEC-AUT-001` carries the amendment record (AUT-MIG-007, AUT-MIG-008) |
| `REQ-AUT-008` windows | the released 0.16.0 evaluator's `validate` on the candidate | 0 errors; `W014` 0 and `W015` 0; every other code's count equals the baseline reading (AUT-MIG-010) |
| `REQ-AUT-008` scope | the handoff check over the Git-derived change set | only the paths `AUT-MIG-011` allows; no product module changed (AUT-MIG-011, AUT-MIG-012) |
| `REQ-AUT-008` regression | the full suite; `doctor`; the hosted lanes | failure set equals the baseline on Windows and Linux; managed set untouched; every lane green |

## Acceptance scenarios

- Record the validator's per-code counts on `main` and on the candidate in
  the evidence; the difference is exactly `W014` −14 and `W015` −15.
- Keep one architecture's `constrains` in a scratch copy: `W015` names it
  and the corpus test fails.
- Give one assessment an unknown trigger in a scratch copy: `E014` names it.
- Run the script twice before deleting it: the second run reports 0 mapped
  and writes nothing.

## Evidence retention

One evidence packet under
`docs/engineering/artifact-authoring/evidence/WO-AUT-005/` holding the
per-code counts before and after, the script's mapping report, the four
steward decisions with their reasons, the list of migrated files, and the
`validate` and `doctor` readings.

## Pass criteria

Every row passes on the Windows workstation and the hosted Linux lane; the
released 0.16.0 evaluator's `validate` reports 0 errors and no `W014` or
`W015`; the pull request's lanes are green through completion and the record
head; no product module and no managed path changes.

## Residual uncertainty

The retroactive assessments record the technical owner's judgement of
decisions taken weeks ago; the deciding ADRs are the evidence for each. The
Windows baseline carries the two known failures recorded under `WO-TST-004`.
The windows themselves stay open in the validator until the following work
order closes them.
