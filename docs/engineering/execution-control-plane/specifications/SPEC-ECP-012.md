+++
id = "SPEC-ECP-012"
type = "specification"
title = "Admission of the selected work order's own records to the change set"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T11:40:51Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-29 with the words 'Approve and start WO-ECP-016': ECP-ADM-001 to ECP-ADM-005, exact-path admission by relation, extending ECP-CHG-007 by the amendment record on SPEC-ECP-001."
+++

# Specification: Admission of the selected work order's own records to the change set

## Scope

The admitted scope that `build_context` assembles for a selected work order
(`ECP-CHG-007`, `ECP-PRB-002`) gains the records that name the work order.
`SPEC-ECP-001`'s `ECP-CHG-007` is amended by record to cite this rule.
Issue #264.

## Terms

- **Own record:** a verification record whose `verifies_work_order`
  contains the selected work order's identifier, or a release record whose
  `releases_work` contains it.
- **Admitted scope:** the tuple `QGP-G4I-PATHS` judges paths against:
  declared paths, then the constructions of `ECP-CHG-007`, `ECP-PRB-002`
  and this specification.

## Behavioral rules

**ECP-ADM-001:** For a selected work order, `build_context` adds to the
admitted scope the catalog path of every own record and, for each, the
path its `evaluator_evidence_path` names when the record declares one,
each as an exact path (never a directory prefix).

**ECP-ADM-002:** Admission is by relation, not by directory: a record under
`verification-records/` or `releases/` that does not name the selected work
order, and any other file there, is judged against the declared paths as
today; a conformance test asserts a record for another work order fails
`QGP-G4I-PATHS` with `WEX201` in the same diff that admits the own record.

**ECP-ADM-003:** The construction applies at every checkpoint that
evaluates the change set (`handoff`, `scope`, `pre-action` with a change
set) and to every change-set source (`--from-git`, typed paths, manifest).

**ECP-ADM-004:** `scope.declared_paths` in the result is unchanged; the
admitted paths are not reported as declared.

**ECP-ADM-005:** `docs/notes/harnessctl-check.md` states the construction
where it states the work order's own file and evidence directory are
admitted.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-023 | ECP-ADM-001 to ECP-ADM-005 |

## Failure behaviour

A record the catalog cannot parse admits nothing (it is already a graph
error that blocks the check); a record whose `evaluator_evidence_path` is
absent admits only its own file. No lifecycle state, gate, digest preimage
or refusal changes.

## Compatibility and migration

No contract file changes; consumers receive the rule with the evaluator.
A work order that listed a records directory to pre-empt the gate keeps
working; it may stop listing it.
