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

Run on 2026-08-28 on this Linux host (the owner installed Docker for it;
`docker` reached the daemon through `sudo` for this invocation only, no
durable system change), at the exact candidate:

| Reading | Value |
| --- | --- |
| command | `python -m repository_tools.release_build replay --repository . --commit aa0c9bc… --version 0.8.0` |
| state | `exact`; two producer runs `a` and `b` byte-identical |
| producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64, digest-pinned by `release/build-toolchain.lock` |
| recipe | `release/build-recipe.json`, `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| wheel | `se_harness-0.8.0-py3-none-any.whl`, `a95497f3535a07202af92e5d280d671fd4a65cb43fa46eae83e797617582911c` |
| sdist | `se_harness-0.8.0.tar.gz`, `8c8fcddf8ea3ac53afc9b4ae57d063c84cfe67f63d2fdb747409f52bda642e00` |
| checksums | `SHA256SUMS`, `dbf6099f1a4042638c39cc65b895f4cf897eee36c4f7135b0b74a904e585ebc5` |
| source manifest | `8c51e34b938105963ac0b250be2462348a8b3e1fe4a7b7a57317dbef84a9b684`, `source_date_epoch` 1787929800 |
| bundle manifest | `scripts/create_release_bundle_manifest.py` → `se-harness-release-bundle/v2`; to be retained as `docs/engineering/release-0-8-0/evidence/RLS-SEH-017-bundle.json` when the record is prepared |

The hosted `release-candidate-replay.yml` dispatch on the review ref, before
the release decision, must reproduce the same wheel and sdist digests.

The original pending text follows for the record. **Pending.** The recipe-bound replay needs a Linux host with the pinned
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

At the candidate head `aa0c9bc` of #242, twelve of thirteen checks pass:
`candidate-evidence.yml` run `33183812371` — candidate source (full suite at
full scale), candidate package, the real upgrade rehearsal 0.7.1 -> 0.8.0 on
Linux and on Windows with agreeing lock digests, the deterministic integration
package built, verified on both platforms and retained;
`publication-rehearsal.yml` run `33183812663` (record selection, the
candidate-mode replay of this candidate's own recipe, the release-record
replay); governor transition assessment run `33183812385`. The managed
`validate` lane (run `33183812351`) failed at "Select the pull-request work
order" with `found 0`: it reads the stored pull-request event, which predates
the body edit that added the `Harness-Work-Order: WO-RLS-014` line. This
commit refreshes the payload; the lane's result at this head is recorded in
the completion decision.
