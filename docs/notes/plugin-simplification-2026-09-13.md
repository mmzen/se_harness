# Simple plugin operation

WO-PLG-021 implements the replacement contract in SPEC-PLG-021.

The old harness skill directories are disposable. Select the installed plugin
with `skill-ownership TARGET --provider plugin --plugin-root DIRECTORY --apply`.
It checks the replacement's presence, deletes the four old directories and saves
`skill_ownership = {"provider": "plugin"}` in schema 4. Rerun after an ordinary
file error. There is no migration mutex, journal, plan hash or recovery state.
Use `--provider repository --apply` to copy the current repository templates back.
Unrelated skills and ordinary report destinations remain protected.

Plugin setup uses `DATA_ROOT/verity-plane/evaluator` outside the checkout.
It installs the selected wheel offline and runs doctor. The same command repairs
an interrupted installation. See the setup skill's environment procedure.

The plugin exposes shared skills with no automatic session or before-tool hooks.
Read repository instructions normally on entry, after compaction and after a
repository switch. Use the repository-selected released checker when beginning
governed work and at its required checkpoints. Host patch versions are not pinned.

For a local development package, run:

```text
python scripts/build_plugin_archives.py develop --repository . --wheel ABSOLUTE_LOCAL_WHEEL --output-directory ABSOLUTE_OUTPUT_OUTSIDE_CHECKOUT
```

This copies current source, including uncommitted edits, and the selected wheel.
Both host packages contain DEVELOPMENT.md. The build can replace its own output
directory; it refuses an unrelated directory. The existing `build` and `check`
commands still require their released-record and archive-identity inputs.
Development output does not establish publication eligibility.

The full source suite includes the small migration and plugin behavior tests.
Existing Windows and Ubuntu package environments run installed migration,
setup repair and package checks. The ownership-only Python 3.13 matrix,
source archive, recursive snapshots and host qualification fixtures are removed.
Earlier formal decisions, verification records, releases and retained evidence
keep their original bytes and historical meaning.
