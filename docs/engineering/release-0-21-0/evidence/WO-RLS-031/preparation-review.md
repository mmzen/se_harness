# VREC-SEH-031 preparation review

VREC-SEH-031 is ready for human mmzen's assurance decision. It binds candidate
4031f0fa4b5c4a95651bd928a110d8b2d94f9775. The thirteen work orders exactly
match REL-SEH-033; contracts are VER-IAR-020, VER-IAR-021, VER-IAR-022 and
VER-RLS-030. WO-RLS-031 is implemented. No aggregate verification or release
decision is inferred from preparation.

## Results at the final candidate

| Check | Result |
| --- | --- |
| Windows source and graph | Pass in a clean temporary Python 3.14 environment; 1,215 full-scale tests, 21 skips. |
| Linux source and graph | Pass in a disposable exact-commit clone; 1,215 full-scale tests, two skips. |
| Distribution records | Pass on both platforms; 20 distribution-bearing records. |
| Pinned recipe | Two clean hosted builds produce identical wheel and sdist bytes at this exact commit. |
| Historical release replay | RLS-SEH-030 reproduced exactly at its recorded b9af631b850c495eace9807361ed3ec3e36a10b2 candidate. |
| Installed packages, resources, lifecycle and migration | Retained Windows/Linux checks and native observations pass for unchanged tested inputs. final-qualification.md documents the reuse comparison and limits. |
| PR CI | Candidate-head PR run passed validation, source/package, predecessor, both upgrade legs and both integration-package legs. Its merge checkout is distinguished from the exact-head manual rehearsal. |
| Verification transition gates | Pass under released evaluator 0.20.1. Record remains ready. |
| Codex Windows desktop | Unverified; limited deviation DEC-RLS-001 and risk RISK-RLS-001 accepted by mmzen. No desktop-support claim. |

The exact-head hosted run is
https://github.com/mmzen/se_harness/actions/runs/36964442551.
Its inert schema-2 manifest is final-build-manifest.json:

- Wheel SHA-256: 13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789
- Sdist SHA-256: f1db9d80acf8ee86ea53b53c64c0f4d25db6fd99c58f903dd841d13f95cca98b

This build identity is distinct from the earlier non-promotable test wheel.
The capture retained the actual hosted receipt in its command output. The
manifest and receipt here are later review companions, not files claimed to
have existed before their candidate was built. Human verification permits the
next release-record preparation step; tagged record binding and bound-record
replay still precede the separate release decision.

## Failures and corrections retained

The initial Linux clone could not use the Windows worktree's .git path.
A Git bundle supplied the exact commit. The bundle origin initially lacked
the canonical repository URL, causing one dashboard test failure; restoring
that URL in the disposable clone fixed the test. The --workers diagnostic was
an expected negative-test message, not the root failure. Distribution validation
then needed the separate historical 0.20.1 commit; importing its existing tag
bundle fixed that fixture input without changing candidate files.

The first Windows captures stopped at runtime identity: workstation Python
exposed an installed 0.15.0 distribution and enabled user site-packages. A clean
temporary environment passed the same identity check and full suite. No global
Python installation, real credentials or saved host settings were changed.
All observed refusals and retries are retained in final-hosted-receipt.json and
the generated capture output. No refused attempt created a verification record.

## Evidence and remaining human decision

Capture explicitly binds 89 evidence files, including the desktop decision,
risk and disposition; native traces; historical failures; and each member's
implementation evidence. All selected evidence digests remain unchanged.
The evaluator companion SHA-256 is
18b56762537c5fe223ee11f6cbc36ed445b69346394c54b176bc1e19f712dc26.
Capture arguments, exact record digest and gate results are in
capture-preparation.json. The generated VREC and companion are unchanged.

Next accountable decision: **I verify VREC-SEH-031 as assurance owner.**
The record also permits rejection or supersession through its returned procedures.
The desktop risk must be revisited before a subsequent release, a verified
support claim, or adoption relying on desktop replacement delivery. Marketplace
publication, latest/last markers and repository adoption remain separate.
