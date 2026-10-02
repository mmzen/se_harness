+++
id = "VER-KIS-004"
type = "verification"
title = "Verify complete scope preparation before approval"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
verifies = ["REQ-KIS-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T11:41:55Z"
decided_by = "mmzen"
reason = "mmzen approved the package published for review in PR #523 with \"Ok i approve\". This approves VER-KIS-004 at reviewed SHA-256 8ec7905235cf9de1b005bd1c0961a933d78d755291c7d0c62af48300175b4fd3, including required commit-bound verification under VER-KIS-004 and bounded local execution under WO-KIS-010. Pending assurance fields were completed from this decision. Verification acceptance and implementation publication remain separate."
+++

# Verify complete scope preparation before approval

## Independence

Expected results come from REQ-KIS-010 and SPEC-KIS-004. Write fixtures with
independently listed planned paths and expected admission reasons. Do not
derive expected coverage by calling the candidate matcher. Reuse existing
scope, lifecycle and fixture helpers where they preserve independent
expectations. Candidate tests exercise future behavior; released evaluator
0.21.0 continues to govern the real repository.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-010 | test | A: planned paths | Exact files, component children and missing future files are classified correctly; sibling lookalikes and omitted files are uncovered. Each match names its reason. |
| REQ-KIS-010 | test | B: automatic outputs | The selected WO file, directly linked VREC/RLS and evaluator evidence are admitted by existing rules; unrelated records and neighboring evidence are not. |
| REQ-KIS-010 | test | C: refusal and invariants | Invalid paths, case duplicates, escapes, conflicting flags and invalid selection are rejected or reported invalid without writes. No plan becomes an actual diff, gate result or approval. |
| REQ-KIS-010 | test | D: compatibility and integrity | Existing commands retain their meaning and result shape when the option is absent; planning data participates in the digest; one repository validation is reused. |
| REQ-KIS-010 | inspection | E: instructions and request | Discovery, reasons, unknown generated destinations and the plain-language decision card appear at the existing preparation/approval entry points without duplicate policy or extra artifact types. |
| REQ-KIS-010 | demonstration | F: complete outcomes | A bug fix and an instruction change each reach verification preparation in temporary fixture repositories under one unchanged WO; a deliberately omitted planned path is caught before approval and a later real expansion requires a decision. |

## Execution conditions

Run A-D through the public CLI in temporary fixture repositories, including
a draft WO and an approved WO. Check human and JSON output. Snapshot fixture
files before and after read-only assessments. Assert no lifecycle events,
evidence files or Git changes are written. Supply an explicit WO and test
the failure of missing, unknown and non-WO selections.

For B, include an unrelated record and a linked record with its concrete
evaluator-evidence path. A future unallocated record is an explained
uncertainty, not a synthetic admitted path. Test explicit evidence files
separately. Keep existing start, scope and handoff regression tests so that
planning cannot weaken real execution checks.

For C, cover absolute paths, parent traversal, case-duplicate inputs, a
component-prefix lookalike and a repository escape through a link. Exercise
mixed planned and actual change-set flags. Where Windows cannot create a
link without privileges, retain the explicit skip and exercise that case
on Linux CI. Never convert a skipped check to a pass.

For D, compare projection without the option with the same selection using
the option. Lifecycle state, next action, gate status and actual change-set
fields remain unchanged. Change only one planned path or its classification
and confirm the result digest changes. Use the existing one-validation test
to prevent another full graph pass for the additional view.

For E, review the released-resource sources, WO template, CLI reference and
their discovery tests. The request must let a reader identify the outcome,
scope, checks, uncertainty and permission without reading IDs or commands.
Exact definitions, WO, VER and reviewed revisions remain linked. This is
an inspection judgement, not a claimed usability score.

For F, use two small temporary repositories with independently recorded
expected file lists. One models a bug fix with a caller, test and fixture.
The other models an instruction, template, documentation and contract test.
Use fixture-only decisions and candidate CLI transitions; never apply
simulated human approval to real records. Retain the starting plan, coverage
output, actual change set, handoff and prepared record for each example.
Both examples must retain the same WO identity and approved scope through
preparation of the VREC. Also show that a proposed extra file is caught before
approval and a genuinely new later change cannot rely on the old scope.

## Commands and platforms

Run the focused modules selected by the implementation in
tests/test_scope_preparation.py, tests/test_cli_shape.py,
tests/test_workflow_execution.py, tests/test_workflow_compliance.py,
tests/test_workflow_restitution.py and tests/test_one_validation.py.
Run the affected authoring and instruction-discovery tests.

Then run python scripts/run_tests.py and the repository distribution checks
after reading their required release-sequence prerequisites. Check CLI help.
Use local Windows and the existing Linux/Windows CI at integration. Local
results do not establish CI success. External model calls, host login and
desktop interaction are not needed for these deterministic checks.

Use the exact selected released evaluator for real validate, doctor,
start/review/handoff checks and commit-bound verification capture. Candidate
source is limited to development tests and isolated demonstrations.

## Evidence retention

Retain commands, input lists, expected and observed results, exit codes,
platforms, skips and the exact candidate commit in the selected WO's evidence
directory. Keep one ordinary review covering requirements, scope, generated
outputs and remaining uncertainty. Do not create a separate benchmark or
planning receipt framework. Capture the VREC through the released evaluator
against the exact clean candidate; its actual ID is allocated later.

## Residual uncertainty

Passing two representative cases does not prove exhaustive impact analysis
or a measured reduction in interruptions across all work. The human still
reviews semantic scope and real expansion. The installed evaluator and
plugin will acquire this behavior only through a later release and adoption.
