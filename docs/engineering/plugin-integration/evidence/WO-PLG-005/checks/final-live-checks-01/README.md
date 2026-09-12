# Final local checks

The focused adapter suite passes all 143 tests. Candidate help, graph validation,
release-distribution records and released 0.17 graph, doctor and preflight checks
pass. `results.json` records exact commands, durations and output digests.

`doctor-assessment.json` confirms candidate doctor failed only for the six
expected candidate-versus-released template differences. Managed integrity
passes under the governing released evaluator.

The separate [complete regression](../final-regression-01/result.json) passes
1,159 tests with 23 skips (183 classes, 8 workers). Its stderr retains the expected
`--workers must be at least 1` diagnostic emitted by a negative runner test.

These are repository checks, not native-hook qualification or assurance. The
source-input manifest still matches every adapter and test file at completion.
