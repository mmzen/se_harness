# Initial focused-test observation

Command: python -B -m unittest tests.test_scope_preparation -v

Observed: 9 tests; 1 failure and 1 skipped test. The release-output test
expected the linked release record and its evaluator path in automatic_matches.
The fixture accidentally declared evaluator_evidence_path twice, so the
record did not enter the parsed catalog. The correction replaces its existing
value instead of inserting a duplicate. Product admission behavior was not
changed to admit malformed records.

The Windows symlink test was skipped with WinError 1314 (missing privilege).
The original output is also retained in this task's tool transcript.
