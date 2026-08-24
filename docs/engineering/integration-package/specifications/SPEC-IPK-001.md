+++
id = "SPEC-IPK-001"
type = "specification"
title = "Commit-addressed integration package workflow and manifest"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-IPK-001", "REQ-IPK-002", "REQ-IPK-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "technical-owner"
+++

# Specification: Commit-addressed integration package workflow and manifest

## Scope

Extend candidate evidence with one deterministic build, two-platform verification,
and final retention path for installable integration packages. Provide one
standard-library repository script for build and verification and one operator
document for download and installation.

Production package code, committed base versions, managed templates, release
orchestration, PyPI publication, and target governor selection are out of scope.

## Workflow model

1. Existing candidate-source, candidate-package, and governance-migration jobs
   run unchanged.
2. `integration-package-build` runs only after those gates pass. It supports a
   pull-request candidate and a push to `refs/heads/main`.
3. The build job creates two independent exports from one `git archive`, applies
   the same identity overlay, builds twice, requires byte equality, and uploads
   `integration-package-staging-<full-commit>` for one day.
4. `integration-package-verify` downloads that staging artifact on Linux and
   Windows and runs the complete verification procedure.
5. `integration-package-retain` runs only after every matrix member passes,
   re-verifies staging, and uploads the same three files as
   `se-harness-integration-<full-commit>` for the channel retention period.

## Identity rules

- Base version comes from both committed version declarations and must agree.
- Event channel is exactly `main` for a push to `refs/heads/main` or
  `pr<number>` for a pull request with a positive numeric ID.
- Commit is exactly 40 or 64 lowercase hexadecimal characters as reported by
  GitHub and must resolve to the exported archive.
- Integration version is `<base>+<channel>.g<first-12-commit-characters>`.
- Overlay paths are exactly `pyproject.toml` and `se_harness/__init__.py`.
- The checkout is never edited. Exports must stay below a disposable root and
  reject absolute paths, traversal, links, duplicate normalized paths, control
  characters, device names, and archive members outside that root.

## Payload contract

The final artifact contains exactly:

- `se_harness-<normalized-integration-version>-py3-none-any.whl`;
- `integration-manifest.json`; and
- `SHA256SUMS`.

`integration-manifest.json` is canonical compact JSON with sorted keys, UTF-8,
and one LF. It contains:

- `schema = "se-harness-integration-package-v1"`;
- `promotable = false` and `distribution_kind = "integration-package"`;
- repository, full commit, event, channel, workflow name, run ID and attempt;
- base and integration versions;
- Python, `build`, `setuptools`, and `wheel` versions;
- the two overlay path entries with pre/post SHA-256;
- wheel filename, size and SHA-256; and
- retention days.

Unknown, missing, duplicate, mistyped, oversized, or noncanonical fields fail
verification. Strings are bounded to 512 characters, arrays to 16 entries, and
payload files to 128 MiB. Secrets, environment dumps, credentials, host paths,
and hidden reasoning are prohibited.

`SHA256SUMS` contains wheel then manifest, ordered by portable filename, using
`<lowercase-sha256>  <filename>\n`.

## Build rules

- Python is 3.11 and build dependencies are exact-pinned in the workflow.
- `SOURCE_DATE_EPOCH` is the selected commit timestamp; `PYTHONHASHSEED=0`,
  `PYTHONNOUSERSITE=1`, and an empty `PYTHONPATH` are set.
- Build uses `python -m build --wheel --no-isolation` against disposable exports.
- Each build must produce exactly one pure-Python `py3-none-any` wheel.
- Wheel filename, dist-info directory, `METADATA` version, imported
  `se_harness.__version__`, and `harnessctl --version` must all agree.
- The two wheel byte sequences and SHA-256 values must agree.

## Verification rules

The verifier independently parses the manifest with duplicate-key rejection,
checks canonical bytes, recomputes all hashes, checks the exact three-file
inventory, and validates wheel metadata before installation. It then creates a
fresh virtual environment, installs with `--no-index --no-deps`, changes out of
the checkout, and uses isolated Python to exercise the package.

The disposable repository is initialized, checked by `doctor` and `validate`,
upgraded with the same integration package, and checked again. Before/after Git
and checkout manifests prove zero source change.

## Documentation rules

`docs/notes/integration-packages.md` explains current-main selection, run and
artifact discovery, `gh run download`, checksum verification on PowerShell and
POSIX, clean-environment installation, package identity, disposable testing,
cleanup, expiration, reproduction, and every non-release boundary. The
developer guide and notes index link to it.

## Security and failure rules

Repository archives, wheel members, manifests, checksums, workflow metadata,
artifact names, and downloaded files are untrusted. The script uses structured
arguments and no shell interpolation. A failure stops before final retention and
never rewrites checkout content or external release state.
