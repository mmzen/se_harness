# WO-DOC-003 implementation verification

Date: 2026-08-11

Work order: `WO-DOC-003`

## Scope and authority

The repository owner approved the `REQ-DST-009..013` chain and bounded implementation with `ok go for implementation`. The implementation changed the public root README, static project metadata, deterministic focused tests, and this artifact packet. It did not build a distribution, change a version, modify either GitHub workflow or the independent baseline pin, mutate installed templates or lock data, create commit-bound records, access an external publication service, or change historical release facts.

## Implemented requirements

| Requirement | Result |
| --- | --- |
| `REQ-DST-009` | The public entry now leads with Python 3.11+, a virtual environment, unpinned PyPI installation, a synchronized exact 0.2.1 example, canonical links, and a new/existing-repository quick start. Source installation moved to distribution development. |
| `REQ-DST-010` | Windows PowerShell and POSIX activation, direct launcher paths, activation semantics, and `python -m se_harness` are explicit without assuming the Windows `py` launcher or a global binary. |
| `REQ-DST-011` | Package upgrade, read-only target plan, explicit transactional apply, and doctor are shown as four ordered operations; package upgrade alone is explicitly non-mutating for repositories. |
| `REQ-DST-012` | `pyproject.toml` selects `README.md`, references `LICENSE`, and declares canonical Homepage, Repository, Issues, and Releases URLs while preserving Python support, no runtime dependencies, and the console entry point. |
| `REQ-DST-013` | The exact README install version matches both metadata sources, release integrity describes protected exact-asset OIDC promotion and attestations without authority inflation, and conceptual CI prose defers the current baseline identity to the workflow. |

## Deterministic focused verification

Added `tests/test_public_onboarding.py` using only `unittest`, `pathlib`, `re`, and `tomllib`.

Before the implementation, `python -m unittest tests.test_public_onboarding -v` executed eight test methods and failed as expected with missing README sections and metadata: 15 failing assertions/subtests and two metadata/ordering errors. This established that the test contract detected the source-first baseline.

After the implementation, the same command passed all eight tests in 0.002 seconds. The checks cover:

- static README, license, URL, Python, dependency, and script metadata;
- synchronized `[project].version`, `se_harness.__version__`, and exact install example at `0.2.1`;
- PyPI-first installation and exclusion of source installation from that section;
- Windows and POSIX environment activation and direct launchers;
- new and existing repository quick-start commands;
- recent implemented governance and publication capabilities;
- ordered two-stage upgrades and non-mutation wording;
- source installation restricted to unreleased development guidance;
- production project links, exact configured baseline wording, OIDC, no rebuild, and attestations;
- UTF-8 decoding, placeholder/mojibake rejection, and local-link existence.

## Full supported-runtime verification

| Runtime | Command | Result |
| --- | --- | --- |
| Python 3.14.6 | `python -m unittest discover -s tests -p "test_*.py"` | PASS; 78 tests in 28.746 seconds, 2 expected skips |
| Python 3.11.9 | `C:\Users\mathi\AppData\Local\Python\pythoncore-3.11-64\python.exe -m unittest discover -s tests -p "test_*.py"` | PASS; 78 tests in 28.151 seconds, 2 expected skips |
| Python 3.14.6 | `python -m se_harness --help` | PASS; all nine commands listed |
| Python 3.11 | `...\python.exe -m se_harness --version` | PASS; `0.2.1` |

The expected skips are existing platform-dependent symlink cases and are unchanged by this work.

## Harness verification

| Check | Result |
| --- | --- |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS; 179 artifacts, 0 errors, 0 warnings |
| `python -m se_harness doctor .` | PASS; required, distribution, fragment, seed, schema-2 lock, and every managed-integrity check passed on Python 3.14.6 |
| `python -m se_harness preflight . --work-order WO-DOC-003` | PASS in start phase with the complete approved manifest |
| Two consecutive `python -m se_harness dashboard .` runs | PASS; 179 artifacts, 631 relations, 0 errors, 1 unrelated historical warning, identical snapshot `be6c502cdddf84b70d928b26988b5627e64c6b1ae634dc2208457578f9a75b60` before the final lifecycle transition |
| `python -m se_harness preflight . --work-order WO-DOC-003 --phase review` | PASS after the work order and implementation artifacts moved to `implemented` |
| Two consecutive final dashboard runs | PASS; 179 artifacts, 631 relations, 0 errors, 1 unrelated historical warning, identical snapshot `cda42fbde04adee903451cd0f4cbe9dd9a43fb7364b6839152d2899252861b9f` |
| `git diff --check` | PASS |

The Explorer warning is the pre-existing derived observation that `VREC-AGR-001` is still `ready` while its work is fully covered by later verified or released records. It is unrelated to `WO-DOC-003` and does not affect formal validation.

## Manual inspection

- The first public screen now presents purpose, Python support, canonical distribution links, PyPI installation, launcher discovery, and repository quick start before the detailed artifact model.
- Existing instruction ownership, governed workflow, formal artifact model, five Explorer questions, aggregate lineage, supersession, command reference, safety boundaries, installed layout, upgrade integrity, and CI bootstrap explanations remain present and consistent with current behavior.
- The production-publication section explicitly separates availability from product authority and states that existing PyPI metadata is immutable.
- `LICENSE` contains the GNU General Public License, Version 3 text; metadata references that retained file without introducing an unreviewed SPDX interpretation.
- The root README is the single public long description; no PyPI-specific duplicate or dynamic build input was added.

## Changed and protected surfaces

Implementation surfaces:

- `README.md`;
- `pyproject.toml` static project metadata;
- `tests/test_public_onboarding.py`;
- `docs/engineering/harness-distribution/` packet, acceptance scenario, and this evidence.

Confirmed unchanged:

- `.github/workflows/engineering-harness.yml` and `.github/workflows/publish-pypi.yml`;
- `.engineering-harness.lock` and every managed self-hosting file;
- `templates/repository/standard/`;
- `se_harness/` runtime and CLI behavior;
- package version `0.2.1`, build-system floor, dependencies, action pins, VREC/RLS records, tags, releases, and external services.

## Deferred release verification

No wheel or source distribution was built because repository policy requires a separately approved release work order. The next release contract must require inspection of generated Core Metadata, README and license inclusion, normalized sdist behavior, clean Python 3.11 installation, package-index rendering, canonical URLs, hashes, and attestations. Existing PyPI 0.2.1 remains immutable and does not receive this README or metadata retrospectively.

## Deviations and residual uncertainty

No implementation deviation from the approved local scope was required. Actual setuptools-generated metadata and PyPI rendering remain deliberately not assessed until an authorized future release build. The `license = { file = "LICENSE" }` form is statically consistent with the configured build contract, but its final generated representation is part of that deferred inspection.

## Completion boundary

The locally authorized documentation and static metadata implementation is complete. This evidence does not approve verification, create a commit or VREC, select a release, build a package, push a branch, open a pull request, tag, publish, or deploy.
