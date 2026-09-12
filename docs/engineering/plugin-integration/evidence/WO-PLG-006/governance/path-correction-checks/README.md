# Required checks after the path correction

`commands.json` records exact invocations, working directory, exits and durations;
the named stdout/stderr files retain each result. Candidate source runs use the
base Python interpreter. Governing runs use released 0.17.0 outside the checkout.

- Candidate CLI help: exit 0.
- Candidate graph validation: exit 0.
- Release-distribution provenance: exit 0, fourteen distribution-bearing records.
- Released doctor: exit 0; managed copies remain intact.
- Released review preflight for WO-PLG-006: exit 0, ready, in_progress, no skew.
- Candidate doctor: exit 1. Candidate version 0.18.0 differs from the root's
  released 0.17.0 templates in six distribution checks. This is the candidate
  versus released boundary documented in AGENTS.md, not permission to modify
  managed copies. The complete failed result remains retained.

The seventeen focused guard/capture tests passed in
`../../path-validation/focused-tests.json`. The current native acceptance is
`../../acceptance-06/`. Broader source/upgrade CI remains owned by the parent;
the full regression suite was not duplicated during this acceptance collection.

The released handoff evidence/check results are retained alongside these checks.
They do not change lifecycle state or qualify the failed C10/C11 routes. Any live
GitHub gate result describes its recorded head only; the later evidence commit
requires its own CI before any delegated lifecycle operation.

Handoff evidence generation and handoff check against origin/main both exited
0. The read-only live check saw validate success for source head fd2419f4,
check-run 103403625697, and kept WO-PLG-006 in_progress. Its suggested
DR-WO-COMPLETE transition is retained verbatim in the structured result and was
not executed. Engineering disposition of the failed routes remains with the
parent and accountable owner; later evidence changes require fresh head CI.

The parent also retained all seventeen CI checks passing at source fd2419f4,
including candidate source/package, Linux and Windows upgrade rehearsal and
integration-package verification. `source-ci-result.json`, `source-ci-checks.json`
and `source-ci-pull.json` are scoped copies of that inspected capture; they name
the exact head and job links. Full original job logs remain in the parent's
external `corrected-guard-ci-01` control capture. These successes do not erase
the earlier 26f32349 Linux cleanup failure or establish CI for this later
evidence-only commit. No cleanup policy was changed or failure waived.
