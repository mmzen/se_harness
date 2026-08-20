# WO-RCA-001 implementation evidence

## Authority and boundary

- Accountable approval received on 2026-08-20 for `INT-RCA-001`, `CAP-RCA-001`, `REQ-RCA-001` through `REQ-RCA-003`, `SPEC-RCA-001`, `ARCH-RCA-001` including its `no_significant_decision` assessment, `VER-RCA-001`, and `WO-RCA-001`.
- The approval authorizes bounded local implementation only. It does not authorize a candidate commit, branch push, pull-request update/readiness transition, issue edit, merge, VREC transition, release, publication, deployment, or operation.
- Draft PR #82 and issue #81 existed before this implementation. Neither was changed during implementation.

## Released-evaluator identity

- Role: `released-evaluator`.
- Version: `0.5.0a1` installed from public PyPI.
- Wheel SHA-256: `c6c99261202ed2519a2da0225d7972d465a0bec9fdf250acdd9a87f1e9694966`.
- Runtime identity schema: `se-harness-runtime-identity-v2`.
- Result: `passed: true`, no diagnostics.
- Python isolated mode: true; user site disabled; `PYTHONPATH` absent.
- Module, distribution, templates, Python executable, and `harnessctl` entry point all resolved inside the dedicated evaluator environment and outside the candidate checkout.

Candidate source and candidate-package observations were not used as root lifecycle authority.

## Start preflight and manifest reading

The external evaluator ran:

```text
harnessctl preflight . --work-order WO-RCA-001 --phase start --json
```

Result: `ready: true`, work order `approved`, no diagnostics, assurance `required`. The implementation agent read every returned manifest file before changing the authorized implementation surface. `WO-RCA-001` then moved to `in_progress`.

## Implemented surface

- Added `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`.
- Added an explicit RCA authority boundary and link to issue #81.
- Added immutable commit links, public alpha/final release links, exact final hashes, and the attestation observation.
- Updated `docs/engineering/README.md` to describe a standard governed repository and index `root-cause-analysis/`.
- Recorded accountable approval and active lifecycle state in the governing packet.
- Added this work-order-keyed evidence.

No source, test, managed template, lock, workflow, publisher, package metadata, version, release record, tag, public release, Pages, or root evaluator file changed. No abandoned local 0.5.0 draft was copied or altered.

## Immutable and public evidence reconciliation

### Workflow runs

All enumerated runs returned `status: completed` and `conclusion: success` from the GitHub API.

| Run | Workflow | Head commit |
| --- | --- | --- |
| `32337079106` | Emergency publish SE Harness 0.5.0a1 | `2e224cecec64deef035b2308ecba2029460b1628` |
| `32338517054` | Engineering Harness | `3685a948dc0f10ef245b3cda022b243384edb682` |
| `32338516996` | SE Harness Candidate Evidence | `3685a948dc0f10ef245b3cda022b243384edb682` |
| `32339092305` | Engineering Harness | `c42bbac20f14268ef162c9628dd1d2b45ea843af` |
| `32339092227` | SE Harness Candidate Evidence | `c42bbac20f14268ef162c9628dd1d2b45ea843af` |
| `32339451590` | Emergency publish SE Harness 0.5.0 | `d7755566d39b0fba5087b7589bb290e455ed5282` |
| `32340101925` | Engineering Harness | `43c05f4235fbcf21d154ff4350cd6a87549f0bea` |
| `32340102021` | SE Harness Candidate Evidence | `43c05f4235fbcf21d154ff4350cd6a87549f0bea` |

### Releases and distributions

