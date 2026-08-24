# WO-HBI-002 Verification Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation and local-qualification
evidence. This file does not approve an artifact, authorize a diff, verify work,
release, publish, deploy, or authorize a push or pull request, and it does not
grant the scope amendment it records. It records what was measured on one Windows
workstation at one working-tree state.

Work order: `WO-HBI-002`, assurance classification `commit_bound_verification =
"required"` decided by the engineering owner. Because verification must bind an
exact candidate commit, the figures below describe the working tree that became
the candidate commit. A file cannot contain the hash of its own commit, so the
candidate commit is named by the later `VREC` and not here. That `VREC` is a
separate, separately authorized act, is not prepared here, and must re-measure
its own figures.

## Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Python | 3.14.6 |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\se_harness_explore_921` |
| Branch | `feat/hbi-002-declared-hash-modes` |
| Base commit | `3de5075b43b3869e8030f1b01e2f9d1c4638cbd8` (the two lifecycle transitions) |
| `core.autocrlf` in the checkout | `true` |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, outside the checkout |

Linux was not exercised. Only the Windows lane is measured here; the Linux lane
is a hosted check that runs only after separately authorized pull-request
creation, and no such authority was given.

## Changed paths

```text
 docs/engineering/hash-bound-integrity/work-orders/WO-HBI-002.md |  48 +-
 repository_tools/release_bootstrap.py                           |  30 +-
 se_harness/candidate_acceptance.py                              |   9 +-
 se_harness/hash_bound.py                                        |  61 ++-
 se_harness/installer.py                                         |   5 +
 se_harness/mutation_guard.py                                    |   5 +-
 se_harness/upgrade_authorization.py                             |  20 +-
 tests/test_hash_bound_integrity.py                              | 491 +++++
 tests/test_mutation_guard.py                                    | 167 ++++-
 9 files changed, 813 insertions(+), 23 deletions(-)
```

Every path lies inside the work order's `[execution_scope]`, including
`se_harness/installer.py`, which the owner added by the amendment recorded below.
This evidence file is a tenth path, also in scope under
`docs/engineering/hash-bound-integrity/`.
`tests/test_release_bootstrap.py`, `tests/test_governor_transition.py` and
`tests/fixtures/hash_bound/` are in scope and were left unchanged: the bootstrap
and transition callers are exercised from
`tests/test_hash_bound_integrity.py`, where the cross-caller assertions belong
together.

## The mode arbiter

`se_harness/hash_bound.py` gained one query and two comparisons built on it:

- `resolve_mode(relative)` returns the mode the path's declared class fixes. It
  is total or failing: an undeclared path raises `HashBoundError` naming the
  path rather than resolving to a default.
- `declared_digest(relative, value)` hashes under that mode.
- `compare_declared_digest(relative, value, expected)` returns exactly one of
  `declared`, `legacy-newline-variant` or `mismatch`.

Measured directly:

| Path | Resolved mode |
|---|---|
| `.engineering-harness.lock` | `utf8-text-lf-v1` |
| `docs/engineering/**/evidence/*.json` | `raw` |
| `se_harness/governance_migration*.py` | `raw` |
| `tests/fixtures/governance_migration/*.json` | `raw` |
| `README.md` | refusal: `no declared hash-bound class covers README.md` |

Undecodable bytes fail closed in a canonical class
(`cannot hash .engineering-harness.lock as utf8-text-lf-v1: managed text must be
valid UTF-8`) and hash normally in a raw class, which binds bytes and never
decodes them.

## The lock's divergence, before and after

The lock's two callers hashed the same file under two rules. Measured over the
historical lock blob at `842ad90869ac153dc7aa407611992f066de78dd5` (5490 bytes,
no CR) against `WO-HUP-002`'s recorded
`prior_lock_sha256 = c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`:

| Materialization | raw SHA-256 | canonical SHA-256 | before (raw rule) | after (declared mode) |
|---|---|---|---|---|
| LF | `08441ec0…7443b3` | `08441ec0…7443b3` | refusal | `legacy-newline-variant` |
| CRLF | `c4c41919…3989af` | `08441ec0…7443b3` | match | `legacy-newline-variant` |

That is the defect in one row pair: the recorded digest is the CRLF
materialization of an LF blob, so the upgrade was authorized from a Windows
checkout and the identical repository state was refused on LF. After the change
both materializations reach one verdict, and that verdict is named rather than
silent.

