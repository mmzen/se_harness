# WO-REB-001 Implementation Evidence

Date: 2026-08-21

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, or deploy anything.

## Implemented scope

- Added schema-3 standard-lock evaluator identity with a canonical installed-payload manifest, optional paired wheel archive identity, strict field validation, and schema-1/schema-2 read compatibility.
- Added deterministic installed payload hashing and PEP 610 wheel-archive verification, including duplicate and contradictory hash rejection.
- Extended runtime identity with payload and installed-archive proof under the supported `released-evaluator` role.
- Replaced repository publication dependency on `.self-hosting/governor.toml` with a standard config-and-lock evaluator resolver.
- Migrated both PyPI evaluator phases and the release-bound Pages workflow to `evaluator_*`, `--role released-evaluator`, `--evaluator-payload-sha256`, and `--evaluator-wheel-sha256`.
- Added source, built-wheel, installed-CLI, workflow, and active repository-surface checks against retired executable contracts.

`WO-REB-002` mutation enforcement and release-readiness binding and `WO-REB-003` upgrade/recovery hardening were not implemented.

## Independent released-evaluator checks

The exact public se-harness 0.5.0 wheel was installed outside the checkout and previously proved with archive SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`. Its runtime identity reported isolated Python, disabled user site, absent `PYTHONPATH`, external module/distribution/template/entry-point origins, and no diagnostics.

- `python -I -m se_harness doctor <checkout>`: PASS.
- `python -I -m se_harness validate <checkout>`: PASS; 564 artifacts, 0 errors, and the same 44 legacy maintenance warnings present before this work.
- `python -I -m se_harness preflight <checkout> --work-order WO-REB-001 --phase review`: PASS.
- `harnessctl inspect <checkout>`: formal validation PASS; `WO-REB-001` was the sole active work order and `WO-REB-002`/`WO-REB-003` remained draft.
- `harnessctl dashboard <checkout>`: PASS; 564 artifacts and 2024 relations.

## Candidate and package checks

- `python -m unittest discover -s tests -p "test_*.py"`: PASS; 284 tests, 4 skipped.
- `python scripts/validate_engineering_artifacts.py --root .`: PASS; 564 artifacts, 0 errors, 44 unchanged legacy maintenance warnings.
- `python scripts/validate_release_distributions.py --root .`: PASS; no distribution-bearing records selected.
- `python scripts/check_portable_release_surface.py --repository .`: PASS.
- `git diff --check`: PASS.

A clean exported candidate wheel was built and inspected outside the checkout. The built wheel is candidate evidence only:

- Wheel: `se_harness-0.5.0-py3-none-any.whl`
- Wheel SHA-256: `ffe8c2b88ab240a9d3f27897358316fd25aa2e9dd6d1b831dd9f799532e3e53f`
- Installed payload manifest: `se-harness-installed-payload-v1`
- Installed payload SHA-256: `04dcd10481fff492c8c3f82060a82c442acfc2225e80c7a560dbe8cea3736761`
- Isolated installed identity: PASS with no diagnostics, exact PEP 610 archive agreement, checkout exclusion, isolated Python, disabled user site, and absent `PYTHONPATH`.
- Disposable consumer initialization and doctor: PASS; its schema-3 lock recorded the exact payload and archive identities above.

## Independent observation

Running `python -m se_harness doctor .` or candidate-source review preflight directly from the checkout reports that `scripts/generate_harness_dashboard.py` differs from the candidate standard template. The difference is pre-existing at `HEAD`: the installed root retains the released 0.5.0 topology threshold while the candidate template contains a later threshold/helper change. Neither file was changed by `WO-REB-001`, and the exact released evaluator doctor and preflight pass.

This observation was not remediated because applying candidate managed content to the installed root or changing its selected evaluator is outside `WO-REB-001` and requires its own governed upgrade. Candidate source remains candidate evidence, not root authority.

## Remaining lifecycle work

- No commit was created.
- No commit-bound VREC was prepared or verified.
- No root evaluator upgrade, release, tag, publication, or deployment occurred.
- Because commit-bound verification is classified `required`, the next stage needs an authorized clean candidate commit followed by `harnessctl capture-verification` for `WO-REB-001` and `VER-REB-001`.
