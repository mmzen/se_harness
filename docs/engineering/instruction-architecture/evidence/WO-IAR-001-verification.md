# Verification Evidence: WO-IAR-001

## Authorization and scope

The repository owner approved the complete IAR artifact chain and authorized bounded implementation on 2026-08-11 with `i approve, you can implement`. The immediately preceding instruction separately authorized the candidate commit, verification capture, later governance commit, normal branch push, and pull request. No verification transition, merge, release, tag, package publication, deployment, or branch-protection mutation is authorized.

The implementation rationalizes agent routing and file ownership, adds transactional ownership migration, implements read-only work-order preflight, adds strict pull-request work-order selection, separates released-baseline and candidate CI assurance, updates canonical and self-hosted content, and retains deterministic tests.

## Implemented requirement matrix

| Requirement | Retained implementation evidence |
| --- | --- |
| `REQ-IAR-001` | AGENTS managed block has one destination; Claude imports AGENTS; managed router owns the remaining route. |
| `REQ-IAR-002` | Fragment adoption/upgrade preservation remains intact; malformed markers and coordinated file/lock changes fail closed. |
| `REQ-IAR-003` | Lock records fragments, managed policy/router, and README/context/PR-template seeds explicitly. |
| `REQ-IAR-004` | Router directly names all four focused policy modules and their decision points. |
| `REQ-IAR-005` | Named context fields are checked individually; arbitrary `TODO` prose outside an unresolved full field does not fail. |
| `REQ-IAR-006` | `preflight` provides deterministic text/JSON, start/review phase rules, complete chain coverage, stable diagnostics, and no writes. |
| `REQ-IAR-007` | CI downloads the exact v0.2.0 GitHub wheel, verifies SHA-256, runs its packaged validator, and separately exercises candidate preflight and PR selection. |
| `REQ-IAR-008` | Managed-to-seed migration handles schema-1/2 newline equivalence, preserves customization, is idempotent, and blocks the entire apply on ambiguity. |
| `REQ-IAR-009` | CLI, router, reports, workflow, and documentation preserve the human authority boundary. |

## Verification results

### Formal graph and preflight

| Command | Result |
| --- | --- |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS; 161 artifacts, 0 errors, 0 warnings. |
| `python -m se_harness preflight . --work-order WO-IAR-001` while active | PASS; deterministic complete reading manifest and repository commands; no diagnostics. |
| `python -m se_harness preflight . --work-order WO-IAR-001 --phase review` | PASS before completion and again with the work order implemented. |
| `python -m se_harness doctor .` | PASS for every required path, seed state, lock digest, managed fragment, and distribution-template comparison. |
| `python -m se_harness upgrade .` | PASS; summary 32 files, 32 unchanged after self-upgrade. |

Preflight negative fixtures cover incomplete and duplicate context fields, start/review lifecycle differences, unknown and injection-shaped IDs, missing relations and coverage through formal validation, managed drift, and a coordinated managed-file plus lock-digest modification. The latter passes lock comparison but fails the independent distribution-template comparison as intended.

### Automated suites and syntax

| Runtime or command | Result |
| --- | --- |
| Python 3.11.9: `python -m unittest discover -s tests -p "test_*.py"` | PASS; 70 tests, 2 conditional Windows symlink skips. |
| Python 3.14.6: `python -m unittest discover -s tests -p "test_*.py"` | PASS; 70 tests, 2 conditional Windows symlink skips. |
| `python -m unittest tests.test_instruction_architecture tests.test_harnessctl` | PASS; 33 focused tests, 1 conditional Windows symlink skip. |
| `python -m compileall -q se_harness templates/repository/standard/scripts tests` | PASS. |
| PyYAML parse of root and canonical `engineering-harness.yml` | PASS after correcting the candidate pip command to a block scalar. |
| `python -m se_harness --help` | PASS; includes `preflight` without adding an installation profile. |
| `python -m se_harness dashboard .` | PASS; 161 artifacts, 554 relations, 0 errors, 1 unrelated derived warning. |

