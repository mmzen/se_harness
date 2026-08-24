# WO-HUP-004 local verification ledger

## Outcome

The bounded implementation replaces the version-specific predecessor workflow
with a generic, read-only governor-transition assessment. Ordinary same-version
changes do not invoke a second evaluator. A real version change is accepted
only when the trusted base, an implemented evaluator-upgrade work order, its
canonical transaction evidence, a released target distribution already present
in the trusted base, and an independently installed exact target evaluator all
agree. The LF/CRLF-sensitive inspection assertion now proves distinct evaluator
paths, root-lock integrity, and candidate semantics instead of requiring raw
root/template inequality.

Local qualification passes. The first hosted candidate proved every lane except
the changed-version pull-request assessment and exposed one POSIX virtual-
environment symlink defect. Its bounded correction is locally qualified and
uncommitted. `WO-HUP-004` remains `in_progress` pending a corrected candidate,
green hosted replay, and its separately governed completion decision.

artifact: WO-HUP-004
checkpoint: handoff
formal_snapshot_sha256: fa548ea1ff6359257fa0918e8ac5009405276526ba0ca11ba80bddf47978021e

## Repository and authority

- Working base commit: `7394a0ca396a6a8b514375a045c5e67ed3872d80`.
- Trusted default-branch base used by the historical replay:
  `7b5a705fbfcd91c79d660d305789dfa1772a0e12`.
- Local branch: `proposal/root-governor-0.6.0`.
- Packet approval: `2026-08-23T20:22:49Z`.
- Work-order start: `2026-08-23T20:23:09Z`.
- First operational candidate:
  `98f5aba4315744919f4a3646b7ca4ffe55c9bee3`, committed and pushed to
  `proposal/root-governor-0.6.0` under later explicit authority.
- This ledger records that candidate's hosted observations and the uncommitted
  POSIX correction. It records no VREC decision, merge, release, publication,
  deployment, maintenance mutation, external-policy change, or root-evaluator
  upgrade.

## Implemented behavior

- `scripts/validate_governor_transition.py` is a standard-library-only
  resolver with `plan` and `assess` phases and a bounded canonical JSON result.
- Base selection accepts only a full Git object identity. Pull requests and
  ordinary pushes use the event base; a zero/empty branch-creation base uses
  the unique merge base with the fetched default branch. Missing, abbreviated,
  non-ancestor, equal-to-target, ambiguous, and shallow-history bases fail
  closed.
- Configuration, lock, upgrade work order, transaction evidence, and release
  record are read from Git objects. Candidate imports cannot decide routing.
- Equal versions require identical raw and canonical locks and return
  `not_applicable`; managed current-governor CI remains authoritative.
- Changed versions require exactly one implemented `[evaluator_upgrade]` work
  order matching the base and target. The declared prior lock may match only
  the exact Git, LF, or CRLF materialization hash of the trusted base blob.
- The target wheel name, version, and SHA-256 must match exactly one `released`
  release record already present in the trusted base commit. Target-only
  governance content cannot authorize evaluator execution.
- Assessment verifies the downloaded wheel before creating the isolated target
  environment, then runs target `identity`, `doctor`, and complete JSON
  validation with user site and checkout imports excluded.
- The workflow has read-only contents permission, disables checkout credential
  persistence, fetches full history without credentials, contains no concrete
  governor version or release-record constant, and proves the checkout is clean
  before and after assessment.

## Routing and negative-case matrix

| Case | Result |
| --- | --- |
| same version, exact lock | `not_applicable`; no external evaluator command |
| same version, lock drift | fail closed |
| synthetic 7.4 to 7.5 with matching trusted records | transition required |
| branch-creation push | unique default-branch merge base selected |
| missing trusted target release | fail closed |
| wrong prior lock or evidence binding | fail closed |
| duplicate matching upgrade work order | fail closed |
| noncanonical transaction evidence | fail closed |
| abbreviated base commit | fail closed |
| dirty checkout | fail closed |
| missing or mismatched external target evaluator | fail closed |
| LF and CRLF materializations of one base lock | same canonical binding |

The original focused resolver, workflow-contract, and inspection replay ran 26
tests with zero failures or errors. The post-POSIX-correction replay ran 29
tests in 16.986 seconds with zero failures or errors and two POSIX-only cases
skipped on Windows.

## Exact historical 0.5.0 to 0.6.0 replay

A disposable clean Git clone overlaid the reviewed implementation and committed
it only inside the fixture. Its target
`7b4460396763f66f6fe48b1fffeb4cd6d59839d9` is fixture evidence, not an
operational candidate.

- Base: `7b5a705fbfcd91c79d660d305789dfa1772a0e12`, version `0.5.0`, schema-2 lock.
- Base Git/LF lock SHA-256:
  `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`.
