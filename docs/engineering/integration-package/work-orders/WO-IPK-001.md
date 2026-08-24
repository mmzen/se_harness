+++
id = "WO-IPK-001"
type = "work_order"
title = "Implement the qualified integration-package lane"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work creates installable candidate distributions and changes hosted CI retention; assurance must bind the exact workflow and package bytes that Linux and Windows verified."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".github/scripts/build_integration_package.py",
  ".github/workflows/candidate-evidence.yml",
  "README.md",
  "docs/engineering/README.md",
  "docs/engineering/integration-package/evidence/WO-IPK-001-verification.md",
  "docs/notes/README.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/integration-packages.md",
  "tests/fixtures/integration_package/",
  "tests/test_integration_package.py",
]

[relations]
implements = ["REQ-IPK-001", "REQ-IPK-002", "REQ-IPK-003"]
specifications = ["SPEC-IPK-001"]
architecture = ["ARCH-IPK-001", "ADR-IPK-001"]
verification = ["VER-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T11:17:45Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T11:42:56Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the qualified integration-package lane

## Lifecycle and authorization

This work order is `draft`. It authorizes no implementation, workflow run,
artifact retention, installation, Git operation, publication or external
action. The assurance classification is a content proposal until the
accountable packet is approved.

Before work starts, the accountable owners must approve the complete IPK chain
and this work order through the managed lifecycle procedure. The engineering
owner must then separately transition this work order to `in_progress` after
the exact released evaluator passes start preflight.

## Objective

Extend candidate evidence so a qualified `main` or pull-request commit produces
one expiring, installable and commit-addressed integration package. Retain final
bytes only after deterministic build and same-byte Linux/Windows installation,
and document a safe operator path that cannot be mistaken for release or
governing-evaluator adoption.

## In scope

- Add one standard-library repository script that safely exports the exact
  commit, derives and applies the disposable local-version overlay, builds
  twice, creates and verifies the canonical manifest and checksums, inspects
  wheel identity, and performs isolated installed-package smoke checks.
- Extend `candidate-evidence.yml` with build, Linux/Windows verification and
  final-retention jobs using exact action and build-tool pins, least privilege,
  bounded timeouts and the approved retention periods.
- Preserve all existing candidate-source, candidate-package and migration gates
  as prerequisites.
- Add verifier-owned fixtures and tests for valid identity, hostile archives and
  payloads, deterministic bytes, manifest/checksum strictness, workflow
  dependencies, retention settings and release-authority separation.
- Add public and contributor documentation for selecting a current-main run,
  downloading the artifact, verifying it, installing by file path into an
  isolated environment, exercising a disposable repository and cleaning up.
- Retain implementation evidence at the declared evidence path.

## Out of scope

- Changing the version committed in `pyproject.toml` or
  `se_harness/__init__.py`, or changing product runtime code.
- Publishing to PyPI, TestPyPI, GitHub Releases or another package index;
  creating a tag, release contract, VREC, REL or release record; or modifying a
  release/publication workflow.
- Promoting an integration artifact into a release bundle or extending its
  lifetime outside the approved Actions retention.
- Automatically installing into a user environment, changing a managed target,
  updating `.engineering-harness.toml` or `.engineering-harness.lock`, or
  selecting the integration package as the governing evaluator.
- Adding credentials, release environments, write permissions, hosted services,
  scheduled publication, private indexes or cleanup automation outside normal
  Actions expiration.
- Committing, pushing, opening or merging a pull request, or applying lifecycle
  transitions beyond separately authorized work-order procedure.

## Authorized decision envelope

After accountable approval and successful start preflight, the implementer may
choose private helper names, bounded diagnostic wording, verifier-fixture
layout within the declared directories, and concise documentation structure.
The implementer may select exact compatible patch versions of `build`,
`setuptools` and `wheel`, provided they are pinned in the workflow and recorded
in the manifest and evidence.

The implementer may not change the manifest schema, version formula, overlay
paths, payload inventory, platform set, final artifact name, retention periods,
authority boundary, workflow eligibility or release separation. A need to do so
requires a revised formal artifact and accountable decision.

## Constraints

- Preserve Python 3.11+ product behavior and use the standard library in the
  repository script except for invoking the exact-pinned external build tools.
- Treat Git archives, event metadata, workflow inputs, paths, wheels, ZIP
  members, manifests and checksums as untrusted.
- Use structured subprocess arguments and safe disposable directories; never
  interpolate untrusted values as shell syntax.
- Never change checkout content during build or installed-package verification.
- Install retained bytes with `--no-index --no-deps` only into disposable
  virtual environments and repositories.
- Preserve unrelated user changes and all managed root files.
- Keep workflow permissions at `contents: read` and expose no publication
  credential or release environment.

## Implementation plan

1. Approve the IPK packet, run exact released-evaluator start preflight, and
   transition only `WO-IPK-001` to `in_progress` through the managed procedure.
2. Implement verifier-owned hostile-input, identity, manifest, checksum,
   deterministic-build and workflow-static cases.
3. Implement the standard-library build/verify script with strict subcommands
   and safe disposable boundaries.
4. Add the staged build, Linux/Windows verification and final-retention jobs to
   the candidate workflow without changing existing gate behavior.
5. Add operator and contributor documentation and rehearse every command.
6. Run the complete `VER-IPK-001` matrix, retain implementation evidence and
   stop for the engineering-owner completion decision and later independent
   commit-bound assurance.

## Required verification

- Every method and case in `VER-IPK-001`.
- Focused integration-package tests and the complete repository test suite.
- Candidate-source syntax, help, package and validation checks labeled as
  candidate evidence.
- Separately identified exact released-evaluator identity, doctor, validation,
  inspection and applicable preflight results.
- One commit-bound candidate workflow proving deterministic build, exact staged
  and final inventories, and same-wheel Linux/Windows installation.
- Static proof that release and publication workflows neither produce nor
  consume integration-package names or schemas.
- Documentation command rehearsal on PowerShell and POSIX.
- `git diff --check` and an exact changed-path manifest proving every change is
  admitted by `[execution_scope]`.

## Evidence to record

Retain exact commands, exit codes, runtimes, evaluator and candidate identities,
formal snapshot, workflow/action/build-tool pins, valid and hostile fixture
digests, derived versions, two build hashes, staging/final inventories,
manifests and checksums, Linux/Windows installed identities, disposable-target
results, checkout pre/post state, workflow dependency and authority scans,
documentation rehearsal, changed paths, deviations and residual risks under
`docs/engineering/integration-package/evidence/WO-IPK-001-verification.md`.

## Stop and escalate conditions

Stop before changing a path outside `[execution_scope]`; modifying product or
committed version files; weakening archive, payload, manifest, checksum,
determinism or same-byte checks; changing the version formula, platform set,
artifact name, retention or eligibility; adding credentials, write permission,
publication, release state, managed-root mutation or evaluator adoption;
performing an installation outside disposable fixtures; running an external
workflow without separate action-time authorization; performing Git or release
actions; or encountering a failed gate that cannot be corrected inside the
approved contracts.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-IPK-001`, exact changed paths, package and
evaluator identities, verification results, evidence path, deviations,
residual uncertainty, and intentionally unperformed installation, Git,
assurance, release, publication, credential and external actions. Recommend
exactly one next authorized step.
