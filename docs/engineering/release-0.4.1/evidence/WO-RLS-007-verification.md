# WO-RLS-007 implementation and preliminary qualification evidence

Date: 2026-08-17

Candidate version: `0.4.1`

Approved-packet base commit: `337f1e269ee692cd84d0796bdaddfd1b186aa90b`

Approved-packet base tree: `e56e36f143e2f3c02fea8c4e409a6927f4921d00`

Previous release candidate and tag target: `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61` (`v0.4.0`)

This evidence is retained by the working-tree candidate. A commit cannot truthfully contain its own not-yet-created identity. The exact candidate commit, tree, timestamp, Git export, final artifact hashes, released-governor replay, and aggregate snapshot therefore remain prerequisites to the later `VREC-SEH-007` proposal. No verification, release, tag, publication, deployment, or governor-promotion decision is asserted here.

## Authorized release scope

The approved aggregate payload is exactly:

- `WO-DPG-001`;
- `WO-DST-011`, `WO-DST-012`, `WO-DST-013`, `WO-DST-014`, `WO-DST-015`, and `WO-DST-016`; and
- release-integration work order `WO-RLS-007`.

The complete verification-contract union is `VER-DPG-001`, `VER-DST-001`, and `VER-DST-010` through `VER-DST-015`.

The eight planned evidence inputs are:

- `docs/engineering/dashboard-publication/evidence/WO-DPG-001-verification.md`;
- `docs/engineering/harness-distribution/evidence/WO-DST-011-verification.md` through `WO-DST-016-verification.md`; and
- this `docs/engineering/release-0.4.1/evidence/WO-RLS-007-verification.md` file.

`WO-RLS-006`, `VREC-SEH-006`, and `RLS-SEH-006` belong to the already released 0.4.0 governance transaction and are explicitly excluded. Historical governance-only commits, merge commits, and derived Pages publication runs are not separately admitted. The allow-list is not inferred from dates, statuses, or every commit after `v0.4.0`.

## Version and protected-control changes

Candidate identity is 0.4.1 in:

- `pyproject.toml` and `se_harness.__version__`;
- README and installation-note public pins;
- current conceptual and self-hosting development notes;
- `.engineering-harness.toml`;
- `.github/workflows/engineering-harness.yml` candidate input;
- the active rendered `ENGINEERING_HARNESS.md`; and
- `.engineering-harness.lock` tool identity and protected-file hashes.

The lock records these canonical protected hashes:

- `.engineering-harness.toml`: `4768b77aeda7d47a8a97b59ef2b429a4f9cfd618be8a37b72a79cfbadca8526d`;
- `.github/workflows/engineering-harness.yml`: `b7492418644a245c9f4d1dfe58191d9f86d6af5f654182085622f653e1bf16ab`; and
- `ENGINEERING_HARNESS.md`: `2aa3532b9e8f589eba69e2cbee053b02ad86a80cddefa7ea182fe31f5cae960e`.