- Base CRLF materialization SHA-256, as retained by the original transaction:
  `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- Resolved upgrade: `WO-HUP-002`; canonical evidence SHA-256:
  `83398eb76d73a96a0aef2bc40e1d9045a8e14cf5bf74b89afe2ecbf39350c284`.
- Trusted released target: `RLS-SEH-012`, tag `v0.6.0`.
- Target lock SHA-256:
  `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79`.
- Exact target wheel: `se_harness-0.6.0-py3-none-any.whl`, SHA-256
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Installed evaluator payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Exact external target identity, doctor, and validation each exited zero.
  Their retained stdout SHA-256 values are respectively
  `06f68371b251b43a29e4a11c1d35d582de5a78d781c95bbd30ef6c381ce3378e`,
  `a7ca37a85887cb30776293163dc9f9d9514b41e43f6b5a9c2acc1bcf08c20a9d`,
  and `663b3d7c6e7d60af2ebb753613e5c50e12e97aee20d41703f8929f9737152122`.
- Final assessment: `passed`; checkout remained clean.

A separate clean same-version replay against
`7394a0ca396a6a8b514375a045c5e67ed3872d80` returned
`assessment: not_applicable` and invoked no evaluator command.

## First hosted candidate and POSIX correction

Candidate `98f5aba4315744919f4a3646b7ca4ffe55c9bee3` triggered both push and
pull-request events.

- Both managed Engineering Harness validation jobs passed.
- Both candidate-source and candidate-package evidence chains passed.
- Linux and Windows governance-migration jobs and both platform-reconciliation
  jobs passed.
- Push governor-transition run `32697128876` passed as same-version
  `not_applicable`.
- Pull-request governor-transition run `32697131783` selected the real
  0.5.0-to-0.6.0 transaction, installed the exact target wheel, and then failed
  before identity with `evaluator entry point is outside the evaluator
  installation`.

The failure was caused by resolving POSIX `bin/python` to its shared system
interpreter before deriving the virtual-environment root. The resolver then
mistook the system interpreter prefix for the installation and rejected the
legitimate sibling `bin/harnessctl`.

The bounded correction now derives the logical environment from the absolute
launcher path before dereferencing it. It separately validates both the
launcher and resolved Python target as ordinary external files, requires
`python` and `harnessctl` to share the environment's `bin` or `Scripts`
directory, rejects an entry-point symlink escaping the environment, and leaves
the exact 0.6.0 identity command to verify `sys.prefix`, origins, isolation, and
payload/wheel hashes. Added cases cover a legitimate POSIX Python symlink, a
Python symlink resolving into the checkout, and an entry point outside the
launcher directory. The two POSIX cases execute on Linux and are skipped on
Windows. An Ubuntu 24.04 WSL replay executed all 16 governor-transition tests,
including both POSIX symlink cases, with zero failures or skips.

## Complete tests and repository gates

- Python 3.14.6 after the POSIX correction: 487 tests passed in 283.039
  seconds; 9 skipped on Windows.
- Python 3.11.9 after the POSIX correction: 487 tests passed in 301.120
  seconds; 9 skipped on Windows.
- Scale cases for 100, 500, and 1,000 artifacts passed on both runtimes.
- Exact public 0.6.0 `doctor`: pass; distribution and managed integrity match.
- Exact public 0.6.0 complete `validate`: pass, 707 artifacts, zero errors,
  50 retained maintenance warnings.
- Checkout-source complete `validate`: same passing result.
- Exact public 0.6.0 `inspect`: pass, 707 artifacts and 2,543 relations.
- Exact public dashboard: pass, zero errors; output manifest
  `61e6f8df3e4b0dfb432f86a5101b241089126e4b2dd3523415b81a45234607ff`.
- Exact public review preflight for `WO-HUP-004`: pass.
- Exact public upgrade replay: `36 files, 36 unchanged`.
- Release-distribution validation: pass, one distribution-bearing record.
- Workflow YAML parsing: pass.
- Concrete governor/release constant scan of the workflow and resolver: no
  match.
- Protected root/config/lock, `se_harness/`, and candidate-template comparison:
  no change.
- `git diff --check`: pass; Git emitted only local LF-to-CRLF checkout notices.

The 50 validator warnings are pre-existing maintenance findings concerning
legacy architecture metadata and historical noncanonical VREC/RLS placement.
There are zero structure, governance, or policy errors, and this work order
does not alter those findings.

## Exact changed-path boundary

The complete local change set is exactly the 16 paths declared by
`WO-HUP-004`:

1. `.github/workflows/predecessor-evaluator-assessment.yml`
2. `docs/engineering/repository-harness-upgrade/README.md`
3. `docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-003.md`
4. `docs/engineering/repository-harness-upgrade/architecture/adr/ADR-HUP-001.md`
5. `docs/engineering/repository-harness-upgrade/capabilities/CAP-HUP-003.md`
6. `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-004-verification.md`
7. `docs/engineering/repository-harness-upgrade/intent/INT-HUP-003.md`
8. `docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-008.md`
9. `docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-009.md`
10. `docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-004.md`
11. `docs/engineering/repository-harness-upgrade/verification/VER-HUP-004.md`
12. `docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-004.md`
13. `scripts/validate_governor_transition.py`
14. `tests/test_governor_transition.py`
15. `tests/test_inspection.py`
16. `tests/test_predecessor_assessment_contract.py`

## Preserved boundaries and remaining evidence

No managed/current-governor workflow, root configuration or lock, product or
candidate template, package version, VREC/RLS/REL record, tag, publication or
deployment workflow, maintenance state, external policy, or root evaluator
changed. The only Git-ref mutation was the authorized push of candidate
`98f5aba4315744919f4a3646b7ca4ffe55c9bee3`; its credential was used only for
that push and hosted-log inspection. The POSIX correction remains local and
uncommitted, and its corrected hosted pull-request assessment remains the only
unexecuted `VER-HUP-004` case.
