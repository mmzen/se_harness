# Connect a project

Use the requested absolute project path and an installed plugin directory containing
`skills/`. Select the project's released checker version. For a new project, select
an available release; development wheels belong only in disposable fixtures.

Prepare the private checker with [environment setup](environment.md). Use its
absolute Python path below as `EVALUATOR_PYTHON`; quote each path separately.

## New harness installation

The target directory must exist. On a project without a harness, setup can install
the checker successfully while its first `doctor` reports missing harness files.
That result is not a healthy-project check. Inspect it: only the expected absence
of a harness leads to initialization; resolve any installation or other failure first.

For the requested initialization, preview and apply the existing installer:

```text
EVALUATOR_PYTHON -I -m se_harness init ABSOLUTE_PROJECT --project-name "Project name" --dry-run --json
EVALUATOR_PYTHON -I -m se_harness init ABSOLUTE_PROJECT --project-name "Project name" --json
```

Review the preview before applying it. The same `init` command handles an empty
directory or an existing code project without a harness. An initialized project
uses `upgrade` for version changes; do not reinitialize it to replace its settings.

## Select plugin skills

First inspect `EVALUATOR_PYTHON -I -m se_harness skill-ownership --help`. If the
selected release lacks that command, stop this switch and explain that it needs
a compatible released checker and an explicitly requested upgrade. Do not run
candidate source against a live project to make the command available.

```text
EVALUATOR_PYTHON -I -m se_harness skill-ownership ABSOLUTE_PROJECT --provider plugin --plugin-root ABSOLUTE_PLUGIN --json
EVALUATOR_PYTHON -I -m se_harness skill-ownership ABSOLUTE_PROJECT --provider plugin --plugin-root ABSOLUTE_PLUGIN --apply --json
EVALUATOR_PYTHON -I -m se_harness doctor ABSOLUTE_PROJECT --json
```

Explain once that this replaces the named generated `harness-orient` and
`harness-operator-brief` directories under `.agents/skills/` and `.claude/skills/`,
including edits inside them. Review the reported paths and run the already
authorized switch. Unrelated files stay; missing replacement skills or an unsafe
destination must be resolved before deletion. After interruption, rerun the same
operation rather than creating a recovery plan or receipt.

The project stores the provider choice, not the plugin's machine path. An ordinary
clone can run checker commands without a plugin installed. To invoke plugin skills,
install the plugin through that host's normal route. Report native discovery only
when the host has actually shown the skills; a successful `doctor` does not prove it.
