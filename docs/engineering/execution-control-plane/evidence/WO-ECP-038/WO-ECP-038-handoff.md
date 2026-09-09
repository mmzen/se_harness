```toml
artifact = "WO-ECP-038"
checkpoint = "handoff"
formal_snapshot_sha256 = "bf11988db6480cec3d29197069bf5b765e189fa2105378e5bac12c53d79ddf79"
rebound_at = "2026-09-09T12:57:46Z"
```

# WO-ECP-038 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`repository_tools/release_build.py` exposes the recipe form under one name,
`recipe_json_bytes`; the alias `canonical_json_bytes` that `WO-ECP-032` kept
for the lane script is gone, and `scripts/replay_release_build.py` imports
and calls `recipe_json_bytes`. The function's body is unchanged, so every
recipe and replay document keeps its bytes and every digest on record
stands. One test pins the module's names and the script's import. No
workflow, recipe, lock, digest or other name changed; `repository_tools`
still imports only the standard library and its own package.

## Evaluators

- Governing: released `se-harness 0.17.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0170` from the wheel file whose
  digest equals `RLS-SEH-026`, for `validate`, the preflights, this packet
  and the handoff check.
- Candidate: this checkout, branch `wo/ecp-038-alias` off `main` at
  `95eb0f6a` (the 0.17.0 root), PR #430; the change commit is `51a704e1`.

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `git diff main -- repository_tools/release_build.py` | workstation | three lines removed (the alias and its two comment lines); no line of `recipe_json_bytes` changes |
| the old name in the module and the script | workstation | none left; the module's docstring keeps its historical sentence "Renamed from `canonical_json_bytes`" |
| `tests/test_release_build.py` | candidate, Windows | 24 tests, OK (2 platform skips); `RecipeJsonBytesNameTests` added |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full --workers 8` | candidate, Windows 11 (CPython 3.13.3) | 1119 tests, 1 error, 23 skipped: the workstation baseline (the read-only `.git` teardown error of `test_artifact_authoring.IdentifierAllocationTests`) plus the one test this work order adds; the 23 skips are the platform set plus the complexity test that runs only where radon is installed |
| `validate --advisories` | exact 0.17.0 | 1,446 artifacts, 0 errors, 46 warnings (all `W013`, pre-existing), 0 advisories |
| `preflight --work-order WO-ECP-038 --phase start` | exact 0.17.0 | PASS |
| `preflight --work-order WO-ECP-038 --phase review` | exact 0.17.0 | PASS |
| `repository_tools` import barrier | workstation | `release_build.py` imports the standard library and its own package only (`ARCH-REB-013`); the inventory tests of the suite read the same |
| handoff check | exact 0.17.0 | completed over the Git-derived change set; the schema-2 result is retained beside this packet as `handoff.json` |

## Hosted lanes

At the change head `51a704e1` (pull-request event of PR #430): Publication Rehearsal 34353497766 `success`, its candidate leg running `scripts/replay_release_build.py` with the renamed import (the reading the work order names); SE Harness Candidate Evidence 34353497476 `success` (the suite on Linux, the package evidence, the upgrade rehearsal on both platforms, the integration package); Predecessor Evaluator Assessment 34353497495 `success`; Engineering Harness 34353497500 stopped at the handoff step on `QGP-G4I-EVIDENCE`, no readable evidence yet, the expected reading before this packet existed. The lanes at the evidence and completion heads are read the same way in the pull request.

## Material non-effects

No byte of `recipe_json_bytes`, `release/build-recipe.json`,
`release/build-toolchain.lock` or any recorded digest changed. No workflow
file changed. The `canonical_json_bytes` of `repository_tools/json_bytes.py`
and its local wrapper in `.github/scripts/build_integration_package.py` are
the integrity primitive and stay as they are. No record is prepared:
commit-bound verification is `not_required`.
