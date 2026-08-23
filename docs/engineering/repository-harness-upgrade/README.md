# Repository harness upgrade

This domain governs separately authorized standard-root evaluator upgrades using exact immutable public releases.

- `INT-HUP-001` through `VER-HUP-001` are approved, and `WO-HUP-001` is `implemented` with retained local evidence after successful start preflight, bounded apply, and HUP-only verification.
- That first transaction moved the root from released bootstrap `se-harness==0.5.0a1` to exact public `se-harness==0.5.0`.
- `INT-HUP-002` through `VER-HUP-002` are approved, and `WO-HUP-002` is `in_progress`. Its bounded transaction has installed exact public `se-harness==0.6.0` and retained canonical evaluator-upgrade evidence; local source regression still has unresolved pre-upgrade expectation failures.
- Neither transaction changes candidate product code, package version, release artifacts, tags, publication, deployment, maintenance state, or historical lifecycle records.
- Work-order completion, candidate commit, VREC preparation or transition, push, pull request, and merge remain separate decisions.
