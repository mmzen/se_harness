# Keep evidence small

For new work, commit a short result and links to its raw output. Keep the command,
tested commit, checker version and actual import location, exit status and a
useful failure excerpt. Do not commit copied repositories, virtual environments,
or entire temporary run directories. These are authoring instructions, not a new
size gate or approval system.

The source suite and release-record suite use `scripts/record_evidence.py`.
It runs the same Python command once, returns its exit status, writes the full
combined output to `output.log`, and writes a small `summary.json` beside it.
Only the last 2,000 bytes of output enter the summary. The selected candidate
must be the checkout's HEAD; dirty work is labelled dirty. This helper records
source checks, not an installed evaluator's assurance decision.

Download the CI artifact, review its summary and retain that summary with the
work-order evidence. CI never commits on the owner's behalf. Keep the raw log in
the artifact. `candidate-source-raw` holds the source suite; the existing
`qualification-<mode>-<record>` artifact holds release-record test output.
Both are uploaded even when the check fails. Candidate package, upgrade and
predecessor result artifacts now also state a 14-day retention period explicitly.
Existing short-lived wheel/integration transfers retain their own periods.

The summary includes the run page, artifact name, exact download command and
estimated expiry. The upload step links the actual source artifact in the job
summary. GitHub's artifact metadata determines the actual expiry; manual
deletion can make it unavailable sooner. An estimate or URL does not prove an
upload succeeded. To check a saved summary's raw artifact:

```sh
python scripts/record_evidence.py check-raw summary.json
```

This uses the existing authenticated `gh` CLI. Missing, expired or unreachable
artifacts report **unavailable** with a failing exit status, even if the saved
test result says pass. A listed artifact still needs a successful download.
An old pass is an observation of that run, not a claim that raw evidence remains
retrievable. Download required evidence before it expires. Permanently required
publication manifests and package hashes remain in the durable release bundle
and bound records; this change does not replace them with expiring CI links.

## Historical archives

Measure the committed tree without reading copied checkout contents or changing
historical files:

```sh
python scripts/inventory_evidence.py --repository . --ref HEAD > inventory.json
```

The inventory gives each evidence bundle's committed size and file count, direct
VREC/RLS path references, and release references through those VRECs. It excludes
`.git`, untracked files and dirty working-copy bytes. It does not discover every
indirect dependency inside sidecars. No detected reference does not mean safe
to delete.

The assessment for WO-KIS-006 is retained in its evidence directory. Prefer a
compressed archive attached to an explicitly approved GitHub archive release,
with a small index giving the source commit, original paths, archive location,
size, digest and affected records. Before any move: enumerate indirect sidecar
references, download and extract the proposed archive in a disposable directory,
and confirm that the existing readers can still resolve the bound evidence.
If readers require the current paths, leave those files in place until a separate
approved change supports their archived location. Do not rewrite old assurance
facts or Git history to make the move appear transparent.

WO-KIS-006 assesses this option only. It creates no archive release and removes
no historical evidence. A later owner decision must identify the exact bundles,
destination, reference-preserving reader plan and deletion diff before a move.
