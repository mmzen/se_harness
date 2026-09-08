# Repository checks

These are repository integrity and distribution-metadata checks. They do not execute the host acceptance cases or make an assurance decision.

- `independent-readonly-validate.json`: released 0.16.0 graph validation.
- `independent-readonly-doctor.json`: released 0.16.0 managed integrity.
- `independent-candidate-help.*`: candidate source CLI help.
- `independent-release-distributions.*`: existing distribution-record validation; no build.

The released evaluator was invoked from outside the checkout with `-I` and the checkout's absolute path. Candidate-source checks used `-B -S`, as recorded in their command files. A `post-sync-readonly-*` result, when present, is the fresh reading after synchronizing the stacked PR base; the earlier reading is retained.

Observed results: graph validation has zero errors and 44 pre-existing warnings; doctor passes 97 checks; CLI help and validation of 13 distribution-bearing records both exit 0. Focused fixture tests are retained separately.