The same convergence measured over the lock as this checkout materializes it
(6343 bytes, 159 CR bytes on disk):

| Materialization | raw SHA-256 | declared digest |
|---|---|---|
| LF | `abcb1fe7…3bf3f79` | `abcb1fe7…3bf3f79` |
| CRLF | `978cebb7…2b79e` | `abcb1fe7…3bf3f79` |

## Nothing recorded was changed

`git diff` over `docs/` shows no added or removed line containing a `_sha256`
field, and `docs/engineering/repository-harness-upgrade/` has no modified path.
`WO-HUP-002`'s `prior_lock_sha256` is exactly as recorded, and a test asserts
that literal against the artifact on disk. Legacy recognition — not a rewrite —
is what keeps that record readable, as `SPEC-HBI-001` rule 11 requires.

## Callers

| Caller | Change |
|---|---|
| `se_harness/upgrade_authorization.py` | Compares through the arbiter; `import hashlib` removed; the dataclass gained `prior_lock_match`; the existing refusal message is byte-for-byte unchanged. |
| `se_harness/mutation_guard.py` | Supplies the declared path's exact bytes from `LOCK_RELATIVE` and chooses no mode. |
| `repository_tools/release_bootstrap.py` | Compares through the arbiter; the byte-order-mark refusal is retained; a legacy newline variant is a distinct refusal, because `from_lock_sha256` was canonical from the start, so a variant there indicates a defect rather than history. |
| `se_harness/candidate_acceptance.py` | Its lock write now names `newline="\n"`. |

`_canonical_utf8_text_lf` is retained in `release_bootstrap`: it still serves the
history-artifact callers in `predecessor_preparation.py` and
`predecessor_publication.py`, which are not lock callers. Only the lock's own
comparison moved to the declaration.

The preparation view reports `contract.from_lock_sha256` rather than a recomputed
value, so `preparation_view_evidence_sha256` cannot move as a result of this
change.

## Mode divergence is detected, in both configurations

Two tests replace the declaration with one whose `standard-lock` class is `raw`
and assert that both callers follow it: the LF bytes still authorize and the CRLF
bytes are refused. Under the real declaration the verdict is the opposite for
CRLF. A caller that kept a canonicalization of its own would pass one
configuration and fail the other, so the pair is what detects divergence rather
than merely asserting today's mode.

## Producer newlines

Audited every `write_text(` and `open(..., "w")` in `se_harness`,
`repository_tools` and `scripts`. One text write names a lock path:
`se_harness/candidate_acceptance.py:387`, which now passes `newline="\n"`. The
installer writes the lock as explicit LF bytes
(`json.dumps(...) + "\n").encode("utf-8")` into `_atomic_write`), and
`provenance.py` already declared its newline; the remaining producers open in
`"wb"`. A static test now fails any future text write whose receiver names a lock
without declaring its newline, and a functional test runs `init` on this
CRLF-default platform and asserts the written lock carries no CR and that its raw
and declared digests therefore coincide.

## Gate results

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 584 tests, 1 failure, 10 skipped, 278.5s |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS — 720 artifacts, 0 errors, 50 warnings (all maintenance-plane) |
| `python scripts/validate_release_distributions.py --root .` | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | exit 0 |
| governing `validate .` (0.6.0, outside the checkout) | PASS — 720 artifacts, 0 errors, 50 warnings |
| governing `doctor .` (0.6.0, outside the checkout) | exit 0 — 87 PASS, 0 FAIL |
| governing `preflight . --work-order WO-HBI-002 --phase review` | PASS |
| in-tree `python -m se_harness doctor .` | exit 1 — 86 PASS, 4 FAIL (candidate-versus-released skew) |

The in-tree `doctor` FAILs are `.gitattributes`, `docs/engineering/WORKFLOW.json`,
`docs/engineering/WORKFLOW.md` and `scripts/validate_engineering_artifacts.py`
differing from the candidate distribution template. None of those four paths is
touched by this change, and the governing run from outside the checkout is clean,
so this is the documented candidate-source boundary rather than a regression. It
is not authorization to overwrite a root managed file.

The suite baseline at `main`'s `d07523f` is 555 tests with 10 skipped, so this
adds 29 tests and no skip. The skips are Windows-only guards. Both the
in-tree and the governing figures — 720 artifacts, 0 errors, 50 warnings — are
identical to `main` at `d07523f`, and the warnings are all maintenance-plane and
pre-existing.

### The one failure is pre-existing and belongs to another work order

