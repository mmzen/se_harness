# WO-PLG-020 completion assessment

The operator requested "mark work order implemented and prepare verification
record". This assessment supplies the observed acceptance evidence for the
engineering-owner completion decision and the later assurance-owner review.
It does not itself change lifecycle state or verify the work.

## Tested implementation and evidence

[PR #462](https://github.com/mmzen/se_harness/pull/462) merged as
`9acdd08e6507d4433bc27f3888d2743d1eea13da`. The hosted push run tests that exact merge,
not an inferred replacement candidate. Its complete tree is
`e90a85deed574bc71da9a4b95c6a3df4961f5526`. [Candidate Evidence](https://github.com/mmzen/se_harness/actions/runs/34719970877)
completed successfully through attempt 2, including
source regression, released-verifier package acceptance, both platform
rehearsals and ownership selections, and the integration-package consumers.

The first main attempt and the unfinished PR run were canceled. The first main
attempt's downloaded observations remain in `cancelled-attempt.zip`; incomplete
observations are not accepted as passing. The resumed jobs use the same
non-promotable wheel built by the source job. Wheel SHA-256:
`3387717c4090e04076a934d62e01c8050c29d49fe8a4b79a3c874568339574b2`. The final artifact archive retains raw JSON, test
logs, runner image and Python identities, command arrays, snapshots and fault
schedules. `merged-candidate-ci.json` inventories the exact archive bytes and
`case-index.json` indexes each ownership result. Ephemeral wheel/sdist files are
kept in the preparation workspace; their verified hashes and source inventory
are retained as evidence, not published release distributions.

GitHub retained duplicate artifact names across attempts. The final evidence
uses the latest creation time for each name and downloads the exact artifact ID;
`github/artifact-selection.json` records that selection and each original ZIP
digest. Older canceled artifacts remain separate. Windows test-module bytes
differ from the Git LF blob only by LF-to-CRLF checkout conversion; both exact
hashes and the per-platform comparison are retained in the acceptance summary.

## Required results

Full-scale canonical source regression: **1240 tests,
9 explicit skips, no failures**, in
93.634 seconds. The released-verifier package contract
passed its ten scenarios. All four real predecessor-to-candidate upgrade
replays passed and produced one cross-platform semantic digest.

| Platform | Python | Mode | Passed | Explicit skips | Seconds |
| --- | --- | --- | ---: | ---: | ---: |
| Linux | 3.11 | source | 8 | 0 | 3.918 |
| Linux | 3.11 | package | 8 | 0 | 5.684 |
| Linux | 3.13 | source | 51 | 2 | 90.906 |
| Linux | 3.13 | package | 51 | 2 | 98.499 |
| Windows | 3.11 | source | 8 | 0 | 22.432 |
| Windows | 3.11 | package | 8 | 0 | 34.846 |
| Windows | 3.13 | source | 53 | 0 | 273.236 |
| Windows | 3.13 | package | 53 | 0 | 382.397 |

The ownership matrix contains 244 test executions:
each full selection has 42 acceptance tests plus 11 bounded-read unit tests,
and each smoke selection has eight acceptance tests. It retains
196 executed acceptance-case JSON records; bounded-read unit
results and skipped fixtures are retained in the logs and runtime records. Skipped
mechanisms and their reasons remain explicit in `acceptance-summary.json` and
the per-selection runtime files. An unavailable mechanism is not a successful
refusal; applicable real linked-path cases remain covered on each platform.
The source selections are candidate-controlled. Package selections use the
isolated installed evaluator and recorded wheel identity on disposable fixtures.

Released-evaluator review preflight, doctor and graph validation passed on the
merged checkout. Candidate help includes `skill-ownership`; release-distribution
validation passed for all 14 distribution-bearing records. These local checks
did not rebuild or publish a release.

## Assessment against VER-PLG-020

| Requirement | Cases | Observed support for acceptance |
| --- | --- | --- |
| REQ-PLG-028 | OWN01, OWN02, OWN03, OWN04, OWN14 | Explicit reviewed plans retire the selected seven-file catalog; unchanged and independently selected inputs are required; customization, ambiguous paths and stale plans preserve the target. |
| REQ-PLG-029 | OWN05, OWN06, OWN07, OWN08, OWN12 | Supported integrity, replay, direct installer and compatible upgrade paths retain ownership; unsupported inputs and protected report destinations refuse; credential-free clones distinguish integrity from availability. |
| REQ-PLG-030 | OWN04, OWN09, OWN10, OWN11, OWN13 | Changed inputs, fault boundaries, killed processes, recovery tampering, intervening owner edits, restoration conflicts and concurrent transactions exercise preservation and recovery. |
| REQ-PLG-031 | OWN01, OWN03, OWN12, OWN14 | Independently supplied identities and bounded inventories are checked as data; external provider bytes and inert execution sentinels remain protected; inventory success makes no native-host claim. |

The current OWN07 criteria include candidate refusal of unsupported old/future
locks and both report protections: qualification cannot recreate a retired skill,
including when inspection fails; dashboard output cannot replace installed
workflow or discovery paths. Both remain in all eight source/package selections.
The tests and suite-hygiene checker are unchanged from the tested merged commit.

## Retained limitations and decisions

The operator's approved exclusion of already distributed 0.17 behavior on
migrated schema-4 targets is part of SPEC-PLG-020, ARCH-PLG-003, ADR-PLG-003 and
VER-PLG-020. The old protected-output counterexamples remain historical failures;
they are excluded from this acceptance and were not converted to passes.
The root-pinned 0.17 governor and ordinary predecessor rehearsal keep their
separate roles.

DEC-PLG-007's narrow schema-4 exception remains in force. Native activation,
macOS qualification, live WO-PLG-009 connection, release and root adoption remain
separate work. The accepted C10/C11 enforcement limitation is unchanged.

## Decision boundary

Completion uses the operator's explicit engineering-owner decision, and record
preparation uses the operator's direct request. The local sandbox could not
fetch the optional live delegation reading over its network connection; those
projection diagnostics remain visible in the receipts. They are not claimed as
passing delegated authorization. Actual hosted checks are independently retained
from GitHub. No delegated decision is substituted for the operator's decision.

The operator explicitly authorized WO-PLG-020 implementation completion and
VREC-PLG-015 preparation. Apply the engineering-owner transition only after its
released-evaluator checkpoint and exact preview pass. Commit that completion and
retained evidence as the clean candidate, then use `capture-verification` to
prepare one ready VREC conforming to VER-PLG-020. The completion commit changes
governance/evidence only relative to the tested merge; record that exact comparison
in the prepared VREC. The assurance owner must decide the VREC separately.
