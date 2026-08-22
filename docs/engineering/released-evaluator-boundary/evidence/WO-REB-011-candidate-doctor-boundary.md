# WO-REB-011 candidate doctor boundary evidence

## Failure retained

Publication run `32596026852` and credential-free qualification job `97087055231` passed exact released authority resolution, the predecessor publication view, C6 candidate validation at 645 artifacts with zero errors, and the Git-aware C6 test suite. The final candidate-source command then exited 1:

```text
python -m se_harness doctor .
```

Its failures were the already documented differences between 0.6 distribution templates and the repository's separately locked 0.5 managed root, including new schema-3 managed files not present in schema 2. Managed-root integrity entries themselves passed unchanged. Build, bundle transfer, GitHub Release, PyPI, Pages, maintenance, tag, root, history, distribution, and policy mutation jobs did not run.

## Correct boundary

Candidate complete-current qualification is `python -m se_harness validate .` plus the full candidate tests and CLI surface. Released-root health is a separate claim: the resolver already acquires exact released 0.5, proves its identity, runs `doctor`, and validates the RLS-bound predecessor-compatible view before qualification. Running candidate 0.6 `doctor` against the intentionally unupgraded 0.5 root adds no valid release-payload claim and deterministically blocks the approved predecessor trust direction.

Local C6 reproduction returned exit 1 with the same root/template drift and no mutation. The correction removes only that inapplicable final command; every complete-current, predecessor, test, build, byte-comparison, and privilege gate remains.

Focused, complete exact-correction, commit identity, and lifecycle results are added after the corrective candidate exists.
