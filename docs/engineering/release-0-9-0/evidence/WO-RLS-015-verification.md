# WO-RLS-015 implementation evidence

artifact: WO-RLS-015
checkpoint: handoff
formal_snapshot_sha256: 3fa898f0c027fdfac8f6c54df562d290018a52f7d95ac0a66c70957f48644ae8

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## 1. What the candidate is

The candidate is the commit that adds this file's sections 1 and 2 and the
index line. No version move is needed: `pyproject.toml`,
`se_harness/__init__.py` and the README install line read 0.9.0 since
`WO-HUP-008`. The packaged bytes are those of `main` at `effbcbc`, the
merge of #251; nothing under `se_harness/`, no template and no workflow
changes on this branch. The governing evaluator for every reading below is
exact public 0.8.0, installed outside the checkout from the wheel file whose
digest `RLS-SEH-017` binds, invoked with `-I`.

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.8.0, outside the checkout, `-I` | 1,088 artifacts, 0 errors, 473 pre-existing maintenance warnings |
| `doctor` | released 0.8.0 | 0 FAIL |
| `preflight --work-order WO-RLS-015 --phase review` | released 0.8.0 | ready, no diagnostic |
| `release-unit --from v0.8.0 --to <candidate> --contract REL-SEH-020` | released 0.8.0 | section 3 (re-run at the candidate) |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate, `python -s`, no user site | section 3 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (5 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout from a clean tree (`se_harness-0.9.0-py3-none-any.whl`, `f3fa54573a1760e83c72e3d134d37d40f299bf8a16a32a2eaf8d00631341255a`) and its `harnessctl` entry point |
| `repository_tools.upgrade_rehearsal`, twice | released 0.8.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.8.0 -> 0.9.0 | lock 3 0.9.0); `semantic_sha256` `74437a1ccea16fc4937d1224345949db481bbbf8236edd55fb40b5808f800ce0` in both, equal |
| `python scripts/run_tests.py --scale full` | candidate, Linux, CPython 3.12 | 1,117 tests, 1 failure, 4 skipped; the failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`, the file-mode artefact of this checkout that passes on the hosted runner; the Windows figure is the hosted lane's |
| `harnessctl check --checkpoint handoff` | released 0.8.0 | section 5 |

## 3. Census re-run at the candidate

`harnessctl release-unit . --from v0.8.0 --to 8573608 --exempt <the nine contract commits> --contract REL-SEH-020`, released 0.8.0: traces `WO-RLS-015` only (this branch's commits carry a parseable trailer), untraced 0, exempted 9. The derivation reports the same shape the contract declares once `WO-RLS-015` reaches `implemented`: at this reading it is `in_progress`, so the derivation is expectedly incomplete and `E-CIP-001` reports `gates` differ (the six existing members are established by the allow-list, not by a trailer this period can parse, exactly as the contract's census section records). No difference beyond that and the nine recorded exemptions; not a stop condition.

## 4. Build of record

Run on 2026-08-28 on this Linux host through the pinned producer image
(`docker` reached the daemon through `sudo` for this invocation only, no
durable system change), at the exact candidate `8573608`:

| Reading | Value |
| --- | --- |
| command | `python -m repository_tools.release_build replay --repository . --commit 8573608 --version 0.9.0` |
| state | `exact`; two producer runs `a` and `b` byte-identical |
| producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64, digest-pinned by `release/build-toolchain.lock` |
| recipe | `release/build-recipe.json`, `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| wheel | `se_harness-0.9.0-py3-none-any.whl`, `e851bccf72e5769b7348119f43a6e9e112f3f3926e7f19d14a24bf3951441d18` |
| sdist | `se_harness-0.9.0.tar.gz`, `6fd34bd721fdbbeccb1a9b8e174fcc44e67e5aec6cedec2a835e0468e3182d58` |
| checksums | `SHA256SUMS`, `d4ccee54b44a3f5d563adc5bf539503042f9b0ffb009dea416af60964ead2f6b` |
| source manifest | `d71715be73cc32b307c2664214b9f42b70439eae1faac60339b87f6577181d0f`, `source_date_epoch` 1787955121 |
| bundle manifest | `scripts/create_release_bundle_manifest.py` → `se-harness-release-bundle/v2`; to be retained as `docs/engineering/release-0-9-0/evidence/RLS-SEH-018-bundle.json` when the record is prepared |

The hosted `release-candidate-replay.yml` dispatch on the review ref, before
the release decision, must reproduce the same wheel and sdist digests.

## 5. Deviations, recorded for the completion decision

1. Governing evaluator is exact public 0.8.0 (the current root, `WO-HUP-008`),
   as `REL-SEH-020` states; the 0.7.1 of earlier packets does not apply.
2. The candidate's evidence packet (section 6) carries the machine header the
   candidate reads and the legacy substring lines the governing 0.8.0
   evaluator reads, as under `WO-ECP-002`; both bind the same formal
   snapshot.
3. The workstation suite failure `test_declared_mode_set_is_what_a_posix_export_already_carries`
   is the file-mode artefact of this checkout; it passes on the hosted runner.

## 6. Handoff checkpoint binding

Bound below with the released 0.8.0 evaluator over the complete changed-path
set; the formal snapshot and the legacy lines follow.

Governing 0.8.0: handoff Completed once the legacy lines below were retained; before them the only non-pass predicate was QGP-G4I-EVIDENCE. Complete changed-path set (6 paths, the work order's own file omitted as 0.8.0 predates ECP-CHG-007):

```
docs/engineering/README.md
docs/engineering/release-0-9-0/evidence/WO-RLS-015-verification.md
docs/engineering/release-0-9-0/README.md
docs/engineering/release-0-9-0/release/REL-SEH-020.md
docs/engineering/release-0-9-0/work-orders/WO-RLS-015.md
docs/notes/developing-se-harness.md
```

Legacy binding for the 0.8.0 governor:

artifact: WO-RLS-015
checkpoint: handoff
formal_snapshot_sha256: 3fa898f0c027fdfac8f6c54df562d290018a52f7d95ac0a66c70957f48644ae8

## 7. Hosted lanes

Pull request #252 at `2950b7c`: all 13 lanes pass, both platform legs of the suite and the 0.8.0-to-0.9.0 upgrade rehearsal included; the publication rehearsal qualified this commit's own recipe in candidate mode.

## 8. Build re-verified at the bound candidate

The replay was re-run at `8adfe1b` (the commit `VREC-SEH-018` binds; the delta from `8573608` is evidence-only, no packaged byte): `state = exact`, two byte-identical producer runs, wheel `e851bccf…` and sdist `6fd34bd7…` equal to section 4, `source_date_epoch` 1787955573. The bundle manifest at this commit is retained as `RLS-SEH-018-bundle.json` when the record is prepared.
