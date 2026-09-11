# Native SessionStart trust review

The parent reviewed the literal commands and updater retained in `../package-03/`
and the bounded `interactive.py` helper before execution. Existing WO-PLG-005
authority covers installation and normal hook trust in this disposable profile;
this review did not grant Windows setup or security changes.

Native `plugin add` installed version `0.0.1+codex.20260911194142`; the command and
inventory are retained in `../native-update-02/`. The UI helper then launched the
fixed Codex 0.153.4 executable in read-only/on-request mode.

Observed navigation, with the screen inspected after every action:

1. Answer `y` to the terminal-capability warning.
2. Select **Review hooks** from the two-changed-hooks prompt.
3. Move from PreToolUse to SessionStart, one down-arrow action at a time.
4. Open SessionStart and select its second hook. The first, historical
   `codex-probe@codex-probe-local` hook remained disabled.
5. Inspect the selected source `verity-plane@verity-plane-codex-fixture`,
   synchronous mode, 30-second timeout and changed-command state; press `t`.
6. Observe **Trusted** and the enabled checkbox for that single hook.
7. Create the reviewed external stop marker from a separate shell. No Escape,
   `/quit`, menu-exit Enter, model prompt or Windows setup action was sent.

The helper's `outcome.json` records PID 4724, external-marker termination and
zero remaining active processes in its owned Windows Job Object. The PTY exited
0. Native startup also displayed an unavailable `codex_apps` MCP connection;
no connection settings were changed to resolve it.

This is preparation evidence, not C02 acceptance. A subsequently confirmed
incomplete-path guard defect requires new command bytes and a fresh package;
this trust observation does not qualify those future bytes. The earlier
preparation incident's unknown historical operating-system effects remain
unresolved.
