```toml
artifact = "WO-HUP-012"
checkpoint = "handoff"
formal_snapshot_sha256 = "2bf3d6ee8478ae6289b485397955e7ed8a10c3c656d313526277e8abccd339ba"
rebound_at = "2026-08-30T19:44:16Z"
```

# WO-HUP-012 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Schema 3 is the only lock schema the harness reads or writes. A schema-1 or
schema-2 lock fails at read, before any write, with one diagnostic: "lock
schema N predates the supported floor (schema 3); remove the stale
.engineering-harness.lock and re-adopt the repository with harnessctl
adopt". Doctor renders it as one failing `lock-schema` check (exit 1);
upgrade plan and apply refuse (exit 2) and leave the tree byte-identical.
The installer's schema-1 preservation branch, the legacy digest machinery
and the four-way match labels are deleted; the hash-bound match vocabulary
is binary; `MG002` is retired and reserved; the transition assessment
script accepts schema 3 only (`REQ-HUP-024`; `HUP-LSF-001` to
`HUP-LSF-008`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included. Its own read paths keep the pre-floor behavior until the next
  root adoption.
- Candidate: this checkout, branch `wo/hup-012-lock-floor` off `main` at
  `7cac025b7b38b9a62973ee72cbf8292b4e96a846`.

## Change

- `se_harness/integrity.py`: `validate_lock` refuses schema 1 and 2 with
  the floor diagnostic and accepts 3 only; `LEGACY_CANONICAL_LOCK_SCHEMA`,
  `matches_legacy_newline_variant`, `legacy_tracked_sha256` and
  `digest_for_schema` are deleted; `compare_lock_entry` returns canonical
  or mismatch and takes no desired parameter.
- `se_harness/installer.py`: the retained schema-1 `sha256` helper, the
  seed-migration and leaving-set legacy acceptance branches and the
  schema-1 output branch are deleted; the absent-lock sentinel and the
  emitted lock are schema 3; the digest is `canonical_sha256`.
- `se_harness/preflight.py`: the `legacy exact` and `legacy canonical
  match` renderings are gone; a pre-3 lock surfaces as the failing
  `lock-schema` check.
- `se_harness/mutation_guard.py`: the ordinary-mutation schema condition
  is deleted; a pre-3 lock fails at read as `MG001`; `MG002` stays
  reserved with a comment naming this work order.
- `se_harness/hash_bound.py`: `MATCH_LEGACY_NEWLINE` and its acceptance
  are deleted; `MATCH_RESULTS` is (declared, mismatch).
- `scripts/validate_governor_transition.py`: lock schema must be 3.
- Tests: `test_harnessctl` gains the pre-3 refusal test with a
  byte-identical snapshot, the remove-and-readopt route test and the
  deletion sweep over `se_harness/`, `scripts/` and `repository_tools/`;
  `test_mutation_guard` asserts the floor message under `MG001`;
  `test_hash_bound_integrity` replaces the newline-recognition tests with
  retirement tests (the recorded historical digest stays on disk and no
  longer matches); `test_instruction_architecture`'s schema-1 half asserts
  the refusal.
- `docs/notes/harness-installation-and-upgrades.md`: the schema paragraphs
  state the floor and the re-adoption route.
- Amendment records on `REQ-PMI-004`, `SPEC-PMI-001` and `ADR-PMI-001`;
  the domain README carries the packet paragraph.

## Verification readings (VER-HUP-012)

- Affected suites: `test_harnessctl`, `test_mutation_guard`,
  `test_hash_bound_integrity`, `test_instruction_architecture` — 164
  tests OK (2 skips: one pre-existing, one revision-availability guard).
- Full Windows suite: 1150 tests, 1 error — the known
  `test_artifact_authoring` temp-directory baseline — 26 Windows-only
  skips; at baseline.
- Deletion sweep over `se_harness/`, `scripts/`, `repository_tools/`:
  zero hits for every deleted symbol and label; enforced by the new test.
- Released 0.11.0 evaluator: `doctor` 0 FAIL; `validate` 1177 artifacts,
  0 errors, 486 warnings (the pre-existing flood plus the root validator
  counting the new requirement's two-clause statement advisory);
  `validate_release_distributions` PASS (8 records); graph validator exit
  0.
- The pull request's own lanes are the lane reading; recorded on the pull
  request when green.

## Material non-effects

Schema-3 semantics, the lock writer's format and the evaluator identity
block are unchanged. `se_harness/release_qualification.py` is untouched.
No hash-locked root file changed. Retained evidence recording
schema-1-era digests is unchanged; the historical
`prior_lock_sha256` stays on its work order as data.
