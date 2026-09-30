# 0.20.1 compatibility implementation review

Human mmzen approved SPEC-RLS-001, VER-RLS-027, WO-RLS-027 and REL-SEH-032,
required commit-bound verification and the retained 0.19.0 role-label encoding.
The exact selected 0.19.0 evaluator applied approval and start in an isolated
maintenance checkout from 7253d13b212ad6f7df670021290fea32e81d66de.

The change reuses the existing acceptance runner and scenario IDs. It selects
the declared layout, checks the minimal default before adding Git integration,
binds that setup into init evidence and exercises managed customization and
payload corruption. Unknown/malformed layouts, extra files, failed setup and
missing managed blocks fail. Existing identity/isolation and refusal checks stay.
No new command, framework, resource resolver or installer behavior is added.
The baseline installer and templates are unchanged. Both version declarations
are 0.20.1; the repository remains governed by its baseline-selected 0.19.0.

The 16 focused tests pass. The full Windows suite passes 1167 tests with 17
reported skips. Its earlier failure was the newly added word 'governor' in the
development note, rejected by the existing retired-term check. The in-scope
documentation now says 'evaluator'; the failed result is preserved. Distribution
validation passes 16 records and formal validation has zero errors, 52 existing
warnings. The implementation diff and necessary refusal cases were reviewed
under the existing design-simplicity guidance.

The maintenance README distinguishes its new candidate from historical baseline
observations and links current-main instructions for current public availability.
The five-surface plan retains pending future identities and downstream work.
No public delivery or native desktop claim is added.

## Local package and Linux results

The exact tested source candidate is
`2f8e64fcede02240972881b942ccf411cf5fffc5`.
Its non-promotable wheel has SHA256
`ad8ebadcf65871a8925c4aad071d259f3155f0ece9cd830505b9b033db482258`.
The native build is test evidence, not the required pinned release build.

Windows and Linux each pass 16 installed-package operations. The installed
maintenance runner passes all ten existing scenarios against public 0.20.0 and
against the exact minimal wheel approved in VER-RLS-027. Its minimal-layout
assessment is candidate-controlled evidence. Separately, the exact public 0.20.0
verifier passes typed candidate-package qualification of the maintenance wheel
on both platforms with independence = released-verifier.

Fresh maintenance initialization has the same 59-file footprint as public 0.20.0.
Both platforms pass a real 0.19.0-to-0.20.1 upgrade and subsequent doctor checks.
The sdist builds back into a wheel with all 115 package/template entries equal
to the directly built wheel. The first sdist attempt hit a denied user pip cache;
rerunning with --no-cache-dir passed without changing permissions or source.

The Linux source suite passes 1167 tests with four skips at the exact candidate
commit. Its first run used an archive without Git metadata: ten errors and two
failures came from tests needing HEAD attributes or the repository origin.
An attempted repair found that the prior temporary directory no longer existed.
A fresh disposable shallow checkout was reconstructed from the exact Git commit
and tree, with the real origin. The full suite then passed. Both failed attempts
remain in tests.json; no product test or requirement was weakened.

A Git comparison confirms no changes to installer.py, integrity.py, packaged
templates, plugin source, installed root/configuration/lock or CI workflows.
The code change is confined to the existing candidate acceptance runner.

## Remaining work and requested external action

Hosted CI and the pinned recipe build have not run. The Docker client cannot
connect to a running Linux engine on this workstation. The existing publication
rehearsal is the documented build route in that condition. Required hosted
wheel/sdist and upgrade lanes remain part of the release checks.

The next requested authority is an ordinary push of work/compatibility-0-20-1
to mmzen/se_harness and a draft PR targeting release/0.20. The existing PR
workflow selects the candidate recipe build because build inputs changed.
If that does not provide the required run, the proposed fallback is dispatch
of publication-rehearsal.yml at the reviewed branch head. That workflow has
no mode input: dispatch selects the candidate build and an eligible existing
release-record rehearsal. Inspect its exact inputs and provider controls before
dispatch. These workflows have read-only permissions and do not publish.
No merge, publication or marker action is part of that request.

The final evidence commit changes only this review and tests.json. Local test
and package results remain bound to the source candidate named above. Hosted
checks must assess the subsequently published review head; the retained local
wheel is not claimed to have been built from that evidence commit.

WO-RLS-027 remains in_progress. No VREC or RLS has been prepared, no candidate
has received human verification, and no push or PR has occurred. After the
required hosted evidence passes, record implementation completion and prepare
the exact commit-bound verification record. Release and adoption stay separate.
