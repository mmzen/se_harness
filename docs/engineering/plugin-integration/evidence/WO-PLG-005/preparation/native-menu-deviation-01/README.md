# Native menu deviation, 2026-09-11

This is an incident observation, not an adapter acceptance result. Native acceptance remains paused. Candidate at the time: `ab8d6e20`; the working tree also contained the uncommitted `interactive.py` and `live.py` acceptance helpers. The existing authenticated disposable WO-PLG-003 profile was used normally; authentication content was neither read nor copied.

## Actual sequence

The following is an observer reconstruction from the terminal interaction, not a byte-for-byte terminal transcript. The retained machine observations below are separate evidence.

1. The owned helper `tests/plugin_integration/codex_adapter/interactive.py` launched accepted Codex 0.153.4 in PTY tool session `77504`, using the disposable profile and new fixture repository. Its argv requested `--sandbox read-only --ask-for-approval on-request`.
2. The operator-facing native UI was used to trust the new fixture repository and to review and trust the new plugin's two hook commands. The old probe's two hooks were explicitly disabled in the native hooks UI after observing that the attempted process-local plugin-disable override had not disabled them.
3. The agent sent Escape and then `/quit` plus Enter without inspecting the intermediate menu. The intermediate screen was the Windows sandbox setup prompt, whose default selection was “Set up default sandbox (requires Administrator permissions)”. Enter selected that setup option unintentionally. This was outside the authorized disposable adapter-installation operation.
4. The agent immediately sent Ctrl-C. The UI displayed “Shutting down...” and session identifier `01a091eb-9de0-7ce0-827f-858c9dcd1fee`. The agent did not accept an elevation request, retry setup, change a security setting intentionally, or perform a rollback. The displayed shutdown message does not prove process termination or absence of host changes.
5. The parent was informed and required native execution to remain paused. Empty PTY polls returned no additional output and still reported an active session. A default-sandbox `Get-CimInstance Win32_Process` read failed with Access denied. Narrow read-only inspection using approved `require_escalated` followed; it did not alter process state or security settings.
6. At `2026-09-11T19:26:23Z`, the specific Codex process PID 28204 was still present under the exact helper ancestry, with no active descendant reported. Its creation time was `2026-09-11T19:21:35.254216Z`. The helper Python processes and launching shell also remained active. Process presence contradicts any claim that Ctrl-C had already terminated the owned host.
7. The parent then explicitly authorized stopping only the owned test process after identity revalidation. At `2026-09-11T19:27:51Z`, every known ancestry PID was revalidated against its retained executable, command line, parent PID and creation time. Only Codex PID 28204 was terminated with `Stop-Process -Id 28204 -Force`. Two seconds later none of the known ancestry PIDs remained. The helper and shell exited without being directly terminated. PTY session 77504 completed with exit status 1. `termination.json` retains the exact revalidation and observation. No sandbox/security setting was changed by this containment operation.

## Observed effects and limits

`owned-processes.json` retains only the known acceptance ancestry and its active descendants. It does not enumerate unrelated processes, and cannot establish whether a short-lived or detached helper previously ran.

`disposable-sandbox-observation.json` records newly created `.sandbox` and `.sandbox-bin` directories in the named disposable `CODEX_HOME`, both created at approximately `2026-09-11T19:23:03Z`. Both were empty at inspection, including hidden entries. Thus setup-related filesystem activity occurred. The older `.sandbox_migration` file predates this incident. The only file in the named `log` directory was the earlier login log; its contents were not read. No setup log was found in those named sandbox directories. No rollout file matching the displayed session identifier was found in this disposable profile.

`disposable-config-after.toml` is the credential-free configuration as inspected after the incident. It records the intended repository trust, the two new trusted hooks, and the two disabled old probe hooks. It contains no Windows sandbox setting. This snapshot has no pre-incident byte snapshot paired with it and is not proof that other host state was unchanged.

No UAC or administrator approval was accepted by the agent. The available observations do **not** establish whether setup requested elevation, whether a setup helper previously exited, or whether an operating-system account, ACL, firewall, or other security state changed. Those questions remain unresolved; no absent-effect claim is made. No credentials, default Codex profile, account policy, or system-security configuration was inspected or changed during this follow-up inspection.

## Continuation boundary

Do not resume native acceptance, rerun setup, approve elevation, alter host security, or silently undo changes based on this record. The parent and independent reviewer must assess the concrete observations first. Future terminal navigation must send one navigation action and inspect the displayed screen before another command or confirmation.

The owned test process has now been stopped as described above. Static and focused non-host adapter work may continue under the parent's instruction; further native-host sessions remain paused.

No C01–C12 case passes because of this interaction. The six focused protocol tests and successful package/native-install preparation remain distinct from the incomplete live acceptance.
