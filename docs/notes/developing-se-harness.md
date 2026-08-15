# Developing and self-hosting SE Harness

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This note applies to contributors developing `se_harness` itself. It does not define a consumer installation profile and grants no implementation, verification, release, publication, or governor-promotion authority.

The self-hosting controls add implementation-specific assurance without changing normal artifact lifecycle or decision rights. See [Self-Hosting Operations](../engineering/self-hosting-boundary/SELF_HOSTING.md#effect-on-normal-governance-operations) for the explicit boundary.

## Development environment

SE Harness requires Python 3.11 or later and has no runtime dependencies outside the standard library. From a trusted source checkout, install candidate source into a dedicated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m se_harness --version
```

`python -m pip install .` performs a non-editable source install. Neither form is released proof; both are candidate development inputs.

## Repository structure

```text
se_harness/                              CLI and safe installation control plane
templates/repository/standard/           one canonical consumer installation
self_hosting/                             published migration and self-hosting workflow data; not an installation profile
scripts/                                 portable validation, Explorer, CI selection, release support
tests/                                   installer, policy, provenance, identity, and regression tests
docs/notes/                              non-authoritative human explanations
docs/engineering/                        self-governing formal artifact graph and evidence
.self-hosting/governor.toml              exact independently released governor selection
.github/workflows/engineering-harness.yml repository-specific three-plane assurance workflow
.github/workflows/self-hosting-governor.yml candidate reusable workflow published for later governors
```

The root validator and Explorer sources remain byte-identical to their canonical managed-template copies. The self-hosting workflow and root self-hosting configuration are intentional repository-specific controls protected by the root lock, not alternative consumer profiles.

## Ordinary development checks

Use the commands confirmed by `docs/engineering/REPOSITORY_CONTEXT.md`:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python -m unittest discover -s tests -p "test_*.py"
python -m se_harness --help
python -m se_harness doctor .
```

Run phase-appropriate work-order preflight and any focused tests required by the governing verification contract. No formatter or linter is currently declared as a repository gate; do not invent one and report it as required evidence.

Generated dashboards, bytecode, environments, raw build output, normalized distributions, and disposable acceptance repositories are derived and must not become formal authority.

## Why self-hosting needs three planes

The harness implementation cannot use unreleased candidate behavior as its only independent governor. Its workflow separates:

| Plane | Origin | Target | Assurance meaning |
| --- | --- | --- | --- |
| Released governor | hash-pinned published wheel selected by `.self-hosting/governor.toml` | a governor-created disposable repository and explicitly compatible read-only candidate data | independent bootstrap evidence |
| Candidate source | reviewed checkout at the candidate commit | source tests and declared ignored derived output | source implementation evidence |
| Candidate package | wheel built from a Git export and installed in a fresh environment | fresh-install and upgrade acceptance repositories outside the checkout | packaged behavior evidence |

`harnessctl identity` makes the role, Python executable, harness version, module/distribution/template origins, expected boundary, candidate commit, or governor digest machine-assessable. A mismatch fails its lane. A published governor may also run `harnessctl accept-candidate` against an exact wheel; its deterministic manifest remains evidence until an accountable assurance decision.

The current package and source version is 0.3.0, while `.self-hosting/governor.toml` intentionally still selects the independently published 0.2.1 wheel and digest. Publication does not automatically promote a candidate to govern itself.

## Building and releasing

A distribution build is allowed only under an approved release-bearing work order. The repository context defines the deterministic sequence: build the wheel and raw sdist in a provisioned build environment, then normalize the final sdist using the candidate commit timestamp.

Build success is evidence, not release authorization. The release lineage remains:

```text
clean candidate C -> ready VREC -> human verification
                  -> ready RLS  -> human release decision
                  -> authorized tag/GitHub Release/publication
```

The tag selects C, not a later governance commit. Production PyPI promotion verifies the already released wheel and sdist hashes and publishes those files without rebuilding. It remains a separate protected-environment decision.

No `harnessctl` command commits, pushes, tags, creates a GitHub Release, publishes, deploys, or exercises accountable promotion authority.

## Promoting a new governor

After a candidate is immutably published, a separate approved work order must identify the previous and proposed governor, release record, full released commit, immutable wheel URL/name, and SHA-256. A governor version that already contains the reconciliation protocol can then run `harnessctl reconcile-governor` as a read-only plan and, after review, with `--apply`. The command reads the target's migration contract and self-hosting workflow as verified data, never imports target code, preserves field-owned repository policy, and stops for authority-bearing decisions or incompatible schema jumps.

The descriptor, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `.engineering-harness.lock` change as one recoverable transaction. The implementation release that introduces this mechanism cannot use it to promote itself: publish it first, select it through the previously trusted promotion process, and use its released reconciler only for later targets. Until a promotion change is accepted, the prior descriptor remains authoritative.

See the authoritative [`SELF_HOSTING.md`](../engineering/self-hosting-boundary/SELF_HOSTING.md), repository [`REPOSITORY_CONTEXT.md`](../engineering/REPOSITORY_CONTEXT.md), and managed entry point [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md) before changing self-hosting controls.
