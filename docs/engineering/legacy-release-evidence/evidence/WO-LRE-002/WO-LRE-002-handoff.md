```toml
artifact = "WO-LRE-002"
checkpoint = "handoff"
formal_snapshot_sha256 = "bc29da1bbba18659d8bcb292a5ff6d73d695d7a107ccb467e466377a70677297"
rebound_at = "2026-08-31T09:01:17Z"
```

# WO-LRE-002 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

A released record carrying neither `evaluator_evidence_path` nor
`evaluator_evidence_sha256` is not assessed against the binding: no error,
no warning, no advisory, no declaration, no refusal. A partial binding is
still an error and a full binding keeps every check, including current-lock
matching for `ready` records. The 327-line package module, the template
validator's resolver and frozen six-identifier set, the per-record `W024`
debt warnings, the installer's pre-apply refusal and declaration write, and
the CLI plan-time notice are gone; `W024` is retired and stays reserved.
The `[evaluator_upgrade]` optional key remains accepted as inert data
(`REQ-LRE-003`; `LRE-FLR-001` to `LRE-FLR-007`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included. Its own validator keeps the resolver and its six `W024`
  warnings until the next root adoption.
- Candidate: this checkout, branch `wo/lre-002-evidence-floor` off `main`
  at `609cb254c05a042fcb28ea6e11f15f08c9337021` (the forward merge of pull requests #292, #295, #296 and
  #297, as the approval required).

## Change

- `se_harness/legacy_release_evidence.py` and
  `tests/fixtures/legacy_release_evidence/`: deleted.
- `se_harness/installer.py`: the transition-time enumeration and refusal,
  the `declared` evidence parameter and the declaration write are removed;
  the upgrade evidence JSON simply omits the key.
- `se_harness/cli.py`: `_report_undeclared_legacy_releases` and its
  planning-path call are removed.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  the constants block is replaced by the retirement comment reserving
  `W024`; the resolver family (`_legacy_declaration` through
  `validate_legacy_release_evidence_warnings`) is deleted; the binding gate
  is `required=not unbound` with unbound meaning both fields absent; the
  warnings wiring is removed.
- `.github/scripts/publish_dashboard.py`: the frozen set is deleted and a
  wholly unbound record publishes without evidence; a partial binding still
  refuses.
- `tests/test_legacy_release_evidence.py`: rewritten as the floor suite —
  unbound/partial/bound fixture rows, the inert-key row, the
  this-repository reading, the publication view, the deletion sweep and the
  no-declaration evidence row (10 tests).
- `tests/test_predecessor_bootstrap_retirement.py`: the root-versus-candidate
  validator ledger gains the WO-LRE-002 opcode table (30 opcodes, line
  delta -222 against the 0.11.0 root copy).
- `tests/test_dashboard_publication.py` and
  `tests/test_revision_provenance.py` (scope amendment of 2026-08-31):
  re-targeted from the wholly-unbound case to the partial-binding case.
- `docs/notes/harness-installation-and-upgrades.md`: the declaration
  section is restated as the floor; `docs/engineering/README.md`: the
  domain line restated.
- Amendment records on `REQ-LRE-001`, `REQ-LRE-002`, `SPEC-LRE-001` and
  `ADR-LRE-001`.

## Verification readings (VER-LRE-002)

- Floor suite: 10 tests OK. Affected suites
  (`test_predecessor_bootstrap_retirement`, `test_dashboard_publication`,
  `test_revision_provenance`, `test_legacy_release_evidence`): 91 tests
  OK.
- Full Windows suite: 1141 tests, 1 error — the known
  `test_artifact_authoring` temp-directory baseline — 26 Windows-only
  skips; at baseline.
- Template validator over this repository: `Artifacts: 1196 | Errors: 0 |
  Warnings: 63 | Advisories: 0` — exactly the six retired `W024` entries
  fewer than the 69 non-advisory warnings recorded under WO-AUT-004, and no
  `W024` anywhere.
- Released 0.11.0 evaluator: `doctor` 0 FAIL; `validate` 1196 artifacts,
  0 errors, 486 warnings (its own resolver still emits the six `W024`
  until the next root adoption); `validate_release_distributions` PASS
  (8 records).
- Deletion sweep over `se_harness/`, the template scripts,
  `.github/scripts/` and `repository_tools/`: zero hits for the module
  name, the frozen set, the declarer constant, hard-coded `RLS-SEH`
  identifiers and the `"W024"` literal; enforced by the sweep test. The
  root `scripts/` copies are the released evaluator's files and are not
  swept.
- The pull request's own lanes are the lane reading; recorded on the pull
  request when green.

## Material non-effects

The six pre-enforcement `RLS-SEH-*` records keep their bytes. The
partial-binding and full-binding failure paths are byte-for-byte today's
behavior. No hash-locked root file changed. The workflow gates forcing
evidence onto the path to `released` are untouched.
