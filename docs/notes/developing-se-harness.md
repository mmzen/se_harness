# Developing SE Harness

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This note applies to contributors developing `se_harness`. It grants no implementation, verification, release, publication, deployment, or repository-upgrade authority.

The one-time emergency bootstrap published version 0.5.0a1 and used that exact external release to convert this checkout from its retired self-hosted evaluator controls. That released alpha evaluates the final 0.5.0 candidate through the ordinary standard repository lifecycle, with no self-hosting installation profile, evaluator descriptor, or special promotion command. Candidate source and packages remain evidence only and must not create formal artifacts, run root preflight, or manage lifecycle state.

The current source candidate version is 0.6.0. That candidate identity does not change the separately locked released root evaluator or grant verification, release, publication, deployment, or repository-upgrade authority.

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
templates/repository/standard/           one canonical repository installation
scripts/                                 portable validation, Explorer, CI selection, release support
repository_tools/                        non-packaged distribution and publication policy
tests/                                   installer, provenance, identity, package, and regression tests
docs/notes/                              non-authoritative human explanations
docs/engineering/                        self-governing formal artifact graph and evidence
.engineering-harness.toml                exact released root evaluator version and repository policy
.github/workflows/engineering-harness.yml exact released standard evaluator workflow
.github/workflows/candidate-evidence.yml  repository-owned source and package evidence
.github/workflows/publish-pypi.yml        one-input release orchestrator
.github/workflows/publish-dashboard-pages.yml release-bound Explorer recovery
```

The root validator and Explorer sources remain managed by the selected released installation. Candidate templates may evolve without overwriting root managed files before the candidate is published.

## Ordinary development checks

Use the commands confirmed by `docs/engineering/REPOSITORY_CONTEXT.md`:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python scripts/validate_release_distributions.py --root .
python -m unittest discover -s tests -p "test_*.py"
python -m se_harness --help
python -m se_harness doctor .
```

Run phase-appropriate work-order preflight and focused checks required by the governing verification contract. No formatter or linter is currently declared as a repository gate.

Generated dashboards, bytecode, environments, raw build output, normalized distributions, and disposable acceptance repositories are derived and must not become formal authority.

## Evaluator and candidate evidence

CI separates three identities without creating a second repository lifecycle:

| Plane | Origin | Purpose | Authority |
| --- | --- | --- | --- |
| Released evaluator | exact version recorded by the standard root installation, installed outside the checkout | root doctor, preflight, validation, and Explorer | evidence only; lifecycle authority remains human |
| Candidate source | reviewed checkout at `GITHUB_SHA` | full source regression and graph checks | evidence only |
| Candidate package | wheel built from an exact Git export and installed in a fresh environment | installed-origin, archive, init/adopt/upgrade, and package behavior | evidence only |

The standard managed workflow owns the released-evaluator lane. `.github/workflows/candidate-evidence.yml` owns candidate source and package jobs. Each job identifies its origin and proves it did not mutate the checkout. Passing candidate jobs cannot approve work, verify a VREC, release an RLS, publish, or update the root installation.

`harnessctl identity` supports `released-evaluator`, `candidate-source`, and `candidate-package` roles. `harnessctl accept-candidate` remains a generic verifier-owned black-box package contract; its manifest is evidence, not an assurance decision.

## Building and releasing

A promotable distribution build is allowed only under an approved release-bearing work order. The repository context defines the deterministic build, normalized sdist, bundle manifest, VREC, RLS binding, and publication sequence.

Build success is evidence, not release authorization:

```text
clean candidate C -> exact bundle manifest -> ready VREC -> human verification
                                         -> generic ready RLS -> bind repository distribution
                                                              -> human release decision
                                                              -> one-input authorized publication
```

The tag selects C, not the later governance commit containing the released record. Publication and Pages workflows validate their governance snapshots with the exact standard released evaluator selected by those snapshots. No `harnessctl` command commits, pushes, tags, creates a GitHub Release, publishes, deploys, or exercises accountable authority.

## Advancing the root evaluator

Candidate success never changes the root evaluator. After a later SE Harness version is immutably published, maintainers select it under a separate approved repository-upgrade work order, install that exact release outside the checkout, review ordinary `harnessctl upgrade`, and authorize `--apply` only when the plan is safe. The standard upgrade transaction preserves repository-owned content and fails closed on customization or integrity ambiguity.

See the current [standard repository lifecycle guide](../engineering/self-hosting-boundary/SELF_HOSTING.md), repository [`REPOSITORY_CONTEXT.md`](../engineering/REPOSITORY_CONTEXT.md), and managed [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md).
