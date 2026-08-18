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
.github/workflows/publish-dashboard-pages.yml repository-specific release-bound demonstration deployment
.github/scripts/publish_dashboard.py          Pages provenance and public-payload gate; not consumer tooling
.github/workflows/publish-pypi.yml             one-input release orchestrator and stable PyPI publisher identity
.github/scripts/publish_release.py              trusted release resolution, reconciliation, and result helper
scripts/create_release_bundle_manifest.py       deterministic pre-RLS distribution evidence producer
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

This is deliberately different from consumer CI. A consumer selects an already released SE Harness package, so its dedicated managed workflow uses one exact isolated released evaluator for all harness checks. It neither runs an older bootstrap that validates only itself nor calls `reconcile-governor`. The three-plane topology exists only because this repository is changing the evaluator implementation itself.

`harnessctl identity` makes the role, Python executable, harness version, module/distribution/template origins, expected boundary, candidate commit, or governor digest machine-assessable. A mismatch fails its lane. A published governor may also run `harnessctl accept-candidate` against an exact wheel; its deterministic manifest remains evidence until an accountable assurance decision.

The current package and source candidate is version 0.4.1, while `.self-hosting/governor.toml` intentionally continues to select the independently published 0.3.0 wheel and digest. Publication does not automatically promote a candidate to govern itself.

## Building and releasing

A distribution build is allowed only under an approved release-bearing work order. The repository context defines the deterministic sequence: build the wheel and raw sdist in a provisioned build environment, normalize the final sdist using the candidate commit timestamp, and use `scripts/create_release_bundle_manifest.py` to retain the exact filenames, hashes, epoch, candidate tree identity, and canonical checksum bytes. `harnessctl prepare-release --distribution-manifest <bundle.json>` validates and copies that structured identity into the ready RLS proposal. Historical RLS files remain valid without the optional block, but they cannot drive the new publication path.

Build success is evidence, not release authorization. The release lineage remains:

```text
clean candidate C -> exact bundle manifest -> ready VREC -> human verification
                                         -> ready RLS  -> human release decision
                                         -> one-input authorized publication
```

The tag selects C, not a later governance commit. After the released RLS is integrated into `main`, the release owner dispatches **Publish authorized SE Harness release** from `main` with only its `RLS-*` ID. The workflow derives every other identity, rebuilds C twice without credentials, creates or verifies the immutable tag and exact GitHub Release, and passes those final assets into the checkout-free PyPI job. The protected `pypi` environment remains a separate human decision. Exact existing state is replay-complete; partial or mismatched immutable state blocks without replacement.

The same main-context orchestration publishes the public Explorer demonstration from the later governance commit containing the released record. It keeps that snapshot distinct from the tagged candidate, validates it with the released governor, and uses target-local code only to render derived post-release output. `publish-dashboard-pages.yml` remains a main-only Pages recovery action taking the same RLS plus its explicit governance commit; it no longer deploys from a tag-ref release event. Neither workflow is copied into the consumer template or grants formal lifecycle authority. See [Publishing the SE Harness development dashboard](harness-dashboard-publication.md).

No `harnessctl` command commits, pushes, tags, creates a GitHub Release, publishes, deploys, or exercises accountable promotion authority.

## Promoting a new governor

After a candidate is immutably published, a separate approved work order must identify the previous and proposed governor, release record, full released commit, immutable wheel URL/name, and SHA-256. A governor version that already contains the reconciliation protocol can then run `harnessctl reconcile-governor` as a read-only plan and, after review, with `--apply`. The command reads the target's migration contract and self-hosting workflow as verified data, never imports target code, preserves field-owned repository policy, and stops for authority-bearing decisions or incompatible schema jumps.

The descriptor, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `.engineering-harness.lock` change as one recoverable transaction. The implementation release that introduces this mechanism cannot use it to promote itself: publish it first, select it through the previously trusted promotion process, and use its released reconciler only for later targets. Until a promotion change is accepted, the prior descriptor remains authoritative.

See the authoritative [`SELF_HOSTING.md`](../engineering/self-hosting-boundary/SELF_HOSTING.md), repository [`REPOSITORY_CONTEXT.md`](../engineering/REPOSITORY_CONTEXT.md), and managed entry point [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md) before changing self-hosting controls.
