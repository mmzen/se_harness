# WO-REB-015 Windows candidate-test temp evidence

## Hosted failure retained

Publication run `32598732033`, qualification job `97093696145`, passed authority resolution, Windows Python 3.11.9 selection, exact candidate export, and C6 current validation at 645 artifacts with zero errors. The complete suite then reported three failures and four errors, all caused by the same Windows runner alias split: temporary paths were created under lexical `C:\Users\RUNNER~1` while Python resolved them under `C:\Users\runneradmin`. Representative failures were repository-relative comparisons, evaluator executable identity, and binder path equality. The build and every downstream privileged job remained skipped.

The correction creates a dedicated directory beneath normalized `D:\a\_temp`, converts that path once to native Windows form, and exports identical `TEMP` and `TMP` values before test execution. It neither changes nor filters the complete C6 suite.

## Corrective qualification

Corrective candidate `e51c0adb8eded412d78771a771980efc86194e6a` contains exactly four paths: the trusted workflow, its regression test, `WO-REB-015`, and this evidence. The stopped untracked `RLS-SEH-008` is absent. The complete C6 test command remains unchanged; the workflow adds only a dedicated long-path temporary directory and identical `TEMP`/`TMP` exports before tool installation and test execution.

A clean exact-commit clone produced these results:

- focused release-workflow policy: 5 tests passed;
- complete release-orchestration module: 22 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 219.853 seconds;
- complete current-semantics graph: 667 artifacts, zero errors, 50 maintenance warnings;
- exact released-distribution validation: passed with one distribution-bearing record;
- portable release surface, diff whitespace, and clean-checkout checks: passed.

At closeout C6 `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, `v0.6.0`, released `RLS-SEH-012`, distribution bytes, rejected history, the schema-2 root evaluator, and external policy remain unchanged. No publication credential, GitHub Release, PyPI file, Pages deployment, maintenance-line mutation, tag movement, root mutation, or distribution replacement occurred. A later commit-bound VREC must be accepted before this correction is pushed and publication resumes.
