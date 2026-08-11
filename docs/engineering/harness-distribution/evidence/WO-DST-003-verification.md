# Verification Evidence for WO-DST-003

Date: 2026-08-11

## Scope

Implemented the shared `AGENTS.md` contract for Claude Code through a bounded `CLAUDE.md` import, added a one-time repository-context seed with explicit repository ownership, extended doctor diagnostics, and updated the canonical template, packaging, self-installation, tests, acceptance scenarios, and documentation.

## Requirement mapping

- `REQ-DST-007`: `CLAUDE.md.fragment` maps to a preserved bounded block containing `@AGENTS.md`; doctor checks the import; tests cover init, adopt, malformed markers, old-installation upgrade, customization preservation, and missing import diagnostics.
- `REQ-DST-008`: `.seed` templates map to repository-owned files; the lock records `present` or `removed` without a content hash; tests cover first creation, pre-existing context preservation, old-installation upgrade, later customization, intentional removal, and missing-context diagnostics.

## Verification commands and results

### Artifact graph

```powershell
python scripts/validate_engineering_artifacts.py --root .
```

Result: PASS. 45 artifacts, 0 errors, 0 warnings.

### Automated and end-to-end tests

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Result: PASS. 29 tests run, 2 skipped because the Windows host did not grant symbolic-link creation privileges. Init and adopt targets validated and generated Harness Explorer successfully. The conditional symlink fail-closed cases remain implemented and execute on hosts that permit symlink creation.

### CLI surface

```powershell
python -m se_harness --help
```

Result: PASS. The existing single-profile command surface loaded successfully.

### Installed-harness diagnostics

```powershell
python -m se_harness doctor .
```

Result: PASS. Required instruction and context files, the Claude import, configuration, lock, and tracked managed hashes all passed.

### Self-installation upgrade

```powershell
python -m se_harness upgrade . --apply
```

Result: expected manual-review exit after safely updating `AGENTS.md` and adding `CLAUDE.md` plus repository context. Pre-existing customized `ENGINEERING_HARNESS.md`, engineering README, check scripts, and validator were preserved. Subsequent doctor diagnostics passed.

### Diff hygiene

```powershell
git -c safe.directory=C:/Users/mathi/RustroverProjects/se_harness diff --check
```

Result: PASS. Git emitted only the repository's existing Windows line-ending conversion notices.

## Deviations and residual risks

- Two symlink tests were not assessable on this Windows host because it lacks the required privilege; no new symlink behavior was introduced by this work order.
- A fresh context scaffold necessarily contains explicit `TODO` fields until a repository owner curates it. The file states that it is non-authoritative, and adoption reports make curation the first human decision.
- Doctor deliberately reports an intentionally removed context file while upgrade deliberately does not recreate it. This makes the ownership conflict visible without overwriting the repository's decision.

## Authority boundary

This evidence supports implementation review only. No verification approval, release authorization, commit, tag, push, package publication, or deployment was performed.
