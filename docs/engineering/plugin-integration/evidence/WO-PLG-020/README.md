# WO-PLG-020 evidence index

Status: implementation in progress. No VREC-PLG-015 is prepared by this index.

## Governing start

The owner-approved definition packet merged in PR #461 at
`6559568e995fc6e28f64e6bc5a6d4a6dc5dcf7de`. Its class-bearing work order
was present at the PR base when the released evaluator applied DR-WO-START.
The required live `validate` check was successful:
[check-run 103560311357](https://github.com/mmzen/se_harness/actions/runs/34696319702/job/103560311357).
Commit `e33d8c86` records the resulting `in_progress` event.

- [Start preflight](governance/start-preflight.json)
- [Start check](governance/start-check.json)
- [Applied start](governance/start-applied.json)

The evaluator is the root-pinned released 0.17.0 outside candidate source.
Neither a source test nor an installed candidate environment governs this checkout.

## Supplemental definition approval

The operator approved [supplement revision 2](governance/supplement-revision-2.md)
on 2026-09-12. The [approval receipt](governance/supplement-revision-2-approval.json)
binds its exact proposal hash, accountable roles, five appended prior-contract
amendments, and ten scope additions. WO-PLG-020 remains in progress. The supplement
reconciles the CI interpreter/acceptance and command target/outcome rules without
weakening VER-PLG-020 or exercising a verification or release decision.

The supplemental implementation checks now pass: [39 CLI/documentation tests](development/supplemental-cli-documentation-final.log)
and [38 CI tests plus script syntax checks](development/ci-script-validation/focused-checks.json).
The CI checks preserve the exact six-job census and one-wheel producer, restrict
the 3.13 selection to its named ownership step, and check full source/package
execution. All 13 extracted PowerShell scripts parse and embedded Python compiles.

Released-evaluator readings after the amendments are retained as
[review preflight](governance/approved-review-preflight.json),
[doctor](governance/approved-doctor.json),
[graph validation](governance/approved-validation.json), and
[scope](governance/approved-scope.json). These checks passed. The scope result also
retains the unavailable live completion gate at the unpublished start commit;
it is not a delegated-completion authorization.

## Acceptance authority and expected inputs

[VER-PLG-020](../../verification/VER-PLG-020.md) defines OWN01 through OWN14.
The expected seven-file catalog, retained raw hashes, and input limits are
fixed in `tests/fixtures/skill_ownership/expected.json`; the retained fixture
bytes originate from approved main `6559568e`. Candidate transaction output
does not define these expectations.

The required final evidence is Ubuntu and Windows source and isolated
installed-package acceptance: Python 3.11 interface/compatibility smoke and
Python 3.13 full ownership/fault coverage, plus the canonical source suite,
actual wheel and sdist inventory, released-evaluator checks, and live CI at
the committed candidate. Unsupported filesystem mechanisms must remain
explicitly unavailable. Native host activation is not observed by these tests.

## Retained development failures and limits

The completed Windows/Python 3.13 ownership source run records 41 cases and
651 events in 1,646.616 seconds: 40 case records passed, and one records six
unavailable symlink subcases. Its 85 exception boundaries and 67 precommit
process-termination boundaries passed, with separate committed-state cleanup
observations. The corrected actual-0.17.0 CLI probe passed separately in
10.201 seconds. These are development observations: source guard and reporting
edits occurred while the full run was active, so no single immutable candidate
is claimed for it.

- [Source observation index and limitations](development/acceptance-source-observation-index.json)
- [Raw member hash inventory](development/acceptance-source-raw-inventory.json)
- [Original source observations archive](development/acceptance-source-development-observations.zip)
- [Final default-upgrade regression observations](development/default-upgrade-regressions.json)

The archive preserves initial failed runs, focused repairs, the completed full
ownership run, and the corrected old-reader probe as separate groups. Its 87
members were verified against the raw inventory; its SHA-256 is
`d7fb07976f821a538ef6d4dc23a44984778c59bcab3743fd1a8688dcbce03c04`.
The later default-upgrade run retains all three passing cases and their raw
console output against the final structural-only schema-3 guard.

[The initial full source regression](development/source-regression-initial.log)
ran 1,207 tests and reported 50 failures, two errors, and 27 skips. It is a
failed development run, not a qualification result. Ownership code changed
while that run was active, so its parent/child transaction observations cannot
qualify a single source snapshot. The raw failures are retained.

Two ordinary-upgrade regressions found by that run were repaired: an older
installation may add its missing host adapter, and customized managed skills
remain reportable without overwriting them. Focused reruns passed. A further
regression proves that ordinary upgrade planning and application can repair a
missing managed retained file. Schema-3 structural validation does not replace
the installer's existing file-presence and customization handling.

The local AGENTS owner-region byte-budget failure came from CRLF checkout
transport. Restoring the exact committed LF bytes made the ten owner-region
tests pass without a Git content change. Command census/reference failures
required the supplemental applicability and scope reconciliation approved above.
Their implementation checks must pass; the original failures are retained and
are not waived by this index.

The local preliminary wheel comes from an uncommitted source snapshot. Its
candidate commit is explicitly unavailable, and its installed identity
diagnostic retains that limitation. Later source fixes are not present in that
wheel. Its archive-inventory checks and installed acceptance are development
evidence only; final CI must use the one wheel built from the committed candidate.

The frozen Windows/Python 3.13.3 package run completed normally: three archive
inventory checks, seven smoke cases, and 41 full cases in 1,707.375 seconds.
The full run has 40 passed case records and one unavailable case containing six
symlink subcases; the 85 exception and 67 precommit process-termination boundaries
passed. No timeout or residual candidate process was observed.

- [Preliminary package index and exact limitations](development/preliminary-package-evidence-index.json)
- [Original package observations archive](development/preliminary-package-raw-evidence.zip)

The archive contains 94 verified raw members and has SHA-256
`2a26d47f50d011fc2269d5850126ada3be429d9525d13fc251acea51fbe34585`.
It retains build commands, snapshot and artifact hashes, raw case evidence,
frozen test inputs, and identity diagnostics. It does not contain the virtual
environments or distribution bytes. The missing candidate-commit `RID015`
refusal remains a refusal; the separate installed-content identity check and
acceptance runs do not convert it into a qualification pass.

The original released-0.17.0 `init` probe incorrectly supplied `--apply`, an
option that command does not support. That observation establishes argument
refusal only. It is retained without being counted as a supported `init`
schema-4 refusal; a corrected focused probe must supply the actual writing
form. The other named probes and shared mutation-guard checks retain their
own observed meanings. The corrected focused record now proves that actual
released 0.17.0 reports unsupported lock schema through `doctor`, default-writing
`init`, and `upgrade`; the new ownership command is separately refused as unknown.

## Interpretation of case evidence

- API event exit codes are conventional mappings from the asserted result;
  actual CLI and worker events retain process return codes.
- The compatible-prior-upgrade fixture is independently constructed with a
  synthetic `0.18.0.dev0` identity. It tests the compatibility rule, not a second
  historical release wheel. Released 0.17.0 refusal is exercised separately.
- The binding checksum and recovery checksums provide consistency checking,
  not cryptographic owner authorization against a coherent full rewrite.
- Preserving an existing binding during an ordinary evaluator upgrade requires
  supported ownership format and unchanged retained catalog digests. Initial
  migration and explicit rebinding inspect the external assembly more strictly:
  its bundled evaluator version and payload must match the governing evaluator,
  together with archive identity when recorded. An older assembly may therefore
  remain bound after a compatible upgrade while being ineligible for a new
  binding until those checks pass. Neither case proves external availability.
- Before durable commit, recoverable interruption restores prior state. After
  durable commit, recovery finalizes the applied state. The evidence must
  distinguish both outcomes and retain observed stage names and recovery phase.
  These cases terminate an independent user process; they do not observe machine
  power loss. The implementation flushes file content and uses directory fsync
  on POSIX; its Windows directory-flush helper is explicitly a no-op.
- On a Windows runner without symlink privilege, those subcases remain
  unavailable; real junction and hardlink cases provide separately named linked
  path observations. An unavailable mechanism never counts as a passed refusal.

## Evidence byte transport

Raw hashes for retained development evidence refer to committed Git blob bytes
or the exact ZIP member bytes, not to a line-ending-converted checkout. The
nested evidence files were staged with conversion disabled and checked against
their observed bytes. Original archives and observations remain unchanged.

The supplement approval receipt's before/after hashes describe the Windows
working-copy bytes observed when the approved text was applied. The separate
[transport manifest](governance/implementation-byte-transport.json) maps those
observations and the other staged implementation files to their committed blob
hashes. Normal source/formal-document staging normalizes line endings; that is
a transport distinction, not another approval or an implementation result.

Evaluator evidence sidecars have their own strict contract: raw SHA-256 and
canonical serialized bytes must both match. These development transport notes
do not relax that contract.

## Completion boundary

Complete WO-PLG-020 only after its required observations pass and the released
evaluator confirms the delegated completion gate for the exact committed head.
Prepare VREC-PLG-015 afterward under its separate preparation right. Verification,
release, adoption, live WO-PLG-009 connection, and the accepted C10/C11 enforcement
limitation remain outside this implementation result.