`tests.test_hash_bound_integrity.DeclarationShapeTests.test_declaration_is_data_only`
fails on `self.assertNotIn(b"\r", raw)`: `core.autocrlf=true` materialized
`se_harness/hash_bound_classes.json` with CRLF, and the assertion reads the
worktree rather than the committed blob. It reproduces on `main` at `d07523f`
unchanged and is not caused by anything here. The fix is `WO-HBI-003`, which the
owner has not approved, and folding it in would defeat the deliberate split
between a read-only assessment change and an authorization change. Until that
work order is approved and merged, `main` stays red on Windows.

## Disclosures

- `scripts/validate_engineering_artifacts.py:884` still chooses the canonical
  mode locally for the lock. It is a root managed file and explicitly outside
  this work order's execution scope, so it was not edited. Its choice agrees
  with the declared mode today, so no behaviour differs; the coupling is
  undeclared rather than wrong.
- `LOCK_RELATIVE` in `se_harness/hash_bound.py` duplicates
  `se_harness/installer.py`'s `LOCK_NAME`. `installer.py` is outside the
  execution scope, so the two cannot be unified here. A test asserts they are
  equal, so drift fails rather than passing silently.
- `scripts/validate_governor_transition.py` records
  `lock_materialization_sha256` with `git`, `lf` and `crlf` variants and accepts
  `prior_lock_sha256` matching any of them. That permissiveness was a workaround
  for exactly this defect and is now redundant, but the script is outside the
  execution scope, so it was left alone. It is not wrong today: a declared
  canonical digest is one of the values it accepts.
- The two tests that read the historical lock blob skip when the object is
  absent, which a depth-1 CI checkout produces. The artifact-only assertions and
  the synthetic legacy case run unconditionally.
- The fresh-CRLF-clone measurement was not taken here: a clone materializes the
  committed tree, and the figures above describe the working tree that became
  the candidate commit. It belongs to the separately authorized verification of
  that commit, and it will surface the `WO-HBI-003` failure above.

## Scope amendment, granted and applied

`VER-HBI-001` acceptance scenario 5 requires that an upgrade authorization which
succeeded before the mode change still succeeds afterwards **and that the report
states a legacy newline variant matched**. The only reporting surface is
`_upgrade_evidence_bytes` in `se_harness/installer.py`, which was outside the
original execution scope, so implementation stopped and the owner was asked.

The engineering owner granted a bounded amendment on 2026-08-24, recorded in
`WO-HBI-002`'s own `## Scope amendment` section and by adding
`se_harness/installer.py` to `[execution_scope]`. The amendment authorizes one
key and nothing else. Applied:

```python
"prior": {
    "lock_sha256": authorization.prior_lock_sha256,
    "lock_match": authorization.prior_lock_match,
    "tool_version": old_lock.get("tool_version"),
    "evaluator": old_lock.get("evaluator"),
},
```

That is the whole diff in that file: five added lines, four of them the comment
explaining why the key exists. `prior_lock_match` was already carried on
`UpgradeAuthorization`, so no other behaviour changed.

Acceptance scenario 5 is now covered end to end by
`tests.test_mutation_guard.MutationGuardTests.test_a_legacy_recorded_prior_lock_still_applies_and_is_reported`:
an upgrade packet recording the raw digest of a CRLF materialization of the
repository's own LF lock still applies, the lock reaches the target evaluator,
and the written evidence reports
`"prior": {"lock_match": "legacy-newline-variant", ...}`. The companion test on
the ordinary path asserts `"declared"`, so the two are distinguished in the
report and not merely in memory.

Nothing validates the `"prior"` object against a closed key set:
`scripts/validate_governor_transition.py` reads `prior["lock_sha256"]` by name
and `tests/test_governor_transition.py` builds its own fixture dict, so the added
key breaks neither. No previously written evidence file was rewritten, so no
recorded evidence digest moved.

## Actions not performed

One candidate commit was made on `feat/hbi-002-declared-hash-modes` on the
owner's explicit authority, given on 2026-08-24. Beyond that: no branch push, no
pull request, no merge, no `VREC` or `RLS`
preparation or transition, no tag, no publication, no deployment, no credential
use, no maintenance mutation, no operational governor adoption, no release
distribution build, no root managed file overwritten, no historical digest
rewritten, and no edit outside the execution scope. The manual acceptances
`VER-HBI-001` requires from the security, quality and repository owners remain
outstanding and are not recorded here.
