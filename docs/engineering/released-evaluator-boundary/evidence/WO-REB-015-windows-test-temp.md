# WO-REB-015 Windows candidate-test temp evidence

## Hosted failure retained

Publication run `32598732033`, qualification job `97093696145`, passed authority resolution, Windows Python 3.11.9 selection, exact candidate export, and C6 current validation at 645 artifacts with zero errors. The complete suite then reported three failures and four errors, all caused by the same Windows runner alias split: temporary paths were created under lexical `C:\Users\RUNNER~1` while Python resolved them under `C:\Users\runneradmin`. Representative failures were repository-relative comparisons, evaluator executable identity, and binder path equality. The build and every downstream privileged job remained skipped.

The correction creates a dedicated directory beneath normalized `D:\a\_temp`, converts that path once to native Windows form, and exports identical `TEMP` and `TMP` values before test execution. It neither changes nor filters the complete C6 suite.

## Corrective qualification

Pending exact implementation-candidate qualification and commit-bound verification.
