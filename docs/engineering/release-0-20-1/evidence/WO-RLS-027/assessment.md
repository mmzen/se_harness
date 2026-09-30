# WO-RLS-027 verification assessment

## Implementation evidence

The implementation candidate is 2f8e64fcede02240972881b942ccf411cf5fffc5.
The reviewed PR head is ee0c807f6f2c415d610bf6994dfd806a840284ff.
Their changes are retained evidence only. GitHub tested merge commit
79e773cbfcfe6469e125643236ed54378777a702, whose complete tree equals the PR head.
tests.json retains the local results and failures. hosted-ci.json retains actual
hosted results, artifact identities, the exact pinned replay and tree comparison.
No results from these commits are relabelled as a later commit.

| Criterion | Assessment and evidence |
| --- | --- |
| REQ-SHB-008 / RLS-COMPAT-001..003 | Pass: focused refusal tests and real installed-runner tests on Windows and Linux cover both layouts and all ten existing scenarios. The fixed minimal input matches VER-RLS-027's archive and payload identities. |
| REQ-REB-020 / RLS-COMPAT-004 | Pass for the retained local wheel: public 0.20.0 independently qualifies it on both platforms. The unreleased maintenance runner's assessment of the minimal wheel is labelled candidate-controlled. |
| REQ-REB-031 | Pass: the typed operation, scenario IDs and role boundaries remain unchanged. Focused identity/refusal tests, full suites and hosted qualification pass. |
| RLS-COMPAT-005 | Pass: Git comparison confirms no installer, integrity module, templates, plugin, selected root or CI changes. Only approved runner/tests/version/documentation and preparation material differ from the maintenance baseline. |
| REQ-RLO-018 | Pass for preparation: REL-SEH-032 and plan.json cover all five delivery surfaces with explicit downstream owners, actions and pending identities. No downstream publication is claimed. |
| REQ-RLO-020 | Pass: maintenance documentation distinguishes candidate preparation and historical observations from current public availability. Marketplace, demonstration and markers remain pending. |
| Source and package checks | Pass: 1,167 Windows tests (17 skips), 1,167 WSL tests (4 skips), and hosted full-scale Linux tests (2 skips). Both platform package matrices, legacy footprint, real predecessor upgrades, 115-entry sdist payload parity and distribution validation pass. Skips do not stand in for any required layout criterion. |
| Hosted integration | Pass: PR #508 harness, predecessor, candidate source/package, both upgrade and integration-package lanes pass. The irrelevant release-record rehearsal is skipped by the existing selector. |
| Pinned recipe | Pass at the exact CI merge commit: two identical wheel/sdist builds. Final verification will require a new replay for its own exact candidate; equal trees do not change commit identity. |

## Final verification preparation

Implementation completion records the executor's completed work. It does not
accept verification or authorize release. The final clean candidate will contain
this retained evidence and the completion event. Before capturing its VREC,
obtain CI and pinned recipe results for that exact candidate and rerun its source
tests through committed-candidate capture. Retain these later observations without
overwriting earlier runs. Compare all package-bearing inputs before reusing local
installed-wheel evidence; changed inputs require affected checks to run again.

The resulting VREC remains ready until human mmzen decides. Publication,
marketplace delivery, marker promotion and successor adoption remain separate.
