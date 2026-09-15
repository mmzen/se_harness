# Install or try the Verity Plane plugin

For the standard marketplace route, use the [distribution guide](../../release/plugin-marketplace/README.md).
[WO-PLG-023](../engineering/plugin-integration/work-orders/WO-PLG-023.md) prepares
its committed catalogs, packages and native acceptance. Its evidence records
publication status; the source guide alone does not establish a public listing.
Maintainers use the [marketplace composition procedure](plugin-marketplace-publication.md).

## Development walkthrough

This guide covers **development packages on Windows**. It does not claim that the
current plugin is published in a public catalog. The checked package contains the
development SE Harness 0.18.0 wheel; use a disposable project for this trial.
Installing plugin instructions does not upgrade an existing project's harness.

You need Python 3.11 or later with `venv` and `ensurepip`, an installed Codex or
Claude Code CLI, this checkout and a local SE Harness wheel. All paths below are
absolute placeholders; replace them and quote paths containing spaces.

## 1. Assemble the local package

From this checkout, use the existing development command:

```text
python scripts/build_plugin_archives.py develop --repository . --wheel "LOCAL_WHEEL" --output-directory "NEW_PACKAGE_DIRECTORY"
```

Choose an output directory outside the checkout. It contains `codex/verity-plane`
and `claude/verity-plane`, each with skills, setup and the selected wheel. These
packages are for development, not publication.

## 2. Load it in your host

**Codex:** put this file at `NEW_PACKAGE_DIRECTORY/.agents/plugins/marketplace.json`:

```json
{
  "name": "verity-local",
  "plugins": [{
    "name": "verity-plane",
    "source": {"source": "local", "path": "./codex/verity-plane"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity"
  }]
}
```

Then run:

```text
codex plugin marketplace add "NEW_PACKAGE_DIRECTORY" --json
codex plugin add verity-plane@verity-local --json
```

Use the returned `installedPath` as `PLUGIN` in step 3. Start a new Codex session
to use its skills. These CLI commands were checked with the version below;
the host's [plugin documentation](https://learn.chatgpt.com/docs/plugins) also
describes its plugin browser. The [local catalog format](https://developers.openai.com/plugins/build/plugins)
comes from the host, not a new SE Harness installer.

**Claude Code:** use `NEW_PACKAGE_DIRECTORY/claude/verity-plane` as `PLUGIN`:

```text
claude --plugin-dir "PLUGIN" plugin details verity-plane
claude --plugin-dir "PLUGIN"
```

The first command displays the plugin and its skills; the second opens a session
using it. This is a [session-only local load](https://code.claude.com/docs/en/plugins-reference),
not a persistent marketplace installation. The interactive model session itself
was not part of this guide's acceptance check.

## 3. Connect a disposable project and check it

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
contain the repair and explicit upgrade procedure. Run checks when needed; this
plugin has no enforcement hook running in the background.

## What was checked

| Host on Windows | Observed route |
| --- | --- |
| Codex CLI 0.154.0-alpha.6.2 | Local catalog installation, native setup-skill discovery, then the installed package's setup, project connection and passing doctor. |
| Claude Code 2.1.266 | Session plugin discovery, then that package's setup, project connection and passing doctor. |

Both used Python 3.14.6 and development checker 0.18.0 in fresh profiles. The
commands were run directly; this does not certify an agent's behavior in a model
session, the desktop UI, other platforms or public installation. No extra host
prompt blocked these command walkthroughs. The initial missing-harness result is
the expected confusing case explained in step 3.

See [the concise results](../engineering/plugin-integration/evidence/WO-PLG-016/README.md).
To repeat the optional local acceptance with both CLIs installed:

```text
python tests/plugin_integration/onboarding/run_acceptance.py --wheel "LOCAL_WHEEL" --output "NEW_DISPOSABLE_DIRECTORY"
```

It uses isolated profiles and makes no model request. It is not a new CI prerequisite.
