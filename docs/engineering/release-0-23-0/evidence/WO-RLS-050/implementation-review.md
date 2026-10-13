# Content-readiness correction: implementation review

mmzen approved WO-RLS-050, required commit-bound verification, the exact linked
REL-SEH-036 membership amendment and review publication in PR #544 on 2026-10-13.
The released evaluator recorded that approval and Codex's start. WO-RLS-050 is
in progress. The exact reviewed product bytes are applied; native qualification
and human verification remain pending.

One shared instruction file now uses one content-readiness decision table at
the drafting step and in reporting. A missing required input leaves content
incomplete, even when a draft saves with no template errors. Repeated wording
was removed. This adds three words overall, no helper, dependency, tool call or
policy layer. Both host packages use the same existing map.

The explicitly approved manual REL-SEH-036 amendment adds only WO-RLS-050 to
its gates. The preceding accepted bytes and lifecycle history are preserved;
release-membership-amendment.json links the actual human decision and digests.

Existing resource, package-route/link and native-input/capture tests passed.
Their actual commands, outcomes and skips are in approved-correction-checks.zip.
These checks establish delivery and local behavior, not native content compliance.
Build the new exact package identities and assess one fresh Claude diagnostic.
Stop on failure under unchanged VER-HAG-008 and VER-RLS-040. All preceding failed
candidates remain unchanged, and desktop evidence stays separately pending.

Temporary runners use distinct candidate/output paths and fresh local sandbox
identities. They do not change the task, fixture, model, permissions or criteria.
No test-specific answer is added to agent input. No new native result is claimed.
