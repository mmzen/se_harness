+++
id = "VER-AUT-001"
type = "verification"
title = "Independent evidence for the authoring policy and requirement-writing rules"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-AUT-001", "REQ-AUT-002", "REQ-AUT-003", "REQ-AUT-004", "REQ-AUT-005", "REQ-AUT-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent evidence for the authoring policy and requirement-writing rules

## Independence

Expected values derive from the six requirements and `SPEC-AUT-001`;
fixtures are written from the specification. Reviewers judge the policy's
guidance sections against the template review's findings.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-AUT-001` | install, lock, router, preflight, create-artifact, skill vector tests | fresh install; customised policy; `create-artifact` with and without `--quiet`; draft-change contract | one managed policy, routed once, listed, checklist printed from the installed file, skill vectors match |
| `REQ-AUT-002` | validator tests over a statement corpus | five valid shapes; unknown opener; two `SHALL`s; 301 characters; no `SHALL` | exact warning or error per case; existing corpus produces warnings only |
| `REQ-AUT-003` | validator and migration tests | array values; string value before and after migration; unknown value; mapping table over the repository's 110 values | `W-AUT-004` then `E-AUT-001`; every value mapped or listed; originals preserved in notes |
| `REQ-AUT-004` | validator tests | valid and invalid `priority`; `source` as text and as a resolving or unknown ID; `measure` | `E-AUT-002` on invalid; absence silent |
| `REQ-AUT-005` | gate tests | placeholder in title, in body, in code span; open decisions `None`, `None.`, prose, absent | predicate outcomes per case; corrective response names the offender |
| `REQ-AUT-006` | template tests | rendered template | six headings, five shapes, attributes, `acceptance/` sentence, under 2,500 bytes |

## Acceptance scenarios

1. Fresh install; `create-artifact --type requirement`; checklist printed; the draft validates with warnings only for its placeholders.
2. Write one requirement per EARS shape; all validate clean.
3. Paste `REQ-AEX-008`'s statement; `W-AUT-002` and `W-AUT-003` fire.
4. Approve a draft with a placeholder; `QGP-G1-AUTHORING` fails naming it.
5. Run the migration on a copy of this repository; 255 requirements re-validate with 0 errors; the steward-decision list is reviewed.
6. Reviewers read the policy's requirement section against the template review and confirm each finding is addressed or explicitly deferred.

## Pass criteria

All deterministic tests pass on Windows and Linux; released-evaluator validation 0 errors; Scenario 6 has no unaddressed finding.
