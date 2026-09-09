# Private evaluator environment

Run these commands through the host's shell tool. Stop on the first failure.
The Python blocks below are arguments to the supplied interpreter's `-c`
option. They are shared checks, not files to install or a new bootstrap command.
Bind each block to the named shell variable before running the shell sequence.

## 1. Select the inputs

Discover Python with the host's executable inventory, PowerShell
`Get-Command python3,python -CommandType Application`, or Bash
`type -a python3 python`. Select one actual, trusted installation. A lookup
failure means the operator must install Python 3.11+ with `venv` and `ensurepip`.
Do not run a store alias, installer or automatic-download shim. An explicitly
provided installation needs no search. This discovery happens before Python
checks or plugin components run.

Bind these values as ordinary shell variables. Use literal values and argument
arrays; do not evaluate values from repository files as shell code.

| Variable | Value selected by the agent |
| --- | --- |
| `SetupPython` | Absolute executable path from the provided Python installation. |
| `Repo` | Absolute existing target repository directory; it is read only here. |
| `Data` | Absolute existing persistent plugin-data directory, writable by this operator. |
| `EnvDir` | One direct child of `Data`, reserved for this evaluator environment. |
| `Wheel` | Absolute local wheel path under the verified plugin's `packages/`. |
| `Version`, `Payload`, `Archive` | Fixed version, canonical payload SHA-256 and wheel SHA-256 from the accepted package and trusted release. |
| `IdentityFile` | A new observation file in `Data`, outside the environment and repository. |

Package acceptance under SPEC-PLG-001 comes first: use its accepted assembly
inventory and independently selected release. An unchecked inventory or the
environment being inspected cannot supply its own expected identity. Recheck
the wheel bytes below. If an installed repository requires a different release,
select an already available matching package or stop for the separately
authorized upgrade procedure. Do not rewrite its lock or download a substitute.

Use a private data directory without concurrent writers. Do not place it in the
plugin installation/cache or the checkout. Check the host-selected location
before binding `Data`; this procedure cannot infer a host's persistent location.

## 2. Shared checks

Bind this block as `PrerequisiteCheck`. A failure leaves setup untouched.
`ensurepip` must expose its bundled pip; environment creation also checks its
actual execution. Disk or creation failures remain incomplete setup.

<!-- snippet:prerequisites -->
```python
import sys
if sys.version_info < (3, 11):
    raise SystemExit('Install Python 3.11 or newer before plugin setup.')
try:
    import venv, ensurepip
    from importlib.resources import files
    bundled = list(files('ensurepip').joinpath('_bundled').iterdir())
    if not any(p.name.startswith('pip-') and p.name.endswith('.whl') for p in bundled):
        raise ImportError('bundled pip unavailable')
    print('Python', sys.version.split()[0], 'venv available; pip', ensurepip.version())
except (ImportError, OSError) as error:
    raise SystemExit('Install Python venv/ensurepip support before plugin setup: ' + str(error))
```

Bind this block as `InputCheck`. Pass `Repo Data EnvDir Wheel Version Payload
Archive IdentityFile`, in that order. It reads paths and wheel bytes; it writes
nothing. It reports `new` or `existing`, followed by the repository state.
The repository lock constrains release selection; it grants no execution rights.

<!-- snippet:inputs -->
```python
import hashlib, json, os, re, stat, sys
from pathlib import Path
repo, data, env, wheel = map(Path, sys.argv[1:5])
version, payload, archive = sys.argv[5:8]
observation = Path(sys.argv[8])
def ordinary(path):
    if not path.is_absolute() or '..' in path.parts:
        raise SystemExit('Select absolute paths without parent traversal.')
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)):
            raise SystemExit('Use ordinary paths without parent links or reparse points: ' + str(item))
for path in (repo, data, env, wheel, observation):
    ordinary(path)
if not repo.is_dir() or not data.is_dir() or not wheel.is_file():
    raise SystemExit('Select existing repository, persistent data and wheel paths.')
if data == repo or data.is_relative_to(repo) or repo.is_relative_to(data):
    raise SystemExit('Persistent data must be separate from the repository.')
if env.parent != data or observation.parent != data or observation == env or observation.exists():
    raise SystemExit('Select an environment child and a new observation file in persistent data.')
if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version) or any(not re.fullmatch(r'[0-9a-f]{64}', h) for h in (payload, archive)):
    raise SystemExit('Provide the fixed published version and SHA-256 identities.')
if wheel.name != 'se_harness-' + version + '-py3-none-any.whl':
    raise SystemExit('Wheel filename does not match the selected release.')
with wheel.open('rb') as stream:
    if hashlib.file_digest(stream, 'sha256').hexdigest() != archive:
        raise SystemExit('Bundled wheel SHA-256 mismatch; do not install it.')
def unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate JSON key')
        value[key] = item
    return value
lock = repo / '.engineering-harness.lock'
if lock.exists():
    ordinary(lock)
    expected = json.loads(lock.read_text(encoding='utf8'), object_pairs_hook=unique)['evaluator']
    if any(expected.get(k) != v for k, v in {'version': version, 'payload_sha256': payload, 'archive_sha256': archive, 'archive_name': wheel.name}.items()):
        raise SystemExit('Repository lock requires a different evaluator; do not upgrade it here.')
    repository_state = 'lock-matched'
else:
    if (repo / '.engineering-harness.toml').exists():
        raise SystemExit('Repository configuration has no governing lock; stop for repair.')
    repository_state = 'uninitialized; tool setup only'
print(('existing' if env.exists() else 'new') + ': ' + repository_state)
```

