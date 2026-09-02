# Testing a current commit with an integration package

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

An integration package is an installable wheel built from one exact `main` or
pull-request commit. Candidate CI builds it twice, requires identical bytes,
installs the same staged wheel on Linux and Windows, and then retains those
bytes as an expiring GitHub Actions artifact.

Use this route when you need to test merged or proposed behavior as an installed
package before the next release. Do not use it as the governing evaluator for
an existing managed repository.

## What this channel guarantees

For an eligible successful workflow run:

- the committed public base version is unchanged;
- the disposable export receives a unique version such as
  `0.15.0+main.g1cdc75259da8` or `0.15.0+pr128.g1cdc75259da8`;
- two independent builds from the exact Git commit are byte-identical;
- `integration-manifest.json` binds the full commit, workflow run, build tools,
  overlay hashes, wheel name, size, and SHA-256;
- `SHA256SUMS` binds the manifest and wheel;
- Linux and Windows verify and install the same staged bytes before final
  retention; and
- the manifest records `promotable: false`.

Final artifacts from `main` expire after 14 days. Pull-request artifacts expire
after 3 days. One-day staging artifacts are internal handoffs and should not be
selected for ordinary testing.

## What it does not mean

An integration package is not a release, release candidate, GitHub Release
asset, PyPI/TestPyPI publication, release record, verification decision, or
automatic repository upgrade. Installing it gives the package technical
capability; it supplies no accountable authority.

In particular:

- it must not replace the exact released governing evaluator selected by an
  existing repository's `.engineering-harness.lock`;
- it must not be installed into that evaluator's environment;
- it must not be copied into a release bundle or uploaded to a package index;
- it creates no tag, RLS, REL, VREC transition, or publication decision; and
- `pip install --upgrade se-harness` uses the configured package index and does
  not select this artifact channel.

Use a new virtual environment and a disposable target repository. A decision to
test against a real managed repository requires its own explicit scope and
evaluator-selection review.

## 1. Find the successful run and exact commit

Authenticate the GitHub CLI for the repository, then list recent successful
`main` runs:

```powershell
gh run list `
  --workflow candidate-evidence.yml `
  --branch main `
  --event push `
  --status success `
  --limit 10 `
  --json databaseId,headSha,createdAt,conclusion
```

For a pull request, replace `--branch main --event push` with
`--event pull_request` and confirm the returned `headSha` is the exact merge
commit you intend to test. Record the numeric `databaseId` as `RUN_ID` and the
full lowercase `headSha` as `COMMIT`.

Inspect the selected run before downloading:

```powershell
gh run view RUN_ID
```

Require the build, both platform verification jobs, and final retention job to
have succeeded. Do not silently switch to a newer successful run when the
selected commit is unavailable.

## 2. Download the final artifact

Choose a new empty directory outside a source checkout and managed repository:

```powershell
$runId = "RUN_ID"
$commit = "FULL_LOWERCASE_COMMIT"
$download = Join-Path $env:TEMP "se-harness-integration-$commit"
New-Item -ItemType Directory -Path $download | Out-Null

gh run download $runId `
  --name "se-harness-integration-$commit" `
  --dir $download
```

The directory must contain exactly:

```text
integration-manifest.json
se_harness-<integration-version>-py3-none-any.whl
SHA256SUMS
```

Reject an extra, missing, linked, renamed, or nested file.

POSIX equivalent:

```bash
run_id=RUN_ID
commit=FULL_LOWERCASE_COMMIT
download="$(mktemp -d)/se-harness-integration-$commit"
mkdir -p "$download"
gh run download "$run_id" \
  --name "se-harness-integration-$commit" \
  --dir "$download"
```

## 3. Verify the downloaded bytes

On PowerShell, verify every line in `SHA256SUMS` without treating file content
as a command:

```powershell
Push-Location -LiteralPath $download
try {
  $files = @(Get-ChildItem -LiteralPath . -File)
  $wheels = @($files | Where-Object Extension -eq '.whl')
  if ($files.Count -ne 3 -or $wheels.Count -ne 1) { throw "unexpected artifact inventory" }
  foreach ($line in Get-Content -LiteralPath SHA256SUMS) {
    $parts = $line -split '  ', 2
    if ($parts.Count -ne 2) { throw "invalid SHA256SUMS line" }
    $expected = $parts[0]
    $name = $parts[1]
    if ($name -notin @('integration-manifest.json', $wheels[0].Name)) {
      throw "unexpected checksum filename: $name"
    }
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $name).Hash.ToLowerInvariant()
    if ($actual -ne $expected) { throw "SHA-256 mismatch: $name" }
  }
} finally {
  Pop-Location
}
```

