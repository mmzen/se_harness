# Private evaluator environment

Choose the host's persistent plugin data directory outside the repository.
The environment always lives at `DATA_ROOT/verity-plane/evaluator`.
On Windows its Python is `Scripts/python.exe`; on Unix it is `bin/python`.

With an available Python 3.11+ installation, run:

```text
PYTHON ABSOLUTE_PLUGIN/scripts/setup.py --target ABSOLUTE_REPOSITORY --data-root ABSOLUTE_DATA_ROOT --wheel ABSOLUTE_SELECTED_WHEEL
```

Use separate shell arguments and quote paths containing spaces. The helper uses
venv, installs the supplied wheel with `--no-index --no-deps --force-reinstall`,
and invokes `doctor ABSOLUTE_REPOSITORY --json` with the private Python and `-I`.
It writes only its private environment and returns the actual checker exit code.

Run this same command again if setup was interrupted or the selected evaluator
changes. No separate receipt, activation script, or new output folder is needed.
Select the release from the repository's installed harness configuration;
doctor reports mismatches and managed-file problems through its normal result.