Bind this block as `EntryCheck`. Pass `EnvDir EnvPython EntryPoint`. Keep the
environment Python's lexical path; resolving its final POSIX symlink would
select the system interpreter instead. Require actual launcher files before
the identity command; a supplied entry-point string alone is insufficient.

<!-- snippet:entry -->
```python
import os, stat, sys
from pathlib import Path
env, python, entry = map(Path, sys.argv[1:])
folder = 'Scripts' if os.name == 'nt' else 'bin'
if python != env / folder / ('python.exe' if os.name == 'nt' else 'python') or entry != env / folder / ('harnessctl.exe' if os.name == 'nt' else 'harnessctl'):
    raise SystemExit('Use this environment\'s exact Python and harnessctl entry point.')
for path in (env, python.parent, entry):
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)):
            raise SystemExit('Unsafe environment or entry-point path.')
if not python.is_file() or not entry.is_file() or not (env / 'pyvenv.cfg').is_file():
    raise SystemExit('Incomplete environment; retain it and use a fresh location for an authorized retry.')
if os.name != 'nt' and not os.access(entry, os.X_OK):
    raise SystemExit('Installed harnessctl entry point is not executable.')
```

Bind this block as `AcceptIdentity`. Pass `IdentityFile Version Payload Archive`.
Accept only successful, complete JSON and the **observed** archive digest.
`evaluator_wheel_sha256` echoes an expected input and cannot replace that check.

<!-- snippet:accept -->
```python
import json, sys
from pathlib import Path
result = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
version, payload, archive = sys.argv[2:]
if (result.get('schema') != 'se-harness-runtime-identity-v3'
        or result.get('passed') is not True
        or result.get('harness_version') != version
        or result.get('evaluator_payload_sha256') != payload
        or result.get('evaluator_archive_sha256') != archive):
    raise SystemExit('Evaluator is not ready: require passing identity and matching observed archive.')
print('Evaluator environment ready; no repository or lifecycle changes made.')
```

## 3. Execute one host sequence

Use one dedicated child shell, with the input variables and the four Python
blocks bound as strings. Process-local changes below end with this shell. There
is no activation, system PATH change, shell profile edit or Python installation.

If `EnvDir` exists, run only its checks: never install over it or silently
rebuild it. For a new environment, reserve the directory exclusively before
`venv` runs. Keep it in its final location; virtual environments are not portable.
An interrupted directory remains unselected until the full identity check
passes. Report partial effects and retry in a new location if necessary.

### Windows / PowerShell

