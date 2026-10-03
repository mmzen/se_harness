# Install or update the Verity Plane plugin

## Published 0.22.0 / 0.2.5

Plugin 0.2.5 with evaluator 0.22.0 is public at
`7d30907f15bd7e06fb632e1ebf4e88e01b68726c`. VREC-PLG-032 verifies local package qualification.
Codex CLI fresh installation and update from the preserved public 0.2.4
installation passed. All 29 installed files match the qualified package.
Offline setup, exact evaluator identity, two-file initialization, resource lookup
and reuse passed on both routes.

Claude Code installation/update and native session tests, and Codex Windows desktop tests, were not run for this release and remain unverified under DEC-RLS-005/006. Both distributed packages were byte-checked.

See the [public observations](../engineering/release-0-22-0/evidence/WO-RLS-036/README.md).
Installing a plugin does not upgrade a project's selected harness.

## Select the distribution

For the currently published tree, follow its
[distribution guide](https://github.com/mmzen/se_harness/tree/plugin-marketplace).
For candidate qualification, maintainers use the
[committed composition procedure](plugin-marketplace-publication.md#assemble-committed-inputs)
to produce an external directory with both complete host packages. Do not install
the incomplete host folders directly from development source.

The [assembly README](../../release/plugin-marketplace/README.md) describes the
current source guidance. The public package uses qualified source
`abbec12ac5524c8adfb28693f846dd59de88f759`. Its
[distribution identity](https://github.com/mmzen/se_harness/blob/7d30907f15bd7e06fb632e1ebf4e88e01b68726c/PACKAGE-IDENTITY.json)
names plugin 0.2.5, evaluator 0.22.0 and wheel SHA-256
`44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4`.
The packaged READMEs retain their original pre-publication wording. Source
corrections do not rewrite those qualified bytes; use this guide for current status.

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

Use the absolute Python path returned by setup as `CHECKER`. On Windows the
new environment is `DATA/evaluators/VERSION/DIGEST/Scripts/python.exe`, where
`DIGEST` is the selected wheel SHA-256. Use that executable for each command:

```text
"CHECKER" -I -m se_harness init "PROJECT" --project-name "Plugin walkthrough" --dry-run --json
"CHECKER" -I -m se_harness init "PROJECT" --project-name "Plugin walkthrough" --json
"CHECKER" -I -m se_harness doctor "PROJECT" --json
```

In PowerShell, prefix a quoted executable with `&`, for example
`& "CHECKER" -I -m se_harness doctor "PROJECT" --json`.
Read the preview before applying. The final doctor must pass. Default 0.22.0
initialization creates only configuration and lock files. It creates no local
skill copies, so a new minimal installation needs no skill-ownership switch.
Existing repository-copy installations retain their selected release and use
its connection procedure until an explicitly approved migration.

The plugin's [connection instructions](../../plugins/verity-plane/common/skills/setup/references/repository.md)
cover existing projects and evaluators that do not yet offer `skill-ownership`.
Use a project's selected release for real project work. A development wheel is not
authority to govern this repository.

## If setup fails

| What you see | Next step |
| --- | --- |
| Python is missing, too old, or lacks `venv`/`ensurepip` | Supply a complete Python 3.11+ installation, then rerun setup. Setup does not download Python. |
| The wheel is missing, invalid or incompatible with Python | Select the correct local SE Harness wheel and rerun setup. The installer uses no package index. |
| Setup was interrupted or the private checker is damaged | Inspect the exact environment and confirm no session uses it before retiring it and retrying setup. Never replace a ready environment used by another session. |
| Doctor reports a project/checker version mismatch | Use the project's matching wheel, or follow the separately requested upgrade procedure. Reinstalling the checker alone does not upgrade a project. |

The shared [maintenance instructions](../../plugins/verity-plane/common/skills/setup/references/maintenance.md)
contain the repair and explicit upgrade procedure. Run checks when needed; the
startup/compaction hooks deliver instructions but do not enforce every tool call.


## Check instruction delivery

Start a session in the connected project. Codex requires review and trust of
the current hook definition. The hook launcher needs Python on PATH. Verify
that the delivered context names the selected checkout, release and exact entry
resource with its matching SHA-256 and final heading `After compaction`. On
0.21.0 and later the entry comes from the selected wheel; older layouts use the repository's
`ENGINEERING_HARNESS.md`. Repeat after manual
compaction. A missing, changed or incompatible root must disclose a delivery
gap; stop the affected governed action and resolve it before continuing.

## Qualification limits

Public fresh/update observations use Codex CLI 0.159.2. Installed bytes and
offline setup passed on both routes. Native debug prompt-input confirms skill
discovery; it does not prove hook execution or a model session.

VREC-PLG-032 retains exact-package Codex CLI/app-server qualification for startup,
activation, manual and automatic compaction, resume, session isolation and repeated
work. Those results apply to the same 29 file digests and host version observed
on the public routes. This is reuse of matching qualification evidence, not a
claim that authenticated model sessions ran in the fresh or update profiles.
Fresh profiles still need normal hook trust.

Claude Code installation/update and native session tests, and Codex Windows desktop tests, were not run for this release and remain unverified under DEC-RLS-005/006. Both distributed packages were byte-checked.

Model sessions require usable host authentication. The
[0.2.3 evidence](../engineering/release-0-20-1/evidence/WO-RLS-029/README.md)
retains its historical package, fixture and host-version comparisons.
The [earlier 0.2.2 delivery report](../engineering/release-0-20-0/evidence/WO-PLG-031/README.md)
preserves its original host versions, failures and results.

<a id="successor-candidate-clone-activate-and-resume"></a>

## Clone, activate and resume

This route is supplied by released plugin 0.2.5 with evaluator 0.22.0.
Installation of the host plugin is separate from a repository's release selection.
An existing repository continues to use its selected release after a plugin update.

1. Start the host session. If no checkout is selected, the hook supplies short
   bootstrap instructions and the host/session and plugin-data inputs.
2. Clone the requested repository, or reuse its identified checkout. Use the
   actual resulting absolute path, including a selected worktree's path.
3. Invoke the setup skill. Prepare any missing exact evaluator in the supplied
   external plugin-data directory. A project without selection needs explicit
   initialization; the selected 0.22.0 default writes only its configuration and lock.
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
See [minimal installation and safe migration](harness-installation-and-upgrades.md#minimal-installation-0210).
CLI observations alone do not qualify desktop delivery.

## Historical qualification

Historical development checks with Codex 0.154.0-alpha.6.2, Claude Code 2.1.266
and a development 0.18.0 checker remain in
[WO-PLG-016 evidence](../engineering/plugin-integration/evidence/WO-PLG-016/README.md).
They do not qualify the current public package. The optional old no-model acceptance helper remains a
development-only check; it does not replace native startup/compaction evidence.
