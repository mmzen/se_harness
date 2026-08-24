+++
id = "VER-IPK-001"
type = "verification"
title = "Independent integration-package qualification contract"
status = "approved"
owners = ["assurance-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-IPK-001", "REQ-IPK-002", "REQ-IPK-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent integration-package qualification

## Independence

Primary acceptance uses verifier-owned archives, payloads, manifests, wheels,
workflow fixtures and expected values derived from the approved IPK contracts.
Tests must not import candidate overlay, manifest, checksum, path-safety or
retention functions as their source of expected results.

Candidate unit tests, builder-reported hashes, successful artifact upload and
implementer-authored snapshots are supplementary evidence only. At least one
commit-bound workflow run must install the exact final candidate bytes on both
Linux and Windows. That run remains candidate assurance evidence; it is not a
release record and does not authorize the package as a governing evaluator.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| `REQ-IPK-001` exact identity and provenance | verifier-owned version, archive, overlay, double-build, manifest and checksum tests | main and PR channels; 40/64-character commits; mismatched/base-local versions; unsafe archives; unexpected overlay matches; metadata mismatch; altered and nondeterministic wheels | accepted packages have the exact derived version, only declared export changes, byte-identical builds, canonical provenance and independently recomputed hashes; every ambiguity fails before final retention |
| `REQ-IPK-002` same-byte cross-platform retention | hosted Linux/Windows matrix plus independent final-payload comparison | valid package; missing/extra/altered files; skipped, failed, cancelled or partial matrix; staging/final mismatch; expiry settings | both platforms verify and install the same wheel digest, exercise a disposable repository outside the checkout, and only their converged success permits the exact staged bytes to receive the final artifact name |
| `REQ-IPK-003` authority boundary | workflow and repository static scan, negative workflow fixtures, documentation rehearsal | tags, release jobs, index upload, release credentials/environments, RLS/REL/VREC inputs, governor changes, ordinary index upgrade, existing non-disposable repository | no integration path creates or consumes release authority, publication state or automatic evaluator selection; operator steps are explicit, isolated, checksum-verified and disposable |

## Version and overlay vectors

- Base `0.6.0`, main, and commit
  `1cdc75259da8156e93ad8c32110ee196296b8cea` produce exactly
  `0.6.0+main.g1cdc75259da8`.
- The same base and pull request `128` produce exactly
  `0.6.0+pr128.g1cdc75259da8`.
- Reject empty, zero, signed, padded or non-numeric pull-request IDs; uppercase,
  short, mixed or nonhex commits; mismatched source versions; base local
  segments; multiple or absent assignment targets; and post-overlay mismatches.
- Confirm wheel filename, dist-info directory, `METADATA`, imported
  `se_harness.__version__`, `harnessctl --version`, manifest and checksum file
  all resolve to the same integration identity.

## Hostile archive and payload matrix

Exercise absolute, traversal, dot-component, alternate-separator, drive, UNC,
device-name, control-character, invalid-encoding, case-collision, duplicate,
symlink, hardlink, junction and oversized members. Exercise payload directory,
link, missing, extra, hidden, duplicate-normalized and oversized entries.

Exercise duplicate JSON keys, unknown or missing fields, floats where integers
are required, booleans as integers, invalid enums, malformed hashes, excessive
nesting, oversized values, noncanonical ordering, encoding/BOM, line endings,
filenames, overlay entries, retention values and checksum syntax. Every unsafe
or ambiguous input fails without extracting outside its disposable root or
retaining a final artifact.

## Determinism and package checks

- Build two independent exports from the same archive with exact-pinned Python
  build tooling, commit-derived `SOURCE_DATE_EPOCH`, fixed hash seed, disabled
  user site and empty `PYTHONPATH`.
- Require exactly one `py3-none-any` wheel per export and byte equality of both
  wheel and independently computed SHA-256.
- Parse ZIP members without extraction before installation. Reject traversal,
  duplicate members, unexpected dist-info identities and unsafe filenames.
- Recompute canonical manifest and checksum bytes independently.
- Repeat deterministic unit cases under randomized enumeration, locale and
  line-ending materialization.

## Cross-platform installed checks

On current hosted Linux and Windows runners:

1. Download the same one-day staging artifact and independently validate the
   exact three-file inventory, canonical manifest and checksums.
2. Create a new virtual environment and install the wheel with
   `--no-index --no-deps`.
3. Leave the candidate checkout and use isolated Python to compare installed
   metadata, imported version and `harnessctl --version` with the manifest.
4. Initialize a disposable standard repository, run `doctor` and `validate`,
   exercise managed upgrade with the same wheel, and run both checks again.
5. Compare candidate-checkout bytes and Git references before and after.

The final job downloads staging again, repeats payload verification, and uploads
those same files only after every required matrix member succeeds.

## Workflow and authority checks

- Confirm the build job depends on every existing candidate gate and the final
  job depends on build plus every platform verifier.
- Confirm pull requests and pushes to `refs/heads/main` are the only eligible
  channels and event metadata cannot select another branch or commit silently.
- Confirm `contents: read`, bounded timeouts, exact action commit pins, exact
  build-tool pins, one-day staging, 14-day main retention and 3-day PR retention.
- Confirm artifact names include the full commit and the final name appears in
  only the post-verification job.
- Scan all release and publication workflows to prove they do not consume the
  integration artifact name, manifest schema or local-version channel.
- Confirm no tag, GitHub Release, PyPI/TestPyPI upload, release environment,
  publication credential, RLS, REL, VREC transition, managed-root update or
  governing-evaluator change is added.

## Documentation checks

Rehearse documented `gh run` discovery and download, PowerShell and POSIX
checksum verification, isolated virtual-environment installation, version
inspection, disposable repository smoke test, cleanup and expired-artifact
reproduction. Confirm warnings distinguish the integration package from a
release and explain that normal `pip` index upgrades do not select it.

## Repository checks and evidence retention

Run focused tests, complete repository tests, candidate-source validation,
exact released-evaluator identity/doctor/validation and commit-bound workflow
verification. Record exact commands, runtimes, action and dependency versions,
commit and run IDs, event channel, two build hashes, staging/final inventories,
Linux/Windows installed identities, disposable-repository results, pre/post
checkout hashes, negative cases, documentation rehearsal, deviations and
residual risks at
`docs/engineering/integration-package/evidence/WO-IPK-001-verification.md`.

The evidence file is not a VREC, release record, publication authorization or
evaluator-selection decision.

## Residual uncertainty

Repository checks cannot guarantee indefinite GitHub artifact availability,
authenticate the substantive intent of every downloader, or make an installed
candidate safe to govern a real repository. GitHub service behavior and hosted
runner images may change. Exact action pins, retained manifests, checksums,
short retention, explicit installation and the separate released-evaluator
boundary limit but do not eliminate those risks.
