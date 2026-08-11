# Verification Evidence: WO-DST-001

Date: 2026-08-11

Scope: `REQ-DST-001` through `REQ-DST-006`, `SPEC-DST-001`, `ARCH-DST-001`, `ADR-DST-001`, and `VER-DST-001`.

## Results

| Verification | Result |
|---|---|
| `python scripts/validate_engineering_artifacts.py --root .` | PASS; 15 artifacts, 0 errors, 0 warnings |
| `python -m unittest discover -s tests -p "test_*.py" -v` | PASS; 13 tests, 1 environment-dependent symlink case skipped |
| `python -m compileall -q se_harness tests scripts` | PASS |
| UTF-8 and trailing-whitespace scan across source, templates, tests, scripts, and engineering docs | PASS |
| Source `init`, `adopt`, `validate`, `dashboard`, `doctor`, and `upgrade` contract cases | PASS |
| Known-conflict all-or-nothing behavior | PASS; no partial installed files or managed blocks |
| Traversal, unsafe lock path, invalid project name, malformed marker, and customized-file preservation cases | PASS |
| New-repository initialization and dashboard generation | PASS; 26 standard template targets installed |
| Existing-repository adoption and dashboard generation | PASS; prior agent and ignore content preserved; observations remained non-authoritative |
| `python -m pip wheel . --no-deps --no-build-isolation` using bundled Python 3.12 | PASS; `se_harness-0.1.0-py3-none-any.whl` |
| Isolated wheel installation and `harnessctl init`, `doctor`, `validate`, and `dashboard` | PASS |
| Isolated `python -m pip check` | PASS; no broken requirements |
| Final distribution Harness Explorer generation | PASS; 15 artifacts, 38 relations, 0 errors, 0 warnings |

Final deterministic dashboard snapshot SHA-256: `a36b37419870d401625048ae277ba1a5a47486da921ff688f00ebe2b2573f7f1`.

Built wheel SHA-256 observed during verification: `d43419cc70495e00403e859266d9c9e4ec2533efe11c6a3473bf9003b44fc92a`.

## Requirement conclusions

- `REQ-DST-001`: one `templates/repository/standard/` tree exists; the CLI has no profile option and rejects one as unknown.
- `REQ-DST-002`: initialization and adoption are fully planned before writes; ordinary conflicts stop with no mutation; shared root content uses bounded markers.
- `REQ-DST-003`: validation, dashboard, and doctor operate against installed repository-local tools with preserved exit outcomes.
- `REQ-DST-004`: lock hashes distinguish unmodified and customized content; plan is read-only and apply preserves customizations.
- `REQ-DST-005`: adoption reports label detections as observations and require human-authored, human-approved intent and requirements.
- `REQ-DST-006`: the console entry point and complete template are present in the wheel; an isolated installed command completed the operating flow.

## Deviations and residual risks

- No minimal or offline installation mode was implemented. The standard installation still contains the self-contained dashboard, but it is not exposed as a selectable profile.
- Windows on this host did not permit creation of a directory symlink, so that one portable test was skipped. Deterministic path traversal and malicious lock-path tests passed; the symlink rejection code remains exercised on hosts that allow symlink creation.
- The system Python lacks an importable `setuptools.build_meta`; the bundled Python build environment supplied setuptools 83.0.0. This is a build prerequisite, not a runtime dependency.
- The wheel was built and installed locally but was not published. No remote Git repository, package registry entry, release promotion, or production operating acceptance was authorized.
- A Git repository was initialized on branch `main`; no initial commit was created because committing was not requested.
