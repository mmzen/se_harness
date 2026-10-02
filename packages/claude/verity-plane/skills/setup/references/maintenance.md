# Maintain the checker and project

## Repair or switch projects

Read the target's selected harness version from `.engineering-harness.toml` and
choose its matching released wheel. Rerun the existing [setup command](environment.md)
using the plugin-data path supplied by the hook. Setup validates and reuses the
matching immutable environment; it never repairs an environment in use. For an
interrupted or damaged preparation, follow the recovery boundary in environment.md.
A failed final doctor check remains a failure to resolve.

Distinct selected releases coexist. Switching projects uses activation; it does
not reinstall either evaluator. A plugin update changes the adapter, not the
project's selected harness version.

## Upgrade when requested

Choose the requested available release and prepare the checker with its wheel.
Before the project is upgraded, `doctor` may report the expected version or template
difference. Inspect that result; do not treat an unrelated failure as an upgrade request.
Use that checker's actual `upgrade --help` for supported options.

```text
EVALUATOR_PYTHON -I -m se_harness upgrade ABSOLUTE_PROJECT --json
EVALUATOR_PYTHON -I -m se_harness upgrade ABSOLUTE_PROJECT --apply --json
EVALUATOR_PYTHON -I -m se_harness doctor ABSOLUTE_PROJECT --json
```

Review the proposed changes and follow the target's existing upgrade requirements.
If the project requires transaction evidence, use its requested path with the
existing `--evidence-output` option. Keep customized owner files unless the owner
has selected replacement; the checker's supported `--replace-file` option can name
an editable file to replace. Disposable plugin skill copies are handled separately
by [the provider switch](repository.md), not as owner-file conflicts.

Report the selected version and final result. If installation is interrupted, rerun
setup with the selected wheel. If upgrading fails, resolve the reported problem
and retry the existing command; do not silently change the project's version to match whichever wheel happens to be installed.

After a successful requested upgrade, activate the same checkout again to use its new selection.
