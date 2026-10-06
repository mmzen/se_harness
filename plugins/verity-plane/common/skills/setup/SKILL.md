---
name: setup
description: Prepare or repair the SE Harness checker, connect a project to plugin skills, or carry out a requested harness upgrade using the existing tools.
---

# Set up a project

Select Python 3.11 or later with venv and ensurepip. If it is unavailable,
report the missing prerequisite; do not install Python or change host settings.
Use the wheel selected for the repository's released evaluator. Plugin source
does not pin that release. A development wheel is only for disposable testing.

Use the target and action already requested; ask only for a missing choice.

## Hosted sandbox selection

Use this route only when the operator explicitly selects a hosted sandbox.
It is separate from checkout activation. Retain the operator's loopback endpoint,
project ID, baseline or versioned context, and named credential environment variable.
Never print the credential. The sandbox is not repository authority.

Obtain the qualified combination report and exact candidate client wheel.
Create a separate disposable Python environment outside the checkout. Verify the
wheel's SHA-256 against that report, then install that file with `pip --no-deps`.
The plugin's bundled released evaluator remains unchanged; do not replace it with
the candidate client. Use the candidate environment's absolute Python as
`CLIENT_PYTHON` in the remote commands below.

```text
CLIENT_PYTHON -I -m se_harness remote status --endpoint ENDPOINT --project PROJECT --token-env TOKEN_VARIABLE --json
```

Compare readiness, authority mode `sandbox-projection`, schema, protocols, and
all component identities with the selected combination. A mismatch stops the
remote action. An unavailable service never selects local file writes as a fallback.
Use harness-orient for reads or change for authorized sandbox draft preparation.
This route grants no approval, verification, release, adoption or deployment right.

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

A checkout without a harness selection follows [project connection](references/repository.md).
For missing evaluators, follow [environment setup](references/environment.md), then
activate again. Use exactly the plugin-data path delivered by the host so setup,
activation and the hook use the same storage. A plugin update does not adopt a release.

For `released-resources-v1`, the entry and required procedures come from the selected
evaluator's `resources ABSOLUTE_REPOSITORY --resource RESOURCE_ID --content --json`.
Read only the current procedure and applicable prerequisites. Legacy selections
continue to use their installed repository entry and task router. Read the selected
SETUP.md, UPGRADE.md or SKILL_PROVIDER.md procedure when it applies. For bootstrap,
use the references here; [maintenance](references/maintenance.md) covers requested upgrades.

Report what changed, the selected checker/version and its final check result.
Follow the project's installed instructions for governed work and retain existing
authorization for the requested action. These instructions install no host plugin
and grant no assurance or release decision.

## Private lifecycle test copy

The unpublished hosted pilot requires a separately installed candidate remote
client, a loopback endpoint, an explicit test project and a new disposable volume.
Use the repository's `server/README.md` Phase 3 procedure. Its configuration must
report `test_copy: true`; select `--test-copy` for each rehearsal or export.
Keep the real checkout selected with its released evaluator. Remote setup does
not activate graph authority or install this candidate into the user's host.
