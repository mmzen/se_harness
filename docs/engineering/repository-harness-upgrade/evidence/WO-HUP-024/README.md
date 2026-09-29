# WO-HUP-024 adoption evidence

The approved adoption applies public SE Harness 0.20.0 from RLS-SEH-029.
CI selects 0.20.0 and development source is 0.21.0. The released installer
replaced the selected work-order template and reconciled its lock.

The upgrade transaction is [../WO-HUP-024-evaluator-upgrade.json](../WO-HUP-024-evaluator-upgrade.json).
[Preservation checks](preservation.json) compare tracked files with the
pre-upgrade state. AGENTS.md and the six old guide pointers retain their bytes;
CLAUDE.md remains absent. Pointer cleanup and native host configuration are separate.

Verification execution is in progress under VER-HUP-022. A candidate and a ready
VREC will be reported only after the required checks and preparation pass.
No human verification, push, PR, merge or publication has occurred in this work.
