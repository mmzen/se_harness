# Proposed native update and hook review

This package was built and independently checked from committed source `c7d30a92dab5d3fb12c6e42fd3d8ae9ed6ce2163`. Its archive SHA-256 is `effa69a1eb7f50a7cb1eda38bd955083886a327b6d9b6eaa3c75e79068707a53`. Version `0.0.1+codex.20260911194142` comes from the Plugin Creator helper's default cachebuster after the disposable marketplace name was validated. This identifies a proposed native cache refresh, not a host/runtime upgrade. `package.json` records all payload bytes; `review-plan.json` records the exact native executable, argv, literal hook commands, command-text digests and external stop actions.

No source-marketplace update, native reinstall, hook-trust action, or UI launch has been performed for this package. The currently loaded cache remains the historical 0.0.1 payload observed in `C01/stale-inventory-02/`. A read-only app-server attempt must refuse that mismatch before thread/model work.

## Update source and argv for separate approval

`proposed-update.py.txt` is the complete proposed update source. If separately approved, the selected external evaluator Python would execute that exact source with `-I -B`. It checks that the new source and existing disposable marketplace tree match their retained inventories, that the file-name sets are identical, and that the selected native executable digest is unchanged. It copies only those existing payload file names into the source marketplace and invokes the accepted native `plugin add` and `plugin list` argv under the existing isolated profile environment. It never edits the native cache, credentials, default profile, marketplace metadata, or security settings. Its native argv are also present in `review-plan.json`.

If any prerequisite or CLI action fails, retain the attempted source/native state and stop. No automatic rollback or repeat is part of the proposal.

## One hook per bounded UI session

Each `trust_reviews` entry in `review-plan.json` is one proposed helper invocation. The helper is still unrun. It uses the existing Windows Job Object observer: the child is created suspended, assigned to its own kill-on-close job, then resumed. `interactive.py` immediately protects that process with cleanup and records its PID. It polls a fresh, exact external stop marker every 50 ms and has a fixed 180-second deadline. Either condition terminates only that owned job and records the cleanup result. The unit test covers those two cleanup branches; it does not claim a real UI stop has already been observed.

For each separately approved session:

1. Launch the exact helper argv in a PTY for one named hook and inspect the displayed screen. Do not infer the next screen from a prior session.
2. Send one navigation action and inspect its returned screen before sending another. Only the named Verity Plane hook's reviewed command may receive trust. An unexpected prompt, including Windows sandbox setup or elevation, requires the external stop action immediately; do not confirm or navigate through it.
3. Immediately after the single trust action, use that entry's `external_stop_powershell` from a separate shell. Do not send Escape, `/quit`, Enter, or another UI command to exit the menu.
4. Confirm the helper's owned-job cleanup says zero active processes and that the PTY completed. If it does not, inspect the exact recorded PID/ancestry before further action. Never kill by process name or change sandbox/security settings.
5. Start a new bounded session only for the other named hook after the first process is confirmed stopped. Native read-only hooks inventory must then show the exact new command and source identities, trusted/enabled and synchronous, before any C02 thread work.

No step in this proposal resolves or waives the earlier incident's unknown historical operating-system effects. The proposed trust sequence authorizes no setup, model work, governed edit, permission expansion, or security configuration change.