The derived warning is the pre-existing `VREC-AGR-001` stale-ready supersession prompt. This work order does not authorize changing that historical record.

### Installation and migration cases

Automated fixtures verified:

- fresh installation and existing-repository adoption;
- owner content around AGENTS and Claude managed fragments, including newline and Unicode behavior already covered by the installer suite;
- incomplete, duplicated, reversed, and malformed markers with no writes;
- unchanged schema-2 managed README to owner seed;
- schema-1 newline-only managed README migration;
- customized managed README blocking the complete apply while preserving the README, missing managed file, and original lock;
- repeated successful upgrade as a no-op;
- explicit self-host adoption of the owner README seed and full managed router lock entry;
- canonical/self-host parity reported as 32 of 32 unchanged template files.

### Independent released baseline

GitHub release `v0.2.0` was inspected through the GitHub API. The wheel asset is:

```text
https://github.com/mmzen/se_harness/releases/download/v0.2.0/se_harness-0.2.0-py3-none-any.whl
```

The release API digest, downloaded `SHA256SUMS`, retained release evidence, and local `Get-FileHash -Algorithm SHA256` all agree on:

```text
56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d
```

The downloaded wheel installed offline with `--no-index --no-deps` into an isolated environment. Its external `harnessctl doctor` passed against this repository, and its packaged validator independently reported 161 artifacts, 0 errors, and 0 warnings.

An attempted `pip download se-harness==0.2.0` returned no matching distribution from the configured package index. The CI baseline therefore uses the immutable named GitHub release asset plus the independently retained SHA-256 rather than falsely depending on PyPI availability.

## Security and authority inspection

- Pull-request body is read from `GITHUB_EVENT_PATH` as bounded JSON with duplicate-key rejection and a 2 MiB limit.
- Exactly one standalone `Harness-Work-Order: WO-...` field is accepted; shell metacharacters and placeholders are rejected before output.
- The validated ID alone crosses into `GITHUB_OUTPUT` and a quoted environment variable.
- Target paths, lock paths, context, artifact metadata, and IDs remain untrusted.
- Preflight executes neither context commands nor repository shell content.
- Managed integrity is checked against both the repository lock and the installed distribution template.
- Candidate scripts cannot replace the prior released validator in the independent lane.
- Candidate tests are not described as independent assurance.
- Automation changes no lifecycle state and performs no commit, push, tag, release, publication, or deployment.

## Deviations and residual risks

1. The approved draft originally required only `approved` preflight status. Review CI occurs after honest completion, so the implemented interface makes phase explicit: `start` accepts `approved`/`in_progress`, while `review` also accepts `implemented`/`verified`/`released`. The requirements, specification, acceptance scenarios, and tests record this correction.
2. The configured package index did not expose `se-harness==0.2.0`. The independently hash-verified GitHub release wheel is used instead.
3. The harness repository necessarily has a one-release bootstrap lag. The last release independently enforces prior graph rules; new preflight behavior is candidate verification until a later release and separately governed baseline-pin update.
4. Structural checks cannot prove that an actor read the manifest or that an arbitrary diff semantically fits the selected work order. Protected human review remains accountable.
5. Branch protection, required-check selection, CODEOWNERS review, and external service availability are outside offline repository control and require owner configuration.
6. The two symlink tests are skipped because this Windows host cannot create the required symbolic links; non-symlink boundary coverage passes.
7. Harness Explorer retains one unrelated stale-ready informational governance prompt for `VREC-AGR-001`.

## Candidate and provenance boundary

This evidence belongs in the clean candidate commit for `WO-IAR-001`. The candidate commit ID and deterministic dashboard snapshot are recorded later by `harnessctl capture-verification` in `VREC-IAR-001`. That prepared record remains `ready` pending a separate accountable assurance decision.
