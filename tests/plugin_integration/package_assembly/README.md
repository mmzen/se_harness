# Package assembly

WO-PLG-001 builds two archives from one committed asset plan and one published
evaluator wheel. It does not install or publish them. The included plan builds
an **inert test fixture**, not a production plugin.

## Inputs

Use Python 3.11+ and Git. Supply an absolute path to an external Python
environment containing a released `se-harness`; it computes the wheel's
canonical payload hash. No Python interpreter is packaged or downloaded.

The plan maps each **destination path to a committed source file**:

```json
{
  "schema": "se-harness-plugin-assembly-v1",
  "name": "example-plugin",
  "shared": {"scripts/example.py": "plugin/shared/example.py"},
  "hosts": {
    "codex": {".codex-plugin/plugin.json": "plugin/codex/plugin.json"},
    "claude": {".claude-plugin/plugin.json": "plugin/claude/plugin.json"}
  }
}
```

These example paths must exist in the selected commit. The builder supplies
no missing production assets. Both manifests must name the plugin directory.
Host adapters and their native manifest validation belong to later work orders.

Select two full commit IDs: the asset source and the trusted commit containing
the released RLS record. Independently obtain the published wheel SHA-256.
The RLS record, expected digest, wheel filename, metadata and bytes must agree.
Trust in the selected release and external evaluator is a caller prerequisite;
the builder does not turn arbitrary repository metadata into release authority.

## Build and check

From the repository root, provide the selected values to:

```text
python scripts/build_plugin_archives.py build
  --revision FULL_SOURCE_COMMIT
  --plan tests/plugin_integration/package_assembly/fixtures/plan.json
  --release-revision FULL_TRUSTED_RELEASE_RECORD_COMMIT
  --release-record docs/engineering/release-0-17-0/releases/RLS-SEH-026.md
  --expected-wheel-sha256 INDEPENDENT_PUBLISHED_SHA256
  --wheel ABSOLUTE_PATH_TO_RELEASED_WHEEL
  --evaluator-python ABSOLUTE_PATH_TO_EXTERNAL_PYTHON
  --output-directory NEW_DISPOSABLE_DIRECTORY
```

This shows argument boundaries; enter it on one line or use your shell's line
continuation syntax. Run the same command with `check` instead of `build` to
recheck the output against the committed inputs. A zero exit and
`"accepted": true` mean the complete pair passed package acceptance.

Each output contains `codex/<name>/`, `claude/<name>/` and two ZIP archives.
Both plugin trees carry the exact wheel under `packages/` and an
`assembly-inventory.json` with file hashes, modes and provenance. ZIP members
have fixed timestamps and Git executable modes. The archive contains the plugin
directory, including its dot-prefixed native manifest directory.

The inventory lists every payload file. It cannot hash itself; the independent
checker regenerates it from committed inputs and compares its complete bytes.
It also checks the ZIP bytes and rejects omitted, extra or changed files.

## Boundaries

- Only explicitly mapped text/plugin image assets are copied. No directory
  scanning, dependency fetching, candidate wheel building or evaluator import.
- Runtime directories, dependency archives, binary executables, top-level
  `bin/`, unsafe names, links and conflicting destinations are refused.
  This is a bounded file policy, not a scanner for arbitrary code disguised as
  plugin scripts. Review the selected source before assembly.
- Source bytes come from Git blobs, so dirty working files cannot change them.
- Use a private output parent without concurrent writers. Output paths must be
  new and must not cross symlinks or Windows reparse points. Cross-process
  races in a directory controlled by another actor are outside this tool's scope.
- Interrupted output is retained for inspection and fails `check`. Reusing that
  directory is refused; retry in a fresh directory and accept only after a full
  recheck. A manifest alone is not evidence that assembly completed.
- Package acceptance does not establish native discovery, runtime bootstrap,
  host support, release approval or permission to publish.

## Verification

Run the focused boundary tests with the external evaluator environment:

```text
python -B -m unittest discover -s tests/plugin_integration/package_assembly -p "test_*.py" -v
```

These tests create synthetic wheels and temporary Git repositories; they do not
claim that a synthetic wheel is published. The repository's top-level unittest
discovery does not descend into this fixture directory: run this command
explicitly as well as the repository suite.

For the real-wheel C01–C08 observations, run `run_acceptance.py` in this directory
with the same inputs as the builder, plus `--repository`, a new
`--evidence-directory`, and a new `--scratch-directory`; omit the action and
`--output-directory`. It preserves commands, raw output, immutable fixture
revisions and expected/observed values per case. Negative variants use a
disposable local clone. Source hashes identify retained inputs after the
scratch directory is discarded.

See [the implementation evidence](../../../docs/engineering/plugin-integration/evidence/WO-PLG-001/README.md)
for executed platforms and limitations. No unrun platform counts as passing.
