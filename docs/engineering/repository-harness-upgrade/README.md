# Repository harness upgrade

This domain governs one standard-repository upgrade of the installed root evaluator from released bootstrap `se-harness==0.5.0a1` to independently published `se-harness==0.5.0`.

- `INT-HUP-001` through `VER-HUP-001` are approved, and `WO-HUP-001` is `implemented` with retained local evidence after successful start preflight, bounded apply, and HUP-only verification.
- The proposed operation uses the public 0.5.0 wheel outside the checkout and the ordinary `harnessctl upgrade` transaction.
- This packet does not change candidate product code, package version, release artifacts, tags, publication, issue #81, or the historical disposition of 0.5.0.
- Candidate commit, candidate-package and hosted acceptance, VREC preparation/transition, push, pull request, and merge remain separate decisions.
