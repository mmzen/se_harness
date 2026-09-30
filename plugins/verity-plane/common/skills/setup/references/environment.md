# Private evaluator environment

Use the absolute persistent plugin-data path supplied by the native hook. It must
be outside repositories and the replaceable plugin package. Separate release
identities use separate directories under `DATA_ROOT/evaluators/VERSION/DIGEST`.
The digest is the selected wheel SHA-256, or the selected payload SHA-256 when a
legacy lock has no archive identity. Use the Python path returned by setup.

With Python 3.11+ and the explicitly selected trusted wheel, run:

```text
PYTHON -I ABSOLUTE_PLUGIN/scripts/setup.py --target ABSOLUTE_REPOSITORY --data-root ABSOLUTE_PLUGIN_DATA --wheel ABSOLUTE_SELECTED_WHEEL
```

Pass paths as separate arguments. Setup installs offline with `--no-index --no-deps`,
validates the installed identity and marks that environment ready only afterward.
Concurrent setup for the same identity reports contention; retry after the first
operation finishes. Different releases remain independent. A ready environment is
validated and reused; setup never reinstalls over one another session could use.

Setup then runs the actual `doctor` with the private Python and `-I -m se_harness`
from outside the checkout. Its exit code is the doctor result. A new project can
have a prepared evaluator while doctor correctly reports no installed harness.
Inspect that result before the separately requested initialization or upgrade.

Interrupted or damaged environments produce an explicit gap. Inspect the exact
private directory and confirm no session uses it before retiring it and retrying
setup. Do not remove another identity's directory or edit readiness metadata.
After preparation, activate the checkout again. Hooks never download or install.
