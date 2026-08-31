```toml
artifact = "WO-RLS-018"
checkpoint = "handoff"
formal_snapshot_sha256 = "fcd8bba6843c53d979abe5a09bb53e0cfd86828dc78249220014a73b14f2f9b5"
rebound_at = "2026-08-31T11:26:12Z"
```

# WO-RLS-018 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.12.0 candidate commit exists on `release/0.12.0` off `main`
at `2761f89`, with the packaged bytes of `main`: this commit. The five
trace commits of `REL-SEH-023`'s trace repair precede it. Qualification
readings, the census at the candidate, the recipe-bound build of record
and the hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`,
  installed from the digest-verified wheel (`ba26ab7b…`), on this Windows
  checkout for every reading, the packet and the handoff check included.
- Candidate: this checkout, branch `release/0.12.0` off `main` at
  `2761f89`; `pyproject.toml` reads 0.12.0 (moved by `WO-HUP-011`).

## Section 1: the candidate

This commit is the candidate: it retains this packet's skeleton and the
branch already carries the packet drafting, the approvals, the start and
the five empty trace commits. Every subsequent branch commit carries the
`Harness-Work-Order: WO-RLS-018` trailer in its final block; the three
governance commits before this one (draft, approve, start) predate that
convention on this branch and are exempted in the recorded census
alongside the contract's fourteen.

## Section 2: readings at the candidate `a60975f`

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate` | released 0.11.0, outside the checkout, `-I`, wheel-installed | 1,210 artifacts, 0 errors, 486 pre-existing maintenance warnings |
| `doctor` | released 0.11.0 | 0 FAIL |
| `preflight --work-order WO-RLS-018` | released 0.11.0 | PASS, no diagnostic |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (8 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`217baced…`) built outside the checkout from a Git export of the candidate and installed into a disposable environment |
| `repository_tools.upgrade_rehearsal`, twice | released 0.11.0 as predecessor, the ephemeral wheel installed outside the checkout as successor | `overall_result` pass both runs (0.11.0 -> 0.12.0); `semantic_sha256` `9850bf40d5f76513587bda1ba7bfc864a252ac80dd3c98c8e967195a6d47e7fa` both runs |
| `python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.14), CRLF checkout | 1,171 tests, 26 skipped, 1 failing name, present on `main` and outside this work order (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`) |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this branch head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-package lane at this branch head, section 5 (`RID018` boundary on Windows, as `REL-SEH-022` records) |
| `harnessctl check --checkpoint handoff --from-git` | released 0.11.0 | section 4 |

## Section 3: census re-run at the candidate

`harnessctl release-unit . --from v0.11.0 --to a60975f --contract REL-SEH-023`
with seventeen `--exempt` values (the contract's fourteen recorded
exemptions plus this branch's three governance commits `e64f1d2`,
`e61d2ef` and `5ae90d7`, which predate the trailer convention on this
branch), released 0.11.0: untraced 0, exempted 17; fifteen work orders
traced — the thirteen members, `WO-RLS-017` through #270's branch commits
(released by `RLS-SEH-020` and excluded, as the contract states by
construction), and `WO-RLS-018` through this branch's trailered commits.
The five trace commits of the contract's trace repair carry their members
exactly as predicted. The comparison reports the four `E-CIP-001` findings
the contract predicts at this stage: no `candidate_commit` and no
top-level `previous_release_tag` are declared (the contract carries the
tag in `[release_unit]`, as its predecessors did), the gates differ by
exactly `WO-RLS-017` (traced, released, excluded), and `WO-RLS-018` is
`in_progress`, the state this reading is taken in.

## Section 4: build of record

`python -m repository_tools.release_build replay --repository . --commit
a60975fdaa215c9a0433571688251184ee459932 --version 0.12.0` on this Windows
workstation through Docker with the pinned linux/amd64 producer image: two
producer runs byte-identical. Wheel
`se_harness-0.12.0-py3-none-any.whl` `dc14f007291a460d5be47d7286d4332fcac67fd2ecc66e1d26f8a5b0cc301cee`;
sdist `se_harness-0.12.0.tar.gz` `1b0e426502d56c315f5f5d2b0175b3e9a4a112f2811670409f62ce39a998a64c`;
source manifest `ae35d09d…`; bundle manifest created by
`scripts/create_release_bundle_manifest.py`, retained as
`RLS-SEH-021-bundle.json` when the record is prepared. These digests are
local readings until the hosted `release-candidate-replay.yml` dispatch
agrees.

## Section 5: hosted lanes

Recorded when the lanes complete at this branch head.

## Section 4b: build re-verified at the bound candidate

`RLS-SEH-021` binds `3dcde4b`, the implemented-transition commit, so the
replay was re-run at that exact commit on the same host and image: two
producer runs byte-identical. Wheel
`639edbeed4bdca7c9e21a5eb2afc3b9fc993ddb3f66177eec962f1646a545811`; sdist
`3f7b22ff484dce8d95728a6ab632b86f0046713b2166498af36d526dab8ce3f2`. The
section-4 digests were the local reading at `a60975f`, whose packaged
bytes are identical; the archives differ only through the commit-derived
`SOURCE_DATE_EPOCH`. The bundle manifest retained as
`RLS-SEH-021-bundle.json` and the record's distribution table carry the
bound-candidate digests; the hosted `release-candidate-replay.yml`
dispatch on this branch must reproduce them.