On POSIX:

```bash
(cd "$download" && sha256sum --check SHA256SUMS)
```

Inspect the manifest as data and compare it with the selected run:

```powershell
$manifest = Get-Content -Raw -LiteralPath (Join-Path $download 'integration-manifest.json') |
  ConvertFrom-Json
if ($manifest.schema -ne 'se-harness-integration-package-v1') { throw 'wrong schema' }
if ($manifest.promotable -ne $false) { throw 'artifact is not marked non-promotable' }
if ($manifest.distribution_kind -ne 'integration-package') { throw 'wrong distribution kind' }
if ($manifest.commit -ne $commit) { throw 'commit mismatch' }
if ($manifest.run.id.ToString() -ne $runId) { throw 'workflow run mismatch' }
$manifest | Select-Object version, commit, channel, retention_days, promotable
```

For `main`, require `channel = main`, `retention_days = 14`, and a version ending
in `+main.g<first-12-commit-characters>`. For a pull request, require its exact
`pr<number>` channel, `retention_days = 3`, and matching version suffix.

## 4. Install by exact file path

Create a fresh environment outside the checkout and outside any released
evaluator environment. Install without consulting an index or resolving
dependencies:

```powershell
$environment = Join-Path $env:TEMP "se-harness-integration-env-$commit"
python -m venv $environment
$python = Join-Path $environment 'Scripts\python.exe'
$wheel = (Get-ChildItem -LiteralPath $download -File -Filter '*.whl').FullName
& $python -m pip install --disable-pip-version-check --no-index --no-deps $wheel
& $python -I -m se_harness --version
```

POSIX:

```bash
environment="$(mktemp -d)/se-harness-integration-env-$commit"
python -m venv "$environment"
python_bin="$environment/bin/python"
wheel="$(find "$download" -maxdepth 1 -type f -name '*.whl')"
"$python_bin" -m pip install --disable-pip-version-check --no-index --no-deps "$wheel"
"$python_bin" -I -m se_harness --version
```

The reported version must equal `manifest.version`. If it reports only the base
release, stop: the wrong wheel was installed.

## 5. Exercise a disposable repository

Initialize a new target that contains no valuable content:

```powershell
$target = Join-Path $env:TEMP "se-harness-integration-target-$commit"
& $python -I -m se_harness init $target --project-name IntegrationTest
& $python -I -m se_harness doctor $target
& $python -I -m se_harness validate $target
& $python -I -m se_harness upgrade $target --apply
& $python -I -m se_harness doctor $target
& $python -I -m se_harness validate $target
```

This smoke test may create and upgrade only that disposable target. It does not
authorize lifecycle decisions inside the target and must not be pointed at the
source checkout or an existing managed repository.

## 6. Clean up

After retaining any required test output elsewhere, remove only the exact
temporary paths you created:

```powershell
Remove-Item -LiteralPath $target -Recurse
Remove-Item -LiteralPath $environment -Recurse
Remove-Item -LiteralPath $download -Recurse
```

The GitHub artifact expires automatically. Local virtual environments and
downloaded wheels do not, so leaving them installed increases the chance of
mistaking stale candidate bytes for a release.

## Expired artifacts and reproduction

Expiration is expected. If the exact run and commit remain eligible, a
repository owner may separately authorize rerunning that workflow run:

```powershell
gh run rerun RUN_ID
```

The rerun must build from the same exact commit and produce a new manifest with
the same wheel identity but its own run attempt. Rerunning a workflow is an
external action; do not do it without that action's normal authorization.

If the exact commit is unreachable or cannot pass current gates, record that
fact. Do not substitute a nearby commit while keeping the old test claim.

## Troubleshooting

- **Final artifact is absent:** one of the candidate, migration, Linux, or
  Windows gates did not pass. Inspect the run; do not use the staging artifact.
- **Checksum fails:** delete the download and retrieve the exact artifact again.
  A second failure is an integrity incident for that run.
- **Version lacks `+main.g...` or `+pr....g...`:** you selected a release wheel
  or an invalid integration payload.
- **Artifact expired:** reproduce only the same reachable commit through a
  separately authorized rerun.
- **You need to test an existing governed repository:** stop. That changes the
  evaluator trust boundary and requires a separate accountable decision.
