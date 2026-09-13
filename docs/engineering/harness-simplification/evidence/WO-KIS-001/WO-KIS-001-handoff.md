```toml
artifact = "WO-KIS-001"
checkpoint = "handoff"
formal_snapshot_sha256 = "6b1d14f476fd574bc415375396c080a174adca71340241dd0308c4e9aae96c65"
rebound_at = "2026-09-13T17:35:53Z"
```

# WO-KIS-001 implementation evidence

Tested source commit: `4793c7bb95ff718d0b05c6de7c1c585e477e445c`. Governing checker: isolated released 0.17.0.
This record covers the first eight cuts only. The work order is in progress; assurance is not yet verified.

| Check | Observation | Evidence |
| --- | --- | --- |
| K01 | LF and CRLF select the same work order in the installed CLI; duplicates and malformed IDs still fail in the source suite. | test_lf_and_crlf_pr_fields_select_the_same_values |
| K02 | Owner text over 6,000 bytes works with LF and CRLF; a damaged managed marker fails doctor. | test_large_owner_instructions_accept_both_line_endings_and_preserve_markers |
| K03 | Literal brackets work through Git and the native CLI path; real traversal and Git-reported escapes fail. | OrdinaryInputsTests and existing scope tests |
| K07 | A top-level evidence_paths reference works through the public handoff command without a header; missing files fail. Descriptive header text survives rebinding. | OrdinaryInputsTests |
| K11 | Selected-artifact projections give actions for draft, approved and implemented work; pre-action now selects its procedure automatically. | test_workflow_execution.py projections and test_pre_action_selects_the_procedure_and_rejects_unrelated_override |
| K35 | A plain statement and the older SHALL form both validate; an empty statement or missing acceptance content fails. | test_plain_requirement_and_old_shall_form_both_validate and SimpleAuthoringTests |
| K36 | Long prose and ordinary capability wording can be approved; hints do not block the owner. Placeholders and explicit blocking decisions still fail. | SimpleAuthoringTests and decision-management tests |
| K37 | Installed raise-risk creates a valid note from description, action and owner alone. Optional scored decisions and existing dispositions retain their tests. | test_risk_management.py and package-risk.json |

Source regression: **1,179 tests run, 25 skipped, pass** on Windows/Python 3.14.
The command was `python scripts/run_tests.py --workers 4 --timings ../work/kis001-committed-timings.json`.
The recorded 132.539 seconds is this run's duration, not a measured speedup.

The non-promotable wheel was built from a Git export of the exact commit and installed
outside the checkout into a disposable Python 3.12 environment. Identity, init, a risk
without scores/decision, graph validation, doctor, and LF/CRLF PR selection all passed.
Wheel SHA-256: `cdce471420afa9f47750c967af8c86e31339cabf7a2e53928e715b82efe1e22b`. This wheel is not a release artifact.

Released doctor, released graph and review preflight passed. The graph contains 1,596
artifacts, zero errors and 46 existing layout warnings. Distribution validation passed
for 14 distribution-bearing records; CLI help passed. Candidate-source doctor reports
the expected 0.18.0-template versus installed 0.17.0-root skew; the isolated governing
doctor is the authority and passed. No installed root copy was changed.

Source changes: 168 lines added, 729 removed.
Tests: 212 lines added, 708 removed;
the changed modules contain 273 test methods instead of 299.
The authoring checker went from 543
to 124 lines.

Retained boundaries: outside-root refusals, managed-fragment checks, atomic writes and
risk/decision rollback tests, package hashes, explicit decisions and effective checker
identity. Workflow permissions were not changed. Historical VREC/RLS records were not edited.

The full source run initially exposed obsolete style/CRLF expectations, a missing input-code
import and a root/candidate documentation comparison. Those were corrected before the
committed run above. Tests enforcing the removed restrictions were deleted or updated,
not disabled. Local Windows checks are complete; Ubuntu and hosted integration results
will be recorded from CI. No assurance or release decision is claimed here.
