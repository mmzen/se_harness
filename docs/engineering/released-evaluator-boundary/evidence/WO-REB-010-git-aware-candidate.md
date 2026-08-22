# WO-REB-010 Git-aware candidate evidence

## Failure retained

Publication run `32595552589` passed released authority resolution, the exact predecessor publication view, and C6 complete validation at 645 artifacts with zero errors. In credential-free qualification job `97085818853`, the C6 suite then ran in an extracted tar archive with no Git metadata. Of 445 hosted tests, exactly two errored:

- `test_existing_managed_workflow_remains_byte_identical_to_head` could not execute `git show HEAD`;
- `test_manifest_producer_hashes_exact_files_and_candidate_tree` could not execute `git rev-parse HEAD`.

The remaining tests passed. Build, bundle transfer, GitHub Release, PyPI, Pages, maintenance, tag, root, and policy mutation jobs did not run.

## Correction boundary

Trusted main already has full credential-free history and the exact C6 commit resolved from released `RLS-SEH-012`. The workflow adds a detached temporary worktree at that commit for validation/tests/help/doctor. Its existing two `git archive` exports remain unchanged and remain the exclusive build inputs. No current-main file is overlaid on C6, and no publication credential is present.

Both exact failing tests pass in the existing detached C6 checkout. Focused policy, complete exact-correction results, commit identity, and lifecycle closeout are added after the corrective candidate exists.
