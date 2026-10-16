## Activate the checkout

After cloning or selecting existing work, reuse that exact absolute checkout path.
Use the host, session_id and plugin-data path delivered by the native hook. The
helper is `scripts/activate.py` under this skill's installed plugin root (two
directories above this skill directory). Do not infer a session identity from a transcript or another chat.
If these inputs are missing, report the host delivery limitation before governed work.

```text
PYTHON -I ABSOLUTE_PLUGIN/scripts/activate.py --host HOST --session-id SESSION_ID --data-root ABSOLUTE_PLUGIN_DATA --target ABSOLUTE_CHECKOUT
```

`HOST` is `codex` or `claude`. Pass each value as one argument. Read the complete
returned `content` before continuing. Activation writes only that session's local
checkout locator. It does not approve work or change repository files.
Use the same command to switch. Replace `--target ABSOLUTE_CHECKOUT` with `--clear`
to remove only this session's selection. A failed activation preserves the old
record and blocks work on the requested target; do not treat the old selection as
permission to continue there instead.

## Prepare missing resources

A checkout without a harness selection follows [project connection](repository.md).
For missing evaluators, follow [environment setup](environment.md), then
activate again. Use exactly the plugin-data path delivered by the host so setup,
activation and the hook use the same storage. A plugin update does not adopt a release.

For `released-resources-v1`, the entry and required procedures come from the selected
evaluator's `resources ABSOLUTE_REPOSITORY --resource RESOURCE_ID --content --json`.
Read only the current procedure and applicable prerequisites. Legacy selections
continue to use their installed repository entry and task router. Read the selected
SETUP.md, UPGRADE.md or SKILL_PROVIDER.md procedure when it applies. For bootstrap,
use the references here; [maintenance](maintenance.md) covers requested upgrades.

Report what changed, the selected checker/version and its final check result.
Follow the project's installed instructions for governed work and retain existing
authorization for the requested action. These instructions install no host plugin
and grant no assurance or release decision.

