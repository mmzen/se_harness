# WO-REB-009 candidate-validator evidence

## Failure retained

Authorized publication run `32594814369` resolved released `RLS-SEH-012` and passed the exact predecessor publication-view adapter. Credential-free qualification job `97084046727` then exported immutable C6 twice and stopped before building or transferring distributions because this command ran inside the archive:

```text
python scripts/validate_engineering_artifacts.py --root .
```

The script is the separately locked released-0.5 root evaluator. It reported 645 artifacts, exact E009 for rejected `RLS-SEH-009`, 47 warnings, and no other error. GitHub Release, PyPI, Pages, maintenance, tag, distribution, root, and policy mutation jobs did not run. Retained release-result artifact `9481271739` has digest `sha256:fd8e7d323e2d698e3f7cd27ad82793c3675c1e280d9169531c6c697823f36dbf`; release-plan artifact `9481266280` has digest `sha256:5eb1f7282bb90307ddee2313d1479bb9febafc6d796da3e42303b018c772372b`.

## Semantic correction

The qualification job already runs inside the exact exported candidate, with no publication credential and before distribution transfer. Its complete-current validation therefore uses:

```text
python -m se_harness validate .
```

This is not a root upgrade or predecessor bypass. The trusted-main resolver continues to run the exact released 0.5 evaluator against the RLS-bound two-omission publication view before qualification. The changed command merely uses C6's validator for C6's complete archive, matching `SPEC-REB-007` rule 4 and the release's successful candidate-evidence lane.

## Local reproduction

In a fresh detached checkout of exact candidate `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`:

- candidate validation passed with 645 artifacts, zero errors, and 48 maintenance warnings;
- candidate `doctor` retained expected locked-root/template drift and exited successfully without mutation;
- the original locked-root command reproduces exact E009;
- candidate identity, tag, RLS, distribution bytes, rejected history, and root files are unchanged.

## Exact corrective qualification

The corrective candidate commit is `dbb5be73e40e885cbadd2ff75e098ed2252492ee`. Its diff contains exactly the trusted workflow line, its regression assertion, `WO-REB-009`, and this evidence. A fresh clone contained no stopped untracked release record.

- focused release-workflow policy: 5 tests passed;
- complete release-orchestration module: 22 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 209.476 seconds;
- complete current graph: 655 artifacts, zero errors, 50 maintenance warnings;
- release-distribution validation: passed with exact `RLS-SEH-012` and one distribution-bearing record;
- portable release surface, diff whitespace, and clean-checkout checks: passed;
- exact C6 candidate validation: 645 artifacts, zero errors, 48 maintenance warnings;
- original locked-root observation: exact E009 retained;
- candidate `doctor`: expected root/template drift only, with no mutation.

The first local full-suite run observed unrelated editable-distribution metadata outside the clone and failed only `RID018`. The same test and the complete suite passed in a fresh dependency-free virtual environment with user packages disabled; this matches the hosted job's isolated Python and changes no repository byte.

At this evidence closeout, work-order completion, later commit-bound VREC preparation and acceptance, trusted-main push, and publication retry remain separate lifecycle actions. No release identity, tag, distribution, root, rejected history, external policy, GitHub Release, PyPI file, Pages deployment, or maintenance ref changed during correction and qualification.
