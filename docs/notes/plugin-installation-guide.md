# Install or update the Verity Plane plugin

The public marketplace observed on 2026-10-01 is plugin 0.2.3 with released
evaluator 0.20.1 at `556d0faf83c32fd188409c5ba191552fad1522e1`.
Public fresh-install and 0.2.2-to-0.2.3 update checks passed on both Windows CLIs.
See the [public confirmation evidence](../engineering/release-0-20-1/evidence/WO-RLS-029/README.md)
for commands, exact native-evidence comparisons and limits.
Installing this plugin does not upgrade a project's selected harness.

## Select the distribution

For the currently published tree, follow its
[distribution guide](https://github.com/mmzen/se_harness/tree/plugin-marketplace).
For candidate qualification, maintainers use the
[committed composition procedure](plugin-marketplace-publication.md#assemble-committed-inputs)
to produce an external directory with both complete host packages. Do not install
the incomplete host folders directly from development source.

The [assembly README](../../release/plugin-marketplace/README.md) describes
development source. The published maintenance package uses the separately
qualified source `7ac05f25f008fa2e35ad1ae69ca3d84aa0c6ccab`.
Read the [published distribution guide](https://github.com/mmzen/se_harness/blob/556d0faf83c32fd188409c5ba191552fad1522e1/README.md)
for its commands. Its `PACKAGE-IDENTITY.json` names plugin 0.2.3, evaluator
0.20.1 and wheel SHA-256
`300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764`.
The plugin-owned minimal layout remains unreleased.

## Install in a disposable profile

Use Python 3.11+ with `venv` and `ensurepip`, installed host CLIs and Git.
Qualification uses disposable HOME/USERPROFILE, CODEX_HOME, CLAUDE_CONFIG_DIR,
APPDATA and LOCALAPPDATA directories. Keep any required host login separate from
retained evidence. Do not change real user profiles to run these checks.
Use the public Git marketplace:

```text
codex plugin marketplace add mmzen/se_harness --ref plugin-marketplace --json
codex plugin add verity-plane@se-harness --json
codex plugin list --marketplace se-harness --json
```

```text
claude plugin marketplace add mmzen/se_harness@plugin-marketplace
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

WO-RLS-028 retains native Windows qualification of plugin 0.2.3, accepted in
VREC-PLG-027. WO-RLS-029 confirms public fresh installation and updates from
the preserved public 0.2.2 package on Codex CLI 0.159.2 and Claude Code 2.1.273.
All 26 packaged files match on each of the four routes. Offline setup and
released-evaluator identity checks pass for all four installed packages.

The accepted startup, manual compaction and resume traces are reused after
exact package, fixture and host-version comparisons. Public Claude startup
and public Codex hook registration were checked again. Registration alone
does not prove execution; Codex still requires its normal hook trust step.

Desktop UI, automatic threshold compaction and other operating systems need
separate evidence. Model sessions require valid host authentication.
The [earlier 0.2.2 delivery report](../engineering/release-0-20-0/evidence/WO-PLG-031/README.md)
preserves its original host versions, failures and results.

## Successor candidate: clone, activate and resume

This route belongs to the successor candidate. Published plugin 0.2.3 does not provide it.
Installation of the host plugin is separate from a repository's release selection.
An existing repository continues to use its selected release after a plugin update.

1. Start the host session. If no checkout is selected, the hook supplies short
   bootstrap instructions and the host/session and plugin-data inputs.
2. Clone the requested repository, or reuse its identified checkout. Use the
   actual resulting absolute path, including a selected worktree's path.
3. Invoke the setup skill. Prepare any missing exact evaluator in the supplied
   external plugin-data directory. A project without selection needs explicit
   initialization; the candidate's default writes only its configuration and lock.
4. Activate the checkout with the helper below. Use the host-provided session ID
   and data directory. Do not invent an ID or copy it from another conversation.
5. Read the complete returned entry before governed work. Follow its current
   procedure to prepare a new change or continue the selected work order.
6. After compaction or resume, inspect the delivered repository and release.
   The same host session recovers its locator and revalidates the selection.
   If the host creates a new session ID, activate its checkout again.

```text
PYTHON -I ABSOLUTE_PLUGIN/scripts/activate.py --host HOST --session-id SESSION_ID --data-root ABSOLUTE_PLUGIN_DATA --target ABSOLUTE_CHECKOUT
```

`HOST` is `codex` or `claude`. The plugin root is the installed package containing
this script. Activation returns the selected compact entry immediately and writes
only a small private session locator. It does not modify repository policy or
grant work authority. Use the same command with another exact `--target` to switch.
Replace `--target ABSOLUTE_CHECKOUT` with `--clear` to clear only that session.

For parallel work, use separate writable checkouts and activate each session's
own path. Release environments coexist; no global last-used checkout is shared.
Repeat cycles within a session reuse its selection. A moved checkout, malformed
locator, missing host identity or altered release produces a delivery gap; the
hook does not search child directories or silently choose another repository.
Authorized push and PR work follows the selected release's delivery procedure.

The entry, procedures and templates come from the selected wheel. `resources`
returns exact local resource paths; formal artifacts remain checkout files.
See [minimal installation and safe migration](harness-installation-and-upgrades.md#minimal-installation-successor-candidate).
CLI observations alone do not qualify desktop delivery.

## Historical qualification

Historical development checks with Codex 0.154.0-alpha.6.2, Claude Code 2.1.266
and a development 0.18.0 checker remain in
[WO-PLG-016 evidence](../engineering/plugin-integration/evidence/WO-PLG-016/README.md).
They do not qualify the current public package. The optional old no-model acceptance helper remains a
development-only check; it does not replace native startup/compaction evidence.
