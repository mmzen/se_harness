+++
id = "VER-AUT-004"
type = "verification"
title = "Independent evidence for the closed compatibility windows"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[relations]
verifies = ["REQ-AUT-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T17:21:18Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-09 by the accountable owner by selecting the presented option 'Approve all four (Recommended)', given after the packet closing the compatibility windows (issue #381 owner decision 3 of 2026-09-07, migrate the corpus then close; SPEC-AUT-003 AUT-MIG-012) was presented on pull request #423 with the released 0.16.0 evaluator reading 0 errors and 0 authoring advisories. Approval of a definition authorizes no work. The retired-relation, unassessed-architecture, dashboard, header-less packet, v1 schema, registry, permanent-branch, amendment, notes, baseline, scope, regression and delegation rows."
+++

# Verification Contract: Independent evidence for the closed compatibility windows

## Independence

Expected values come from `REQ-AUT-009` and the rules of `SPEC-AUT-004`,
never from the diff. Every refusal is exercised on a scratch fixture built
by the test, not on this corpus. The baseline is the released 0.16.0
evaluator's reading of `main` at the work order's base, taken before the
change; the candidate's reading of the same tree is compared against it,
count by count. The candidate suite runs on the hosted Linux lane; the local
Windows suite is a control, not the record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-AUT-009` retired relation | test | an approved and an implemented architecture with `constrains` in a fixture (AUT-WIN-001, AUT-WIN-002) | `validate` reports `E016` naming the retired relation for both; no `W015` anywhere in the report |
| `REQ-AUT-009` unassessed architecture | test | an implemented architecture without `[decision_assessment]` (AUT-WIN-003 to AUT-WIN-005) | `validate` reports `E014`; the preflight prints no `W019`; an `adr_required` architecture without a deciding ADR still reads `E015` |
| `REQ-AUT-009` dashboard | test | the snapshot of a fixture with a typed architecture (AUT-WIN-006) | no `legacy_` assessment state is produced; the relation set holds `addresses` and `conforms_to` only |
| `REQ-AUT-009` header-less packet | test | a packet carrying only the substring lines (AUT-WIN-007, AUT-WIN-008) | `QGP-G4I-EVIDENCE` is `not_assessable`, the message names `harnessctl evidence`, no `W-ECP-002` in the result |
| `REQ-AUT-009` v1 schema | test | a `quality_gates_contract.json` copy with `se-harness-quality-gates-v1` (AUT-WIN-009, AUT-WIN-010) | the loader raises its own schema error; `WEX-ECP-030` is still raised for a missing transition binding |
| `REQ-AUT-009` registry | test | `se_harness/codes.py` and the index (AUT-WIN-011) | none of `W014`, `W015`, `W019`, `W-ECP-002` in the module or the page; `E014`, `E015`, `E016`, `WEX-ECP-030` present; `--check` of the index passes |
| `REQ-AUT-009` permanent branches | inspection | the two branches and the note (AUT-WIN-012) | each branch carries a comment naming it permanent; the note states the two counts measured at the base |
| `REQ-AUT-009` amendments | inspection | the four specifications (AUT-WIN-013) | each carries an amendment record naming `WO-AUT-006`; rule identifiers, statements and relations unchanged against `main` |
| `REQ-AUT-009` notes | inspection | `harnessctl-reference.md`, `diagnostic-codes.md` (AUT-WIN-014) | the grace sentence is gone; the index equals the source |
| `REQ-AUT-009` baseline | the released 0.16.0 evaluator and the candidate on the same tree | (AUT-WIN-016) | both read 0 errors and the same counts per code; the candidate reports none of the four codes |
| `REQ-AUT-009` scope | the handoff check over the Git-derived change set | (AUT-WIN-017, AUT-WIN-018) | only the paths the rule allows; no managed template, no root managed byte, no corpus artifact |
| all | regression | the full suite, `validate`, `doctor`, the hosted lanes | failure set at the baseline on Linux and Windows; managed set untouched; every lane green at the head |
| all | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Acceptance scenarios

- In a scratch worktree at the bound commit, add `constrains = ["REQ-…"]`
  to an approved architecture of this corpus: `validate` reports `E016`
  naming the file and the relation.
- In the same worktree, delete the `[decision_assessment]` table of an
  implemented architecture: `validate` reports `E014` naming the file; the
  preflight for a work order selecting it prints no `W019`.
- Rewrite a retained handoff packet's header into the three substring
  lines: the handoff check reports `QGP-G4I-EVIDENCE` `not_assessable` and
  names `harnessctl evidence`.
- Copy `quality_gates_contract.json` with its schema set to
  `se-harness-quality-gates-v1`: the loader raises its schema error, not a
  hint.
- Restore the `W015` branch in a scratch copy: the traceability test fails
  naming the code.

## Evidence retention

`docs/engineering/artifact-authoring/evidence/WO-AUT-006/`: the baseline
and candidate `validate` readings count by count, the scenario outputs, the
code inventory before and after, the two measured counts, the suite
readings labelled hosted and local, and the handoff check result.

## Pass criteria

Every row of the matrix passes on the hosted Linux lane and on the Windows
workstation; the released 0.16.0 evaluator reports 0 errors on the
candidate; the pull request's lanes are green through completion and the
record head; no managed template, root managed byte or corpus artifact
changes.

## Residual uncertainty

This repository's root evaluator is released 0.16.0 and keeps the windows
until the root adoption of the carrying release; the closed branches are
exercised by the candidate's tests and scratch scenarios, not by a live
consumer whose corpus still holds a legacy shape. The first such consumer
reads `E016` or `E014` at its upgrade, which is the intended refusal. The
Windows baseline carries the two known failures recorded under `WO-TST-004`.
