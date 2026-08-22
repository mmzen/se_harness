# WO-REB-010 Git-aware candidate evidence

## Failure retained

Publication run `32595552589` passed released authority resolution, the exact predecessor publication view, and C6 complete validation at 645 artifacts with zero errors. In credential-free qualification job `97085818853`, the C6 suite then ran in an extracted tar archive with no Git metadata. Of 445 hosted tests, exactly two errored:

- `test_existing_managed_workflow_remains_byte_identical_to_head` could not execute `git show HEAD`;
- `test_manifest_producer_hashes_exact_files_and_candidate_tree` could not execute `git rev-parse HEAD`.

The remaining tests passed. Build, bundle transfer, GitHub Release, PyPI, Pages, maintenance, tag, root, and policy mutation jobs did not run.

## Correction boundary

Trusted main already has full credential-free history and the exact C6 commit resolved from released `RLS-SEH-012`. The workflow adds a detached temporary worktree at that commit for validation/tests/help/doctor. Its existing two `git archive` exports remain unchanged and remain the exclusive build inputs. No current-main file is overlaid on C6, and no publication credential is present.

Both exact failing tests pass in the existing detached C6 checkout.

## Exact corrective qualification

Corrective candidate `3a47e782d151ccc1708e34dd1a44afaa4bb8065e` contains exactly the trusted workflow worktree/cwd correction, its regression assertions, `WO-REB-010`, and this evidence. A clean exact-commit clone excluded the stopped untracked release record.

- the two exact C6 Git-provenance tests: passed;
- focused release workflow policy: 5 tests passed;
- complete release-orchestration module: 22 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 212.770 seconds;
- complete current graph: 657 artifacts, zero errors, 50 maintenance warnings;
- release-distribution validation: passed for exact `RLS-SEH-012` with one distribution-bearing record;
- portable release surface, diff whitespace, and clean-checkout checks: passed;
- build inputs remain the same two `git archive` exports; worktree content is used only for qualification;
- workflow permissions and privileged job dependencies remain unchanged.

At closeout no publication credential, GitHub Release, PyPI file, Pages deployment, maintenance mutation, tag movement, root mutation, distribution rebuild, rejected-history mutation, or external-policy change occurred. Work-order completion, later commit-bound VREC acceptance, trusted-main push, and publication retry remain separate governance actions.
