+++
id = "INT-IPK-001"
type = "intent"
title = "Make the exact current candidate installable for integration testing"
status = "approved"
owners = ["product-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "product-owner"
+++

# Intent: Make the exact current candidate installable for integration testing

## Problem

The candidate workflow already exports the exact Git commit, builds a wheel,
installs it in a fresh environment, and exercises a disposable repository. The
wheel is then discarded. A tester can see that `main` passed, but cannot obtain
the exact package that passed.

Installing directly from Git is possible, but the resulting package still
reports the public release version from `pyproject.toml` and
`se_harness/__init__.py`. After `0.6.0`, an unreleased `main` installation and
the released `0.6.0` evaluator therefore have the same version while containing
different bytes. That ambiguity is unsafe for testing an installed harness and
especially unsafe near the governing-evaluator boundary.

## Desired outcomes

- Every qualified `main` commit has a short-lived installable wheel that a
  tester can download without rebuilding source.
- Pull-request candidates can exercise the same packaging lane before merge.
- Package version, full commit, wheel digest, workflow run, and controlled
  version overlay are explicit and machine-readable.
- Linux and Windows install the same retained bytes without package-index
  access and exercise a disposable standard repository.
- The package is visibly non-promotable and cannot be confused with a release,
  PyPI publication, release record, or selected governing evaluator.
- Operators have copyable download, digest-check, install, smoke-test, and
  cleanup instructions.

## Success measures

| Measure | Baseline | Target |
| --- | ---: | ---: |
| Qualified `main` commits with a retained installable wheel | 0% | 100% |
| Retained wheels with unique commit-addressed version identity | 0% | 100% |
| Retained wheel bytes installed on Linux and Windows before availability | 0% | 100% |
| Integration artifacts that create a tag, GitHub Release, PyPI upload, RLS, or governor adoption | 0 | 0 |
| Documented clean-environment installation path | none | one supported path |

## Stakeholders

- Repository and engineering owners testing merged behavior before a release.
- Quality and assurance owners reproducing package-level failures.
- Release owners who need integration artifacts kept separate from promotable
  release distributions.
- Operators evaluating the new agent skill from an installed package rather
  than from a source checkout.

## Non-goals

- Publishing to PyPI or TestPyPI.
- Creating tags, GitHub Releases, release contracts, release records, or a new
  release version.
- Promoting an integration wheel into the release pipeline.
- Automatically selecting the integration package as a repository's governing
  evaluator or upgrading any managed repository.
- Retaining artifacts indefinitely or operating a permanent package index.
- Changing the version committed in candidate source.
