# WO-CIP-009: evidence for verification review

This report maps VER-CIP-005 to retained observations. It supports record
preparation and does not exercise the assurance owner's decision.

## Scope and candidate identity

The implementation head is `fd5c058fd3608c03eae2f4b8c242c72ab6a1093f`.
[Run 34632721158](https://github.com/mmzen/se_harness/actions/runs/34632721158)
tested merge `7aa659e2d74ebc44d288b01e7e6fe875d1529afb`. Source/package checks,
both platform replays, exact-commit integration build and Windows/Linux
installation checks passed. The managed gate, predecessor assessment,
publication rehearsals and CodeQL also passed for that implementation head.

The record's later candidate includes the authorized completion decision and
this retained evidence. No implementation file changes after the tested head.
Its exact identity is captured by the released evaluator after a clean commit.
Earlier hosted checks are evidence for their named implementation head, not
claims that the later governance/evidence commit was already run in CI.

The operator explicitly confirmed marking WO-CIP-009 implemented and preparing
its verification record on 2026-09-11. This authorizes preparation, not a
verification decision, merge or release.

## Verification coverage

| VER-CIP-005 case | Evidence and observed result |
| --- | --- |
| TIM01: unchanged handover | `scratch-focused.txt`: 67 focused tests pass. Fixtures compare timing on/off commands, original result fields, digest and success/failure verdicts; the only extra command is the separately timed read-only Git path query. |
| TIM02: timing accuracy | Controlled-clock tests prove nested elapsed times, flushed progress and partial observations. Stage identifiers and timing remain separate from the semantic digest. |
| TIM03: failures | Tests exercise export, handover, cleanup, interruption and diagnostic-write failures. Failures are retained or propagated; no failed handover becomes a pass. |
| TIM04: boundaries | Tests reject checkout-contained output/workspace paths and verify the diagnostic field allowlist. Workflow inspection finds no Defender mutation, extra replay or broad environment dump. |
| TIM05: hosted comparison | Four `location-*-result.json` files pass; all four semantic digests equal `c3f2ddc6fca4cf1db464c92eb453b15c51e39347cbf5f748e711f0b088adbb6a`. Matching timing and runtime files name the run, implementation head and tested merge. |
| TIM06: candidate checks | `scratch-full.txt`: 1,159 tests pass with 23 skips. `scratch-distributions.txt`: 14 distribution-bearing records pass. Released doctor, preflight, graph, scope and handoff checks pass; hosted source/package and downstream jobs pass. |
| CAP01: entry count | Retained `capacity-tests.txt`: 19 packaging tests pass, including real TAR boundaries at 19,999/20,000/20,001 and a successful small-limit extraction fixture counting directories. These tests remain in the later full suite. |
| CAP02: safety budgets | The tests retain the 128 MiB member and 512 MiB archive/expanded-total caps and reject oversize, unsafe paths, links, duplicates and empty archives before extraction. |
| CAP03: real archive | The explicit-location candidate has 10,033 entries, above the old cap and within 20,000. The normal exact-commit integration build and same-package Windows/Linux installation jobs pass. |
| LOC01: location/isolation | Tests honor default/explicit roots, reject missing/file/checkout-contained roots before writes, preserve the operational checkout, and remove scratch directories after success or failure. |
| LOC02: observable storage | Four timing files record default, selected, actual repository and Git-resolved storage paths. Query-failure tests make measurement incomplete while preserving the handover failure. Paths remain outside the result digest. |
| LOC03: hosted placement | Each actual disposable repository and Git directory/index/objects is beneath that job's RUNNER_TEMP. Both platform pairs pass and agree. `location-index.json` retains source paths, byte hashes and successful job identities. |

## Windows observations

The new runner's Python default is on C:. Explicit placement uses D: for the
disposable repository and Git directory, index and objects. The former run did
not record its scratch path, so it cannot be reconstructed as a measured fact.

| Measurement | Default-location baseline | Explicit RUNNER_TEMP |
| --- | ---: | ---: |
| Windows replay 1 | 168.45 s | 34.21 s |
| Windows replay 2 | 112.18 s | 33.77 s |
| Complete Windows job | 338 s | 116 s |
| Linux replay 1 | 10.66 s | 11.32 s |
| Linux replay 2 | 10.49 s | 11.29 s |

Windows replay time is about 76% lower and the complete Windows job about 66%
shorter. Different hosted VMs were used, and the new archive includes 15 added
evidence files. This is an observed improvement, not a controlled disk benchmark
or a speed guarantee. No RAM disk, extra replay, security-setting change or
weakened check was introduced.

## Retention and review boundary

`measurement-index.json`, `default-baseline-index.json` and `location-index.json`
identify three separate hosted runs. Each index preserves hashes of its raw
JSON observations. Local check indexes identify the tested source bytes and
retained test outputs; an earlier index describes its earlier candidate.
Full hosted logs and non-promotable wheels are retained outside the checkout,
with their hashes in the corresponding index. Actions artifact retention is
temporary; compact review evidence is retained in this repository.

Review this report, the indexes and underlying files against VER-CIP-005 before
deciding the prepared record. Its state remains ready until the assurance owner
explicitly verifies or rejects it. Work-order verification and repository merge
are separate actions.
