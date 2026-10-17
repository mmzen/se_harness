# Historical release rehearsal correction — implementation review

mmzen approved WO-RLS-055, required commit-bound verification and the exact linked
REL-SEH-036 amendment from review head 9c42b4d00e744bc1f3b2461a0819081141dd4c3b.
The evaluator recorded approval and start. The exact membership amendment is
applied; accepted bytes and lifecycle history remain preserved.

The correction is implemented, but **actual hosted rehearsal and final release
qualification remain pending**. WO-RLS-055 is in progress. No final verification
or release decision is claimed.

## Behavior and scope

The existing resolver has an explicit `--historical` mode for released-record
qualification. It requires the exact released record bytes at its integration
commit and keeps all existing plan, evidence, candidate, marketplace and recipe
checks. Documentation must match at its approved commit and release integration;
later main documentation may differ. The default live route still requires
current-main consistency. The production publisher workflow is unchanged.

Historical output uses a qualification-only schema. Only the two inert bundle
verifiers accept it; publication consumers refuse it. The read-only rehearsal
caller selects that mode and does not upload a publication bundle. The same
qualification/build sequence is reused. No additional service, formal artifact
type, publisher or policy copy was added.

This distinct output label is needed to prevent rehearsal output from being
mistaken for current delivery readiness. Adding a second build lane or disabling
the shared documentation guard would add cost or weaken publication checks.

## Observed local checks

- Affected resolver, delivery, CI and documentation suites: 141 tests, 1 skip,
  exit 0. Distribution validation and source CLI smoke check passed.
- Ordinary artifact validation passed: zero errors. Existing warnings remain.
- An intermediate actual RLS-SEH-033 historical resolution succeeded against
  unchanged origin/main and retained the released 0.22.1 candidate identity.
  It preceded the final record-byte guard; hosted qualification must exercise
  the final committed correction. It is not a final-candidate pass.
- Tests cover legitimate later documentation, changed plan/record/evidence,
  missing history and wrong candidate; bad integration documentation still
  fails. Publication consumers refuse qualification output before a write.
- Original failures remain retained. The first affected run had one assertion
  expecting a different refusal message; the input was already refused.
  A separate record-body regression then exposed missing exact-byte validation
  in historical mode; the new guard fixes it and the regression passes.

## Release limits and next work

Run both real publication rehearsal legs and complete-delivery/recovery tests.
Retain the exact candidate and CI subjects, then finish full required qualification
and handoff. Refresh final package/staging identities and assess input reuse
explicitly before preparing the aggregate VREC. Existing native source observations
remain at their original inputs; no new native or desktop result is inferred.

R23-NATIVE-010/011 stay open under DEC-RLS-010. Codex Windows desktop remains
unverified under DEC-RLS-011. This correction does not repair or retest those
findings. It grants no release, merge, public ref, provider-setting or host change.

initial-implementation-checks.zip retains actual commands, output, exits,
timings, approvals and failed observations. The evaluator refused an attempted
refresh of older WO-RLS-045 because WO-RLS-055 is the only active work order;
header-refresh-055.zip preserves its unchanged prior bytes. Only WO-RLS-055's
own packet was created. The complete PR check passed with the old packets
unchanged. Earlier records and archives remain unchanged.
