# Plugin 0.2.3 qualification

WO-RLS-028 satisfies VER-RLS-028 for the locally assembled Windows packages.
The source remains `7ac05f25f008fa2e35ad1ae69ca3d84aa0c6ccab`; the release
revision is `489814dd15bff0b4f93151fab04acd69cec47d0c`. The latter supplies
the exact published, corrected RLS-SEH-030 record; no main plugin source is used.

| Criterion | Observed result |
| --- | --- |
| REQ-PLG-002 | Both manifests are 0.2.3. The unchanged public 0.20.1 wheel and shared assets match across hosts. Builder build/check pass. Eight acceptance cases include wrong-wheel and changed-inventory refusals. |
| Native installation | Fresh Codex CLI 0.159.2 and Claude Code 2.1.273 profiles pass discovery, setup, isolation, provider ownership and doctor. All 26 packaged files match on each host. |
| Native instruction delivery | Actual startup, manual compaction and resumed sessions pass on both hosts. Full delivered roots match the fixture files and hashes. Agent replies preserve the absence of implementation authority. Fixture files remain unchanged. |
| REQ-RLO-018 | The new delivery-plan-qualified.json preserves the earlier reviewed plan and adds source, package, prepared public revision and host content identities. Public-route observations remain assigned to WO-RLS-029. |
| Source and guidance | Only the two version fields and five approved guidance files differ among assembly inputs from the fixed public 0.2.2 baseline. Shared skills, hooks, setup, plan and builder remain identical. All 32 package/guidance tests pass, including context-appropriate link checks. |
| Distribution | The complete 63-file Git tree equals the checked distribution, with an ordinary parent equal to the observed public marketplace head. No marketplace publication occurred. |

## Review and limitations

The change uses the existing builder and native acceptance tools. No new product
mechanism, dependency or runtime behavior was added. The only earlier test issue
was a moved Codex executable; the failed invocation and the passing retry remain
retained. The isolated fixture setup needed normal-account access to the existing
authenticated disposable profile. No real host settings or credentials were changed.
Raw credential files and unfiltered debug logs are excluded from retained evidence.

Desktop and automatic compaction are unverified. Human assurance, source merge,
marketplace publication, public-route tests, moving markers and adoption remain
separate. Local qualification does not establish complete release delivery.
