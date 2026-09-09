# Environment setup checks

These tests execute the command blocks in the setup skill's
[environment procedure](../../../plugins/verity-plane/common/skills/setup/references/environment.md).
The runner is test tooling and is not part of the plugin. It does not supply
an alternative setup algorithm.

## Run the quick checks

From the repository root:

```text
python -B -m unittest discover -s tests/plugin_integration/environment_setup -p "test_*.py" -v
```

Run this explicitly; top-level discovery does not enter this directory.

## Run ENV01–ENV12

Provide an existing Python installation, a published wheel and two absent
directories outside the repository. The runner uses native PowerShell on
Windows or Bash on Linux. It installs only into disposable fixture directories.

```text
python -B tests/plugin_integration/environment_setup/run_acceptance.py
  --python ABSOLUTE_PROVIDED_PYTHON
  --wheel ABSOLUTE_PUBLISHED_WHEEL
  --version 0.16.0
  --scratch NEW_DISPOSABLE_DIRECTORY
  --evidence NEW_EVIDENCE_DIRECTORY
  --network-constraint DESCRIPTION_OF_ACTUAL_NETWORK_RESTRICTION
```

Enter the command on one line or use the host shell's continuation syntax.
Version `0.17.0` is also supported. Expected version, payload and archive digests
are fixed from published release evidence before execution. An arbitrary wheel
cannot supply its own expected hash.

On Linux, run inside `unshare -Urn` when available and include `namespace` in
the network-constraint description. The runner then checks that `/proc/net/dev`
has no external interface and `/proc/net/route` has no routes. The Windows runs
use the Codex sandbox's network restriction. Offline pip flags apply on both.
A description alone does not disable networking.

Each run retains `inputs.json`, `env01.json` through `env12.json`, a snapshot
comparison and `summary.json`. It also retains the exact executed reference and
runner. Records contain command output, fixed expectations, observations,
timings and platform facts; local fixture prefixes are normalized.

Missing Python uses a real absent executable. The old-version and missing-module
cases inject those conditions into an isolated prerequisite probe; they do not
pretend that an old or damaged Python installation was available. The version
mismatch modifies the installed runtime's version in a disposable environment.
Interrupted setup stops after environment creation and before package install.
All mutated installed files are restored after each negative case.

The lock fixtures test release selection, not repository initialization or
formal governance. Passing these checks establishes only the reported
OS/Python/evaluator combination. Native plugin activation, unavailable platforms
and repository upgrades are separate work.