`.self-hosting/governor.toml` is unchanged. It continues to select version 0.3.0, tag `v0.3.0`, wheel `se_harness-0.3.0-py3-none-any.whl`, release record `RLS-SEH-005`, candidate commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, and wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`. The self-hosting workflow retains that governor identity and immutable reusable-workflow pin; only its candidate-version input changed to 0.4.1.

## Preliminary repository qualification

All commands below completed with exit code 0 unless explicitly described otherwise.

- Start preflight passed for `WO-RLS-007` with commit-bound verification classified `required` by `repository-owner`.
- `python -m se_harness doctor .` passed required files, distribution parity, lock integrity, repository-specific self-hosting controls, and Python checks. It confirmed governor 0.3.0 and reported only known historical non-canonical-location observations.
- Formal validation passed with 446 artifacts, zero errors, and 42 maintenance warnings. Structure, governance, and policy planes contain zero errors and zero warnings. The 42 warnings are the existing declared legacy-location and architecture-compatibility backlog; none was introduced, hidden, or converted into a health score by this work.
- The complete Python 3.14.6 suite passed 232 tests with three conditional skips.
- The complete Python 3.11.9 suite passed 232 tests with the same three conditional skips.
- The focused self-hosting, progressive-documentation, public-onboarding, and instruction-architecture suite passed 69 tests.
- Workflow topology and package-owned command assertions passed in the complete suites. The standard consumer render contains one job, exact version 0.4.1, the `consumer-evaluator` role, isolated `python -I -m se_harness` operations, and no governor or candidate-source lane.
- Two inspection JSON projections were byte-identical, SHA-256 `fa3503949aafbfe093ccd1ab1c32199758f2ef6636df04d2a447ca805298cb02`. They reported 446 artifacts, 1,612 relations, zero error findings, 42 maintenance warnings, and 38 informational lifecycle observations.
- Two Explorer generations each emitted 531 files. All 530 authoritative payload/resource files were byte-identical; both recorded manifest SHA-256 `bb0ed24a85ee83d4e3628f012972a58d2464dfc976bc0b6ffc630a304a2ac0bc`, rendered HTML SHA-256 `be2ccc80b0b7a5ce4132e715e2228486e5cd696619c2989d0242ae369e5dcdb3`, and 528 integrity-addressed resources. Only `generation-summary.json` differed, as designed, in its observational `generated_at` and `elapsed_ms` fields. Those fields are not an authoritative payload manifest and are not represented as deterministic evidence.
- `git diff --check` passed. The changed-path ledger contains only the approved version/protected controls, public version guidance, work-order lifecycle, and this evidence.

The complete suites cover Pages exact-set validation, browser acquisition integrity and race/failure behavior, init/adopt/upgrade/conflict fixtures, event selection, checkout/environment manipulation, archive rejection, and candidate-source/package role checks. No new dependency or policy profile was added for this release integration.

Immediately after the honest `in_progress -> implemented` transition and initial evidence retention, review preflight, formal validation, doctor, and protected canonical-hash checks passed again. Inspection exposed exactly one expected assurance item, `WO-RLS-007`, with the `prepare-commit-bound-verification` suggestion; it did not imply that assurance had occurred. Two review projections were byte-identical at that point, SHA-256 `2031b527977e1dc227412a08d7cae019a23ac24edd2ff38f2930faa5b16e7562`. Two review Explorer runs emitted 532 files with manifest SHA-256 `4d4e5360edf2f899f0a67aa16d022b326d4cb338c150f804204b9520e8116bc`, rendered HTML SHA-256 `550ee61d695c76ee04cea836d941606d73c85b7a6694d287187b687c8e939a41`, and 529 resources; again, only the observational generation summaries differed. These are implementation-review observations, not the later exact candidate artifact snapshot.

## Preliminary reproducible package exercise

Two independent working-tree builds used Python 3.14.6, `python -m build --wheel --sdist --no-isolation`, `SOURCE_DATE_EPOCH=1786988208`, and the same explicit preliminary normalization epoch, which is the approved-packet commit timestamp.

- wheel A SHA-256: `f0dd9530057a1ad383211e3b14b1531a7318875eaf4eaa4203fd3e60d4e953c3`;
- wheel B SHA-256: `f0dd9530057a1ad383211e3b14b1531a7318875eaf4eaa4203fd3e60d4e953c3`;
- raw sdist A SHA-256: `f7f31582dfe5aef0ce62c68ef3dcb7011ce8a861c92927ed1405c225da6d4cbf`;
- raw sdist B SHA-256: `52ab44b5e27c847ecb56eba82d5921e20cc436b98b093e9d0207cd8e7a07b15c`;
- normalized sdist A and B SHA-256: `8f7ecefd78023cf998ca87b9cb4d11ca3d76bd6e3cd204b1a81e39ada98c33a5`; and
- wheel rebuilt from the safely normalized sdist SHA-256: `f0dd9530057a1ad383211e3b14b1531a7318875eaf4eaa4203fd3e60d4e953c3`.

The raw gzip containers vary before normalization as designed. Wheels are byte-identical, normalized sdists are byte-identical, and the reconstructed wheel equals both direct wheels. The normalizer validated canonical member paths, uniqueness, and ordinary file/directory types before extraction. Generated checkout-local `build/` and `se_harness.egg-info/` directories were absent before the exercise and removed after each direct build; repository-owned content was not deleted.

Setuptools emitted the existing deprecation warning for the TOML-table form of `project.license`, with a stated 2027-02-18 deadline. It does not affect current metadata, build success, archive safety, or reproducibility. Changing license metadata is outside this release-integration work order and remains later governed maintenance.

## Fresh Python 3.11 package exercise

The wheel reconstructed from the normalized sdist installed with `pip --no-index --no-deps` into a new Python 3.11.9 virtual environment. Every authoritative command ran from outside the source checkout and proved:

- package and distribution version 0.4.1;
- module and Python executable origins below the isolated environment, not the checkout;
- initialization of all 34 standard consumer files;
- managed-integrity doctor success;
- formal validation with zero artifacts, errors, or warnings;
- inspection with zero findings;
- Explorer generation with zero errors;
- an idempotent 34-file safe upgrade;
- adoption beside a pre-existing repository file; and
- one exact 0.4.1 consumer workflow job using package-owned isolated commands, with no self-hosting governor lane.

The direct source environment, reconstructed candidate package, disposable consumer repositories, and selected released governor remain separately identifiable. The candidate package was not treated as its own independent governor.

## Residual checks and authority boundary

The exact candidate commit and timestamp do not exist yet. After the authorized clean candidate commit, qualification must be replayed from an exact Git export at the candidate epoch, the final distribution and archive hashes must be recorded, and the released 0.3.0 governor must assess that exact candidate/package boundary before `VREC-SEH-007` can be prepared as `ready`. Hosted three-plane CI remains later external evidence.

No push, merge, ready verification record, verification transition, release record, release decision, tag, GitHub Release, PyPI publication, Pages deployment, governor reconciliation, force push, or history rewrite was performed during this implementation step.
