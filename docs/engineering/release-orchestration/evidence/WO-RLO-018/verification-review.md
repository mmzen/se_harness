# Publication correction: implementation present, verification blocked

WO-RLO-018 and VER-RLO-012 were approved by mmzen on 2026-10-03. Codex started
the work through the selected released 0.21.0 evaluator. The work remains
`in_progress`; no completion or verification decision is claimed.

The shared publisher now accepts an integer schema-5 lock only when it declares
`released-resources-v1` and omits `skill_ownership`. Schema-3/4 behavior remains.
The implementation is in commit `73224164fd38cc2c52317bc468bd225774253677`.
Later review commits add evidence only. No approved release input changed.

## Observed checks

| Check | Result |
| --- | --- |
| Focused publication tests, Windows Python 3.14.6 | 85 tests pass. |
| Focused publication tests, Linux Python 3.12.3 | 85 tests pass at the implementation commit. |
| Actual adopted evaluator descriptor | Pass; still selects evaluator 0.21.0 and its original public wheel. |
| Actual RLS-SEH-032 release resolution | Pass; preserves candidate, main integration, version, tag, archive hashes and evidence binding. |
| Disposable Pages resolution | Pass with a local-only tag at the recorded candidate; no publication. |
| Hosted publication rehearsal | All jobs pass in [run 37092302884](https://github.com/mmzen/se_harness/actions/runs/37092302884). Both rebuilt archives equal the approved hashes. |
| Released evaluator validation | Zero errors, 60 existing warnings. |
| Complete Windows source suite | 1,259 tests run; one topology-budget failure, 22 skips. |
| PR source suite, Linux Python 3.11.16 | Same failure among 1,259 tests, two skips, at merge candidate `be8169eed2c383d1e3f9f886b5bcb94ca339bbbe`. |

The first focused run had two fixture errors in one new test: it tried to
commit identical bytes while testing different metadata. Allowing an empty
fixture commit corrected that setup. The original result and passing rerun
are retained in [execution.json](execution.json).

## Blocking capacity result

`test_progressive_bundle_is_deterministic_partitioned_and_bounded` fails at
`tests/test_dashboard_webui.py:779`:

```text
AssertionError: 2099060 not less than or equal to 2097152
```

Measurements from disposable checkouts use the same test projection and full
Git history. Both graphs remain valid.

| Checkout | Artifacts | Relations | Topology bytes | Headroom |
| --- | ---: | ---: | ---: | ---: |
| Merged main `01ec43c86c9d30949295c07ac91c742be91e713a` | 1,881 | 7,176 | 2,097,049 | 103 |
| Correction `865b78a17903f82b37c55c165664c0d9318a70a7` | 1,883 | 7,182 | 2,099,060 | -1,908 |

The two approved artifacts add 2,011 bytes. The unchanged generator produces
the same failing size locally and on the PR merge ref.

[REQ-DST-062](../../../harness-distribution/requirements/REQ-DST-062.md)
requires the current repository to pass the exact 2 MiB target and explicitly
requires reassessment of topology sharding beyond that capacity.
[REQ-DST-063](../../../harness-distribution/requirements/REQ-DST-063.md)
requires the check on both the branch and PR merge history.
[SPEC-DST-020](../../../harness-distribution/specifications/SPEC-DST-020.md)
preserves the current-repository assertion. A smaller synthetic fixture, a
larger constant or an ignored failure would change those accepted obligations.
None is included in WO-RLO-018's three-file publication correction.

PUB5-01 through PUB5-04 have the positive, negative, compatibility and real
resolver evidence described above. PUB5-05 remains failed because its complete
source-suite condition fails. VREC-RLO-015 has not been created. The passing
publisher rehearsal does not override this failure.

## Required decision and remaining work

The proposed next step is a separate capacity assessment and bounded artifact
package before changing the dashboard or its acceptance contract. A temporary
exception would instead require an explicit, bounded proposal and decision;
no exception is currently approved. Keep PR #529 in draft until the required
checks and human verification are complete. Release publication is pending.

## Retained evidence

- [execution.json](execution.json): command identities, result excerpts,
  original failures, focused checks, full-suite failure, real resolver plans,
  baseline comparison and seven unchanged release/configuration byte hashes.
- [rehearsal.json](rehearsal.json): successful hosted jobs, downloaded replay
  and artifact metadata; candidate remains
  `abbec12ac5524c8adfb28693f846dd59de88f759`.
- [ci-source-summary.json](ci-source-summary.json): exact merge candidate,
  checker origin, command and failure excerpt.
- [ci-source-availability.json](ci-source-availability.json): observed upload
  and successful download of the raw CI log. Artifact `11263141477` expires
  on 2026-10-17T03:13:17Z unless deleted earlier. Download with
  `gh run download 37092393950 --repo mmzen/se_harness --name candidate-source-raw`.

No tests called publication APIs. The disposable Pages tag exists only in its
temporary clone. RLS-SEH-032, VREC-SEH-032, their evaluator evidence, the bundle,
and the adopted lock/configuration are byte-identical to the pre-fix inputs.
