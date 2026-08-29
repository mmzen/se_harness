```toml
artifact = "WO-RLS-016"
checkpoint = "handoff"
formal_snapshot_sha256 = "30f6ff8ce7a3efbf5bcdbd1ced708f895694d80c9a45c2c8fa7a72e0ee20d7c0"
rebound_at = "2026-08-29T09:46:32Z"
```

# WO-RLS-016 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## 1. What the candidate is

The candidate is the commit that adds this file's sections 1 and 2. No
version move is needed: `pyproject.toml`, `se_harness/__init__.py` and the
README install line read 0.10.0 since `WO-HUP-009`. The packaged bytes are
those of `main` at `3139f24`, the merge of #259; nothing under
`se_harness/`, no template and no workflow changes on this branch. The
governing evaluator for every reading below is exact public 0.9.0,
installed outside the checkout from the wheel file whose digest
`RLS-SEH-018` binds, invoked with `-I`; where the 0.9.0 root cannot run a
command on this Windows checkout (issues #254 and #256, repaired in this
candidate), the same wheel runs from an isolated Linux environment (WSL
Ubuntu 24.04, CPython 3.12.3) over an LF clone, and the evidence says so.

This file is the keyed handoff packet that the 0.9.0 root's `harnessctl
evidence` writes (`ECP-EVD-001`); it stands where `REL-SEH-021` and
`WO-RLS-016` name `WO-RLS-016-verification.md`, because the packet path is
decided by the evaluator, not the author, as `WO-ECP-012`'s packet recorded.

## 2. Qualification readings

| Check | Actor | Reading |
| --- | --- | --- |
| `validate` | released 0.9.0, outside the checkout, `-I` | 1,115 artifacts, 0 errors, 475 pre-existing maintenance warnings |
| `doctor` | released 0.9.0 | 0 FAIL |
| `preflight --work-order WO-RLS-016 --phase review` | released 0.9.0 | PASS, no diagnostic |
| `release-unit --from v0.9.0 --to <candidate> --contract REL-SEH-021` | released 0.9.0 | section 3 (re-run at the candidate) |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate, `python -s`, no user site | section 3 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (6 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel built outside the checkout from a clean `git archive` export of the packet head (`se_harness-0.10.0-py3-none-any.whl`, `8e4bab8f7abb6b6fe940980f68d307462324d41bbad31fb3944281bb4d17df08`, discarded) |
| `repository_tools.upgrade_rehearsal`, twice | released 0.9.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.9.0 -> 0.10.0, lock schema 3, successor payload `723c98ec…`); `semantic_sha256` `daae780d3696e9fa6d764aa9c0d2038e63d8a64e85c3eea62837b00eaecbb4ce` both runs |
| `python scripts/run_tests.py --scale full` | candidate, Linux (WSL Ubuntu 24.04, CPython 3.12.3), LF clone at `0579672` | OK, 4 skipped |
| `python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.12), CRLF checkout at `0579672` | 1,117 tests, 2 failing names, both present on `main` and outside this work order: `test_artifact_authoring…test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`, `test_instruction_architecture…test_owner_region_stays_within_the_size_bound` (the CRLF-only owner-region reading) |
| `harnessctl check --checkpoint handoff --from-git` | released 0.9.0, LF clone | section 6 |

## 3. Census re-run at the candidate

`harnessctl release-unit . --from v0.9.0 --to 8344244 --exempt <the four contract commits> --contract REL-SEH-021`,
released 0.9.0: untraced 0, exempted 4; traces `WO-RLS-016` through its
five branch commits and `WO-RLS-015` through `7291602`, the merge of the
0.9.0 release record, as the contract states by construction. The
comparison reports the three `E-CIP-001` findings the contract predicts at
this stage: no `candidate_commit` and no top-level `previous_release_tag`
are declared (the derivation reads them at the top level; the contract
carries the tag in `[release_unit]`, as `REL-SEH-020` did), and the gates
differ by exactly `WO-RLS-015` (traced, released, excluded) and the four
members whose merges are exempted. Its remaining blocker,
`WO-RLS-016 is in_progress, not implemented`, is the state this reading is
taken in.

`qualify complete-candidate . --candidate-commit 8344244` with candidate
source, `python3 -s`, on the Linux environment: PASS — CC001 candidate
runtime bound to the checkout, CC002 HEAD and tracked tree match the
candidate, CC003 artifacts=1115 errors=0 warnings=475, CC004 target state
unchanged. On this Windows interpreter the same command reads CC001 FAIL
with `RID018`: a machine-wide `se-harness 0.8.0` distribution sits on its
system site-packages, which is the candidate-source runtime boundary
`AGENTS.md` documents and not a property of the candidate; recorded as
deviation 1.

## 4. Build of record

Run on 2026-08-29 on this Windows workstation through Docker Desktop
(daemon 29.7.2, linux/amd64) and the pinned producer image, at the exact
candidate `8344244`; the Windows build-of-record faults of earlier releases
are repaired on `main` and the replaying tree is the candidate's own:

| Reading | Value |
| --- | --- |
| command | `python -m repository_tools.release_build replay --repository . --commit 834424464a0284cea3cb929d3f5b55a34e6d8ace --version 0.10.0` |
| state | `exact`; two producer runs `a` and `b` byte-identical |
| producer | `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, linux/amd64, digest-pinned by `release/build-toolchain.lock` |
| recipe | `release/build-recipe.json`, `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc` |
| wheel | `se_harness-0.10.0-py3-none-any.whl`, `5e4e014dc0921afffc3fb3c3d86c5a3ee3295b13cbb8c25dd3d83aab5aa1281c` |
| sdist | `se_harness-0.10.0.tar.gz`, `4b2d2103694ddea45d3aec058148e8c7124fe4673b9abbeab3fe89e15129d10f` |
| checksums | `SHA256SUMS`, `cab0af3258748063b95476549bf8b7b730e4237fd0a0ad5f8563c86ea5870f28` |
| source manifest | `d7b0213c4be141caf74da5f7c063905902ab753e397288692f0d5ae492c4324a`, `source_date_epoch` 1787997099 |
| bundle manifest | `scripts/create_release_bundle_manifest.py`; to be retained as `docs/engineering/release-0-10-0/evidence/RLS-SEH-019-bundle.json` when the record is prepared, re-created at the commit the record binds |

These are local replay readings. The hosted `release-candidate-replay.yml`
dispatch on the review ref, before the release decision, must reproduce the
wheel and sdist digests of the commit the record binds; until it does they
are not quoted in any record.

## 5. Deviations, recorded for the completion decision

1. `qualify complete-candidate` on the Windows workstation reads CC001
   `RID018` because a machine-wide `se-harness 0.8.0` distribution is on the
   interpreter's system site-packages; the reading of record is the Linux
   interpreter's PASS (section 3). The candidate's bytes are the same on
   both.
2. This packet is the keyed handoff packet the 0.9.0 root writes, not the
   `WO-RLS-016-verification.md` file `REL-SEH-021` and `WO-RLS-016` name;
   the packet path is the evaluator's (section 1).
3. The five branch commits were first written with the
   `Harness-Work-Order:` line in a paragraph above the `Co-Authored-By`
   paragraph, which Git does not parse as a trailer, so the census read them
   as untraced — the defect `REL-SEH-020` recorded as an open question. With
   the owner's explicit permission the five commits were recreated with the
   same trees, order and author dates and the work-order line folded into
   the final trailer paragraph (`d5eff38`, `e2143b0`, `373959d`, `0579672`,
   `c0c917e` became `6a317ec`, `188571d`, `025e14b`, `ad121fc`, `8344244`;
   `git diff` between the old and new heads is empty). The lifecycle reasons
   on `REL-SEH-021` and `WO-RLS-016` therefore cite the pre-rewrite
   identifiers (`373959d` as the approval commit); the content they describe
   is byte-identical at `025e14b`. Nothing had been pushed and no record
   bound the old identifiers.
4. The governing 0.9.0 root cannot run `evidence`, `check` or
   `transition --apply` on this Windows checkout (issues #254, #256,
   repaired in this candidate); those readings come from the same released
   wheel on a Linux environment over an LF clone, as every work order since
   `WO-HUP-009` recorded.

## 6. Handoff checkpoint binding

`harnessctl check . --artifact WO-RLS-016 --checkpoint handoff --from-git 3139f24`
with released 0.9.0 outside the checkout on the Linux environment over an LF
clone, run to its fixed point on the committed packet (the retained
`handoff.json` is in the change set it digests): outcome completed; every predicate
of `QG-G4-IMPLEMENTATION-EVIDENCE` passes. Formal snapshot as bound in the
header above. Complete changed-path set, as Git derived it (6 paths):

```
docs/engineering/README.md
docs/engineering/release-0-10-0/evidence/WO-RLS-016/handoff.json
docs/engineering/release-0-10-0/evidence/WO-RLS-016/WO-RLS-016-handoff.md
docs/engineering/release-0-10-0/README.md
docs/engineering/release-0-10-0/release/REL-SEH-021.md
docs/engineering/release-0-10-0/work-orders/WO-RLS-016.md
```

## 7. Hosted lanes

Pull request #260 at `4d16419`: every lane passes (13 pass). The managed
Engineering Harness lane (https://github.com/mmzen/se_harness/actions/runs/33246651101/job/99085168635) ran the 0.9.0 root's handoff-only step, which
completed inside the declared scope with the declared `Harness-Restitution`
`0d2ef59a…` equal to the recomputed `result_sha256`; the Governor Transition
Assessment (https://github.com/mmzen/se_harness/actions/runs/33246651087/job/99085168695), both candidate-evidence lanes, both migration legs (the real
upgrade rehearsal 0.9.0 to 0.10.0 on Linux and Windows), both qualification
rehearsals and the integration-package build, verify (Linux, Windows) and
retain lanes pass. From the completion transition on, the managed lane is
expected red by issue #255 on the 0.9.0 root.
