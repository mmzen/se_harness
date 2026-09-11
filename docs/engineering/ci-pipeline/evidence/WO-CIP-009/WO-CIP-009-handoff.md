```toml
artifact = "WO-CIP-009"
checkpoint = "handoff"
formal_snapshot_sha256 = "e9c268e5e92f44646edbd9af4fec38c8227cc935b9a83852a6a4623a7efffcef"
rebound_at = "2026-09-11T18:17:28Z"
```

# WO-CIP-009 handoff evidence

Header retained by the released 0.17.0 `harnessctl evidence` command; the
observations below are implementation evidence, not an assurance decision.

## Authority and change

The operator approved WO-CIP-009 and VER-CIP-005 and authorized diagnostic
implementation on 2026-09-11: "i approve both". The later "you can raise the
limit" authorized the capacity amendment recorded in both artifacts.

The diagnostic implementation adds opt-in timings and read-only runtime facts.
The amendment raises only the integration-package archive entry cap from
10,000 to 20,000. Files and directories count. The 128 MiB member and 512 MiB
archive/expanded-total limits and hostile-path, duplicate and member-type
checks stay unchanged. That amendment changed no performance or security setting.
The subsequent authorized scratch-placement change is described below.

## Hosted measurement

[Run 34627146995](https://github.com/mmzen/se_harness/actions/runs/34627146995)
tested merge `719d9d506b9db118e3d5b13994812d6fee2aedd6` from PR head
`9b2adbd44094d5c3451d997048dd80dca7057102`, before the capacity amendment.
It exported 8,300 files and 1,700 directories per replay. The ten original
timing/result/runtime JSON files are retained byte-for-byte beside this packet;
`measurement-index.json` records their source paths and SHA-256 hashes.

| Stage, seconds | Windows 1 | Windows 2 | Linux 1 | Linux 2 |
| --- | ---: | ---: | ---: | ---: |
| Extraction | 42.71 | 24.05 | 1.35 | 1.37 |
| Git add | 131.83 | 102.65 | 2.34 | 2.34 |
| Git commit | 34.86 | 26.11 | 0.23 | 0.18 |
| Upgrade plan and apply | 0.57 | 0.65 | 0.33 | 0.42 |
| Complete replay | 222.73 | 165.09 | 8.36 | 8.38 |

Extraction, staging and commit creation consumed 93.4% of Windows replay time.
This locates the expensive operations; it does not isolate filesystem, storage
or Git internals as the cause. Windows Defender reported real-time protection
disabled, with both C:\ and D:\ excluded. The runtime query took 16 seconds
outside the replay timings. The run is an observation, not a general benchmark.

All four replays passed with semantic digest
`65b65c97b9adbfe05078044173d549a921e1c358b165e60431fc303cfb68fc05`.
Candidate source/package and downstream integration checks passed. The managed
handoff check at that earlier candidate was blocked by missing tracked evidence;
this amendment addresses that separate blocker. Do not label the earlier
measurement as evidence that the later capacity change passed CI.

## Capacity and regression checks

`local-checks.json` records exact commands, results and checked source hashes.
`capacity-tests.txt` and `capacity-full-tests.txt` retain their output.

- The packaging module's 19 tests pass. Real TAR headers exercise 19,999,
  20,000 and 20,001 entries. A forbidden-member sentinel shows whether the
  archive passed the count check without extracting 20,000 files. A separate
  small boundary fixture proves full extraction at the inclusive limit and
  counts directory entries. Empty and above-limit archives are refused.
- Member, archive and expanded-total byte-budget cases and the existing hostile
  path/link/duplicate cases pass. Large declared-size cases use parsed metadata
  fixtures to avoid allocating hundreds of MiB.
- The full suite passes 1,155 tests, with 23 skips. The diagnostic tests cover
  identical on/off results and calls, controlled timing, interrupted execution,
  export/cleanup failures, write failures and output/credential boundaries.
- Released doctor, graph, scope and phase checks and release-distribution
  validation are run outside the candidate checkout. Candidate-source doctor
  has the previously identified 0.18.0-versus-0.17.0 managed-template skew.

## Scratch-placement amendment

The operator authorized the first proposed storage improvement with "ok go":
make the disposable workspace explicit and observable. Both existing platform
replays now pass `--workspace $env:RUNNER_TEMP`. The CLI accepts only an existing
directory outside the operational repository and retains unique temporary
subdirectories and cleanup. Its omitted default remains Python's temp selection.

Timing diagnostics now record Python's default, the selected and actual scratch
paths, and Git-resolved directory/index/object paths. Only TMPDIR, TEMP, TMP and
RUNNER_TEMP are included from the environment. A separately timed read-only Git
query adds no handover decision. A failed query makes measurement incomplete
without hiding a failed handover. No RAM disk or extra replay was introduced.

`scratch-local-checks.json` names the tested source hashes, exact commands and
retained outputs: 67 focused tests and the full 1,159-test suite pass, with 23
full-suite skips; release-distribution validation passes. These tests cover
placement, checkout boundaries, CLI selection, actual Git paths, cleanup,
incomplete diagnostics and unchanged handover results.

The ten original default-location baseline JSON files from run 34630231918 are
retained byte-for-byte as `default-baseline-*`; their hashes, head and tested
merge are in `default-baseline-index.json`. That run passed the full candidate
pipeline. Its Windows replays took 168.45 and 112.18 seconds; Linux took 10.66
and 10.49 seconds. Its actual scratch path was not recorded. New hosted paths
and timings must identify their own run and must not retroactively establish
where the earlier run wrote. Cross-run duration differences alone cannot prove
a drive-performance cause.

## Hosted acceptance and handoff boundary

The normal [PR #453 checks](https://github.com/mmzen/se_harness/pull/453/checks)
run against each actual PR head and tested merge. CAP03 requires a committed
archive above 10,000 entries, a passing exact-commit integration build, and
same-byte Windows/Linux integration verification. The authoritative result is
the completed run for that head, not this pre-run description or the older
measurement. Raw logs/run metadata are downloaded outside the checkout; their
identities and results are reported in the PR.

LOC03 additionally requires the new run's actual disposable repository and Git
storage to be under RUNNER_TEMP, with all four replay verdicts and digests
matching. The new run is reported separately from both earlier baselines.

This packet supplies the handoff input; it does not mark WO-CIP-009 implemented,
prepare a VREC, verify work, merge the PR or authorize a release. Those remain
separate accountable decisions.