<!-- snippet:powershell -->
```powershell
$ErrorActionPreference = 'Stop'
if (-not [IO.Path]::IsPathRooted($SetupPython) -or -not (Test-Path -LiteralPath $SetupPython -PathType Leaf)) {
    throw 'Select an installed Python 3.11+ executable before plugin setup.'
}
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PIP_CONFIG_FILE = 'NUL'
& $SetupPython -I -S -c $PrerequisiteCheck
if ($LASTEXITCODE -ne 0) { throw 'Python prerequisites failed; no environment created.' }
& $SetupPython -I -S -c $InputCheck $Repo $Data $EnvDir $Wheel $Version $Payload $Archive $IdentityFile
if ($LASTEXITCODE -ne 0) { throw 'Setup inputs refused; no installation attempted.' }
$EnvPython = Join-Path $EnvDir 'Scripts/python.exe'
$EntryPoint = Join-Path $EnvDir 'Scripts/harnessctl.exe'
$env:PATH = (Join-Path $EnvDir 'Scripts') + [IO.Path]::PathSeparator + $env:PATH
if (-not (Test-Path -LiteralPath $EnvDir)) {
    New-Item -ItemType Directory -Path $EnvDir -ErrorAction Stop | Out-Null
    & $SetupPython -I -m venv $EnvDir
    if ($LASTEXITCODE -ne 0) { throw 'Environment creation incomplete; retain this directory.' }
    & $EnvPython -I -m pip --isolated --disable-pip-version-check install --no-index --no-deps --only-binary=:all: --no-cache-dir --no-compile $Wheel
    if ($LASTEXITCODE -ne 0) { throw 'Wheel installation incomplete; retain this directory.' }
}
& $SetupPython -I -S -c $EntryCheck $EnvDir $EnvPython $EntryPoint
if ($LASTEXITCODE -ne 0) { throw 'Environment entry point refused.' }
$IdentityOutput = & $EnvPython -I -m se_harness identity --role released-evaluator --expected-version $Version --expected-root $EnvDir --checkout-root $Repo --evaluator-payload-sha256 $Payload --evaluator-wheel-sha256 $Archive --entry-point $EntryPoint --require-entry-point --require-isolated-python --json
$IdentityExit = $LASTEXITCODE
[IO.File]::WriteAllText($IdentityFile, ($IdentityOutput -join "`n"), [Text.UTF8Encoding]::new($false))
if ($IdentityExit -ne 0) { throw 'Released evaluator identity refused; retain the observation.' }
& $SetupPython -I -S -c $AcceptIdentity $IdentityFile $Version $Payload $Archive
if ($LASTEXITCODE -ne 0) { throw 'Plugin readiness refused.' }
```

### Linux / Bash

<!-- snippet:bash -->
```bash
set -euo pipefail
case "$SetupPython" in /*) ;; *) echo 'Select an absolute Python 3.11+ executable.' >&2; exit 1 ;; esac
test -x "$SetupPython" || { echo 'Install Python 3.11+ with venv and ensurepip before plugin setup.' >&2; exit 1; }
unset PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1 PIP_CONFIG_FILE=/dev/null
"$SetupPython" -I -S -c "$PrerequisiteCheck"
"$SetupPython" -I -S -c "$InputCheck" "$Repo" "$Data" "$EnvDir" "$Wheel" "$Version" "$Payload" "$Archive" "$IdentityFile"
EnvPython="$EnvDir/bin/python"
EntryPoint="$EnvDir/bin/harnessctl"
export PATH="$EnvDir/bin:$PATH"
if test ! -e "$EnvDir"; then
    mkdir -- "$EnvDir"
    "$SetupPython" -I -m venv "$EnvDir"
    "$EnvPython" -I -m pip --isolated --disable-pip-version-check install --no-index --no-deps --only-binary=:all: --no-cache-dir --no-compile "$Wheel"
fi
"$SetupPython" -I -S -c "$EntryCheck" "$EnvDir" "$EnvPython" "$EntryPoint"
"$EnvPython" -I -m se_harness identity --role released-evaluator --expected-version "$Version" --expected-root "$EnvDir" --checkout-root "$Repo" --evaluator-payload-sha256 "$Payload" --evaluator-wheel-sha256 "$Archive" --entry-point "$EntryPoint" --require-entry-point --require-isolated-python --json > "$IdentityFile"
"$SetupPython" -I -S -c "$AcceptIdentity" "$IdentityFile" "$Version" "$Payload" "$Archive"
```

## 4. Use or stop

Retain the identity observation outside the plugin cache. Use the returned
absolute environment Python with `-I -m se_harness`, cleared `PYTHONPATH`, and
its `Scripts` or `bin` first in the command's PATH. Recheck identity when
selecting an environment for governed work. Do not use global `harnessctl`.

For an installed repository, run existing `doctor` and the selected workflow's
checks before any governed operation. A missing lock means this procedure
prepared the tool only; repository initialization requires its own workflow.
Never infer work, assurance, release or upgrade authority from readiness.

On any failure, report the failed command, observation and any partial private
directory. Preserve the repository and the failed environment. Do not repair
metadata to manufacture an archive observation, weaken expected hashes, fall
back to another executable or delete an environment automatically.

These are the standard [venv](https://docs.python.org/3.11/library/venv.html),
[ensurepip](https://docs.python.org/3.11/library/ensurepip.html) and
[pip install](https://pip.pypa.io/en/stable/cli/pip_install/) commands.
Plugin identity requirements come from SPEC-PLG-002 and the existing released
evaluator; this reference does not redefine lifecycle policy.
