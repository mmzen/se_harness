# Prepare or repair the evaluator

## Read this when

The selected released evaluator is unknown, missing or mismatched.

## Before this action

Read the repository configuration and lock identity fields listed in the procedure. These are setup inputs, not a reason to read the machine lifecycle contracts.

## Procedure

### Prepare or repair the released evaluator

**Inputs:** The absolute repository path, its installed configuration and
lock, an available Python 3.11 or later with `venv` and `ensurepip`, and the
selected released wheel.

**Output:**

- **Environment files:** A reusable private evaluator environment outside
  the repository, with the selected wheel installed.
- **Repository files and artifacts:** None changed by environment preparation,
  `identity`, or `doctor`.
- **Transient working material:** The absolute evaluator Python path, selected
  version and digests, and actual identity and doctor results.

**Actions:**

1. Read `[harness].tool_version` in `.engineering-harness.toml`. Compare it
   with `tool_version` and `evaluator.version` in `.engineering-harness.lock`.
   Read `evaluator.payload_sha256` and, when present,
   `evaluator.archive_sha256` for the identity checks below. Report any
   mismatch before continuing with an ordinary repository mutation. Do not
   edit these values to make them agree.
2. Obtain the matching released wheel. If the lock records an archive digest,
   compare the wheel's SHA-256 with it before installation. Do not substitute a
   development build with the same version label.
3. Select a private environment outside the repository, keyed by the complete
   release identity. Verity Plane uses `DATA-ROOT/evaluators/VERSION/IDENTITY`,
   where `IDENTITY` is the archive SHA-256, or the payload SHA-256 when no archive
   digest is recorded. Reuse a matching completed environment. Keep environments
   for other releases unchanged; concurrent sessions may still use them.
4. Use Verity Plane's setup helper below to prepare a missing environment. It
   coordinates concurrent setup for the same identity, installs the wheel without
   index lookup or dependencies, validates identity, then marks the environment
   ready. An incomplete or mismatched environment requires inspection; do not
   reinstall over a possibly active environment. Without the plugin, prepare
   a separate environment with Python's environment and package tools and perform
   the same identity checks before use.
5. Resolve the environment's absolute Python executable: `Scripts/python.exe`
   on Windows or `bin/python` on Unix. Use it with `-I -m se_harness` from a
   working directory outside the checkout.
6. Inspect runtime identity with the locked version, payload digest, and
   environment root. Include the locked archive digest when one exists.
7. Run doctor and inspect every failure. Environment setup success is not a
   passing repository check.
8. On interruption, inspect the exact environment before retrying. Retire an
   incomplete environment only after confirming it is unused. When switching
   repositories, select that repository's matching environment. After cloning or
   changing the selected checkout, use the plugin setup skill's activation helper
   with the actual host session identity and checkout path. Read its returned
   entry before governed work. Environment setup alone does not activate a session.

**Harness commands:**

In these commands `ENV` is the absolute environment directory, `VERSION` is
the locked version, and `PAYLOAD-SHA256` is `evaluator.payload_sha256`:

```text
harnessctl identity --role released-evaluator --expected-version VERSION --expected-root ENV --checkout-root REPO --evaluator-payload-sha256 PAYLOAD-SHA256 --require-isolated-python --json
harnessctl doctor REPO --json
```

If `evaluator.archive_sha256` is present, add
`--evaluator-wheel-sha256 ARCHIVE-SHA256` to the identity command. The identity
check and doctor must pass before ordinary governed writes; those writes still
perform their own identity and action checks.

When the installed Verity Plane helper is used, its separate setup command is:

```text
PYTHON -I ABSOLUTE-PLUGIN/scripts/setup.py --target REPO --data-root DATA-ROOT --wheel ABSOLUTE-WHEEL
```

Here `PYTHON` is the available Python 3.11+ executable, and every path is an
actual absolute path supplied as a separate argument. Quote paths containing
spaces. The helper writes only its private environment and returns its final
doctor exit code. It does not install the host plugin or change repository
policy. If the required Python facilities are missing, report that prerequisite;
do not silently install Python or change host settings.

**Completion:** The absolute released evaluator and its identity are known.
The actual doctor result passes, or the exact environment/installation problem
is reported. A mismatch alone is not an instruction to upgrade the repository.

**Later use:** All subsequent `harnessctl` examples use this executable. Return
here when its selected release changes or its environment needs repair.

## Read next when

The exact release is usable → [CONTINUE.md#procedure](CONTINUE.md#procedure). An upgrade is explicitly authorized → [UPGRADE.md#procedure](UPGRADE.md#procedure). A provider repair is requested → [SKILL_PROVIDER.md#procedure](SKILL_PROVIDER.md#procedure).
