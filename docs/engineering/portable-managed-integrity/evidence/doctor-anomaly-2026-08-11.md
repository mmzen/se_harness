# Managed-File Doctor Anomaly

Observed on 2026-08-11 after pull request #4 was merged into `main` at `ef2a112973addc340c0151c837cec1955d9bb7b6`.

## Trigger

The governance preflight for transitioning `VREC-AGR-001` from `ready` to `verified` ran:

```powershell
python -m se_harness doctor .
```

Doctor reported six managed files as customized or missing. The transition was restored to `ready`; no governance commit, push, or pull request was created.

## Hash observations

| Managed path | Lock SHA-256 | Raw checkout SHA-256 | LF-normalized SHA-256 | Diagnosis |
|---|---|---|---|---|
| `docs/engineering/TRACEABILITY.md` | `dc35f9e2b2697aa04d12d1b6a9ebd3555bbd335e56298d896a3d2784d547adfd` | `9322702c7071d2f8cc212243d54d3b6d92b7548f3615f2e829f434652a95df6d` | `dc35f9e2b2697aa04d12d1b6a9ebd3555bbd335e56298d896a3d2784d547adfd` | newline representation only |
| `docs/engineering/WORKFLOW.md` | `37fc350b66fac659636f2cdc384e49e709f148f71b4bd572f92abb7ec878d8fe` | `4aff40b2d9026f65b355304eb10fdf82ac6df0939d5a930330f64eda1022f4b9` | `37fc350b66fac659636f2cdc384e49e709f148f71b4bd572f92abb7ec878d8fe` | newline representation only |
| `docs/engineering/templates/RELEASE_RECORD.template.md` | `61b30eb7f9f104e0278e953a3fa8d8397f5c346e680e0320890344e49fa43bb3` | `4aaa96676f7678e302cc6f1c35cd3564fc78e90d9fef351921eb3065a5505247` | `61b30eb7f9f104e0278e953a3fa8d8397f5c346e680e0320890344e49fa43bb3` | newline representation only |
| `docs/engineering/templates/VERIFICATION_RECORD.template.md` | `4725b1bbf400a7a3a9b37002ba2802d4009a89a5f1e74659a971e716217c2a96` | `583a2affdd0071ff87cdfa64d59271be2962d2e24b703ee59cd17d45b8b73cc5f` | `4725b1bbf400a7a3a9b37002ba2802d4009a89a5f1e74659a971e716217c2a96` | newline representation only |
| `scripts/harness_explorer/index.template.html` | `c168b3a6a858d19bcb994ab13780c0c7473ea586850b1d3f7d1b2a5b9da66f4f` | `41a34e063c93f7b7e519bdcbbff36eb99d1daa5c630de3cf6511b1f29ced5ec6` | `c168b3a6a858d19bcb994ab13780c0c7473ea586850b1d3f7d1b2a5b9da66f4f` | newline representation only |
| `scripts/validate_engineering_artifacts.py` | `09ccfdcdcfd40d45fcc7704985374f6bfebc00aa1c1a924d221e0af6a1495c6f` | `10786dd6fe95e8aa3a019653081fe97c52c90a2e08ccb2d8eaf2647ae5a99ddd` | `a3a24d64e0855a9bcb7940103879031936e95102345ba19012f5e2550e22d5c7` | stale lock digest plus checkout newline representation |

The source validator and its canonical standard-template copy were byte-identical at observation time. The stale digest is therefore a lock-generation or lock-maintenance defect, not source/template divergence.

## Passing controls

- Artifact validation: 70 artifacts, 0 errors, 0 warnings while the two proposed governance work orders were present.
- Unit suite: 37 tests passed; 2 conditional tests were skipped because the Windows host lacks symbolic-link privilege.
- CLI help: passed.
- Candidate `3f3ba521d7b19455e1f2eacb9aeea42928806aef`: available locally and an ancestor of the merged governance checkout.
- Diff hygiene: passed.

## Consequence

`VREC-AGR-001` remains `ready`. A corrected candidate must make integrity semantics portable, regenerate a consistent self-repository lock through the supported mechanism, rerun the verification contract, and capture a new commit-bound verification record before an assurance transition is reconsidered.
