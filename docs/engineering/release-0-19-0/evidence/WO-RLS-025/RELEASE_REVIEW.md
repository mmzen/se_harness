# SE Harness 0.19.0 release review

RLS-SEH-028 is ready. The human verified VREC-SEH-028 on 2026-09-27.
The release record selects all 14 work orders and binds their aggregate
verification to candidate `30d4dba2a088c4f83756c1241b76cdab40f796bd`. It is governed by REL-SEH-030.
The approved WO-RLS-025 authorizes this preparation and the read-only replay.

## Proposed release identity

Version: `0.19.0`. Planned tag: `v0.19.0`, as required by the repository's
version-to-tag rule. No Git tag has been created by this preparation.

| Distribution | SHA-256 |
| --- | --- |
| `se_harness-0.19.0-py3-none-any.whl` | `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8` |
| `se_harness-0.19.0.tar.gz` | `e8aae38d4f6896078739902491a9268cf3ebdfc199af05a7ae6d74cda7daaffe` |

The existing binder applied `bundle-0.19.0.json` to the ready record. The
manifest came from the manual exact-candidate rehearsal 36339047270. That
rehearsal produced each archive twice with matching hashes. The recipe,
producer, complete toolchain and source identity remain in `build-final.json`.

## Checks and boundaries

The released 0.18.0 evaluator passed release-decision pre-action gates and
formal graph validation. Distribution validation passed for all 16 bound
records, explicitly requiring RLS-SEH-028. The exact-record hosted replay
must also pass before the release decision; its result will be retained here.

The final integration and disclosed Windows fixture line-ending limitation
remain in [the verification review](FINAL_REVIEW.md). The user's verification
decision accepts VREC-SEH-028; it does not change those observed facts or fix
the fixture. The accepted native-host limits and future-capability disclosures
remain in the release notes and contract.

Only checker 0.19.0 is proposed for release. Plugin 0.2.0 inputs are prepared;
final plugin archives require an independently obtained public checker wheel
and their later archive checks. The repository's installed evaluator remains
0.18.0. This preparation performs no merge, release transition, publication,
latest-marker promotion, live plugin installation or root adoption.

## Accountable decision

After the exact-record replay passes, the release owner decides whether to
authorize RLS-SEH-028. The verification decision and passing checks do not
supply that release decision. External delivery requires its own authorization.

## Exact-record replay result

The [ready-record replay](https://github.com/mmzen/se_harness/actions/runs/36340880463)
passed on review commit `e156c5a59347d231c56b34644facef65790a3c8b`. It validated
the complete ready record, rebuilt its exact candidate twice and matched both
bound archive hashes. `ready-release-replay.json` retains the producer, recipe,
toolchain, expected hashes and both observed builds. `ready-release-replay-ci.json`
retains the run identity and retrieval details. The hosted artifact expires at
`2026-12-26T18:30:13Z`; its replay document is also retained in this repository.

All required release-preparation checks are complete. RLS-SEH-028 remains ready
for the human release decision. No release transition or publication occurred.

## Human release authorization

On 2026-09-27 the human said: “I authorize the release record”. The released
0.18.0 evaluator applied `RLS-SEH-028: ready -> released` with
`authorized_by = "release-owner"`. Only this release record changed state.
The candidate, version, tag, distribution hashes, verified VREC and its
evidence remain unchanged. The preceding sections retain the preparation
and review history; the current release record is now `released`.

The first transition preview stopped with `WEX201` / `E009`: the generated
ready record named its preparation actor, `Codex`, as its sole owner. The
release decision actor therefore did not match an owner. That preview wrote
nothing. The ready record's `owners` field was corrected to `["release-owner"]`
to record the human accountability explicitly supplied in this task.
`prepared_by = "Codex"` and every other record byte were preserved before
the transition. `release-owner-correction.json` retains both byte digests
and the exact field change; the failed preview remains alongside the
passing corrected preview and apply results.

The existing hosted replay remains evidence for the unchanged candidate,
recipe and bound archive hashes at its recorded review ref. It did not run
on the owner correction. Fresh released gates and structural graph checks
validated the corrected record and the applied transition. No build input
changed, so no new build or source-test result is claimed.

This records the human release decision. PR #490 still needs integration;
merge and publication remain separately authorized external actions.

Post-transition graph validation passed. Distribution validation passed for
all 16 bound records, requiring RLS-SEH-028. Its first local invocation lacked
the sandbox command-local Git ownership setting and could not read Git objects;
the retry passed with the established exact-repository setting. Details are
retained in `released-distribution-validation.json`.
