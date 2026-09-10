$SetupPython='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\se-harness-plugin-eval-016\Scripts\python.exe'
$Repo='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\plugin-skill-acceptance\independent-20260910\transition-repository'
$Data='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\plugin-skill-acceptance\independent-20260910\plugin-data'
$EnvDir='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\plugin-skill-acceptance\independent-20260910\plugin-data\evaluator-016'
$Wheel='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\plugin-evaluator-wheels\se_harness-0.16.0-py3-none-any.whl'
$Version='0.16.0'
$Payload='51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c'
$Archive='a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae'
$IdentityFile='C:\Users\mathi\Documents\Codex\2026-09-04\hel\work\plugin-skill-acceptance\independent-20260910\plugin-data\chg08-transition-setup-identity.json'
$PrerequisiteCheck='import sys
if sys.version_info < (3, 11):
    raise SystemExit(''Install Python 3.11 or newer before plugin setup.'')
try:
    import venv, ensurepip
    print(''Python'', sys.version.split()[0], ''venv available; pip'', ensurepip.version())
except (ImportError, OSError) as error:
    raise SystemExit(''Install Python venv/ensurepip support before plugin setup: '' + str(error))'
$InputCheck='import hashlib, json, os, re, stat, sys
from pathlib import Path
repo, data, env, wheel = map(Path, sys.argv[1:5])
version, payload, archive = sys.argv[5:8]
observation = Path(sys.argv[8])
def ordinary(path):
    if not path.is_absolute() or ''..'' in path.parts:
        raise SystemExit(''Select absolute paths without parent traversal.'')
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), ''st_file_attributes'', 0) & getattr(stat, ''FILE_ATTRIBUTE_REPARSE_POINT'', 0)):
            raise SystemExit(''Use ordinary paths without parent links or reparse points: '' + str(item))
for path in (repo, data, env, wheel, observation):
    ordinary(path)
if not repo.is_dir() or not data.is_dir() or not wheel.is_file():
    raise SystemExit(''Select existing repository, persistent data and wheel paths.'')
if data == repo or data.is_relative_to(repo) or repo.is_relative_to(data):
    raise SystemExit(''Persistent data must be separate from the repository.'')
if env.parent != data or observation.parent != data or observation == env or observation.exists():
    raise SystemExit(''Select an environment child and a new observation file in persistent data.'')
if not re.fullmatch(r''[0-9]+\.[0-9]+\.[0-9]+'', version) or any(not re.fullmatch(r''[0-9a-f]{64}'', h) for h in (payload, archive)):
    raise SystemExit(''Provide the fixed published version and SHA-256 identities.'')
if wheel.name != ''se_harness-'' + version + ''-py3-none-any.whl'':
    raise SystemExit(''Wheel filename does not match the selected release.'')
with wheel.open(''rb'') as stream:
    if hashlib.file_digest(stream, ''sha256'').hexdigest() != archive:
        raise SystemExit(''Bundled wheel SHA-256 mismatch; do not install it.'')
def unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(''duplicate JSON key'')
        value[key] = item
    return value
lock = repo / ''.engineering-harness.lock''
if lock.exists():
    ordinary(lock)
    expected = json.loads(lock.read_text(encoding=''utf8''), object_pairs_hook=unique)[''evaluator'']
    if any(expected.get(k) != v for k, v in {''version'': version, ''payload_sha256'': payload, ''archive_sha256'': archive, ''archive_name'': wheel.name}.items()):
        raise SystemExit(''Repository lock requires a different evaluator; do not upgrade it here.'')
    repository_state = ''lock-matched''
else:
    if (repo / ''.engineering-harness.toml'').exists():
        raise SystemExit(''Repository configuration has no governing lock; stop for repair.'')
    repository_state = ''uninitialized; tool setup only''
print((''existing'' if env.exists() else ''new'') + '': '' + repository_state)'
$EntryCheck='import os, stat, sys
from pathlib import Path
env, python, entry = map(Path, sys.argv[1:])
folder = ''Scripts'' if os.name == ''nt'' else ''bin''
if python != env / folder / (''python.exe'' if os.name == ''nt'' else ''python'') or entry != env / folder / (''harnessctl.exe'' if os.name == ''nt'' else ''harnessctl''):
    raise SystemExit(''Use this environment\''s exact Python and harnessctl entry point.'')
for path in (env, python.parent, entry):
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), ''st_file_attributes'', 0) & getattr(stat, ''FILE_ATTRIBUTE_REPARSE_POINT'', 0)):
            raise SystemExit(''Unsafe environment or entry-point path.'')
if not python.is_file() or not entry.is_file() or not (env / ''pyvenv.cfg'').is_file():
    raise SystemExit(''Incomplete environment; retain it and use a fresh location for an authorized retry.'')
if os.name != ''nt'' and not os.access(entry, os.X_OK):
    raise SystemExit(''Installed harnessctl entry point is not executable.'')'
$AcceptIdentity='import json, sys
from pathlib import Path
result = json.loads(Path(sys.argv[1]).read_text(encoding=''utf-8-sig''))
version, payload, archive = sys.argv[2:]
if (result.get(''schema'') != ''se-harness-runtime-identity-v3''
        or result.get(''passed'') is not True
        or result.get(''harness_version'') != version
        or result.get(''evaluator_payload_sha256'') != payload
        or result.get(''evaluator_archive_sha256'') != archive):
    raise SystemExit(''Evaluator is not ready: require passing identity and matching observed archive.'')
print(''Evaluator environment ready; no repository or lifecycle changes made.'')'
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
