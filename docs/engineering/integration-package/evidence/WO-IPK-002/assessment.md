# Integration archive capacity correction — local result

The approved three-line change raises the fixed source archive and expanded-file
budget from 512 MiB to 1 GiB. The implementation matches the reviewed diff exactly.
The 128 MiB member cap, 20,000-entry cap, path/link/duplicate checks, wheel budgets,
exact-commit export, two-build comparison and Windows/Linux verification stay unchanged.

WO-IPK-002 is in_progress; VER-IPK-002 is approved. Human mmzen's approval and required
assurance classification are recorded in the formal artifacts. Human verification
and merge remain separate. This result does not complete the work.

| Check | Result |
| --- | --- |
| Integration-package focused suite | 19 tests pass, no skips |
| Source suite | Ran 1339 tests in 196.273s (193 classes, 8 workers); OK (skipped=24) |
| Distribution check | pass |
| CLI smoke | pass |
| Released validation | zero errors; existing warnings retained in the exact result |
| Scope and review preflight | pass |
| Actual CI double build, Windows/Linux installation, retention | pending on the committed review candidate |

The original full-suite run and diagnostic reproduced a Windows Git filename-too-long
error in a disposable test fixture. The suite reran with process-local
core.longpaths=true; no persistent Git setting or source file was changed.
Both failures, the retry environment, prototype failures and original CI failure
remain alongside later results.
The previous native qualification evidence is unchanged. Claude's two focused
drafting failures and the HAG handoff blocker remain separate unfinished work.

The larger fixed bound increases worst-case temporary disk use. It does not
improve performance or solve indefinite evidence growth. Reusing the existing
builder and hostile-input tests avoids a new export mode or policy framework.
No historical evidence is deleted or excluded from the committed source archive.

Exact commands, outputs, exits, file identities and runtime are in local-checks.zip
with a hashed inventory. The local suite ran on the working implementation; the
following committed candidate and actual CI run must establish CAP3 before handoff
and verification preparation. Skipped or pending CI checks are not passes.
