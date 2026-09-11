# Proposed extension: make the existing allocation test portable on Windows

**Pending engineering-owner and assurance-owner approval. Not implemented.**

The resolver repair passes 94 focused tests and the frozen incident replay on
Windows and Linux. The full Linux suite passes 1,142 tests with four skips.
The full Windows suite reaches the same 1,142 tests but fails one existing test:
`IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`.

That test deletes its temporary `.git` directory with `shutil.rmtree` to prove
allocation refuses a directory outside a checkout. On Windows, deletion fails
on a read-only Git object before the refusal assertion runs. The same failure
was reproduced in unchanged pre-repair checkout `e78d257a67c448ae54e12439e70925befcad3c20`.
This is a test setup defect, not evidence that the repaired resolver failed.
Its raw results remain in `local-results.json`.

## Exact proposed amendment

Add only `tests/test_artifact_authoring.py` to WO-RLO-009's execution scope.
Within the named test, replace deletion of `.git` with renaming that directory
inside the same disposable fixture. Remove the now-unused local `shutil`
import. Leave every assertion and product implementation unchanged.
The fixture then lacks `.git`, so the existing refusal assertion still tests
the same condition. Its registered `TemporaryDirectory.cleanup()` handles
final removal, including read-only entries.

Add DISC08 to VER-RLO-006: run the unchanged refusal assertions and both full
platform suites after this fixture-only correction; no new failure is accepted
or skipped. Retain the baseline failure and corrected results. Existing
DISC01–DISC07, historical-byte preservation, the archive limit and required
commit-bound verification remain unchanged.

Approval would authorize only this additional test setup correction and its
retained evidence. Completion, VREC preparation, assurance and merge remain
separate decisions. Without approval, the file and approved scope stay unchanged.
