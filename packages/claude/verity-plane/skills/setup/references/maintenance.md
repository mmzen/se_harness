# Maintain the checker and project

## Repair or switch projects

Read the target's selected harness version from `.engineering-harness.toml` and
choose its matching released wheel. Rerun the existing [setup command](environment.md)
in the same private data directory. It repairs the environment in place and runs
the actual `doctor`. A failed final check remains a failure to resolve.

One private environment can serve projects with different selected versions by
reinstalling the matching wheel when switching projects. Do not assume the wheel
last used for another project is compatible. No activation receipt is needed.
A plugin update changes its skills, not the project's selected harness version.

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
and retry the existing command; do not create a second environment or silently
change the project's version to match whichever wheel happens to be installed.
