# Missing domain parents: implementation review

Human mmzen approved WO-IAR-037 and required commit-bound verification in
VREC-IAR-020. Released evaluator 0.20.0 applied approval and start.

The scaffold planner now includes missing docs and docs/engineering parents.
It validates, previews and creates the same ordered directory list. The existing
rollback list removes only newly created empty directories after a failed write.
Existing parent directories and owner files remain unchanged. Initialization
still writes only the selection files; a preview creates no directory.

The source correction adds no command, dependency or framework. It reuses path
validation, resource identity checks, mutation authority and the atomic writer.
Tests cover the real missing-parent regression, preview/apply agreement, repeat
with an owner-edited index, a parent file conflict, symlink refusal where the
host permits it, and rollback with both absent and pre-existing parents.

The focused resource/authoring/mutation group passed 53 tests with three skips.
The stable integrated suite passed 1205 tests with 20 skips. These skips include
Windows symlink privileges; actual Linux link checks remain part of package
qualification. Distribution validation passed all 18 distribution-bearing
records. Formal validation reported zero errors and 54 existing warnings.
Earlier failing runs remain retained under WO-IAR-035 and WO-IAR-036.

The next evidence stage builds a non-promotable wheel from a local exact commit
and checks actual installation on Windows and Linux. Full integrated handoff,
native evidence assessment and VREC-IAR-020 preparation are still outstanding.
This review records no human verification, release or publication decision.

## Installed candidate follow-up

Local commit 6dd70f29cd43ffc230779d61ee1a7ced43a7a611 contains the approved
implementation and retained source-test evidence. No push occurred. A complete
non-promotable wheel was built from its Git export, not a dirty source copy.
Its SHA256 is e518c10d0fe34ae8d2864d7af5ecef0f84e0b94fe4c90afccc4f2d407b791f3b.

Actual installed-wheel checks passed: 13 command steps on Windows and 14 on
Ubuntu WSL. They cover exact resource identity, the two-file default, empty
validation, repeat initialization, domain preview/apply, owner-index preservation,
draft creation from the package and parent-path refusals. Linux also exercised
the real symlink boundary; Windows could not create that test symlink.

Two initial Linux setup attempts could not read the build output because of host
file permissions. The exact wheel and test inputs were transferred through stdin
to private Linux temporary storage. The successful check independently verifies
the wheel digest and selected resource identity. No workstation ACL was changed.

These results resolve the domain-creation defect. Integrated verification remains
pending. The separate released-verifier compatibility reproduction and proposed
sequence are recorded in WO-IAR-030/compatibility-check.json and DEC-IAR-004.
Native evidence still requires its final integrated assessment. This is not a
claim that VREC-IAR-020 is ready or that the work order transitioned to implemented.