- GitHub `v0.5.0a1`: public prerelease, not draft, three assets.
- GitHub `v0.5.0`: public final release, not prerelease or draft, three assets.
- PyPI `0.5.0a1` wheel SHA-256: `c6c99261202ed2519a2da0225d7972d465a0bec9fdf250acdd9a87f1e9694966`.
- PyPI `0.5.0a1` sdist SHA-256: `de73d5cc22cc0ba5c6d941c92523bcebe10207a044e2dbad81eaddb8b6b80dda`.
- PyPI `0.5.0` wheel SHA-256: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- PyPI `0.5.0` sdist SHA-256: `c575bac2b61837859e03fda852d9a3a1cba8516106a2f3f3ad3b732b5a28bc42`.
- PyPI integrity API returned one attestation bundle for each final distribution.
- GitHub issue #81 was open and publicly readable.

These are technical observations. They do not retroactively create normal lifecycle authorization for the emergency releases.

## Local verification

| Check | Result |
| --- | --- |
| Released `0.5.0a1` `harnessctl doctor .` | PASS; managed and distribution files unchanged |
| Released `0.5.0a1` `harnessctl validate .` | PASS; 521 artifacts, 0 errors, 44 pre-existing maintenance warnings, none in the RCA domain |
| `python scripts/validate_release_distributions.py --root .` | PASS; 0 distribution-bearing records in this candidate change |
| Candidate `python -m se_harness --help` | PASS; candidate-source observation only |
| RCA path and single-H1 check | PASS |
| Required-section check | PASS; no missing sections |
| Formal-front-matter and `status =` scan of the RCA | PASS; absent |
| Issue #81 link check | PASS |
| Local user-path and trailing-whitespace scan | PASS; none found |
| Forbidden changed-surface scan | PASS; no product, managed, workflow, self-hosting, package, or release path |
| `git diff --check` | PASS |

The first complete test invocation used an ambient Python installation whose `se-harness 0.4.1` distribution metadata lived outside this checkout. One candidate-source identity test correctly failed with `RID018`; 262 tests passed and four were skipped. This was test-environment contamination, not a product or RCA failure.

The suite was rerun from a fresh virtual environment with no installed `se-harness`, matching the hosted candidate-source model. Result: 263 tests passed, four skipped, in 76.890 seconds.

## Review readiness and inspection

- Released-evaluator review preflight for `WO-RCA-001` returned `ready: true`, work order `implemented`, and no diagnostics.
- `harnessctl inspect .` reported formal validation PASS, 521 artifacts, 1903 relations, zero errors, the unchanged 44 maintenance warnings, and one expected assurance-pending item for `WO-RCA-001`.
- The inspection recommendation is to create a clean candidate commit and then prepare commit-bound verification; neither action has been authorized or performed.
- `harnessctl dashboard .` passed with 521 artifacts, 1903 relations, zero errors, 44 warnings, and manifest SHA-256 `692070d81368ee567eff3768b44d59045a94fc5599fe71a7334e7dcbacb9770b`.
- Final formal states are `approved` for the intent, capability, requirements, specification, architecture, and verification contract, and `implemented` for `WO-RCA-001`.
- Final worktree inspection lists only `docs/rca/`, `docs/engineering/README.md`, and `docs/engineering/root-cause-analysis/` changes.

## Manual assessments

- The RCA identifies one primary architectural/process cause and keeps contributing factors subordinate.
- The analysis is blameless and does not infer personal intent.
- Completed corrective actions and unimplemented recommendations are separated.
- The RCA states that it is supporting documentation and that issue #81 grants no authority.
- `ARCH-RCA-001` applies the existing standard-repository boundary and introduces no controlled significant-decision trigger; the accountable owner explicitly accepted this assessment.

## Residual uncertainty

- Causal analysis still requires accountable human review and cannot be proven solely by automated checks.
- Public presentation URLs may change even though immutable commits, run IDs, tag targets, filenames, and hashes remain durable.
- Hosted PR checks for the implemented candidate cannot run until a separately authorized commit and PR update.
- Commit-bound verification is required; no ready or verified VREC exists before a clean candidate commit.

## External actions

- Candidate commit: not performed.
- Branch push or PR #82 update: not performed.
- PR readiness transition or merge: not performed.
- Issue #81 edit: not performed.
- VREC transition, release, tag, publication, deployment, or operation: not performed.
