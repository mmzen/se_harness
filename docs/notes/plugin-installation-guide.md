# Install or update the Verity Plane plugin

The public marketplace observed on 2026-09-28 is plugin 0.1.0 with evaluator
0.18.0 at `ed68b30c88043773be929540b7b10ae537957c2d`. The prepared candidate is
plugin 0.2.1 with the unchanged released evaluator 0.19.0. Its public publication
and update confirmation remain pending. This guide does not upgrade a project's
selected harness.

## Select the distribution

For the currently published tree, follow its
[distribution guide](https://github.com/mmzen/se_harness/tree/plugin-marketplace).
For candidate qualification, maintainers use the
[committed composition procedure](plugin-marketplace-publication.md#assemble-committed-inputs)
to produce an external directory with both complete host packages. Do not install
the incomplete host folders directly from development source.

The [assembly README](../../release/plugin-marketplace/README.md) is rendered at
the distribution root. Its package links resolve there, not in the source tree.
Check `PACKAGE-IDENTITY.json`: plugin 0.2.1, evaluator 0.19.0, the accepted source
commit and wheel SHA-256
`43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.

## Install in a disposable profile

Use Python 3.11+ with `venv` and `ensurepip`, installed host CLIs and Git.
Qualification uses disposable HOME/USERPROFILE, CODEX_HOME, CLAUDE_CONFIG_DIR,
APPDATA and LOCALAPPDATA directories. Keep any required host login separate from
retained evidence. Do not change real user profiles to run these checks.
Replace `MARKETPLACE_DIRECTORY` with the absolute composed directory:

```text
codex plugin marketplace add "MARKETPLACE_DIRECTORY" --json
codex plugin add verity-plane@se-harness --json
codex plugin list --marketplace se-harness --json
```

```text
claude plugin marketplace add "MARKETPLACE_DIRECTORY"
claude plugin install verity-plane@se-harness --json
claude plugin list --json
```

Use the returned installed path as `PLUGIN` below. Inspect the configured
marketplace source and installed manifest. Restart the host. Confirm the loaded
plugin path and compare its files with the composition's identity inventory.

## Update an existing Git installation

First confirm that `se-harness` selects the intended Git source. Once the public
identity matches the accepted candidate, refresh and install its new version:

```text
codex plugin marketplace upgrade se-harness --json
codex plugin add verity-plane@se-harness --json
codex plugin list --marketplace se-harness --json
```

```text
claude plugin marketplace update se-harness
claude plugin update verity-plane@se-harness --json
claude plugin list --json
```

Restart and inspect active bytes again. A marketplace named `se-harness` may
instead point to a local development tree. Before switching that source, record
its location and inspect the host's marketplace list. Remove only the selected
source through the native marketplace command, then add the intended source
and update the plugin. Preserve other installations. A cache directory or a
successful refresh alone does not prove the new package is loaded.

## Connect a disposable project and check it

Create an empty `PROJECT` directory. Choose a persistent `DATA` directory outside
that project and the plugin's replaceable package directory. `WHEEL` is the selected
file under `PLUGIN/packages/`. Run:

```text
python "PLUGIN/scripts/setup.py" --target "PROJECT" --data-root "DATA" --wheel "WHEEL"
```

On a new project, setup creates the checker environment, then reports a missing
harness with a nonzero exit. Confirm that this is the reported problem before
continuing. A Python or wheel installation error needs fixing first.

On Windows, `CHECKER` below is `DATA/verity-plane/evaluator/Scripts/python.exe`.
Use that executable for each command:

```text
"CHECKER" -I -m se_harness init "PROJECT" --project-name "Plugin walkthrough" --dry-run --json
"CHECKER" -I -m se_harness init "PROJECT" --project-name "Plugin walkthrough" --json
"CHECKER" -I -m se_harness skill-ownership "PROJECT" --provider plugin --plugin-root "PLUGIN" --json
"CHECKER" -I -m se_harness skill-ownership "PROJECT" --provider plugin --plugin-root "PLUGIN" --apply --json
"CHECKER" -I -m se_harness doctor "PROJECT" --json
```

In PowerShell, prefix a quoted executable with `&`, for example
`& "CHECKER" -I -m se_harness doctor "PROJECT" --json`.
Read each preview before applying. The final doctor must pass. The provider switch
replaces the disposable generated skill copies with plugin skills; project-owned
content stays in the project. It records only the provider, not this machine's path.

The plugin's [connection instructions](../../plugins/verity-plane/common/skills/setup/references/repository.md)
cover existing projects and evaluators that do not yet offer `skill-ownership`.
Use a project's selected release for real project work. A development wheel is not
authority to govern this repository.

## If setup fails

| What you see | Next step |
| --- | --- |
| Python is missing, too old, or lacks `venv`/`ensurepip` | Supply a complete Python 3.11+ installation, then rerun setup. Setup does not download Python. |
| The wheel is missing, invalid or incompatible with Python | Select the correct local SE Harness wheel and rerun setup. The installer uses no package index. |
| Setup was interrupted or the private checker is damaged | Rerun the same setup command with the same data directory and selected wheel. |
| Doctor reports a project/checker version mismatch | Use the project's matching wheel, or follow the separately requested upgrade procedure. Reinstalling the checker alone does not upgrade a project. |

The shared [maintenance instructions](../../plugins/verity-plane/common/skills/setup/references/maintenance.md)
contain the repair and explicit upgrade procedure. Run checks when needed; the
startup/compaction hooks deliver instructions but do not enforce every tool call.


## Check instruction delivery

Start a session in the connected project. Codex requires review and trust of
the current hook definition. The hook launcher needs Python on PATH. Verify
that the delivered context names this project's `ENGINEERING_HARNESS.md`, its
matching SHA-256 and final heading `After compaction`. Repeat after manual
compaction. A missing, changed or incompatible root must disclose a delivery
gap; stop the affected governed action and resolve it before continuing.

## Qualification limits

WO-PLG-026 retains this candidate's Windows native fresh, update and local 0.2.0
replacement observations. WO-PLG-028 will retain later public-route observations.
Until a route has a passing retained result, it is a procedure to check, not a
claim of success. Desktop UI, automatic threshold compaction and other operating
systems need separate evidence. Model sessions require valid host authentication.

Historical development checks with Codex 0.154.0-alpha.6.2, Claude Code 2.1.266
and a development 0.18.0 checker remain in
[WO-PLG-016 evidence](../engineering/plugin-integration/evidence/WO-PLG-016/README.md).
They do not qualify 0.2.1. The optional old no-model acceptance helper remains a
development-only check; it does not replace native startup/compaction evidence.
