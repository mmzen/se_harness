# WO-RLS-014 candidate qualification evidence

Work-order-keyed evidence for `WO-RLS-014` under `REL-SEH-019` and
`VER-DST-001`. Readings taken on 2026-08-28 on Linux (CPython 3.12.13, Git
2.52.0) from branch `governance/release-0-8-0-packet`, whose five packet and
governance commits all carry the `Harness-Work-Order: WO-RLS-014` trailer, at
`f356a01` (the tree the candidate commit adds this file to). Windows figures
come from the hosted lanes, section 6.

## 1. What the candidate is

The candidate is the commit that adds this file. No version move is needed:
`pyproject.toml`, `se_harness/__init__.py` and the README install line read
0.8.0 since `WO-HUP-007`, and no migration scenario exists since
`WO-ECP-010`. The packaged bytes are those of `main` at `ff0e337`, the
merge of #241; nothing under `se_harness/`, no template and no workflow
changes on this branch.

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.7.1, outside the checkout, `-I` | 1,064 artifacts, 0 errors, 471 pre-existing maintenance warnings |
| `doctor` | released 0.7.1 | 0 FAIL |
| `preflight --work-order WO-RLS-014 --phase review` | released 0.7.1 | PASS |
| `release-unit --from v0.7.1 --to f356a01 --exempt <the fifteen contract commits> --contract REL-SEH-019` | released 0.7.1 | traces `WO-HUP-007`, `WO-RLO-008`, `WO-RLS-013` (released, not a member) and `WO-RLS-014` (five commits); untraced 0, exempted 15; incomplete only because `WO-RLS-014` is `in_progress` at this reading; `E-CIP-001` on the contract's top-level `candidate_commit` and `previous_release_tag` (deviation 1) |
| `qualify complete-candidate --candidate-commit f356a01` | candidate, `python -s`, no user site | completed, candidate-controlled: CC001 runtime bound to the checkout, CC002 HEAD and tracked tree match, CC003 1,064 artifacts 0 errors, CC004 target unchanged (a first run with the checkout on `PYTHONPATH` failed CC001 on the runtime identity, not on the candidate) |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (4 records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout from a clean tree (digest `561c6a64cb8763c1…`, not the build of record) |
| `repository_tools.upgrade_rehearsal`, twice | released 0.7.1 as predecessor, the ephemeral wheel installed outside the checkout as successor | PASS (0.7.1 -> 0.8.0) both runs; `semantic_sha256` `2f8dc136e6f712384ae852e865b67c9117ad599fb7c52b0414a809d0c93b845a` identical; `E012` tolerated on no record (the two former ready records are verified) |
| `python scripts/run_tests.py` | candidate, Linux | 1,011 tests, 1 failure, 4 skipped; the failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`, the file-mode artefact of this checkout that passes on the hosted runner |
| `harnessctl check --checkpoint handoff` | released 0.7.1 | section 5 |

## 3. Build of record

**Pending.** The recipe-bound replay needs a Linux host with the pinned
`linux/amd64` producer image; this workstation has no container runtime. To be
run by the release owner at the candidate commit and appended here:

```text
python -m repository_tools.release_build replay --repository . --commit <candidate> --version 0.8.0 --output-directory <bundle-dir> --result <replay.json>
python scripts/create_release_bundle_manifest.py --repository . --commit <candidate> --version 0.8.0 --wheel <bundle-dir>/<wheel> --sdist <bundle-dir>/<sdist> --build-recipe release/build-recipe.json --output <bundle.json>
```

Required outcome: state exact, two byte-identical producer runs, the wheel and
sdist digests recorded here, the manifest retained as
`docs/engineering/release-0-8-0/evidence/RLS-SEH-017-bundle.json` when the
record is prepared, and the hosted `release-candidate-replay.yml` dispatch on
the review ref reproducing the same digests.

## 4. Deviations, recorded for the completion decision

1. **The census re-run reports `E-CIP-001` on two top-level fields.** The
   released 0.7.1 `release-unit --contract` compares top-level
   `candidate_commit` and `previous_release_tag`; `REL-SEH-019`, like
   `REL-SEH-018`, names no candidate (it does not exist before this work
   order) and carries `previous_release_tag` and the exemptions in its
   `[release_unit]` table, which the command does not read — the fifteen
   exemptions are passed as `--exempt` flags. The contract's ten-member
   allow-list is the authority; `QGP-G5P-RELEASE-UNIT` passed unmeasured at
   approval. Recorded, not enforced, as `WO-RLS-013` recorded for
   `REL-SEH-018` (its deviation 2).
2. **The derivation reads four of the ten members.** Seven members reached
   `main` through merge commits without a trailer, exempted by name; the
   allow-list is the authority.
3. **The five branch commits were re-labelled after the fact.** They were
   pushed without the trailer, then rebased to carry
   `Harness-Work-Order: WO-RLS-014` before any candidate existed, and
   force-pushed on the draft branch; no record bound any of the earlier
   hashes.
4. **No build of record on this host** (section 3).
5. The two entry-condition verifications (`VREC-REB-026`, `VREC-REB-027`)
   carry a decision reason that over-states one re-measurement; the
   correction is in `REL-SEH-019`'s entry criteria.

## 5. Handoff checkpoint binding

artifact: WO-RLS-014
checkpoint: handoff
formal_snapshot_sha256: be60859139c7d6d6a292a9ccbb13b291b185c200be88f6a11e5c30fc9d266c91

Rerun: completed pass d0f1ffe617b94ecd6013ec5626e636a51c6a81a99451d5ae92bb7a24fab58c1f

## 6. Hosted lanes

Recorded in a later commit once the pull request has run them at the candidate head.
